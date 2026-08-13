# Drawbridge — Amendments 01–03, propagation changelog

**Applied:** 14 Aug 2026 · **Scope:** every planning document, diagram source, wireframe generator and outward-facing draft in `research/`, excluding master doc §5 and §6, which were rewritten before this pass and are the authority everything else was made consistent with.

**Amendment IDs.** `C1–C5`, `D1–D4` are Amendment 01. `B1–B5`, `U1–U6` are Amendment 02 (Model Armor). `A1–A7`, `B1–B6`, `C1–C8`, `D`, `F` are Amendment 03 — prefixed `03·` below wherever a bare letter would collide with Amendment 02's.

**Conflict resolutions applied, overriding the amendments where they differ:** the rubric sums to **100** (subprocessors 10 → 15), not 95; the number is the **Trust Score, 0–100, higher is safer**, and no instance of "risk score raised" survives; **G1/G2 are human gates, P1/P2/P3 are gateway policies**, never interchangeable; **min-instances 0 everywhere**; Amendment 03 Part F **Tier 2 and Tier 3 items are marked `(Target)`** and appear only in the §5.6 ladder or in "What's next" — never as built behaviour.

---

## `drawbridge-hackathon-master-doc.md`

| § | Amendment | Change |
|---|---|---|
| 1 Executive summary | C1, C4, 03·A1 | Fleet named an **ADK 2 graph workflow**; memory described as four layers; "raises that vendor's risk score" → **drops their Trust Score by 25 points and forces escalation**, with the risk/trust distinction stated |
| 2.2 Sponsor's incentive | C3 | New paragraph: all four webinars answered, each mapped to the § that answers it, including self-improvement → §6.10 |
| 7 Rubric mapping · Innovation | 03·B1, 03·B2 | Re-tiering and the fourth-party chain (Target) added as decisions rather than processing |
| 7 Rubric mapping · Architecture | C1, C3, C4, C5, 03·A5, 03·C2, 03·C3, 03·C4 | Four-layer memory; collection-level identity; three named policies; asymmetric tokens; late-event handling; plan-versioned keys; enforced ceiling; ADK 2 graph workflow with a code-generated diagram; the **scale-safely sentence** (concurrency, fan-out, per-agent instance caps) |
| 7 Rubric mapping · Demo | C2, U6 | Published detection rate across the injection corpus; public surface that reaches no model; Model Armor templates added to the console-shot list |
| 8 Production decisions | 03·B6 | **Time-compression control moved here from §5.5**, with a parenthetical saying so and why (a demo technique, not a product property); "Day 17" → "27 Aug" |
| 8 Demo script 0:45 | C5 | Queue shows **12 reviews in flight**; narration gains the fan-out line |
| 8 Demo script 1:20–1:45 | C1, 03·B1 | Retrieval named in the contradiction beat; **the re-tier beat added at ~1:35** with its narration |
| 8 Demo script 1:45–2:20 | 03·A1, U5 | Narration corrected: the **Trust Score falls** 25 and the band flips; the policy log line names template and filter |
| 8 Demo script 3:10 | U6 | **Detection-rate table** cut into the proof sequence; Model Armor templates added to the console montage |
| 8 Demo script 3:35 | U6 | Metrics card gains "10 of 12 injection variants caught at ingress, the other two named" |
| 9 Elevator | 03·A1 | Rewritten to Trust Score wording |
| 9 Description structure | D (03) | Journeys now J1–**J7** |
| 9 Challenges | B1, C1, 03·A7 | Three named challenges, including **the scrub-before-screen bug** written out with its generalisable lesson |
| 9 Technologies | C1, C4 | ADK 2 graph workflows, `text-embedding-005`, Firestore KNN, Model Armor's two templates, Agent Gateway, Secret Manager |
| 9 Other data sources | U6 | Injection corpus added, disclosed as synthetic |
| 9 Findings & learnings | U6, C3 | The detection rate as **the honest negative result**, with the two failures named; the "cannot game a metric it does not hold the pen for" closing line |
| 9 What's next (new) | 03·F Tier 3 | The designed-but-unbuilt items named specifically: follow-ups, Watchdog guards, outbound screening, supersession, fourth-party expansion |
| 9 Architecture diagram | C4 | `graph_dump.py` output committed alongside, captioned as generated |
| 9 Hosted URL | C2 | Scale-to-zero, statically rendered entry page, cached read paths, rate limits, **min-instances 0** |
| 10 Bonus plan | U6, 03·C1 | Medium outline gains the detection-rate table and the memory-poisoning paragraph; day numbers → dates |
| 11.2 Phase 0 | C4, C5 | **GEAR badge and free sandbox**; ADK 2 version pin; **`graph_dump.py`** run and committed; dates replace all day numbers, with a note saying why |
| 11.2 Phase 1 | C1, D1–D4 | Evidence chunking, embedding and KNN retrieval (Aug 17–19); the four contradictions fixed before M1 |
| 11.2 Phase 2 | B1–B5, U1–U3, U5, 03·C2, 03·B1 | Armor built correctly the first time (screen-before-scrub, unified paths, execution-state check, verdict-bearing stamp, fail-closed, two templates, malicious URI, output screening); asymmetric tokens; re-tiering; structured memory writes |
| 11.2 Phase 3 | C2, U6, 03·F | Public-surface hardening (Aug 26); the injection corpus and its published rate; Tier 2/3 items listed as conditional |
| 11.2 Phase 4 | 03·A6 | Day numbers → dates throughout |
| 11.4 Claude playbook | U6, 03·A6 | Corpus generation added; "Day 1" → "11 Aug" |
| 12 Risk 1 | C5 | GEAR sandbox as the mitigation; dates not day numbers |
| 12 Risk 2 | C2, 03·C7 | Min-instances 0, lifecycle rule, **enforced** ceiling that parks the review |
| 12 Risk 3 | 03·B1 | The re-tier beat as a second live decision moment, so one weak take is not fatal |
| 12 Risk 7, 8 | 03·A6 | Dates not day numbers |
| 12 Risk 9 | U6 | Differentiation now includes a *measured* detection rate |
| 12 **Risk 11 (new)** | C2 | Public endpoint credit drain — no model path, rate limits, max-instance caps, budget alerts, static entry page |
| 12 **Risk 12 (new)** | C4 | ADK 2 surface change — version pin, contract-not-call rule, `step()` vs Workflow day-one check, regenerated graph diagram |
| 12 **Risk 13 (new)** | 03·C1 | Memory poisoning — structured writes, controlled vocabulary, provenance tags, L2 for exact wording |
| 13 Final-week checklist | C2, C4, U3, U6, 03·A1, 03·A4, 03·C2 | Seven new rows: corpus and published table; public-surface audit; templates from `bootstrap.sh`; asymmetric signing verified; Trust Score wording consistent; gate/policy taxonomy; generated graph diagram committed. Quarantine lifecycle added to the cost row |
| Appendix A | C1, U6, 03·B2, 03·B4 | Expected end-states sharpened (retrieved chunk, rule-sourced expiry, unreviewed fourth party); **the twelve-variant injection corpus added** with its table, published result format, the variant-9 blind spot and the two non-negotiable constraints |
| Appendix B | D4, 03·A1, 03·A2, 03·B4, U2, B1 | **Rewritten**: retitled Trust-scoring; domain table summing to **100** with subprocessors at 15 and the reason for that placement; bands; "scoring is arithmetic, not judgement"; a **finding-source mapping table** covering PI, SDP, malicious URI, RAI, deterministic checks, unknown fourth parties and model contradictions, each with domain, severity and `rule`/`model` provenance |
| Appendix C | 03·B1, 03·B3 | Seven domains not eight; tier re-evaluation named; **follow-ups generated from low-confidence answers (Target)** with the worked example and the two-per-question cap |
| Appendix D | C1, U3, 03·B4, 03·C6 | Cover states template-rendered-not-model-written; §1 carries tier changes; §3 carries template id and version; §4 carries retrieval provenance and `rule`/`model` labels; §5 shows arithmetic out of 100; §7 notes spans carry no external content |
| Appendix E | 03·A1, U6, C3 | Elevator rewritten to Trust Score; learning sentence gains the ordering bug; **new containment sentence** (five layers + assume-breach); new measured-defence and self-improvement sentences |

