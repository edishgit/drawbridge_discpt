# Drawbridge — Implementation Handbook
### Everything needed to build, ship, and win · All Things Agentic Hackathon (Fortified Enterprise Fleet)
**Owner:** Ambrstack (solo) · **Window:** 11 Aug – 1 Sept 2026 · **Companion docs:** `drawbridge-hackathon-master-doc.md` (strategy, evidence, demo script), `drawbridge-architecture-doc.md` (diagrams, repo tree, decision log)

---

## 0. How to use this handbook

Sections 1–7 are foundations you build once and stop thinking about. Sections 8–14 are the fleet itself, agent by agent. Sections 15–20 are the parts that actually win the prize: deployment, cost, observability, the demo, and the content package. Section 21 is the master checklist — phase by phase, every item from environment setup to the last social post.

Code in this document is **reference implementation sketch**, not final code: it fixes the shape, the contracts, and the failure semantics so that when you (or Claude Code) write the real thing, the hard decisions are already made. Where the ADK or GEAP API surface differs from what's written here, keep the *contract* and adapt the call — the contracts are what the architecture story rests on.

**The one rule that governs every decision below:** if a feature does not appear in the four-minute video, in the README spin-up, or in the architecture diagram, it does not get built.

---

## 1. Environment and prerequisites

### 1.1 Local machine setup (Day 1, ~90 minutes)

| Item | Version / choice | Note |
|---|---|---|
| Python | 3.11 or 3.12 | ADK targets modern Python; avoid 3.13 edge cases during a hackathon |
| Node | 20 LTS | Next.js 14+ frontends |
| gcloud CLI | latest | `gcloud components update` before starting |
| Docker | latest | Cloud Run local builds and container parity |
| uv or venv | either | pick one and never mix |
| OBS Studio | latest | install on Day 1, not Day 28 — you'll test recording early |
| GitHub CLI | optional | speeds repo/release work |

```bash
# one-time local bootstrap
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install google-adk google-cloud-firestore google-cloud-pubsub \
            google-cloud-storage google-cloud-trace opentelemetry-sdk \
            opentelemetry-exporter-gcp-trace pydantic pytest python-dotenv
gcloud auth login
gcloud auth application-default login
```

### 1.2 Google Cloud account posture

Create a **dedicated project** (`drawbridge-hack`) — never build this inside an existing project, because you need to screenshot the console with only your resources visible, and teardown must be surgical. Enable billing, apply the $150 hackathon credits, and set the budget alerts *before* the first API call (§18).

```bash
export PROJECT_ID=drawbridge-hack
export REGION=us-central1          # pick the region with the widest GEAP availability
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud services enable \
  aiplatform.googleapis.com run.googleapis.com pubsub.googleapis.com \
  firestore.googleapis.com storage.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com \
  cloudtrace.googleapis.com logging.googleapis.com modelarmor.googleapis.com
```

**Day-1 non-negotiable:** deploy a hello-world agent to Agent Engine and a hello-world service to Cloud Run *before writing any product code*. Platform friction is the number-one schedule risk in this project; it must surface on Day 1 when you have 20 days of slack, not on Day 19 when you have none. If a GEAP component turns out to be gated or unavailable in your region, you learn it now and take the interface-fallback path in §20.2.

### 1.3 Region and quota notes

Pick one region and stay in it for Agent Engine, Cloud Run, Firestore, Storage, and Pub/Sub. Cross-region calls add latency that shows up in your demo and cost you nothing but grief. Record the region in `.env.example` and the README so a judge reproducing the project doesn't hit a "resource not available" wall.

---

## 2. Repository conventions

### 2.1 Git discipline

Public repo from day one (not private-then-flipped — the commit history showing three weeks of steady work *is* evidence the project was built in the contest window, which the rules require). Commit at least twice a day with meaningful messages. Tag milestones: `v0.1-spine`, `v0.2-armor`, `v0.3-binder`, `v1.0-submission`.

```
feat(evidence): cross-examine questionnaire claims against SOC 2 exceptions
fix(gateway): reject unstamped content before model dispatch
docs(readme): 30-minute spin-up path with synthetic seed
```

### 2.2 Code conventions

- **Everything typed.** Pydantic models for every event, document, and tool payload. Judges skim code; typed contracts read as engineering maturity, and they make Claude Code far more accurate when generating the implementations.
- **Every agent module exposes the same four things:** `agent` (the ADK agent object), `TOOLS` (list), `handle_event(event)` (the Pub/Sub entrypoint), `SERVICE_ACCOUNT` (documented identity).
- **No tool calls outside the gateway.** If a module imports an SDK client directly for an external effect, that's a bug — route it through `shared/gateway.py`. This is what makes the security claim true rather than decorative.
- **No secrets in code, ever.** `.env.example` documents keys; Secret Manager holds values.
- **Failure semantics documented per agent** in a module docstring: what it does when input is malformed, when a model call fails, when a dependency is unavailable. This docstring is quotable in the Devpost writeup.

### 2.3 The Makefile is the product's front door

```make
bootstrap:      ## enable APIs, create topics, buckets, firestore, IAM
	./infra/bootstrap.sh
seed:           ## load synthetic vendors into Firestore + Storage
	python -m scenarios.seed
run-local:      ## ADK dev UI against local emulators where possible
	adk web agents/
deploy:         ## build + push + deploy agents and services
	./infra/deploy/deploy_all.sh
demo:           ## run the scripted end-to-end demo scenario
	python -m scenarios.demo_runner --vendor nimbuswrite --compress 240
teardown:       ## delete everything except the demo dashboard
	./infra/teardown.sh
test:
	pytest -q
```

A judge who can read this Makefile understands your whole system in fifteen seconds. Write it in week one, not week three.

---

## 3. Infrastructure provisioning

### 3.1 What gets created

| Resource | Name | Purpose |
|---|---|---|
| Firestore (Native) | default | workflow ledger, events, findings, approvals |
| Storage bucket | `${PROJECT}-evidence-quarantine` | raw vendor uploads; no agent read access |
| Storage bucket | `${PROJECT}-evidence-clean` | armor-stamped documents; Evidence agent read-only |
| Storage bucket | `${PROJECT}-binders` | exported audit binders |
| Pub/Sub topics | see §6 | event backbone |
| Artifact Registry | `drawbridge` | container images |
| Secret Manager | `drawbridge-*` | any API keys, signing key for approval tokens |
| Service accounts | 5 (one per agent) + 3 (services) | least privilege (§3.2) |

