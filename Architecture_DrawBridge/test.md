**NEXUS is a memory operating system for AI agents.** Operational knowledge lives in
CockroachDB as memory that is *born, competes, mutates, merges, is promoted, and dies* —
and the agents that act on it are thin enough to fit on a screen.

The claim we set out to defend is narrow and testable: **retrieval is not context for a
decision — retrieval *is* the decision.**

---

## Inspiration

Every production incident generates knowledge, and almost all of it evaporates. The
postmortem is written, filed, and never read again by the system that would need it. The
next person to see the same failure re-derives the same fix from scratch, six months later,
at 3am.

The obvious response is "give the agent memory." But almost everything shipped under that
name is a **transcript**: text retrieved to condition a generation, where a language model
does the deciding and the database is a filing cabinet. That design has three properties we
did not want:

1. **It cannot be wrong in a measurable way.** If the model's answer is judged by another
   model, there is no number to argue with.
2. **It cannot prove what it knew.** Ask "what evidence did you have at 04:12?" and a
   transcript store cannot answer, because the store has been written to since.
3. **It does not improve.** Adding documents is not learning. Nothing is ever *retired*.

So we inverted it. In NEXUS a telemetry trajectory is embedded and matched against the
trajectories of past incidents, and **the k nearest neighbours' outcomes *are* the
parameters of a Beta posterior.** That posterior decides whether to predict, whether to act,
and which remediation gets the turn. No language model appears anywhere in that path. It
appears in exactly three places, all of them authoring a new playbook genome: **birth,
mutation, merge.**

Once memory is a population of competing strategies with measurable fitness rather than a
pile of documents, the biological framing stops being a metaphor and starts being the
implementation. Playbooks acquire a family tree. Selection has to give newborns a turn or
they die untested. Failure has to breed. Convergent siblings have to merge. Proven doctrine
has to be promoted somewhere every region can read it locally. And a strategy that keeps
losing has to be retired — *after breeding on the way down*, which turns out to be the
entire point of the mechanism.

That is a database problem before it is an AI problem, and it is the reason the whole thing
is built on CockroachDB rather than on a vector store bolted to Postgres. Four capabilities
are load-bearing and only one of them is vector search:

| Capability | What it makes possible |
|---|---|
| Distributed vector indexing | k-NN over trajectories *inside* the transactional store — no consistency gap between the vectors and the rows they describe |
| `AS OF SYSTEM TIME` | Provenance replay for free out of MVCC — no audit table, no snapshot copies, no write amplification |
| Serializable isolation | `SELECT … FOR UPDATE` is a *correct* claim protocol against at-least-once delivery, not an optimistic guess |
| `REGIONAL BY ROW` + `LOCALITY GLOBAL` | Each incident homed where it was observed; promoted doctrine in every region's local read path |

---

## What it does

NEXUS watches a fleet, predicts failures **before** they happen from the shape of the
telemetry leading up to them, applies a remediation drawn from an evolving population of
playbooks, verifies the result, rolls back if it made things worse, and writes what happened
back into the memory that made the next decision better.

