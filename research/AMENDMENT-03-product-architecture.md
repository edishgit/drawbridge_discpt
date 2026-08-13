# Drawbridge — Amendment 03
## Deep review of §5 Product definition and §6 Architecture: seven contradictions, six product improvements, eight hardening items
**Raised:** 14 Aug 2026 · **Owner:** Ambrstack · **Status:** proposed — **read §6 before committing to any of it**
**Companion to:** `AMENDMENT-01.md`, `AMENDMENT-02-model-armor.md`

---

## 0 · How this was reviewed

Every claim in §5 and §6 was checked three ways: against the other section of the same document, against the implementation handbook, and against what the thing would actually do when a real vendor is on the other end. The contradictions in Part A are all internal — your own documents disagreeing with each other — and each one becomes either a runtime bug or a sentence you cannot defend on camera. Parts B and C are additions, and **§6 is a capacity warning you should read before you agree to any of them.**

---

## Part A · Contradictions and bugs

### A1 · "The risk score increases" is backwards ★★★

**Where:** §5.3 J2 (*"the risk score increases"*), §5.5.1 (*"risk score raised"*), the elevator pitch, the gallery card, the video narration at 1:45, and the W2/W3/W4 wireframes.

Your score is a **goodness** number: 95 is a maximum, ≥80 approves, and the adversarial penalty is `raw - 25`. So when a vendor attempts manipulation, the number **goes down**. Calling it a "risk score" and then saying it was "raised" is wrong twice over, and it is wrong in the one sentence you repeat most often.

A judge who reads the gallery card, then watches the number fall from 56 to 31 on screen, notices immediately. It reads as a system the builder does not understand.

**Fix — rename the number, keep the line:**

> **Trust Score · 0–95, higher is safer.** Attempted manipulation costs 25 trust points and forces escalation.

The marketing sentence survives intact because *risk* and *the score* are now different things: *"a vendor who tries to manipulate your reviewer has raised your risk — and Drawbridge drops their trust score 25 points and forces escalation."* Prose talks about risk; the number is trust. This also resolves the tension with Amendment 01's D4 (the 95-point scale), because "Trust Score 71 / 95" reads naturally where "risk score 71/100" implied a percentage.

**Effort:** 1h, mostly find-and-replace across two docs, five diagrams and three wireframes. **Do this first** — it touches more artefacts than anything else in this amendment and gets more expensive every day.

### A2 · §5.4 says Flash scores; §11.1 says Python scores ★★★

**Where:** §5.4 Risk Scorer (*"Model: Flash scoring; Pro writes the final memo"*) versus handbook §11.1 (*"Scoring is deterministic arithmetic in Python"*) and `ROUTING["score_rubric"] = MODEL_FAST`.

This is not a wording slip. It undercuts the single strongest architectural claim you have — *the model judges severity, the code computes the score* — which is also your entire answer to the Aug 20 self-improvement webinar and the reason the binder can show its arithmetic.

**Fix:** severity is assigned by the **Evidence agent** at finding-creation time, where the model is already reading the passage and has the context to judge. The Risk Scorer makes **no model call except the memo**. Delete `score_rubric` from the routing table and rewrite §5.4 to: *Model: none for scoring — deterministic arithmetic over model-assigned severities; Pro for the memo only.*

Side benefit: it removes a Flash call per review from your cost figure.

**Effort:** 0.5h.

### A3 · The Orchestrator escalates to Pro, but Pro isn't routed to it

**Where:** §5.4 Orchestrator (*"Gemini 3.5 Flash for planning; escalates synthesis to Pro"*) versus §6.6 (*"Pro is spent only on the final risk-memo synthesis and contradiction analysis"*) and the routing table, which has no Orchestrator entry.

Pick one. **Recommendation: delete the escalation.** Planning is structured selection over a tiering policy you wrote — it does not need Pro, and "Pro is spent in exactly two places" is a cleaner sentence than "Pro is spent in two places and sometimes a third."

**Effort:** 0.25h.

### A4 · G2 and P1 are the same thing with two names

§5.4 calls first-outbound-contact **G2**. §6.4 calls it **P1**. The handbook calls it P1. The wireframes label it P1. Diagrams use both.

**Fix — one taxonomy, stated once and used everywhere:**

