# Drawbridge — Amendment 01
### Nine changes, where each one lands, and how to keep the repo consistent
**Raised:** 14 Aug 2026 · **Owner:** Ambrstack · **Status:** proposed, apply before M1 where marked ★
**Sources:** the hackathon webinar schedule, the Fortified Enterprise Fleet track detail, the GEAR section, and the cost pro-tips page
**Affects:** `drawbridge-hackathon-master-doc.md`, `drawbridge-implementation-handbook.md`, 22 diagrams, `FRONTEND.md`, 10 wireframe SVGs

---

## 0 · How to use this document

Neither source document needs rewriting. Section 1 is the change register — read it and decide. Section 2 gives the exact edit for each change, grouped by the file it lands in, with old-and-new text where a copy-paste is possible. Section 3 is the same information inverted: **one list per file**, so you can open a file once and make every edit to it in one sitting. Section 4 is the consistency pass that proves you didn't miss one. Section 5 is the schedule cost and what to cut if it doesn't fit.

Changes are numbered **C1–C5** (driven by the new hackathon information) and **D1–D4** (contradictions already present inside your own documents, found during the diagram audit). The D-changes are not optional — each becomes a runtime bug.

---

## 1 · Change register

| ID | Change | Driver | Hours | Phase | If skipped |
|---|---|---|---|---|---|
| **C1** ★ | Semantic retrieval layer (L2.5) in the Evidence agent — Firestore KNN over chunked, screened documents | Aug 27 webinar names *Vector Search* as a memory tier; cost tips bless *serverless vector search* | 6 | 1 | Cross-examination stays a whole-document Pro call — unreliable, expensive, and `evidence_ref` is a best-effort claim rather than a retrieval result |
| **C2** ★ | Public-surface hardening — no model call reachable without a token; S0 statically rendered; rate limits; quarantine lifecycle rule | Cost tips: *protect public Cloud Run URLs… so unexpected web traffic can't drain your credits*, and *keep minimum instances at 0* | 3 | 3 | A bot on your hosted URL burns Gemini tokens; also reverses my earlier min-instances-1 advice, which conflicted with the organisers' guidance |
| **C3** | The self-evolving-agent answer — architectural position plus one bounded learning loop on question phrasing | Aug 20 webinar is the only one Drawbridge has no answer to; *"catch it gaming the metric"* is an invitation | 1 (position)<br/>4 (loop, stretch) | 3 | You leave a graded theme unaddressed while already holding the best answer to it |
| **C4** | ADK 2 vocabulary — name Drawbridge a **graph workflow**, and commit a code-generated structural diagram | Aug 11 webinar: *Mastering the Three Orchestration Patterns of ADK 2* | 1 | 0–1 | You describe your orchestration in generic terms while the sponsor has just published a taxonomy |
| **C5** | "Scale them safely" — seeded concurrency in the demo, plus GEAR sandbox on day one | Track text: *discover… audit… trust… and scale them safely*; GEAR gives 35 free monthly credits | 2 (−time saved) | 0, 4 | Your weakest word in the track brief stays weakest, and you burn paid credits learning GEAP |
| **D1** ★ | `GATED` gains `gate_scope` (`contact` \| `decision`) | §9 parks first contact in `GATED`; the §5.2 table forbids it | 0.5 | 1 | The state validator raises at the 1:05 demo beat |
| **D2** ★ | Add `review.rescore` and `watchdog.sweep` to the topic table | §11.3 publishes one, §12 implies the other; §6.1 lists neither | 0.25 | 1 | Undocumented means untested |
| **D3** ★ | `NEEDS_HUMAN` reachable from every state | §5.2 prose says any state; its table omits four | 0.25 | 1 | Failure paths you documented cannot execute |
| **D4** ★ | Tier-1 rubric sums to 95, not 100 | Appendix B: 20+15+15+15+10+10+10 | 0.5 | 1 | The binder prints arithmetic that doesn't reconcile with bands read as percentages |

**Total: ~14 hours, of which 4 are stretch.** Against a 20–30% buffer on a 125–150 hour scope, this fits without touching the cut ladder.

---

## 2 · The changes in detail

### C1 · Semantic retrieval (L2.5)