```
                        ┌──────────────────────────────┐
                        │        SERVICE FLEET         │
                        │  4 services · 3 regions      │
       ┌───────────────►│  8 failure archetypes        │◄──────────────┐
       │                └──────────────┬───────────────┘               │
       │                               │ 5-min telemetry               │
       │                               ▼                               │
       │            ┌──────────────────────────────────┐               │
       │            │  trajectory_text()               │               │
       │            │  shape, not samples:             │               │
       │            │  trend · decile · peak · form    │               │
       │            └──────────────┬───────────────────┘               │
       │                           ▼                                   │
       │            ┌──────────────────────────────────┐               │
       │            │  Titan Text Embeddings V2        │               │
       │            │  VECTOR(1024) · cosine           │               │
       │            └──────────────┬───────────────────┘               │
       │                           ▼                                   │
       │   ╔═══════════════════════════════════════════════════════╗   │
       │   ║   COCKROACHDB CLOUD · 3 regions · SURVIVE REGION      ║   │
       │   ║                                                       ║   │
       │   ║   SENSORY ──promote──► EPISODIC ──evidence──► k-NN    ║   │
       │   ║   TTL 2h               7-day MVCC            k = 14   ║   │
       │   ╚═══════════════════════╤═══════════════════════════════╝   │
       │                           ▼                                   │
       │            ┌──────────────────────────────────┐               │
       │            │  ORACLE — Beta posterior over    │               │
       │            │  the neighbours' outcomes        │               │
       │            │  silent below 5 matches / 0.60   │               │
       │            └──────────────┬───────────────────┘               │
       │                           │ INSERT predictions                │
       │                           ▼   ── the only thing that          │
       │            ┌──────────────────────────────┐  starts a pipeline│
       │            │  CHANGEFEED → webhook        │                   │
       │            │  RECEIVER λ → EventBridge    │                   │
       │            └──────────────┬───────────────┘                   │
       │                           ▼                                   │
       │   ┌───────────────────────────────────────────────────────┐   │
       │   │        STEP FUNCTIONS · four thin Lambdas             │   │
       │   │                                                       │   │
       │   │  SENTINEL ─► DIAGNOSTICIAN ─► GUARDIAN ─► CHRONICLER  │   │
       │   │  claim +      RCA + promote    act +       evolve      │   │
       │   │  compete      + birth          verify      the memory  │   │
       │   └───────────────────────┬───────────────────────────────┘   │
       │                           │                                   │
       └───────────────────────────┴───────────────────────────────────┘
                    apply · watch · undo          write back
```

### The six things it actually does

**1 · It predicts with a posterior, not a score.**
Confidence is a Beta distribution over the matched neighbours' outcomes, and **both
parameters are stored**, so "3 of 3 neighbours agree" never collapses into the same number
as "30 of 30 agree." The credible interval survives all the way to the UI.

**2 · It can prove what it knew.**
Every prediction records its own commit timestamp *inside* the transaction that wrote it.
The replay pins to that timestamp. The live pane **disagrees** — because Diagnostician later
promoted the very window the prediction was about — and the posterior is unchanged. That
disagreement is the proof: the conclusion did not depend on anything learned afterwards.

**3 · It acts, and it can take the action back.**
The action vocabulary is closed and declarative: 20 actions, validated by pydantic before
anything runs. Every step declares its inverse. Guardian watches the target metric for a
verification window and, on degradation, replays each inverse against the exact step it
undoes.

**4 · It knows when it must ask a human.**
Two of the twenty actions — `rotate_certificate`, `prune_disk` — have no inverse. A playbook
containing either is *not reversible*, and that is a property of the data, not a branch
someone remembered to write. Those never run unattended; they park at an approval gate. And
a human's rejection is not discarded — it becomes a shadow record, scored against whatever
actually happens.

**5 · Its memory evolves — including dying.**
Thompson sampling rather than argmax, so a zero-trial challenger gets a turn. Failure breeds
a variant. Convergent siblings merge into one canonical child. Proven doctrine is promoted
into a `GLOBAL` table. Losers retire.

**6 · It tells you when it does not know.**
"Flat" is reported as `inconclusive`, never as success. An unreachable model produces "no
proposal produced," never an invented playbook. An unreachable fleet produces
`no_substrate`, never a fix that was not run.

### The memory, concretely

Four tiers, four tables, four different lifetimes — and **something in the database, not in
application code, enforces every one of them**:

