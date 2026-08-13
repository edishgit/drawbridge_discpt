# Drawbridge — Frontend & UI Flow
### Design system, screen specs, and navigation · Fortified Enterprise Fleet track
*Companion to the implementation handbook (§16 covers the build mechanics; this document owns the design). Mockups live in `mockups/` as standalone SVGs and are referenced by relative path.*

---

## 1. Why the UI is a scored deliverable

Three of the prize surfaces reward the frontend directly: Demo & Production Readiness (30% of the main rubric), Best Multimodal UX ($5k), and the presentation quality that separates a grand-prize project from an honorable mention. The winning AWS project you shared didn't win on novelty alone — it won because the docs site and interface *looked like a product a company already runs*. This document's job is to make Drawbridge read the same way: not a hackathon prototype with a purple gradient, but a security tool a CISO would trust on sight.

**The design thesis:** a vendor-trust product must itself look trustworthy. Trust in interfaces reads as restraint — Linear's discipline, Google for Developers' confident dark surfaces — not decoration. So the whole design spends its boldness in exactly one place (the adversarial-conduct moment, in alarm red) and keeps everything else quiet, dense, and precise.

---

## 2. Design system

![Design system](mockups/07-design-system.svg)

### 2.1 Palette
A near-black canvas with layered dark surfaces, one blue accent for action, and a set of **semantic** state colors that always mean the same thing.

| Token | Hex | Use |
|---|---|---|
| `canvas` | `#0B0D10` | app background |
| `raised` | `#0E1116` | sidebars, panels, nav |
| `card` | `#12171E` | content cards, rows |
| `input` | `#161B22` | fields, secondary buttons |
| `border` | `#22262D` | 1px hairlines |
| `accent` | `#4F7CFF` | primary actions, active state, links |
| `approve` | `#3FB950` | approved / healthy / on-budget |
| `conditional` | `#D29922` | needs-a-human / conditional |
| `escalate` | `#F85149` | rejected / high-severity / **adversarial** |
| `human` | `#A371F7` | human-gate and time-compression markers |
| `warn` | `#F0883E` | contradictions, warnings |
| text | `#E6EAF0` / `#8B97A6` / `#5B6673` / `#3A434F` | primary / secondary / muted / ghost |

The state colors are the load-bearing decision: a red row *always* means escalate, an amber badge *always* means a human is needed. A judge learns the color language in the first ten seconds of the demo and reads the rest of the interface without narration.