| Layer | Names | Meaning |
|---|---|---|
| **Human gates** | G1 risk acceptance · G2 first outbound contact | what a person does |
| **Gateway policies** | P1 approval-token required · P2 verdict-bearing stamp required · P3 egress allowlist (new, §C4) | what the chokepoint enforces |

And the sentence that connects them, which is worth saying out loud: **G2 is a human act; P1 is the machine's inability to skip it.**

**Effort:** 0.5h.

### A5 · The Questionnaire agent cannot write the answers it parses

Handbook §3.2 denies `sa-questionnaire` "Firestore findings write" — but the agent must write `qa_responses`, and the matrix does not distinguish the two collections. As written, either the agent is over-permissioned or the parse cannot persist.

**Fix:** collection-level precision in the matrix — `sa-questionnaire`: `qa_responses` read/write ✅, `findings` write ❌, `scores` write ❌, `approvals` write ❌. Same treatment for every agent. Vague permission rows are how least-privilege claims quietly become false.

**Effort:** 0.25h, and it makes `test_iam_boundaries.py` sharper.

### A6 · Day numbers and calendar dates disagree

§5.6 says "MVP by Day 8" and "Target Day 14"; §11.2 says M1 is Aug 19 and M2 is Aug 24. Counting from Aug 11, Day 8 is Aug 18 and Day 14 is Aug 24. M1 is Day 9.

**Fix:** drop day numbers entirely and use dates. The build plan is a graded artefact and a judge who spots a one-day drift starts checking your other numbers.

**Effort:** 0.25h.

### A7 · Idempotency keys break when the plan changes

`idem_key = f"{review_id}:{step_id}"` is correct **only while the plan is immutable**. The moment re-tiering exists (§B1 below), a review can be re-planned mid-flight, and a step name that meant one thing in plan v1 may mean something else in plan v2 — or a legitimately new step may collide with a completed key and be skipped.

**Fix:** `idem_key = f"{review_id}:plan_v{n}:{step_id}"`, with the plan version incremented on every re-plan and recorded on the review. Steps carried over from the previous plan explicitly inherit their old key so completed work is still skipped.

**Effort:** 0.5h if done now; a nasty debugging session if done after re-tiering ships.

---

## Part B · Product improvements

### B1 · Evidence-corrected re-tiering — the fleet overrules the intake form ★★★

**The gap.** J1 tiers the vendor from what Marcus typed into the intake form. In every real procurement organisation, the initiator understates data scope — not maliciously, but because a Tier 3 review clears in a week and a Tier 1 takes a month, and Marcus has a contract to close. **Your fleet currently trusts the most conflicted party in the process.**

**The improvement.** The Orchestrator re-evaluates tier whenever new evidence arrives. If questionnaire answers or extracted controls reveal broader data access than intake declared, the review **re-tiers upward mid-flight**, generates the additional domain's questions, and records why.

```
Day 0   intake says "internal analytics only"        → Tier 2, 30 questions
Day 6   Q23 answer: "customer records are processed
        in our EU environment for model training"    → re-tier to Tier 1
        + AI-specific domain added, 30 questions sent
        + timeline entry: "Re-tiered 2 → 1. Reason: vendor's own
          answer to Q23 contradicts the declared data scope."
```

**Why it wins.** It is a second moment where the fleet *decides something* rather than processes something — and unlike the injection, it is a decision every procurement person in the room has watched a human fail to make. It exercises the state machine, the plan versioning and Memory Bank in one beat. It costs no extra video time: the tier badge simply changes on a screen already being filmed.

**Implementation.** A `reassess_tier` step after each reply batch and after evidence extraction; deterministic rules first (declared data categories, system access, is_ai_vendor), model only for classifying free-text answers into those categories. Tier only ever moves **up** — never down — because "when evidence is ambiguous, tier up" is already your policy and a downward re-tier is an attack surface.

**Effort:** 3h. Depends on A7.

### B2 · The fourth-party chain — your vendor's vendors ★★★

**The gap.** Appendix B allocates 10 points to "subprocessor & fourth-party chain." NimbusWrite's pack includes "a subprocessor list including a fourth-party model provider." **No agent does anything with it.** It is a scoring domain with no evidence pipeline behind it.

**The improvement.** The Evidence agent extracts the subprocessor list as structured data and evaluates the chain: which fourth parties process customer data, which are already known to the organisation, which are unknown, and whether any appear on the approved-vendor register with their own review history.