**What it is.** After a document passes screening and is clean-stamped, chunk it, embed each chunk with Vertex AI text-embeddings, and store the vectors in Firestore with a KNN index. At cross-examination time, retrieve the top-k passages per questionnaire claim and hand *those* to Pro, instead of the whole document.

**Why it is load-bearing, not decorative.** A Tier-1 SOC 2 runs 60–100 pages. Your hero finding depends on Pro locating exception note 3.2 inside it. Retrieval turns that from luck into a query, makes `FINDING.evidence_ref` an actual pointer, and cuts Pro tokens at the same time. It also gives you the third tier the memory webinar is built around.

**Where it sits in the hierarchy.** L1 session · L2 Firestore ledger · **L2.5 semantic retrieval** · L3 Memory Bank. L2.5 answers a different question from all three: *which passage says this?*

**Degradation rule (non-negotiable).** If the index or embedding call is unavailable, log a degraded-mode warning and fall back to whole-document context. Retrieval must never be on the critical path — same rule as the Gemma scrubber.

#### Master doc edits

| § | Edit |
|---|---|
| 5.4.3 Evidence Agent | Change "Two-pass design" to **three-pass**: extract (Flash) → retrieve (KNN) → reconcile (Pro). Add to Tools: *Firestore vector read; Vertex AI text-embeddings*. |
| 6.2 State and memory hierarchy | Change "three explicit layers" to **four**, inserting: *(b½) a semantic retrieval layer — screened evidence chunked, embedded and indexed in Firestore KNN, so cross-examination retrieves the passage that contradicts a claim rather than re-reading the document*. Update the "Judge sees" line to mention the retrieval provenance shown in the UI. |
| 6.6 Model economics | Add `text-embedding-005` to the routing table at roughly $0.000025 per 1k characters; note that retrieval **reduces** Pro spend, so the <$0.50/review target holds. |
| 9 Technologies | Add: *Firestore KNN vector search, Vertex AI text-embeddings*. |
| 11.2 Phase 1 | Add "evidence chunking, embedding and KNN retrieval" to the Aug 17–19 block. |
| Appendix D | Section 4 now carries retrieval provenance — chunk id and page — alongside the source passage. |

#### Handbook edits

| § | Edit |
|---|---|
| 1.1 bootstrap | Add `google-cloud-aiplatform` to the pip line. |
| 3.1 What gets created | New row: *Firestore KNN vector index · `evidence_chunks.embedding` · composite with `review_id` for pre-filtered search*. |
| 3.2 Permission matrix | **`sa-evidence` changes**: add `evidence_chunks` read/write to Granted. Its denials are unchanged — still no egress, no email, no quarantine. This is a real IAM edit, not just documentation. |
| 4 `.env.example` | Add `MODEL_EMBED=text-embedding-005`, `VECTOR_TOP_K=6`, `CHUNK_TOKENS=400`. |
| 5.1 Core types | Add `EvidenceChunk(chunk_id, review_id, doc_ref, page, text, embedding)`. |
| 7.2 `armor.py` | After `storage.write(BUCKET_CLEAN, …)`, add `index_chunks(clean_ref, review_id)` — chunk, embed, write with the review-scoped pre-filter. Chunking happens **after** the clean-stamp, never before. |
| 7.3 ROUTING | Add `"embed_evidence": MODEL_EMBED`. |
| 10 Evidence agent | Rewrite "Two-pass design" as three-pass. Update `CROSS_EXAM_PROMPT` to receive *retrieved passages*, and add a rule: *cite the chunk id you used; if no retrieved passage supports a contradiction, it is a gap, not a contradiction.* |
| 19 Testing | `test_cross_exam.py` gains an assertion: the finding's `evidence_ref` resolves to a chunk whose text contains the SOC 2 exception language. |
| 20 Failure modes | New row: *embedding or index unavailable → degraded-mode warning, whole-document fallback, logged.* |

---

### C2 · Public-surface hardening

**The conflict this resolves.** The rules require a hosted URL that loads logged-out. The organisers warn that public Cloud Run URLs drain credits and that min-instances should stay at 0. My earlier frontend advice (min-instances 1) sided with the rules against the organisers. This resolves both.

**The rule to adopt, stated once and enforced structurally:**

> No route reachable without a token may reach `shared/models.py`'s router.

