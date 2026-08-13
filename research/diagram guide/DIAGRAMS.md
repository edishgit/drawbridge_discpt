# Drawbridge — Diagram Set

Twenty-four diagrams generated from `drawbridge-hackathon-master-doc.md` and `drawbridge-implementation-handbook.md`.
Every claim in every diagram traces back to a decision in one of those two documents — nothing here is invented.

**Amendments 01–03 have been applied to the sources.** Every `.mmd` in `src/` is current; **the PNGs and SVGs are not** — they were exported before the amendments and must be regenerated (see *Regenerating*, below). Diagram **23** is deliberately absent from `src/`: it is not hand-drawn.

**Three formats per diagram**

| Folder | Use it for |
|---|---|
| `src/*.mmd` | Mermaid source. Paste into your docs site (it renders Mermaid natively, as in your screenshots), into the repo's `docs/diagrams/`, and into GitHub README files — GitHub renders Mermaid in Markdown. |
| `png/*.png` | Retina-scale PNG on white. **Use these for Medium** (it rejects SVG), for the Devpost gallery, and for LinkedIn/X. |
| `svg/*.svg` | Transparent vector. Use for the docs site if you want theme-independent assets, and for anything that will be zoomed. |

---

## Where each diagram goes

| # | Diagram | Devpost | Medium | Docs site | Video |
|---|---|---|---|---|---|
| 01 | System architecture | ★ gallery image 1 | ★ hero image | Architecture (canonical) | 3:10 console montage |
| 02 | The fleet on one page | ★ gallery image 2 | ★ opening explainer | Home / Getting started | 0:25 setup |
| 03 | Review lifecycle sequence (J1) | "What it does" | "Why a fleet, not a chatbot" | Architecture | narration spine |
| 04 | Adversarial content defense | ★ gallery image 3 | ★ the money-shot section | Security | 1:45 injection beat |
| 05 | Kill and resume | "How I built it" | ★ the idempotency-trap section | Architecture | 2:20 crash beat |
| 06 | Memory hierarchy | "What I learned" | deep-dive #2 | Architecture | — |
| 07 | Event backbone | "How I built it" | deep-dive #2 | Architecture | — |
| 08 | Review state machine | "How I built it" | deep-dive #2 | Architecture | 2:50 gate beat |
| 09 | Zero-trust permissions | ★ gallery image 4 | the five decisions | Security | 3:10 IAM console |
| 10 | Risk scoring pipeline | "What it does" | the five decisions | Architecture | 2:50 memo |
| 11 | Audit binder composition | "Accomplishments" | ★ the binder section | Architecture / Live demo | 3:10 export |
| 12 | Technology stack | ★ tech-stack gallery image | closing section | Home | — |
| 13 | Firestore data model | — | deep-dive #2 | Architecture | — |
| 14 | Deployment and cost | — | "what GEAP made easy vs hard" | Getting started | 3:10 Cloud Run |
| 15 | Twenty-day build plan | "Challenges" | ★ the honest-process section | — | — |
| 16 | Synthetic vendor pack | "Other data sources" | reproducibility section | Getting started | — |
| 17 | Approval-token lifecycle | "How I built it" | the human-approval section | Security | 1:05 G2 gate |
| 18 | Personas and adoption (J6) | ★ "What it does" | why a fleet is adoptable | Home | 0:25 registry |
| 19 | Questionnaire loop | "Challenges" | incremental-parsing challenge | Architecture | — |
| 20 | Failure semantics | ★ "How I built it" | the five decisions | Architecture / Security | — |
| 21 | Tests, claims and demo beats | ★ "Accomplishments" | the testing section | Getting started | — |
| 22 | Demo shot map | — | — | — | ★ your own shooting plan |
| 23 | ADK 2 graph dump *(generated, not drawn)* | "How I built it" | the orchestration section | Architecture | — |
| 24 | The fourth-party chain *(Target)* | ★ "What it does" | the fourth-party section | Architecture / Security | — |

★ = the ones worth the most; if you only ship five images, ship **01, 02, 04, 09, 12**.

Diagram 22 is a working document for you, not an audience artefact — it belongs in your notes, not in the submission.

---

## The diagrams

