# Drawbridge — Frontend & UI Design
### What we build, what we deliberately don't, and how every screen earns its place in the four minutes
**Owner:** Ambrstack · **Companion to:** `drawbridge-implementation-handbook.md` §16, `DIAGRAM-GUIDE.md`
**Assets:** 10 annotated wireframes (`svg/W*.svg`) · 4 flow diagrams (`svg/F*.svg`, `mmd/F*.mmd`) · regenerate with `python3 src/wireframes.py`

---

## 0 · The one question this document answers

Not *what would a good TPRM product look like* — that question has no end and would consume the whole schedule. The question is:

> **What must a person see on a screen for the four demo pillars, the operational-utility claim, and the reproducibility claim to be believed?**

Everything below follows from that. Where the answer is "nothing", the feature does not get built, however obviously a real product would have it.

### The budget

Handbook §11 gives roughly 170 hours total, of which the frontend can afford **~48 hours** without starving the fleet. That is the constraint that makes this document mostly a list of refusals.

| Surface | Hours | Why it gets that much |
|---|---|---|
| Internal dashboard (S1) | **30** | 3 of the 4 demo pillars happen here, and it is where a judge spends their exploration time |
| Docs site (S4) | 6 | Graded artefact — architecture, security, spin-up |
| Vendor portal (S2) | 5 | ~15 seconds of screen time, but the injection has to enter somewhere |
| Judge entry (S0) | 4 | The hosted URL is a graded item and the first click after the video |
| Inbox simulator (S3) | 3 | Exists to hold exactly one email on camera |

---

## 1 · Surfaces: what we build

![Surface map](svg/F1-surface-map.svg)

**Five surfaces, two deployables.** One Next.js app on Cloud Run serves S0/S1/S2/S3 under different routes; the docs site is separate so it survives a teardown of everything else.

```
/                      S0 · judge entry (public, no auth)
/queue                 S1 · review queue
/review/[id]           S1 · review timeline — the demo screen
/review/[id]/gate      S1 · gate card (G1) — also renders the P1 card
/binders               S1 · binder list and export
/portal/[token]        S2 · vendor portal (token-scoped, no login)
/inbox/[address]       S3 · inbox simulator
docs.<domain>          S4 · docs site (separate deploy)
```

### 1.1 Do we build a landing page? Yes — but not the one you're imagining

The rules require a hosted URL that loads logged-out, and it is the first thing a judge clicks after the video. The failure mode is real and common: the URL opens a dashboard that requires auth, or opens an empty one with no data, and the judge closes the tab having scored only your video.

So S0 is **not** a marketing site. It is a **triage screen with three doors**: watch the demo, explore a completed review read-only, read the architecture. Four hours of work that protects the value of the other 165.

What S0 carries, in order: the one-liner, the injection story in plain language, a live stats strip pulled from real fields (`cost_usd`, `screenings`, resumed-after-crash count), the eight-step pipeline, and the three doors. No pricing, no testimonials, no fake logos, no email capture.

### 1.2 What we deliberately do not build

Each of these is a normal, reasonable product feature. Each one costs days and scores nothing:

- **Auth, accounts, roles, org settings.** The demo has three named humans; hard-code them and put the identity in the approval token where it actually matters. A login screen adds a wall between the judge and the product.
- **Vendor CRUD, contract records, renewal tracking, spend management.** This is the incumbent GRC-suite surface area, and building any of it invites the comparison you cannot win.
- **Charts, analytics, trend dashboards.** A judge has seen a thousand. None of them prove a fleet works.
- **Responsive layouts below 1280px.** Judges watch a video and open a desktop browser. Ship a polite "best viewed on desktop" note under 1024px and move on.
- **Dark mode for the product UI.** The docs site is dark; the product is light. Two themes is two sets of bugs.
- **Any settings page.** Configuration lives in `rubric.yaml`, `bank.yaml` and `.env` — which is also the better engineering story.

---

## 2 · The judge's journey — the only user journey that scores

![Judge journey](svg/F2-judge-journey.svg)

Three failure modes worth engineering against explicitly:

**The auth wall.** Solved by S0 and by read-only public routes for one seeded review. A `?demo=1` seeded state is honest as long as the README says the data is synthetic — which it already must.

**The empty dashboard.** `make seed` runs at deploy, so the hosted URL always has CleanCloud (approved), DataDynamo (gated), NimbusWrite (escalated with the injection) and Northwind Payroll (stalled) in the queue. A judge landing on an empty queue learns nothing.

**The cold start.** Cloud Run at min-instances 0 saves credits and costs you thirty seconds of a judge's eight minutes. Compromise: **min-instances 1 on the dashboard only**, from the day you submit until judging closes, and 0 on everything else. Budget it — it is the cheapest insurance in the project.