Public routes render from cached Firestore reads only. A bot hitting your URL costs fractions of a cent in reads, never Gemini tokens.

**Four concrete measures.**
1. **S0 statically rendered** (Next.js SSG), with the live stats strip hydrating from one cached aggregate endpoint. A static page cold-starts in ~1s, which removes the argument for min-instances 1 entirely — keep 0 and keep the credits.
2. **Per-IP rate limit** on all public routes; `max-instances 2`.
3. **Token required for every write** — intake, approvals, portal submissions, exports — which is already true and now stated as a boundary rather than an implementation detail.
4. **Cloud Storage lifecycle rule** deleting quarantine objects after 7 days. The blocked excerpt already lives in Firestore as inert text, so the binder survives the deletion — and *"we do not retain hostile payloads longer than we need them"* is a security story as well as a cost one.

#### Master doc edits

| § | Edit |
|---|---|
| 6.8 Deployment topology | Add: *public read-only surface is statically rendered and reaches no model; writes require a signed token; per-IP rate limits and max-instances caps on every public service.* |
| 9 Hosted URL | Replace any implication of a warm instance with: *scale-to-zero, statically rendered entry page, cached read paths.* |
| 12 Risk register | New risk #11: *public endpoint credit drain — Medium — no model path on public routes, rate limits, max-instance caps, budget alerts, and static rendering of the entry page.* |

#### Handbook edits

| § | Edit |
|---|---|
| 3.1 | Add a lifecycle rule row on `${PROJECT}-evidence-quarantine` (7 days). |
| 16 Frontend | New §16.5 *Public surface* stating the no-model-path rule and the four measures. |
| 18 Cost engineering | Add rows: *public routes — no model calls, rate-limited, max-instances 2*; *quarantine lifecycle — 7-day delete*; and reaffirm *min-instances 0 everywhere*. |
| 21 Phase 3 checklist | Add: ★ *public surface audited — no route without a token reaches a model; rate limits in place; S0 statically rendered.* |

---

### C3 · The self-evolving-agent answer

**The position (free, one paragraph, adopt regardless).** The Aug 20 webinar ends on *"then catch it gaming the metric."* Drawbridge's answer is structural: **the model judges severity, Python computes the score.** No agent in the fleet holds the pen on its own metric, so self-improvement cannot leak into scoring. Say exactly that in the Devpost writeup, the Medium article, and one line of narration.

**The bounded loop (stretch, 4h, Phase 3 only if green).** At review close, `remember()` also writes *question effectiveness* — which questions produced low-confidence parses or non-answers of the "we follow best practices" variety. The next review's Questionnaire agent prefers the phrasings that produced usable evidence.

**The boundary, stated in the docs and enforced in code:** *the fleet may improve how it asks; never how it scores.* Question phrasing is safe to learn because a bad question produces a visible gap, not a silently wrong number.

#### Edits

| File | § | Edit |
|---|---|---|
| Master doc | 2.2 | Add a sentence: all four webinars are answered — orchestration (§6.1), long-running workflows (§6.5), memory (§6.2), and self-improvement (§6.9, below). |
| Master doc | new 6.9 | *Bounded self-improvement.* Decision → Why → What the judge sees, in the same form as the rest of §6. |
| Master doc | 9 Findings & learnings | Add the "cannot game a metric it does not hold the pen for" line — it is a strong closing thought. |
| Handbook | 7.7 `memory.py` | Add `MemoryNote` type `question_effectiveness`, written at review close only. |
| Handbook | 9 Questionnaire | Add: selection from `bank.yaml` consults recalled question-effectiveness notes; phrasing may be preferred, never invented, and never scored. |
| Handbook | 21 Phase 3 | Add as a stretch item, below the Gemma scrubber in priority. |

---

### C4 · ADK 2 vocabulary

ADK 2's three patterns are **graph workflows** (structure known before the input arrives), **collaborative agents** (team known, request picks the subset), and **dynamic workflows** (shape depends on the input).

**Drawbridge is a graph workflow.** A tiered review plan is drawn before the vendor replies. Say it in those words — it signals you watched, and it justifies the design against the two alternatives you did not pick.

**The free artefact.** The ADK 2 codelab ships `scripts/graph_dump.py`, which points at any Workflow and prints its real edges. Run it against the Orchestrator and commit the output to `docs/diagrams/`. **A diagram generated from the code is the strongest possible answer to "does the picture match the repo."**

