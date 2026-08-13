# Drawbridge — Devpost Submission Description
### The public write-up judges read first · fill-in-ready template
*How to use this file: everything in normal prose is drafted and ready. Everything in `[SQUARE BRACKETS]` is a placeholder you complete on submission day — links, screenshots, or a personal detail only you can supply. Callout lines beginning with **▶ IMAGE** tell you exactly which asset from `diagrams/`, `mockups/`, or a product screenshot to drop at that spot. Delete this instruction block before publishing. Devpost renders Markdown, so headings, bold, and image embeds all work — but paste images via Devpost's own image uploader rather than relying on relative paths.*

---

# Drawbridge — The Autonomous Vendor-Trust Fleet

> **Live demo:** [INSERT hosted Cloud Run URL] · **Docs:** [INSERT docs site URL] · **Repo:** [INSERT GitHub URL] · **Demo video:** [INSERT YouTube URL]

*Built solo in 20 days for the All Things Agentic Hackathon — Fortified Enterprise Fleet track.*

**▶ IMAGE — hero:** lead with the money-shot. Use the built product screenshot of the red adversarial-conduct banner on the review timeline (the built version of `mockups/02-review-timeline.svg`), or `diagrams/01-system-architecture.png` if the screenshot isn't camera-ready. One image only here; it's the thumbnail people judge in half a second.

---

## __Inspiration

*[This section must be rewritten in your own true voice before publishing — the draft below is a scaffold in the right register. Judges can smell a manufactured origin story, and the EcoLafaek example wins precisely because its inspiration is genuinely personal. Keep the structure — personal observation → the number that alarmed you → the realization that agents were the answer — but make the words and the moment yours.]*

Every company I read about getting breached lately had the same detail buried in the story: it started with a vendor. Not their own systems — someone they had trusted enough to hand data or access to. I kept seeing it, and then I saw the number that made it undeniable.

Verizon's 2025 Data Breach Investigations Report, which analyzed over 22,000 security incidents, found that **third-party involvement in breaches doubled in a single year — from 15% to 30%.** A third of all breaches now come through the side door. And the only thing standing in that doorway, at most companies, is a process built entirely on email: a 60-question spreadsheet, a stack of SOC 2 PDFs nobody has time to read closely, three departments cc'd on the same thread, and two to four weeks of waiting before anyone can say yes or no.

I looked closer at that process and it got worse. Security teams spend around **15 hours a week** just filling out and chasing questionnaires. These reviews are one of the **top deal blockers in B2B sales** — contracts sit frozen while a CISO waits on an assessment. And after all that effort, **fewer than half of organizations ever look at a vendor again** once the contract is signed, even though a vendor's security posture can change the week after onboarding.

It struck me that this is the *perfect* job for a fleet of autonomous agents — long-running, multi-step, full of specialized sub-tasks and external documents — and the *worst possible* job for a single chatbot. When I read what Google's Gemini Enterprise Agent Platform could do — agents that run for weeks, remember across sessions, hold their own identities, and screen hostile inputs — I realized I could build something that doesn't just help a human do vendor reviews faster. It could run them.

*This project and this write-up were created for the purposes of entering the All Things Agentic Hackathon.*

---

## __The problem, in numbers

*[This section makes the "real and worthy" case explicit. Every statistic below is sourced; keep the source links live so a judge can verify — verifiable numbers are what separate a credible submission from a pitch. Format as a short, scannable evidence block.]*

- **Third-party breaches doubled.** Third-party involvement in breaches rose from 15% to 30% year-over-year — the single biggest shift in Verizon's 2025 DBIR. *[link: verizon.com/about/news/2025-data-breach-investigations-report]*
- **Reviews take weeks and block revenue.** Vendor security reviews run 2–4 weeks and are among the top deal blockers in enterprise sales; security managers spend ~15 hours per week on questionnaires. *[link: infosecflow.com vendor-security-questionnaire-automation]*
- **The questionnaires are enormous.** Tier-1 vendor questionnaires run 60–80 questions with a 2–3 week expected turnaround. *[link: atlassystems.com vendor-risk-assessment-questionnaire]*
- **Almost nobody monitors after signing.** Fewer than half of organizations continuously monitor vendors post-onboarding, and only 9% have fully mature third-party risk programs. *[link: liminal.co third-party-risk-management-solutions-forecast]*
- **It's now the law.** NIS2 Article 21(2)(d) makes supply-chain security a legal requirement for covered EU entities; DORA imposes documented third-party risk registers on financial firms; SOC 2 and ISO 27001 both mandate vendor-management evidence.
- **The market reflects the pain.** Third-party risk management spending is projected to more than double, from ~$9B in 2025 to ~$20B by 2030. *[links: liminal.co; grandviewresearch.com third-party-risk-management-market-report]*