---

## 3 · Design system

Deliberately tiny. Everything is Tailwind core utilities so there is no config to fight.

### 3.1 Colour — the same language as the architecture diagrams

This is the highest-leverage design decision in the project: **the UI and the diagrams use one colour system.** A judge who studied diagram 01 already knows what a red banner means when they see it on screen at 1:45.

| Token | Hex | Means | Tailwind |
|---|---|---|---|
| `ink` | `#0f172a` | primary text | `slate-900` |
| `mute` | `#64748b` | secondary text | `slate-500` |
| `faint` | `#94a3b8` | labels, metadata | `slate-400` |
| `line` | `#e2e8f0` | borders | `slate-200` |
| `shell` | `#f8fafc` | page background | `slate-50` |
| `accent` | `#1d4ed8` | agents, in-flight, links | `blue-700` |
| `danger` | `#b91c1c` | untrusted, blocked, stalled | `red-700` |
| `warn` | `#b45309` | screening, contradictions, conditional | `amber-700` |
| `ok` | `#15803d` | verified, durable, approved | `green-700` |
| `human` | `#c2410c` | gates and human action | `orange-700` |
| `violet` | `#6d28d9` | gateway policy, models | `violet-700` |

**One accent, used sparingly.** Blue is the only colour allowed on non-semantic elements. If everything is coloured, the red banner stops meaning anything.

### 3.2 Type

System stack (`Inter` if you want one webfont, nothing more). Six sizes, no others:

| Use | Size | Weight |
|---|---|---|
| Page title | 22px | 700 |
| Screen headline / vendor name | 17–24px | 700 |
| Body | 13.5px | 400 |
| Emphasised body / row title | 13px | 600 |
| Metadata, labels | 11–12px | 500–800 uppercase, tracked |
| Numbers on display (score, counts) | 28–40px | 700 |

**Monospace for anything machine-generated**: idem keys, span ids, log lines, timestamps, the blocked excerpt. This is a small trick with a large effect — mono signals *this is real output, not copy I wrote*.

### 3.3 Layout and rhythm

8px grid. 28px page gutters. 12px card radius, 8px controls. Cards are white on `slate-50` with a 1px `slate-200` border — no shadows except on modals. Two-column layouts run 880 / 476 with a 28px gap.

**Generous whitespace is a scoring behaviour.** Handbook §16 is right that judges rate polish subconsciously; the cheapest way to look considered is to put less on the screen and let it breathe.

### 3.4 States — the part most hackathon UIs skip

- **Loading:** skeleton rows matching the final layout. Never a spinner on a blank page.
- **Empty:** a sentence explaining what will appear here and why it hasn't. "No reviews need you right now — the fleet is carrying four."
- **Streaming:** the fleet status strip counters tick during the demo. Movement reads as *this is running*, which is exactly what a judge is trying to decide.
- **Error:** never a red toast that disappears. Failures become `NeedsHumanCard`s that persist, because in this product a failure is a state, not a notification.

### 3.5 Motion

Three animations, no more. Number transitions on the score (56 → 31 counts down over ~600ms). The adversarial banner slides down over 200ms. New timeline entries fade in. Everything else is instant — animation on a demo screen costs you seconds you do not have.

---

## 4 · The screens

Each wireframe carries its own annotations explaining the design decisions; below is the intent and the build note.

### S0 · Judge entry — `svg/W1-judge-entry.svg`
The hosted URL. Dark hero, three doors, live stats from real fields, the eight-step pipeline strip, and the injection story called out above the fold with a link straight into the evidence. **Build note:** static except the stats strip, which reads a single cached aggregate endpoint. Four hours in Phase 3, not before.

### S1a · Review queue — `svg/W2-queue.svg`
The opening shot of the video. Rows carry state, score, elapsed days and model cost together, so one glance makes three arguments. Default filter is **Needs you**, because the product's claim is that humans appear only at decision points. The fleet activity ticker at the bottom is where a policy-block line appears on camera unprompted. **Build note:** Phase 1 for rows, Phase 2 for the ticker and the status strip.

### S1b · Review timeline — `svg/W3-review-timeline.svg`
The screen the demo lives on. A single vertical event stream, because a review is a story that happened over days. Every entry expands to `goal`, `decision`, `model`, `tokens`, `cost`, `latency`, `span id` — the OpenTelemetry span rendered as prose, and the same data the binder prints. Right rail: Memory Bank dossier, evidence inventory with per-document screening verdicts, findings. **Build note:** collapsed entries Phase 1, expansion Phase 2. The expansion is worth more than any other single component.