---

## `drawbridge-implementation-handbook.md`

| § | Amendment | Change |
|---|---|---|
| 0 How to use | C4 | ADK 2 named as the surface to verify on day one; the three patterns and why Drawbridge is a graph workflow |
| 1.1 Bootstrap | C1, C4 | `google-cloud-aiplatform` added; **ADK 2 pinned**; two notes on why each matters. "Day 1" → dates |
| 1.2 | C5, 03·A6 | Day-1 non-negotiable rewritten to dates, with the GEAR sandbox first |
| 3.1 Resources | C1, C2, U3 | **Firestore KNN vector index**; **7-day quarantine lifecycle rule**; **both Model Armor templates** with their settings; `sa-armor`; private key note; "create templates in `bootstrap.sh`, not the console" |
| 3.2 Permission matrix | 03·A5, C1, U-index | **Rewritten at collection level**, row-for-row identical to master doc §6.3; `sa-armor` added with its rationale; `sa-evidence` gains `evidence_chunks`; bootstrap loop and quarantine binding updated; verification step now names the collection-level cases |
| 4 `.env.example` | C1, U3, U5, 03·A7, 03·B3, 03·B5, 03·C7 | `MODEL_EMBED`, `VECTOR_TOP_K`, `CHUNK_TOKENS`, `MODEL_ARMOR_TEMPLATE_UNTRUSTED`, `MODEL_ARMOR_TEMPLATE_OUTPUT`, `ARMOR_FAIL_CLOSED`, `PLAN_VERSION`, `FOLLOWUP_CAP`, `WATCHDOG_CONFIDENCE_MIN`; approval key split into private/public; ceiling comment changed from "soft guard" to **ENFORCED** |
| 5.1 Core types | C1, D1, 03·A7, 03·B1, 03·B2, 03·B4, 03·C1 | `EvidenceChunk`, `Subprocessor`, `MemoryNote` (with `provenance`, `supersedes`), `TierChange`; `Review.gate_scope`, `.plan_version`, `.tier_history`; `Finding.source`; a paragraph on why `gate_scope` and `plan_version` exist |
| 5.2 State machine | D1, D3, 03·B1 | **`ALLOWED` rewritten**: `QUESTIONNAIRE_OUT → GATED`, `GATED → QUESTIONNAIRE_OUT`, `NEEDS_HUMAN` from every state and back, and the re-tier backward transitions; three explanatory rules including "tier only moves up" |
| 6.1 Topics | D2 | **`review.rescore` and `watchdog.sweep` added** — eleven topics — with the docs↔`bootstrap.sh` consistency note |
| 6.2 Envelope | 03·A7 | `idem_key` shape updated to `review_id:plan_vN:step_id` |
| 6.3 Delivery | 03·C3 | **Late/out-of-order event table added** with the four defined behaviours and the `guard()` sketch |
| 7.1 Gateway | U5, 03·A4, 03·C4 | **P2 becomes verdict-aware** with `admissible()`; **P3 added**; gate-vs-policy taxonomy stated; `log_policy_block` names policy, template and filter, with the example log line |
| 7.2 `armor.py` | B1–B5, C1, U1, U2 | **Rewritten**: one internal `_screen()` with two wrappers; **screen before scrub**; `verdict_is_trustworthy()` execution-state check; **verdict-bearing signed stamp**; fail-closed; `index_chunks()` after the clean-stamp; a five-row verdict-consequence table; the `sa-armor` findings boundary; **output screening** sketch |
| 7.3 Routing | C1, 03·A2, 03·B1, 03·B3 | **`score_rubric` deleted** (with a comment saying why it must not return); `embed_evidence`, `followup_question`, `classify_data_scope` added |
| 7.4 Idempotency | 03·A7, 03·C8 | Key becomes `review_id:plan_vN:step_id` with a `key_for()` sketch and inherited keys; **TTL on completed records** |
| 7.5 Checkpoint | C4 | Day-one ADK 2 Workflow-vs-`step()` check |
| 7.6 Telemetry | 03·C6 | **Spans carry refs, hashes and enumerated verdicts, never raw external content**, with a wrong/right sketch |
| 7.7 Memory | C3, 03·C1, 03·C8 | `ALLOWED_NOTE_TYPES` and provenance asserted in `remember()`; supersession; **the memory-poisoning rationale**; `question_effectiveness` as the one learning note |
| 8 Orchestrator | 03·A3, 03·B1 | **No Pro** — the escalation deleted, with the reason; **`reassess_tier` step** with its sketch, upward-only rule, plan versioning and the worked example; `test_retier.py` |
| 9 Questionnaire | D1, C3, 03·B3, 03·C5, 03·C3 | Collection-level permissions stated; effectiveness-informed selection (phrasing never scoring); **G2/P1 naming fixed**; `gate_scope="contact"`; **outbound screening before send**; state `guard()` in `on_reply`; unified screening path note; **targeted follow-ups (Target)** with sketch, prompt example and cap |
| 10 Evidence | C1, 03·B2, 03·B4 | **Two-pass → three-pass** (extract / retrieve / reconcile); `cross_examine` sketch over retrieved passages; prompt rules for chunk citation; severity assigned here; **`deterministic_checks()` with `source="rule"`**; **subprocessor extraction (Target)**; hero finding now asserts a retrieved chunk; retrieval degraded-mode fallback |
| 11.1 Scoring | D4, 03·A2 | **100-point rubric** with subprocessors at 15 and the reason; **no model call in scoring**, `score_rubric` deletion restated; reconciliation with Appendix B and the binder |
| 11.2 Memo | U1 | Memo screened before display; sanitised content inadmissible to this call |
| 11.3 Adversarial Conduct | 03·A1, U2, B1 | Trust Score wording; template and filter in the summary; `source="rule"`; **`findings_from_verdict()`** for SDP and malicious-URI findings |
| 12 Watchdog | 03·B5, 03·C4, D2 | `watchdog.sweep` named; **P3 allowlist**; **identity matching, confidence threshold, triage queue** with sketch, marked (Target) |
| 13 Gemma | B1 | **Role changed to scrub-after-screen, guided by SDP hits**, with the reason the old order was wrong; the optional-degrades vs mandatory-fails-closed asymmetry |
| 14 Approval tokens | 03·C2, 03·A4, D1 | **Asymmetric signing** with both sketches and the forgery argument; G1/G2 named as human gates with P1 as the policy; `gate_scope` on both parks; `test_token_forgery.py` |
| 15 Binder | 03·C6, C1, U3, 03·B4, D4 | **Template-rendered, never model-rendered**, stated on the cover; the three provenance labels; section calls updated for tier history, template id/version, chunk/page, rule/model and 100-point arithmetic |
| **16.5 (new)** Public surface | C2 | The no-model-path rule, the four measures, min-instances 0, and the CI grep |
| 17 Vendor pack | C1, C5, 03·B2 | Expected outcomes sharpened; **seed 10–12 reviews**; a deliberately vague answer for the follow-up path |
| **17.1 (new)** Injection corpus | U6 | The twelve-variant table, the published result format, the variant-9 blind spot and its bounding rule, and the two non-negotiable constraints |
| 18 Cost | C1, C2, 03·C7 | Embedding cost row (and why retrieval *reduces* spend); public-route row; lifecycle row; min-instances 0 everywhere; **enforced ceiling** with sketch |
| 19 Testing | C1, U6, B2, 03·A5, 03·B1, 03·C3, 03·C2 | Corpus run and false-positive check; fail-closed-on-skipped-detector; collection-level IAM test; retrieval assertion on the hero finding; **`test_retier.py`, `test_late_events.py`, `test_token_forgery.py`** |
| 20.0 (new) | B5, C1, 03·C3, 03·C7 | **Optional-degrades vs mandatory-fails-closed table**, including retrieval fallback, late events and the cost ceiling |
| 20.3 | 03·F | Cut order updated to the revised master order; corpus above the Gemma scrubber |
| 21 Phase 0 | C4, C5, D2, D4, U3 | GEAR badge and sandbox; ADK 2 pin; `graph_dump.py`; eleven topics; both templates from `bootstrap.sh`; lifecycle rule; six service accounts at collection level; rubric summing to 100; 10–12 seeds |
| 21 Phase 1 | C1, D1–D4, 03·A2, 03·A7, 03·C3, 03·C6, 03·C7 | The four contradictions as a starred row; P3; plan-versioned keys with TTL; span content rule; enforced ceiling; retrieval; no `score_rubric` |
| 21 Phase 2 | B1–B5, U1–U3, U5, 03·B1, 03·C1, 03·C2 | Ten new rows covering the armor rebuild, output screening, asymmetric tokens, re-tiering and the structured memory guard |
| 21 Phase 3 | C2, U6, 03·B4, 03·C3, 03·B2, 03·F | Public-surface hardening; corpus and false-positive check; binder provenance; stretch list restated in cut order; four-layer memory language |
| 21 Phase 4 | C4, C5, C1, 03·B1 | Live-take shot list gains the 12-review queue and the re-tier; technologies list updated |
| 22 Definition of done | U6 | The corpus and its published rate added to the completion bar |