| File | § | Edit |
|---|---|---|
| Master doc | 6.1 | Add: *the fleet is an ADK 2 graph workflow — known structure, drawn before the input arrives — with event-driven dispatch between nodes.* |
| Master doc | 9 Technologies | `ADK (Python)` → `ADK 2 (Python) — graph workflows`. |
| Handbook | 0 | Reaffirm the "keep the contract, adapt the call" rule, now naming ADK 2 as the surface to verify on day 1. |
| Handbook | 1.1 | Pin the ADK 2 version in the pip line once verified. |
| Handbook | 7.5 `checkpoint.py` | Day-1 check: does ADK 2's Workflow node model subsume `step()`? If it does, keep the wrapper as the checkpointing layer and note the relationship rather than duplicating it. |
| Handbook | 21 Phase 0 | Add: ★ *run `graph_dump.py` against the Orchestrator; commit the generated structural diagram.* |

---

### C5 · "Scale them safely" and GEAR

The track asks how an organisation can *discover your agents, audit their reasoning, trust their data handling, and **scale them safely***. You are strong on the first three. Scale is one fleet, one department, one review at a time on camera.

**Two cheap fixes.** Seed 10–12 reviews so the queue shows genuine concurrency; add one line about Pub/Sub fan-out with per-agent max-instance caps. J6 covers organisational scale; this covers operational scale.

**GEAR, on day one.** Free, no prerequisites, 35 monthly credits on Google Skills, and a **no-cost sandbox**. Burn the Agent Engine and Model Armor learning curve there *before* touching the $150. This is a direct mitigation for risk #1 and it saves more hours than it costs.

| File | § | Edit |
|---|---|---|
| Master doc | 7 Architectural Discipline | Add a scale sentence: concurrent reviews, per-agent instance caps, event fan-out. |
| Master doc | 8 Demo script, 0:45 | The queue shot shows 12 reviews in flight, not 4. |
| Master doc | 11.2 Phase 0 | Add: claim the GEAR badge; run the Agent Engine and Model Armor labs in the free sandbox before spending credits. |
| Handbook | 17 | Seed count rises to 10–12 (the three hero vendors plus filler with realistic states). |
| Handbook | 21 Phase 0 | Add: ★ *GEAR badge claimed; GEAP components de-risked in the free sandbox.* |

---

### D1–D4 · The four internal contradictions

Full reasoning is in `DIAGRAM-GUIDE.md` §25. The edits:

| ID | File | § | Edit |
|---|---|---|---|
| D1 | Handbook | 5.2 | Add `gate_scope: Literal["contact","decision"]` to `Review`. Extend `ALLOWED`: `QUESTIONNAIRE_OUT: {REPLIES_IN, GATED, NEEDS_HUMAN}` and `GATED: {DECIDED, QUESTIONNAIRE_OUT}`. |
| D1 | Handbook | 9, 14 | Reference the scope explicitly wherever the P1 park is described. |
| D2 | Handbook | 6.1 | Add rows: `review.rescore` (published by armor pipeline / scorer, consumed by scorer) and `watchdog.sweep` (published by Cloud Scheduler, consumed by watchdog). |
| D3 | Handbook | 5.2 | Add `NEEDS_HUMAN` as a permitted target from `SCORED`, `GATED`, `DECIDED` and `MONITORED`, matching the prose. |
| D4 | Master doc | Appendix B | Either add 5 points to a domain or state the scale as 95. **Recommendation: state 95** and set bands as ≥76 approve / 57–75 conditional / <57 escalate, or normalise to percent for display. Whichever you pick, the binder's section 5 must reconcile. |
| D4 | Handbook | 11.1 | Mirror the same decision in `rubric.yaml` and `band_for()`. |

---

## 3 · Edit index by file

Open each file once; make every edit listed.

