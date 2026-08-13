# Drawbridge — Architecture & Documentation Asset Pack
### The autonomous vendor-trust fleet · Fortified Enterprise Fleet track
*This document is written to be dropped straight into the repo as `docs/architecture.md`, published as the Architecture page of the docs site, and mined for the Devpost description and Medium article. Every diagram it references lives in `diagrams/` as a standalone SVG.*

---

## 1. How to use this asset pack

| Asset | Docs site | Devpost | Medium blog | Demo video |
|---|---|---|---|---|
| `01-system-architecture.svg` | Architecture page hero | The required architecture diagram + gallery image #1 | Section: "Why a fleet, not a chatbot" | B-roll at 3:10 |
| `02-review-sequence.svg` | Architecture page | Gallery image | Section: "Three weeks of work as one sequence" | — |
| `03-injection-defense.svg` | Security page hero | Gallery image #2 (the hook) | The centerpiece: "…gets prompt-injected for a living" | Freeze-frame at 1:45 |
| `04-memory-hierarchy.svg` | Architecture page | — | Section: "Persistence is not memory" | — |
| `05-security-architecture.svg` | Security page | Gallery image | Section: "Least privilege for agents" | Cutaway at 2:20 |
| `06-deployment-architecture.svg` | Getting Started page | — | Closing section on cost | — |
| `07-data-model.svg` | Data page | — | Optional appendix | — |
| `08-tech-stack.svg` | Home page footer | Gallery image | Header image candidate | Closing card |

Two practical notes. First, Medium does not accept SVG uploads — export each diagram to PNG at 2× before publishing (open the SVG in any browser and screenshot at zoom, or run it through any SVG-to-PNG converter; keep the SVGs as the source of truth). Second, GitHub renders these SVGs inline in the README and docs, so reference them with relative paths exactly as this document does.

---

## 2. System overview

Drawbridge is organized as seven horizontal layers, and the architecture's core claim is that a request only moves *downward* through increasing levels of trust: actors interact with Cloud Run surfaces; every vendor-origin byte crosses a screening boundary (**Model Armor first, then the in-VPC Gemma scrub** — the order matters and is explained in §6) before it may touch a model; every agent call passes the Agent Gateway's **three** named policies; all lifecycle transitions travel as Pub/Sub events so no agent ever polls or blocks on another; the fleet itself runs on Vertex AI Agent Engine as an **ADK 2 graph workflow** of long-running, resumable, idempotent workers; durable state and long-term memory live in their own layer, now **four tiers deep**; and everything the fleet does lands in the governance layer, where reasoning traces become the Audit Binder. Removing any single component degrades the system gracefully instead of breaking it — with one deliberate exception, stated plainly because the asymmetry is the point: **optional controls degrade, mandatory controls fail closed.** If Model Armor is unavailable, nothing is promoted out of quarantine and affected reviews park.

**The public surface is a boundary, not a page.** The entry page and the read-only review path are statically rendered and serve cached Firestore reads, and the rule that makes that a security property rather than a performance note is structural: **no route reachable without a token may reach the model router.** A bot hitting the hosted URL costs fractions of a cent in reads and never a Gemini token. Every write — intake, approvals, portal submissions, exports — requires a signed token; public routes are rate-limited per IP and capped at two instances; minimum instances stay at 0 everywhere. A diagram cannot draw an absent edge, so it is written here instead: **there is deliberately no arrow from the public surface to the model plane.**

![System architecture](diagrams/01-system-architecture.svg)

---

## 3. Repository layout

The tree below is the complete intended structure of the public repo. Judges grade the README's spin-up path, so the layout optimizes for a stranger finding everything where they expect it: agents are one folder each, all demo data ships in-repo, and one Makefile drives bootstrap → seed → demo → teardown.