### S1c · The injection moment — `svg/W4-injection-moment.svg`
Same screen, mid-attack. The only full-bleed banner in the product. The blocked payload rendered in mono inside a bordered box, labelled *never re-entered into a prompt*. The score panel shows 56 → 31 with the −25 itemised, and an italic line naming Python rather than a model as the thing that computed it. A separate panel states the consequence beyond this review: the flag persists in Memory Bank. **Build note:** Phase 2, and it is the highest-value hour of frontend work in the project.

### S1d · Gate card — `svg/W5-gate-risk-acceptance.svg`
The memo gets the largest panel because a CISO reads it and nothing else. Four fixed sections: recommendation, what drove it, mitigations, what to re-check in 90 days. Beside it, the per-domain arithmetic answering *why 71?* before it is asked. Three decisions mirroring the score bands, with conditional pre-selected because that is what the score says. Under the button: *You are signing as Elena Torres, CISO. This writes a signed, single-use approval token; no code path can set DECIDED without it.* **Build note:** Phase 1 basic, Phase 2 for the breakdown bars.

### S1e · Human gates and stalls — `svg/W6-human-gates.svg`
The P1 card shows the **actual email** before it is sent, not a summary — autonomy that asks permission is a stronger claim than autonomy that doesn't. The `NEEDS_HUMAN` card states what the fleet did *and what it refuses to do*: score on 34% coverage, or infer missing answers. Framing a stall as designed behaviour rather than an error is the difference between reading as mature and reading as broken. The DLQ panel is visible even when empty. **Build note:** Phase 1 for P1, Phase 2 for the stall card and DLQ panel.

### S1f · Audit binder — `svg/W7-audit-binder.svg`
Cover preview on the left doing the arguing — vendor, outcome, named approver, four compliance frameworks. Contents with page counts on the right, because page counts make it a document rather than a screen. Prior binders listed below, so it reads as a register. **Build note:** Phase 3. Pre-warm the service before recording; the export must complete in under three seconds on camera.

### S2 · Vendor portal — `svg/W8-vendor-portal.svg`
One question at a time with a long-form answer and an attachment slot — the evidence-demanding style rule showing up as UI. Uploads display a **processing** state, which is the screening pipeline being honest. **Build note:** Phase 1, five hours, then stop. The red annotation panel in the wireframe is for your readers, not the vendor.

### S3 · Inbox simulator — `svg/W9-inbox-crash-proof.svg`
Leads with the number: **1 message**, in green, before any explanation. Operator view (eight log lines) and vendor view (one email) side by side — that asymmetry is the entire value of idempotency without a paragraph of prose. Header names it a simulated channel, which costs nothing and pre-empts the one question that could undermine the beat. **Build note:** Phase 1 as a list, Phase 2 for the log panel.

### S4 · Docs site — `svg/W10-docs-site.svg`
Dark, five sections, numbered pages grouped by concern, diagrams embedded from the same `.mmd` sources shipped in `docs/diagrams/` with **Expand** and **Copy source**. Every page opens with a one-line summary. The canonical page carries the four-command spin-up. **Build note:** Phase 3, six hours. Use a docs framework, do not hand-roll.

---

## 5 · State-to-UI mapping

![State to UI](svg/F3-state-to-ui.svg)

**One machine state, one visual treatment, no exceptions.** The test: an operator should be able to name the state from the screen alone. This also protects you during the demo — if a review shows a treatment you don't recognise, the state machine is doing something you didn't expect, and you want to know that in rehearsal rather than on camera.

Note that `GATED` renders two different cards depending on `gate_scope` (`contact` → the email approval card; `decision` → the risk-acceptance card). This is the state-machine correction from `DIAGRAM-GUIDE.md` §25 surfacing in the UI: if you don't add the scope, these two very different moments collapse into one indistinguishable state.

---

## 6 · Build order

![Component build order](svg/F4-component-build-order.svg)

**Phase 1 (Aug 14–19) — ugly is fine, working is not optional.** App shell, `StatePill`, `ReviewCard`, `Timeline` + collapsed `TimelineEntry`, `GateCard` v1, vendor portal, inbox list. M1 is *a stranger could watch J1 happen*, which is a UI milestone as much as a backend one.

**Phase 2 (Aug 20–24) — the four pillars must be visible.** `AdversarialBanner`, expanded `TimelineEntry`, `ScoreDelta`, `NeedsHumanCard` + DLQ panel, `FleetStatusStrip`, `ActivityTicker`.

**Phase 3 (Aug 25–27) — polish is a scoring activity.** S0, `BinderView`, `TimeCompressionBadge`, empty states and skeletons, docs site.