**Why it is the strongest product idea available to you.** Your entire thesis is *"your attack surface is now other companies."* The fourth-party chain is that thesis applied recursively, and it is exactly where the AI-vendor wedge bites hardest: **NimbusWrite processes your customer text, and NimbusWrite's model provider processes it too — a company you never reviewed and never signed anything with.** That is a genuinely uncomfortable sentence for anyone in procurement, and no incumbent's copilot surfaces it.

It also produces the one visual you are missing: a small three-level graph — you → vendor → their subprocessors — with the unknown ones in red.

**Implementation.** Structured extraction (Flash) into a `subprocessors` collection; deterministic set-difference against the approved-vendor register; findings for unknown fourth parties that process customer data. Memory Bank makes it compound: the second review that names the same model provider recognises it.

**Effort:** 4h. **Put it in the README, the binder and the gallery images — give it ten seconds of video at most.** The demo is full at 3:55 and the four pillars are not negotiable.

### B3 · Follow-ups for bad answers, not just missing ones ★★

**The gap.** §3.2 of your own evidence file quotes the actual pain: *vendors return vague, templated answers ("we follow best practices") that then require manual chasing.* Your Questionnaire agent chases **missing** answers on a schedule and caps at three rounds. It does nothing about **present but useless** ones — it records low confidence and moves on, and the analyst inherits the problem you promised to remove.

**The improvement.** A low-quality answer generates one targeted follow-up: quote their answer, name the specific evidence required, ask once. Cap at two follow-ups per question so it cannot become an infinite politeness loop.

> *"Your answer to Q14 states that encryption follows industry best practice. The review requires the specific standards used for data at rest and in transit, and your key-management policy as an attachment. Could you provide those two items?"*

**Why it wins.** It closes the loop on the pain you cited to justify the project, and it is the difference between an agent that *collects* and an agent that *interrogates* — which is the same distinction that makes the Evidence agent interesting.

**Implementation.** Reuse the confidence score you already compute. Below threshold → `generate("followup_question")` on Flash, gated by the same P1/thread delegation, its own idempotency key (`followup:q14:v1`).

**Effort:** 3h.

### B4 · Deterministic evidence checks, in code ★★

**The gap.** §5.4 gives the Evidence agent one job: semantic reconciliation. But several checks in your own rubric are **arithmetic, not judgement** — certificate expiry dates, whether a SOC 2 report period is stale, whether the report's scope covers the service you are buying, whether the auditor is named. Handbook §10 mentions expired certificates in a prompt rule, which means a model is currently being asked to compare dates.

**The improvement.** A `deterministic_checks()` pass in Python: expiry, report period age, scope coverage, presence of an auditor and an opinion. Findings from it are marked `source="rule"`; model findings are marked `source="model"`.

**Why it wins.** It extends the argument that already makes your scorer credible — *use code where code is better* — into the agent a judge will interrogate most. It also lets you say a sentence almost nobody in this hackathon can: **"Findings in this binder are labelled by provenance: rule or model."** An auditor cares enormously about that distinction.

**Effort:** 2h. Also removes a class of model error from your hero demo, since DataDynamo's expired ISO certificate becomes a guaranteed finding rather than a hoped-for one.

### B5 · The Watchdog must not cry wolf ★★

**The gap.** §5.4 has the Watchdog fetch breach/news feeds and open re-reviews on hits. There is no entity disambiguation and no confidence threshold. "Northwind" appears in unrelated news constantly; a re-review opened on a false positive costs an analyst an hour and destroys trust in the feature — which is precisely why real continuous-monitoring products are so widely ignored.

**The improvement.** Three cheap guards:
1. **Match on identity, not name** — primary domain plus legal entity name from the dossier, never a bare string match.
2. **Confidence threshold** — the Flash relevance check returns a score; below threshold the signal goes to a triage queue, not to a new review.
3. **Only high-confidence, materially relevant signals auto-open a review**; everything else is a card for Priya.

**Why it wins.** "Fewer than half of organisations continuously monitor" is your justification for the Watchdog existing. The reason they don't is noise. Addressing that in the design is a more sophisticated answer than adding another feed.

**Effort:** 2h.

### B6 · Swap signature feature #5

"Three weeks in three minutes" is a **demo technique**, not a product feature. It belongs in §8 alongside the recording decisions, not in the five things a judge remembers about the product.

**Replace it with the measured injection defence** (Amendment 02 U6): *"we tested twelve injection variants and published the detection rate."* That is a product property, it is unusual, and it is the one that supports the startup sentence later.