---

## `drawbridge-architecture-doc.md`

| § | Amendment | Change |
|---|---|---|
| 2 System overview | B1, C1, C2, C4, 03·C4, B5 | Screening-before-scrub order; ADK 2 graph workflow; three policies; four memory tiers; degrade-vs-fail-closed; **a new paragraph on the public-surface boundary**, including the absent edge a diagram cannot draw |
| 3 Repo tree | C1, C2, U3, U6, 03·B2, 03·B4, 03·C2, 03·C3 | `retrieval.py`, `checks.py`, `subprocessors.py`; `app/(public)/`; `approvals/`; `infra/model_armor/`; `injection-corpus/`; eleven topics; six identities; three new tests |
| 4 Tool table | 03·A2, C1, U1, 03·B1, 03·C4, 03·C6, 03·C2, 03·A7 | **`score_rubric` replaced by `compute_score` (no model)**, with a note saying so; `retrieve_passages`, `screen_output`, `reassess_tier`, `fetch_url` (P3) added; binder templated; token asymmetric |
| 5 One review end to end | 03·A4, C1, 03·B1 | **G2/P1 taxonomy stated in full**; retrieval in the contradiction beat; **the re-tier as the second decision moment** |
| 6 Adversarial pipeline | B1–B5, U1, U6, 03·A1 | Ordering fix with its rationale; **the five layers named**; verdict-bearing P2; Trust Score falls; the assume-breach sentence; the measured detection rate |
| 7 Memory hierarchy | C1, 03·C1, 03·C8 | **Three layers → four**, with the full table; L2.5 rationale and degraded mode; the structured-write guard as a security control; supersession |
| 8 Security architecture | 03·A5, 03·C2, 03·C4 | **The collection-level permission matrix inlined**; three named policies; **asymmetric approval tokens** |
| 9 Data architecture | 03·A7, C1, D1, D3, 03·B1, 03·C3 | Plan-versioned keys; `evidence_chunks` KNN; the three state-machine exceptions; **the late-event behaviours** |
| 10 Decision log | C1, C4, B1, U6, 03·A2, 03·A3, 03·A7, 03·C2, C2 | Nine rows rewritten or added — ADK 2 with its two rejected patterns named, Pro in exactly two places, **scoring with no model call**, retrieval, scrub-after-screen, plan-versioned keys, collection-level identity, asymmetric approval, public surface, the measured guardrail |
| 10 (new entries) | U-index, C3 | **§6.9 adversarial content defence** and **§6.10 bounded self-improvement** added as decision-log entries |