```
 TIER            TABLE                     LIFETIME              ENFORCED BY
 ─────────────────────────────────────────────────────────────────────────────────
 SENSORY         telemetry_embeddings      2 hours               Row-Level TTL
                                                                 ttl_job_cron '*/5'
                        │
                        │  Diagnostician promotes the window
                        │  and REUSES its embedding — Titan is
                        ▼  never paid twice for the same bytes
 EPISODIC        incidents                 permanent, with a     gc.ttlseconds
                 precursor_snapshots       7-day readable past   = 604800
                        │
                        │  k-NN evidence for every prediction
                        ▼
 PROCEDURAL      playbooks                 90 days of DISUSE     ttl_expiration_
                 REGIONAL BY ROW           (every trial winds    expression
                                            the clock forward)   = 'expires_at'
                        │
                        │  posterior mean ≥ 0.9 over ≥ 10 trials
                        ▼
 INSTITUTIONAL   institutional_playbooks   permanent            promotion only;
                 LOCALITY GLOBAL           read from a local    entry by no
                                           replica everywhere    other path
```

Plus a signal table (`predictions`, whose changefeed drives the entire pipeline), an
append-only `evolution_log`, an `approvals` queue, and a `backtest_runs` table that stores
the honesty numbers rather than recomputing them.

---

## How we built it

### The mathematics

Oracle embeds the live telemetry window and retrieves its \\(k\\) nearest neighbours from
episodic memory under a similarity floor. Let \\(N_k\\) be the retrieved set. Then:

$$
\alpha = \bigl|\{n \in N_k : \text{led to an incident}\}\bigr| + 1
\qquad
\beta  = \bigl|\{n \in N_k : \text{recovered on its own}\}\bigr| + 1
$$

$$
p \sim \mathrm{Beta}(\alpha, \beta),
\qquad
\mathbb{E}[p] = \frac{\alpha}{\alpha + \beta}
$$

with \\(k = 14\\), a cosine-similarity floor of \\(0.72\\), and an emit gate that stays
**silent** unless at least 5 neighbours clear the floor *and* \\(\mathbb{E}[p] \ge 0.60\\).
Both parameters are persisted, so any consumer downstream recomputes the credible interval
rather than trusting a number somebody else already collapsed.

Selection is a **contextual bandit**, not a leaderboard. For each candidate playbook \\(i\\)
with \\(s_i\\) successes, \\(f_i\\) failures and cosine similarity \\(\sigma_i\\) to the
precursor pattern:

$$
\theta_i \sim \mathrm{Beta}(s_i + 1,\; f_i + 1)
\qquad
\text{winner} = \arg\max_i \; \theta_i \cdot \sigma_i
$$

The sampling is the whole point. Argmax over a fitness score is a leaderboard, and a
leaderboard means a newborn playbook is *never selected, never gathers evidence, and dies by
TTL*. Drawing from the posterior lets a zero-trial challenger on a flat prior beat a 0.9
incumbent's draw roughly one time in ten — which is exactly often enough to earn a trial.

Fitness is **never stored**. It is recomputed from `success_count` and `failure_count` at
read time, so there is no cached float that can drift away from the evidence it came from.

When two convergent siblings merge, the canonical child inherits

$$
s_{\text{child}} = \min_j s_j,
\qquad
f_{\text{child}} = \max_j f_j
$$

— the most conservative reading of the evidence that still transfers it. A flat prior would
retire two proven playbooks in favour of an untested one, leaving a hole exactly where the
memory was strongest.

### The decision gate

```
              ┌─────────────────────────────────────────┐
              │  top-8 candidates by cosine (< 0.35)    │
              │  one prefixed vector-index lookup       │
              └────────────────────┬────────────────────┘
                                   ▼
              ┌─────────────────────────────────────────┐
              │  θᵢ ~ Beta(sᵢ+1, fᵢ+1) · score = θᵢ·σᵢ  │
              │  every draw → evolution_log             │
              └────────────────────┬────────────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  posterior mean?     │
                        └──┬────────────────┬──┘
                  < 0.75   │                │   ≥ 0.75
                           ▼                ▼
                  ┌────────────────┐   ┌─────────────────────┐
                  │    SHADOW      │   │  every step has an  │
                  │  record what   │   │  inverse?           │
                  │  would have    │   └──┬───────────────┬──┘
                  │  run · weight  │  yes │               │ no
                  │  0.30          │      ▼               ▼
                  └────────────────┘  ┌────────┐   ┌──────────────┐
                                      │  AUTO  │   │   APPROVE    │
                                      │ act now│   │ ask a human  │
                                      └────────┘   └──────────────┘
```