**Effort:** 0 — a doc edit.

---

## Part C · Architecture hardening

### C1 · Memory poisoning — the durable compromise nobody thinks about ★★★

**The gap.** L3 (Memory Bank) is written at review close from material *derived from vendor-supplied content*. Model Armor screens content at ingress; nothing screens what gets **written into durable memory**. An injection that survived screening — or simply a cleverly-worded questionnaire answer — could persist a false fact into the vendor's dossier, where it is recalled at the start of every future review, before any screening runs.

That is a durable compromise of the review process, seeded through the legitimate channel, and it is exactly the failure mode your whole thesis exists to talk about.

**The fix — memory accepts structure, not prose:**

```python
ALLOWED_NOTE_TYPES = {"outcome", "band", "negotiated_exception", "conduct_flag",
                      "contact_change", "cert_expiry", "subprocessor", "question_effectiveness"}

def remember(vendor_id, note: MemoryNote):
    assert note.type in ALLOWED_NOTE_TYPES
    assert note.provenance in ("human", "rule", "model_structured")   # never raw vendor text
    ...
```

Free text derived from vendor content never enters L3. Enumerated fields, values from a controlled vocabulary, and a provenance tag on every note. If a future review needs the vendor's exact wording, it reads L2, where it sits behind the screening record that describes it.

**Why it wins.** It is a genuinely novel threat to raise — most agent systems treat memory as a benign convenience — and it is the natural extension of your own argument. One paragraph in the Medium article, one line in the video, two hours of code.

**Effort:** 2h.

### C2 · Asymmetric approval tokens — the gateway can verify but cannot mint ★★★

**The gap.** §14 signs approval tokens with a key from Secret Manager and verifies them at the gateway. If both sides use the same secret, then **anything that can verify can also forge** — and the gateway is reachable by every agent in the fleet. Your strongest security sentence ("no code path can approve a vendor without a signed human artefact") has a hole in it exactly the size of one leaked symmetric key.

**The fix:** asymmetric signing. The private key lives only in the approval service that renders the gate card; the gateway holds the public key. Rotate by publishing a new public key; the gateway never holds signing capability at any point in its life.

**Why it wins.** It is thirty to sixty minutes of work and it upgrades the claim from *"the gateway checks for a token"* to **"the gateway can recognise a human decision but is structurally incapable of manufacturing one."** That is the sentence a security-minded judge remembers, and it is the difference between a demo and a design.

**Effort:** 1h.

### C3 · Out-of-order and late events ★★

**The gap.** §6.1 makes everything an event, and Pub/Sub gives you at-least-once delivery with **no ordering guarantee**. §6.5 covers duplicates. Nothing covers *sequence*. What happens when a vendor reply arrives after the review reached `SCORED`? When `evidence.screened` lands before the plan is written? A judge with backend experience will ask this, and "it hasn't come up" is not an answer.

**The fix:** every consumer checks review state before acting, and each event type has a defined behaviour when it arrives out of phase:

| Late event | Behaviour |
|---|---|
| Reply after `SCORED` | attach to the ledger as an addendum; if it changes an answer that produced a finding, re-open the score, do not silently discard |
| `evidence.screened` before plan exists | park the message, retry with backoff, DLQ after five |
| `watchdog.hit` on a review already reopened | deduplicate on signal id |
| Any event for a `DECIDED` review | append to ledger, never mutate — a decided review is immutable |

**Why it wins.** Distributed-systems maturity is directly graded under Architectural Discipline, and this is one table plus a state guard in each handler.

**Effort:** 2h.

### C4 · P3 — the egress allowlist ★★

**The gap.** The Watchdog fetches "web/news retrieval through the gateway." Nothing bounds *where*. An agent with unbounded outbound fetch is a data-exfiltration channel and an SSRF surface, which is a strange thing to leave open in a product whose thesis is untrusted content.

**The fix:** a third named gateway policy — **P3: outbound fetch is restricted to an allowlist of feed domains; everything else is blocked and logged.** Same enforcement point, same log line format, same on-screen visibility as P1 and P2.

**Why it wins.** Three named policies is a policy *system*; two is a pair of special cases. And the P3 block line is another visible enforcement moment for the console montage.

**Effort:** 0.5h.

### C5 · Screen outbound communications, not just memos ★