---

## `drawbridge-submission-description.md` *(outward-facing)*

| § | Amendment | Change |
|---|---|---|
| What it does | 03·A1, U6 | "raises that vendor's risk score" → **drops their Trust Score by 25 points**; a new paragraph on the measured defence |
| Capability 1 | 03·B1 | **Evidence-corrected re-tiering**, with the conflicted-initiator argument |
| Capability 4 | D4, 03·A1, 03·A2, 03·B4, U1 | Seven domains; **Trust Score 0–100, higher is safer**; no model call in scoring; `rule`/`model` provenance; memo screened |
| Capability 5 | 03·A1, U1, U3, U6, B2 | Trust Score drops; five families, two templates, fail-closed; output screening; twelve variants in CI |
| Capability 6 | 03·B5, 03·C4 | P3 allowlist; identity matching, relevance threshold, triage queue |
| Capability 7 | 03·C6, U3, C1, 03·B4 | Template-rendered binder; template id/version; retrieval provenance; rule/model labels; spans carry no raw text |
| Memory hierarchy | C1, 03·C1 | **Three layers → four**; structured writes and why |
| Security architecture | 03·C2, 03·C4, 03·A5 | Five layers; three policies; collection level; asymmetric tokens; **the assume-breach sentence** |
| Resumability | 03·A7 | Plan-versioned keys |
| Deployment and cost | C2, 03·C7 | Min-instances 0; **enforced** ceiling; no-model public surface |
| Technology stack / Built with | C1, C4 | ADK 2 graph workflows, `text-embedding-005`, Firestore KNN, two Model Armor templates; tag list updated |
| Challenges | B1, 03·A7 | **The scrub-before-screen bug** written out with its lesson; plan versioning added to the idempotency challenge |
| Accomplishments | U6, 03·B1, 03·C6 | Trust signal wording; the measured guardrail; re-tiering; templated binder; enforced ceiling |
| What I learned | U6, 03·C1, C3 | Three new lessons: a guardrail without a number is an anecdote; memory is an attack surface; improve how it asks, never how it scores |
| **Designed but not built (new)** | 03·F Tier 3, U4 | Follow-ups, outbound screening, supersession, image-layer screening — named as designs that lost a scheduling argument, with the variant-9 blind spot stated |
| Try it yourself | U6 | The corpus and its CI job described, with the synthetic/technique-class constraint |