### 3.2 Service accounts and the permission matrix

This matrix is a *deliverable*, not just config — it appears in the README, the security diagram, and the video. Implement it exactly as documented.

| Service account | Granted | Explicitly denied (never granted) |
|---|---|---|
| `sa-orchestrator` | Firestore read/write, Pub/Sub publish/subscribe, Vertex AI user | email send, Storage read, approval write |
| `sa-questionnaire` | Pub/Sub, Vertex AI user, portal write, email send *via gateway* | Firestore findings write, Storage read |
| `sa-evidence` | Storage **clean bucket read-only**, Firestore findings write, Vertex AI user | any egress, email, quarantine bucket |
| `sa-scorer` | Firestore read + score write, Vertex AI user | external calls, approvals write |
| `sa-watchdog` | Pub/Sub publish, outbound fetch *via gateway*, Firestore task write | approvals, email, vendor data write |

```bash
for a in orchestrator questionnaire evidence scorer watchdog; do
  gcloud iam service-accounts create sa-$a --display-name "Drawbridge $a agent"
done
# example: evidence gets read-only on the clean bucket only
gsutil iam ch \
  serviceAccount:sa-evidence@$PROJECT_ID.iam.gserviceaccount.com:objectViewer \
  gs://$PROJECT_ID-evidence-clean
```