Amendment 02 U1 screens what agents produce for **internal** consumption. The Questionnaire agent composes email to an **external** party, using content assembled from internal state. Nothing checks that an outbound message does not contain internal notes, another vendor's details, or dossier content.

**Fix:** run outbound bodies through the `drawbridge-output` template before send, with SDP enabled. It closes the exfiltration path in the one place the fleet legitimately talks to the outside world.

**Effort:** 1h once U1 exists.

### C6 · Traces must not carry raw external content ★

§6.7 says spans carry "inputs summary." If that summary contains vendor-supplied text, hostile content is now in Cloud Trace, and from there it is rendered into the binder — and anything that later summarises a binder would be reading it back.

**Fix:** spans carry refs, hashes and enumerated verdicts; never raw external content. And state the rule that makes the binder safe: **the binder is rendered by a template, never by a model.** One sentence, and it forecloses an entire question.

**Effort:** 0.5h.

### C7 · Enforce the cost ceiling instead of warning about it ★

`COST_CEILING_PER_REVIEW_USD` currently "logs a warning when exceeded." A budget that is observed rather than enforced is not a control.

**Fix:** exceeding the ceiling parks the review in `NEEDS_HUMAN` with a cost card. Retries and model calls stop. *"Budgets are enforced, not observed"* is a production-readiness line, and it protects your credits from a runaway loop at 2 a.m. on Aug 27.

**Effort:** 0.5h.

### C8 · Memory supersession and idempotency cleanup ★

Two small ones. **L3 notes need supersession** — a changed contact or a superseded exception should replace, not accumulate; add `supersedes` and have `recall_dossier` return the current view. **The idempotency collection needs a TTL** — completed keys older than the demo window are execution artefacts, and the organisers' own cost guidance says to clean those up.

**Effort:** 1.5h.

---

## Part D · What is missing entirely, and what to do about it

Three gaps I would name in the docs even if you build none of them, because naming a known limitation is stronger than leaving it to be discovered:

**The rejection path has no journey.** J1–J6 cover approval, injection, crash, monitoring, binder and discovery. Nothing describes what happens when a vendor is rejected or never responds — which in real TPRM is 10–20% of reviews. The UI has a Reject button and the state machine has `NEEDS_HUMAN`; add a two-line **J7** so the product looks complete rather than optimistic.

**The fleet has no operator persona.** Five personas, none of whom administers the fleet — who publishes to the Registry, rotates the signing key, reviews the DLQ, tunes the Model Armor template? For a track whose brief ends in *"scale them safely,"* the absence of an operator is conspicuous. Add **Sam, Platform/AI Operations** to §5.2 with three responsibilities and no new UI.

**Nothing states data residency or tenancy.** Irrelevant for a hackathon, first question in a startup conversation. One line in §6.8 costs nothing: single region, single tenant, confidential vendor documents never leave the project boundary except to Google-managed services in the same region.

---

## Part E · Edit index

**`drawbridge-hackathon-master-doc.md`**
§5.1 Trust Score in the one-liner *(A1)* · §5.2 add Sam *(D)* · §5.3 J1 gains re-tiering, J2 wording *(A1, B1)*, new J7 *(D)* · §5.4 Risk Scorer model row *(A2)*, Orchestrator model row *(A3)*, Evidence gains deterministic checks and subprocessor extraction *(B2, B4)*, Watchdog gains disambiguation and thresholds *(B5)*, gate naming *(A4)* · §5.5 swap feature 5 *(B6)* · §5.6 dates not day numbers *(A6)*, place the new items on the ladder · §6.1 out-of-order table *(C3)* · §6.2 memory poisoning guard and supersession *(C1, C8)* · §6.3 collection-level matrix, asymmetric tokens *(A5, C2)* · §6.4 add P3, restate the G/P taxonomy *(C4, A4)* · §6.5 plan-versioned keys, TTL *(A7, C8)* · §6.6 remove score_rubric, enforce the ceiling *(A2, C7)* · §6.7 spans carry no external content; binder is templated *(C6)* · §6.8 residency line *(D)*