```
drawbridge/
├── README.md                     # problem, demo video, spin-up in 30 minutes, teardown
├── LICENSE
├── .env.example                  # project id, region, model names — no secrets ever
├── Makefile                      # bootstrap · seed · run-local · deploy · demo · teardown
├── agents/
│   ├── orchestrator/
│   │   ├── agent.py              # ADK root agent: plan, dispatch, enforce gates
│   │   ├── planner.py            # vendor tiering → review plan
│   │   ├── state.py              # checkpoints + idempotency key writes
│   │   └── prompts/              # planning and gating prompt templates
│   ├── questionnaire/
│   │   ├── agent.py
│   │   ├── generator.py          # tier → question set (see Appendix C of master doc)
│   │   ├── parser.py             # incremental reply parsing over days
│   │   └── chaser.py             # polite scheduled follow-ups
│   ├── evidence/
│   │   ├── agent.py
│   │   ├── extractors.py         # SOC 2 / cert / policy control extraction
│   │   ├── retrieval.py          # chunk · embed · Firestore KNN search (L2.5)
│   │   ├── checks.py             # deterministic checks — expiry, staleness, scope
│   │   ├── subprocessors.py      # fourth-party chain extraction (Target)
│   │   └── cross_exam.py         # claims-vs-retrieved-passages contradiction detection
│   ├── risk_scorer/
│   │   ├── agent.py
│   │   ├── rubric.yaml           # weighted domains summing to 100, bands, −25 modifier
│   │   └── memo.py               # Gemini Pro risk-memo synthesis (the only model call)
│   ├── watchdog/
│   │   ├── agent.py
│   │   └── sources.py            # allowlisted breach feeds + cert-expiry checks
│   └── shared/
│       ├── gateway.py            # all tool calls route here; policies P1/P2/P3 enforced
│       ├── armor.py              # Model Armor screening + verdict-bearing clean-stamp
│       ├── memory.py             # Memory Bank dossier read/write; structured notes only
│       ├── telemetry.py          # OTel span schema: goal, decision, model, cost
│       └── models.py             # Flash/Pro/embedding/Gemma routing table
├── services/
│   ├── portal/                   # vendor-facing upload + questionnaire UI (Cloud Run)
│   ├── dashboard/                # internal timeline, gates, time-compression control
│   │   └── app/(public)/         # statically rendered · cached reads · NO model import
│   ├── approvals/                # renders gate cards; sole holder of the private key
│   ├── binder/                   # trace query → Audit Binder PDF export (templated)
│   └── vendor_inbox/             # simulated vendor mailbox (honest demo substitute)
├── infra/
│   ├── pubsub.yaml               # 11 topics + subscriptions + DLQs
│   ├── iam/                      # one service account per agent, plus sa-armor
│   ├── model_armor/              # drawbridge-untrusted + drawbridge-output templates
│   ├── deploy/                   # Agent Engine + Cloud Run configs
│   └── budgets.yaml              # alerts at $50 / $100 / $130
├── synthetic-vendors/
│   ├── cleancloud/               # the clean control vendor
│   ├── datadynamo/               # the contradictor (MFA claim vs SOC 2 exceptions)
│   ├── nimbuswrite/              # the adversary — labeled injection payload inside
│   └── injection-corpus/         # 12 labeled variants; CI publishes the detection rate
├── scenarios/
│   └── demo_runner.py            # replays the entire demo end-to-end, deterministically
├── docs/
│   ├── architecture.md           # this document
│   ├── diagrams/                 # the SVGs, incl. the graph_dump.py-generated one
│   └── site/                     # docs website source (see §11)
└── tests/
    ├── test_idempotency.py       # kill mid-step → exactly one email
    ├── test_resume.py            # checkpoint → restart → same end state
    ├── test_armor_flow.py        # payload blocked → flag raised → trust score drops
    ├── test_retier.py            # evidence overrules intake; plan version increments
    ├── test_late_events.py       # out-of-phase events attach, never mutate
    └── test_token_forgery.py     # the gateway cannot mint what it can verify
```

---

## 4. The fleet and its tools

Every capability an agent has is a named tool routed through `shared/gateway.py`, which is what makes the policy story enforceable rather than aspirational. This table is written in the same format as winning submissions use, and belongs verbatim on the docs site.