---

## `drawbridge-content-social-playbook.md` *(outward-facing)*

| § | Amendment | Change |
|---|---|---|
| Blog 1 subtitle | 03·A1, U6 | "risk signals" → "trust signals"; the measured-defence clause added |
| Blog 1 §1 cold open | 03·A1 | "raises their risk score" → **drops their Trust Score 25 points, forcing escalation** |
| Blog 1 §4 | 03·C4, 03·C2, 03·A7, C1, 03·A5 | Two policies → **three**; asymmetric key; plan-versioned keys; three memory layers → **four** plus the structure rule; collection-level identity |
| Blog 1 §5 | B1, 03·A1 | Pipeline order corrected (screen, then scrub); the consequence framed as trust falling |
| Blog 1 **§5b (new)** | U6 | The detection-rate section — the twelve technique classes, the honest table, and why the honest number is the stronger play |
| Blog 1 **§5c (new)** | B1, 03·C1 | The scrub-before-screen bug and its generalisable lesson; a memory-poisoning paragraph |
| Blog 2 outline | C1, 03·A7, 03·C1 | Four layers with the retrieval tier; plan versioning; the structure rule as the more interesting half of the memory story |
| LinkedIn post | 03·A1, U6, C4 | Trust Score wording; a corpus paragraph; ADK → ADK 2 |
| X thread | 03·A1, U6, C4 | Tweet 1 rewritten; **new tweet 3** carrying the detection rate; ADK 2 graph workflows |
| 30-second clip | 03·A1 | Caption "Risk score raised −25" → **"Trust Score −25, escalation forced"** |