### The stack

| Layer | Choice | Why |
|---|---|---|
| Memory | **CockroachDB Cloud**, 3 regions, `SURVIVE REGION FAILURE` | The four capabilities in the table above |
| Vectors | `VECTOR(1024)` · `vector_cosine_ops` · **prefixed** vector indexes | 1024 is Titan V2's default, *not* 1536. Prefixing lets one lookup serve the filtered k-NN |
| Compute | **AWS Lambda**, 8 functions, Python 3.12, arm64, one shared layer | Thin agents. No agent holds state |
| Orchestration | **Step Functions** ×2 + **EventBridge** | A second state machine is entered only after a human approves |
| Trigger | **CockroachDB changefeed → webhook → Lambda Function URL** | An `INSERT` is the only thing that starts a pipeline |
| Models | **Bedrock** — Titan V2 for every vector, Claude for genomes | Three places only: birth, mutation, merge |
| Storage / obs | **S3** artifacts, **CloudWatch** dashboard, structured JSON logs | Every log line carries incident / prediction / playbook ids |
| Secrets | **Secrets Manager**, read at cold start | Nothing in code, nothing in git history |
| IaC | **AWS SAM** | 47 resources, one `make deploy` |
| UI | **React 19 · Vite · Tailwind 4 · Recharts · React Flow** | Five views over the same handler the Lambda runs |

### The pipeline, and why it is exactly-once

Changefeed delivery is at-least-once. That is the contract, not a defect to be worked
around, so the claim is a database primitive rather than application logic:

```
 CHANGEFEED ──POST──►┐
 (delivery 1)        │
                     ├──► RECEIVER λ ──► EventBridge ──► 2 Step Functions executions
 CHANGEFEED ──POST──►┘    Bearer auth      nexus-bus         racing for one row
 (delivery 2, retry)

     exec 1 ─► SELECT … WHERE prevention_status='pending' FOR UPDATE  ─► row locked
                                                                      ─► 'preventing'
     exec 2 ─► blocks on the lock, re-reads under SERIALIZABLE
                                                    ─► 0 rows ─► duplicate ignored

     `make pipeline-concurrency` → five deliveries, one claim, four clean no-ops
```

And if an execution dies *after* claiming, the row would sit in `preventing` forever holding
Oracle's dedup guard — making that failure permanently unpredictable, a silent blind spot
worse than the crash. Chronicler's sweep releases it as `missed` after 30 minutes.

### The synthetic world — how a demo becomes an experiment

A demo becomes an experiment the moment part of the world is withheld from it.
`world.build(seed, anchor)` is a pure function: the same seed rebuilds the identical world
down to the last sample.

```
  baseline ──────► precursor drift ──────► failure ──────► recovery
   45 min           60–180 min              20 min          40 min
                         ▲                     ▲
                         │                     └── incidents.symptom_embedding
                         └── precursor_snapshots.trajectory_embedding
                             ── what Oracle matches.
                                The failure is NEVER in it.
```

| | Written to the database | Withheld |
|---|---|---|
| Incidents | 120 | — |
| Precursor snapshots | **155** — 120 that failed, **35 that recovered on their own** | — |
| Playbooks across 4 generations | 30 | — |
| Institutional playbooks | 1 | — |
| `evolution_log` events | 185 | — |
| Held-out windows → `backtest_set.jsonl` | — | **42** |

The 35 negatives are the load-bearing part. Without windows that drifted and then recovered,
the system has never seen a false alarm, and every wobble becomes a prediction.