**Aug 28 — feature freeze.** No new components. Demo-breaking bug fixes only.

### Component inventory (~18 components total)

```
components/
  shell/        TopBar  NavTabs  FleetStatusStrip  TimeCompressionBadge
  queue/        ReviewCard  StatePill  FilterChips  ActivityTicker
  review/       ReviewHeader  Timeline  TimelineEntry  ScoreDelta
                AdversarialBanner  EvidenceInventory  DossierPanel  FindingsList
  gates/        GateCard  ApprovalCard  NeedsHumanCard  DlqPanel
  binder/       BinderCover  BinderContents  ExportButton
  portal/       QuestionCard  UploadDropzone  ProgressHeader
  primitives/   Pill  Card  Button  SkeletonRow  EmptyState  Bar
```

If a new component is proposed after Aug 24, the answer is no.

---

## 7 · Demo choreography — which screen, at which second

| Time | Screen | What must be on it |
|---|---|---|
| 0:25 | Agent Registry (console) | fleet published, v1.2, capabilities and identity scopes |
| 0:45 | S1a queue → intake | the four seeded reviews, then a new one appearing |
| 1:05 | S1e P1 card | the actual email, the parked state, one tap |
| 1:20 | S1b timeline | **TimeCompressionBadge visible**, days ticking, entries arriving |
| 1:40 | S1b expanded entry | the MFA contradiction with both passages |
| 1:45 | S2 portal → S1c | upload, then the banner, the excerpt, 56 → 31 |
| 2:20 | terminal + S1b | kill on camera, parked state, restart, resume at the exact step |
| 2:40 | S3 inbox | **one message** |
| 2:50 | S1d gate card | memo, breakdown, sign as Elena Torres |
| 3:10 | S1f binder → console | export in under 3s, then Agent Engine, Cloud Run, Pub/Sub, IAM, Trace |

Two production rules from §8 that are really UI rules: **pre-warm every service five minutes before recording** (cold starts are the most likely on-camera failure), and **the time-compression badge must be on screen whenever the factor ≠ 1** — real events, accelerated clock, stated honestly.

---

## 8 · Anti-patterns — the ways a hackathon UI loses points

1. **A chart that proves nothing.** A pie of vendors by tier looks like product screenshots and says nothing about a fleet. Cut it.
2. **A spinner on a blank page.** Reads as broken even when it isn't. Skeletons always.
3. **Toast notifications for failures.** They vanish; a judge misses them. Failures are cards that persist.
4. **A settings page.** Implies configuration you did not build and invites a click that dead-ends.
5. **Fake data that contradicts the demo.** If the queue shows 47 reviews but the video shows four, the judge stops trusting both.
6. **Polishing the vendor portal.** Fifteen seconds of screen time. Every hour there is an hour not spent on the timeline.
7. **Two themes.** The docs site is dark, the product is light, and neither toggles.
8. **Hiding the mechanism.** The idem key, the span id, the policy line and the token sentence are the product. Put them on the screen in mono, not behind a "details" disclosure.
9. **A login screen between the judge and anything.** The single most expensive mistake available.
10. **New components after the freeze.** Every one is a chance to break the path you already recorded.

---

## 9 · Accessibility and performance floor

Not for points — for not losing them when a judge tabs through or a service cold-starts.

- Contrast ≥ 4.5:1 for body text (the palette above passes; verify `faint` on white, which is borderline at 11px — reserve it for uppercase labels only).
- Focus rings visible on every control. Never `outline: none`.
- Semantic HTML: `<button>` for actions, `<a>` for navigation, real headings. Screen-reader labels on icon-only controls.
- Colour is never the sole carrier of meaning — every pill has a word in it.
- Route-level code splitting; the timeline is the only heavy screen.
- Target: S0 interactive in under 2s cold, under 500ms warm. Dashboard at min-instances 1 during judging.
- Test at 1440×900 and 1280×800 — the two most likely judge viewports.

---

## 10 · Regenerating these assets

```bash
python3 src/wireframes.py                     # rebuilds all 10 wireframe SVGs
python3 -c "import cairosvg,glob,os;[cairosvg.svg2png(url=f,write_to='png/'+os.path.basename(f)[:-4]+'.png',scale=1.4) for f in glob.glob('svg/W*.svg')]"
mmdc -i mmd/F1-surface-map.mmd -o png/F1-surface-map.png -c mermaid-config.json -b white -s 2 -w 2000
```

The wireframes are generated from `src/wireframes.py` plus one script per screen group, so a copy change is a one-line edit and a re-run rather than a redraw. Keep them in `docs/design/` in the repo — a judge who finds annotated wireframes alongside the architecture diagrams reads the whole project as designed rather than assembled.