### `drawbridge-hackathon-master-doc.md`
- **2.2** — all four webinars answered *(C3)*
- **5.4.3** — Evidence agent becomes three-pass *(C1)*
- **6.1** — name the ADK 2 graph-workflow pattern *(C4)*
- **6.2** — four memory layers, L2.5 inserted *(C1)*
- **6.6** — add embedding model and its cost *(C1)*
- **6.8** — public surface hardening *(C2)*
- **6.9 (new)** — bounded self-improvement *(C3)*
- **7** — add the scale-safely sentence *(C5)*
- **8** — 0:45 shot shows 12 concurrent reviews *(C5)*
- **9** — technologies: ADK 2, Firestore KNN, text-embeddings; hosted-URL wording *(C1, C2, C4)*; findings & learnings gains the metric-gaming line *(C3)*
- **11.2** — Phase 0 gains GEAR and `graph_dump`; Phase 1 gains retrieval; Phase 3 gains hardening *(C1, C2, C4, C5)*
- **12** — new risk #11 public endpoint drain; consider #12 ADK 2 surface change *(C2, C4)*
- **Appendix B** — 95-point reconciliation *(D4)*
- **Appendix D** — retrieval provenance in section 4 *(C1)*

### `drawbridge-implementation-handbook.md`
- **0** — ADK 2 as the surface to verify *(C4)*
- **1.1** — `google-cloud-aiplatform`; ADK 2 pin *(C1, C4)*
- **3.1** — KNN vector index; quarantine lifecycle rule *(C1, C2)*
- **3.2** — `sa-evidence` gains `evidence_chunks` read/write *(C1)* ← **real IAM change**
- **4** — `MODEL_EMBED`, `VECTOR_TOP_K`, `CHUNK_TOKENS` *(C1)*
- **5.1** — `EvidenceChunk`; `Review.gate_scope` *(C1, D1)*
- **5.2** — transition table: D1 and D3
- **6.1** — two missing topics *(D2)*
- **7.2** — `index_chunks()` after the clean-stamp *(C1)*
- **7.3** — `embed_evidence` routing *(C1)*
- **7.5** — ADK 2 Workflow vs `step()` day-1 check *(C4)*
- **7.7** — `question_effectiveness` note type *(C3)*
- **9** — effectiveness-informed selection; scope wording *(C3, D1)*
- **10** — three-pass design; prompt rules for retrieved passages *(C1)*
- **11.1** — rubric scale *(D4)*
- **14** — scope wording *(D1)*
- **16.5 (new)** — public surface *(C2)*
- **17** — seed 10–12; DataDynamo expectation includes the retrieved passage *(C1, C5)*
- **18** — embeddings cost, lifecycle, rate limits, min-instances 0 *(C1, C2)*
- **19** — `test_cross_exam` retrieval assertion *(C1)*
- **20** — retrieval degraded-mode fallback *(C1)*
- **21** — Phase 0: GEAR, `graph_dump`; Phase 1: retrieval, D-fixes; Phase 3: hardening, learning loop *(all)*

### Diagrams — `src/*.mmd`