| Tool | Purpose | Platform component | Example moment in the demo |
|---|---|---|---|
| `send_questionnaire` | Email the tiered question set to a vendor | Gateway policy P1 → email channel | "60 questions sent — after one human tap" |
| `parse_reply` | Incrementally structure replies as they arrive | Gemini 3.5 Flash | "Partial replies, day 3, parsed and checkpointed" |
| `fetch_evidence` | Read screened documents from the clean bucket | Cloud Storage (read-only IAM) | Evidence agent opens the SOC 2 |
| `retrieve_passages` | Top-k passages per claim from the review's own chunks | Firestore KNN + `text-embedding-005` | "Here is the exception note that contradicts them" |
| `screen_content` | Screen all vendor-origin bytes, then scrub for model use | Model Armor + Gemma (in-VPC) | The blocked hidden-text payload |
| `screen_output` | Screen what the fleet itself produces, before a human reads it | Model Armor `drawbridge-output` | The memo checked before the gate card renders |
| `compute_score` | Apply weighted domains → Trust Score 0–100 + band | **`rubric.yaml` only — no model** | "71 · conditional" |
| `reassess_tier` | Re-evaluate tier as evidence arrives; upward only | Flash (free-text classification) + rules | The tier badge changing from 2 to 1 on camera |
| `write_checkpoint` | Persist step state + plan-versioned idempotency key | Firestore ledger | The kill-and-resume segment |
| `recall_dossier` | Load prior history before acting; current view, structured notes only | Memory Bank | The second-review moment |
| `open_rereview` | Reopen an approved vendor on a high-confidence signal | Pub/Sub `watchdog.hit` | Breach headline → review reopened |
| `fetch_url` | Outbound fetch, allowlisted feed domains only | Gateway policy P3 | A blocked non-allowlisted fetch in the console montage |
| `export_binder` | Render traces into the evidence pack — by template, never by a model | Cloud Trace query → PDF | The one-click binder |
| `request_approval` | Park the workflow at a human gate, with its scope recorded | Approval service + asymmetric token | CISO approves with mitigations |

Note what is *not* in this table: there is no `score_rubric` tool. Scoring makes no model call at all — the Evidence agent assigns severity where it is already reading the passage, and `compute_score` is arithmetic over `rubric.yaml`. That division is why "why 71?" always has an answer a human can re-do by hand, and why a self-improving fleet cannot reach its own metric.

---

## 5. One review, end to end