Remediation is modelled as a **counter-force on the same metric axis**: an effective step
slows the drift, a correct playbook reverses it, a mismatched step accelerates it. That is
why the bad-fix rollback is a *consequence of the simulation* rather than a scripted
animation.

---

## Challenges we ran into

These are the ones that changed the design. Each is written as symptom → cause → what it
taught, because the cause was never the obvious one.

### 1 · A provenance proof that looked exactly like a working one

**Symptom.** The `AS OF SYSTEM TIME` replay worked perfectly: the historical pane and the
live pane matched, every time.

**Cause.** We were replaying at `crdb_internal_mvcc_timestamp` of the prediction row. That
is the row's *latest* version — and Sentinel and Guardian both write to that row after the
decision. We were reading the outcome back as evidence.

**What it taught.** A broken proof of this class is indistinguishable from a working one,
because "the panes agree" is what success is *supposed* to look like. The fix was to capture
`cluster_logical_timestamp()` inside the transaction that writes the prediction. The panes
now **disagree** — a neighbour was promoted afterwards — and that disagreement is the actual
evidence. The wrong timestamp source is called out in a comment in the code, because
avoiding a trap silently means the next person walks into it.

### 2 · `TRUNCATE` silently discarded a zone config

**Symptom.** None. For days. Everything passed.

**Cause.** A manual `TRUNCATE` during development recreated `precursor_snapshots` under a
new table ID — which **discards its zone configuration**. The 7-day `gc.ttlseconds` reverted
to a 75-minute default. Provenance replay kept passing the entire time, because a replay in
a test runs *seconds* after the decision it replays.

**What it taught.** The failure mode of a retention setting is invisible until exactly the
moment you need the retention. Reset now uses `DELETE`, re-asserts the zone configs from the
migration, and `make verify` asserts `gc.ttlseconds = 604800` on both tables as a standing
check.

### 3 · The vector index that was not being used

**Symptom.** Retrieval was correct and quick at demo scale.

**Cause.** Our real queries are *filtered* nearest-neighbour searches
(`WHERE outcome_category = $1 … ORDER BY embedding <=> $2`). Against an unprefixed vector
index the planner cannot combine the two halves: it picks the secondary index on the filter
columns, index-joins, and sorts the survivors. Correct — but a scan.

**What it taught.** "It returns the right answer" and "it will still return the right answer
at a million rows" are different claims. CockroachDB vector indexes accept **prefix
columns**, which partition the index so one lookup serves the whole query; `EXPLAIN` then
shows a `vector search` node with `prefix spans`. `make verify` now asserts that shape —
*and separately asserts recall 1.000 against an exact scan*, because an approximate index
that returns plausible neighbours is indistinguishable from a correct one until you check.

We also left a tradeoff open rather than hiding it: Oracle's neighbourhood query has no
category filter **by design** — the category is the thing it is inferring, so filtering by it
would assume the conclusion — and a prefixed index cannot serve a query with no prefix. That
one query falls back to a scan, and it is in the gaps table.

### 4 · Serialization failures under concurrent incidents

**Symptom.** `make load` — three simultaneous incident ramps — produced `RETRY_SERIALIZABLE`
errors escaping to the caller.

**Cause.** We were holding a serializable transaction open across a Bedrock call. A model
round-trip is hundreds of milliseconds of contention window, for work that touches no rows.

**What it taught.** Serializable isolation does not punish you for being distributed; it
punishes you for holding transactions across things that are not database work. Model calls
moved outside the transaction boundary and the failures went to zero. The reproduction is
still a `make` target.

### 5 · Every merge returned the parent

**Symptom.** The merge rule, which should join two convergent *siblings*, kept selecting a
playbook's own parent.