### 01 · System architecture
Eight numbered trust zones, top to bottom: untrusted → ingress screening → event backbone → agent runtime → tool and model plane → state and memory → human gates → governance. The two red-flagged paths are the ones judges should notice: the blocked payload becoming a risk signal, and the fact that no `DECIDED` state exists without a named human. This is your canonical architecture image; it replaces the layered zone sketch referenced in §9 of the master doc.

### 02 · The fleet on one page
The thirty-second version for anyone who won't read the architecture. Intake → Orchestrator → Questionnaire → **G2** first-contact gate (enforced by policy **P1**) → vendor → Model Armor → (clean → Evidence | hostile → Adversarial Conduct) → Risk Scorer → **G1** gate → Watchdog + binder. Gates are what a person does; policies are what the chokepoint enforces — the diagram now names each by only one of the two.

### 03 · Review lifecycle sequence (J1)
Ten participants, four colour-banded phases with day markers, ending on the metric: fifteen days of vendor time, under one hour of human time. Note beat 6 — the gateway blocking its own agent's email until a human authorises first contact.

### 04 · Adversarial content defense
The signature feature as a pipeline, with both branches drawn: clean documents get stamped, hostile ones get blocked, stripped, stored inert, flagged, and *rescored*. The italic callout at the end is the sentence for the video: a vendor who tries to manipulate your reviewer has told you something material.

### 05 · Kill and resume
Four bands: normal claim-before-effect execution, SIGKILL, restart with the idempotency ledger returning the recorded result, and the conservative case — a crash between claim and effect surfaces for human reconciliation rather than blind resend.

### 06 · Memory hierarchy
L1 session / L2 Firestore / L3 Memory Bank, each labelled with its lifetime and the question it answers, plus the distillation rule and the explicitly rejected anti-pattern.

### 07 · Event backbone
Nine topics, their publishers and consumers, the shared envelope, and the DLQ path to `NEEDS_HUMAN`.

### 08 · Review state machine
Every allowed transition, `NEEDS_HUMAN` reachable from anywhere, and the note that a reopened review is a new linked record — history is never mutated.

### 09 · Zero-trust permissions
Five identities, their capabilities, and the never-granted column, with the denials drawn as dotted red edges. Pair it on screen with `tests/test_iam_boundaries.py` failing as expected.

### 10 · Risk scoring pipeline
Weighted domains → deterministic Python arithmetic → adversarial modifier → band → one Pro-written memo → human gate. The point of the diagram is the split: the model judges severity, the code computes the score.

### 11 · Audit binder composition
Six sources that already exist because the review ran, one generator, a cover plus eight sections, and the compliance mapping that reframes logs as the artefact an auditor asks for.

### 12 · Technology stack
Mindmap across platform, models, framework, infrastructure, observability, security, frontend, and engineering discipline. This is the "Technologies" field on Devpost in picture form.

### 13 · Firestore data model
Thirteen collections with the fields that carry the architecture: `completed_steps`, `idem_key`, `matched_excerpt`, `reopened_from`, per-review `cost_usd`, and span `goal`/`decision`.

### 14 · Deployment and cost
Workstation → Makefile → Cloud Build → Agent Engine and five Cloud Run services, with the cost-engineering band and the day-one hello-world rule called out.

### 15 · Twenty-day build plan
Gantt across the four phases with M1, M2, the webinars and the deadline as milestones; critical-path items in red.

### 17 · Approval-token lifecycle
The §14 primitive drawn end to end — an agent blocked at the gateway, the human signing a scoped single-use token, the effect happening once, and both replay and privilege escalation failing closed. The last note is the line to narrate: even a compromised agent cannot email or approve, because the capability requires a signed human artefact it cannot forge.

### 18 · Personas and adoption
The five personas from §5.2 arranged around the fleet, with J6 drawn explicitly — Legal discovering the published agent in the Registry and the governance that lets the answer be yes. This is the cross-department story the track brief asks for, and nothing else in the set depicts it.

### 19 · Questionnaire loop
The hardest-to-explain agent: bank-driven generation, the no-yes/no style rule, reply-body screening, incremental merge with confidence and provenance, the 90 percent coverage threshold, three capped chase rounds, and the two exits that lead to a human rather than a guess.