### 2.2 Typography
- **Inter** for all UI text — a characterful-but-neutral face that reads as modern-infrastructure rather than marketing.
- **JetBrains Mono** for machine facts only: ids, model names, cost figures, idempotency keys, trace refs. This is a signature move — the moment a number is monospaced, the reader knows it came from the system, not from a designer. It's what makes "$0.42 / review" and "gemini-3.5-flash" feel like live telemetry.
- Scale: Display 28/800, Title 20/700, Body-strong 14/600, Body 13/400, Eyebrow 11/600 with +0.6 letter-spacing. Sentence case everywhere (Linear's rule) — never Title Case Buttons.

### 2.3 Space, radius, motion
8-pt spacing grid; radii 6/8/10/12/16 (rows and inputs small, cards and modals large); 1px borders in `border`. Motion is functional and fast: ≤160ms ease-out on hover and state changes, a single orchestrated reveal on the review timeline, and nothing else. `prefers-reduced-motion` disables all of it. Extra animation is the fastest way to make a serious tool look like a toy — restraint is the point.

### 2.4 Component inventory
Buttons (primary / secondary / destructive), status badges (tier, state, adversarial), score chip, event-timeline node, expandable step card, gate card, stat cell (for the status strip), empty state, skeleton loader, toast. That's the whole kit — resist adding more. Every screen in this document is built from exactly these.

---

## 3. Screen-by-screen specification

### 3.1 Queue — the opening shot
![Queue](mockups/01-dashboard-queue.svg)

The first thing the video shows and the first thing a judge sees, so it must communicate "this is running in production" instantly. Left sidebar carries workspace nav and a **live fleet health list** (each agent with a status dot). The top **status strip** shows active reviews, needs-you count, events today, spend today, and average cost per review — five numbers that tick during the demo and quietly prove the system is real and cheap. The table gives one row per review with a single colored left-edge indicating state, the vendor name with tier/type badges, stage, elapsed *wall-clock* time (reinforcing the weeks-long story), score, and a status pill. Ghost rows (muted) show additional in-flight reviews without competing for attention.

Copy rule: stages are named for what's happening to the review ("Awaiting you," "Monitored"), never for internal state enums.

### 3.2 Review timeline — the core screen
![Review timeline](mockups/02-review-timeline.svg)

Where the demo spends most of its time and where the two money-shots live. Layout: a header with the vendor identity and the persistent **time-compression badge** (purple, always visible when the demo clock is running); a full-width **adversarial-conduct alert banner** when relevant; a left **event timeline** with colored nodes; a bottom **expanded step card** showing the selected step's goal, decision, model, and cost; and a right rail with the **score chip** (big number, band, domain breakdown) and the **risk memo**.

The expandable step card is the single most important UX idea in the product: it turns an OpenTelemetry span into something a human reads, showing GOAL and DECISION in plain English plus the CLAIM-vs-EVIDENCE contradiction inline. This is what makes "you can audit its reasoning" concrete rather than claimed. The three decision buttons (Reject / Conditional / Approve) sit under the memo, and the caption states that the decision writes to the binder with identity and timestamp.

### 3.3 The human gate — the accountability moment
![Approval gate](mockups/03-approval-gate.svg)

A focused modal over a dimmed queue. Eyebrow "GATE G1 · RISK ACCEPTANCE" in the human-purple; the vendor, score chip, and top finding up top; an editable **conditions** checklist (pre-filled from the findings — remediate MFA, provide current ISO cert); the **approver identity** row making explicit that signing records who decided; and three clearly-weighted actions. The caption states the guarantee that matters: the fleet cannot reach "decided" without a signed human token, enforced at the gateway rather than the UI. This screen is the visible half of the security architecture — narrate it as "autonomy that still can't act alone."

### 3.4 Audit binder — the deliverable
![Audit binder](mockups/04-audit-binder.svg)

Split view: a contents nav on the left mirroring the binder sections, a light-surfaced **page preview** on the right (deliberately light — it's a document, and the contrast against the dark app sells that this is an export). The cover shows vendor, dates, outcome, approver, and the **compliance-framework mapping** (SOC 2 CC9.2, ISO A.5.19–5.23, DORA) as chips — the single detail that reframes the artifact from "logs" to "the thing your auditor asks for." The Export PDF button is top-right, and the subhead states it was generated from N reasoning spans in ~2 seconds, which is itself a flex.

### 3.5 Vendor portal — the external surface
![Vendor portal](mockups/05-vendor-portal.svg)

The only screen a light theme is used, because it's a different audience (the vendor) on a different trust footing, and the shift signals "you've left the internal tool." Deliberately minimal: token-scoped header, a progress bar, one question at a time with the evidence-demanding phrasing, an autosaving answer field, and an upload dropzone that notes uploads are scanned before review. Its entire job in the demo is ~15 seconds when NimbusWrite uploads the poisoned PDF — so it's calm and trustworthy, not feature-rich. Copy carries a subtle nudge ("Specific answers move your review faster than 'we follow best practices'") that quietly teaches the behavior the whole product depends on.

### 3.6 Docs site landing
![Docs landing](mockups/08-docs-landing.svg)

Modeled on Google for Developers' dark hero + resource-card pattern, because that's the visual language Google's own judges associate with production credibility. A confident two-line hero built from the tagline, three primary actions (Watch demo / Live demo / GitHub), a hero visual card that *is* the injection money-shot rendered as product, and three resource cards (Getting Started, Architecture, Security) using the `{ curly-brace }` monospace eyebrow the inspiration used. Footer line: "Built for the All Things Agentic Hackathon." The docs site can host on GitHub Pages — only the product must run on Google Cloud.

---

## 4. Navigation flow

![Navigation flow](mockups/06-navigation-flow.svg)

Two surfaces, one highlighted path. **Internal** (authenticated analyst/CISO): Queue → New review → Review timeline → Gate G1 → Audit binder, with a side branch from the timeline into the Incident view. **External** (token-scoped vendor, no login): Questionnaire → Evidence upload → Confirmation. The two surfaces connect through events, not links — a vendor upload publishes to Pub/Sub and surfaces on the internal timeline (the orange dashed cross-surface arrow).

The blue route on the map is deliberately the **exact click-path the demo video follows**, so the flow diagram doubles as the demo storyboard: open a review from the queue, watch the compressed timeline, hit the injection block, kill-and-resume, approve at the gate, export the binder. Building the UI to make that one path flawless matters more than breadth — depth on the demo path beats twelve half-built screens.

---

## 5. Frontend decisions (choice → why → rejected alternative)

| Decision | Choice | Why | Rejected |
|---|---|---|---|
| Framework | Next.js 14 (App Router) + Tailwind on Cloud Run | Fast for a solo builder; SSR for the docs; scale-to-zero; a real hosted URL for judges | Streamlit — faster to write, but reads as a prototype and loses the UX prize |
| Theme | Dark internal tool, light vendor portal + binder | Dark = infrastructure credibility; the light shift signals a trust/audience boundary | All-dark — loses the "this is an external document" cue |
| Accent | Exactly one (blue) + semantic state colors | A learnable color language; restraint reads as trustworthy | Multi-color palette — noisy, toy-like |
| Data type | JetBrains Mono for all machine facts | Makes numbers feel like live telemetry, not design | One font everywhere — loses the "system-generated" signal |
| Realtime | Server-sent events / polling for the timeline + status strip | The ticking status strip is what proves "it's running" on camera | Static refresh — kills the live feel |
| Time in demo | Injected clock + always-on compression badge | Honest acceleration; protects against the one demo-credibility question | Hidden speed-up — dishonest, disqualifying if noticed |
| State mgmt | Server components + minimal client state (no Redux) | Less code for a solo build; fewer bugs under deadline | Heavy client store — over-engineering for 4 screens |
| Charts | Almost none — one score chip, one status strip | A vendor-risk tool is about decisions, not dashboards; avoids the generic-dashboard look | Chart-heavy dashboard — the template answer, and off-thesis |
| Empty/loading | Real empty states + skeletons, never a bare spinner | The frontend-design quality floor; empty screens are invitations to act | Spinners — read as unfinished |
| Component scope | The fixed kit in §2.4, nothing more | Consistency is how judges learn the UI fast; scope control protects the timeline | Ad-hoc components per screen — inconsistent, slow |

---

## 6. Quality floor (non-negotiable, from the design skill)

Responsive down to a laptop at minimum (the demo is recorded at 1080p; don't chase mobile for a B2B internal tool, but never break below 1280px). Visible keyboard focus rings on every interactive element. `prefers-reduced-motion` respected. Real copy everywhere — no lorem, no "Lorem vendor 1." Errors explain what happened and what to do, in the interface's voice, never apologizing and never vague ("Couldn't reach the evidence bucket — retrying, or open the review to continue manually"). Every action keeps its verb through the flow: the button says Approve, the toast says Approved, the binder says Approved.

---

## 7. Build order (maps to the handbook's phases)

- **Phase 1:** Queue + Review timeline in their ugly-but-working form (real data, no polish) — enough that M1's "a stranger could watch it" is true. Design tokens defined in Tailwind config on day one so nothing is restyled later.
- **Phase 2:** the adversarial banner, the gate modal, the status strip going live — the screens the four demo pillars need.
- **Phase 3:** the polish pass (skeletons, empty states, motion, the time-compression badge, spacing audit) and the binder view and docs site. This is the lightest-coding phase deliberately, because polish is where the presentation score is won and it shouldn't compete with core logic for your freshest hours.

Export PNGs of these mockups at 2× for the Medium article and Devpost gallery (Medium rejects SVG); keep the SVGs as source of truth in `mockups/`, where GitHub renders them inline in the frontend README.
