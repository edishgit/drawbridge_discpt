# Drawbridge — Hackathon Master Document
### The autonomous vendor-trust fleet · All Things Agentic Hackathon (Fortified Enterprise Fleet track)
**Owner:** Ambrstack (solo) · **Deadline:** 1 Sept 2026, 5:30 AM IST · **Version:** 1.0, 11 Aug 2026

---

## 0. How to use this document

This is the single source of truth for the next 20 days. Section 2 is the strategy you re-read when you're tempted to change ideas mid-build. Sections 3–7 are the product: they become your Devpost description, your blog post, and your video narration almost verbatim. Sections 8–13 are execution: demo script, submission package, bonus plan, day-by-day schedule, risks, final checklist. Appendices hold the depth (synthetic data spec, rubrics, copy bank). No code lives here — decisions and specifications only. When a decision is made, it is written as **Decision → Why → What the judge sees**, because in this hackathon 60% of the score (Architecture 30% + Demo/Production Readiness 30%) is awarded for *visible* engineering discipline.

---

## 1. Executive summary

**Drawbridge is a fleet of autonomous agents that runs an enterprise's third-party vendor security review from intake to approval to continuous monitoring — a process that today takes 2–6 weeks of cross-department email ping-pong — and produces a regulator-ready audit binder of every decision it made.**

It is built natively on the Gemini Enterprise Agent Platform: reviews run for weeks on Agent Runtime, vendor dossiers persist in Memory Bank, every agent holds a least-privilege identity, all inter-agent traffic flows through the Agent Gateway, all inbound vendor content is screened by Model Armor, and the OpenTelemetry reasoning traces are not just logs — they export as the compliance evidence pack auditors demand. The signature feature: when a vendor's uploaded document attempts prompt injection against the reviewing agents, Drawbridge blocks it, logs it, and **automatically raises that vendor's risk score for attempted manipulation**.

**Primary prize target:** The Fortified Enterprise Fleet ($20,000). **Backstop targets (same single build):** Grand Prize ($50,000), Best Architectural Design ($5,000 × 2 winners), Individual/Hobbyist ($10,000 × 2 winners), Honorable Mentions ($2,000 × 5 winners). One build, eleven winnable slots.

---

## 2. Strategy: why this track, why this idea

### 2.1 The competition math
Comparable Google/Devpost hackathons show submission rates of 3–5% of registrants: the ADK Hackathon converted 10,400+ participants into 477 submissions; GKE Turns 10 converted 4,773 into 133. At 1,528 participants (growing), expect roughly **150–400 total submissions across three tracks**. The marketing funnel ("all skill levels welcome," GEAR onramp for non-coders) and the two worked examples on the overview page (transcripts→Jira, inbox→proposal) push the mass of entrants into The Taskmaster. The Fortified Enterprise Fleet's seven-component platform requirement is a skill wall that filters out most of the field. Realistic serious competition in this track: **15–40 projects, many shallow**.