**The one-line version:** a third of breaches now come through vendors, the review process to prevent them is slow, manual, legally mandatory, and rarely repeated — a job built for a fleet of agents.

**▶ IMAGE (optional):** a simple stat card is fine here if you want one, but the numbered list carries this section on its own. Don't over-decorate the evidence.

---

## __What it does

**Drawbridge** is an autonomous fleet of AI agents that runs an enterprise's entire third-party vendor security review — from the moment a new vendor is proposed, through questionnaires, evidence analysis, and risk scoring, to a human approval decision and ongoing monitoring — and produces a regulator-ready audit binder of every decision it made along the way.

It is built natively on the **Gemini Enterprise Agent Platform**: reviews run for weeks on Vertex AI Agent Engine, vendor dossiers persist in Memory Bank, every agent holds a least-privilege identity, all inter-agent traffic flows through the Agent Gateway, and all inbound vendor content is screened by Model Armor. Humans appear at exactly two points — authorizing first contact with a vendor, and making the final risk decision — and the fleet does everything in between.

The capability that makes Drawbridge different from every "AI-powered" compliance tool: **when a vendor's uploaded document tries to prompt-inject the reviewing agents, Drawbridge blocks it, logs it, and drops that vendor's Trust Score by 25 points — forcing the review to escalate.** A vendor who tries to manipulate your reviewer has raised your risk, and has told you something about their trustworthiness that no questionnaire would have revealed.

And the defence is **measured, not asserted**: twelve injection variants live in the repository, run in CI, with the detection rate published — including the two that got through and what was done about them.

**▶ IMAGE:** `diagrams/01-system-architecture.png` — the seven-layer system diagram, so the reader can see the shape of the fleet before the capabilities are enumerated.

### Core Capabilities

**1. Autonomous review orchestration**
- A new vendor is proposed with a one-line description; the Orchestrator agent tiers it by risk (does it process customer data? is it an AI service?), plans the review, and opens a persistent dossier.
- **The tier is not final.** In every real procurement organisation the initiator understates data scope — not maliciously, but because a Tier 3 review clears in a week and a Tier 1 takes a month, and there is a contract waiting. So the fleet re-evaluates the tier as evidence arrives: when a vendor's own answer reveals broader data access than intake declared, the review **re-tiers upward mid-flight**, generates the additional domain's questions, and writes a timeline entry naming the answer that caused it. Tier only ever moves up.
- Long-running by design: a review spans days or weeks of real time but only minutes of human time.
- **▶ IMAGE:** built screenshot of the queue (`mockups/01-dashboard-queue.svg` as implemented) showing multiple reviews at different stages with the live status strip.

**2. Intelligent questionnaire management**
- The Questionnaire agent generates a tier-appropriate question set (60/30/12 questions), delivers it, and parses replies incrementally as they arrive over days.
- Every question demands evidence, not yes/no answers — "list your encryption standards and attach your key-management policy," never "do you encrypt data?"
- Polite, capped follow-ups chase silent vendors; unparseable answers are routed to a human instead of being guessed.

**3. Evidence cross-examination**
- The Evidence agent reads uploaded SOC 2 reports, certificates, and policies, and *cross-examines* them against the vendor's questionnaire answers — catching, for example, a vendor who claims org-wide MFA while their own SOC 2 exception notes admit an administrative gap.
- Contradictions are flagged with both the claim and the contradicting passage cited.
- **▶ IMAGE:** built screenshot of the review timeline with the expanded step card showing a CLAIM-vs-EVIDENCE contradiction.

**4. Defensible trust scoring**
- The Risk Scorer applies a weighted rubric across seven security domains to produce a **Trust Score — 0 to 100, where higher is safer** — and a band (≥80 approve / 60–79 conditional / <60 escalate).
- **The model judges severity; deterministic code computes the score.** There is no model call in scoring at all — so "why 71?" always has an arithmetic answer a human can re-do by hand, and no agent in the fleet holds the pen on its own metric.
- Every finding is labelled by provenance — **`rule` or `model`** — so an auditor can see which conclusions were arithmetic (a certificate expiry date) and which were judgement (a contradiction between a claim and a passage).
- A one-page risk memo, written for a CISO, accompanies every decision — and is itself screened before a human reads it.