**Cause.** A mutation is deliberately placed at its parent's position in precursor space —
that is what makes it a variant rather than a stranger. So `ORDER BY distance LIMIT 1`
returns the parent every single time. Without a lineage check, every family collapses into
itself the moment a child wins a trial.

**What it taught.** In a system where similarity is *engineered*, "nearest" and "related"
are not the same relation, and the distinction has to be expressed in SQL. Merge now refuses
relatives via the `lineage[]` array.

### 6 · Three ways for a Lambda to fail to reach the database

Deploying the pipeline surfaced a chain of failures with nothing in common but the error
message being about something else:

- `No module named 'nexus_common'` — SAM's `python3.12` layer builder shipped the package to
  `/opt/python/python/`, because our `ContentUri` already contained `python/`.
- `no pq wrapper available` — the makefile builder used SAM's default **x86_64** image while
  the functions declare **arm64**, so the wheels were `manylinux2014_x86_64`. Fixed by
  pinning `--platform manylinux2014_aarch64 --only-binary=:all:`.
- `root certificate file "~/.postgresql/root.crt" does not exist` — libpq with
  `sslmode=verify-full` and no `sslrootcert` looks for a path that cannot exist in Lambda.
  And `sslrootcert=system` fails *too*, because psycopg's manylinux wheel bundles an OpenSSL
  whose compiled-in CA path is absent from the Lambda filesystem. The cluster presents an
  ordinary Let's Encrypt chain, so the answer was Amazon Linux's own bundle:
  `sslrootcert=/etc/pki/tls/certs/ca-bundle.crt`.

**What it taught.** Serverless build toolchains fail at the *packaging* layer and report at
the *application* layer. We now build the layer explicitly rather than letting the builder
infer.

### 7 · Rotating a secret did nothing

**Symptom.** We wrote a new secret version. Nothing changed. The old value kept working.

**Cause.** `config.get_secret` is `@functools.cache`d and the connection pool is a module
global. A warm execution environment serves the old value until it ages out.

**What it taught.** This is the worst shape a failure can have: it looks like success, then
breaks hours later with no deploy to blame. Rotation is documented as **two** steps — write
the value, then replace every execution environment — with an explicit warning never to
cycle them via `--environment`, which *replaces* the whole variable map instead of merging.

### 8 · The one we did not fix, on purpose

Bedrock model access has not been granted for the account: Titan V2 and Claude both return
`ValidationException: Operation not allowed` with IAM verified correct. Birth, mutation and
merge therefore log and **decline** rather than fabricating a playbook. The lifecycle harness
substitutes exactly one seam and stamps `proposed_by: "lifecycle-harness"` on every row it
writes — never `"bedrock"`.

Faking that path would have been about twenty minutes of work and would have made every
other number in the project untrustworthy.

---

## Accomplishments that we're proud of

**The honesty layer is a feature, not a disclaimer.**
`make backtest` scores Oracle on 42 windows the seeder **deliberately never wrote to the
database**, using Oracle's own retrieval and emit gate. A window it declines to predict on
counts as a negative, because that is what silence means in production.

| Metric | Value |
|---|---|
| Held out | **42 windows** — 30 incidents, 12 negatives |
| Precision · Recall | **0.882** · **1.000** |
| Confusion | TP 30 · FP 4 · FN 0 · TN 8 |
| Category named correctly | 32 of 34 predictions |
| Median warning available | **80 minutes** of precursor pattern before failure |

And the calibration table is on the dashboard, not buried:

| Bucket | n | Stated | Realized | Gap |
|---|---|---|---|---|
| 0.60–0.70 | 6 | 0.667 | 0.500 | **−0.167** |
| 0.70–0.80 | 4 | 0.750 | 1.000 | +0.250 |
| 0.80–0.90 | 4 | 0.828 | 0.750 | −0.078 |
| 0.90–1.00 | 20 | 0.938 | 1.000 | +0.062 |