**Verification step (do this, it's a demo asset):** after provisioning, run a script that attempts a denied action per agent and asserts it fails. `tests/test_iam_boundaries.py` failing-as-expected is a *feature* — screenshot it.

---

## 4. Configuration and secrets

`.env.example` (committed) documents every knob; `.env` (gitignored) holds local values; Secret Manager holds deployed values.

```bash
PROJECT_ID=drawbridge-hack
REGION=us-central1
MODEL_FAST=gemini-3.5-flash        # default for all parsing/scoring
MODEL_DEEP=gemini-pro              # memos + contradiction analysis only
MODEL_LOCAL=gemma-3                # in-VPC PII scrub (stretch)
BUCKET_QUARANTINE=drawbridge-hack-evidence-quarantine
BUCKET_CLEAN=drawbridge-hack-evidence-clean
BUCKET_BINDERS=drawbridge-hack-binders
APPROVAL_TOKEN_SECRET=projects/…/secrets/drawbridge-approval-key/versions/latest
DEMO_TIME_COMPRESSION=240          # 1 real second = 4 simulated minutes
COST_CEILING_PER_REVIEW_USD=0.50   # soft guard; logs a warning when exceeded
```

A single `shared/config.py` loads and validates these with Pydantic at import time and **fails loudly on startup** if anything is missing — a service that boots half-configured produces the worst class of demo failure.

---

## 5. Domain model

### 5.1 Core types

```python
# shared/models.py
from enum import StrEnum
from pydantic import BaseModel, Field
from datetime import datetime

class ReviewState(StrEnum):
    INTAKE = "intake"
    QUESTIONNAIRE_OUT = "questionnaire_out"
    REPLIES_IN = "replies_in"
    EVIDENCE_REVIEW = "evidence_review"
    SCORED = "scored"
    GATED = "gated"              # parked, waiting on a human
    DECIDED = "decided"
    MONITORED = "monitored"
    NEEDS_HUMAN = "needs_human"  # terminal-ish: fleet refuses to guess

class Vendor(BaseModel):
    vendor_id: str
    name: str
    category: str
    is_ai_vendor: bool = False
    tier: int = 2
    status: str = "active"
    adversarial_flag: bool = False

class Review(BaseModel):
    review_id: str
    vendor_id: str
    state: ReviewState = ReviewState.INTAKE
    score: int | None = None
    band: str | None = None
    opened_at: datetime
    decided_at: datetime | None = None
    cost_usd: float = 0.0        # accumulated model spend — a demo metric

class Finding(BaseModel):
    finding_id: str
    review_id: str
    domain: str
    severity: str                 # low | medium | high
    contradiction: bool = False
    summary: str
    evidence_ref: str | None = None
    trace_ref: str | None = None
```

### 5.2 State machine rules

States advance monotonically; the only backward transition is `MONITORED → EVIDENCE_REVIEW` when the Watchdog reopens a review (and that creates a *new* review record linked to the old one, rather than mutating history — audit integrity). `NEEDS_HUMAN` can be entered from anywhere and always parks rather than guesses. Encode this as a transition table and validate every write:

```python
ALLOWED = {
  ReviewState.INTAKE: {ReviewState.QUESTIONNAIRE_OUT, ReviewState.NEEDS_HUMAN},
  ReviewState.QUESTIONNAIRE_OUT: {ReviewState.REPLIES_IN, ReviewState.NEEDS_HUMAN},
  ReviewState.REPLIES_IN: {ReviewState.EVIDENCE_REVIEW, ReviewState.NEEDS_HUMAN},
  ReviewState.EVIDENCE_REVIEW: {ReviewState.SCORED, ReviewState.NEEDS_HUMAN},
  ReviewState.SCORED: {ReviewState.GATED},
  ReviewState.GATED: {ReviewState.DECIDED},
  ReviewState.DECIDED: {ReviewState.MONITORED},
  ReviewState.MONITORED: {ReviewState.MONITORED},
}
```

An invalid transition raises and lands in `NEEDS_HUMAN` — **never** silently corrects. "The system refuses to guess" is a line worth saying out loud in the video.

---

## 6. Event contract

### 6.1 Topics

| Topic | Published by | Consumed by | Payload |
|---|---|---|---|
| `review.intake` | portal / dashboard | orchestrator | vendor details, tier hints |
| `review.plan_ready` | orchestrator | questionnaire | review_id, question tier |
| `vendor.reply_received` | inbox service | questionnaire | message ref |
| `vendor.evidence_uploaded` | portal | armor pipeline → evidence | object ref (quarantine) |
| `evidence.screened` | armor pipeline | evidence | clean object ref + verdict |
| `review.findings_ready` | evidence | scorer | review_id |
| `review.score_ready` | scorer | orchestrator | score, band, memo ref |
| `review.approved` | dashboard (human) | orchestrator, watchdog | decision, identity |
| `watchdog.hit` | watchdog | orchestrator | signal, vendor_id |

### 6.2 Envelope

Every message carries the same envelope — this is what makes tracing, replay, and idempotency uniform:

```python
class EventEnvelope(BaseModel):
    event_id: str          # uuid4
    type: str              # topic name
    review_id: str
    idem_key: str          # f"{review_id}:{step_id}" — the exactly-once guard
    trace_id: str          # ties the event to its OTel span tree
    source: str            # emitting agent/service
    ts: datetime
    payload: dict
```

### 6.3 Delivery semantics

Pub/Sub is at-least-once, so **every consumer must be idempotent** (§7.4). Set ack deadlines generously (60s) with explicit extension for long model calls, and configure a dead-letter topic (`*.dlq`) after 5 delivery attempts. A message landing in the DLQ moves its review to `NEEDS_HUMAN` and surfaces on the dashboard — visible failure handling is a graded behavior, so make it visible.

---

## 7. The shared kernel

Six modules that every agent depends on. Build these in Phase 1 before any agent logic — they encode the architectural claims, and retrofitting them later is how hackathon projects die.

### 7.1 `shared/gateway.py` — the policy chokepoint

Every outbound effect and every model input passes through here. Two named policies, enforced in code, logged when they fire.

```python
class PolicyViolation(Exception): ...

def call_tool(tool_name: str, ctx: ToolContext, **kwargs):
    """Single funnel for all agent side effects."""
    # P1: no outbound email to a new contact without a human approval token
    if tool_name == "send_email":
        if not verify_approval_token(ctx.review_id, kwargs["to"]):
            log_policy_block("P1", ctx, kwargs["to"])
            raise PolicyViolation("P1: outbound email requires human approval token")

    # P2: no external content reaches a model without an armor clean-stamp
    if tool_name in MODEL_INPUT_TOOLS:
        if not kwargs.get("armor_stamp") or not verify_stamp(kwargs["armor_stamp"]):
            log_policy_block("P2", ctx, kwargs.get("ref"))
            raise PolicyViolation("P2: unscreened content rejected at gateway")

    # rate + spend guards
    enforce_limits(ctx)
    with span(f"tool.{tool_name}", ctx) as s:
        result = TOOL_REGISTRY[tool_name](**kwargs)
        s.set_attribute("tool.result_size", len(str(result)))
        return result
```

`log_policy_block` writes a structured log line *and* a dashboard event — because the blocked-by-policy line appearing on screen during the demo is worth more than the code itself.

### 7.2 `shared/armor.py` — screening and the clean-stamp

```python
def screen_and_promote(quarantine_ref: str, review_id: str) -> ScreenResult:
    raw = storage.read(quarantine_ref)                  # bytes, never sent to a model
    text = extract_text(raw)                            # local parsing only
    scrubbed = gemma_scrub_pii(text)                    # stretch: in-VPC, §13
    verdict = model_armor.screen(scrubbed)              # injection / poisoning / PII

    result = ScreenResult(
        clean=not verdict.threat_found,
        categories=verdict.categories,
        excerpt=verdict.matched_excerpt,   # preserved for the binder, never re-fed to a model
    )
    record_screening(review_id, quarantine_ref, result)

    if verdict.threat_found:
        raise_adversarial_conduct(review_id, result)     # §11.3 — the signature feature
        sanitized = strip_payload(scrubbed, verdict)
        clean_ref = storage.write(BUCKET_CLEAN, sanitized, stamp=sign_stamp(...))
    else:
        clean_ref = storage.write(BUCKET_CLEAN, scrubbed, stamp=sign_stamp(...))
    publish("evidence.screened", review_id, {"ref": clean_ref, "verdict": result.dict()})
    return result
```

Two implementation notes that matter. First, the matched excerpt is stored as **inert evidence** — it goes into Firestore and the binder, and is never included in a prompt again (re-feeding it would defeat the whole point). Second, screening is a *pipeline stage owned by the platform*, not a step inside an agent — the Evidence agent has no code path that can read the quarantine bucket at all.

### 7.3 `shared/models.py` router — Flash-first economics

```python
ROUTING = {
    "parse_reply":       MODEL_FAST,
    "extract_controls":  MODEL_FAST,
    "score_rubric":      MODEL_FAST,
    "chase_message":     MODEL_FAST,
    "cross_examine":     MODEL_DEEP,   # depth is user-visible here
    "risk_memo":         MODEL_DEEP,   # and here
    "pii_scrub":         MODEL_LOCAL,  # in-VPC Gemma
}

def generate(task: str, prompt: str, ctx) -> ModelResult:
    model = ROUTING[task]
    with span(f"model.{task}", ctx) as s:
        r = vertex.generate(model=model, prompt=prompt)
        cost = estimate_cost(model, r.usage)
        s.set_attributes({"model": model, "tokens": r.usage.total, "cost_usd": cost})
        accumulate_review_cost(ctx.review_id, cost)     # powers the "<$0.50/review" metric
        return r
```

Accumulating cost per review is a ten-line feature that produces a headline number no competitor will show. Build it in Phase 1.

### 7.4 `shared/idempotency.py` — the exactly-once guard

The organizers dedicated a webinar to *"why a resumable agent might order two laptops."* This module is your on-camera answer.

```python
def once(idem_key: str, ctx, fn, *args, **kwargs):
    """Execute fn at most once across all retries, restarts, and redeliveries."""
    ref = db.collection("idempotency").document(idem_key)

    @firestore.transactional
    def claim(tx):
        snap = ref.get(transaction=tx)
        if snap.exists:
            return snap.to_dict()          # already done → return the recorded result
        tx.set(ref, {"status": "in_progress", "ts": now(), "source": ctx.agent})
        return None

    prior = claim(db.transaction())
    if prior:
        log_idempotent_skip(idem_key, ctx)   # visible in the demo: "skipped, already sent"
        return prior.get("result")

    result = fn(*args, **kwargs)             # the actual side effect
    ref.update({"status": "done", "result": serialize(result), "done_ts": now()})
    return result
```

**Key derivation rule:** `idem_key = f"{review_id}:{step_id}"` where `step_id` is deterministic from the workflow position (e.g. `questionnaire_send:v1`, `chase:round2`), never from a timestamp or uuid. If the key isn't reproducible after a restart, the guard is worthless.

The claim happens *before* the side effect, so a crash mid-effect leaves an `in_progress` record. On resume, `in_progress` records older than a timeout are surfaced for reconciliation rather than blindly re-run — for email, the safe default is "do not resend, flag for human confirmation," which is exactly the conservative choice a security product should make and a great line for the video.

### 7.5 `shared/checkpoint.py` — durable workflow steps

```python
def step(name: str, ctx, fn):
    """Checkpoint before executing; resume skips completed steps."""
    doc = db.collection("reviews").document(ctx.review_id)
    state = doc.get().to_dict()
    if name in state.get("completed_steps", []):
        return state["step_results"].get(name)

    doc.update({"current_step": name, "step_started": now()})
    result = fn()
    doc.update({
        "completed_steps": firestore.ArrayUnion([name]),
        f"step_results.{name}": serialize(result),
    })
    return result
```

The Orchestrator's plan is therefore just a list of named steps, and *resume* is "replay the list, skipping completed ones." This is why the kill-and-resume demo works with no special-case recovery code — recoverability is structural.

### 7.6 `shared/telemetry.py` — spans that become the binder

Design the span schema once, use it everywhere. Every span carries: `review_id`, `agent`, `goal` (what it was trying to do, in plain English), `decision` (what it concluded), `model`, `tokens`, `cost_usd`, `latency_ms`, `policy_events`.

```python
@contextmanager
def span(name: str, ctx, **attrs):
    with tracer.start_as_current_span(name) as s:
        s.set_attributes({"review_id": ctx.review_id, "agent": ctx.agent, **attrs})
        try:
            yield s
        except Exception as e:
            s.set_attribute("error", str(e)); s.set_status(StatusCode.ERROR); raise
```

The plain-English `goal` and `decision` attributes are what let the Audit Binder read like a human wrote it. Set them on every meaningful span, not just the top-level ones.

### 7.7 `shared/memory.py` — Memory Bank access

```python
def recall_dossier(vendor_id: str) -> Dossier:
    """Prior reviews, findings, negotiated exceptions, contacts, policy notes."""

def remember(vendor_id: str, note: MemoryNote):
    """Write a distilled, durable fact — not raw transcript."""
```

The distillation rule matters: L2 (Firestore) holds *everything that happened*; L3 (Memory Bank) holds *what's worth knowing next time*. Write to Memory Bank only at review close and at notable events (adversarial flag, negotiated exception, contact change). Dumping the whole review into memory is the mistake the "persistence is not memory" webinar exists to warn against.

---

## 8. Agent: Orchestrator

**Mission.** Turn an intake request into a tiered plan, dispatch steps, enforce gates, and own the review's state.

**Trigger.** `review.intake`, plus `review.score_ready`, `review.approved`, `watchdog.hit`.

**Prompt design.** The planning prompt is short and structured: it receives the vendor facts and the tiering policy, and returns a JSON plan (list of step names + parameters). Give it the tiering rules explicitly rather than hoping the model infers them:

> Tier 1 if the vendor processes customer data, has production system access, or is an AI service handling company text. Tier 2 if it handles internal non-customer data. Tier 3 otherwise. When evidence is ambiguous, tier *up* and say why.

**Implementation shape.**

```python
def handle_intake(ev: EventEnvelope):
    ctx = Context(review_id=ev.review_id, agent="orchestrator")
    dossier = recall_dossier(ev.payload["vendor_id"])          # L3 memory
    plan = step("plan", ctx, lambda: generate_plan(ev.payload, dossier))
    save_review(ev.review_id, state=ReviewState.QUESTIONNAIRE_OUT, plan=plan)
    publish("review.plan_ready", ev.review_id, {"tier": plan.tier})
```

**Failure behavior.** Any sub-agent failure that repeats past the DLQ threshold → `NEEDS_HUMAN` with a dashboard card explaining what stalled and why. The Orchestrator never invents a missing answer and never approves.

**Test.** `test_resume.py` — kill the process after `plan` but before publish; on restart the plan step is skipped and exactly one `plan_ready` is published.

---

## 9. Agent: Questionnaire

**Mission.** Generate the tier-appropriate question set, deliver it, parse replies incrementally over days, and chase politely.

**Question generation.** Don't have the model invent questions from scratch each run — that's non-deterministic and wastes tokens. Keep a curated bank in `agents/questionnaire/bank.yaml` organized by rubric domain, and let the model *select and tailor* (Tier 1 ≈ 60 questions, Tier 2 ≈ 30, Tier 3 ≈ 12), adding AI-specific questions when `is_ai_vendor`. This makes the demo reproducible and the questions defensible.

**Evidence-demanding style rule** (bake this into the prompt): never generate a yes/no question. "Do you encrypt data?" becomes "List encryption standards for data at rest and in transit and attach your key-management policy." Specificity is what makes the later contradiction detection possible.

**Sending — the P1 gate.**

```python
def send_questionnaire(ctx, review_id, vendor_contact, questions):
    key = f"{review_id}:questionnaire_send:v1"
    return once(key, ctx, lambda: gateway.call_tool(
        "send_email",
        ctx,
        to=vendor_contact,
        subject=f"Security review — {org_name()}",
        body=render_questionnaire(questions),
        approval_token=fetch_approval_token(review_id, vendor_contact),
    ))
```

If no token exists, the gateway raises `PolicyViolation`, the review parks in `GATED`, and the dashboard shows an approval card. **That parked state is the demo moment** — autonomy that asks permission before speaking to an outsider.

**Incremental parsing.** Replies arrive across days and partially. Parse each message on arrival, merge into `qa_responses` keyed by `question_id`, and record `confidence` and `source_msg`. Anything below the confidence threshold sets `needs_human=True` rather than guessing — unparseable answers get quoted back to the analyst queue, never silently dropped.

```python
def on_reply(ev):
    ctx = Context(ev.review_id, "questionnaire")
    msg = fetch_message(ev.payload["msg_ref"])
    screened = armor.screen_text(msg.body, ev.review_id)      # replies are untrusted too
    parsed = generate("parse_reply", PARSE_PROMPT.format(...), ctx)
    merge_responses(ev.review_id, parsed, source=msg.id)
    if coverage(ev.review_id) >= 0.9:
        publish("review.findings_ready", ev.review_id, {})
    else:
        schedule_chase(ev.review_id, days=3)
```

**Note:** vendor *replies* are screened exactly like uploads. An injection attempt can arrive in an email body just as easily as in a PDF, and demonstrating that you understood this is a differentiator.

**Chasing.** Scheduled, capped at three rounds, escalating in tone from reminder → deadline notice → escalation to the analyst. Each chase is its own idempotency key (`chase:round2`). Three rounds without response → `NEEDS_HUMAN`.

---

## 10. Agent: Evidence

**Mission.** Read screened documents, extract control claims, and **cross-examine** them against questionnaire answers.

**Two-pass design.** Pass one (Flash): extract structured control claims from each document — control name, stated implementation, scope, exceptions, dates, auditor if present. Pass two (Pro): reconcile the extracted claims against `qa_responses` and emit findings, flagging contradictions.

```python
CROSS_EXAM_PROMPT = """
You are reconciling a vendor's questionnaire answers against their own audit evidence.
For each rubric domain, compare CLAIMS (from the questionnaire) with EVIDENCE (extracted
from the SOC 2 / certificates / policies).

Output JSON findings: domain, severity, contradiction (bool), summary,
evidence_ref (quote the specific passage), claim_ref (the question id).

Rules:
- A contradiction requires BOTH a specific claim and a specific contradicting passage.
- Missing evidence is NOT a contradiction — it is a gap. Label it as such.
- Expired certificates are findings regardless of what the questionnaire says.
- Do not speculate about intent. Report what the documents say.
"""
```

The "missing ≠ contradiction" rule prevents the model's most common failure here (over-flagging), which would make your demo's headline finding look cheap.

**The hero finding.** DataDynamo claims org-wide MFA in the questionnaire; its SOC 2 exception notes list an unremediated MFA gap for administrative access. The pipeline must produce: `domain=access_control, severity=high, contradiction=True`, with both passages cited. Verify this exact finding lands in every test run — it's the 1:20 mark of your video.

**Failure behavior.** Unreadable or corrupt documents produce a `needs_human` finding with the file reference — never a silent skip. A document that fails screening never reaches this agent at all.

---

## 11. Agent: Risk Scorer

**Mission.** Convert findings into a defensible 0–100 score, band, and memo.

### 11.1 The rubric is config, not prompt

`rubric.yaml` holds weighted domains (data protection 20, access control 15, incident response 15, compliance posture 15, business continuity 10, subprocessors 10, AI-specific 10, plus modifiers). Scoring is **deterministic arithmetic in Python** over model-produced findings — the model judges severity, the code computes the score. This matters for three reasons: reproducibility in the demo, defensibility to a judge who asks "why 71?", and the ability to show the computation in the binder.

```python
def compute_score(findings: list[Finding], rubric: Rubric, flags: Flags) -> ScoreResult:
    domain_scores = {d.name: d.max_points for d in rubric.domains}
    for f in findings:
        domain_scores[f.domain] -= rubric.penalty(f.severity, f.contradiction)
    raw = max(0, sum(domain_scores.values()))
    if flags.adversarial_conduct:
        raw = max(0, raw - rubric.adversarial_penalty)   # −25
    band = rubric.band_for(raw, forced_escalation=flags.adversarial_conduct)
    return ScoreResult(score=raw, band=band, breakdown=domain_scores)
```

### 11.2 The memo

One Pro call. Input: findings, score breakdown, vendor context, prior dossier. Output: a one-page risk memo written for a CISO — the recommendation, the three things that drove it, the mitigations required for conditional approval, and what to re-check in 90 days. This is the single artifact a human reads before approving, so it deserves the expensive model.

### 11.3 The Adversarial Conduct signal (the signature feature)

```python
def raise_adversarial_conduct(review_id: str, screen: ScreenResult):
    set_flag(review_id, "adversarial_conduct", True)
    set_vendor_flag(vendor_of(review_id), adversarial_flag=True)
    add_finding(Finding(
        domain="conduct", severity="high", contradiction=False,
        summary="Vendor-supplied document contained concealed instructions targeting "
                "the automated reviewer. Content blocked; attempt recorded.",
        evidence_ref=store_inert_excerpt(review_id, screen.excerpt),
    ))
    publish("review.rescore", review_id, {"reason": "adversarial_conduct"})
    notify_dashboard(review_id, banner="ADVERSARIAL CONDUCT DETECTED", severity="high")
```

Three things happen at once: the score drops, the band is forced to escalate regardless of arithmetic, and the vendor record carries the flag into all future reviews via Memory Bank. Say this in the video: *"the vendor just told us something about themselves that no questionnaire would have revealed."*

---

## 12. Agent: Watchdog

**Mission.** Prove the review doesn't end at signature — the statistic that fewer than half of organizations continuously monitor vendors is the reason this agent exists.

**Implementation.** Scheduled sweep (Cloud Scheduler → Pub/Sub → agent) over the approved-vendor portfolio. For each vendor: check certificate expiry dates from the dossier, fetch breach/news signals through the gateway, and evaluate relevance with a cheap Flash call. A hit publishes `watchdog.hit`, which opens a *new* linked review rather than mutating the closed one.

**Scope discipline.** The MVP version is a scheduled job over a small curated feed plus expiry math — that is genuinely useful and honest. Live multi-source news ingestion is a Phase-3 stretch. If it doesn't get built, the demo shows a scheduled sweep firing on a seeded signal, clearly labeled as seeded.

**Failure behavior.** Feed outage → log and skip; the Watchdog never blocks or degrades an active review.

---

## 13. Gemma in-VPC PII scrubber (stretch, bonus-earning)

Runs as a Cloud Run service with a small Gemma model, called by the armor pipeline before screening. Input: extracted document text. Output: same text with detected personal data replaced by typed placeholders (`[PERSON_1]`, `[EMAIL_2]`), plus a mapping stored separately in Firestore for the binder.

Why it's worth building: it satisfies the "integrate an additional Google model" bonus with a feature that is actually *on-theme* (data sovereignty in a vendor-review product) rather than a bolt-on. Why it's a stretch: it's the only component that needs model hosting, and it must never become a critical path — if the scrubber is unavailable, the pipeline logs a degraded-mode warning and proceeds to Model Armor directly.

**Honesty rule:** if it isn't built, it isn't mentioned. Do not claim the Gemma bonus without the code.

---

## 14. Human gates and approval tokens

Two gates, both implemented with the same primitive: a signed, single-use, scoped token.

```python
def issue_approval_token(review_id, scope, identity) -> str:
    payload = {"review_id": review_id, "scope": scope, "identity": identity,
               "jti": uuid4().hex, "exp": now() + timedelta(hours=24)}
    return jwt_sign(payload, key=secret("drawbridge-approval-key"))
```

- **G1 · Risk acceptance** (`scope="decision"`). The dashboard shows the memo, findings, and score breakdown; approval writes an `approvals` record with the named identity, the decision, and any conditions. No code path can set `state=DECIDED` without a valid token.
- **P1 · First outbound contact** (`scope="email:<address>"`). One tap authorizes the thread; subsequent messages in the same thread are delegated. Tokens are single-use (`jti` recorded in Firestore) so a replayed request fails.

**Design point worth narrating:** the gate is enforced at the gateway, not in the UI. Even a compromised or confused agent cannot email a vendor or approve a decision, because the capability requires a signed human artifact it cannot produce.

---

## 15. Audit Binder generation

**Input:** a `review_id`. **Process:** query the trace tree and the event ledger, assemble sections, render to PDF. **Output:** a file in the binders bucket plus a download link on the dashboard.

```python
def export_binder(review_id: str) -> str:
    review   = load_review(review_id)
    events   = load_events(review_id)            # ordered, immutable
    spans    = trace_client.list_spans(review_id)  # reasoning chain
    findings = load_findings(review_id)
    approval = load_approval(review_id)
    screens  = load_screenings(review_id)        # includes any blocked payloads

    doc = BinderDoc(cover=Cover(
        vendor=review.vendor_name, review_id=review_id, tier=review.tier,
        opened=review.opened_at, decided=review.decided_at,
        outcome=review.band, approver=approval.identity,
        frameworks=["SOC 2 CC9.2", "ISO 27001 A.5.19–5.23", "DORA ICT third-party"],
    ))
    doc.add_timeline(events)
    doc.add_questionnaire(load_responses(review_id))     # with parse provenance
    doc.add_evidence_inventory(screens)                  # armor verdicts verbatim
    doc.add_findings(findings)                           # with source passages
    doc.add_score_computation(review.score_breakdown)    # the arithmetic, shown
    doc.add_decisions(approval)                          # identity + timestamp
    doc.add_reasoning_appendix(spans)                    # goal/decision per step
    doc.add_monitoring_log(load_watchdog(review_id))
    return storage.write_pdf(BUCKET_BINDERS, doc.render())
```

**Implementation advice.** Generate HTML with a print stylesheet and convert to PDF (WeasyPrint or headless Chrome) rather than fighting a PDF library directly — you'll iterate on layout at least five times, and HTML iteration is minutes versus hours. Put the compliance-framework mapping on the cover page: that single line reframes the artifact from "logs" to "the thing your auditor asks for."

**Demo requirement:** the export must complete in under three seconds on screen. Pre-warm the service before recording.

---

## 16. Frontend implementation

### 16.1 Internal dashboard (the thing judges actually look at)

Next.js + Tailwind on Cloud Run. Four screens, no more:

1. **Queue** — all reviews as cards: vendor, tier, state, score, days elapsed, and a badge for anything needing a human. This is the opening shot of the video.
2. **Review timeline** — the vertical event stream (intake → questionnaire → replies → evidence → findings → score → gate → decision), each entry expandable to show the agent, its goal, its decision, and cost. This is where the injection banner and the contradiction flag appear.
3. **Gate card** — memo, findings, score breakdown, Approve / Conditional / Reject with a conditions field.
4. **Binder view** — export button and prior binders.

**Design notes that raise the presentation score:** one accent color, generous whitespace, real empty states, skeleton loaders (never a spinner on a blank page), and a persistent header strip showing live fleet stats (active reviews, events processed, model spend today). Judges rate polish subconsciously; a status strip that ticks during the demo reads as "this is running."

### 16.2 Time compression control

```python
# scenarios/clock.py — simulated time for the demo, honestly labeled
class DemoClock:
    def __init__(self, factor: int):   # 240 → 1s real = 4 simulated minutes
        self.factor = factor
        self.t0_real = time.time()
        self.t0_sim = datetime(2026, 8, 20, 9, 0)
    def now(self) -> datetime:
        return self.t0_sim + timedelta(seconds=(time.time()-self.t0_real)*self.factor)
```

Every timestamp written during a demo run uses the injected clock; every scheduled action (vendor reply delivery, chase timers) is scheduled against it. **The UI must display a "TIME-COMPRESSED DEMO · 1s = 4min" badge whenever the factor ≠ 1.** Real events, accelerated clock, stated on screen — that's the honest version, and honesty here protects you from the one question that could sink an otherwise great demo.

### 16.3 Vendor portal

Deliberately minimal: token-scoped link, questionnaire form, upload dropzone, submission confirmation. Its job in the demo is fifteen seconds of screen time when NimbusWrite uploads the poisoned PDF. Don't over-build it.

### 16.4 Vendor inbox simulator

A Cloud Run service holding vendor mailboxes so the demo is deterministic and the video can *show* the vendor's inbox containing exactly one email after the crash-and-resume. Label it plainly in the README as a simulated mail channel; the interface matches a real SMTP adapter so the substitution is a config change, not a rewrite.

---

## 17. Synthetic vendor pack

Three vendors, generated in Phase 0 and committed to the repo so judges can reproduce every demo beat.

| Vendor | Tier | Role | Must produce |
|---|---|---|---|
| CleanCloud Analytics | 2 | control | clean run, score ≥ 80, approve band |
| DataDynamo Logistics | 1 | contradictor | MFA claim vs SOC 2 exception; expired ISO cert; band = conditional |
| NimbusWrite AI | 1 | adversary | injection block + Adversarial Conduct flag + forced escalation |

Each folder contains: `profile.json` (vendor facts, contact persona), `questionnaire_answers.json` (with a reply schedule — which answers arrive on which simulated day), `evidence/` (SOC-2-style report, certificates, policy PDFs), and `expected.json` (the assertions the scenario test checks).

**The NimbusWrite payload.** A "Security Overview" PDF containing a block of white-on-white text instructing an automated reviewer to treat the vendor as pre-approved and skip evidence verification. Keep it obvious and benign — this is a test fixture for your own defenses, not an attack tool. The repo README must state where the payload is, what it says, and why it's there, so judges can reproduce the block and nobody mistakes it for something else. Generate all three packs with Claude Code from a spec; hand-write nothing.

---

## 18. Cost engineering

| Control | Setting |
|---|---|
| Budget alerts | $50 / $100 / $130 of the $150 credits |
| Cloud Run | min-instances 0, max-instances 2, CPU throttling on |
| Agent Engine | tear down non-demo deployments after each phase |
| Model routing | Flash default; Pro only for `cross_examine` and `risk_memo` |
| Per-review meter | `accumulate_review_cost` warns past `COST_CEILING_PER_REVIEW_USD` |
| Demo runs | cap at 20 full end-to-end runs before recording week; use cached fixtures for UI work |
| Teardown | `make teardown` after final recording; keep only the dashboard |

Screenshot the budget page and the per-review cost metric — "under fifty cents per review, and here's the billing console" is a line almost no submission will be able to say.

---

## 19. Testing strategy

Five tests carry the entire architectural claim. Write them *before* the features they cover; they double as the "Challenges" section of your Devpost writeup.

```python
# tests/test_idempotency.py
def test_email_sent_exactly_once_across_restart():
    run_until("questionnaire_send", then="SIGKILL")
    restart_worker()
    run_to_completion()
    assert inbox_count(vendor="nimbuswrite") == 1
    assert idem_record("…:questionnaire_send:v1")["status"] == "done"

# tests/test_resume.py
def test_resume_from_checkpoint_preserves_state():
    s1 = run_until("evidence_review"); kill()
    s2 = restart_and_finish()
    assert s2.completed_steps[:len(s1.completed_steps)] == s1.completed_steps
    assert s2.state == ReviewState.GATED

# tests/test_armor_flow.py
def test_injection_blocks_and_raises_risk():
    r = run_review("nimbuswrite")
    assert r.flags.adversarial_conduct is True
    assert r.score <= baseline_score("nimbuswrite") - 25
    assert r.band == "escalate"
    assert "conduct" in [f.domain for f in r.findings]

# tests/test_iam_boundaries.py
def test_evidence_agent_cannot_send_email():
    with pytest.raises(PolicyViolation):
        as_agent("evidence").gateway_call("send_email", to="x@y.z")

# tests/test_cross_exam.py
def test_mfa_contradiction_detected():
    f = run_review("datadynamo").findings
    assert any(x.contradiction and x.domain == "access_control" for x in f)
```

Beyond these: a `scenarios/demo_runner.py` smoke run in CI on every push (against fixtures, not live models, to keep it free) so you never discover on Day 28 that the demo path broke on Day 24.

---

## 20. Failure modes and fallbacks

### 20.1 Demo-day failure decision tree
- Live segment fails once → retake same day.
- Fails across three takes on different days → drop the on-camera kill; show restart-and-resume from a clean start. Never fake it.
- Model latency spikes mid-recording → cut to the console proof sequence, return after. (Record console footage separately so you always have B-roll.)
- Cloud Run cold start on camera → pre-warm every service with a scripted health check five minutes before recording.

### 20.2 If a GEAP component is unavailable to you
Implement the same contract behind an interface (`shared/armor.py`, `shared/gateway.py`, `shared/memory.py` are already interfaces for exactly this reason), state the substitution plainly in the README and the video, and keep the architecture story intact. A judge respects "Model Armor wasn't available in my region, so this is the same screening contract implemented against X, swappable in one file." A judge does not respect a claim that isn't true.

### 20.3 Solo-builder continuity
Daily push, daily 10-minute log entry, weekly export of the Firestore fixtures. If you lose two days to illness, the cut order in the master doc (Contract Clause → registry versioning → live Watchdog feeds → cosmetics) is pre-decided so you don't spend recovery time deliberating.

---

## 21. Master checklist — start to win

Check items off in order within each phase. Items marked **★** are load-bearing for a prize.

### Phase 0 · Foundations (Aug 11–13)

**Rules and admin**
- [ ] ★ Read the Official Rules end to end; write a one-page compliance checklist
- [ ] ★ Confirm: new-projects-only clause, one-prize-per-project allocation, multiple-submission rules
- [ ] ★ Confirm whether non-Google AI tooling is restricted to development use (Claude Code) and whether AI-assisted development must be disclosed
- [ ] Confirm eligibility for Individual/Hobbyist prize as a solo entrant; note the Startup prize requires incorporation (skip)
- [ ] Register on Devpost; join the Discord/community channel if one exists
- [ ] Diarize all four webinars (Aug 13, 20, 27 + any others); calendar the submission deadline **minus 24 hours** as your personal deadline
- [ ] Claim the $150 GCP credits

**Environment**
- [ ] Create dedicated GCP project; enable billing + credits
- [ ] ★ Set budget alerts at $50 / $100 / $130
- [ ] Enable all APIs (§1.2); pick and record the region
- [ ] Local toolchain installed (Python, Node, gcloud, Docker, OBS)
- [ ] ★ Hello-world agent deployed to Agent Engine — *proves the platform works for you*
- [ ] ★ Hello-world service deployed to Cloud Run with a public URL
- [ ] Verify access to Model Armor, Agent Gateway, Memory Bank, Agent Registry; log any gaps and pick fallbacks now (§20.2)
- [ ] Create the public GitHub repo with the folder skeleton, LICENSE, `.env.example`, and a stub README

**Design fixtures**
- [ ] ★ Generate the three synthetic vendor packs with expected outcomes
- [ ] Write `rubric.yaml` (weights, penalties, bands, −25 adversarial modifier)
- [ ] Write `bank.yaml` question bank across the eight domains
- [ ] Provision Firestore, three buckets, Pub/Sub topics + DLQs
- [ ] ★ Create five agent service accounts with the exact permission matrix
- [ ] Write the Makefile targets (even if some are stubs)
- [ ] Attend the Aug 13 long-running-agents webinar; capture notes on idempotency/human-approval language for reuse

### Phase 1 · The spine (Aug 14–19) — Milestone M1: a stranger could watch J1 happen

- [ ] `shared/config.py` with fail-loud validation
- [ ] `shared/models.py` domain types + state machine table
- [ ] ★ `shared/gateway.py` with P1 and P2 enforced and logged
- [ ] ★ `shared/idempotency.py` with transactional claim-before-effect
- [ ] ★ `shared/checkpoint.py` step wrapper
- [ ] `shared/telemetry.py` span schema incl. goal/decision/cost attributes
- [ ] ★ Per-review cost accumulation wired into the model router
- [ ] Pub/Sub publisher/subscriber plumbing with the shared envelope
- [ ] Orchestrator: intake → tiering → plan → dispatch
- [ ] Questionnaire: generation from bank, send through gateway, incremental parsing, chase scheduling
- [ ] Evidence: document extraction pass (Flash)
- [ ] Evidence: cross-examination pass (Pro) producing findings
- [ ] Risk Scorer: deterministic scoring from `rubric.yaml` + Pro memo
- [ ] Dashboard v1: queue + review timeline (ugly is fine, working is not optional)
- [ ] Vendor portal v1 + inbox simulator
- [ ] Human gate G1 with signed tokens; `DECIDED` unreachable without one
- [ ] ★ CleanCloud runs end to end (Aug 17)
- [ ] ★ DataDynamo produces the MFA contradiction finding (Aug 19)
- [ ] `test_cross_exam.py` green
- [ ] Daily: commit, push, log entry

### Phase 2 · Armor and steel (Aug 20–24) — Milestone M2: all four demo pillars work on demand

- [ ] ★ Quarantine → screen → clean-bucket promotion pipeline
- [ ] ★ Model Armor integration with verdict capture and inert-excerpt storage
- [ ] ★ Adversarial Conduct flag: score penalty, forced escalation, vendor flag, dashboard banner
- [ ] ★ NimbusWrite injection is blocked and rescored (`test_armor_flow.py` green)
- [ ] Reply-body screening (not just uploads)
- [ ] ★ Kill-and-resume works: `test_resume.py` + `test_idempotency.py` green
- [ ] In-progress reconciliation policy for interrupted email steps (no blind resend)
- [ ] DLQ handling → `NEEDS_HUMAN` card on the dashboard
- [ ] ★ Per-agent service accounts actually enforced; `test_iam_boundaries.py` green
- [ ] ★ Memory Bank: dossier write at review close; recall at intake
- [ ] Second-review scenario demonstrating recall (the L3 payoff)
- [ ] ★ Publish the fleet to the Agent Registry with version + capability description
- [ ] Cloud Scheduler → Watchdog sweep (seeded signal acceptable)
- [ ] Dashboard v2: gate card, injection banner, fleet status strip
- [ ] Watch Aug 20 webinar; note any rubric language to mirror in the writeup
- [ ] Freeze feature scope for anything not in the demo script

### Phase 3 · The proof layer (Aug 25–27)

- [ ] ★ OTel spans on every agent step with goal/decision populated
- [ ] ★ Audit Binder generator: all eight sections, compliance mapping on the cover
- [ ] Binder renders in under 3 seconds; layout reviewed at print size
- [ ] Time-compression clock + on-screen "TIME-COMPRESSED DEMO" badge
- [ ] `scenarios/demo_runner.py` replays the full demo deterministically
- [ ] Dashboard polish pass: empty states, skeletons, one accent color, real copy
- [ ] Stretch: Gemma in-VPC PII scrubber (build only if everything above is green)
- [ ] Stretch: Watchdog live feed
- [ ] Attend Aug 27 memory webinar; align the memory-hierarchy language in docs
- [ ] ★ Architecture diagrams finalized and committed to `docs/diagrams/`
- [ ] ★ Docs site built and deployed (Home, Getting Started, Architecture, Security, Live Demo)
- [ ] ★ README rewritten: problem, video placeholder, architecture image, 30-minute spin-up, synthetic data note, teardown, permission matrix table
- [ ] Cost check: per-review figure measured and recorded; screenshot the billing page

### Phase 4 · The performance (Aug 28–30)

**Recording (Aug 28)**
- [ ] Feature freeze — no new code except demo-breaking bug fixes
- [ ] Pre-warm all services; run the scenario twice to warm caches
- [ ] ★ Record console B-roll separately: Agent Engine, Cloud Run, Pub/Sub, IAM (per-agent SAs), Cloud Trace waterfall, budget page
- [ ] ★ Record the live segment take 1 (registry → intake → compressed replies → contradiction → injection block → kill/resume → gate)
- [ ] Record take 2 and take 3 (different times of day)
- [ ] Record the cold open and the closing metrics card
- [ ] Assemble to ≤4:00; captions on; audio normalized; no music over narration
- [ ] ★ Verify the video shows explicit Google Cloud console proof
- [ ] Upload to YouTube as **public**; title, description with repo + docs links

**Submission assets (Aug 29)**
- [ ] ★ Devpost: name, tagline, full description (Inspiration → What it does → How I built it → Challenges → Accomplishments → What I learned → What's next)
- [ ] ★ Rewrite Inspiration as your own true origin story
- [ ] Technologies list complete (Gemini 3.5 Flash/Pro, ADK, Agent Engine, Memory Bank, Model Armor, Registry, Gateway, Cloud Run, Pub/Sub, Firestore, Storage, Cloud Trace, IAM, Gemma if built)
- [ ] Gallery images uploaded (system architecture, injection defense, security, tech stack)
- [ ] ★ Hosted URL live and loading logged-out
- [ ] ★ Repo public, README final, synthetic pack included, tests passing
- [ ] ★ Submit a complete draft (never leave first submission to the last day)

**Bonus content (Aug 29)**
- [ ] ★ Medium article published: "I Built an Agent Fleet That Gets Prompt-Injected for a Living"
- [ ] ★ Article contains the required "created for this hackathon" disclosure sentence
- [ ] Article embeds PNG exports of the diagrams (Medium rejects SVG)
- [ ] Article links: repo, docs site, video, Devpost
- [ ] ★ LinkedIn post with the 30-second injection clip + **#AllThingsAgenticHackathon**
- [ ] ★ X/Twitter thread (2–3 posts) with the same hashtag and clip
- [ ] Add all bonus links into the Devpost submission fields

**Final pass (Aug 30)**
- [ ] ★ Cold-follow your own README on a clean GCP project; fix every friction point
- [ ] Verify every link in incognito (video, repo, docs, hosted URL, article, socials)
- [ ] Re-read the Official Rules checklist line by line against the submission
- [ ] Confirm no non-Google AI in the *product* path
- [ ] Update the submission with any fixes; save the confirmation screenshot
- [ ] `make teardown` for everything except the demo dashboard; confirm spend
- [ ] Post a short "submitted" note tagging the hashtag (visibility, costs nothing)

**Aug 31 · Buffer only**
- [ ] No new features. Platform-surprise response only.
- [ ] Final link check 12 hours before the deadline

### Post-submission (Sept 1 onward)
- [ ] Write a second Medium piece (architecture deep-dive) — SalesShortcut published two
- [ ] Open-source contribution or issue report to ADK/GEAP repos from real friction found
- [ ] Respond to any judge/organizer questions within hours
- [ ] Keep the hosted URL alive through judging; monitor spend
- [ ] If it wins or places: publish results post, update repo badges, decide whether the startup path in §4 of the master doc is worth pursuing

---

## 22. Definition of done

The build is done when: `make bootstrap && make seed && make deploy && make demo` works on a clean project; the five tests are green; the four pillars (injection block, kill-and-resume, human gate, audit binder) each happen live on camera; the per-review cost is a number you can say out loud; and every link in the submission opens in an incognito window.