**5. Adversarial-conduct detection** *(the signature capability)*
- Every vendor-supplied document and reply is screened through Model Armor before any generative model sees a word — five detection families, two templates, at HIGH confidence, failing closed if a detector is skipped.
- A detected manipulation attempt is not merely blocked — it **drops the vendor's Trust Score by 25 points**, forces escalation, and is preserved as inert evidence in the audit trail.
- The fleet also screens **its own outputs** — the risk memo and every outbound message — before a human acts on them. It is the one control that assumes all the earlier ones failed.
- Twelve injection variants, run in CI, detection rate published in the README.
- **▶ IMAGE:** `diagrams/03-injection-defense.png` — the adversarial-content pipeline with the decision diamond and the hidden-payload annotation.

**6. Continuous monitoring**
- After approval, the Watchdog agent runs scheduled sweeps over breach feeds and certificate-expiry dates for the approved-vendor portfolio, reopening a review when a vendor's posture changes. Outbound fetch is restricted to an allowlist of feed domains — an agent with unbounded egress is an exfiltration channel.
- Signals are matched on the vendor's registered domain and legal entity rather than a bare name, and scored for relevance; only a high-confidence, materially relevant signal opens a re-review, and anything weaker becomes a triage card. Fewer than half of organizations continuously monitor their vendors — and the reason they stop is noise, so the design addresses noise rather than adding another feed.

**7. One-click audit binder**
- Every action the fleet takes is an OpenTelemetry reasoning trace; one click renders those traces into a regulator-ready evidence pack — timeline (including every tier change and why), questionnaire provenance, screening results naming the template and version that produced each verdict, findings labelled `rule` or `model` with the retrieved passage they cite, the score computation as arithmetic out of 100, and human approvals with identity and timestamp.
- **The binder is rendered by a template, never by a model** — which forecloses the question of whether a blocked payload could influence the document that reports it. Spans carry refs, hashes and enumerated verdicts, never raw vendor text.
- The binder maps directly onto SOC 2 CC9.2, ISO 27001 A.5.19–5.23, and DORA third-party register requirements.
- **▶ IMAGE:** built screenshot of the audit binder export view (`mockups/04-audit-binder.svg` as implemented).

**8. Governed, discoverable fleet**
- The fleet is published to the Agent Registry with a version and capability description, so a second department (Legal, Procurement) can discover and adopt it — and per-agent identities plus gateway policies are what make granting that access safe.

*Note on the vendors shown: NimbusWrite AI, DataDynamo Logistics, and CleanCloud Analytics are fictional vendors from the project's synthetic test pack, which ships in the repository so anyone can reproduce every demo — including the injection block.*

---

## __Architecture overview

*[This is the section that wins the Architectural Discipline score (30% of the rubric). Keep the prose tight and let the diagrams carry the weight — a judge should be able to understand the whole system from the images alone, then read the prose to confirm the depth. Each sub-section below is a heading scaffold with an image callout and a one-to-two-sentence anchor; expand each to a short paragraph once the corresponding piece is built and screenshotted.]*