We say the uncomfortable part out loud: **the model is over-confident in the 0.60–0.70
bucket**, and recall of 1.000 is the *easiest possible case* — held-out incidents are
complete precursor windows, and eight synthetic archetypes are far more separable than real
telemetry. The number worth trusting is precision.

**Every claim has a command.**

| Claim | Command | Evidence |
|---|---|---|
| The vector index really serves the query | `make verify` | `vector search` + `prefix spans`, recall 1.000 vs exact scan · **21/21 live** |
| Predictions are not overfitted | `make backtest` | 0.882 / 1.000 on withheld windows |
| The evidence is replayable | `make verify` | AOST at the decision's own commit timestamp |
| Duplicates cannot double-execute | `make pipeline-concurrency` | one claim, four no-ops |
| A bad fix is undone | `make pipeline-rollback` | fleet degrades → inverses replay → variant bred |
| Memory evolves, including dying | `make lifecycle` | **36 assertions**, all 8 event types |
| The pipeline holds under load | `make load` | three concurrent ramps · **7/7** |
| The cluster survives a region | `make region-config` | survival goal + replica spread, live · **5/5** |
| The whole story runs | `make demo-run` | **24-check** scorecard |
| AWS is deployed, not written | `make deploy` + `make changefeed` | INSERT → changefeed → Step Functions `SUCCEEDED` |

Plus **242 unit tests** that need no database, and CI on every push.

**The genealogy is real.** These three families were read out of the seeded cluster, not
drawn by hand:

```
  connection_pool_exhaustion              memory_leak_oom
  ──────────────────────────              ───────────────
  Static pool bump          gen 1         Blind rolling restart      gen 1
  6/11 → 0.37  RETIRED                    4/9 → 0.33   RETIRED
        │                                       │
        ▼                                       ├──────────────┐
  Pool bump w/ drain        gen 2               ▼              ▼
  14/6 → 0.68                             Drain-then-     Graceful recycle
        │                                 restart  gen 2  w/ headroom  gen 2
        ├──────────────┐                  11/4 → 0.71     9/3 → 0.71
        ▼              ▼                        │
  Adaptive pool   Breaker-first                 ▼
  w/ breaker      pool relief             Pre-emptive headroom scale  gen 3
  gen 3           gen 3                   24/1 → 0.93   ★ INSTITUTIONAL
  17/1 → 0.90     6/4 → 0.58                    promoted to LOCALITY GLOBAL
  one trial from
  promotion                        thread_pool_starvation
        │                          ──────────────────────
        ▼                          Widen thread pool  gen 1 · 7/6 → 0.53
  Predictive pool                        │
  pre-scale       gen 4                  ├────────────────┐
  0/0 → FLAT PRIOR                       ▼                ▼
  never tried — and                Widen and shed   Widen w/ retry
  the sampler will                 gen 2 · MERGED   gen 2 · MERGED
  still give it a turn             10/4             9/5
                                         └────────┬───────┘
                                                  ▼
                                    Canonical starvation relief  gen 3 · 13/2
                                    neither parent deleted — both stay in the tree
```

Read across, that is the entire thesis in data: a founder that failed and was retired but is
still in the tree; a lineage that improved across generations; two convergent siblings
replaced by one canonical child with **both parents preserved**; a genome promoted into
institutional doctrine; and a zero-trial challenger on a flat prior, waiting for the sampler
to give it a turn.

**Exactly-once execution over at-least-once delivery**, proven by delivering one prediction
five times in parallel — not argued for in a design document.

**Honest degradation everywhere.** `no_substrate` instead of a tunnel that would make the
beat "work." "No proposal produced" instead of an invented playbook. `inconclusive` instead
of a flattering win. In every case the honest failure was the better answer, and in every
case it took *more* work than faking it.

---

## What we learned

**Retention policy is a correctness property.** We started treating TTLs and GC windows as
housekeeping. The 75-minute GC window taught us they are load-bearing: a provenance guarantee
is exactly as strong as the MVCC history behind it, and it fails silently, and it fails at
the moment you need it most.