---

## `diagram guide/` — Mermaid sources (`drawbridge-diagrams/src/*.mmd`)

| Diagram | Amendment | Change |
|---|---|---|
| **01** system architecture | C1, C2, C4, B1, U1, U3, D2, 03·A4, 03·A5, 03·C4, 03·C6 | Zone ② reordered to **screen-then-scrub**; ARMOR label gains five filters / two templates / fail-closed; quarantine gains the 7-day rule; clean bucket gains the verdict-bearing stamp; Z3 gains `review.rescore` and `watchdog.sweep`; Z4 relabelled **ADK 2 graph workflow**; Z5 gains **P3**, `EMB` and `OUTSCREEN`; Z6 retitled **four layers** with `L25` inserted; Z7 gains `PUB` (**deliberately with no edge to the model plane**) and G2 renamed; Z8 IAM → six identities, spans carry no raw content, binder templated. `linkStyle 8` preserved on the threat edge |
| **02** fleet overview | 03·A4 | `P1 gate` → **G2 first outbound contact, enforced by P1** |
| **03** lifecycle sequence | C1, B1, 03·A4, 03·A2, 03·B1, U1, 03·A1 | Screen-before-scrub and chunk/index beats; **retrieve top-k** and deterministic-checks self-messages; **re-tier beat**; no model call in scoring; memo screened; Trust Score 71 of 100; gate naming corrected |
| **04** injection defense | B1–B5, U1, U2, U6, C1, 03·A1 | **Rewritten**: ordering fixed; `TRUST`/`PARK` execution-state branch; SDP and malicious-URI finding branches; verdict-bearing stamp; **`CHUNK`** between clean and P2; output screening before G1; Trust Score −25; a measured-defence note |
| **06** memory hierarchy | C1, 03·C1, 03·C8 | Retitled **four layers, four jobs**; `L25` and `CROSSEX` inserted with the degraded-mode edge; a `STRUCT` guard node and a `POISON` node |
| **07** event backbone | 03·A7, 03·C3 | `idem_key` gains `plan_vN`; **a late/out-of-order `ORDER` note added**. (D2 needed no change — both topics were already drawn) |
| **08** state machine | D1, D3, 03·B1, 03·A4, 03·C2 | Gate labels corrected to the taxonomy; **re-tier transitions added**; `NEEDS_HUMAN` from `GATED`, `DECIDED`, `MONITORED`; the `GATED` note rewritten with gates-vs-policies and public-key verification; a re-tier note added |
| **09** permissions | C1, 03·A5, U-index, 03·C2 | **Six identities** with `sa-armor` and its grants/denials; rows rewritten at **collection level**; P3 named on the Watchdog row; a `COLL` note on why rows name collections; service-identity note gains the private-key holder |
| **10** trust scoring | D4, 03·A1, 03·A2, 03·B4, U1 | Retitled; findings carry the retrieved passage and a rule/model label; **domains total 100** with subprocessors at 15; −25 trust points; **`GAME` note** (cannot game its own metric); **`TRUST` note** (0–100, higher is safer, the score falls); output screening before the gate |
| **11** audit binder | C1, U3, 03·B4, 03·C6 | Sources gain template id/version and provenance; generator marked **template-rendered, never model-rendered**; sections 3, 4 and 5 relabelled; a `TPL` note on why |
| **12** tech stack | C1, C3, C4, 03·A5, 03·C4, 03·C2, U3, U6, 03·C3, 03·C7, 03·A7 | ADK 2 graph workflows; `text-embedding-005`; KNN index; lifecycle rule; six SAs at collection level; P3; asymmetric tokens; two templates and fail-closed; the corpus; late-event handling; enforced ceiling; bounded self-improvement |
| **13** data model | C1, D1, 03·A7, 03·B1, 03·B2, 03·B4, 03·C1, 03·C8, U3, 03·B5 | New entities `EVIDENCE_CHUNK`, `TIER_CHANGE`, `SUBPROCESSOR` with their relationships; `gate_scope`, `plan_version` on `REVIEW`; `source` on `FINDING`; screening gains template/version/per-filter verdicts/sanitised; idem key gains `plan_vN` and a TTL note; dossier gains `question_notes`, provenance and supersedes; watchdog task gains signal id and confidence |
| **14** deployment and cost | C2, C4, U-index, 03·C2, 03·C7, 03·A6 | ADK 2 and `sa-armor`; private/public key split; **`PUBSAFE` and `LIFECYCLE` cost nodes**; the meter becomes **enforced**; the day-one note re-dated and gains the GEAR sandbox |
| **15** build timeline | C1, C2, C4, C5, 03·C2, 03·B1, U6 | New bars: GEAR/rules, ADK 2 pin and graph dump, evidence retrieval (Aug 17–19), asymmetric tokens, re-tiering and the memory guard, public-surface hardening (Aug 26), injection corpus |
| **16** synthetic vendors | C1, C5, U6, 03·B2, 03·B4, 03·A1 | DataDynamo expects a **retrieved chunk** and a rule-sourced expiry; NimbusWrite expects a Trust Score drop and an unknown fourth party; **`SEED`** (10–12 reviews) and **`CORPUS`** nodes added |
| **17** approval tokens | 03·C2, 03·A4, D1 | Participants relabelled **public-key gateway / private-key approval service**; RS256; a forgery-attempt beat added; the closing note rewritten around asymmetry |
| **18** personas | 03·A4 | `P1 · approve first contact` → **G2, enforced by P1** |
| **19** questionnaire loop | 03·A4, 03·B3, 03·B1, 03·C5, 03·A7 | Gate naming corrected; outbound screening on send; plan-versioned key; **`FOLLOW` (Target)** and **`RETIER`** nodes added |
| **20** failure semantics | B5, C1, 03·A2, 03·C3, 03·C7 | Scorer node corrected (no model call); `P5` restated as **optional degrades**; **new `P7` mandatory-fails-closed**, `P8` late events, `P9` enforced ceiling |
| **21** tests and claims | C1, U6, 03·B1, 03·C3, 03·C2, 03·A1, 03·A6 | `test_armor_flow` claim becomes **measured, not asserted**; `test_cross_exam` asserts a resolved chunk; **new `T6/C6/D6` row** for re-tier, late events and token forgery; the 1:45 beat says the Trust Score falls; day numbers → dates |
| **22** demo shot map | C5, 03·B1, U6, 03·A1 | 0:45 shows 12 reviews; **new 1:35 re-tier beat**; 1:45 says Trust Score falls; 3:10 includes the detection table |
| **23** ADK 2 graph dump | C4 | **Deliberately no `.mmd` source.** Documented in `DIAGRAMS.md` and `DIAGRAM-GUIDE.md` §26 with the `graph_dump.py` command; it is committed tool output, not a drawing |
| **24 (new)** fourth-party chain | 03·B2 | New source file `24-fourth-party-chain.mmd`: you → vendor → subprocessors, unknowns in red, structured extraction and deterministic set-difference, marked **(Target)** and explicitly kept out of the video |