### 20 · Failure semantics
Per-agent failure behaviour on the left, platform-level fallbacks on the right, and the principle in the middle. "Documented failure behaviour per agent" is an explicitly graded item under Architectural Discipline, and this is the picture of it.

### 21 · Tests, claims and demo beats
Each of the five tests, the architectural claim it defends, and the moment in the video where a judge watches that claim be true. Useful to you as a build check and to a judge as proof the demo isn't theatre.

### 22 · Demo shot map
Your 3:55 laid out against the clock, with the four pillars as milestones and the unbroken live take marked. The re-tier beat now sits at 1:35, on footage already being shot — the tier badge simply changes on a screen the camera is pointed at. A working document — keep it out of the submission.

### 23 · ADK 2 graph dump — generated, not drawn
**There is no `src/23-*.mmd`, and there should not be.** This diagram is the output of the ADK 2 codelab's `scripts/graph_dump.py` pointed at the Orchestrator, committed to `docs/diagrams/` with a caption stating plainly that it was generated from the workflow code. A picture produced by the repo is the strongest possible answer to *"does the diagram match the code?"* — a claim no hand-drawn diagram can make. Regenerate it after any ADK version bump; a drift shows up immediately, which is half the value.

```bash
python scripts/graph_dump.py --workflow agents.orchestrator:workflow \
       --out docs/diagrams/23-adk2-graph-dump.svg
```

### 24 · The fourth-party chain *(Target)*
You → the vendor → their subprocessors, with the unknown ones in red. Structured extraction into a `subprocessors` collection, then a deterministic set-difference against the approved-vendor register, producing `source="rule"` findings for every unknown fourth party that processes customer data. It is the thesis applied recursively: *your attack surface is now other companies* — and the vendor's model provider processes your customer text too, a company you never reviewed and never signed anything with.

Marked **(Target)** and deliberately kept out of the video: the demo is full at 3:55 and the four pillars are not negotiable. This one lives in the README, the binder and a gallery image.

### 16 · Synthetic vendor pack
CleanCloud, DataDynamo and NimbusWrite with what each proves and what the scenario tests assert — the reproducibility story, including the honesty note about the payload.

---

## Regenerating

**Outstanding after Amendments 01–03: every PNG and SVG in this set is stale.** The `.mmd` sources are current; the exports are not. Sixteen diagrams changed (01, 02, 03, 04, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22) and one is new (24). Run the loop below before publishing anything.

```bash
npm install -g @mermaid-js/mermaid-cli
npx puppeteer browsers install chrome            # if no local Chrome

# regenerate everything — the only safe option after an amendment pass
for f in src/*.mmd; do
  n=$(basename "$f" .mmd)
  mmdc -i "$f" -o "png/$n.png" -c mermaid-config.json -b white -s 2 -w 2000
  mmdc -i "$f" -o "svg/$n.svg" -c mermaid-config.json -b transparent
done

# or one at a time
# PNG for Medium / Devpost / socials
mmdc -i src/01-system-architecture.mmd -o png/01-system-architecture.png \
     -c mermaid-config.json -b white -s 2 -w 2000

# SVG for the docs site
mmdc -i src/01-system-architecture.mmd -o svg/01-system-architecture.svg \
     -c mermaid-config.json -b transparent

# 23 is NOT regenerated this way — it comes from the code
python scripts/graph_dump.py --workflow agents.orchestrator:workflow \
       --out docs/diagrams/23-adk2-graph-dump.svg
```

`mermaid-config.json` holds the shared theme: Inter, slate line colour, 460px label wrapping. Keep it in `docs/diagrams/` so every future diagram matches.

## Colour language (used consistently across the whole set)

| Colour | Means |
|---|---|
| Red | untrusted, hostile, or explicitly forbidden |
| Amber | screening and policy configuration |
| Blue | agents and inputs |
| Purple | gateway policies and models |
| Green | verified, durable, or safe state |
| Orange | humans and human gates |
| Slate | governance, observability, evidence |

## Corrections applied — the four contradictions, now resolved in the source documents

These four were found by checking every diagram against both documents. They were contradictions inside the docs rather than diagram errors, and all four have since been fixed at source (Amendment 01, D1–D4):

