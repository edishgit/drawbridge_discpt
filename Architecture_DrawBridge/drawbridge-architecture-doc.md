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

Drawbridge is organized as seven horizontal layers, and the architecture's core claim is that a request only moves *downward* through increasing levels of trust: actors interact with Cloud Run surfaces; every vendor-origin byte crosses a screening boundary (in-VPC Gemma scrub, then Model Armor) before it may touch a model; every agent call passes the Agent Gateway's named policies; all lifecycle transitions travel as Pub/Sub events so no agent ever polls or blocks on another; the fleet itself runs on Vertex AI Agent Engine as long-running, resumable, idempotent workers; durable state and long-term memory live in their own layer; and everything the fleet does lands in the governance layer, where reasoning traces become the Audit Binder. Removing any single component degrades the system gracefully instead of breaking it — the property the sequence and failure sections below make concrete.

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
│   │   └── cross_exam.py         # claims-vs-answers contradiction detection
│   ├── risk_scorer/
│   │   ├── agent.py
│   │   ├── rubric.yaml           # weighted domains, bands, Adversarial Conduct −25
│   │   └── memo.py               # Gemini Pro risk-memo synthesis
│   ├── watchdog/
│   │   ├── agent.py
│   │   └── sources.py            # breach feeds + cert-expiry checks
│   └── shared/
│       ├── gateway.py            # all tool calls route here; policies P1/P2 enforced
│       ├── armor.py              # Model Armor screening client + clean-stamp
│       ├── memory.py             # Memory Bank dossier read/write
│       ├── telemetry.py          # OTel span schema: goal, decision, model, cost
│       └── models.py             # Flash/Pro/Gemma routing table
├── services/
│   ├── portal/                   # vendor-facing upload + questionnaire UI (Cloud Run)
│   ├── dashboard/                # internal timeline, gates, time-compression control
│   ├── binder/                   # trace query → Audit Binder PDF export
│   └── vendor_inbox/             # simulated vendor mailbox (honest demo substitute)
├── infra/
│   ├── pubsub.yaml               # topics + subscriptions
│   ├── iam/                      # one service account per agent + role bindings
│   ├── deploy/                   # Agent Engine + Cloud Run configs
│   └── budgets.yaml              # alerts at $50 / $100 / $130
├── synthetic-vendors/
│   ├── cleancloud/               # the clean control vendor
│   ├── datadynamo/               # the contradictor (MFA claim vs SOC 2 exceptions)
│   └── nimbuswrite/              # the adversary — labeled injection payload inside
├── scenarios/
│   └── demo_runner.py            # replays the entire demo end-to-end, deterministically
├── docs/
│   ├── architecture.md           # this document
│   ├── diagrams/                 # the 8 SVGs
│   └── site/                     # docs website source (see §11)
└── tests/
    ├── test_idempotency.py       # kill mid-step → exactly one email
    ├── test_resume.py            # checkpoint → restart → same end state
    └── test_armor_flow.py        # payload blocked → flag raised → score drops