### 2.2 The sponsor's incentive
Every one of the four official webinars — orchestration patterns, long-running persistent workflows (crash recovery, human approval, "the idempotency trap"), self-improving agents, memory hierarchies — is a Fleet-relevant topic. GEAP is Google Cloud's current strategic product push, and hackathon history shows the Grand Prize goes to the project that best showcases the sponsor's newest platform (the ADK Hackathon's grand prize, SalesShortcut, was a maximal showcase of ADK + A2A + Cloud Run). The webinars are telegraphing the rubric. Drawbridge is designed so that a judge can screenshot it for a GEAP marketing deck.

### 2.3 What past winners prove (the seven patterns)
From SalesShortcut (ADK grand prize), the GKE Turns 10 winners, and the Gemini API Competition winners, seven patterns repeat: (1) a real problem with a first-person origin story; (2) a **closed action loop** — the system sends, files, scores, and schedules rather than drafting text; (3) genuine multi-agent architecture using named patterns (fan-out/gather, critique loops, human-in-the-loop); (4) event-driven triggers proving autonomy; (5) explicit security and failure handling; (6) every bonus point collected (SalesShortcut published two Medium articles, LinkedIn posts, a YouTube video, and open-source PRs); (7) a live hosted URL and a tight demo showing the actual cloud console. **Ideas were never exotic — execution discipline won every time.** Drawbridge's plan is engineered around all seven.

### 2.4 Why not a different idea — the five-filter test
Every credible Fleet-track challenger was run through five filters: (F1) is every GEAP pillar *load-bearing* rather than decorative? (F2) can a solo builder demo it credibly in 20 days with synthetic data? (F3) does it produce a natural Model Armor "money shot"? (F4) will Google Cloud judges personally relate to the pain? (F5) is the clone density low?

| Challenger | Fails on |
|---|---|
| Supply-chain / procurement orchestrator | F5 — it is literally the track's worked example; expect the most clones |
| SOC / incident-response fleet | F2, F5 — needs realistic telemetry to be credible; "agentic SOC" is the most crowded pitch in security; a GKE winner already did detect→investigate→act |
| Financial close / audit fleet | F1, F3 — internal data is trusted, so Model Armor becomes decorative; spreadsheet demos are flat |
| Employee joiner-mover-leaver fleet | F3 — great identity story, no adversarial-content story; dry demo |
| KYC/AML client onboarding | F2 — regulated-domain accuracy nitpicks; banking systems are hard to fake convincingly solo |
| M&A due-diligence data-room fleet | F4 — episodic, niche; judges don't live this pain |
| **Drawbridge (vendor risk fleet)** | **Passes all five.** Weeks-long by nature (F1: Runtime/Memory Bank are the product), fully demo-able with a synthetic vendor pack (F2), vendor uploads are hostile external content (F3: the injection demo), Google engineers personally suffer vendor reviews from both sides (F4), and nobody clones what isn't on the examples page (F5). |

**Verdict: no replacement idea beats Drawbridge on the rubric. One refinement adopted (below).**

### 2.5 The adopted refinement: the AI-vendor wedge
The hero vendor in every demo, screenshot, and story is a fictional **AI SaaS vendor** ("NimbusWrite AI"). Reason: reviewing AI tools is 2026's fastest-growing procurement pain — the Verizon DBIR found 15% of employees already use generative AI on corporate devices, 72% of them through personal accounts (shadow AI), which is precisely what a working vendor-review process prevents. The engine stays general-purpose TPRM; the wedge sharpens novelty, rides the zeitgeist judges live in, and makes the injection demo poetic: *the AI vendor's own marketing document tries to jailbreak the AI reviewing it.*

### 2.6 Prize-stacking rules — what to assume
Google-run Devpost hackathons follow a consistent rules pattern: a project wins at most one prize (Google allocates at its discretion if it places in multiple), multiple submissions are allowed only if substantially different, and **projects must be newly created during the contest period**. Action items: read this hackathon's Official Rules page on day 1 and confirm all three clauses; treat Architecture/Hobbyist prizes as backstops, not stacks. **Decision:** do NOT build a second submission — 170 solo hours buy one excellent project or two mediocre ones, and mediocre loses everywhere.

### 2.7 Solo feasibility check
Capacity: 60 h/week × ~2.9 weeks ≈ **170–180 hours**, amplified by Claude Max as a force multiplier for scaffolding, test-data generation, documentation, and rubber-duck architecture review (§11.4). Scope estimate for the MVP-through-Target ladder in §5.6: **125–150 focused hours**, leaving a 20–30% buffer. SalesShortcut was built by two people without today's coding agents; a 2026 solo builder with Claude Max is at comparable effective capacity. Feasible — with the scope discipline in §5.6 enforced ruthlessly.

---

## 3. The problem — evidence file (this is your "problem is real and worthy" proof)

### 3.1 The breach data
Verizon's 2025 Data Breach Investigations Report, analyzing 22,000+ incidents and 12,195 confirmed breaches, found **third-party involvement in breaches doubled year-over-year from 15% to 30%** — the single most dramatic shift in the report. Source: verizon.com/about/news/2025-data-breach-investigations-report. Every company's attack surface is now substantially *other companies*, and the only pre-contract control an enterprise has is the vendor security review.

### 3.2 The operational pain
- Vendor security reviews take **2–4 weeks** and are cited as one of the top deal blockers in B2B enterprise sales; security managers report spending **~15 hours per week** on questionnaire work, and answer quality degrades — "by the 80th questionnaire of the year," responses get copy-pasted and burned out. Source: infosecflow.com/blog/vendor-security-questionnaire-automation.
- Tier-1 (critical vendor) questionnaires run **60–80 questions with a 2–3 week expected turnaround**; even Tier-3 lightweight checks take 1–2 weeks. Source: atlassystems.com/blog/vendor-risk-assessment-questionnaire.
- Organizations typically wait **7+ days just to receive completed questionnaires**, and vendors return vague, templated answers ("we follow best practices") that then require manual chasing. Source: vanta.com/collection/tprm/vendor-risk-assessment-questionnaire.
- Complex single questionnaires can consume **up to 30 business days** when multiple departments must contribute. Source: vendict.com/blog/50-essential-security-questionnaire-questions.

Back-of-envelope unit economics for the pitch: a Tier-1 review consuming 40–60 analyst-hours at a $100–150 loaded hourly cost is **$4,000–$9,000 per vendor per review**, and mid-size enterprises run hundreds of new reviews plus annual renewals per year. That is a seven-figure annual line item spent on reading PDFs and chasing email.

### 3.3 The maturity gap (why "it should be automated" hasn't happened)
- Only **9% of organizations have fully advanced TPRM capabilities**. Source: liminal.co/news/third-party-risk-management-solutions-forecast.
- **Fewer than half of organizations continuously monitor** their vendors after onboarding — risk assessment is a point-in-time snapshot that goes stale in weeks. Source: same Liminal report. (This statistic is the entire justification for the Watchdog agent.)

### 3.4 The regulatory forcing function
- **NIS2 Article 21(2)(d)** explicitly requires covered EU entities to address "supply-chain security" including supplier relationships — vendor review is becoming a legal obligation, not a best practice. Source: infosecflow.com (analysis).
- **DORA** (in force for EU financial entities since January 2025) imposes ICT third-party risk management with documented registers and oversight — auditable evidence of vendor due diligence is mandatory.
- **SOC 2 (CC9.2) and ISO 27001 (A.5.19–5.23)** both contain vendor-management controls, meaning every certified company must *prove* it reviews vendors — which is exactly what Drawbridge's audit binder produces automatically.
- The EU AI Act's phased obligations make AI-tool procurement reviews (the §2.5 wedge) an emerging compliance category of their own.

### 3.5 The market worthiness
The TPRM market was ~$8–9B in 2024–25 and is projected to more than double to **~$19–20B by 2030** (Liminal: $9.0B→$19.9B at 17.1% CAGR; Grand View Research: $7.4B 2023→$20.6B 2030 at 15.7% CAGR). Sources: liminal.co, grandviewresearch.com/industry-analysis/third-party-risk-management-market-report. This is a large, fast-growing, compliance-driven market — the "Update from the future: we started a startup" ending that SalesShortcut earned is available here too, and judges can feel it.

### 3.6 The one-paragraph problem statement (use verbatim in submission and video)
"Thirty percent of breaches now involve a third party — double last year — yet the only gate between an enterprise and a risky vendor is a review process built on email: a 60-question spreadsheet, a stack of SOC 2 PDFs nobody fully reads, three departments cc'd, and 2–4 weeks of waiting. Security analysts spend 15 hours a week on it, deals stall behind it, regulators now legally require it, and fewer than half of companies ever look at a vendor again after signing. It is the perfect job for a fleet of agents — and the worst possible job for a single chatbot."

---

## 4. Market landscape and differentiation

### 4.1 Who exists
Platform incumbents: OneTrust, ProcessUnity, Prevalent, Archer (GRC suites with TPRM modules). Ratings/monitoring: SecurityScorecard, BitSight, UpGuard. Compliance-automation entrants: **Vanta** (Vendor Risk Management with AI-powered assessments and questionnaire automation) and **Drata** (launched a TPRM solution in December 2025). Vendor-side responders (answering inbound questionnaires): Conveyor, SecurityPal, Whistic, Vendict. The honest read: incumbents are adding AI *features* — summarize this SOC 2, draft this answer.

### 4.2 The differentiation (say it exactly this way)
1. **Fleet, not feature.** Incumbents bolt a copilot onto a workflow tool a human still drives. Drawbridge is an autonomous fleet that *owns* the review end-to-end — humans appear only at approval gates. This is the difference the track exists to showcase.
2. **Adversarial-content defense as a product feature, not a disclaimer.** Every agentic reviewer ingests documents written by the party being judged — a structurally adversarial input channel that no incumbent treats as such. Drawbridge screens all vendor content through Model Armor and converts detected manipulation into a risk signal (the Adversarial Conduct flag). No one demos this. It will be remembered.
3. **The audit trail *is* the deliverable.** Incumbents log actions; Drawbridge exports its full reasoning-chain traces as a regulator-ready evidence binder, turning GEAP observability from telemetry into user value — and directly satisfying SOC 2/ISO/DORA documentation duties.
4. **Governance-native.** Registry-published, identity-scoped, gateway-policed agents are exactly what lets a *second* department safely adopt the fleet — the cross-department story the track brief demands.

### 4.3 Hackathon framing (important)
This is judged as a platform showcase, not a venture-capital whitespace analysis. SalesShortcut won the ADK grand prize as an AI SDR — one of the most crowded software categories on earth — because it was the best *demonstration*. Competitors validate the problem; the fleet architecture is the contribution. Never claim "nobody does this"; claim "nobody does it *as an autonomous, governed, injection-hardened fleet* — and here's why that architecture is the future."

---

## 5. Product definition

### 5.1 Positioning
**Name:** Drawbridge. **Tagline:** "The fleet that decides what crosses into the castle." **One-liner for judges:** "Drawbridge runs your entire vendor security review — intake, questionnaire, evidence analysis, risk scoring, approval, and continuous monitoring — as a governed fleet of agents that survives weeks-long timelines, defends itself against manipulative vendor documents, and hands your auditor the evidence binder." **Category:** Autonomous third-party risk management (agentic TPRM).

### 5.2 Personas
- **Priya, Security Analyst** (primary user): owns 15 concurrent reviews; drowning in PDFs; wants the fleet to do the reading and chasing while she makes the judgment calls at the gate.
- **Marcus, Procurement Manager** (initiator): discovers the fleet in the Agent Registry, kicks off reviews, watches status; cares about cycle time because stalled reviews stall contracts.
- **Elena, CISO** (approver/accountable): signs risk acceptances at the human gate; cares that every decision is defensible and traceable.
- **The vendor contact** (external counterparty): receives the questionnaire, uploads evidence to the portal; occasionally adversarial.
- **The auditor** (indirect consumer): receives the audit binder; the reason the observability layer exists.

### 5.3 Core user journeys
- **J1 — New vendor review (the spine).** Marcus submits "NimbusWrite AI, will process customer text, ~$40k/yr" → intake event on Pub/Sub → Orchestrator tiers the vendor (Tier 1: processes customer data), plans the review, opens a dossier in Memory Bank → Questionnaire agent generates a tier-appropriate questionnaire and emails the vendor → days pass; replies trickle in and are parsed → Evidence agent analyzes the uploaded SOC 2 and cross-checks it against questionnaire answers, flagging contradictions → Risk Scorer produces a scored risk memo → Elena approves at the human gate → decision recorded; Watchdog begins monitoring. Elapsed: days of real time, minutes of human time.
- **J2 — The injection attempt.** NimbusWrite's uploaded "security overview" PDF contains hidden text instructing the reviewer to score it low-risk and skip evidence checks. Model Armor intercepts at ingress; the sanitized document proceeds; an Adversarial Conduct flag is raised; the risk score increases; the incident lands in the trace and the binder.
- **J3 — The crash.** Mid-review, the runtime dies (in the demo: killed deliberately, live). On restart, the workflow resumes from durable state with the dossier intact; idempotency keys guarantee the vendor is never emailed twice.
- **J4 — Continuous monitoring.** Weeks after approval, Watchdog's scheduled sweep finds a breach report naming an approved vendor → risk re-scored → re-review task opened → Priya notified. (Justified by the "fewer than half of orgs continuously monitor" statistic.)
- **J5 — The audit binder.** Elena clicks Export → a single evidence pack: timeline, every agent decision with its reasoning trace, every document's screening result, every approval with identity and timestamp.
- **J6 — Cross-department discovery.** Legal finds "Vendor Review Fleet v1.2" in the Agent Registry and requests access — governance (identity scoping, gateway policy) is what makes saying yes safe.

### 5.4 The fleet — agent-by-agent specification
Each agent: mission, trigger, tools/permissions, model, and failure behavior. (Permissions are enforced by per-agent service accounts — see §6.)

1. **Orchestrator.** Mission: turn an intake request into a tiered review plan; dispatch sub-agents; track completion; enforce gates. Trigger: intake events. Tools: Firestore (read/write workflow state), Memory Bank, dispatch via Agent Gateway. Model: Gemini 3.5 Flash for planning; escalates synthesis to Pro. Failure: any unrecoverable sub-agent failure parks the review in "needs human" rather than guessing.
2. **Questionnaire Agent.** Mission: generate a tier-appropriate questionnaire (Appendix C), deliver it, parse replies incrementally as they arrive over days, chase politely on a schedule. Tools: email send (gated by an approval-token policy at the gateway), portal write. Model: Flash. Failure: unparseable replies are quoted back to the human queue, never silently dropped.
3. **Evidence Agent.** Mission: read SOC 2 reports/certs/policies from the evidence bucket; extract control claims; **cross-examine** — reconcile document claims against questionnaire answers and flag contradictions (e.g., questionnaire says "MFA enforced everywhere," SOC 2 exception notes say otherwise). Tools: Cloud Storage read-only; no email, no external network. Model: Flash for extraction; Pro for the contradiction analysis. Failure: unreadable documents are flagged, not skipped.
4. **Risk Scorer.** Mission: apply the weighted rubric (Appendix B) to produce a 0–100 score, tier-appropriate findings, and a draft risk memo; incorporate the Adversarial Conduct flag. Tools: Firestore read; rubric config. Model: Flash scoring; Pro writes the final memo (the one place Pro is spent — mirroring the organizers' own cost guidance, which judges wrote).
5. **Watchdog.** Mission: post-approval sweeps (scheduled) over breach/news feeds and cert-expiry dates for the approved-vendor portfolio; open re-reviews on hits. Tools: web/news retrieval through the gateway; Firestore write for re-review tasks. Model: Flash. Failure: feed outages log-and-skip; never blocks reviews.
6. **Contract Clause Agent (stretch only).** Mission: check the vendor's DPA/security addendum against a clause library. First on the cut list (§5.6).

**Human gates (non-negotiable features, not compromises):** (G1) risk acceptance — no vendor is approved without a named human decision; (G2) first outbound email to any new external contact requires one-tap approval, after which the thread is delegated. The Aug 13 webinar ("human approval") confirms judges want exactly this.

### 5.5 Signature features — the five things a judge remembers
1. **The Adversarial Conduct signal.** Injection attempt → blocked → *risk score raised*. Turns a safety mechanism into a product insight: "a vendor who tries to manipulate your reviewer has told you something material about their trustworthiness."
2. **The Audit Binder.** One click converts OpenTelemetry reasoning traces into the evidence pack compliance frameworks demand. Observability as a feature, not plumbing.
3. **Kill-and-resume.** Live in the demo: terminate the runtime mid-review, watch it resume with dossier intact and zero duplicate side effects. Directly answers the "idempotency trap" webinar.
4. **Least-privilege fleet.** The permission matrix (§6.3) shown on screen: the agent that reads evidence cannot email; the agent that emails cannot touch internal data.
5. **"Three weeks in three minutes."** A review-timeline UI with a time-compression control for the demo, making multi-week autonomy visible in a four-minute video without faking anything (real events, accelerated clock — stated honestly on screen).

### 5.6 Scope ladder and cut discipline
- **MVP (must exist by Day 8):** J1 end-to-end on synthetic vendors with Orchestrator + Questionnaire + Evidence + Risk Scorer, Firestore state, Pub/Sub events, deployed on Agent Engine + Cloud Run, human approval gate.
- **Target (Day 14):** Model Armor integration + Adversarial Conduct flag (J2); kill-and-resume with idempotency keys (J3); Memory Bank dossiers; per-agent identities; Audit Binder v1 (J5); Registry publication (J6); portal UI polish.
- **Stretch (only if Day 16 is green):** Watchdog live sweep (J4 — otherwise shown as a simulated scheduled event), Contract Clause agent, Gemma in-VPC PII scrubber (§6.6), registry version-rollback demo.
- **Cut order (pre-committed, in order):** Contract Clause agent → registry versioning demo → Watchdog live feeds (keep simulated) → portal cosmetics. **Never cut:** Model Armor, kill-and-resume, the binder, human gates — these are the four pillars of the demo.

---

## 6. Architecture and platform decisions (the decision log)

Each entry: **Decision → Why → What the judge sees.** This section becomes the "Architectural Discipline" story in the submission.

### 6.1 Event backbone
**Decision:** All lifecycle transitions (intake, reply-received, evidence-uploaded, score-ready, approved, watchdog-hit) are Pub/Sub events; agents react to events, never poll. **Why:** event-driven autonomy is the track's definition; decoupling lets any agent crash without stalling the fleet. **Judge sees:** a topology diagram where removing any one box doesn't break the arrows, plus live Pub/Sub metrics in the console shot.

### 6.2 State and memory hierarchy (mirrors the Aug 27 webinar)
**Decision:** three explicit layers — (a) session state inside Agent Engine for in-flight reasoning; (b) Firestore as the durable workflow ledger (review status, findings, event log, idempotency keys); (c) Memory Bank for cross-session, cross-review vendor dossiers and org-level policy memory ("we always require SOC 2 Type II for data processors"). **Why:** "persistence is not memory" — the webinar's exact framing; each layer has a distinct job. **Judge sees:** the README's memory-hierarchy diagram and, in the demo, a *second* review of the same vendor months later where the fleet recalls the prior negotiation history from Memory Bank.

### 6.3 Zero-trust fleet identity
**Decision:** one service account per agent; a written permission matrix: Evidence Agent = storage read-only, no egress; Questionnaire Agent = email send + portal write, no internal data; Risk Scorer = Firestore read + rubric; Orchestrator = state read/write + dispatch; nobody holds broad roles. **Why:** an agent fleet with a shared god-credential is one injection away from disaster; least privilege makes the Model Armor story credible end-to-end. **Judge sees:** the IAM console filtered to the fleet's service accounts, and the matrix as a table in the README.

### 6.4 Gateway policy
**Decision:** all inter-agent calls and all tool calls route through the Agent Gateway with two named policies: (P1) no outbound email without a human-approval token for new contacts; (P2) no external content reaches any model without a Model-Armor-passed stamp. **Why:** policies enforced at a chokepoint, not by prompt hygiene. **Judge sees:** a blocked-by-policy log line, on screen, during the demo.

### 6.5 Idempotency and resumability
**Decision:** every side effect (email, score write, approval record) carries an idempotency key derived from review-id + step-id; workflow steps are checkpointed to Firestore before execution; restart replays from the last checkpoint and skips completed keys. **Why:** the organizers dedicated a webinar to "why a resumable agent might order two laptops" — this is a graded question and Drawbridge answers it on camera. **Judge sees:** the kill-and-resume demo segment, and exactly one email in the vendor's inbox afterward.

### 6.6 Model economics and the Gemma sovereignty scrubber
**Decision:** Gemini 3.5 Flash is the default for all parsing, extraction, scoring, and chasing; Gemini Pro is spent only on the final risk-memo synthesis and contradiction analysis. Additionally (stretch, and the bonus-points model integration): a small **Gemma** model runs *inside the project's own infrastructure* as a PII pre-screener, so raw vendor documents are scrubbed before any content leaves the trust boundary. **Why:** Flash-first mirrors the organizers' published cost guidance; Gemma-in-VPC turns the "integrate Gemma/Veo/Lyria" bonus into an on-theme data-sovereignty feature instead of a gimmick. **Judge sees:** a model-routing table in the README and a per-review cost figure (target: under $0.50/review) — a number no other team will show.

### 6.7 Observability → Audit Binder
**Decision:** every agent step emits OpenTelemetry spans (goal, inputs summary, decision, model, latency, cost) into Cloud Trace/Logging; the binder generator queries a review's trace tree and renders the evidence pack (Appendix D). **Why:** the track demands "audit their reasoning"; regulations demand documented due diligence; making the trace user-facing is the elegant double-win. **Judge sees:** the trace waterfall in the console, then the same data as a polished binder PDF two seconds later.

### 6.8 Deployment topology
**Decision:** agents on Vertex AI Agent Engine (Agent Runtime); the vendor portal + internal dashboard + binder service on Cloud Run (scale-to-zero, max-instance caps, budget alerts per the organizers' cost tips); evidence in Cloud Storage; state in Firestore; events on Pub/Sub; build with **ADK (Python)**. Everything torn down after final recording except the demo-window services. **Why:** satisfies every required-tech clause (Gemini 3.5 via Vertex AI ✓, Google agent framework ✓, multiple GCP infra services ✓) with a defensible cost posture. **Judge sees:** the Cloud Run and Agent Engine dashboards, live, in the video — the explicit "proof it runs on Google Cloud" requirement.

---

## 7. Judging rubric mapping (40 / 30 / 30)

**Innovation & Operational Utility (40%).** Friction removed: 2–4 weeks of cross-department review compressed to days; ~40–60 analyst-hours to under 1 human-hour at the gates; autonomous action includes sending questionnaires, chasing, cross-examining evidence, scoring, opening re-reviews — with humans only at decision points. Post-approval, Watchdog keeps acting for weeks (the track's defining ask). The Adversarial Conduct signal is a genuinely novel capability, not a wrapper.

**Architectural Discipline & Tech Stack (30%).** Decoupled event-driven services; explicit three-layer memory hierarchy; per-agent least-privilege identity; policy enforcement at the gateway chokepoint; idempotent, checkpointed, resumable workflows; secured credentials (no shared keys); documented failure behavior per agent; Flash/Pro/Gemma routing with a cost number. Every one of these is named in §6 with console-visible proof — this section is also the Best Architectural Design backstop case.

**Demo & Production Readiness (30%).** Live, unedited core segment including a deliberate mid-demo crash; clean architecture diagram (already drafted); reproducible README with spin-up instructions and synthetic data included; hosted Cloud Run URL; explicit console shots of Agent Engine, Cloud Run, Pub/Sub, IAM, and Cloud Trace. The demo script (§8) allocates screen time in proportion to these graded items.

---

## 8. The demo video — script and shot list (target 3:55)

**Production decisions:** 1080p screen capture (OBS), single-take core segment (1:20–3:10) explicitly labeled "live, unedited," calm narrated voiceover recorded separately over the cut, captions on, no background music louder than -20 LUFS, YouTube **public** (not unlisted — bonus-content rules require public). Record after Day 17; keep every raw take.

| Time | Shot | Narration beat |
|---|---|---|
| 0:00–0:25 | Title card → stock-style shots of a spreadsheet questionnaire and an inbox thread | "Thirty percent of breaches now involve a third party — double last year. Yet the gate protecting your company from a risky vendor is… a 60-question spreadsheet and a three-week email thread." (§3.6 condensed) |
| 0:25–0:45 | Agent Registry: Marcus searches, finds "Vendor Review Fleet v1.2," views its published capabilities and identity scopes | "So we built a fleet, not a chatbot — published, versioned, and discoverable by any department in the company's Agent Registry." |
| 0:45–1:20 | Intake form: NimbusWrite AI submitted → review timeline appears → Orchestrator plans, tiers it Tier-1 → questionnaire generated and (after a one-tap human approval) emailed | "One request. The Orchestrator tiers the vendor, opens a persistent dossier in Memory Bank, and the Questionnaire agent reaches out — after a human approves first contact. From here, the fleet works while everyone else doesn't." |
| 1:20–1:45 | **LIVE SEGMENT BEGINS (banner on screen).** Time-compression control engaged: days tick past on the timeline; vendor replies arrive; Evidence agent ingests the SOC 2; a contradiction flag appears | "We're compressing three weeks into three minutes — real events, accelerated clock. Watch the Evidence agent catch the vendor claiming MFA everywhere while their own SOC 2 exceptions say otherwise." |
| 1:45–2:20 | **The money shot.** NimbusWrite uploads a 'security overview' PDF; Model Armor banner: content blocked — hidden instruction detected; Adversarial Conduct flag raised; risk score visibly increases; gateway policy log line shown | "And here's why enterprise agents need armor. This vendor's PDF contains hidden text telling our reviewer to approve them. Model Armor catches it at the gateway — and Drawbridge does something new: attempted manipulation *raises* your risk score. The vendor just told us who they are." |
| 2:20–2:50 | **The crash.** Terminal visible: the runtime process is killed on camera; dashboard shows the review parked; restart; the review resumes at the exact step; the vendor's inbox shown with exactly one email | "Enterprise workflows run for weeks, so they must survive failure. We'll kill the runtime ourselves… and it resumes from durable state — idempotency keys mean the vendor is never emailed twice." |
| 2:50–3:10 | Human gate: Elena reviews the risk memo on the dashboard, approves with one click; decision recorded with identity + timestamp. **LIVE SEGMENT ENDS.** | "Autonomy with accountability: no vendor is approved without a named human at the gate." |
| 3:10–3:35 | Audit Binder export → PDF opens: timeline, decisions, reasoning traces, the injection incident. Quick cut to Cloud Trace waterfall, Agent Engine dashboard, Cloud Run services, IAM per-agent accounts, Pub/Sub metrics | "Every decision the fleet made is an OpenTelemetry trace — and one click turns those traces into the audit binder your regulator asks for. All of it running on Google Cloud: Agent Engine, Cloud Run, Pub/Sub, Firestore, per-agent IAM." |
| 3:35–3:55 | Metrics card: "3 weeks → 3 days · ~50 analyst-hours → <1 · <$0.50 model cost/review" → logo + track name | "Drawbridge: the fleet that decides what crosses into the castle. Built solo, on the Gemini Enterprise Agent Platform, for the Fortified Enterprise Fleet track." |

**Fallback rule:** record three full takes of the live segment on different days; submit the best; if the live crash-resume misbehaves in all takes, the segment is re-scoped to resume-after-restart without the on-camera kill (never faked).

---

## 9. Devpost submission package (every field, pre-planned)

- **Project name:** Drawbridge — Autonomous Vendor-Trust Fleet.
- **Elevator (for gallery card):** "A governed fleet of agents that runs enterprise vendor security reviews end-to-end for weeks at a time — and raises a vendor's risk score when their documents try to prompt-inject the reviewer."
- **Text description structure:** Inspiration (a first-person origin story: watching a deal stall for a month behind a security review — write yours truthfully) → What it does (J1–J6 from §5.3) → How we built it (§6 decision log, condensed) → Challenges (pick three honest ones; the idempotency trap and incremental questionnaire parsing are strong) → Accomplishments (five signature features, §5.5) → What we learned (memory hierarchy; policy-at-the-gateway beats prompt hygiene) → What's next (continuous monitoring depth, clause library, real GRC integrations) → Bonuses (list with links, mirroring SalesShortcut's format).
- **Features & functionality:** the six agents, two human gates, five signature features, portal + dashboard + binder.
- **Technologies:** Gemini 3.5 Flash + Pro (Vertex AI), ADK (Python), Agent Engine (Runtime + Memory Bank), Model Armor, Agent Registry, Cloud Run, Pub/Sub, Firestore, Cloud Storage, Cloud Trace/Logging (OpenTelemetry), IAM per-agent service accounts, Gemma (in-VPC PII scrubber, if built).
- **Other data sources:** the synthetic vendor pack (Appendix A) — disclosed as synthetic; public breach-news feed for Watchdog.
- **Findings & learnings:** include the per-review cost figure and one honest negative result (e.g., what Flash misparsed until the prompt was restructured) — honesty reads as engineering maturity.
- **Repository:** **public** GitHub (Decision: public > private; removes judge friction; if anything forces private, share with testing@devpost.com and cloudhackathons@google.com). Structure: /agents (one folder per agent), /portal, /binder, /infra (deploy configs), /synthetic-vendors (the full data pack so judges can reproduce the injection demo), /docs (architecture diagram, permission matrix, memory hierarchy), README.
- **README spin-up section (graded item):** prerequisites → one-command infra bootstrap → seed synthetic vendors → run the fleet locally via ADK → deploy → run the demo scenario script → teardown. A judge must be able to *believe* they could run it in 30 minutes.
- **Architecture diagram:** the layered diagram already drafted in this project (untrusted zone → Model Armor → Gateway → Runtime fleet → state/memory → governance strip); redraw cleanly, one page, with the permission matrix as an inset table.
- **Hosted URL:** the Cloud Run dashboard stays live through judging at scale-to-zero with an access note in the README; everything expensive is torn down after the final recording per the organizers' own guidance ("record proof, then switch off").

---

## 10. Bonus points plan (all three, scheduled)

1. **Published content — Medium article (Day 18–19).** Title: "I Built an Agent Fleet That Gets Prompt-Injected for a Living." Outline: the vendor-review problem in numbers (§3) → why a fleet, not a chatbot → the five architecture decisions that mattered (§6.1–6.5, prose) → the injection demo with screenshots → the idempotency trap in practice → cost figure → what GEAP made easy vs. hard (balanced, credible). **Mandatory line, verbatim requirement:** include a sentence stating the piece was created for the purposes of entering this hackathon. Must be public.
2. **Social posts (Day 19).** LinkedIn: 150-word version of the injection story + 30-second clip + repo link + **#AllThingsAgenticHackathon**. X: 2-tweet thread, same clip, same hashtag. Post from your real account; judges and Google DevRel demonstrably browse the hashtag.
3. **Additional Google model — Gemma (Stretch, §6.6).** The in-VPC PII scrubber. If time runs out, do not fake it — the first two bonuses are guaranteed points; this one is upside. (Veo/Lyria: considered and rejected — no honest fit in a TPRM product; forced integrations read as point-chasing.)

---

## 11. The 20-day build plan (solo, 60 h/week, Claude Max)

### 11.1 Capacity vs. scope
~170–180 available hours against a 125–150-hour MVP→Target scope = a real buffer, which exists to absorb GEAP platform friction (the #1 schedule risk), not to add features.

### 11.2 Phase plan
- **Phase 0 — Foundations (Aug 11–13, ~18h):** read Official Rules top to bottom (confirm §2.6 clauses + any AI-assistance disclosure requirement); claim $150 credits + free trial; set budget alerts; **deploy a hello-world agent to Agent Engine and a hello-world service to Cloud Run on Day 1–2** (deployment pain must surface now, not Day 19); stand up Pub/Sub topics + Firestore schema; generate the synthetic vendor pack (Appendix A); attend the Aug 13 long-running-agents webinar live (its content is §6.5's grading key).
- **Phase 1 — The spine (Aug 14–19, ~55h):** Orchestrator + Questionnaire + Evidence + Risk Scorer; J1 runs end-to-end on CleanCloud (the easy vendor) by Aug 17; DataDynamo (contradictions) passing by Aug 19; approval gate v1; ugly-but-real dashboard. **Milestone M1 (Aug 19): a stranger could watch J1 happen.**
- **Phase 2 — The armor and the spine of steel (Aug 20–24, ~50h):** Model Armor at ingress + Adversarial Conduct flag (J2 with NimbusWrite); idempotency keys + checkpointing + kill-and-resume (J3); per-agent service accounts + gateway policies; Memory Bank dossiers; Registry publication. Watch the Aug 20 webinar recording. **Milestone M2 (Aug 24): all four demo pillars work on demand.**
- **Phase 3 — The proof layer (Aug 25–27, ~30h):** OTel spans everywhere → binder generator v1 (J5); portal/dashboard polish pass; time-compression control; Watchdog (simulated event minimum, live feed if green); Gemma scrubber only if everything above is green. Attend the Aug 27 memory webinar (validates §6.2 language for the writeup).
- **Phase 4 — The performance (Aug 28–30, ~30h):** Day 28: freeze features; record three takes of the live segment; assemble the video. Day 29: finalize README + architecture diagram + Devpost description; publish Medium article + social posts; **submit a complete draft on Devpost**. Day 30: fresh-eyes pass — follow your own README on a clean project as a stranger would; fix; resubmit final; teardown of non-demo resources. Aug 31: buffer for platform surprises only. **Never touch the deadline hour.**

### 11.3 Weekly rhythm
Six days on, one half-day fully off (solo-project burnout is a listed risk, not a virtue). Each day ends with a 10-minute log entry — those logs become the Medium article and the "challenges/learnings" Devpost sections for free.

### 11.4 The Claude Max leverage playbook
Use Claude (Claude Code + chat) as the second teammate: scaffolding services and configs from §6's specifications; generating the entire synthetic vendor pack (questionnaire answers, SOC-2-style reports with planted contradictions, the injection document); writing tests for the idempotency and resume logic before implementing it; adversarial design reviews ("attack this permission matrix," "where does this resume logic double-fire?"); drafting README/blog/Devpost text from this document; tightening the demo narration to the second. **Boundary (Decision):** Claude is development tooling only — the *product* calls exclusively Google models (Gemini/Gemma), per required tech; verify the rules' AI-tooling language on Day 1 and disclose AI-assisted development if the rules ask.

---

## 12. Risk register

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| 1 | GEAP component access friction (Agent Engine/Model Armor allowlists, region gaps, API changes) | High | Day-1/2 hello-world deploys of *every* platform component; if a managed piece is blocked, implement the same contract behind an interface (e.g., screening service) and label it transparently in README — architecture credit survives, dishonesty doesn't |
| 2 | Credit burn past $150 | Medium | Flash-first routing, scale-to-zero, max-instance caps, budget alerts at $50/$100/$130, teardown after recording; target <$0.50/review makes this visible |
| 3 | Live demo segment fails | Medium | Three recorded takes on different days; scripted scenario runner; fallback scope rule in §8 |
| 4 | Scope creep (the solo-builder disease) | High | §5.6 cut order is pre-committed; M1/M2 milestone gates; anything not serving the four demo pillars after Aug 24 is frozen |
| 5 | Email deliverability for questionnaire flow | Medium | Vendor "inbox" is a simulated mailbox service in the portal (honest, disclosed); real SMTP is a stretch |
| 6 | Solo illness / life event | Low–Med | The Aug 31 buffer day + draft-submitted-by-Aug-29 rule means a lost day never loses the entry |
| 7 | Rules compliance (new-project-only, one-prize allocation, content-disclosure line, AI-tooling clause) | Low | Day-1 full rules read with a written checklist; all code authored within the contest window; mandatory disclosure sentence in the blog |
| 8 | Judges can't reproduce | Medium | Synthetic pack shipped in-repo; scenario script that replays the whole demo; README tested by following it yourself on a clean project on Day 30 |
| 9 | A near-identical competing entry | Low | Unlikely off-examples-page; if seen in the gallery, differentiation = injection-as-risk-signal + binder + kill-resume, which are execution moats not idea moats |
| 10 | Burnout degrading the final week (the part worth 30%) | Medium | §11.3 rest rhythm; the performance phase is deliberately the *lightest* coding phase |

---

## 13. Final-week checklist (print this)

- [ ] Official Rules re-read; every requirement line itemized and checked
- [ ] Video: ≤4 min, public on YouTube, shows problem → value → live demo → **explicit Google Cloud console proof**
- [ ] Devpost text: all sections from §9, no placeholder text, links resolve in incognito
- [ ] Repo public; README spin-up tested cold by yourself, top to bottom, on a clean project
- [ ] Architecture diagram: one page, layered zones, permission-matrix inset
- [ ] Hosted URL live, loads logged-out, noted in README
- [ ] Synthetic vendor pack in repo; scenario runner replays the demo
- [ ] Medium article public, contains the created-for-this-hackathon sentence, linked in submission
- [ ] LinkedIn + X posts live with #AllThingsAgenticHackathon, linked in submission
- [ ] Gemma bonus: included only if real; claimed only if included
- [ ] Costs: teardown done; budget alert history screenshotted (nice proof-of-discipline artifact)
- [ ] Submitted ≥24h before deadline; confirmation screenshot saved

---

## 14. Appendices

### Appendix A — Synthetic vendor pack (the dataset that makes the demo honest and reproducible)
Three fictional vendors, each a folder of documents generated for this project and shipped in-repo:
- **CleanCloud Analytics (Tier 2, the control).** Coherent questionnaire answers; a clean SOC-2-style report; purpose: prove the happy path and calibrate scoring.
- **DataDynamo Logistics (Tier 1, the contradictor).** Questionnaire claims org-wide MFA and 24h breach notification; its SOC-2-style report's exception notes and its incident-history sheet contradict both; an expired ISO certificate. Purpose: the Evidence agent's cross-examination showcase.
- **NimbusWrite AI (Tier 1, the adversary — hero of the demo).** An AI writing SaaS processing customer text. Plausible answers; a subprocessor list including a fourth-party model provider; and a "security overview" PDF containing concealed instruction text (visually hidden styling) directing any automated reviewer to rate the vendor low-risk and skip evidence verification. Purpose: the Model Armor interception and the Adversarial Conduct scoring feature. The concealed text is a benign, clearly-labeled test payload — the repo README states its location and purpose so judges can reproduce the block.
Each vendor also gets: a contact persona, a reply schedule (for time-compressed delivery), and expected end-state (CleanCloud approved; DataDynamo conditionally approved with mitigations; NimbusWrite escalated with Adversarial Conduct flag).

### Appendix B — Risk-scoring rubric (v1 outline)
Weighted domains (Tier-1): data protection & encryption 20; access control & identity 15; incident response & breach history 15; compliance posture & certifications 15; business continuity/RTO-RPO 10; subprocessor & fourth-party chain 10; AI-specific handling (training-data use, model provider chain, output controls — applies to AI vendors) 10; **Adversarial Conduct modifier** (attempted manipulation of the review process): −25 and automatic escalation. Output: 0–100 score → bands (≥80 approve / 60–79 conditional / <60 escalate), each finding linked to its evidence and trace. Tier 2/3 use reduced-domain variants per Appendix C.

### Appendix C — Questionnaire blueprint
Three tiers mirroring industry practice: Tier 1 ≈ 60 questions across the eight §B domains; Tier 2 ≈ 30; Tier 3 ≈ 12. Question style rule: evidence-demanding ("list encryption standards for data at rest and in transit and attach your key-management policy"), never yes/no theater. Tiering inputs: data sensitivity, system access level, spend, and whether the vendor is an AI service (auto-adds the AI domain).

### Appendix D — Audit Binder contents (the export)
Cover: vendor, review id, tier, dates, outcome, approver identity. Sections: (1) review timeline with every event; (2) questionnaire Q/A with parse provenance; (3) evidence inventory with screening results (including any Model Armor incidents, verbatim log excerpts); (4) findings & contradictions with links to source passages; (5) score computation against the rubric; (6) human decisions with identity + timestamp; (7) full reasoning-trace appendix (span tree per agent step: goal, decision, model, latency, cost); (8) post-approval monitoring log. This table of contents maps one-to-one onto SOC 2 CC9.2 / ISO 27001 A.5.19–5.23 / DORA register expectations — say so on the cover page.

### Appendix E — Copy bank
- **Elevator (10s):** "Drawbridge is a fleet of agents that runs your entire vendor security review — for weeks at a time, with humans only at the gates — and it raises a vendor's risk score if their documents try to prompt-inject the reviewer."
- **Video cold open (already scripted in §8).**
- **Tagline options:** "The fleet that decides what crosses into the castle." / "Vendor trust, decided by agents, proven by traces." / "Weeks of review. Minutes of human time. Zero unaudited decisions."
- **The differentiation sentence:** "Incumbents added a copilot to a workflow a human still drives; Drawbridge is a governed fleet that owns the workflow — and treats the vendor's own documents as the untrusted input they are."
- **The learning sentence (for judges):** "The hardest problem wasn't intelligence — it was durability: making an agent that can be killed on Tuesday and finish the job on Wednesday without emailing anyone twice."

---

## 15. Definition of victory
The submission is done when a judge with eight minutes can: watch a ≤4-minute video and see all four pillars (injection block, kill-resume, human gate, audit binder) happen live on Google Cloud; open the repo and believe the README; open the diagram and understand the fleet in thirty seconds; and open the gallery card and retell the one-liner to a colleague. Everything in this document exists to produce those eight minutes.