1. **`GATED` was doing two jobs.** §9 said an unapproved first contact "parks the review in GATED", but the §5.2 transition table only allowed `SCORED → GATED → DECIDED`. **Resolved:** `GATED` carries a `gate_scope` of `contact` or `decision`, and the `ALLOWED` table now includes `QUESTIONNAIRE_OUT → GATED → QUESTIONNAIRE_OUT`. Diagram 08 shows both scopes and names which human gate each belongs to.
2. **`review.rescore` was missing from the topic table.** §11.3 published it; §6.1 didn't list it. **Resolved:** both `review.rescore` and `watchdog.sweep` are now in the topic table, in `bootstrap.sh`, and in diagram 07 — eleven topics, all documented. Undocumented meant untested.
3. **`NEEDS_HUMAN` from anywhere.** §5.2's prose said it was enterable from any state; the table omitted `SCORED`, `GATED`, `DECIDED` and `MONITORED`. **Resolved:** the table now matches the prose, which was always the safer design. A documented failure path that cannot execute is worse than one never written down.
4. **The Tier-1 rubric summed to 95, not 100.** **Resolved:** subprocessor & fourth-party chain rose from 10 to 15, so the domains total exactly 100 and the bands (≥80 / 60–79 / <60) are arithmetically true as percentages rather than approximately so. The extra weight landed on the domain the Evidence agent's subprocessor extraction is built to feed. Diagram 10 shows the new weights.

**Terminology, fixed everywhere:** the number is the **Trust Score, 0–100, higher is safer**. Prose may say a vendor *raised your risk*; the score always *falls*. No diagram, wireframe or piece of copy now says a score was "raised" by an injection. And **gates are distinct from policies** — G1 risk acceptance and G2 first outbound contact are human acts; P1 approval token, P2 verdict-bearing stamp and P3 egress allowlist are gateway enforcement. G2 is a human act; P1 is the machine's inability to skip it. Nothing is called by both names.

**Structural changes from the amendments, now in the sources:** the screening pipeline screens **before** it scrubs (04, 01, 03) — the old order would have blinded the SDP filter permanently; the memory hierarchy has **four** layers with the semantic retrieval tier inserted (06, 01); the permission matrix is stated at **collection level** and gains `sa-armor` (09); there are **three** gateway policies (01, 09, 12); approval tokens are **asymmetric** (17); the state machine carries the re-tier transitions (08); the event backbone documents late and out-of-order behaviour (07); and the failure-semantics diagram draws the line between controls that **degrade** and controls that **fail closed** (20).

Also corrected earlier: the permission matrix matches handbook §3.2 grant-for-grant and denial-for-denial, and notes the service identities beyond the agents; and the J1 day markers were re-based so the sequence ends on "about three days", matching the metrics card, instead of implying a fifteen-day cycle.

Two deliberate omissions: the **Contract Clause agent** appears nowhere, because it is stretch and first on the cut list — add it to 01 and 02 only if it survives. **Veo and Lyria** likewise, per §10's rejection of forced integrations.

And one deliberate absence a diagram cannot draw: **there is no edge from the public read-only surface to the model plane in diagram 01**, and that absence is the point. No route reachable without a token may reach the model router. A diagram cannot draw an edge that isn't there, so it is stated here, in the guide text, and in handbook §16.5 as a grep you can put in CI.

## Two notes before you publish

Diagram 01 shows the Gemma scrubber and diagram 12 lists it under models — both are marked stretch in the handbook, and §13's honesty rule applies: **if it isn't built, delete it from the diagram before publishing.** Same for the Watchdog live feed in 07 and 16, the targeted follow-up in 19, the subprocessor extraction in 16, and all of diagram 24 — every one of those is marked **(Target)** or **(Stretch)** in master doc §5.6, and a diagram is not the place to promise something the build didn't ship. Delete, don't grey out.

If a GEAP component turns out to be unavailable in your region (risk #1 in the register), change the node label in the source rather than leaving the diagram aspirational — `Model Armor` becomes `Screening service · same contract, X implementation`. The architecture story survives that edit; a diagram that doesn't match the repo does not.