```

---

## 4. The fleet and its tools

Every capability an agent has is a named tool routed through `shared/gateway.py`, which is what makes the policy story enforceable rather than aspirational. This table is written in the same format as winning submissions use, and belongs verbatim on the docs site.

| Tool | Purpose | Platform component | Example moment in the demo |
|---|---|---|---|
| `send_questionnaire` | Email the tiered question set to a vendor | Gateway policy P1 → email channel | "60 questions sent — after one human tap" |
| `parse_reply` | Incrementally structure replies as they arrive | Gemini 3.5 Flash | "Partial replies, day 3, parsed and checkpointed" |
| `fetch_evidence` | Read screened documents from the clean bucket | Cloud Storage (read-only IAM) | Evidence agent opens the SOC 2 |
| `screen_content` | Scrub then screen all vendor-origin bytes | Gemma (in-VPC) + Model Armor | The blocked hidden-text payload |
| `score_rubric` | Apply weighted domains → 0–100 + band | Flash + `rubric.yaml` | "71 · conditional" |
| `write_checkpoint` | Persist step state + idempotency key | Firestore ledger | The kill-and-resume segment |
| `recall_dossier` | Load prior history before acting | Memory Bank | The second-review moment |
| `open_rereview` | Reopen an approved vendor on new signal | Pub/Sub `watchdog-hit` | Breach headline → review reopened |
| `export_binder` | Render traces into the evidence pack | Cloud Trace query → PDF | The one-click binder |
| `request_approval` | Park the workflow at a human gate | Dashboard + approval token | CISO approves with mitigations |

---

## 5. One review, end to end

The sequence diagram is the honest version of the demo: five phases spanning days of wall-clock time, in which the fleet acts continuously and humans appear exactly twice — once to authorize first contact (P1) and once to make the risk decision (G1). The contradiction flag in Phase 3 is the moment that separates Drawbridge from a summarizer: the Evidence agent does not summarize the SOC 2, it cross-examines it against what the vendor claimed in the questionnaire.

![Review sequence](diagrams/02-review-sequence.svg)

---

## 6. The adversarial content pipeline

The structural insight of the product: a vendor review is an AI system whose inputs are authored by the party being judged. Drawbridge therefore treats every vendor byte as hostile until proven otherwise — quarantine bucket, in-VPC Gemma PII scrub, Model Armor screening, and a gateway policy (P2) that refuses to hand any unstamped content to a model. The novel step is the last one: a detected manipulation attempt is not merely blocked, it becomes evidence, dropping the vendor's score by 25 points and escalating the review. A vendor who attacks your reviewer has answered your questionnaire more honestly than they intended.

![Injection defense](diagrams/03-injection-defense.svg)

---

## 7. Memory hierarchy

Three layers, three jobs, three lifetimes. Session state is disposable by design; the Firestore ledger is the resume point that makes the on-camera kill survivable; Memory Bank is what makes the *second* review of a vendor smarter than the first and what stores organization-level policy ("data processors require SOC 2 Type II"). The one-line framing for judges and the blog: persistence is not memory.

![Memory hierarchy](diagrams/04-memory-hierarchy.svg)

---

## 8. Security architecture

Defense in depth across five layers, with the per-agent permission matrix as the centerpiece: the agent that reads evidence has no email permission and no network egress; the agent that emails cannot touch internal data; nobody but a named human can approve a vendor. Policies live at the gateway chokepoint, not in prompts — prompt hygiene is a courtesy, IAM is a guarantee.

![Security architecture](diagrams/05-security-architecture.svg)

---

## 9. Data architecture

Firestore is the append-heavy workflow ledger; the diagram doubles as the schema reference for the repo. Two design points worth stating in every writeup: the `events` collection is an ordered, immutable log (which is why the Audit Binder can be *generated* rather than assembled by hand), and every side-effecting step writes its idempotency key before executing (which is why a resumed review never emails a vendor twice — the "two laptops" trap from the organizers' own webinar, answered in the schema itself). Review states advance monotonically: `intake → questionnaire_out → replies_in → evidence_review → scored → gated → decided → monitored`.

![Data model](diagrams/07-data-model.svg)

---

## 10. Deployment architecture and technology decisions

![Deployment architecture](diagrams/06-deployment-architecture.svg)

The decision log, in the form judges reward — choice, reason, rejected alternative:

| Area | Choice | Why | Rejected alternative |
|---|---|---|---|
| Agent framework | ADK (Python) on Agent Engine | Required-tech alignment; managed long-running sessions; Memory Bank integration | Self-hosted loop on GKE — more ops, no platform story |
| Default model | Gemini 3.5 Flash everywhere | Mirrors organizers' cost guidance; <$0.50/review is a headline metric | Pro-everywhere — 10× cost, no visible quality gain on parsing |
| Synthesis model | Gemini Pro for memos + contradictions | The two places reasoning depth is user-visible | Flash — memos read noticeably thinner |
| PII handling | Gemma scrubber inside the VPC | Sovereignty story + the Gemma bonus, earned honestly | Cloud DLP only — fine, but no bonus and weaker narrative |
| Events | Pub/Sub between all agents | Autonomy = event-driven; any agent can die without stalling the fleet | Direct RPC — couples agents, breaks the resume story |
| State | Firestore ledger + explicit checkpoints | Exactly-once side effects; resume from any crash | Agent memory alone — "persistence is not memory" |
| Identity | One service account per agent | The security demo *is* the IAM console screenshot | Shared SA — one injection from disaster |
| Frontend | Next.js + Tailwind on Cloud Run | Fast for a solo builder; scale-to-zero; hosted URL for judges | Streamlit — faster but reads as a prototype |
| Email | Simulated vendor inbox service | Deterministic demo; honestly labeled in README | Real SMTP — deliverability risk during judging week |
| Dev tooling | Claude Code (development only) | Solo force multiplier; the product itself calls only Google models | — |

![Technology stack](diagrams/08-tech-stack.svg)

---

## 11. The docs site plan

The inspiration project's docs site is a large part of why it read as production-grade, and it is cheap to replicate: a Nextra or Docusaurus site in `docs/site/`, deployed to GitHub Pages (the *product* must run on Google Cloud; the documentation can live anywhere). Navigation, mirroring what worked: **Home** (one-paragraph pitch, hero diagram, Live Demo button, Download/Repo buttons) · **Getting Started** (the README spin-up, deployment diagram) · **Architecture** (this document, all eight diagrams) · **Security** (diagrams 03 + 05 — our differentiator deserves its own page) · **Live Demo** (link to the hosted Cloud Run dashboard). Add a "Built for the All Things Agentic Hackathon" line in the footer, and link the docs site from the Devpost submission, the README, and the Medium article so every surface reinforces the others.
