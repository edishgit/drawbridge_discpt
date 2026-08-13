# Drawbridge — Diagram Set

Twenty-two diagrams generated from `drawbridge-hackathon-master-doc.md` and `drawbridge-implementation-handbook.md`.
Every claim in every diagram traces back to a decision in one of those two documents — nothing here is invented.

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
| 17 | Approval-token lifecycle | "How I built it" | the human-approval section | Security | 1:05 P1 gate |
| 18 | Personas and adoption (J6) | ★ "What it does" | why a fleet is adoptable | Home | 0:25 registry |
| 19 | Questionnaire loop | "Challenges" | incremental-parsing challenge | Architecture | — |
| 20 | Failure semantics | ★ "How I built it" | the five decisions | Architecture / Security | — |
| 21 | Tests, claims and demo beats | ★ "Accomplishments" | the testing section | Getting started | — |
| 22 | Demo shot map | — | — | — | ★ your own shooting plan |

★ = the ones worth the most; if you only ship five images, ship **01, 02, 04, 09, 12**.

Diagram 22 is a working document for you, not an audience artefact — it belongs in your notes, not in the submission.

---

## The diagrams

### 01 · System architecture
Eight numbered trust zones, top to bottom: untrusted → ingress screening → event backbone → agent runtime → tool and model plane → state and memory → human gates → governance. The two red-flagged paths are the ones judges should notice: the blocked payload becoming a risk signal, and the fact that no `DECIDED` state exists without a named human. This is your canonical architecture image; it replaces the layered zone sketch referenced in §9 of the master doc.

### 02 · The fleet on one page
The thirty-second version for anyone who won't read the architecture. Intake → Orchestrator → Questionnaire → P1 gate → vendor → Model Armor → (clean → Evidence | hostile → Adversarial Conduct) → Risk Scorer → G1 gate → Watchdog + binder.

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
Your 3:55 laid out against the clock, with the four pillars as milestones and the unbroken live take marked. A working document — keep it out of the submission.

### 16 · Synthetic vendor pack
CleanCloud, DataDynamo and NimbusWrite with what each proves and what the scenario tests assert — the reproducibility story, including the honesty note about the payload.

---

## Regenerating

```bash
npm install -g @mermaid-js/mermaid-cli
npx puppeteer browsers install chrome            # if no local Chrome

# PNG for Medium / Devpost / socials
mmdc -i src/01-system-architecture.mmd -o png/01-system-architecture.png \
     -c mermaid-config.json -b white -s 2 -w 2000

# SVG for the docs site
mmdc -i src/01-system-architecture.mmd -o svg/01-system-architecture.svg \
     -c mermaid-config.json -b transparent
```

`mermaid-config.json` holds the shared theme: Inter, slate line colour, 460px label wrapping. Keep it in `docs/diagrams/` so every future diagram matches.

## Colour language (used consistently across all sixteen)

| Colour | Means |
|---|---|
| Red | untrusted, hostile, or explicitly forbidden |
| Amber | screening and policy configuration |
| Blue | agents and inputs |
| Purple | gateway policies and models |
| Green | verified, durable, or safe state |
| Orange | humans and human gates |
| Slate | governance, observability, evidence |

## Corrections applied — and four things to fix in the source documents

These were found by checking every diagram against both documents. Four are contradictions inside your own docs, not diagram errors, and they need fixing in the source before you build:

1. **`GATED` is doing two jobs.** §9 says an unapproved first contact "parks the review in GATED", but the §5.2 transition table only allows `SCORED → GATED → DECIDED`. Diagram 08 resolves it by giving `GATED` a `gate_scope` of `contact` or `decision`, with `QUESTIONNAIRE_OUT → GATED → QUESTIONNAIRE_OUT` added. Update the `ALLOWED` table to match, or the first thing your state validator does in the demo is raise.
2. **`review.rescore` is missing from the topic table.** §11.3 publishes it; §6.1 doesn't list it. Diagram 07 includes it, plus the `watchdog.sweep` trigger implied by §12's Cloud Scheduler path. Add both to §6.1.
3. **`NEEDS_HUMAN` from anywhere.** §5.2's prose says it is enterable from any state; the table omits it from `SCORED`, `GATED`, `DECIDED` and `MONITORED`. The diagrams follow the prose, which is the safer design. Fix the table.
4. **The Tier-1 rubric sums to 95, not 100.** Appendix B: 20 + 15 + 15 + 15 + 10 + 10 + 10. Diagram 10 no longer claims 100 points. Either add five points somewhere or state the scale as 95 — it matters because the binder shows the arithmetic, and the bands (≥80 / 60–79 / <60) read as percentages of 100.

Also corrected in the diagrams: the permission matrix now matches §3.2 grant-for-grant and denial-for-denial, and notes the three service identities beyond the five agents; and the J1 day markers were re-based so the sequence ends on "about three days", matching your own metrics card, instead of implying a fifteen-day cycle.

Two deliberate omissions: the **Contract Clause agent** appears nowhere, because it is stretch and first on the cut list — add it to 01 and 02 only if it survives. **Veo and Lyria** likewise, per §10's rejection of forced integrations.

## Two notes before you publish

Diagram 01 shows the Gemma scrubber and diagram 12 lists it under models — both are marked stretch in the handbook, and §13's honesty rule applies: **if it isn't built, delete it from the diagram before publishing.** Same for the Watchdog live feed in 07 and 16.

If a GEAP component turns out to be unavailable in your region (risk #1 in the register), change the node label in the source rather than leaving the diagram aspirational — `Model Armor` becomes `Screening service · same contract, X implementation`. The architecture story survives that edit; a diagram that doesn't match the repo does not.