| Diagram | Edit | Change |
|---|---|---|
| **01 system architecture** | In **Z6**, add `L25["<b>L2.5 · Semantic retrieval</b><br/>Firestore KNN over screened evidence<br/>which passage says this?"]` with `EV --> L25`. In **Z5**, add `EMB["<b>text-embedding-005</b><br/>evidence chunks"]` under the model plane. Relabel **Z4** to `ADK 2 graph workflow · one service-account identity per agent`. Append `· 7-day lifecycle rule` to the `QB` label. In **Z7**, add `PUB["<b>Public read-only surface</b><br/>S0 and one seeded review · cached Firestore reads<br/>no route without a token reaches the model plane"]` with `L2 --> PUB` and **deliberately no edge to Z5** — call that out in the guide text, since a diagram cannot draw an absent edge. | C1, C2, C4 |
| **04 injection defense** | After `CLEAN`, insert `CHUNK["<b>Chunk, embed, index</b><br/>only stamped content is ever indexed"]` between `CLEAN` and `P2`. | C1 |
| **06 memory hierarchy** | Insert an `L25` node between `L2` and `DISTILL`, with its own *Lifetime — the review* / *Answers — which passage says this?* lines. Edge `L2 -- "chunk and embed screened documents" --> L25` and `L25 -- "top-k passages per claim" --> CROSSEX`. Retitle to *four layers, four jobs*. | C1 |
| **07 event backbone** | No change — `review.rescore` and `watchdog.sweep` are already drawn. Confirms D2 is a docs-only fix. | D2 |
| **08 state machine** | No change — already carries `gate_scope` and the `NEEDS_HUMAN` edges. Confirms D1/D3 are docs-only fixes. | D1, D3 |
| **09 permissions** | `G3` (sa-evidence grants) gains `evidence_chunks read/write`. Denials unchanged. | C1 |
| **10 risk scoring** | `F` node: findings now carry *the retrieved passage that supports them*. Add note node `GAME["<b>Why an agent here cannot game its own metric</b><br/>the model judges severity, the code computes the score —<br/>self-improvement never touches the number"]` off `CALC`. Reconcile the domain total with D4. | C1, C3, D4 |
| **11 audit binder** | Section 4 label gains *and retrieval provenance*. | C1 |
| **12 tech stack** | Under *Google Cloud infrastructure → Firestore*: add `KNN vector index`. Under *Models*: add `text-embedding-005 for evidence retrieval`. Under *Agent framework*: `ADK 2 graph workflows`. Under *Engineering discipline*: `Bounded self-improvement — phrasing only, never scoring`. | C1, C3, C4 |
| **13 data model** | New entity `EVIDENCE_CHUNK { string chunk_id PK; string review_id FK; string doc_ref; int page; text text; vector embedding "Firestore KNN index" }` with `SCREENING ||--o{ EVIDENCE_CHUNK : indexes` and `FINDING }o--|| EVIDENCE_CHUNK : "cites"`. Add `gate_scope` to `REVIEW`. Add `question_notes` to `DOSSIER`. | C1, C3, D1 |
| **14 deployment and cost** | Add to the cost band: `PUBSAFE["<b>Public surface</b><br/>statically rendered · no model path<br/>rate-limited · max-instances 2"]` and `LIFECYCLE["<b>Quarantine lifecycle</b><br/>objects deleted after 7 days"]`. | C2 |
| **15 build timeline** | Add a Phase 1 bar *Evidence chunking, embedding and retrieval* (Aug 17–19) and a Phase 3 bar *Public surface hardening* (Aug 26). Add *GEAR sandbox de-risking* to Phase 0. | C1, C2, C5 |
| **16 synthetic vendors** | DataDynamo's *Expected* gains: *the contradiction cites a retrieved chunk from the SOC 2 exception notes.* | C1 |
| **20 failure semantics** | New platform node: *retrieval or embedding unavailable → degraded-mode warning, whole-document fallback; never on the critical path.* | C1 |
| **21 tests and claims** | `test_cross_exam` row: claim becomes *the Evidence agent reconciles against a retrieved passage, and can point at it.* | C1 |
| **22 demo shot map** | 0:45 shot note: *queue shows 12 reviews in flight.* | C5 |
| **new 23** | `docs/diagrams/23-adk2-graph-dump.*` — the structural diagram generated by `graph_dump.py`. Not hand-drawn; commit the tool output and say so in the caption. | C4 |

Diagrams **02, 03, 05, 17, 18, 19** need only wording touches: add a retrieval beat to **03** (`E->>E: retrieve top-k passages per claim from the KNN index`, between the extract and reconcile self-messages), and nothing structural elsewhere.

### `FRONTEND.md` and the wireframe SVGs

| Location | Edit | Change |
|---|---|---|
| `FRONTEND.md` §2, *The cold start* | **Replace wholesale.** Old text recommends min-instances 1. New: *S0 is statically rendered, so a cold start is ~1s; keep min-instances 0 everywhere, per the organisers' cost guidance. Public routes serve cached Firestore reads and never call a model, so traffic cannot drain credits.* | C2 |
| `FRONTEND.md` §9 | Replace the *"Dashboard at min-instances 1 during judging"* bullet with the rate-limit and no-model-path rule. | C2 |
| `FRONTEND.md` §1.1 | Add the no-model-path rule to the S0 description. | C2 |
| `FRONTEND.md` §4, S1b | The expanded timeline entry now shows retrieval provenance alongside model, tokens, cost, latency and span. | C1 |
| `src/s03_04.py` (W3) | In the expanded entry's metadata row, add a sixth cell: `("SOURCE","SOC 2 p.42 §3.2")`; widen the spacing from 162 to 138. | C1 |
| `src/s03_04.py` (W4) | No change — the blocked-payload panel is unaffected by retrieval. | — |
| `src/s01_02.py` (W2) | Queue shows 12 reviews in the *All* chip count, not 8. | C5 |
| `src/wireframes.py` | No change. | — |