The sequence diagram is the honest version of the demo: five phases spanning days of wall-clock time, in which the fleet acts continuously and humans appear exactly twice — once to authorize first contact (**gate G2**, made unskippable by **gateway policy P1**) and once to make the risk decision (**gate G1**). *(One taxonomy, used everywhere: **gates are what a person does — G1 risk acceptance, G2 first outbound contact. Policies are what the chokepoint enforces — P1 approval token, P2 verdict-bearing stamp, P3 egress allowlist.** G2 is a human act; P1 is the machine's inability to skip it. Nothing is called by both names.)*

Two moments in the sequence separate Drawbridge from a summarizer. The contradiction flag in Phase 3 is the first: the Evidence agent does not summarize the SOC 2, it retrieves the passage relevant to each claim and cross-examines it against what the vendor said in the questionnaire — so the finding cites a chunk it can point at rather than a quotation it hopes it got right. The second is quieter and, to anyone who has run a procurement process, more startling: **the fleet re-tiers the review upward when the vendor's own answers reveal broader data access than the intake form declared.** Tier moves up and never down, the plan version increments, and the timeline records the answer that caused it.

![Review sequence](diagrams/02-review-sequence.svg)

---

## 6. The adversarial content pipeline

The structural insight of the product: a vendor review is an AI system whose inputs are authored by the party being judged. Drawbridge therefore treats every vendor byte as hostile until proven otherwise — quarantine bucket, local text extraction, **Model Armor screening across five detection families through two templates**, an in-VPC Gemma scrub *afterwards* for content on its way to a generative model, and a gateway policy (P2) that refuses to hand a model any content without a **verified, verdict-bearing** clean-stamp.

**The ordering is load-bearing and was wrong in the first design.** Scrubbing before screening meant Model Armor's Sensitive Data Protection filter examined text whose sensitive data had already been removed — it would have returned "no match" on every document forever, without ever erroring. Screening now runs on the real extracted text, and the SDP result tells the scrubber what to scrub. The sovereignty claim survives and is now stated precisely: raw text reaches a *screening service* but never a *generative* model, which is a different trust category.

The defence is five layers, not one, and naming them is what separates an engineering position from a product pitch: **isolation** (quarantine, no agent holds a role on it) → **local extraction** (raw bytes never reach a generative model) → **screening** (fail-closed, two templates, five filters, a skipped detector treated as unscreened) → **enforcement** (P2 verifies the signed verdict; sanitised content is admissible to the Evidence agent and inadmissible to the memo-writing Pro call) → **containment** (the agent that reads evidence has no egress, no email, no approval).

The novel step is what happens after the block: a detected manipulation attempt is not merely stopped, it becomes evidence — **dropping the vendor's Trust Score by 25 points and forcing the review to escalate.** A vendor who attacks your reviewer has answered your questionnaire more honestly than they intended.

Then the assume-breach sentence, which is true today and is the strongest security claim available: **even if an injection reached the Evidence agent, that agent holds no outbound capability and no approval capability. The instruction would have nothing to actuate.**

And the claim is *measured* rather than asserted: twelve injection variants live in `synthetic-vendors/injection-corpus/`, run in CI, with the detection rate published — including the one caught only by output screening and the one (an instruction rendered as an image, with no text layer to extract) not detected at all and bounded by a rule instead. Knowing a blind spot and stating it is a stronger position than claiming there isn't one.

![Injection defense](diagrams/03-injection-defense.svg)

---

## 7. Memory hierarchy

**Four layers, four jobs, four lifetimes.** Session state is disposable by design; the Firestore ledger is the resume point that makes the on-camera kill survivable; the semantic retrieval layer answers a question none of the others can — *which passage says this?*; and Memory Bank is what makes the *second* review of a vendor smarter than the first and what stores organization-level policy ("data processors require SOC 2 Type II").

| Layer | What it holds | Lifetime | The question it answers |
|---|---|---|---|
| **L1** session state, Agent Engine | in-flight reasoning, tool scratchpad | the turn | *what am I doing right now?* |
| **L2** Firestore ledger | reviews, steps, events, findings, `qa_responses`, screenings, approvals, idempotency keys | forever, immutable | *what happened, exactly?* |
| **L2.5** semantic retrieval, Firestore KNN | screened documents chunked, embedded, indexed, pre-filtered by `review_id` | the review | *which passage says this?* |
| **L3** Memory Bank | vendor dossiers, negotiated exceptions, conduct flags, org policy memory | across reviews and years | *what is worth knowing next time?* |

L2.5 exists because a Tier-1 SOC 2 runs 60–100 pages, and a claim about a specific control needs the specific passage rather than the whole document — it turns the hero finding from luck into a query and cuts the most expensive call in the system at the same time. Only clean-stamped content is ever chunked and indexed; retrieval is never on the critical path, and if the index or the embedding call is unavailable the agent logs a degraded-mode warning and falls back to whole-document context.

**L3 accepts structure, not prose — and that is a security control, not a schema preference.** Memory is written from material derived from the party under review, and it is recalled at the *start* of every future review, before any screening runs in that review. So L3 takes only enumerated note types with values from a controlled vocabulary and a provenance tag (`human`, `rule`, `model_structured`); free text derived from vendor content never enters it. Notes supersede rather than accumulate, and `recall_dossier` returns the current view. A review that needs the vendor's exact wording reads L2, where it sits behind the screening record that describes it.

The one-line framing for judges and the blog: persistence is not memory — and memory is a write path an attacker would like to reach.

![Memory hierarchy](diagrams/04-memory-hierarchy.svg)

---

## 8. Security architecture

Defense in depth across five layers, with the per-agent permission matrix as the centerpiece — and the matrix is written at **collection level**, not service level, because a row that says "Firestore" cannot express the difference between the `qa_responses` the Questionnaire agent must write and the `findings` it must never touch. Vague permission rows are how least-privilege claims quietly become false.

| Identity | Granted | Never granted |
|---|---|---|
| `sa-orchestrator` | Firestore review state read/write, Pub/Sub, Vertex AI | email, Storage, `approvals` write |
| `sa-questionnaire` | `qa_responses` read/write, portal write, email *via gateway*, Pub/Sub, Vertex AI | `findings`/`scores`/`approvals` write, Storage read |
| `sa-evidence` | clean bucket read-only, `evidence_chunks` read/write, `findings` write, Vertex AI | **any** egress, email, quarantine bucket |
| `sa-scorer` | Firestore read, `scores` write, Vertex AI | external calls, `approvals` write |
| `sa-watchdog` | Pub/Sub publish, outbound fetch *via gateway allowlist*, task write | approvals, email, vendor data write |
| `sa-armor` (screening pipeline) | quarantine read, clean write, `screenings` write, `modelarmor.user` | any generative model call, email, `findings` write |

The agent that reads evidence has no email permission and no network egress; the agent that emails cannot write a finding or a score; the component that handles the rawest, most hostile bytes in the system is the one component structurally incapable of prompting anything; and nobody but a named human can approve a vendor.

Policies live at the gateway chokepoint, not in prompts — prompt hygiene is a courtesy, IAM is a guarantee. There are **three** of them, which makes it a policy system rather than a pair of special cases: **P1** an approval token for outbound email to a new contact, **P2** a verdict-bearing clean-stamp before any external content reaches a model, **P3** an allowlist on outbound fetch, because an agent with unbounded egress is an exfiltration channel.

**Approval tokens are asymmetric**, and this is the sentence to remember: the private signing key lives only in the approval service that renders the gate card, and the gateway holds the public key. If both sides shared a secret, anything that could verify could also forge — and the gateway is reachable by every agent in the fleet. Rotation publishes a new public key. **The gateway can recognise a human decision but is structurally incapable of manufacturing one.**

![Security architecture](diagrams/05-security-architecture.svg)

---

## 9. Data architecture

Firestore is the append-heavy workflow ledger; the diagram doubles as the schema reference for the repo. Three design points worth stating in every writeup. The `events` collection is an ordered, immutable log (which is why the Audit Binder can be *generated* rather than assembled by hand). Every side-effecting step writes its idempotency key before executing, and the key is **`review_id : plan_vN : step_id`** — the plan version is in there because a re-tiered review is re-planned mid-flight, and a step name that meant one thing in plan v1 must not silently satisfy a different step in plan v2 (the "two laptops" trap from the organizers' own webinar, answered in the schema itself). And `evidence_chunks` carries a KNN vector index composite with `review_id`, so retrieval is pre-filtered to one review's own evidence.

Review states advance monotonically — `intake → questionnaire_out → replies_in → evidence_review → scored → gated → decided → monitored` — with three deliberate exceptions the transition table encodes explicitly: `NEEDS_HUMAN` is reachable from **every** state, because a documented failure path that cannot execute is worse than one never written down; `gated` carries a **`gate_scope`** of `contact` or `decision`, since a review parks at two different gates for two different humans; and a **re-tier moves a review backwards on purpose** (`replies_in → questionnaire_out`) to send the additional domain's questions, incrementing the plan version and writing a `TierChange` that names the evidence. Tier only ever moves up — a downward re-tier is an attack surface.

Pub/Sub gives at-least-once delivery and **no ordering guarantee**, so every consumer checks review state before acting: a reply arriving after `SCORED` attaches as an addendum and reopens the score rather than being discarded; `evidence.screened` arriving before a plan exists parks and retries; a `watchdog.hit` on an already-reopened review deduplicates on signal id; and any event for a `DECIDED` review appends to the ledger and never mutates, because a decided review is immutable.

![Data model](diagrams/07-data-model.svg)

---

## 10. Deployment architecture and technology decisions

![Deployment architecture](diagrams/06-deployment-architecture.svg)

The decision log, in the form judges reward — choice, reason, rejected alternative:

| Area | Choice | Why | Rejected alternative |
|---|---|---|---|
| Agent framework | **ADK 2 (Python) as a graph workflow**, on Agent Engine | Required-tech alignment; managed long-running sessions; Memory Bank integration. A graph workflow is the pattern for work whose structure is known before the input arrives, which a tiered review plan is | ADK 2's other two patterns: *collaborative agents* (the team is known but the request picks the subset — our subset is decided by tier, before the vendor speaks) and *dynamic workflows* (shape depends on the input — which would make the plan unauditable). Self-hosted loop on GKE — more ops, no platform story |
| Default model | Gemini 3.5 Flash everywhere | Mirrors organizers' cost guidance; <$0.50/review is a headline metric | Pro-everywhere — 10× cost, no visible quality gain on parsing |
| Synthesis model | Gemini Pro for memos + contradictions, and nowhere else | The two places reasoning depth is user-visible | Flash — memos read noticeably thinner. Also rejected: Pro for orchestration, so that "Pro is spent in exactly two places" stays true |
| Scoring | **No model call at all** — the Evidence agent assigns severity, Python computes the score from `rubric.yaml` | Reproducible in the demo; defensible when a judge asks "why 71?"; showable as arithmetic in the binder; and it means no agent holds the pen on its own metric, which is the whole answer to the self-improvement webinar | A Flash `score_rubric` call — cheaper to write, and it would have quietly undone the strongest architectural claim in the project |
| Evidence retrieval | Chunk, embed with `text-embedding-005`, index in Firestore KNN, retrieve top-k per claim | A Tier-1 SOC 2 runs 60–100 pages; the hero finding becomes a query rather than a hope, `evidence_ref` becomes a real pointer, and Pro context shrinks — the layer pays for itself | Whole-document Pro context — unreliable at 100 pages and the most expensive call in the system. Kept as the degraded-mode fallback |
| PII handling | Gemma scrubber inside the VPC, **after** Model Armor screens | Sovereignty story + the Gemma bonus, earned honestly — and the SDP hits tell the scrubber what to scrub | Scrub-then-screen, the original design: it blinds the SDP filter permanently and silently. Cloud DLP only — fine, but no bonus and weaker narrative |
| Events | Pub/Sub between all agents | Autonomy = event-driven; any agent can die without stalling the fleet | Direct RPC — couples agents, breaks the resume story |
| State | Firestore ledger + explicit checkpoints; plan-versioned idempotency keys | Exactly-once side effects; resume from any crash; a re-planned review cannot collide with its own history | Agent memory alone — "persistence is not memory". Keys without a plan version — correct only while the plan is immutable |
| Identity | One service account per agent plus one for the screening pipeline, at **collection level** | The security demo *is* the IAM console screenshot, and collection-level rows are the ones that catch drift | Shared SA — one injection from disaster. Service-level rows — they read as least privilege while permitting more than they say |
| Human approval | **Asymmetric** signing: private key in the approval service, public key at the gateway | The gateway can recognise a human decision but cannot manufacture one — a structural property rather than a policy | A shared symmetric secret: anything that can verify can also forge, and every agent can reach the gateway |
| Public surface | Statically rendered entry page, cached reads, **no model path**, min-instances 0 | The rules require a URL that loads logged-out; the organizers require credits not be drained. A static page cold-starts in ~1s, so both hold | A warm dashboard instance during judging — pays continuously for a second of cold start and leaves the token path open |
| Frontend | Next.js + Tailwind on Cloud Run | Fast for a solo builder; scale-to-zero; hosted URL for judges | Streamlit — faster but reads as a prototype |
| Email | Simulated vendor inbox service | Deterministic demo; honestly labeled in README | Real SMTP — deliverability risk during judging week |
| Guardrail claim | A twelve-variant injection corpus run in CI, detection rate published | Everything else makes the defence better; this makes it *evaluated*, which is a different category of claim | One fixture and an anecdote — enough for a demo, not enough for a company |
| Dev tooling | Claude Code (development only) | Solo force multiplier; the product itself calls only Google models | — |

Two entries in this log that are positions rather than choices, both of which belong on the Security page of the docs site:

**Adversarial content defence.** Model Armor is one layer of five, not the defence. It runs at HIGH confidence across five detection families through two templates, it fails closed (a skipped detector is treated as unscreened, not as clean), and its verdict travels in a signed stamp so the gateway can enforce policy on *what screening said* rather than merely *that screening happened*. The fleet also screens **its own outputs** — the risk memo and outbound mail — before a human reads them, which is the only control in the system that assumes all the earlier ones failed.

**Bounded self-improvement.** The fleet may improve **how it asks**, never **how it scores**. At review close, memory records which questions produced low-confidence parses or non-answers, and the next review prefers the phrasings that produced usable evidence. Scoring is arithmetic over model-assigned severities, so a self-improving agent cannot game a score it does not compute. Question phrasing is the one place learning is safe, because a bad question produces a visible gap rather than a silently wrong number.

![Technology stack](diagrams/08-tech-stack.svg)

---

## 11. The docs site plan

The inspiration project's docs site is a large part of why it read as production-grade, and it is cheap to replicate: a Nextra or Docusaurus site in `docs/site/`, deployed to GitHub Pages (the *product* must run on Google Cloud; the documentation can live anywhere). Navigation, mirroring what worked: **Home** (one-paragraph pitch, hero diagram, Live Demo button, Download/Repo buttons) · **Getting Started** (the README spin-up, deployment diagram) · **Architecture** (this document, all eight diagrams) · **Security** (diagrams 03 + 05 — our differentiator deserves its own page) · **Live Demo** (link to the hosted Cloud Run dashboard). Add a "Built for the All Things Agentic Hackathon" line in the footer, and link the docs site from the Devpost submission, the README, and the Medium article so every surface reinforces the others.