**▶ IMAGE:** `diagrams/01-system-architecture.png` (repeat the hero diagram here if it wasn't used above, or place it here and use a screenshot up top). This is the required architecture diagram for the submission.

### System architecture — seven layers, one trust path
A request only ever moves downward through increasing levels of trust: actors → Cloud Run surfaces → the screening boundary → the event backbone → the agent fleet → state and memory → governance and observability. Removing any single component degrades the system gracefully rather than breaking it.

### The agent fleet
> Six specialized agents coordinated over an event backbone, each with a single mission and a documented failure behavior.

- **Orchestrator** — tiers vendors, plans reviews, enforces gates.
- **Questionnaire** — generates, delivers, parses, and chases.
- **Evidence** — extracts control claims and cross-examines them.
- **Risk Scorer** — applies the rubric and writes the memo.
- **Watchdog** — monitors approved vendors continuously.
- *(Contract Clause — roadmap; see What's next.)*

**▶ IMAGE:** `diagrams/02-review-sequence.png` — the end-to-end sequence diagram showing all agents across the five review phases.

### Event-driven backbone
> All lifecycle transitions travel as Cloud Pub/Sub events; agents react to events and never poll, so any agent can fail without stalling the fleet.

### Adversarial content pipeline
> Every vendor-origin byte is quarantined, scrubbed, screened by Model Armor, and admitted to a model only with a clean-stamp — and a detected attack becomes a risk signal.

**▶ IMAGE:** `diagrams/03-injection-defense.png` (if not already placed in Core Capabilities; otherwise skip to avoid repetition).

### Memory hierarchy — persistence is not memory
> Four layers with four lifetimes: disposable session state; a durable Firestore workflow ledger; a semantic retrieval layer over screened evidence that answers *which passage says this?*; and cross-session Memory Bank dossiers that make the second review of a vendor smarter than the first. Durable memory accepts **structure, not prose** — enumerated note types with a provenance tag, never free text derived from vendor content — because memory is recalled before any screening runs, which makes it a write path worth defending.

**▶ IMAGE:** `diagrams/04-memory-hierarchy.png`

### Security architecture — zero trust for a fleet
> Defense in depth across five layers — isolation, local extraction, screening, gateway enforcement, containment. Three named gateway policies, one least-privilege service account per agent written at **collection level**, and a tamper-evident audit trail. The agent that reads evidence cannot send email or reach the network; the agent that emails cannot write a finding or a score. Approval tokens are **asymmetric**: the gateway can recognise a human decision but is structurally incapable of manufacturing one.
>
> And the assume-breach sentence, which is true today: **even if an injection reached the Evidence agent, that agent holds no outbound capability and no approval capability — the instruction would have nothing to actuate.**

**▶ IMAGE:** `diagrams/05-security-architecture.png` — includes the per-agent permission matrix.

### Resumability and idempotency
> Every side effect carries an idempotency key claimed before execution, and every workflow step is checkpointed — so a review killed mid-flight resumes from its last checkpoint and never emails a vendor twice. The key is `review_id : plan_vN : step_id`, because a review that re-tiers mid-flight is re-planned, and a step name from plan v1 must not silently satisfy a different step in plan v2. *(This is the "idempotency trap" the hackathon's own long-running-agents session described.)*

### Data architecture
> Firestore is the append-heavy workflow ledger; an ordered, immutable event log is what lets the audit binder be generated rather than assembled by hand.

**▶ IMAGE:** `diagrams/07-data-model.png` — the collection schema and relationships.

### Deployment and cost posture
> Deployed on Vertex AI Agent Engine and Cloud Run with scale-to-zero, minimum instances at 0 everywhere, budget alerts, and Flash-first model routing — under $0.50 in model cost per review, with the ceiling **enforced rather than observed**: a review that exceeds it parks for a human instead of continuing to spend. The public surface is statically rendered and reaches no model, so a hosted demo cannot be made to spend money on tokens.

**▶ IMAGE:** `diagrams/06-deployment-architecture.png`, and optionally a cropped billing-console screenshot showing the per-review cost.

### Technology stack
**▶ IMAGE:** `diagrams/08-tech-stack.png` — the full clustered stack map.

Built with: Gemini 3.5 Flash and Gemini Pro (Vertex AI), `text-embedding-005`, **ADK 2 (Python) — built as a graph workflow**, Vertex AI Agent Engine (Runtime + Memory Bank), Model Armor (two templates, five detection families), Agent Registry, Agent Gateway, Cloud Run, Cloud Pub/Sub, Firestore (including **KNN vector search** for evidence retrieval), Cloud Storage, Cloud Trace and Logging (OpenTelemetry), per-agent IAM service accounts, Secret Manager[, and Gemma for in-VPC PII scrubbing — *include this last clause only if the Gemma scrubber was actually built*]. Next.js and Tailwind for the dashboard and vendor portal. *(Claude Code was used as a development assistant; the product itself runs exclusively on Google models.)*

---

## __How I built it

*[Optional but recommended — this section reads as engineering maturity. Keep it to three or four short paragraphs. Draft below; adjust to what actually happened during your build.]*

The build started with the shared kernel before any agent logic — the gateway that funnels every side effect, the idempotency guard, the checkpoint wrapper, and the OpenTelemetry span schema — because those four pieces are what the whole architecture rests on, and retrofitting them later would have meant rewriting everything. With that foundation, each agent became a relatively small, single-purpose module reacting to Pub/Sub events.

The hardest problem wasn't intelligence — it was durability. Making an agent that can be killed on Tuesday and finish its job on Wednesday, without emailing a vendor twice, took more care than any prompt. The answer was to claim each side effect's idempotency key *before* executing it, and to treat "resume" as simply replaying a list of named steps and skipping the completed ones.

The second hard problem was trust boundaries. A fleet of agents that shares one powerful credential is one prompt injection away from disaster, so every agent got its own service account with the narrowest possible permissions, and every tool call was routed through a single gateway that enforces two policies in code rather than hoping the models behave.

*[Add one genuine challenge and how you solved it, and one honest limitation of the platform with the workaround you shipped — authentic friction is what makes this section credible rather than promotional.]*

---

## __Challenges I ran into

*[Pick three real ones. Strong candidates from the build, adjust to your reality:]*
- **The idempotency trap.** [How you made side effects exactly-once across restarts and Pub/Sub redeliveries — and why the plan version had to go into the key once reviews could be re-planned mid-flight.]
- **We built the screening pipeline in the wrong order and it silently destroyed a signal.** The first version scrubbed PII locally and *then* screened with Model Armor — so the Sensitive Data Protection filter ran against content whose sensitive data had already been removed, and would have returned "no match" on every document forever. Nothing errored; a filter simply never fired. Screening now runs first on the real text, and its results tell the scrubber what to scrub. The lesson generalises: **a control that cannot fail loudly has to be tested for the presence of its own signal, not just for the absence of errors.**
- **Over-flagging in cross-examination.** [Teaching the Evidence agent that missing evidence is a gap, not a contradiction — and giving it retrieval so a contradiction has to cite the passage it came from, which is what made the headline finding credible rather than lucky.]

---

## __Accomplishments that I'm proud of

- Turned a prompt-injection defense into a *product feature* — attempted manipulation becomes a trust signal, something no vendor-review tool does.
- **Measured the guardrail instead of asserting it** — twelve injection variants, run in CI, detection rate published including the failures.
- Built a fleet that survives being killed mid-review and resumes without duplicate side effects.
- Built a fleet that **overrules the intake form**: when a vendor's own answers reveal broader data access than was declared, the review re-tiers upward mid-flight and records why.
- Made the audit trail the deliverable: reasoning traces export as a regulator-ready binder in one click, rendered by a template and never by a model.
- Kept model cost under $0.50 per review through Flash-first routing, with the ceiling enforced rather than observed.
- Shipped it solo in 20 days, with a reproducible synthetic test pack so anyone can replay the demo.

---

## __What I learned

- **Persistence is not memory.** Keeping a process alive and helping an agent *remember* are different problems that need different layers.
- **Policy belongs at the chokepoint, not in the prompt.** Prompt hygiene is a courtesy; IAM and a gateway are a guarantee.
- **The interesting part of a blocked attack is what you do with it.** Blocking is table stakes; scoring the attempt is the insight.
- **A guardrail without a number is an anecdote.** Building the corpus changed what I could honestly claim more than any of the individual filters did.
- **Memory is an attack surface.** Durable memory is written from material that originated with the party under review and recalled before any screening runs — so it takes structured, enumerated, provenance-tagged notes and never free text.
- **The fleet may improve how it asks; it may never improve how it scores.** An agent cannot game a metric it does not hold the pen for.
- [Add one thing GEAP specifically taught you — a platform capability that changed your design, or a constraint that did.]

---

## __What's next for Drawbridge

*[The EcoLafaek example ends on a credible, tiered roadmap, and it works because the goals are concrete and believable rather than grandiose. The draft below follows that short/medium/long structure. Keep it realistic — judges reward a roadmap that sounds like it was written by someone who understands the domain, not a wishlist.]*

### Short-term goals

**1. Deeper evidence intelligence**
- Expand cross-examination beyond SOC 2 to ISO 27001 statements of applicability, penetration-test reports, and DPAs.
- Confidence scoring on every extracted claim, so analysts see not just *what* was found but how certain the fleet is.

**2. Real communication channels**
- Move from the simulated vendor inbox to production email with deliverability handling and threading.
- Slack and Microsoft Teams notifications for analysts, so approval gates reach humans where they already work.

**3. Richer audit binder**
- Configurable binder templates mapped to specific frameworks a customer names (SOC 2, ISO, DORA, HIPAA).
- Export to the formats auditors actually request, and a shareable read-only link with an expiry.

### Medium-term goals

**4. Contract Clause agent**
- Add the sixth agent: check a vendor's DPA and security addendum against a configurable clause library, flagging missing or weak terms before signature.

**5. Continuous monitoring at depth**
- Live, multi-source breach and news ingestion for the approved-vendor portfolio, with relevance scoring.
- Automatic re-review triggers on certificate expiry, subprocessor changes, and disclosed incidents.

**6. Multi-tenant and cross-department**
- Organization-level policy memory ("we always require SOC 2 Type II for data processors") that different teams inherit.
- Role-scoped access so Procurement, Legal, and Security each see the slice of a review that concerns them, governed by the identity model already in place.

### Designed but not built (yet)

*[These are specified in the project's own design documents with effort estimates against them — they are designs that lost a scheduling argument, not aspirations.]*

- **Targeted follow-ups for unusable answers.** Chasing handles *missing* answers; nothing yet handles *present but vague* ones. A low-confidence answer would generate one targeted follow-up that quotes the vendor's own words back and names the exact evidence required, capped at two per question. It is the difference between an agent that collects and an agent that interrogates.
- **Screening of outbound communications** against the same output template, closing the exfiltration path in the one place the fleet legitimately talks to the outside world.
- **Memory supersession**, so a changed contact or a superseded exception replaces its predecessor rather than accumulating beside it.
- **Image-layer injection screening.** The known blind spot, stated rather than hidden: text extraction reads the PDF text layer, so an instruction rendered as an image has nothing to extract. Today it is bounded by a rule — documents with images and no extractable text are flagged for human review — rather than detected.

### Long-term goals

**7. An ecosystem of trust signals**
- Integrate with security-ratings feeds and shared trust centers so the fleet corroborates a vendor's self-attestations against external evidence.
- Portfolio-level risk analytics — which vendors, which domains, which trends are increasing an organization's aggregate third-party exposure.

**8. From tool to standard**
- Open, documented interfaces so the fleet plugs into existing GRC platforms rather than replacing them.
- A path toward the reviews themselves becoming portable — a vendor completes a rigorous, governed review once and reuses the verified result, reducing the questionnaire burden the whole industry complains about.

---

## __Built with

*[Devpost has a structured "Built with" tags field — fill it with these. Also keep this list in the description body for readers who skim.]*

`gemini` · `gemini-3.5-flash` · `text-embedding-005` · `google-adk-2` · `vertex-ai` · `agent-engine` · `memory-bank` · `model-armor` · `agent-registry` · `agent-gateway` · `cloud-run` · `pub-sub` · `firestore` · `firestore-vector-search` · `cloud-storage` · `cloud-trace` · `opentelemetry` · `iam` · `secret-manager` · [`gemma` — if built] · `next-js` · `tailwindcss` · `python`

---

## __Try it yourself

- **Live demo:** [INSERT hosted Cloud Run URL — confirm it loads logged-out]
- **Documentation site:** [INSERT docs site URL]
- **Source code:** [INSERT GitHub URL — public, with the 30-minute spin-up README]
- **4-minute demo video:** [INSERT YouTube URL — public, with chapters]
- **Deep-dive write-up:** [INSERT Blog 1 Medium URL]
- **Architecture & state-design article:** [INSERT Blog 2 Medium URL, if published]

The repository includes the full synthetic vendor pack — including the labeled injection payload — so you can reproduce every moment in the demo, including the adversarial-conduct block. It also includes `injection-corpus/`: twelve labelled injection variants and the CI job that produces the published detection rate, so the guardrail claim is one you can re-run rather than one you have to take on trust. Every payload is obviously synthetic and uses only publicly documented technique classes; these are tests of our own defences, not an attack toolkit.

*This project and this write-up were created for the purposes of entering the All Things Agentic Hackathon. Vendors shown are fictional, from the project's synthetic test pack.*

---

## Submission-day fill-in checklist

*[Delete this section before publishing — it's your pre-flight list for completing this document.]*

- [ ] Rewrite **Inspiration** in your own true voice; keep it personal and specific
- [ ] Confirm every statistic link in **The problem** resolves
- [ ] Replace the hero **▶ IMAGE** with the best available real product screenshot
- [ ] Export all referenced diagrams to PNG at 2× and upload via Devpost's image tool (not relative paths)
- [ ] Capture the four product screenshots called out in Core Capabilities (queue, contradiction card, injection banner, binder)
- [ ] Fill every `[INSERT ...]` link; verify each in an incognito window
- [ ] Remove the Gemma clause everywhere if the scrubber wasn't built
- [ ] Choose three real items for **Challenges**; write one honest platform limitation into **How I built it**
- [ ] Fill the **Built with** tags in Devpost's structured field
- [ ] Confirm the disclosure sentence appears at least once, prominently
- [ ] Confirm the fictional-vendor note appears where vendors are first named
- [ ] Read the whole thing once as a judge who has never seen the project — does it stand alone?