### `DIAGRAMS.md` and `DIAGRAM-GUIDE.md` *(both top-level and `drawbridge-diagrams/` copies, kept identical)*

| Amendment | Change |
|---|---|
| all | Counts 22 → 24; a status banner stating the sources are current and the exports are stale |
| C4, 03·B2 | Catalogue rows and full write-ups for **23** (generated, not drawn) and **24** (Target) |
| D1–D4 | The "four corrections you still owe" sections **rewritten as resolved**, with what each fix was — nothing deleted |
| 03·A1, 03·A4 | New §25.1 settling the Trust Score and gate/policy vocabulary across every artefact |
| all | New §25.2 table: the nine structural changes the amendments made, which diagrams each touched, and why each is not cosmetic |
| C2 | The absent public→model edge documented in prose, since a diagram cannot draw it |
| 03·F | The honesty rule extended to every `(Target)` item — delete, don't grey out |
| C1, D4, 03·A1 | Diagram 06 and 10 write-ups rewritten for four layers, the 100-point scale and the Trust Score naming |
| C4 | §26 gains the whole-set regeneration loop and the `graph_dump.py` command |

---

## `frontend/`

### `FRONTEND.md` *(both copies, kept identical)*

| § | Amendment | Change |
|---|---|---|
| header | all | Status banner: document and generators current, exports stale |
| 1 routes | 03·A4 | `gate card (G1) — also renders the P1 card` → **G2 first-contact card** |
| 1.1 S0 | C2 | **The no-model-path rule** added to the S0 description, with the min-instances-0 consequence |
| 2 The cold start | C2 | **Replaced wholesale.** The min-instances-1 recommendation is superseded and marked as such; static rendering, cached reads, no model path |
| 4 S1b | C1, U3, 03·B1, 03·B4 | The expanded entry gains **retrieval provenance**; the evidence inventory shows **per-filter** verdicts rather than one pill; a tier-change timeline entry |
| 4 S1c | 03·A1, U5 | **TRUST SCORE**, never RISK SCORE, and the number falls; the blocked line names template and filter |
| 4 S1d | U1, D4, 03·B4 | Memo-screened line on the gate card; arithmetic **out of 100**; rule/model provenance chips |
| 4 S1e | 03·A4, D1 | G2/P1 naming; `gate_scope="contact"` |
| 9 Performance floor | C2 | **min-instances 1 bullet replaced** with the no-model-path rule, rate limits and the CI grep |
| 10 Regenerating | all | Stale-export warning naming which wireframes changed |