**The most dangerous bug is the one that looks like success.** The provenance replay, the
zone config, the secret rotation — all three *passed*. None of them raised an error. We now
ask a different question in review: not "does this work?" but "**what would this look like if
it were broken?**" If the answer is "the same," the test is not a test.

**Argmax is a policy, and it is usually the wrong one.** The first competition implementation
picked the highest fitness. It worked, and it quietly made the entire evolutionary mechanism
inert: no newborn was ever selected, so no newborn ever gathered evidence, so every newborn
died by TTL. Thompson sampling is three lines of difference and it is the difference between
a population and a leaderboard.

**In an engineered similarity space, "nearest" is not "related."** Placing a mutation at its
parent's position is what makes it a variant — and it is also what makes distance-based
sibling selection return the parent forever. Structure has to be represented explicitly, not
inferred from geometry.

**Serializable isolation is a scalpel, not a tax.** It gave us the `FOR UPDATE` claim
protocol for free — a genuinely correct answer to at-least-once delivery. It only ever cost
us when we held a transaction across work that was not database work.

**Building the plumbing first was the highest-leverage decision.** The changefeed → webhook →
EventBridge → Step Functions spine was built before any agent had real logic in it. Every
later capability was demoable the day it was written, rather than integrated at the end.

**Saying "we did not build that" is cheap; making it cheap is the hard part.** The reason we
could afford honesty about Bedrock is that the degradation paths were designed in from the
start. Honesty is not a virtue you apply at write-up time — it is an architectural property
you pay for early.

---

## What's next for NEXUS —Darwinian memory evolution for AI agents

**Close the two open gaps.** Bedrock model access unblocks birth, mutation and merge on the
production path — the code is written and unit-tested, and one Console grant away. And
`make region-demo` needs its rehearsal: `make region-config` already proves the survival
configuration live at 5/5, but watching a region die mid-transaction needs a cluster whose
plug is reachable.

**Fix the calibration honestly.** The 0.60–0.70 bucket is over-confident. The fix is
reweighting the prior against neighbour similarity — a change worth *measuring* rather than
guessing, which means extending the backtest to compare weighting schemes before shipping
one.

**Restore the unprefixed vector index.** Oracle's uncategorized neighbourhood query currently
falls back to a scan. Invisible at 155 snapshots; not invisible at a million. The cost is a
second vector index maintained on every write, which is a decision that deserves a benchmark.

**Real telemetry.** The synthetic world is deliberately separable — eight archetypes with
distinct metric signatures. The honest next step is Prometheus or CloudWatch ingestion
against a real fleet, where archetypes overlap, labels are wrong, and the emit gate has to
earn its floor.

**Cross-organisation institutional memory.** `institutional_playbooks` is already `LOCALITY
GLOBAL`. The interesting question is whether a promoted playbook can transfer between
*organisations* — an anonymised doctrine exchange where a strategy proven at one company
enters another's population as a challenger with a flat prior, and has to earn its trials
like anything else.

**The MCP Server and Agent Skills.** Both are scope cuts, not rejections. Exposing NEXUS's
memory through the Managed MCP Server would let any MCP client query the genealogy and the
provenance replay directly — which is, in the end, the same argument as the rest of the
project: the memory should be the interface.

---

### Built with

`cockroachdb` · `cockroachdb-cloud` · `ccloud-cli` · `distributed-vector-indexing` ·
`aws-lambda` · `aws-step-functions` · `amazon-eventbridge` · `amazon-bedrock` ·
`amazon-titan-embeddings` · `claude` · `amazon-s3` · `amazon-cloudwatch` ·
`aws-secrets-manager` · `aws-sam` · `python` · `psycopg3` · `pydantic` · `numpy` ·
`fastapi` · `react` · `vite` · `tailwindcss` · `recharts` · `react-flow` · `pytest`