**`drawbridge-implementation-handbook.md`**
§3.2 collection-level permissions *(A5)* · §4 add `PLAN_VERSION`, `FOLLOWUP_CAP`, `WATCHDOG_CONFIDENCE_MIN` · §5.1 `Review.plan_version`, `tier_history`, `Subprocessor`, `MemoryNote.provenance` *(A7, B1, B2, C1)* · §5.2 re-tier transition *(B1)* · §6.1 late-event table *(C3)* · §7.1 add P3 *(C4)* · §7.3 delete `score_rubric`, add `followup_question`, `classify_data_scope` *(A2, B3, B1)* · §7.4 key derivation *(A7)* · §7.6 span content rule *(C6)* · §7.7 allowed note types and supersession *(C1, C8)* · §8 `reassess_tier` step *(B1)* · §9 follow-up loop *(B3)* · §10 deterministic checks and subprocessor extraction *(B4, B2)* · §11.1 no model call *(A2)* · §12 Watchdog guards *(B5)* · §14 asymmetric signing *(C2)* · §18 ceiling enforcement *(C7)* · §19 tests for re-tier, late events and token forgery · §21 checklist rows

**Diagrams** — 02, 03 (re-tier beat), 04 (unchanged), 07 (late-event note), 08 (re-tier transition), 09 (collection-level rows), 10 (**Trust Score** relabel, no model call), 11 (finding provenance in §4), 13 (`plan_version`, `tier_history`, `SUBPROCESSOR`, `MemoryNote.provenance`), 16 (NimbusWrite fourth-party expectation), 20 (late-event and cost-ceiling rows), plus **new 24 · the fourth-party chain graph** *(B2)*

**Wireframes** — every "RISK SCORE" label → **TRUST SCORE** *(A1)*; W3 gains a tier-change timeline entry *(B1)* and a subprocessor panel *(B2)*; W5 findings show `rule` / `model` provenance *(B4)*

---

## Part F · Capacity — read this before agreeing to anything

Honest arithmetic across all three amendments:

| Amendment | Hours |
|---|---|
| 01 (retrieval, hardening, ADK 2, scale, four contradictions) | 14 |
| 02 (Model Armor bugs and upgrades) | 14 |
| 03 (this one, if fully adopted) | 26 |
| **Total** | **54** |

Your buffer is 20–30 hours. **You cannot do all of it, and trying is how the four pillars end up half-finished on Aug 27.** Here is the split I would defend:

**Tier 1 — do it, ~11h of this amendment.** Every contradiction in Part A (3.25h — they are cheap, and A1 and A2 damage the pitch itself), plus C1 memory poisoning, C2 asymmetric tokens, C4 the P3 policy, C6 span content, C7 cost enforcement (4.5h), plus B1 re-tiering (3h). That set is defensible, cheap, and every item strengthens something you are already demoing.

**Tier 2 — only if Aug 24 is green.** B4 deterministic checks (2h), C3 late events (2h), B2 fourth-party chain (4h, and in the README rather than the video). ~8h.

**Tier 3 — probably not, and that is fine.** B3 follow-ups, B5 Watchdog quality, C5 outbound screening, C8 supersession. Document them in "What's next" on Devpost, which is a section you have to write anyway and which reads better when it contains specific, designed things rather than aspirations.

**Revised master cut order** across all amendments: Contract Clause agent → registry versioning → Amendment 02 U4 image screening → B3 follow-ups → B5 Watchdog quality → question-effectiveness loop → Gemma scrubber → live Watchdog feeds → portal cosmetics.

One thing to protect above all of this: **the demo is full.** Four pillars, 3:55, and every new feature competes for seconds it does not have. B1 earns its place because the tier badge changes on footage you are already shooting. B2 does not — it goes in the README, the binder and a gallery image.

---

## Part G · Which of these is startup-shaped

You are reading §5 with a company in mind, so: of everything above, three items are product rather than polish.

**The fourth-party chain (B2)** is the most commercially interesting thing in this document. It is the natural expansion path — you review a vendor, you discover four subprocessors you have never assessed, and each of those is a review someone should be doing. That is land-and-expand built into the product's own output, and it gets more valuable the more customers you have, because the chains overlap.

**Evidence-corrected re-tiering (B1)** is the feature a buyer would name when explaining why they switched. Every security team has been burned by a review that was scoped from an optimistic intake form.

**Provenance-labelled findings (B4)** is what makes the output survive an audit. "Rule or model" on every finding is the kind of unglamorous distinction that decides enterprise procurement.

Everything else in this amendment is engineering hygiene — necessary, invisible, and not a story. Say so, and be precise about which three you would build first with real money. Being able to name that split is itself a signal that the startup sentence is more than a hackathon flourish.