---

## 4 · Consistency pass

Run this after applying. Each line is a pair that must agree; if they disagree, one of them is wrong.

- [ ] `.env.example` model names ↔ diagram 12 model leaves ↔ handbook §7.3 ROUTING ↔ master doc §6.6
- [ ] Handbook §3.2 permission matrix ↔ diagram 09 ↔ `tests/test_iam_boundaries.py` ↔ the IAM bindings actually created by `bootstrap.sh`
- [ ] Handbook §6.1 topic table ↔ diagram 07 ↔ the topics `bootstrap.sh` creates
- [ ] Handbook §5.2 `ALLOWED` table ↔ diagram 08 ↔ the transition validator
- [ ] `rubric.yaml` weights and bands ↔ Appendix B ↔ diagram 10 ↔ binder section 5 output
- [ ] Memory tiers: master doc §6.2 ↔ diagram 06 ↔ diagram 01 zone ⑥ ↔ `shared/memory.py` + the retrieval module
- [ ] Firestore collections in diagram 13 ↔ `shared/models.py` Pydantic types
- [ ] Public-route inventory ↔ the no-model-path rule — **grep every public handler for an import of the model router; there should be none**
- [ ] Devpost technologies field ↔ diagram 12 leaves ↔ what is actually imported
- [ ] Every stretch item that did not get built has been **deleted** from diagrams 01 and 12, not greyed out

Two greps worth automating in CI:
```bash
# no model calls on public routes
grep -rn "from shared.models import generate" portal/app/\(public\)/ && echo "VIOLATION"
# every topic in the docs exists in infra
comm -3 <(grep -o 'review\.[a-z_]*\|vendor\.[a-z_]*\|watchdog\.[a-z_]*' docs/handbook.md | sort -u) \
        <(grep -o 'topics create [a-z._]*' infra/bootstrap.sh | awk '{print $3}' | sort -u)
```

---

## 5 · Schedule impact

| Change | Hours | Lands in | Cut if late? |
|---|---|---|---|
| C1 retrieval | 6 | Phase 1 (Aug 17–19) | **No** — it improves the hero finding and reduces Pro spend |
| C2 hardening | 3 | Phase 3 (Aug 26) | **No** — it protects the credits and the hosted URL |
| C3 position | 1 | Phase 4 writing | No — it is prose |
| C3 learning loop | 4 | Phase 3, stretch | **Yes** — cut above the Gemma scrubber |
| C4 ADK 2 vocabulary + graph dump | 1 | Phase 0–1 | No |
| C5 concurrency + GEAR | 2 | Phase 0 and 4 | No — GEAR returns more hours than it costs |
| D1–D4 | 1.5 | Phase 1, before M1 | **No** — each is a runtime bug |

**Revised cut ladder** (§5.6 order, amended): Contract Clause agent → registry versioning demo → **question-effectiveness loop (C3)** → Gemma scrubber → live Watchdog feeds → portal cosmetics.

Note that C1 partially *pays for itself*: retrieving six passages instead of sending a whole SOC 2 to Pro cuts the most expensive call in the system, which protects the <$0.50/review headline.

---

## 6 · What explicitly does not change

- **The idea.** Nothing in the new material contradicts the five-filter analysis in §2.4. The track's own worked example is still the supply-chain orchestrator, which confirms rather than refutes the F5 clone-density reasoning — Drawbridge stays off the examples page.
- **The four demo pillars.** Injection block, kill-and-resume, human gate, audit binder. C1 strengthens the cross-examination beat but adds no pillar. Resist the urge to make retrieval a fifth pillar; it is a mechanism, not a moment.
- **Scoring.** Self-improvement never touches the rubric. This is the position, not a limitation.
- **Auth.** Still none on read paths. C2 hardens the public surface without putting a wall in front of a judge.
- **The permission model.** `sa-evidence` gains one collection; everything else — especially the denials — is untouched.
- **The phase structure and milestones.** M1 Aug 19, M2 Aug 24, freeze Aug 28, buffer Aug 31. Amendment 01 fits inside the existing buffer; if it stops fitting, the cut ladder decides, not the calendar.