### `frontend/drawbridge-frontend/src/*.py` *(wireframe generators)*

| File | Amendment | Change |
|---|---|---|
| `s01_02.py` (W1, W2) | 03·A1, C5 | S0 copy rewritten to Trust Score; **queue chips 8 → 12** with the sub-counts adjusted |
| `s03_04.py` (W3, W4) | 03·A1, C1, U3, U5, 03·B1, 03·B4 | `RISK SCORE` → **`TRUST SCORE`**; a sixth metadata cell **`SOURCE · SOC 2 p.42 §3.2`** with spacing 162 → 138; a **re-tier timeline entry**; per-filter evidence-inventory verdicts naming the template; findings carry `rule`/`model`; the blocked and P2 lines name template and filter; the payload text no longer says "risk score" |
| `s05_07.py` (W5, W6, W7) | 03·A1, D4, U1, 03·B4, 03·A4 | `RISK SCORE` → **`TRUST SCORE`**; the breakdown table re-weighted (**subprocessors 15**) and totalling **71 / 100**; a memo-screened line; a provenance line; the P1 card relabelled **G2 · FIRST OUTBOUND CONTACT** with a `P1 BLOCKED AT GATEWAY` pill; the binder cover reads **Trust Score 31 / 100** |
| `s08_10.py`, `wireframes.py` | — | No change required |

---

## Regeneration still outstanding

Nothing in this pass regenerated a binary asset. All of the following are unrun:

```bash
# Mermaid — every PNG and SVG in the diagram set is stale
cd "research/diagram guide/drawbridge-diagrams"
for f in src/*.mmd; do
  n=$(basename "$f" .mmd)
  mmdc -i "$f" -o "png/$n.png" -c mermaid-config.json -b white -s 2 -w 2000
  mmdc -i "$f" -o "svg/$n.svg" -c mermaid-config.json -b transparent
done

# Wireframes — W2, W3, W4, W5, W6, W7 changed
cd research/frontend/drawbridge-frontend
python3 src/wireframes.py
python3 -c "import cairosvg,glob,os;[cairosvg.svg2png(url=f,write_to='png/'+os.path.basename(f)[:-4]+'.png',scale=1.4) for f in glob.glob('svg/W*.svg')]"
mmdc -i mmd/F1-surface-map.mmd -o png/F1-surface-map.png -c mermaid-config.json -b white -s 2 -w 2000

# Diagram 23 — generated from the code, not authored; run once the Orchestrator exists
python scripts/graph_dump.py --workflow agents.orchestrator:workflow \
       --out docs/diagrams/23-adk2-graph-dump.svg
```
