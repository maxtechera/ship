# Ship Engine — Workflow Specification v3

## Documentation Tree

| Document | Path | Purpose |
|----------|------|---------|
| Workflow Spec (this file) | `skills/ship-engine/WORKFLOW.md` | Canonical pipeline definition — 8 core stages + Stage 9 continuous launch/measure loop, production manifests, tool stack |
| Skill Doc | `skills/ship-engine/SKILL.md` | Skill-level spec — Linear integration, state schema, quality gates, file structure |
| **Critic Agent** | **`skills/ship-critic/SKILL.md`** | **Automated quality gate — PASS/REVISE before every gate + verified state. Invoke the `ship-critic` skill with args. Rubrics: `skills/ship-critic/rubrics/`.** |
| Skill Review | `docs/SHIP-ENGINE-REVIEW.md` | Gap audit: spec vs code, template quality, priority recommendations |
| Canvas UI Spec | `docs/SHIP-ENGINE-CANVAS-SPEC.md` | Canvas component spec — stage nodes, detail panels, board-card model, API contract |
| Canvas Vision | `docs/SHIP-ENGINE-CANVAS-VISION.md` | Pencil-first execution vision — boards, lanes, deliverable previews, AI actions |
| Simulation | `docs/SHIP-ENGINE-SIMULATION.md` | [REDACTED_PROJECT] stage-by-stage stress test — gaps, timing, cost estimates |
| Agentic Map | `docs/SHIP-ENGINE-AGENTIC-MAP.md` | Gen AI automation points per stage — agent roles, prompts, quality gates |
| Holistic Review | `docs/SHIP-ENGINE-HOLISTIC-REVIEW.md` | Cross-document gap analysis, inconsistencies, decisions needed |

> **Reading order for new contributors:** Workflow Spec → Skill Doc → Simulation → Review → Agentic Map

---

## Design Decisions

All major architectural and product decisions for Ship Engine, locked in as of **[REDACTED_PHONE]** after a structured decision interview with Max.

| # | Decision | Choice Made | Rationale |
|---|----------|-------------|-----------|
| 1 | Pipeline scope | **GTM only (no BUILD stage)** | Engine assumes the product already exists. SKILL.md is legacy — it describes a 12-stage pipeline with BUILD/OUTBOUND that was superseded by this spec. |
| 2 | Google Drive integration | **Integrated in v1 — auto-create folders per run** | Every ship run gets a Drive folder automatically. Artifacts land in Drive for easy review and sharing without manual file management. |
| 3 | Approval model | **Approve-by-template — critic agent flags exceptions** | Max reviews and approves prompt templates, not individual output runs. The critic agent surfaces exceptions and anomalies. This scales: once a template is approved, Max isn't in every output loop. |
| 4 | Landing page hosting | **[REDACTED_PROJECT] apps platform (`{product}.{slug}.[REDACTED_PROJECT].app`)** | Landing pages deploy to the [REDACTED_PROJECT] app platform using the product slug as subdomain. No external hosting required for v1. |
| 5 | API wrappers | **Build `mailerlite.py` + `stripe.py` wrappers** | Both wrappers are required for v1 execution. Email group/automation setup (Nurture) and payment flow setup (Closing) depend on these directly. |
| 6 | Prompt templates | **6 templates done, iterate from first run** | The 6 highest-leverage templates (validate-pain-discovery, validate-icp-synthesis, awareness-landing-page, awareness-blog-post, nurture-email-sequence, closing-objection-handler) are built before first run. Remaining templates are created during/after. |
| 7 | Canvas MVP scope | **Pipeline graph + deliverable execution lanes** | Canvas MVP shows the governance pipeline as a flow graph and tracks deliverable cards through lifecycle lanes. The advanced board-card model in CANVAS-VISION.md is deferred to v2. |
| 8 | Products per run | **Single product per run in v1** | One product, one run at a time. Multi-product parallel execution is a future capability once the engine is proven. |
| 9 | Content language | **EN + ES bilingual from day 1** | All content output (landing pages, emails, blog posts, social) is generated in both English and Spanish. Spanish-language market is underserved, aligns with Max's audience and brand. |
| 10 | First real run | **[REDACTED_PROJECT] — Command Center dashboard** | [REDACTED_PROJECT] CC is the first product to run through the engine end-to-end. Mock data already in CANVAS-SPEC uses this product. |
| 11 | Blackboard protocol | **`{stage}.{artifact}` naming + publish events, trust agents** | All shared state keys follow `{stage}.{artifact}` convention. Engine publishes a `blackboard.written` event on every write. No read/write permissions in v1 — trust-by-default keeps infra lean before the engine has run once. |
| 12 | Budget tracking | **Strategy proposes per-stage budgets, Max approves. Warn at 80%, soft-block at 100% with override. Track API/tokens + ad spend.** | Budget visibility before spending is non-negotiable. Strategy has the full picture to produce estimates. Validation Probe spend is pre-authorized up to $30/72h/1 channel to gather demand signal before Strategy; anything beyond is gated by Strategy budget approval. Soft-block (not hard-stop) prevents killing live runs — Max explicitly acknowledges over-budget and decides whether to continue. |
| 13 | Talent tickets | **Linear ticket on same board + Telegram notify Max. AI placeholder continues. Swap deliverable when talent delivers.** | Talent work belongs in Linear with the rest of the run. Pipeline doesn't block — AI placeholder keeps progress moving. Telegram ping for immediate visibility. Swap-in when talent delivers, no stage rerun needed. See [AI Generation Protocol](#ai-generation-protocol) for the full per-deliverable spec. |
| 14 | Stage revisit / rollback | **Incremental revision. Agent-recommended, Max-approved. Preserve originals as v1. Max 2 stages back.** | Keep what works, revise only what needs to change. Preserving originals as v1 enables before/after comparison and revert. 2-stage limit prevents cascading revisits that would effectively restart the run. |
| 15 | Critic agent | **Auto before every gate + before any deliverable can be marked `verified` in production. Separate spawn with full context. `REVISE` blocks gate and blocks the deliverable from going live (Max can override at gates only). Cross-deliverable consistency checks. Implementation: `skills/ship-critic/` (SKILL.md + rubrics/).** | Quality gates only mean something if something is actually checking quality. Separate spawn avoids self-assessment bias. Cross-deliverable consistency is the key value: ICP language in Validate must flow through to landing page copy to email subject lines. Max override prevents infinite REVISE loops while preserving hard-gate integrity. |
| 16 | Content approval queue | **Canvas + Telegram. Batch per-stage. Daily digest for stragglers. Delegation via approval rules (auto-approve categories).** | Dual-surface matches Max's workflow: canvas for monitoring, Telegram for living. Batching per stage eliminates per-item fatigue. Delegation rules provide a gradual path to more automation as template trust builds. |

> Full decision log with options considered: `docs/SHIP-ENGINE-DECISIONS.md`

---

## What Ship Engine Is

Ship Engine takes a working app and gets it to people who need it, want it, and will pay for it. It handles everything after the product exists: validation, positioning, marketing, distribution, monetization, and measurement.

Ship Engine scope:
- Ship Engine defines and executes the internal GTM + marketing strategy system (Hormozi/acquisition.com frameworks).
- It is strategy-first and delivery-first: generate, verify, and ship artifacts by stage.
- The canvas/UI visualizes and approves flow; strategy logic remains in this workflow.

**The engine doesn't just plan. It builds, generates, and ships real artifacts.** Every stage produces deployable pages, published articles, live email sequences, configured payment flows, and generated media assets — not just documents.

**Input:** A web app (at any stage — idea to fully deployed with billing).
**Output:** People know about it, use it, and pay for it. Every asset required to make that happen: live, deployed, and trackable.

### Pencil-First Surface Policy

- Pencil is the default visual workspace for GTM run execution.
- OpenClaw is the system of record for stage state, transitions, and automation outcomes.
- Pencil cards must link to real artifacts (repo paths, deployed URLs, or generated files).

### Run Naming Convention

- Board name: `RUN-<ticket>-<slug>`
- Lane name: `<stage-number>-<stage-name>`
- Card name: `<deliverable-type>-<short-id>`

---

## Orchestrator Contract (Required)

Ship Engine follows the shared orchestrator contract across all engines:
- Linear description + attachments are the **Inputs**
- Each stage produces explicit **Deliverables** (artifacts)
- Each stage defines **Verification**
- Each stage ends with **Artifacts** (links/paths)

Canonical spec: `https://github.com/maxtechera/orchestrator/blob/main/SKILL.md`

Enforcement rules:
- Stage tickets do not move to `In Review` until deliverables exist.
- Stage tickets do not move to `Done` until verification is recorded and artifacts are linked.
- If the artifact isn't linked in Linear, it doesn't exist.

---

## Engine Motor (Linear + Webhooks + Kanban Sweep)

Linear is the system of record. The always-on supervisor (`supervisors/engine/SKILL.md`) keeps runs moving via wake-driven cycles triggered by Linear webhooks and periodic sweeps.

This section describes the current integration surfaces in this repo and the intended execution semantics.

### Linear Model

- One parent run ticket labeled `ship-engine`.
- One stage ticket per stage (Intake, Validate, Gate-V, Strategy, Gate-S, Parallel lanes, Gate-L, Launch, Measure).
- Deliverable cards live inside stage tickets as checklists + artifacts; Stage 9 lifecycle is reflected via blackboard objects and Linear comments.

Linear schema cross-reference:
- Canonical field map and feature usage live in `ship-engine/SKILL.md` under `Linear Issue Structure & Feature Usage (Current Runtime)`.
- Use that section as the source of truth for issue attributes, comment packet fields, linkage keys, and webhook metadata.

### Linear Webhooks (Wake Triggers)

Webhook events should wake the supervisor. On wake, run ONE safe bounded cycle (no infinite loops).

Canonical ingress (official OpenClaw):
- `POST /hooks/wake` on the gateway (Bearer hook token).
- Payload: `{ "text": "...", "mode": "now|next-heartbeat", "agentId": "main", "metadata": { ... } }`.

Repository components (current):
- `openclaw-config/tools/linear-webhook.py`: standalone Linear webhook receiver (HMAC via `Linear-Signature`) that forwards events to gateway `/hooks/wake` with an idempotent `metadata.event_id` envelope.
- `openclaw-config/apps/server.mjs`: can dispatch a wake hook via `sendOpenclawWakeHook()` which calls gateway `/hooks/wake`.
- Observability endpoints live under `/neo/api/webhooks/*` (Command Center), but ingest is gateway-native.

Wake triggers (minimum):
- Ticket created/updated (description, checklist changes)
- Comment added (especially Max decisions)
- Status changed (Blocked/In Review/Done)
- Attachment/artifact added

Event envelope (recommended, idempotent):
- `metadata.event_id`: stable unique id (e.g. `linear:Issue.update:<issueId>:<updatedAt>`)
- `metadata.source`: `linear`
- `metadata.trigger_type`: `webhook` or `cron_sweep`
- `metadata.entity_key`: Linear identifier (`MAX-123`)
- `metadata.occurred_at`: ISO timestamp

On webhook wake:
- Re-read the affected run + stage tickets.
- If a gate decision is present, apply it immediately (advance state / spawn next stage / kill).
- If deliverables were added, run verification + critic checks and advance Stage 9 lifecycle.

#### Decision Parsing Contract (Warn-Only -> Fail-Closed)

Decisions must be machine-parseable to prevent accidental state transitions.

Decision source:
- Only `Comment.create` events on the relevant gate ticket (or run parent) are considered.
- Only Max-author comments (configured allowlist) are considered valid decisions.

Required machine line (single line, anywhere in the comment):
- `decision: approve|revise|hold|kill|ship|explore|proceed|launch|fix`

Precedence:
- Latest valid decision wins by `createdAt` (tie-breaker: `comment_id`).

Enforcement mode:
- `run_mode=iteration`: warn-only (accept common synonyms once, then comment a warning requiring the `decision:` line next time).
- `run_mode=production`: fail-closed (ignore free-text; if no valid `decision:` line, do not transition; comment `BLOCKED` with required format).

Idempotency + dedupe (required):
- Webhooks may retry; cron sweeps may overlap.
- Any wake handler must be safe to run twice (no double-comment spam, no duplicate child tickets).
- Dedupe key is `metadata.event_id` (and/or the Linear comment id) and should be recorded in a local event log (SQLite) before side effects.

Idempotency layers (required):
- `event_id` (wake-level): dedupe identical wake events.
- `intent_key` (action-level): dedupe logical transitions (e.g. `run:MAX-123:state:intake->validating`, `deliverable:<id>:status:verified->draft_scheduled`).
- `effect_key` (side-effect-level): dedupe external writes (e.g. `linear:comment:<ticket>:<hash>`, `linear:create_issue:<run>:<stage>`).

Persistence (normative):
- SQLite DB: `ship-engine/data/ship-engine.db` (WAL mode).
- `wake_events(event_id PRIMARY KEY, entity_key, issue_id, comment_id, source, trigger_type, payload_hash, status, first_seen_at, last_seen_at, attempt_count, next_retry_at, error)`
- `leases(entity_key PRIMARY KEY, holder_id, lease_token, acquired_at, heartbeat_at, expires_at)`
- Retention: keep 30 days; purge daily.

Concurrency control (lease):
- Acquire a short TTL lease on `entity_key` before running the cycle. If lease is held, skip.
- Keep lease TTL short (seconds/minutes), because cycles are bounded.

Lease defaults (normative):
- TTL: 120s
- Heartbeat: 30s
- Acquire is atomic: only succeed if `expires_at <= now`.
- Fencing: include `lease_token` on any writeback; stale tokens must not write.

Failure + retry policy (normative):
- Transient errors (timeouts/429/5xx): retry with backoff + jitter: 30s, 2m, 10m (max 3).
- Terminal errors (auth/schema/invalid decision): no retry.
- After max attempts: mark wake event `failed`, add Linear comment (`status_summary` + `next_steps`) and label `engine-error`.

### Kanban Sweep (Reconciliation)

Sweeps are periodic (cron) and also run on-demand. They fix drift and unstick the system.

Use the existing cron fastpath pattern to avoid expensive work when nothing is actionable:
- Wrapper: `openclaw-config/tools/cron-fastpath.sh`
- Cheap checks: `openclaw-config/tools/cron-fastpath-check.py`
- Pattern: cron script calls `cron_fastpath_should_run "$0" <args>`; exit 20 means skip.

Ship Engine sweep should be implemented as its own cron entrypoint (isolated target) that wakes the supervisor using the same `/hooks/wake` envelope with `trigger_type=cron_sweep`.

Current script locations:
- `openclaw-config/tools/ship-engine-sweep-cron.sh`
- `openclaw-config/tools/fastpath/ship-engine-sweep-cron.sh`

Sweep algorithm:
1. Discover active runs (label `ship-engine`, not `Done`, not `dead`).
2. For each run, identify the current run state and the next actionable ticket(s).
3. Enforce orchestrator contract on each actionable ticket:
   - If Inputs missing: comment with exact missing Inputs and mark `blocked`.
   - If Deliverables missing: create/expand checklist and delegate work.
   - If Verification missing: request/run verification; do not close.
   - If Artifacts not linked: comment with exact missing links.
4. Critic enforcement in `production`:
   - If critic verdict missing: spawn critic before moving deliverables to `verified`.
   - If verdict is `REVISE`: keep ticket open and generate a concrete fix list.
5. Gate prefill:
   - If state is `awaiting-*` or deliverable is `awaiting_max_approval`, ensure a prefilled Decision Packet exists.
6. Stage 9 reconciliation:
   - For each deliverable object, ensure `status_summary`, `next_steps`, `draft_id`, and evidence links are present.
   - Promote / iterate / kill based on evidence; never bypass hard gates.
7. Write back:
   - Update Linear status (`In Progress`/`Blocked`/`In Review`/`Done`) only when orchestrator rules are satisfied.
   - Post a concise status update when a gate is waiting or a stage completes.

Sweep outputs are always traceable: every automatic change must leave a Linear comment explaining `status_summary` + `next_steps`.

### Keepalive (webhook reliability)

If Linear webhook ingress uses a tunnel (Cloudflare/ngrok), reliability requires:
- A keepalive job that restarts the webhook process if dead.
- Re-registration of the Linear webhook URL when the public URL rotates.

In this repo, that pattern exists as `openclaw-config/tools/linear-webhook-keepalive.sh` for the standalone server; gateway-native `/hooks/wake` remains the canonical downstream trigger.

---

## Supervisor Skills (Stage Owners)

Each stage is owned by a supervisor skill. Supervisors do not do all production themselves; they:
- translate Inputs into a concrete Deliverables checklist (Linear)
- delegate execution to flat `content-*` skills and existing tools
- verify artifacts exist and are linked (orchestrator contract)
- write back blackboard keys using `{stage}.{artifact}` naming

Supervisor skills:
- `skills/ship-intake-supervisor/SKILL.md`
- `skills/ship-validate-supervisor/SKILL.md`
- `skills/ship-strategy-supervisor/SKILL.md`
- `skills/ship-awareness-supervisor/SKILL.md`
- `skills/ship-lead-capture-supervisor/SKILL.md`
- `skills/ship-nurture-supervisor/SKILL.md`
- `skills/ship-closing-supervisor/SKILL.md`
- `skills/ship-launch-supervisor/SKILL.md`
- `skills/ship-measure-supervisor/SKILL.md`

Cross-cutting quality agent:
- `skills/ship-critic/SKILL.md` — Critic Agent (auto-fires before every gate and every `verified` transition in production)

Approval gates are owned by the adjacent supervisors:
- Stage 3 (Post-Validation gate) -> `ship-validate-supervisor`
- Stage 6 (Pre-Launch gate) -> `ship-launch-supervisor`

Implementation note:
- The legacy `skills/ship-engine/engine.py` CLI is deprecated. Ship Engine is skills-first and runs via wake-driven supervision.
- Active control loop is `skills/ship-engine-supervisor/SKILL.md` delegating to `skills/ship-*-supervisor/SKILL.md`.

---

## Deliverable Ownership Table (Canonical)

Stage transitions are deliverable-driven: the next stage starts only when the required artifacts exist and are linked in Linear.

| Deliverable | Blackboard key | Primary owner | Primary execution skill(s) | Verification evidence |
|------------|---------------|---------------|----------------------------|----------------------|
| Product brief | `intake.product_brief` | `ship-intake-supervisor` | `content-page`, `content-copy` | Linked doc + key fields present |
| Validation report | `validate.validation_report` | `ship-validate-supervisor` | `content-research`, `content-copy` | Sources/URLs + scoring rubric applied |
| ICP document (VoC bank) | `validate.icp` | `ship-validate-supervisor` | `content-research` | Quotes + channel map + segments |
| Ship plan (GTM playbook) | `strategy.ship_plan` | `ship-strategy-supervisor` | `content-offer`, `content-distribution`, `content-copy` | Channel priorities + offer + budgets |
| B-roll asset library + manifest | `awareness.broll_manifest` | `ship-awareness-supervisor` | `content-broll` | `manifest.json` + screenshots exist |
| Landing page (live preview) | `awareness.landing_page_url` | `ship-awareness-supervisor` | `content-page`, `content-copy` | Live URL + mobile/desktop screenshots |
| Hero/OG/social images | `awareness.image_pack` | `ship-awareness-supervisor` | `content-image` | Crop-safe + thumbnail legible + saved paths |
| Blog post pack | `awareness.blog_pack` | `ship-awareness-supervisor` | `content-blog`, `content-copy` | PR-ready markdown + metadata + internal links |
| Social content pack | `awareness.social_pack` | `ship-awareness-supervisor` | `content-copy`, `content-distribution` | Per-platform formatting + UTMs |
| Offer stack | `lead_capture.offer_stack` | `ship-lead-capture-supervisor` | `content-offer`, `content-copy` | Hormozi value stack + guarantee + CTA |
| Lead magnet artifact | `lead_capture.lead_magnet` | `ship-lead-capture-supervisor` | `content-offer`, `content-page`, `content-form`, `content-image` | Download URL + delivery test |
| Forms + list wiring | `lead_capture.capture_wiring` | `ship-lead-capture-supervisor` | `content-form` | End-to-end signup test logged |
| Nurture sequence (live) | `nurture.email_sequence` | `ship-nurture-supervisor` | `content-copy` | Test email received + links tracked |
| Pricing/checkout (tested) | `closing.checkout` | `ship-closing-supervisor` | `create-app`, `content-copy` | Test purchase/flow evidence |
| Launch playbook | `launch.playbook` | `ship-launch-supervisor` | `content-distribution`, `content-copy` | Checklist + scheduled posts |
| Measure report | `measure.report` | `ship-measure-supervisor` | analytics tools | KPI targets + deltas + next actions |
| Publish evidence bundle (per deliverable) | `stage9.publish_evidence` | Deliverable owner supervisor | lane + launch supervisor policies | `draft_id` (platform draft or publish-ready queue ref) + approval record (if high-risk) + `live_id_or_url` + metrics snapshot + disposition |

Lineage rule for this entire table:
- Every deliverable row above must include prompt + lineage metadata (see Universal Prompt + Lineage Contract).

---

## The Pipeline

```
INTAKE -> VALIDATE -> [Gate-V] -> STRATEGY -> [Gate-S] -+- AWARENESS   -+
                                                         +- LEAD CAPTURE  |
                                                         +- NURTURE       +-> [Gate-L] -> LAUNCH (Scale) -> MEASURE (Synthesis) -> done
                                                         +- CLOSING      -+

                 Stage 9: CONTINUOUS LAUNCH + MEASURE (deliverable-level async loop)
```

Core flow uses 8 governance stages plus Stage 9 as a cross-cutting execution loop.

The execution unit is the deliverable card. Workstreams collaborate to move each deliverable through verification, draft scheduling, approval (when required), live launch, and measurement.

---

## States & Transitions

| State | What's happening | Next state | Transition type |
|-------|-----------------|------------|----------------|
| `intake` | App received, context being gathered | `validating` | Automatic |
| `validating` | Deep demand research + audience intelligence | `awaiting-validation-approval` | Automatic on completion |
| `awaiting-validation-approval` | Validation report + ICP + decision packet delivered, waiting on Max | `strategizing` or `dead` | 🔒 Max decides |
| `strategizing` | Go-to-market plan being defined | `awaiting-strategy-approval` | Automatic on completion |
| `awaiting-strategy-approval` | Strategy lock pack + decision packet delivered (ICP->positioning->offer->channels), waiting on Max | `parallel` or back to `strategizing` or `dead` | 🔒 Max decides |
| `parallel` | 4 agent workstreams producing and verifying deliverables; low-risk deliverables can move through Stage 9 | `awaiting-launch-approval` | Automatic when coordinated scale package is ready |
| `awaiting-launch-approval` | Scale-readiness checklist + decision packet delivered, waiting on Max | `launching` or back to `parallel` | 🔒 Max decides |
| `launching` | Coordinated scale push across approved channels | `measuring` | Automatic when scale wave completes |
| `measuring` | Run-level synthesis and final verdict using Stage 9 evidence | `done` | 🔒 Max confirms final verdict |
| `done` | Archived with lessons and final decision | — | Terminal |
| `paused` | Frozen, no work happening | (returns to previous state) | Max resumes |
| `dead` | Killed with reason | — | Terminal |

**Rules:**
- 🔒 = hard gate, requires Max's explicit decision
- Automatic = triggers as soon as the previous stage's completion criteria are met
- Completion criteria is deliverable-driven (see Deliverable Ownership Table). If deliverables are not linked in Linear, the stage is not complete.
- Stage 9 can progress individual deliverables asynchronously, but it cannot bypass Gate-V, Gate-S, Gate-L, or Final Social Push approval.
- In `production`, a deliverable cannot enter `verified` (or go live) without a critic `PASS` recorded. If critic returns `REVISE`, it stays `in_production`.
- On every gate entry (`awaiting-*`) and on every deliverable entering `awaiting_max_approval`, the agent must prefill a decision packet with recommendation + next steps.
- Any state can transition to `paused` or `dead` at any time via Max's command
- `paused` remembers the previous state and resumes to it

### Deliverable Lifecycle States (Stage 9)

| Deliverable state | What's happening | Next state | Transition type |
|-------------------|------------------|------------|-----------------|
| `requested` | Deliverable card created with Inputs contract | `in_production` | Automatic |
| `in_production` | Agents create the artifact | `verified` | Automatic when checks pass |
| `verified` | Production complete and critic-verified; verification evidence + artifact links recorded | `draft_scheduled` | Automatic |
| `draft_scheduled` | Publish-ready: platform draft scheduled OR queued as a publish-ready package (no calendar required). Delivery disabled until enabled. | `live` or `awaiting_max_approval` | Policy-based |
| `awaiting_max_approval` | High-risk deliverable awaiting explicit approval | `live`, `iterating`, or `killed` | 🔒 Max decides |
| `live` | Deliverable is published/active | `measured` | Automatic |
| `measured` | Metrics snapshot linked to card | `promoted`, `iterating`, or `killed` | Policy + owner decision |
| `promoted` | Deliverable scales to broader distribution | `measured` | Automatic loop |
| `iterating` | Deliverable revised from evidence | `verified` | Automatic |
| `killed` | Deliverable stopped and archived with reason | — | Terminal |

### Run Mode + Hard Gate Integrity

- `run_mode` is required on every run: `production` (default) or `iteration`.
- In `production`, hard gates (`Gate-V`, `Gate-S`, `Gate-L`, final social push gate) cannot be bypassed.
- In `iteration`, continuity simulation is allowed only with a documented exception packet containing: `decision_by`, `reason`, `expires_at`, `rollback_plan`, and `simulated_decision=true`.
- Simulated gate outcomes are learning artifacts only and do not count as production-grade approvals.

### Automation Fastpath Policy

- Before any heavy stage automation, run the fastpath pre-check.
- If no actionable work is detected, skip the full LLM-heavy flow.
- If work exists, execute the full stage flow and sync artifact/status updates.

### Human Validation Pattern (Draft-First, Batch Not Per-Asset)

Use human validation to approve a small `seed_pack`, then automate the batch:
- Validate gate: approve ICP + VoC truth
- Strategy Lock gate: approve offer + channels + angles (prevents waste)
- First-batch creative seed: approve 1 landing hero/OG + 1 thumbnail + 1 carousel cover + `style_seed`
- High-risk deliverables: explicit Max approval before `live`
- Low-risk deliverables: auto-canary allowed after verification

After approval, generate the full asset batch autonomously using the approved `seed_pack`.

### Exception-First Approval Model

Ship Engine is automate-first. Human review focuses on exceptions and strategic decisions, not per-item production.

- Default: agents generate and progress work using approved templates/playbooks.
- Human intervention required for:
  - hard gates (Post-Validation, Post-Strategy Lock, Pre-Launch)
  - final social push package approval before broad social publishing
  - high-risk deliverables before live publishing
  - `high` risk decision packets
  - policy violations or unresolved critic failures
- Seed approvals are batch-level controls (approve representative set, then fan out).

Decision packet field library (flexible, non-strict):
- `status_summary` (one line)
- `delta` (what changed)
- `rationale` (why)
- `risk_level` (`low|medium|high`)
- `confidence`
- `recommended_action` (one of the `allowed_decisions` for this gate/item)
- `recommendation_notes` (why this is recommended)
- `next_steps` (what the engine will do immediately after the decision)
- `downstream_impact`
- `owner`, `due_by`, `evidence_links`
- `queue_priority` (`P0|P1|P2|P3`)
- `kanban_proof_links` (Inputs/Deliverables/Verification/Artifacts)

Supervisors choose the smallest useful subset by stage/risk. No rigid schema is required.

Required minimum for all hard-gate packets (P0 by definition):
- `status_summary`, `risk_level`, `confidence`, `recommended_action`, `next_steps`, `owner`, `due_by`, `queue_priority`, `evidence_links`, `kanban_proof_links`

### Gate Prefill Requirement (Max-Facing)

For any user validation event (hard gates and high-risk deliverables), the agent must pre-fill the decision packet so Max can decide fast:
- Delivery: post the packet as a Linear comment on the relevant ticket and mirror it to Canvas. Notifications (Telegram/Slack) include `status_summary`, `recommended_action`, and the primary link.
- Key artifacts + verification + critic verdict links
- A clear recommendation (`recommended_action`) with short justification
- `next_steps` that will execute immediately after approval
- If `revise` is recommended: an explicit change list (what to fix, who owns it, and what will be re-presented)

### Writeback Schema (Canonical)

AI should support every gate, status, and step by writing small, consistent updates.

- Linear (source of truth):
  - Every meaningful status/step change: add a comment that contains `status_summary` and `next_steps`.
  - Every Max-facing validation (hard gates + high-risk deliverables): post a Decision Packet comment using the template below.
- Blackboard (machine-readable):
  - Deliverable objects follow the State Schema (see AI Generation Protocol) and must include `status_summary`, `next_steps`, and `critic_verdict` in `production`.

#### Decision Packet Template (Linear comment)

```markdown
### Decision Packet — <Gate or Deliverable>
status_summary: <one line>
recommended_action: <one of allowed_decisions>
recommendation_notes: <why>
risk_level: low|medium|high
confidence: 0.xx

allowed_decisions: <pipe-separated>

next_steps:
- <what runs immediately after decision>

Max reply format (required in production):
decision: <one of allowed_decisions>

evidence_links:
- <link>

kanban_proof_links:
- Inputs: <link>
- Deliverables: <link>
- Verification: <link>
- Artifacts: <link>
```

### Review Queue Prioritization

To reduce review fatigue, the system surfaces a prioritized reviewer queue:
- P0: hard-gate decisions and `high` risk items
- P1: cross-stage consistency conflicts (offer/ICP mismatch)
- P2: medium-risk revisions
- P3: low-risk informational updates (can auto-approve by policy)

Only P0/P1 should interrupt flow in real time. Everything else can be batch-reviewed.

### Confidence-to-Action Policy

Use confidence and risk together to reduce arbitrary gate decisions:
- `confidence >= 0.80` and `risk_level in {low,medium}` -> `approve` is allowed.
- `confidence 0.60-0.79` or unresolved critical assumptions -> default `revise` unless Max override is explicitly recorded.
- `confidence < 0.60` with medium/high risk -> default `hold` or `kill`.
- Any override must include `override_by`, `override_reason`, and `expected safeguard` in the decision packet.

---

## Stage 1: INTAKE

Supervisor: `ship-intake-supervisor`

**Purpose:** Receive the app from Max and understand what we're working with.

**How it starts:** Max always initiates. He drops the app — URL, description, voice message, screenshot, whatever format. Could be a raw idea or a fully deployed app with billing. Creating apps is fast now — an idea can go to fully built, deployed, billing-integrated app quickly. The app's readiness level doesn't change the workflow — we always start at Validate regardless.

Minimum viable intake:
- A single product URL is sufficient to start a run.
- Additional assets (screenshots, notes, voice memos, docs, repo links, analytics) are optional at kickoff and improve output quality.

**What happens:**
1. Understand what the app does, who it's for, and what state it's in
2. Look at what exists — visit the URL, assess what's built, what's working, what's missing
3. Structure a lightweight Product Brief:
   - App name and URL (if exists)
   - What it does (one line)
   - Target user (who has the pain)
   - Current state: idea / MVP / fully built / billing integrated
   - Revenue model: free / freemium / paid / subscription / one-time
   - Max's angle: connection to his brand and audience

**Products are web apps only (for now).**

**Completion (Deliverables):**
- Product brief exists and is linked in Linear (Artifacts)
- Blackboard keys set: `intake.product_brief`, `intake.product_url`

Intake upgrade (required for research-first execution):
- Run an explicit intake interview (Q&A) and link it in the Stage 1 ticket
- Produce a research kickoff brief for Validate so research agents can start immediately
- Kick off deep research tasks BEFORE handing off to Stage 2 (Validate)

Blackboard keys (expanded):
- `intake.interview`
- `intake.research_kickoff`

Validation starts automatically — no approval needed. Validation may include a capped Validation Probe (<= $30, <= 72h, 1 channel) which is pre-authorized by policy.

> 📎 **Deep dives:** [Simulation § Intake](../docs/SHIP-ENGINE-SIMULATION.md#stage-1-intake) · [Agentic Map § Intake](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-1-intake) · [Review § Template Quality](../docs/SHIP-ENGINE-REVIEW.md#3-template-quality)

---

## Stage 2: VALIDATE

Supervisor: `ship-validate-supervisor`

**Purpose:** Two equally important goals:
1. **Go/no-go decision** — is there real demand worth pursuing?
2. **Audience intelligence gathering** — who are these people, where do they live, what words do they use, what do they care about? This feeds EVERYTHING downstream.

Validation is the heavy lift. No shortcuts. Depth AND breadth. This stage is critical because it feeds every communication and marketing campaign that follows. The individuals, the audience, the ideal customers, the truth about their pain points — all validated here.

### A. Pain Validation

Find real threads, real complaints, real people — not assumptions. Use the best 2026 practices and trends to validate.

**Sources to mine:**
- **Reddit** — subreddits where target users complain, request, discuss
- **X/Twitter** — complaints, wishes ("I wish there was..."), frustration threads
- **Answer the Public** — actual questions people ask about the problem (real human queries)
- **Google's People Also Ask** — real search queries and related questions
- **AlsoAsked.com** — question trees around the topic
- **Quora** — longer-form pain descriptions and discussions
- **IndieHackers / HackerNews** — builder and user perspectives
- **Product Hunt** — launches in the space, comments, reception
- **G2 / Capterra / App Store reviews** — 1-3 star reviews of alternatives
- **YouTube comments** — complaints under tutorial/review videos in the space
- **Niche forums / Discord servers / Slack groups** — community-specific discussions

**Research tooling:** Mine Reddit, X, HackerNews for pain threads using `tools/research.py --social` (social-focused with query decomposition across all sources simultaneously) or `tools/research.py --x-only` for X/Twitter-specific signals via the xAI/Grok API. Use `web_search` (Brave API) for targeted Reddit/HN threads. For deep competitive and market intelligence, use `tools/research.py --deep` (Perplexity sonar deep research mode). Use `web_fetch` to extract full content from relevant threads, reviews, and competitor pages. Use the `search` skill for dedicated social media signal gathering.

**For each pain point found:**
- Exact quote
- Source URL
- Engagement (upvotes, replies, likes)
- Date (recency matters)

**Categorize** pain points by theme (e.g., "too expensive," "too complex," "missing feature X").
**Rank** by frequency and intensity.

### B. Audience Profiling

- **Who exactly has this pain?** Not "developers" — which developers? What stack? What company size? What job title? What career stage?
- **Where do they hang out?** Specific subreddits, Discord servers, Slack groups, X accounts they follow, newsletters they read, YouTube channels they watch, podcasts they listen to
- **What language do they use?** The exact words and phrases they use to describe their pain. This becomes copy for everything downstream.
- **What have they tried?** Existing solutions, workarounds, DIY approaches. What they like and hate about each.
- **What would make them switch?** Price? Features? UX? Integration? Trust?

### C. Competitor Landscape

- Who else solves this? Direct and indirect competitors
- What do they charge? Pricing model, tiers, free vs paid features
- What are their weaknesses? (from their own users' reviews and complaints)
- What's the gap we can own?
- Traffic estimates, social following, market position

### D. Demand Signals

- Search volume trends (growing/stable/declining) via Google Trends
- CPC for solution keywords (high CPC = commercial intent)
- Competitor traffic estimates
- GitHub stars/issues on related open-source projects
- Social media conversation volume over time
- Answer the Public volume and question types

### E. Max's Angle

- Can Max credibly reach these people through his existing channels?
- Is there a Spanish-language advantage? (less competition, underserved market)
- Content angle: what content can Max create authentically about this problem?
- Brand fit: does this align with what Max is building publicly?

### F. Ideal Customer Profile (ICP)

Synthesize everything above into a clear, standalone ICP document:

- **Demographics:** role, experience level, company size, geography, language
- **Psychographics:** what they value, what frustrates them, what motivates buying decisions
- **Behaviors:** where they spend time online, how they discover tools, how they evaluate and buy
- **Pain triggers:** specific moments when the pain is worst (what situation triggers them to search for a solution)
- **Budget:** what they're currently spending on this problem (money or time)
- **Voice of Customer (VoC):** raw collection of the best quotes, phrases, and expressions the target audience uses to describe their pain. This is the copy bank that ALL downstream stages pull from directly. No need to invent language when the audience already gave it to us.

**The ICP is a standalone document that gets referenced throughout ALL downstream stages.** It's a living document — stages can enrich it with new data as they learn more. It has everything that continues to evolve and traces back across the whole strategy.

### Scoring

| Signal | Weight | How to score |
|--------|--------|-------------|
| Pain frequency | 25% | 1 = no threads found. 3 = monthly threads with moderate engagement. 5 = weekly threads with 100+ upvotes. |
| Willingness to pay | 25% | 1 = no payment evidence. 3 = people use free workarounds reluctantly. 5 = people paying $50+/mo for bad alternatives. |
| Competition gap | 20% | 1 = market saturated with good options. 3 = options exist but UX is poor. 5 = nothing good exists for this niche. |
| Audience fit | 15% | 1 = zero overlap with Max's audience. 3 = adjacent. 5 = Max's audience IS the target user. |
| Market timing | 15% | 1 = declining interest. 3 = stable. 5 = growing trend, new enabling tech, or regulatory tailwind. |

**Weighted score:**
- **≥ 4.0 → SHIP** 🟢 — strong evidence across the board
- **3.0–3.9 → EXPLORE** 🟡 — promising but risks identified. Flag specific concerns and suggest de-risking steps.
- **< 3.0 → KILL** 🔴 — insufficient evidence. Document why and note conditions under which to revisit.

> **Default weights provided.** Agent may propose alternative weights with written justification based on product context (e.g., audience fit weighted higher for personal brand products, willingness to pay weighted higher for pure SaaS). Custom weights are stored in `state["scoring_weights"]` and used by the quality gate.

**The score is important, but the real output is the intelligence package.** Even if we kill the idea, the audience research might reveal a better idea to pursue.

**Outputs:**
- Validation Report (evidence, scoring, recommendation)
- ICP Document (standalone, living document referenced by all downstream stages)
- Validation Probe Pack (optional in mature categories, required on first-cycle runs)

**Completion (Deliverables):**
- Validation report exists and is linked in Linear
- ICP document exists and is linked in Linear
- Probe Pack evidence linked (when required by run policy)
- Blackboard keys set: `validate.validation_report`, `validate.icp`, `validate.score`, `validate.recommendation`, `validate.probe_pack`, `validate.probe_metrics`, `validate.probe_verdict`

### Validation Probe Policy (required for first-cycle runs)

Run a minimal live-signal probe before Gate-V to reduce strategy risk.

Policy (locked):
- Spend cap: `<= $30` total
- Timebox: `<= 72h`
- Channels: exactly `1` channel per probe cycle

Approval: this micro-budget is pre-authorized by policy; no additional Max approval is required. Spend must still be logged and linked.

Required Probe Pack artifacts:
- One demo landing page or waitlist page with clear CTA
- 2-3 ad creatives (or equivalent test assets in the selected channel)
- UTM setup + event tracking proof
- Spend log + metrics snapshot (CTR, CPC/CPL, signup/waitlist conversion)

Probe constraints:
- No pricing/billing launch actions in Validate
- No broad social push beyond the selected probe channel
- All probe assets must be production complete and critic-verified before going live/spending
- If probe exits inconclusive at cap/timebox, emit `revise` packet; do not silently expand scope

Gate-V readiness minimum (first-iteration baseline):
- Validation packet must include at least 3 falsifiable riskiest assumptions with test method + kill condition.
- Evidence mix must include at least 2 independent evidence types (behavioral + qualitative) and at least one disconfirming-evidence section.
- Evidence table must include `quote`, `source_url`, `captured_at`, `source_date`, `engagement`, and `confidence_note`.
- Evidence breadth floor: at least 3 independent source types and at least 2 disconfirming signals, or default `revise`.
- Report `behavioral_evidence_ratio` (`behavioral` vs `opinion` evidence); confidence is capped at `0.79` when behavioral evidence is below 50% unless Max override is explicitly recorded.

> 📎 **Deep dives:** [Simulation § Validate](../docs/SHIP-ENGINE-SIMULATION.md#stage-2-validate) · [Agentic Map § Validate](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-2-validate) · [Review § Scoring Mismatch](../docs/SHIP-ENGINE-REVIEW.md#3-template-quality)

---

## Stage 3: APPROVAL GATE — Post-Validation 🔒

Supervisor: `ship-validate-supervisor`

**Max sees the validation report + ICP and chooses:**

Agent pre-fills the decision packet (see Gate Prefill Requirement) with probe evidence (if required), top risks, recommendation, and next steps.

| Decision | What happens |
|----------|-------------|
| **Ship It** | Advance to Strategy. |
| **Explore** | Validation has gaps. Max specifies concerns. Re-investigate those specific areas, re-present. |
| **Kill** | Not worth pursuing. Archive with reason and lessons. → `dead` |

Decision line for automation parsing (required in production): `decision: ship|explore|kill`

**Completion (Deliverables):**
- Max decision is recorded in the Stage 3 ticket (comment + state update) with links preserved.
- Gate packet includes required minimum hard-gate fields (`owner`, `due_by`, `queue_priority`, `kanban_proof_links`, `evidence_links`).
- For first-cycle runs, gate packet includes Validation Probe links (`validate.probe_pack`, `validate.probe_metrics`, `validate.probe_verdict`).
- If run mode is `iteration` and continuity override is used, attach exception packet (`simulated_decision=true`) and expiry.

**If Max doesn't respond:**
- 24h: reminder ping
- 48h: second ping
- After 48h: auto-pause. No more pings. Wait for Max to re-engage.

---

## Stage 4: STRATEGY

Supervisor: `ship-strategy-supervisor`

**Purpose:** Take the validated intelligence and turn it into the go-to-market playbook. Every decision here gets executed in the parallel stages. The Ship Plan is the single reference document everything pulls from.

### Positioning
- **One-liner:** what is this in one sentence
- **Value proposition:** pain → solution → outcome (using Voice of Customer language from ICP)
- **Competitive positioning:** "Why us over [X]" for each top competitor. Specific — not "we're better," but "they charge $50/mo for Y, we do Z for free." This becomes content: comparison pages, "[competitor] alternative" SEO articles. This is very important for SEO and content strategy.
- **Differentiation:** the specific gap we own (from validation)

### Pricing
- **Competitive pricing research:** What do alternatives charge? What model? What tiers? What's included free vs paid? How do people in this space expect to pay? > Run `tools/research.py --deep "{product category} pricing tiers 2026"` for deep competitive intel, `web_search` for competitor pricing pages, and `browser` tool to navigate and screenshot live competitor pricing pages directly.
- **Audience payment expectations:** What did validation reveal about willingness to pay? What price range feels natural to the ICP?
- **Tier structure:** What's free, what's paid, what triggers upgrade. Name the tiers. How tiers are being done in the similar space.
- **Pricing psychology:** Anchoring, decoy pricing, annual vs monthly discount, founding member / early bird strategy. Everything needs to be taken into account.
- **Launch pricing:** Special offer for early adopters — what, how much, how long, how many
- **Guarantee:** Money-back period, trial length, refund terms

### Channel Strategy
- **All platforms.** IG, X/Twitter, LinkedIn, TikTok, YouTube Shorts, Reddit, newsletters, communities.
- Content gets created once and adapted for each platform's format
- AI generation at the core of content creation
- Full distribution — shotgun the same content on all platforms at the same time
- Then double down on what Measure shows is working

### Content Strategy
- What content pieces are needed across all phases
- Formats per platform: carousels (IG), threads (X), short-form video (TikTok/Reels/Shorts), long-form (YouTube/blog), posts (LinkedIn/Reddit)
- **Competitor comparison content:** "[Product] vs [Competitor]", "[Competitor] alternative", "Best [category] tools" — targeting competitor search traffic. This is part of positioning and leverage.
- SEO keyword targets from validation data
- Content themes mapped to pain points from ICP

### Phased Execution
- Use phased execution with event triggers and lightweight calendar windows for scheduling drafts and review queues.
- Sprint-based: each phase has clear deliverables and "done" criteria
- Phase 1: Parallel prep + first deliverable drafts
- Phase 2: Coordinated scale launch waves
- Phase 3: Synthesis + iteration decisions from continuous measurement
- Dependencies between phases are explicit
- Think in terms of phases, iterations, and what actions need to be done sprint by sprint

### Budget
- Estimated costs: domains, APIs, ad spend, tools
- Breakdown by category
- Max approves before parallel stages spend anything beyond the Validation Probe policy (`<= $30`, `<= 72h`, `1` channel)

### Success Targets
- Targets for post-launch measurement: visitors, signups, activation, revenue
- Defined per phase, not per calendar date
- These are what Measure tracks against

### Go-to-Market Summary
- How all 4 parallel agents connect and collaborate
- Awareness plays
- Lead capture and offer strategy
- Nurture flow design
- Closing approach
- How positioning flows into every touchpoint consistently

### Segment Lock (required before Gate-S)

- Name one `primary_segment` for the next execution cycle.
- Name one `deferred_segment` for later testing.
- Name explicit `excluded_segments` that will not receive fanout assets this cycle.
- Channel and offer decisions must map to `primary_segment` first; anything else is optional and non-blocking.

**Output:** Ship Plan — the single reference document all parallel stages pull from.

**Completion (Deliverables):**
- Ship Plan exists and is linked in Linear
- Parallel workstream tickets have Inputs/Deliverables/Verification/Artifacts sections filled
- Blackboard keys set: `strategy.ship_plan`, `strategy.budget`, `strategy.targets`

### Approval Gate — Post-Strategy Lock 🔒

Purpose: prevent fanning out 100+ assets when the ICP/positioning/offer is not yet trusted.

Max reviews the Strategy Lock Pack (links required):
- ICP + VoC bank (Validate)
- Positioning one-liner + value prop
- Offer stack + pricing hypothesis + guarantee
- Channel priorities + distribution plan
- 3-5 "winning angles" (hooks) to generate the first batch from
- Budget + spend policy (what can spend money, what cannot)
- Segment lock (`primary_segment`, `deferred_segment`, `excluded_segments`)
- Kanban proof block for downstream parallel tickets (Inputs/Deliverables/Verification/Artifacts links)
- 30-day experiment map (`hypothesis -> metric -> success/fail boundary -> decision window -> owner`)

Agent pre-fills the decision packet (see Gate Prefill Requirement) with recommendation, risks, and next steps.

Max chooses:
- **Proceed** -> start Parallel Execution
- **Revise Strategy** -> back to Strategy with specific notes
- **Kill** -> `dead`

Decision line for automation parsing (required in production): `decision: proceed|revise|kill`

Default policy:
- First run for a product: Strategy Lock is mandatory.
- Once templates are trusted for a category: Strategy Lock can be shortened to approving (offer + channels + 1 exemplar pack).

> 📎 **Deep dives:** [Simulation § Strategy](../docs/SHIP-ENGINE-SIMULATION.md#stage-4-strategy) · [Agentic Map § Strategy](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-3-strategy) · [Canvas Spec § Stage Nodes](../docs/SHIP-ENGINE-CANVAS-SPEC.md#3-stage-node-design)

---

## Stage 5: PARALLEL EXECUTION

Supervisors:
- Awareness -> `ship-awareness-supervisor`
- Lead Capture -> `ship-lead-capture-supervisor`
- Nurture -> `ship-nurture-supervisor`
- Closing -> `ship-closing-supervisor`

Four agent workstreams launch simultaneously. Each is owned by a specialized agent. They run independently but collaborate through defined interfaces, all referencing the Ship Plan and ICP.

Execution unit in this stage is the deliverable card, not the lane. Lanes provide domain ownership; cards move asynchronously through Stage 9 lifecycle once verified.

**This is an iterative process — collaborative through all the different modules of the engine. They work together to get this product launched, shipped, and successful. These phases are not one-and-done.**

**Spawn 4 parallel sub-agents** via `sessions_spawn` — one per workstream (Awareness, Lead Capture, Nurture, Closing). Each runs independently with full tool access. Create a Linear ticket per workstream for tracking: `tools/linear.py create "Ship: {product} — {workstream}" --team NEO --state "In Progress"`.

Add a deliverable card per artifact class (`script`, `storyboard`, `thumbnail`, `landing-page`, `offer-stack`, `email-sequence`, etc.) and enforce Inputs/Deliverables/Verification/Artifacts per card.

### Agent Team

| Agent | Owns | Core concern | Funnel position |
|-------|------|-------------|-----------------|
| **Awareness Agent** | Content creation + distribution + community presence | Get the product in front of the right people everywhere | Top of funnel |
| **Lead Capture Agent** | Offer engineering + funnel architecture + conversion optimization | Turn attention into captured leads (Hormozi/acquisition.com style) | Middle of funnel |
| **Nurture Agent** | Email sequences + drip content + relationship building | Move leads from interested to ready-to-buy | Middle-bottom of funnel |
| **Closing Agent** | Payment flow + pricing implementation + post-purchase | Convert warm leads into paying customers + retain them | Bottom of funnel |

### Collaboration Interfaces

The agents are not siloed — they collaborate through defined touchpoints:

| From | To | What gets shared | When |
|------|-----|-----------------|------|
| Awareness → Lead Capture | "Here's what messaging is resonating in communities" | When engagement data comes in |
| Lead Capture → Awareness | "Here's the offer stack — make sure all content points to this" | When offer is finalized |
| Lead Capture → Nurture | "Here's what we promised in the lead magnet, here's the ICP segment" | When capture mechanism is defined |
| Nurture → Closing | "Here's the objection data from email replies, here's where leads drop off" | As sequence runs |
| Closing → Awareness | "Here's testimonials and results for social proof content" | Post-purchase, feeds back to top of funnel |
| Awareness → Nurture | "Here's content pieces that can be repurposed for email drip" | As content is created |

### Talent Tickets

Any agent can create a **talent ticket** when they need a human. Talent tickets are things that require a real person or avatar — on camera, voiceover, or something that really needs a human. Everything else is managed by the agents.

Examples:
- Awareness: "Record this video. Script, storyboard, and AI-generated first pass attached."
- Lead Capture: "Review this offer stack. Approve pricing."
- Nurture: "Record voiceover for this email video."
- Closing: "Approve these guarantee terms."

All talent tickets go to a single queue. Designed to be batchable — "here are 4 videos to record, all pre-production done, block 2 hours and knock them all out."

> The pipeline never blocks waiting for a talent ticket to close. Every deliverable that needs human talent gets an AI-generated version first — shipped and functional. When talent delivers, the human version swaps in, no stage reruns. Full spec: [AI Generation Protocol](#ai-generation-protocol).

---

### 5A. AWARENESS AGENT

**Purpose:** Get the product in front of the right people everywhere. Owns ALL content creation and ALL distribution. Everything that's content — all the copywriting coming out for the product, speaking to the user in landing pages, emails, ads, content creation, blogs — everything gets thrown through the Awareness Agent to make sure it's aligned with the ICP and following the strategy to optimize the lead funnel for the customer. We're solving and using the pain points and everything we know about the ICP all the time.

**Content Creation:**

*Copy & Messaging:*
- Landing page copy: hero section (problem-first, not feature-first), feature descriptions, FAQ, social proof section
- All copy across every touchpoint: landing pages, emails (written here, used by Nurture), ads, blogs, social posts
- Everything uses Voice of Customer language from ICP
- Everything humanized — no AI-sounding text. All copy runs through the `humanize` skill before output: `channel=twitter` for threads, `channel=linkedin` for professional posts, `channel=instagram` for IG captions, `channel=blog` for articles. No exceptions.
- All copy aligned with ICP and Strategy to optimize the lead funnel

*Visual Assets:*
- OG image (1200×630) for link previews
- Social share images adapted per platform
- Product screenshots or mockups
- Logo/icon if needed

*Video Content:*
- Full scripts with hooks — visual hooks, VFX hooks, viral hooks
- Research-backed hook strategies leveraging the research engine and best 2026 viral patterns
- Storyboards with visuals described in detail — not frame by frame, but as much detail as needed (like storyboards, enough for talent to execute)
- **AI-generated first pass:** Complete raw video using AI — avatar, images, visuals, music, mural. The raw storyboard output should be a fully AI-generated video, even using AI avatar, leaving it ready for talent to do the final recording. Use and leverage AI generation as much as possible for the video creation. For voiceover first-pass, use `sag` skill (ElevenLabs TTS via `ELEVENLABS_API_KEY`) to generate narration audio that talent can replace; or use the `tts` tool for quick voice drafts.
- Creates talent ticket: "Record this. Script, storyboard, and AI first-pass attached." Once all pre-production is ready, the talent just does the video recording.

*Content Pieces (created once, adapted for all platforms):*
- Launch announcement
- Product demo / tutorial
- Behind-the-scenes / building story
- Competitor comparison content ("[Product] vs [X]")
- SEO articles targeting pain keywords
- Adapted per platform format: carousels (IG), threads (X), short-form video (TikTok/Reels/Shorts), long-form (YouTube/blog), posts (LinkedIn/Reddit)

**Distribution:**
- Produce a publish-ready pack for all platforms and queue it in `tools/content-engine.py` (commands: `add`, `sync-trending`, `plan-week`, `today`, `script`, `batch-prep`, `posted`) to manage the content pipeline.
- Social publishing is user-enabled: no platform draft/calendar step is required; Max enables actual publishing when ready. If Meta API is configured, publishing can be automated AFTER enablement.
- AI generation at the core of content adaptation per platform
- Content calendar: pre-launch teasers → launch push → post-launch tutorials/results/social proof

**Community Presence:**
- Build presence in mapped communities from validation. Monitor new pain threads with `tools/research.py --social "{pain topic}"` and `tools/research.py --x-only "{pain keywords}"` for X/Twitter signals.
- Engage in pain threads with genuinely helpful replies
- Become a known, trusted voice before and during launch
- The engine starts building all community presence, social network presence, landing page, SEO, reels, stories — everything is handled by the Awareness Agent
- Draft and schedule public-facing engagement by default; route high-risk items to Max approval before `live`. Low-risk items can auto-canary once production is complete and critic-verified.

**SEO:**
- Competitor comparison pages ("[Product] vs [Competitor]", "[Competitor] alternative")
- Pain-keyword articles
- Landing page SEO optimization

---

#### Awareness Agent — Production Pipeline

The Awareness Agent doesn't just plan content — it generates and deploys the actual artifacts. Everything below is produced as a concrete, deployable output, not a document describing what to do.

**B-Roll Auto-Capture (runs first, before any content production):**

Before producing any content, the agent captures all visual assets — screenshots, code snippets, terminal output, UI captures — into an organized asset library. This gives every downstream production step (landing pages, blog posts, social content, video) a rich visual toolkit to pull from instead of scrambling for screenshots mid-production.

> 📎 **Full spec:** [`templates/b-roll-capture.md`](templates/b-roll-capture.md)

Process:
1. **Scan the brief + strategy** for capturable assets — URLs, competitor names, CLI commands, file paths, dashboard references
2. **Auto-detect** what needs capturing using heuristics (URL mentioned → screenshot it, competitor named → screenshot their page, etc.)
3. **Capture assets** using the appropriate tool per type:
   - `browser` → screenshot URLs (full-page for dashboards, viewport for hero sections; desktop 1440px + mobile 375px)
   - `canvas` → render code snippets, architecture diagrams, styled terminal output
   - `exec` → run commands and capture terminal output for rendering
4. **Save to organized directory:** `content-assets/{brief-slug}/broll-{nn}-{description}.png`
5. **Generate asset manifest** (`manifest.json`) — JSON listing all captures with descriptions, dimensions, source URLs, and suggested content formats (blog/reel/carousel/thread)

Quality settings: 1280×720 for video thumbnails, 1200×800 for blog, 1080×1080 for carousel, full-page for dashboards. All PNG.

The manifest enables all production agents to browse available b-roll without filesystem scanning. Every content piece references assets by manifest ID.

**Landing Page Production:**

The landing page is not a wireframe or a copy doc. It's a running page, deployed to a live URL, ready for Max to review and approve.

- AI generates the full landing page (HTML/Next.js) using the `create-app` skill, seeded with: product context, ICP, and direct VoC language from the validated copy bank → deployed live at `{product}.max-techera.[REDACTED_PROJECT].app` (static HTML, no build step)
- Hero section is problem-first: the headline comes from the ICP's most-used pain phrase, not invented copy
- Feature descriptions translate benefits into outcomes using the audience's own words
- FAQ section populated from validation's most common questions
- Social proof skeleton: placeholder sections pre-formatted for testimonials (filled in post-launch)
- All copy passes through the `humanize` skill before the page is assembled — zero AI-sounding sentences
- OG image generated via `content-image` skill (Gemini-first): 1200×630, product mockup style, brand-consistent
- Page deployed to live preview URL — Max reviews a running page, not a doc
- After approval, `browser` tool captures polished screenshots of the deployed product for use as marketing assets — automated navigation to core screens, full-page capture at 1440px desktop and 375px mobile
- Architecture/workflow diagrams generated as Mermaid → polished SVG, embedded in landing page where applicable

**Blog Post Production:**

Reference menu of article types — agent determines count and selection based on SEO opportunity and ICP channel fit:

| Article Type | Purpose | When to use |
|-------------|---------|-------------|
| "The [Pain] Problem Nobody Talks About" | Organic discovery via pain keywords | Almost always — strong SEO play |
| "How to [Solve Problem] Without [Bad Alternative]" | Mid-funnel, drives activation | When ICP searches for solutions |
| "[Product] vs [Top Competitor]: An Honest Comparison" | Competitor traffic + decision-stage SEO | When competitors have search traffic |
| "Step-by-Step: [Core Use Case] in Under 10 Minutes" | Activation + SEO long-tail | When product has clear use cases |
| "Why [Industry] Is Finally Getting Serious About [Problem]" | Brand authority, link bait | When thought leadership fits brand |

Each article is 2000+ words and includes:
- Hero image (AI-generated, branded, 1200×628) via `content-image` skill (Gemini-first)
- 10-15 long-tail keywords woven naturally (sourced from validation data)
- FAQ section with FAQ schema markup embedded
- Full meta tags (title, description, OG tags, Twitter card)
- Internal linking structure (articles link to each other + landing page)
- All copy humanized via the `humanize` skill before output

Output format: PR-ready frontmatter + markdown files, dropped into `awareness/blog-posts/`. Competitor comparison pages are dual-purpose — they function as SEO articles AND as landing page variants for decision-stage visitors.

**Social Content Production:**

Every content piece is automatically adapted for every platform. One piece of source content → full platform pack:

- **IG Carousel (if ICP is active on Instagram):** Branded slides generated via `content-image` skill (Gemini-first) + templating. Slide 1 = hook (the pain, no product mention). Middle slides = insights, steps, or comparisons. Last slide = CTA. Each slide sized 1080×1080. Agent determines slide count based on content depth.
- **X/Twitter Thread:** Hook tweet is problem-first (no product mention in tweet 1). Structured: hook → pain → insight/story → solution → CTA. Agent determines thread length based on content complexity. Optimized for engagement-first algorithm.
- **LinkedIn Post:** Professional long-form angle. 800-1200 words. Opens with a pattern-interrupt observation about the industry. Story arc: problem witnessed → attempt → insight → tool. No hard sell.
- **Reddit Posts:** One version per relevant subreddit, tone-adapted. r/entrepreneur gets a different angle than r/SaaS or the product-specific subs. Value-first framing on every post — the product appears naturally, never as the opening.
- **YouTube Script + Storyboard:** Full video script with spoken word, timestamps, B-roll notes. Shot-by-shot storyboard with visual descriptions detailed enough for talent execution.
- **TikTok/Reels/Shorts Script:** <60 seconds, visual hook in first 3 frames, spoken hook in first 3 words. Pattern: visual hook → spoken hook → fastest possible demo → one CTA. Formatted with scene-by-scene cues.

Social share images auto-sized per platform: 1200×630 (OG/Twitter/LinkedIn), 1080×1080 (IG), 1080×1920 (Stories/Reels cover), 1280×720 (YouTube thumbnail). All generated via `content-image` skill (Gemini-first) with platform-specific crop logic.

**Video Production:**

The AI doesn't just write a script — it produces a complete video first-pass artifact:

- Hooks researched via `tools/research.py --social "{product category} viral hooks 2026"` + `tools/research.py --x-only "viral {problem} reels shorts"` for X/Twitter trending patterns: what visual hooks, VFX hooks, and verbal patterns are performing in this category right now
- Full script written: every spoken word, every pause, every CTA
- Storyboard: scene-by-scene with visual descriptions, B-roll notes, on-screen text, transitions — detailed enough that talent can execute without asking questions
- AI first-pass video generated via AI video gen API: avatar + product screenshots + animated visuals + background music + title cards. This is a complete rough cut, not a storyboard PDF.
- The AI first-pass serves dual purpose: (1) Max can review pacing, messaging, and flow before a human records, and (2) talent can literally re-record over it — audio replacement on an existing cut is faster than recording cold
- Talent ticket created with all three artifacts attached: script + storyboard PDF + AI video file. "Block 30 minutes per video. Everything is pre-built. You're just doing the final human recording."

**SEO Package Production:**

SEO is not an afterthought — it's produced as deployable files with structured data embedded:

- Competitor comparison articles function as both articles AND landing page variants (e.g., `/[product]-vs-[competitor]` route)
- FAQ schema (JSON-LD) generated for every blog post and landing page FAQ section — embedded directly in the HTML `<head>`
- Product schema (JSON-LD) generated for the product landing page — name, description, URL, offers
- Organization schema generated for brand credibility signals
- Sitemap generated or updated with all new URLs
- Meta tags verified across all pages (title length, description length, OG tags, canonical URLs)
- Pain-keyword articles map 1:1 to the pain categories from validation — every validated pain point has a corresponding article targeting it

**Visual Asset Production:**

A complete visual asset pack, produced programmatically:

- **Logo variants:** Light version, dark version, icon/favicon, SVG source — generated via AI image gen with brand brief from Product Brief
- **Product screenshots:** `browser` tool navigates the live product URL, captures the core screens in polished state — real dashboard, not mockups. Use `browser snapshot` to verify UI state before screenshot capture.
- **Architecture/workflow diagrams:** Source written in Mermaid DSL → rendered to polished SVG → embedded in landing page and relevant blog posts
- **Demo GIF:** Browser automation records the core product flow (sign up → first value moment) as a GIF — real product, real flow, auto-looping
- **Social share images:** Per platform, per content piece — hero image for each blog post (AI-generated, branded, shows problem concept or solution)
- **OG images:** One per landing page variant and per blog post — auto-generated batch via `content-image` skill (Gemini-first)

**Done when:** Landing page deployed to live URL, awareness content addresses top ICP pains across selected channels, social content ready for all channels in strategy plan, video first-passes produced and talent tickets created, SEO package targets validated pain keywords, visual asset pack covers all content needs.

> 📎 **Deep dives:** [Simulation § Awareness](../docs/SHIP-ENGINE-SIMULATION.md#stage-5a-awareness-agent) · [Agentic Map § Awareness](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-5a-awareness-agent) · [Canvas Vision § Artboards](../docs/SHIP-ENGINE-CANVAS-VISION.md#concrete-artboard-examples)

---

### 5B. LEAD CAPTURE AGENT

**Purpose:** Turn attention into captured leads. This is offer engineering — Hormozi/acquisition.com style. Not just "put a form on the page" but designing an irresistible reason to give us contact info. If acquisition.com was our lead capture company — that's the level and approach.

**Offer Engineering:**
- **Value stack:** What's the total perceived value? Stack bonuses, features, guarantees to create massive value perception.
- **Lead magnet design:** What free thing do we offer that's so valuable it feels like stealing? Guide, template, tool, free tier, checklist, mini-course, audit. The lead magnet structure is owned here.
- **Risk reversal:** What removes all risk from the prospect? Money-back guarantee, free trial, "keep the bonuses even if you cancel."
- **Irresistible offer construction:** Price anchoring, value-to-price ratio, urgency/scarcity elements that are real (not fake).
- **Offer stacking:** How bonuses, guarantees, and features layer to create an offer that feels like a no-brainer.

Lead Capture reviews and optimizes and makes informed decisions on what are the ways to capture leads. This is the strategic brain of conversion.

**Funnel Architecture:**
- Map every entry point to its capture mechanism:
  - Social platforms → bio link / post CTA → landing page → signup
  - Search → SEO article → in-content CTA → landing page → signup
  - Communities → helpful reply → profile → landing page → signup
  - Email → campaign CTA → landing page → signup/purchase
  - Ads (if budget) → landing page → signup
- Each funnel has its own tracking (UTM parameters)

**Email Capture:**
- Dedicated email list/group for this product
- Signup form on landing page / product
- Lead magnet delivery mechanism

**Analytics & Tracking:**
- UTM links for every channel and content piece
- Conversion events defined: signup, activation, purchase — tracked via GA4 (or equivalent web analytics) and Meta Pixel (`tools/lib/meta_api.py`)
- Analytics collected and normalized via `tools/analytics-collector.py` (GA4, GSC, Meta)
- Funnel visualization via the `brand-report` skill — comprehensive view across all 7 data sources
- Analytics verified and working before launch
- Funnel visualization: where are people dropping off?

**Collaboration with Awareness:** Shares the finalized offer stack so all content points to the same offer. Awareness writes the copy, Lead Capture defines what the copy needs to communicate.

---

#### Lead Capture Agent — Production Pipeline

Lead Capture doesn't define funnels — it builds and deploys them. The output is live infrastructure, not a plan.

**Offer Stack Production:**

The Hormozi framework is applied programmatically to generate the offer stack:

- Value stack copy generated by plugging ICP data into the Hormozi formula: Dream Outcome (what the ICP most wants) × Perceived Likelihood of Achievement (proof, guarantee) ÷ Time Delay (how fast they get it) ÷ Effort & Sacrifice (how little they have to do)
- Each element of the offer stack written as deployable copy: headline, benefit bullets, bonus stack list, guarantee statement
- All copy humanized via the `humanize` skill with `channel=blog` (offer stack) and platform-appropriate channel flag for any social-facing variant
- Pricing page generated as a standalone deployable component — matching the landing page's design system, connected to Stripe (or equivalent payment processor) checkout
- Guarantee badge/section designed and generated: visual badge (AI-generated), copy, and placement spec for the landing page

**Lead Magnet Production:**

Lead magnets are produced as real, downloadable artifacts — not outlines:

- Guides and checklists generated as styled PDFs via the Markdown → PDF pipeline: written by the agent → formatted with brand styles → exported as downloadable file, hosted at a direct URL
- Templates and worksheets generated from product context: what would genuinely help the ICP before they need the product? Produces the actual filled-in template, not a template description
- If the product has a free tier: free tier is configured via API calls to the product backend — the lead magnet IS the product experience, not a PDF

**Funnel Infrastructure Production:**

Every funnel is wired end-to-end before launch:

- Email provider group created via API (MailerLite (or equivalent email automation)): product-specific group, subscriber tags, double opt-in configured
- Signup form created via API: form fields, confirmation message, redirect URL — embedded in landing page and blog posts
- UTM links batch-generated: every channel × every content piece × every CTA gets a unique UTM link. Stored in `lead-capture/funnels/utm-links.csv` with columns: source, medium, campaign, content, full URL
- GA4 (or equivalent web analytics) conversion events configured programmatically via Measurement Protocol or GTM: `signup`, `lead_magnet_download`, `checkout_start`, `purchase` events defined with correct parameters
- Conversion tracking verified via `browser` tool end-to-end test: automated session visits the landing page via a UTM link, fills the form, verifies the analytics event fires, checks the email group has the new subscriber. Pass/fail logged in `lead-capture/analytics/tracking-test-log.md` before launch approval.
- Landing page capture forms confirmed wired to the correct email group — form submit triggers list add, triggers welcome sequence

**Analytics Setup Production:**

Not just "set up GA4 (or equivalent web analytics)" — configured to track the actual funnel:

- Analytics property configured with custom event schema: events match the funnel stages defined in the Ship Plan
- Funnel stages defined as conversion goals in analytics: Visitor → Lead → Activated → Paying
- UTM parameter handler verified: all UTM parameters captured in analytics session source/medium dimensions
- Real-time dashboard or report template configured — shows live funnel performance at a glance, not buried in raw analytics reports

**Done when:** Offer stack finalized and deployed, lead magnets live and downloadable, email capture mechanism wired and tested, UTM links generated for all active channels, analytics events verified end-to-end, all funnels operational.

> 📎 **Deep dives:** [Simulation § Lead Capture](../docs/SHIP-ENGINE-SIMULATION.md#stage-5b-lead-capture-agent) · [Agentic Map § Lead Capture](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-5b-lead-capture-agent)

---

### 5C. NURTURE AGENT

**Purpose:** Move captured leads from "just signed up" to "ready to buy" through a structured sequence. Bridge the gap between interest and purchase.

**Email Welcome Sequence (5-7 emails over 14 days):**

> *Example sequence for a consumer SaaS product with a 14-day sales cycle. Agent adjusts email count, timing, and content based on product type, ICP, and sales cycle complexity. Simple products may need 3-5 emails; enterprise considered purchases may need 10-15.*

| Timing | Email | Purpose |
|--------|-------|---------|
| Day 0 | Welcome | Deliver promised value (lead magnet), set expectations |
| Day 1 | Origin Story | Why this exists, the pain that inspired it, build personal connection |
| Day 3 | Tutorial | Show how to get maximum value, drive activation |
| Day 5 | Social Proof | What others are experiencing, testimonials, results |
| Day 7 | Objection Killer | Address the #1 reason people don't buy (from ICP data) |
| Day 10 | Urgency | Early bird ending, limited spots, price increasing — whatever's real |
| Day 14 | Last Call | Final push. Clear CTA. After this, move to regular newsletter cadence. |

Each email: subject line, body copy, CTA. Copy written by Awareness Agent using Voice of Customer language. Nurture Agent defines the sequence logic, timing, triggers, and conditions.

**Content Drip:**
- What to post between launch and D+14 to keep momentum
- Repurpose content from Awareness Agent for email-specific formats
- Maintains awareness while email sequence does the heavy nurturing

**Retargeting (if ad budget exists):**
- Landing page visitors who didn't sign up → reminder ad
- Signed up but inactive → activation prompt
- Define audiences and creative direction

**Collaboration with Lead Capture:** Receives captured lead data and lead magnet context (what was promised). Nurture must deliver on that promise immediately in email 1.

**Collaboration with Closing:** Shares objection data and drop-off points from the sequence so Closing can address them in the purchase flow.

---

#### Nurture Agent — Production Pipeline

Nurture doesn't draft emails — it builds and imports live automation sequences. The sequence is running before launch day.

**Email Sequence Production:**

All emails in the sequence generated as complete, deployable artifacts:

- Subject lines: 3 A/B variant options per email (different angles — curiosity vs benefit vs urgency). The agent picks the strongest, presents alternatives for Max's override.
- Body copy: full email body, written in Max's voice, using VoC language from the ICP. Personalization tokens included (`{{ first_name }}`, `{{ product_name }}`).
- All copy humanized via the `humanize` skill with `channel=blog` — no AI cadence, no "I hope this email finds you well"
- CTAs: primary CTA per email is consistent with funnel stage (Day 0-3 = activate, Day 5-10 = convert, Day 14 = last call)
- Email HTML templates generated: brand-consistent, mobile-responsive HTML, tested in major email clients
- Sequence imported into the email provider as a live automation via API: each email added as a step, delays configured, triggers set
- Trigger configured: automation fires when a subscriber joins the lead capture group created by Lead Capture Agent
- Test email sent to a seed address to verify: delivery, rendering on mobile, link tracking, unsubscribe footer — pass/fail logged before launch approval

**Content Drip Production:**

14 days of social posts produced as ready-to-publish content:

- Posts written for all platforms: per-platform tone and format, sourced from Awareness Agent's content bank. All copy humanized via the `humanize` skill with `channel={platform}` before output.
- Hero images generated for each post via `content-image` skill (Gemini-first)
- Posts formatted as a structured schedule: `content-drip/schedule.csv` with columns: day, platform, copy, image path, status
- Content pipeline managed via `tools/content-engine.py` — use `sync-trending`/`add` to queue posts, `plan-week` for calendar view, `today` for daily queue, `posted` to mark published
- Publishing is user-enabled: queue publish-ready assets; Max enables actual publishing. If Meta API is configured, publishing can be automated AFTER enablement.
- Schedule publishing cadence via `cron` tool — daily posts for first 14 days, weekly cadence thereafter

**Retargeting Definitions:**

- Custom audience definitions written for Meta Ads Manager: pixel events, lookalike seed conditions, exclusion lists
- Ad copy directions written per retargeting segment (non-signups vs signups who didn't activate)
- Handed to Max for activation if ad budget was approved in Strategy

**Done when:** Nurture sequence covers full buyer journey from awareness to decision, humanized and imported into email provider as live automation. Trigger configured and test email verified. Content drip pack ready for post-launch momentum.

> 📎 **Deep dives:** [Simulation § Nurture](../docs/SHIP-ENGINE-SIMULATION.md#stage-5c-nurture-agent) · [Agentic Map § Nurture](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-5c-nurture-agent) · [Canvas Vision § Email Artboard](../docs/SHIP-ENGINE-CANVAS-VISION.md#-email-artboard)

---

### 5D. CLOSING AGENT

**Purpose:** Convert warm leads into paying customers. Remove every friction point between "I want this" and "I paid for this." Own the post-purchase experience.

**Pricing Implementation:**
- Final pricing tiers (from Strategy's pricing research)
- Launch pricing specifics: discount amount, duration, limit
- Guarantee terms finalized
- Pricing page structure and copy direction (Awareness writes the copy)

**Payment Flow:**
- Checkout experience: what the user sees, clicks, and receives
- Receipt and confirmation flow
- Access provisioning: how does a paying user get access immediately?
- Refund process if guarantee is triggered

**Conversion Triggers:**
- What prompts a free user to upgrade? (usage limit, feature gate, time limit)
- What creates urgency? (countdown, limited spots, price increase)
- Where do these triggers appear? (in-product, email, landing page)

**Objection Handling:**
- Top 3-5 objections from ICP data and competitor reviews
- Response for each: where it appears (FAQ, pricing page, email) and what it says
- ROI framing: "this problem costs you X hours/dollars → solution costs Y"

**Post-Purchase Flow:**
- Immediate: onboarding (get to first value in <5 minutes)
- Day 3: check-in ("how's it going?")
- Day 7: ask for testimonial or review
- Day 14: referral prompt or upsell (if tiers exist)
- Day 30: retention check

**Collaboration with Awareness:** Sends back testimonials and results for social proof content — feeds back into top of funnel.

---

#### Closing Agent — Production Pipeline

Closing doesn't describe a checkout flow — it builds one. Stripe (or equivalent payment processor) is configured, the pricing page is deployed, and the post-purchase sequence is live before launch day.

**Payment Setup Production:**

Full payment infrastructure provisioned via Stripe (or equivalent payment processor) API before a single visitor arrives:

- Products created via Stripe API: one product per tier defined in the Ship Plan, with full name and description
- Prices created via Stripe API: monthly and annual price objects for each tier, with correct currency and billing interval
- Checkout session URLs generated and tested: each tier has a working checkout URL that routes to the correct Stripe checkout page
- Webhook endpoint scaffold deployed: `/api/stripe-webhook` endpoint created and registered in Stripe dashboard, handles `checkout.session.completed` and `customer.subscription.updated` events
- Coupon codes created via Stripe API: founding team discount (e.g., 40% off for life for first 50), early bird discount (time-limited), with usage limits and expiry dates set programmatically
- Stripe Customer Portal configured: subscribers can manage their own billing, upgrade, downgrade, cancel — self-service, zero manual intervention required

**Pricing Page Production:**

Not a copy doc — a deployed, functional pricing page:

- Full pricing comparison table generated as a deployable component via `create-app` skill, integrated into the Awareness Agent's landing page or as a standalone `/pricing` route at `{product}-pricing.max-techera.[REDACTED_PROJECT].app`
- Monthly/annual toggle: JavaScript toggle built in, price values swap dynamically, annual savings highlighted
- Stripe checkout integration wired: each "Get Started" button links to the correct Stripe checkout session URL for that tier
- Integration tested end-to-end via `browser` tool: agent navigates to pricing page → clicks a tier → confirms Stripe checkout loads correctly → verifies coupon code applies discount → test transaction completed in Stripe test mode. Full flow logged as pass/fail before pre-launch checklist is generated.
- Mobile responsive: verified via browser automation at 375px viewport
- Deployed alongside the landing page before pre-launch checklist is generated

**Objection Content Production:**

ICP pain data and competitor weakness data are the source of truth — no invented objections:

- Top 5 objections synthesized from: ICP's documented hesitations, competitor's 1-3 star reviews, and pain threads from validation
- Each objection gets a complete response written in VoC language, humanized via the `humanize` skill with `channel=blog`, formatted for three contexts simultaneously:
  - **Landing page FAQ:** `question: ..., answer: ...` formatted for the FAQ component
  - **Email copy:** standalone paragraph that addresses the objection naturally in the Day 7 Objection Killer email (handed to Nurture Agent)
  - **Sales deck slide:** one-line objection + two-line response in slide format
- ROI calculator generated as an interactive web component: inputs (time spent on the problem, hourly rate, or current tool cost), outputs (cost of problem vs cost of solution). Simple, honest math — not inflated. Embedded in the landing page or as a standalone `/roi` page.

**Post-Purchase Sequence Production:**

Paying customers get a completely separate sequence from the nurture flow — this is onboarding, retention, and referral:

> *Example post-purchase sequence for a typical SaaS product. Agent adjusts based on product complexity and price point. A $5/mo tool may only need 2-3 emails; enterprise onboarding may need a 30-day drip.*

- **Email 1 (immediate):** "You're in. Here's exactly what to do first." Single CTA, single action, path to value in under 5 minutes.
- **Email 2 (Day 3):** "How's it going?" — conversational check-in, invite reply, surface support proactively before they churn
- **Email 3 (Day 7):** "Getting results? We'd love to hear." — testimonial ask, low-friction (link to a 2-question form, not a paragraph request)
- **Email 4 (Day 14):** Referral program invitation — "Share [product] with a colleague and you both get [benefit]." Referral link generated per user.
- **Email 5 (Day 30):** Retention check or upsell prompt — for products with multiple tiers, this is the natural upgrade nudge based on usage signals
- All 5 emails: 3 A/B subject line variants, humanized copy, brand-consistent HTML templates
- Sequence imported into email provider as a separate automation from the nurture sequence — triggered by `purchase` event, not group join
- Full sequence tested: test purchase triggers the correct automation, Day 0 email delivers correctly, subsequent delays configured
- Schedule post-purchase check-in measurement via `cron` tool: daily snapshot for Days 1-7, then weekly — tracks activation rate, D3 retention, D14 revenue per cohort

**Done when:** Payment infrastructure live and tested end-to-end, pricing page deployed and mobile-verified, top objections addressed across landing page, email, and sales contexts, post-purchase onboarding sequence active and verified.

> 📎 **Deep dives:** [Simulation § Closing](../docs/SHIP-ENGINE-SIMULATION.md#stage-5d-closing-agent) · [Agentic Map § Closing](../docs/SHIP-ENGINE-AGENTIC-MAP.md#stage-5d-closing-agent) · [Canvas Vision § Pricing Page Artboard](../docs/SHIP-ENGINE-CANVAS-VISION.md#-pricing-page-artboard)

---

## AI Generation Protocol

> **Implements [Decision #13](#decision-13--talent-tickets-linear--telegram-ai-placeholder-continues) and extends the Talent Tickets pattern.** Not a separate doc — this is how every parallel agent handles all deliverable generation throughout Stage 5.

### Core Principle

**AI generates everything. Most of it IS the final product.**

This is not a "placeholder" strategy. The engine produces real, shippable deliverables — landing page copy, email sequences, blog posts, social content, images, data visualizations, screenshots — and the AI-generated version is the actual deliverable, not a draft waiting for a human. For a small number of high-touch items, a human version is an optional upgrade that improves quality but is never required to ship.

The pipeline never blocks. Every deliverable ships in the AI-generated version. Human upgrades happen asynchronously, tracked in Linear, and swap in when they're ready.

### Three-Tier Model

Every deliverable is classified into one of three tiers at the start of the workstream:

| Tier | Name | What it means | Talent ticket? |
|------|------|---------------|---------------|
| **1** | **AI-Final** | AI output IS the deliverable. No human version ever needed. | Never |
| **2** | **AI-Excellent** | AI output ships as final. Human upgrade is optional, rarely a priority. | Optional, at Max's discretion |
| **3** | **AI-Starter** | AI version ships immediately. Human version is a meaningful improvement. | Yes — auto-created, auto-notified |

---

#### Tier 1: AI-Final

The AI version is the real thing. These are not "AI drafts" — they are done.

- **Copy:** Landing page copy, blog posts, email sequences (full nurture + post-purchase), social posts, objection handling, FAQ, offer stack, press quotes, ad copy
- **Data & config:** SEO metadata, schema JSON-LD, UTM links, GA4 event schema, Stripe config
- **Visual — data-driven:** Product screenshots (via `browser` tool), social proof cards (HTML template + real analytics data), infographics (LLM + Mermaid → SVG), OG images, demo GIFs (browser automation)
- **Infrastructure:** Pricing page, landing page (deployed), email automation sequences (live), funnel forms

---

#### Tier 2: AI-Excellent

AI output ships as the final version. A human or design upgrade exists but isn't worth prioritizing unless a specific quality bar demands it. No talent ticket created — agent optionally flags the upgrade path.

- Hero images (blog article heroes, launch announcement visual)
- Blog post illustrations (in-article imagery)
- Ad creative (image variants + copy combinations)
- Logo variants (light, dark, icon, favicon — generated from Product Brief brand context)
- Sales deck design (template + branded visuals)
- Lead magnet cover design, opt-in page hero visual
- Email header images

---

#### Tier 3: AI-Starter

AI version ships immediately and is fully functional. Human version delivers meaningfully better authenticity, warmth, or social proof. Talent ticket auto-created (Decision #13), Max pinged via Telegram.

| Deliverable | AI Version | Tool | Human Upgrade | Why It Matters |
|-------------|-----------|------|---------------|----------------|
| Floating head / founder video | AI avatar + voice clone narration | `sag` skill + `content-image` + `ffmpeg` | Max on camera | Personal authenticity and audience connection — significant conversion impact |
| Podcast / audio content | Voice clone narration | `sag` skill (`ELEVENLABS_API_KEY`) | Studio recording | Production warmth and naturalness |
| Customer testimonial video | AI-generated using real user metrics and quotes | Avatar tools + `analytics-collector.py` data | Real customer on camera | Social proof authenticity — the "real person" signal matters |

> **Team photos and founder headshots** are Tier 2 by default (AI portrait via `content-image` ships fine), not Tier 3 — unless a specific high-visibility use case (press feature, PH About page) warrants professional photography. Agent classifies per context.

---

### Generation Lifecycle

Lifecycle varies by tier. Only Tier 3 enters the talent ticket flow.

```
For every deliverable:
  └─ Classify tier (1, 2, or 3)

Tier 1:
  → Generate with AI
  → Humanize copy via the `humanize` skill (if copy deliverable)
  → Upload to Drive run folder
  → Set blackboard key {stage}.{artifact}
  → Set tier: 1, ai_tool: "{tool}"
  → Ship. Done. No further action.

Tier 2:
  → Generate with AI
  → Upload to Drive run folder
  → Set blackboard key {stage}.{artifact}
  → Set tier: 2, ai_tool: "{tool}"
  → Optionally note upgrade path in run log
  → Ship. Human upgrade at Max's discretion.

Tier 3:
  → Generate AI version
  → Upload to Drive run folder
  → Set blackboard key {stage}.{artifact}
  → Create Linear talent ticket (NEO board, Decision #13)
  → Ping Max via Telegram
  → Set tier: 3, ai_tool: "{tool}", talent_ticket: "NEO-XXX"
  → Continue pipeline — do not block

  Talent delivers (Tier 3 only):
    → Upload human version to Drive
    → Move AI version to /ai-original/ subfolder (keep as variant)
    → Update blackboard key to human version
    → Set talent_ticket_closed: true, human_version_drive_id: {id}
    → Close Linear ticket
    → Canvas updates via blackboard.written event (Decision #11)
```

### Quality Expectations

- **No lower bar for AI output.** Tier 1 and 2 deliverables are the product — they face the same critic gate as anything else. "AI-generated" is not a pass. If it's not good enough to ship, revise it.
- **Tier 3 AI versions must be ship-quality, not visibly rough.** The AI starter is the live version until a human upgrade arrives. It must be indistinguishable from intentional design. An AI avatar video should match the product's tone and ICP language; a generated portrait should look like a professional headshot.
- **Tier 2 upgrades are Max's call.** Agent surfaces the option; Max decides if the ROI is worth it. Default: skip unless the specific deliverable is high-visibility.
- **Tier 3 never blocks a gate.** Pre-Launch checklist marks Tier 3 deliverables with `[AI-Starter, upgrade pending]` for visibility — not as blockers. The run proceeds.

### Per-Stage Tier Assignments

Each agent classifies its deliverables at workstream start. Quick reference:

| Stage | Tier 1 (AI-Final) | Tier 2 (AI-Excellent) | Tier 3 (AI-Starter) |
|-------|-------------------|----------------------|---------------------|
| **Awareness** | Landing page copy, blog posts, social content packs, SEO package, OG images, screenshots, demo GIF, UTM-tagged assets | Hero images, blog illustrations | Founder / floating head video |
| **Lead Capture** | Offer stack copy, UTM links, email group config, GA4 schema, tracking test log | Lead magnet cover design, opt-in page hero | — |
| **Nurture** | Full nurture email sequence copy, content drip schedule | Email header images, social proof graphics | — |
| **Closing** | Pricing page, objection handling (FAQ + email + deck), post-purchase email sequence, Stripe config | Sales deck design, pricing page hero | Demo video (if Max-on-camera version planned) |
| **Launch** | PH maker comment, press release copy, directory listings | PH gallery images, launch announcement visual, founder bio photo | Launch announcement video, testimonial videos |

> *These are default classifications. Agent may reclassify any deliverable with justification based on ICP expectations and product positioning. A design-focused enterprise product might elevate hero images to Tier 3. A developer tool audience might accept Tier 1 AI avatar video.*

Awareness carries the highest AI generation volume across all three tiers. The AI video first-pass described in the [Awareness Video Production](#awareness-agent--production-pipeline) section is the Tier 3 delivery mechanism for all video deliverables.

### State Schema

Every deliverable tracked in the blackboard (Decision #11) carries these fields alongside `drive_id` and `status`.

Writeback requirements:
- `status_summary` and `next_steps` are required on every meaningful update.
- In `production`, `critic_verdict=PASS` is required before a deliverable can be marked `verified` (and before it can go `live`).
- `talent_ticket` and `human_version_drive_id` are only populated for Tier 3.

**Tier 1 example (blog post):**
```json
{
  "drive_id": "1abc...xyz",
  "status": "live",
  "status_summary": "Published blog post; CTA routes to lead magnet",
  "next_steps": ["Collect 24h metrics snapshot", "Iterate hook if CTR is low"],
  "risk_level": "low",
  "critic_verdict": "PASS",
  "critic_evidence": "linear://comment/...",
  "draft_id": "content-engine:draft:123",
  "approval_record": null,
  "live_id_or_url": "https://example.com/blog/...",
  "metrics_snapshot": ["ga4://report/..."],
  "disposition": "iterating",
  "tier": 1,
  "tier_label": "ai-final",
  "ai_tool": "llm+humanize",
  "talent_ticket": null,
  "human_version_drive_id": null
}
```

**Tier 3 example (founder video, pre-upgrade):**
```json
{
  "drive_id": "1def...uvw",
  "status": "live",
  "status_summary": "AI-starter video is live; talent upgrade pending",
  "next_steps": ["Collect 24h metrics snapshot", "Swap human version when ready"],
  "risk_level": "low",
  "critic_verdict": "PASS",
  "critic_evidence": "linear://comment/...",
  "draft_id": "ig:draft:456",
  "approval_record": null,
  "live_id_or_url": "ig:reel:...",
  "metrics_snapshot": ["meta://insights/..."],
  "disposition": "iterating",
  "tier": 3,
  "tier_label": "ai-starter",
  "ai_tool": "elevenlabs+gemini+ffmpeg",
  "talent_ticket": "NEO-142",
  "talent_ticket_closed": false,
  "human_version_drive_id": null
}
```

| Field | Values | Meaning |
|-------|--------|---------|
| `status` | `requested|in_production|verified|draft_scheduled|awaiting_max_approval|live|measured|promoted|iterating|killed` | Deliverable lifecycle state (Stage 9) |
| `status_summary` | `string` | One line: what changed + what's next |
| `next_steps` | `string[]` | Immediate next actions for this deliverable |
| `risk_level` | `low`, `medium`, `high` | Risk label (defaults to `low`) |
| `critic_verdict` | `PASS`, `REVISE` | Critic outcome required in `production` to reach `verified` |
| `critic_evidence` | `string` | Link to critic comment/report |
| `draft_id` | `string` / `null` | Platform draft OR publish-ready queue reference (calendar draft optional) |
| `approval_record` | `string` / `null` | Link to explicit approval when required |
| `live_id_or_url` | `string` / `null` | Publish ID or URL when live |
| `metrics_snapshot` | `string[]` | Time-stamped analytics/insights links |
| `disposition` | `promoted`, `iterating`, `killed`, `null` | Current/final disposition |
| `tier` | `1`, `2`, `3` | Generation tier (see Three-Tier Model above) |
| `tier_label` | `"ai-final"`, `"ai-excellent"`, `"ai-starter"` | Human-readable label; shown in Canvas |
| `ai_tool` | e.g. `"dalle"`, `"elevenlabs"`, `"playwright"`, `"llm+humanize"` | Tool that produced the AI version |
| `talent_ticket` | `"NEO-XXX"` / `null` | Linked Linear ticket. Only set for Tier 3. |
| `talent_ticket_closed` | `true` / `false` / `null` | Tier 3 only — set when human version arrives |
| `human_version_drive_id` | Drive file ID / `null` | Tier 3 only — set when talent delivers |

Blackboard keys follow `{stage}.{artifact}` (Decision #11): `awareness.founder_video`, `launch.testimonial_video`. A `blackboard.written` event fires on every write and swap — Canvas updates automatically.

### Tools

All tools available on this instance. See [Available Services Reference](#available-services-reference). Tool selection follows Decision #9 (capability-based references).

| Capability | Default Tool | Primary Tier Usage |
|-----------|-------------|-------------------|
| Copy generation | LLM + `humanize` skill | Tier 1 — all copy humanized before output, no exceptions |
| Image generation | `content-image` skill (Gemini-first) | Tier 1/2 — OG images, heroes, social assets, brand visuals |
| Screen capture | `browser` tool | Tier 1 — product screenshots, social proof cards, template renders |
| Voice synthesis | `sag` skill (ElevenLabs via `ELEVENLABS_API_KEY`) | Tier 3 — AI narration for video first-pass; `tts` tool for quick drafts |
| Video assembly | `ffmpeg` | Tier 3 — combine `sag` narration + `content-image` stills into AI video |
| Data visualization | LLM + Mermaid → SVG | Tier 1 — infographics, architecture diagrams, workflow charts |

> **HeyGen/Synthesia not configured in v1.** Tier 3 video first-pass: build using `sag` (narration) + `content-image` (stills) + `ffmpeg` (assembly). External avatar APIs are a P2 integration, configurable once the first run demonstrates demand.

---

## Parallel Join

All 4 agent workstreams are tracked independently. When one lane is blocked, other lanes continue and verified deliverables can still move through Stage 9.

**Join behavior:**
1. Deliverables do not wait for all lanes to finish to enter `draft_scheduled`.
2. Low-risk deliverables can auto-canary after verification.
3. High-risk deliverables pause at `awaiting_max_approval` before `live`.
4. Gate-L (Stage 6) waits for coordinated scale package readiness, not for every possible draft to be published.

**If a lane is blocked:**
- Mark it blocked with reason
- Other stages continue independently
- Notify Max of the blocker
- Check back periodically

**Iterative, not one-and-done:** Agents collaborate throughout execution. Insights from one stage feed back into others. The parallel phase is a continuous feedback loop, not four isolated sprints.

---

## Stage 6: APPROVAL GATE — Pre-Launch 🔒

Supervisor: `ship-launch-supervisor`

**Max sees a checklist summarizing coordinated scale readiness:**

Agent pre-fills the decision packet (see Gate Prefill Requirement) with recommendation, top blockers, and next steps.

| Area | Status | Key question |
|------|--------|-------------|
| Awareness | ✅/❌ | Landing page deployed to live URL? All content and assets generated? Talent recordings done? |
| Lead Capture | ✅/❌ | Offer stack deployed? Email group + forms live? UTM links generated? Tracking end-to-end verified? |
| Nurture | ✅/❌ | Email sequence imported and live in automation? Test email verified? |
| Closing | ✅/❌ | Stripe products/prices live? Checkout tested? Pricing page deployed? Post-purchase sequence active? |
| Product | ✅/❌ | App live, working, mobile-responsive? |
| Stage 9 | ✅/❌ | Draft queue healthy? high-risk approvals resolved? rollback plan ready? |

**Max chooses:**

| Decision | What happens |
|----------|-------------|
| **Launch** | Execute coordinated scale sequence (Stage 7) |
| **Fix Issues** | Max specifies what's not ready. Relevant agent(s) re-open, fix, re-present. |
| **Kill** | Not worth launching. Archive. → `dead` |

Decision line for automation parsing (required in production): `decision: launch|fix|kill`

**Completion (Deliverables):** Max decision is recorded in the Stage 6 ticket (comment + state update) with links preserved.

**Same timeout rules:** 24h ping, 48h ping, then auto-pause.

---

## Stage 7: LAUNCH (COORDINATED SCALE)

Supervisor: `ship-launch-supervisor`

**Purpose:** Execute coordinated scale waves after Gate-L. Stage 7 orchestrates timing, channel sequencing, and high-visibility pushes using already-verified deliverables moving through Stage 9.

**Core principle:** Stage 9 runs continuously; Stage 7 is the scale amplifier, not the first moment launch/measurement exists.

---

### Phase 1: Pre-Launch Warm-Up (Before L-Day)

The parallel agents have already built community presence, content, and assets. Pre-launch focuses on **generating anticipation and priming the audience.**

**Build-in-Public Content:**
- Share the building journey across all platforms — what we're making, why it matters, what problem it solves
- Show behind-the-scenes: early screenshots, design decisions, "this is what X looks like" previews
- This isn't just marketing — it's audience research. See what resonates, what gets questions, what gets ignored
- Every build-in-public post is a data point for launch messaging

**Waitlist / Early Access:**
- If applicable: open a waitlist or early access signup before launch
- Creates urgency and a ready-made audience for L-Day
- Waitlist size = demand signal. <20 signups after a week of promotion = re-evaluate positioning

**Platform-Specific Pre-Launch:**

| Platform | Pre-Launch Action |
|----------|------------------|
| **Product Hunt** | Build PH profile (photo, bio, links). Comment thoughtfully on 10+ launches in your category over 2+ weeks. Engage with makers. Build recognition before your own launch. |
| **Reddit** | Ensure accounts have 100+ karma in relevant subreddits. Post valuable content (not product) in target subs for 2+ weeks. Be a known, helpful member before mentioning any product. |
| **IndieHackers** | Post build log / journey updates. Engage in discussions. Establish credibility. |
| **X/Twitter** | Thread about the problem space. Share insights from validation research. Build audience around the pain, not the product. |
| **LinkedIn** | Share professional perspective on the problem. Network with ICP-matching connections. |
| **TikTok/Reels/Shorts** | Teaser content: "Building something for [pain]" — hook-driven short video |

**Directory Pre-Submissions:**
Submit to these directories BEFORE launch day (many have review queues):
- BetaList
- SaaSHub
- LaunchingNext
- MicroLaunch
- Uneed
- There's An AI For That (if AI-related)
- ToolFinder
- SaaSWorthy
- AlternativeTo
- Relevant niche directories for the specific category

These provide:
- Free distribution to targeted audiences
- SEO backlinks (compounds over time)
- Category presence (shows up when people search for alternatives)

**Supporter Rally (Product Hunt specific):**
- Build a list of 150-300 supporters segmented by timezone (APAC/EU/US)
- Warm them up by asking for feedback on the product (not asking for upvotes — that gets flagged)
- Day-of, they'll naturally engage because they already know and care about the product

**Pre-Launch Checklist (finalize before L-Day):**

| Check | Status |
|-------|--------|
| Product URL live, core feature works, mobile responsive | |
| Landing page deployed to live URL, copy final, OG tags working, share preview looks good | |
| Analytics tracking verified end-to-end (GA4 events firing, UTMs working, email group wired) | |
| Payment/checkout flow tested end-to-end (Stripe test mode + live mode) | |
| Email capture forms live and tested | |
| Welcome email sequence active and tested (test email verified) | |
| Post-purchase sequence active and tested | |
| All launch content drafted per platform | |
| Product Hunt submission drafted (tagline, description, images, maker comment) | |
| Reddit posts drafted per subreddit (value-first, not self-promo) | |
| IndieHackers "Shipped" post drafted | |
| X/LinkedIn launch threads drafted | |
| Video content recorded and edited (from talent tickets) | |
| Launch email to existing list drafted | |
| Directory submissions sent | |
| Supporter list ready with timezone segments | |
| <15 min response capability confirmed for L-Day | |

---

### Mandatory Human Gate — Final Social Push Package 🔒

Before any broad social media push is enabled/published, Max must approve the final social package. Platform draft/calendar is optional; publish-ready package is sufficient.

Agent pre-fills the approval packet (see Gate Prefill Requirement) with the proposed wave plan, highest-impact posts, risks, and next steps.

Package contents (required):
- Platform-ready copy for each target platform (EN + ES when applicable)
- Final media assets mapped per post (images/video/thumbnail variants)
- Links + UTMs + destination validation
- Posting sequence and timing (wave mapping)
- Risk notes (brand/legal/compliance, if any)

Max chooses:

| Decision | What happens |
|----------|-------------|
| **Approve Push** | Social push is unlocked and publishing begins. |
| **Revise Package** | Returns package to relevant supervisor(s) for edits and re-review. |
| **Hold Push** | Social publishing stays paused while other launch operations can continue. |

Decision line for automation parsing (required in production): `decision: approve|revise|hold`

Rules:
- No social API publish or manual social push request before this approval.
- If no response: 24h reminder, 48h reminder, then social push remains paused until explicit decision.

---

### Phase 2: Launch Day (L-Day)

**When to launch:** Tuesday, Wednesday, or Thursday. These have highest engagement across PH, Reddit, and IH. Avoid Mondays (slow start) and Fridays (weekend drop-off).

**Launch is executed in timezone waves, not a single blast.** This maximizes engagement across global audiences and keeps momentum building throughout the day.

**Wave 1 — Seed (early supporters, warm audience, community)**

Activate the people who already know and care about the product. Personal outreach, not broadcast.

| Action | Details |
|--------|---------|
| Notify early supporters (first timezone wave) | "We're live — check it out and share your thoughts." Personal, genuine. NOT "please upvote/share." |
| Post to builder communities | "Shipped" post format: the build story + metrics from validation + what you learned + link. Communities value transparency and story over polish. |
| Directory/platform submissions | Submit to any launch platforms included in Strategy (e.g., Product Hunt, IndieHackers, BetaList). |

**Wave 2 — Amplify (broader audience, social channels, partnerships)**

Expand reach beyond warm audience. Value-first content across social channels.

| Action | Details |
|--------|---------|
| Community posts | Post in 3-5 relevant communities (Reddit, Discord, forums). Value-first format: describe the problem, what you learned building a solution, share the product naturally. Each community gets a slightly different angle tailored to its culture. Stagger posts 30-60 min apart. |
| Launch email blast | To existing list + waitlist. "It's live. Here's your founding member access." Include the launch offer, clear CTA, and one-click path to the product. |
| Notify supporters (next timezone wave) | Same personal outreach, next timezone segment. |

**Wave 3 — Peak (maximum visibility push, paid amplification if applicable)**

Peak engagement window. Long-form social content, cross-platform updates, momentum signals.

| Action | Details |
|--------|---------|
| Social launch threads | 5-7 post thread (X, LinkedIn, etc.). Hook is about the pain (not the product). Walk through: problem → what you tried → what you built → results → CTA. |
| Cross-post momentum updates | Share live metrics ("50 signups in the first 3 hours!") on active platforms. Social proof compounds. |
| Notify supporters (final timezone wave) | Final timezone segment. |

**Wave 4 — Sustain (follow-up content, retargeting, ongoing momentum)**

Capture the long tail. Rich media, community engagement, paid channels if applicable.

| Action | Details |
|--------|---------|
| Short-form video push | Launch video — hook-driven, <60s. Problem → solution → demo → CTA. Publish across all short-form platforms (TikTok, IG Reels, YT Shorts) simultaneously. |
| Community engagement | Post in relevant Discord servers, Slack groups, Facebook groups. Follow each community's rules. Some allow product shares, some only in designated channels. |
| Visual content push | Visual launch announcement (carousel, post, etc.) across image-friendly platforms. |
| Activate ads | If budget allocated in Strategy. Start with small daily spend, test creative variants. |

> **Product Hunt example timing:** If PH is in the launch plan: Wave 1 = submit at 12:01 AM PT, notify APAC/EU supporters. Wave 2 = 8-10 AM PT, engagement peaks. Wave 3 = 12-2 PM PT, share live metrics in maker comment. Wave 4 = 3-6 PM PT, cross-post final results. PH-specific: tagline under 40 chars, 4-6 outcome-first screenshots, <45s demo video, 300-word maker comment.

**Throughout L-Day — Continuous:**

| Action | Why | Target |
|--------|-----|--------|
| **Reply to EVERY comment within 15 minutes** | Engagement speed drives algorithmic boost on every platform. Early comments get more visibility. People who get fast replies become advocates. | All platforms |
| **Monitor and share live metrics** | "Just hit 100 signups" posts create FOMO and social proof. Real numbers > vague hype. Pull live data via `tools/analytics-collector.py`. Notify Max via `message` tool (Slack DM) with milestone alerts. | PH, X, IH |
| **Fix issues in real-time** | First users WILL find bugs. Fix fast, announce the fix publicly ("Great catch by @user — fixed in 10 minutes"). Makes you look responsive and builds trust. | Product + all platforms |
| **Capture testimonials in real-time** | Screenshot positive comments, DMs, reactions. These become social proof assets for days 2-7+. | All platforms |
| **Route everything to capture** | Every reply, every comment, every DM should naturally point toward the product/signup. Not pushy — helpful with a link. | All platforms |

**L-Day Success Metrics:**

| Metric | Good signal | Concerning signal |
|--------|------------|-------------------|
| Product Hunt | Top 5 of the day | Below #10 |
| Signups | 50+ | <10 |
| Landing page conversion | 15-25% visitor→signup | <5% |
| Engagement | Lots of questions and discussion | Silence or only "cool" reactions |
| First paying customers | Any on day 1 | — (not expected but great signal) |

---

### Phase 3: Post-Launch Momentum (L+1 to L+14)

**Traffic drops 60-75% by day 3.** This is normal. The goal of post-launch is to capture the long tail, activate signups, and build sustained organic growth.

**Content Cadence:**

| Day | Content | Platform | Purpose |
|-----|---------|----------|---------|
| L+1 | Tutorial: "How to get [result] with [product] in 5 minutes" | All platforms (adapted per format) | Drive activation. Show the aha moment. |
| L+2 | Behind-the-scenes: launch day metrics and reactions | X, IH, LinkedIn | Build in public. Transparency builds trust. |
| L+3 | Early results thread: "What users are saying after 72 hours" | X, Reddit | Social proof from real users (use captured testimonials from L-Day) |
| L+5 | Second community engagement round | Reddit, Discord, forums | New posts in different subreddits or different angles in same subs |
| L+7 | Lessons learned: "What I learned launching [product]" | All platforms (long-form for blog/YT, adapted for social) | SEO play + genuine reflection + audience building |
| L+10 | User spotlight / case study | All platforms | Deep social proof. One user's specific result. |
| L+14 | "Two weeks in — here's the data" | X, IH, LinkedIn | Transparent update with real numbers. Sets up sustained content cadence. |

**Activation Push (L+1 to L+7):**

This is the most critical post-launch window. Research shows 40% of users "ghost" on Day 1 if they don't reach the aha moment.

- **Onboarding email (immediate on signup):** Get to first value in <5 minutes. Pre-filled examples, 2-step max to first meaningful result. Not a product tour — a result.
- **Day 1 nudge:** If they signed up but didn't activate — email with direct path to aha moment. "You're 1 click away from [result]."
- **Day 3 check-in:** Personal-feeling email. "How's it going? Hit reply if you need help."
- **Day 7 activation report:** Internal — what % of signups activated? If <50%, onboarding is broken. Fix it before spending on more awareness.

**Platform-Specific Follow-Up:**

| Platform | Post-Launch Action |
|----------|-------------------|
| **Product Hunt** | Add "first update" post after 7 days. Share what you built/fixed based on PH feedback. PH community loves iteration stories. |
| **Reddit** | Don't re-post the product. Instead, continue being helpful in pain threads. Your profile now shows the product — organic discovery. |
| **IH** | Post milestone updates ("Week 1: X signups, Y revenue, here's what I learned"). IH rewards consistent journey sharing. |
| **Directories** | Check submissions — many have 1-2 week review queues. Follow up on pending ones. Update listings with post-launch info. |

**SEO Compounding:**
- The competitor comparison articles and pain-keyword articles from Awareness are now live
- Directory backlinks are accumulating
- Launch content generates social signals
- Monitor which keywords are getting impressions in the first 2 weeks
- This is the beginning of the organic flywheel — it compounds over weeks and months

---

### Phase 4: Sustained Distribution (L+14 onwards)

Launch energy fades. Sustained growth comes from systems, not events.

**Ongoing Content Engine:**
- Continue publishing content mapped to pain keywords from ICP
- Repurpose launch content into new formats (blog → carousel → thread → reel)
- Community participation continues — this is not a launch tactic, it's a growth habit
- User stories and testimonials become a regular content type

**Growth Loops:**
- Happy users → referral program → new users (from Closing Agent's post-purchase flow)
- Content → SEO → organic traffic → signups (compounds monthly)
- Community presence → trust → organic mentions → signups (slow but high quality)
- Email list → nurture → conversion → testimonial → content → email list (circular)

**When to Re-Launch:**
- Major feature release = mini-launch (not full campaign, but content push + community posts)
- Significant milestone (100 users, $1K MRR) = build-in-public post across platforms
- Product Hunt allows re-launches for major versions — save this for a meaningful update

**Handoff to Measure:** Once L+14 content is published and all launch systems are running, Launch transitions to Measure. The content engine and community presence continue as ongoing operations — they don't stop when Measure starts.

---

### Launch Coordination

**Who does what during launch:**

| Actor | Responsibility |
|-------|---------------|
| **Awareness Agent** | Publishes all content across all platforms. Adapts per platform format. Manages content calendar timing. |
| **Lead Capture Agent** | Monitors funnel performance in real-time. Adjusts capture mechanisms if conversion is low. Ensures UTMs are tracking correctly. |
| **Nurture Agent** | Activates welcome sequence. Monitors activation rates. Sends nudge emails to non-activated signups. |
| **Closing Agent** | Monitors payment flow. Handles checkout issues. Captures early testimonials for social proof loop. |
| **Talent (Human)** | Available for real-time engagement on personal accounts. Responds to DMs, comments, questions. Records any spontaneous video content. Batch availability: at least 2-3 hours on L-Day. |

**Reply SLA:** <15 minutes on all platforms during L-Day. This is non-negotiable. Engagement speed drives algorithmic boost and converts curious visitors into users. After L-Day, <2 hours is acceptable.

---

### What Makes a Good Launch vs a Bad Launch

| Good Launch | Bad Launch |
|-------------|-----------|
| Traffic converts to signups (15-25%) | High traffic, no signups (landing page problem) |
| Users activate within 24h (>50%) | Users sign up and never return (onboarding problem) |
| Engagement is questions and discussion | Engagement is only "cool" or nothing |
| Organic mentions appear within 48h | Zero organic mentions (positioning problem) |
| Early revenue on day 1-3 | — |
| Content gets shared/saved | Content gets ignored |
| Community replies feel genuine | Community flags posts as spam |

**If launch underperforms:** Don't panic. Review the data:
- Low traffic → distribution problem (Awareness)
- High traffic, low signup → landing page / offer problem (Lead Capture)
- High signup, low activation → onboarding problem (Closing)
- High activation, low payment → pricing / value problem (Closing + Strategy)

This diagnostic feeds directly into Measure's iteration loop.

---

**Done when:** Coordinated scale waves execute, high-risk approvals are honored, and all scaled deliverables link back to Stage 9 evidence (draft id, approval record, live id/url, metrics snapshot).

---

## Stage 8: MEASURE (SYNTHESIS + FINAL VERDICT)

Supervisor: `ship-measure-supervisor`

**Purpose:** Synthesize Stage 9 measurement evidence at run level, compare performance to targets, and recommend final direction.

**Cadence:**
- Stage 9 starts measurement as soon as first deliverables go live.
- **Phase 1 (first sprint post-scale):** Daily synthesis. Internal — not posted unless anomaly or great news.
- **Phase 1 checkpoint:** Report with early read on what's working and what's not.
- **Phase 2 (subsequent sprints):** Weekly tracking. Adjust based on Phase 1 learnings.
- **Phase 2 checkpoint:** Final report with recommendation.

**Tooling:** Pull all metrics via `tools/analytics-collector.py` (GA4, GSC, Meta simultaneously). Synthesize into a cross-channel report via the `brand-report` skill (7 data sources). Schedule recurring data pulls via `cron` tool: daily for Phase 1, weekly for Phase 2. Notify Max via `message` tool with report summaries. Pull Instagram insights (reach, engagement, profile visits) via `tools/lib/meta_api.py`.

**What gets tracked:**

| Category | Metrics |
|----------|---------|
| Traffic | Visitors, source breakdown, UTM performance per channel |
| Conversion | Signups, signup rate, signup rate by channel |
| Activation | Users reaching first value moment (product-specific) |
| Revenue | Total revenue, transactions, average revenue per user |
| Email | Open rates, click rates, unsubscribe rates per email in sequence |
| Social | Reach, engagement rate, link clicks per platform |
| Outbound | Community engagement, reply effectiveness |
| Retention | Return rate over time |

**Decision Framework:**

| Performance vs targets | Verdict |
|----------------------|---------|
| ≥80% | **DOUBLE DOWN** 🟢 — invest more: content, ads, features, new channels |
| 40-79% | **ITERATE** 🟡 — promising but needs tuning: A/B test, fix funnel leaks, try different channels |
| 10-39% | **MAINTAIN** 🟠 — keep alive with minimal effort, see if it compounds |
| <10% | **KILL** 🔴 — archive, extract lessons, move on |

**Max makes the final call.** The engine recommends with data, doesn't decide.

**If killed:**
- Stop all active activities (email sequences, ads, scheduled content)
- Archive everything
- Extract lessons
- Close tracking

**Done when:** Max confirms final verdict and disposition is recorded for all launched deliverable cards (`promoted`, `iterating`, or `killed`).

---

## Stage 9: CONTINUOUS LAUNCH + MEASURE

Owner: shared lane supervisors (`ship-awareness-supervisor`, `ship-lead-capture-supervisor`, `ship-nurture-supervisor`, `ship-closing-supervisor`) with `ship-launch-supervisor` policy oversight.

**Purpose:** Run an always-on deliverable lifecycle loop so validated artifacts can be scheduled, launched, measured, and iterated without waiting for full-lane completion.

### Trigger

Any deliverable card with complete Verification + Artifacts enters Stage 9 automatically. In `production`, Verification includes a critic `PASS`.

On every deliverable status transition, the owner agent writes a one-line status summary and the next step into the card/ticket.

### Lifecycle

`verified -> draft_scheduled -> awaiting_max_approval (high-risk only) -> live -> measured -> promote|iterate|kill`

### Risk policy (hybrid)

- Risk rubric is intentionally lax: default `low`.
- Low-risk deliverables: auto-schedule drafts and allow auto-canary to `live`.
- High-risk deliverables: require explicit Max approval before `live`.
- Hard gates remain mandatory for stage transitions (`Gate-V`, `Gate-S`, `Gate-L`, Final Social Push).

High-risk triggers (minimal set): money beyond policy/budget, pricing/billing changes, broad social push waves, and any publishing action that speaks as Max (including posting to Max-owned social accounts).

Enablement semantics:
- High-risk deliverables are publish-ready after critic `PASS`, but publishing stays disabled until Max enables it (Publish Enablement Queue or Final Social Push gate).
- Enablement must be recorded as `approval_record` linking to a Max decision comment that contains the required `decision:` line.

### Mandatory evidence per deliverable card

- `status_summary` (one line)
- `critic_verdict` (PASS/REVISE + link)
- `recommendation` (approve/revise/kill + why)
- `next_steps` (what executes next)
- `draft_id` (platform draft OR publish-ready queue reference; calendar draft is optional)
- `approval_record` (required when high-risk)
- `live_id_or_url`
- `metrics_snapshot` (time-stamped links)
- `disposition` (`promoted|iterating|killed`)

### Safety controls

- Kill-switch: any supervisor or Max can pause/kill a deliverable instantly.
- Rollback: if canary fails threshold, revert to last stable draft/live variant and mark `iterating`.
- No social push bypass: Final Social Push gate still applies before broad social wave publishing.

---

## Approval Gates Summary

Pipeline-level hard gates (always required):

| Gate | When | Options | Default on silence |
|------|------|---------|-------------------|
| Post-Validation | After validation report + ICP | Ship / Explore / Kill | Pause after 48h |
| Post-Strategy Lock | After Ship Plan + lock pack | Proceed / Revise / Kill | Pause after 48h |
| Pre-Launch | After coordinated scale package is ready | Launch / Fix / Kill | Pause after 48h |

Launch-scoped mandatory gate:

| Gate | When | Options | Default on silence |
|------|------|---------|-------------------|
| Publish Enablement Queue (high-risk only) | Before high-risk deliverables move from publish-ready to live | Approve / Revise / Hold / Kill | Publish remains disabled |
| Final Social Push Package | Before Wave 2+ social publishing | Approve Push / Revise Package / Hold Push | Social push paused after 48h |

Decision lines (required in production):
- Publish Enablement Queue: `decision: approve|revise|hold|kill`
- Final Social Push Package: `decision: approve|revise|hold`

Everything else is automatic under policy. Max can intervene at any point (pause, kill, skip), but the engine does not publish final social push packages without this explicit gate.

All Max-facing gates must include a prefilled decision packet (see Gate Prefill Requirement).

Hard gates remain mandatory for stage transitions in production; they do not imply per-deliverable manual review when risk policy allows draft/canary automation.

---

## Supervision Gates (Feedback Loop Between Skills and Experts)

In addition to hard gates, runs can use supervision gates to tighten feedback without freezing the whole engine.

Rules:
- Supervision gates are configurable per run.
- They can block a stage lane, but should not block unrelated lanes.
- They are used for expert feedback loops, not for routine low-risk output.

---

## Engine Collaboration (Research + Content + Analytics)

Ship Engine is the governance layer. Research, Content, and Analytics engines collaborate by writing auditable artifacts and small, consistent writebacks into Linear and the ship-run blackboard.

### Roles

- Research Engine: discovers and stores structured intelligence (trend score, relevance, takeaways, VoC pain points) plus Drive vault links.
- Content Engine: produces content assets (pillar + waterfall), auto-schedules drafts, syncs artifacts to Linear, and maintains an append-only event log for auditability.
- Analytics Engine: snapshots performance evidence and emits iteration feedback events.

### Collaboration rules

- Linear remains the source of truth for work state. All meaningful changes must include `status_summary` + `next_steps` comments.
- Draft autoscheduling is allowed under policy. Auto-publishing to Max-owned social accounts is treated as high-risk and remains gated.
- Learning is metrics-gated: edits can be logged immediately, but preference updates must reference a real metrics snapshot.
- Each run has a Linear Project container. Any issues created during the run (stage tickets, content calendar tickets, feedback tickets) must inherit the run project's `projectId`.

### Required blackboard keys (minimum set)

Research / Validate / Strategy:
- `validate.research_dataset` (vetted sources + evidence links)
- `validate.research_brief` (synthesis + confidence + evidence)
- `strategy.voc_pain_points` (aggregated pain points)

Awareness / Content production:
- `awareness.content_candidates` (ranked candidates derived from research + semantic inspiration)
- `awareness.content_waterfall` (pillar + derivatives, linked)
- `awareness.content_calendar` (scheduled drafts mapped to assets)
- `awareness.social_pack` (per-platform pack summary)
- `awareness.research_to_content_sync` (audit map: research -> assets -> Linear)

Measure:
- `measure.kpis` (short KPI snapshot)
- `measure.feedback_events` (asset-level iteration actions + evidence links)

### Delegation guidance (skills-first)

- Awareness supervisors may delegate pillar drafting, waterfall generation, and draft autoscheduling to Content Engine skills.
- Measure supervisor may delegate asset-level metrics snapshotting and scoring to Content Engine measurement.
- Any delegation must still satisfy Stage 9 evidence rules (`draft_id`, `approval_record` when high risk, `live_id_or_url`, `metrics_snapshot`).

Suggested supervision gates:

| Gate | Trigger | Owner | Expert input | Effect |
|------|---------|-------|--------------|--------|
| SG-Validate-Depth | Validate reaches first evidence bundle | `ship-validate-supervisor` | Scope corrections, missing-source flags | Refines validation before Gate-V |
| SG-Strategy-Draft | First Ship Plan draft is ready | `ship-strategy-supervisor` | Positioning/offer/channel critique | Refines plan before Gate-S |
| SG-Parallel-Sync | Any cross-lane dependency conflict | Lane supervisors | Resolve offer/ICP/messaging drift | Blocks only impacted lanes |
| SG-Seed-Pack | First creative `seed_pack` generated | `ship-awareness-supervisor` | Approve/revise seed direction | Unlocks safe fanout for that asset family |
| SG-Publish-Risk | High-risk deliverable enters `draft_scheduled` | Deliverable owner supervisor | Approve/revise/kill before live | Blocks only that deliverable card |
| SG-Social-Push | Final social package assembled for launch | `ship-launch-supervisor` | Approve/revise/hold social push package | Mandatory before publishing social push |
| SG-Measure-Replan | Measure produces weak-signal verdict | `ship-measure-supervisor` | Replan direction (iterate/hold/pivot) | Opens next execution cycle with clear constraints |

---

## Pause, Kill & Skip

**Pause:** Freezes the run. No work, no notifications. Remembers where it was. Resumes to exact same state.

**Kill:** Stops everything immediately. All active work cancelled. Archived with reason and lessons. Terminal.

**Skip:** Jump to a specific stage. Useful when Max already has parts covered. Skipped stages marked as "skipped" — can be revisited if needed.

---

## How Stages Connect

Stages provide governance and context. Deliverable cards execute asynchronously through Stage 9.

```
VALIDATE produces → ICP (audience, pain, language, competitors, VoC)
    ↓
STRATEGY uses ICP to produce → Ship Plan (positioning, pricing, channels, targets)
    ↓
AWARENESS / LEAD CAPTURE / NURTURE / CLOSING produce verified deliverables
    ↓
STAGE 9 loop per deliverable: verified -> draft_scheduled -> (awaiting_max_approval if high-risk) -> live -> measured -> promote|iterate|kill
    ↓
LAUNCH (Stage 7) coordinates scale waves using Stage 9 live inventory
    ↓
MEASURE (Stage 8) synthesizes run-level results and recommends final verdict
```

No agent works in isolation. The ICP and Ship Plan are loaded as context for every agent. Stage 9 keeps launch + measurement always-on at deliverable level.

### Universal Prompt + Lineage Contract (All Deliverables)

Every deliverable must store prompt and lineage metadata across all tasks/deliveries.

Minimum lineage payload per deliverable:
- `prompt_source` (generated template, manual custom, or hybrid)
- `prompt_text` (or reference to stored prompt artifact)
- `prompt_overrides` (custom adjustments applied)
- `input_artifacts[]` (upstream artifacts used)
- `feedback_events[]` (expert/critic feedback tied to revisions)
- `feeds_into[]` (downstream deliverables/stages)
- `owner_skill` and `owner_supervisor`
- `draft_id` (platform draft OR publish-ready queue reference; calendar draft optional)
- `approval_record` (required for high-risk live transitions)
- `live_id_or_url`
- `metrics_snapshot` (time-stamped measurement links)
- `disposition` (`promoted|iterating|killed`)

This contract is mandatory for traceability and stage-to-stage prompt chaining.

---

## Document Structure

Minimal files, maximum reuse:

| Document | Created in | Referenced by | Evolves? |
|----------|-----------|---------------|----------|
| **Product Brief** | Intake | Validate, Strategy | No — snapshot at intake |
| **ICP** | Validate | ALL downstream stages and agents | Yes — enriched as we learn more |
| **Validation Report** | Validate | Strategy, Measure | No — point-in-time assessment |
| **Ship Plan** | Strategy | ALL parallel agents, Launch, Measure | Yes — updated if strategy pivots |
| **Agent Deliverables** | Each parallel agent | Launch, Measure, other agents | Yes — iterated based on collaboration |

---

## Agency Philosophy

> **The engine provides structure, not micromanagement.** Stages, gates, and state management are the engine's job. Creative decisions — what content to produce, which tools to use, how many emails to write, which channels to target — belong to the agents. Defaults and reference menus are provided as starting points, not mandates. Agents should justify deviations but are empowered to deviate.

### Miro-Inspired Concepts (Adapted to Ship Engine)

Boundary note:
- These are UI/design references for how work is visualized and reviewed.
- They do NOT alter Ship Engine internals: stage sequence, gate model, deliverable ownership, or strategy frameworks.
- The core remains AI Gen-first GTM execution using expert structures (Hormozi/acquisition.com) and existing supervisor-driven automation.

Applied principles:
- **Canvas as prompt:** agents act on canvas/context state, not isolated prompt boxes.
- **Sidekick specialization:** stage supervisors behave as domain sidekicks with explicit ownership.
- **Visual multi-step flows:** transformations are inspectable end-to-end.
- **Exploration with control:** variant generation is encouraged; fanout is gated by `seed_pack` approval.
- **Repeatable playbooks:** winning flows become reusable run templates.
- **Model-per-step routing:** best model per task, one coherent run ledger.

Our distinction from general collaboration tools:
- User primarily approves and steers.
- Agents primarily create and execute.
- Progress is measured by shipped artifacts, not whiteboard completeness.

### Playbook Lifecycle (Repeatability)

Runs should continuously improve through reusable playbooks:
- Capture winning stage patterns as templates with explicit inputs/outputs.
- Reuse approved templates by default on new runs in the same category.
- Promote revisions when measured outcomes improve (higher conversion, lower revision count, faster cycle time).
- Keep rollback-ready history for template versions; never overwrite without traceability.

## Production Manifest

> **This is a reference menu of possible artifacts, not a mandatory checklist.** The agent selects what's relevant for this specific product and ICP. Not every product needs every artifact listed below. During Strategy, the agent declares which outputs are expected for this run.

A complete ship run generates concrete artifacts organized under `runs/{ticket}/`. What "done" looks like varies by product.

```
runs/{ticket}/
├── intake/
│   └── product-brief.md
├── validate/
│   ├── validation-report.md
│   ├── icp.md
│   └── voc-bank.md
├── strategy/
│   └── ship-plan.md
├── awareness/
│   ├── landing-page/               (deployable Next.js or HTML site, live URL)
│   ├── blog-posts/                 (5-7 articles, PR-ready frontmatter + markdown)
│   ├── social/                     (per-platform content packs)
│   │   ├── twitter-threads/        (5-7 tweet threads per content piece)
│   │   ├── linkedin-posts/         (long-form professional posts)
│   │   ├── reddit-posts/           (per-subreddit tone-adapted versions)
│   │   ├── ig-carousels/           (10-slide decks per piece, images generated)
│   │   └── video-scripts/          (full scripts + storyboards)
│   ├── seo/                        (comparison pages, schema JSON-LD, sitemap)
│   ├── assets/
│   │   ├── og-images/              (1200×630, one per page/article)
│   │   ├── hero-images/            (1200×628, one per blog post)
│   │   ├── screenshots/            (real product captures via browser automation)
│   │   ├── demo-gifs/              (recorded product flows)
│   │   └── logo-variants/          (light, dark, icon, favicon)
│   └── video/                      (scripts + storyboard PDFs + AI first-pass video files)
├── lead-capture/
│   ├── offer-stack.md              (Hormozi-framework copy, value stack, guarantee)
│   ├── lead-magnets/               (styled PDFs, guides, checklists — downloadable)
│   ├── funnels/
│   │   ├── utm-links.csv           (all channels × content pieces × CTAs)
│   │   └── funnel-map.md           (entry points → capture mechanisms, documented)
│   └── analytics/
│       ├── ga4-events.md           (event schema, configured and verified)
│       └── tracking-test-log.md    (end-to-end verification results)
├── nurture/
│   ├── email-sequence/             (7 emails, HTML + markdown, imported to provider)
│   │   ├── email-1-welcome.*
│   │   ├── email-2-origin-story.*
│   │   ├── email-3-tutorial.*
│   │   ├── email-4-social-proof.*
│   │   ├── email-5-objection-killer.*
│   │   ├── email-6-urgency.*
│   │   └── email-7-last-call.*
│   ├── content-drip/
│   │   ├── schedule.csv            (14 days × all platforms, ready to publish)
│   │   └── images/                 (generated images per post)
│   └── retargeting/
│       └── audience-definitions.md (Meta/Google audience segments)
├── closing/
│   ├── stripe-config/
│   │   ├── products.json           (Stripe product IDs)
│   │   ├── prices.json             (price objects per tier/interval)
│   │   └── coupons.json            (coupon codes, discounts, limits)
│   ├── pricing-page/               (deployable component, tested end-to-end)
│   ├── objection-handling/
│   │   ├── faq.md                  (top 5 objections + responses, landing page format)
│   │   ├── email-copy.md           (objection responses formatted for email)
│   │   ├── sales-deck-slides.md    (one-line objection + response, slide format)
│   │   └── roi-calculator/         (interactive web component)
│   └── post-purchase/
│       ├── onboarding-email-1.*    (immediate — first value)
│       ├── check-in-email-2.*      (Day 3)
│       ├── testimonial-ask-3.*     (Day 7)
│       ├── referral-invite-4.*     (Day 14)
│       └── retention-email-5.*     (Day 30)
├── launch/
│   ├── pre-launch-checklist.md
│   ├── launch-day-playbook.md
│   └── post-launch-calendar.md
└── measure/
    ├── targets.md
    └── reports/
        ├── phase-1-daily/
        └── phase-2-weekly/
```

Manifest items are produced incrementally. Deliverables can move live through Stage 9 once verified; Gate-L confirms coordinated scale readiness, not first publication of every artifact.

---

## Tool Stack for Autonomous Production

Every production task maps to a specific tool or pipeline. This is how the engine does the work, not just what it decides to do.

| Production Task | Tool | How |
|----------------|------|-----|
| Landing pages | `create-app` skill | Template-driven generation seeded with ICP + VoC → deploy to `{product}.max-techera.[REDACTED_PROJECT].app` for live review |
| Blog posts | Sub-agents + `humanize` skill | Parallel sub-agents (`sessions_spawn`) generate 5-7 articles simultaneously; all copy humanized via `channel=blog` before output; delivered as PR-ready frontmatter + markdown |
| Images (hero, OG, social) | `content-image` skill (Gemini-first) | Batch generation per content piece; platform-specific sizing logic; branded style seed from Product Brief; mockup workflow prefers real screenshots as canonical. |
| Product screenshots | `browser` tool | Automated navigation of live product; snapshot + screenshot at 1440px desktop + 375px mobile; captures polished state of core screens |
| Demo GIFs | `browser` tool + screen recording | Records actual product flows (signup → first value); auto-looping GIF output |
| Video voiceover | `sag` skill (ElevenLabs TTS) | Generate AI first-pass narration via `ELEVENLABS_API_KEY`; talent re-records final version over existing audio track |
| Video frames/clips | `video-frames` skill | Extract frames and clips from existing videos with ffmpeg for repurposing into social content |
| Audio transcription | `openai-whisper-api` skill | Transcribe recorded videos/audio via OpenAI Whisper for captions, blog posts, subtitle generation |
| Email sequences | Email automation tool (default: MailerLite API, alternatives: any tool supporting groups, automations, and analytics) | Create groups, forms, automations programmatically via API; test email sent and logged before launch |
| Payment setup | Payment processing (default: Stripe API via `stripe.py`, alternatives: any tool supporting products, prices, checkout, and portal) | Products, prices, checkout URLs, coupons, Customer Portal — all provisioned via API, nothing manual |
| Analytics collection | Web analytics (default: `tools/analytics-collector.py` for GA4/GSC/Meta, alternatives: any tool providing pageviews, sessions, conversions) | Pulls analytics simultaneously; normalized for reporting |
| Analytics reporting | `brand-report` skill | Comprehensive cross-channel report across data sources; run on Phase 1 daily, Phase 2 weekly cadence |
| Analytics setup | Web analytics + UTM generation | Custom event schema configured; UTM links batch-generated; end-to-end verification via `browser` tool |
| Instagram publishing | `tools/lib/meta_api.py` | Publish posts, reels, stories to @[REDACTED_HANDLE] AFTER Max enables publishing; pull insights (reach, engagement, saves) |
| Content pipeline | `tools/content-engine.py` | Queue, plan-week, today, script, batch-prep, posted, stats, backlog commands. Manages full content lifecycle. |
| Research (market/pain) | `tools/research.py` | `--deep` for Perplexity sonar research; `--x-only` for X/Twitter via xAI; `--social` for multi-source social signals |
| Deep research (async/overnight) | `gemini-deep-research` skill | Full market/competitor research via Gemini's research agent; async, no Perplexity/xAI credits needed; ideal for VALIDATE stage |
| Parallel cheap execution | `swarm` skill | Gemini Flash workers for parallel stage execution; 200x cheaper than Opus; use for the 4 parallel stages in PARALLEL state |
| Overnight autonomous runs | `agent-autonomy-kit` skill | No-gate blocking; self-continuation for unattended runs; wrap VALIDATE and STRATEGY stage sub-agents |
| Web research | `web_search` (Brave API) + `search` skill | Targeted Reddit/HN searches, competitor pages, keyword research; `search` skill does parallel Perplexity+Brave+xAI fan-out |
| CRM / relationships | `tools/crm.py` | Track contacts, follow-ups, interactions from launch outreach |
| Project tracking | `tools/linear.py` | Create/update Linear tickets per workstream (NEO team). One ticket per parallel agent. |
| Scheduling / crons | `cron` tool | Schedule measurement pulls, content publishing cadence, post-purchase sequence triggers |
| Notifications | `message` tool + `tools/lib/notify.py` | Send Slack DMs/channel messages at stage completions, approval gates, blockers, milestone alerts |
| Calendar scheduling | `tools/gcal.py` | Block launch-day time, schedule talent recording sessions, set review deadlines |
| PDFs | Markdown → PDF pipeline | Lead magnets, guides, checklists — written as markdown, rendered to styled PDF, hosted at direct URL |
| SEO markup | Structured data generation | FAQ schema (JSON-LD), Product schema, Organization schema — generated and embedded in HTML `<head>` |
| Copy humanization | `humanize` skill | ALL copy — landing pages, emails, social, blog posts, video scripts — passes through before any output. Channels: `channel=twitter|blog|linkedin|instagram`. No exceptions. |
| Diagrams | Mermaid → SVG | Architecture diagrams, workflow comparisons, product flow diagrams — source in Mermaid DSL, rendered to polished SVG |
| Social images | `content-image` skill (Gemini-first) + templating | Platform-specific sizing (1200×630, 1080×1080, 1080×1920, 1280×720); brand-consistent style across all variants |
| Pricing page | `create-app` skill + deployable component | Monthly/annual toggle, Stripe checkout integration, mobile-responsive — generated, tested via `browser` tool, deployed |
| ROI calculator | Interactive web component | Inputs from ICP pain data; simple, honest math; embedded in landing page or standalone `/roi` route |
| GitHub releases | `github` skill (`gh` CLI) | Tag releases, manage repos, create PRs for landing page and content deployments — authenticated as [REDACTED_HANDLE] |

The default posture is: if it can be generated, it gets generated. If it can be deployed, it gets deployed. If it can be verified, it gets verified. Max sees finished work, not proposals.

---

## Available Services Reference

Quick-reference table of every service available on this instance and where it fits in the pipeline.

| Tool / Service | What it does | Pipeline stage(s) |
|---------------|-------------|-------------------|
| `tools/research.py --deep` | Perplexity sonar deep research; comprehensive market/competitor intel | Validate, Strategy |
| `tools/research.py --social` | Multi-source social signal research (Perplexity + xAI simultaneously); pain thread mining | Validate, Awareness |
| `tools/research.py --x-only` | X/Twitter search via xAI/Grok API; trending complaints, viral hooks | Validate, Awareness |
| `search` skill | Multi-source social media research (Perplexity + xAI); replaces social-research.py | Validate |
| `web_search` (Brave API) | Web search for Reddit/HN threads, competitor pages, keyword research | Validate, Strategy, All |
| `web_fetch` | Extract readable content from URLs; competitor pages, review sites | Validate, Strategy |
| `humanize` skill | AI content humanizer → human-sounding copy. Channels: `twitter|blog|linkedin|instagram` | All content output stages |
| `tools/content-engine.py` | Content pipeline: queue/add/plan-week/today/script/batch-prep/posted/stats/backlog | Awareness, Nurture, Launch |
| `tools/content-engine.py` | Content pipeline management (pitch/posted/queue/add/plan-week/today/script/batch-prep/stats/backlog) | Awareness, Launch |
| `daily-content-brief` skill | Daily content brief generation | Launch, Measure |
| `content-image` skill | Batch image generation via Gemini. Gallery + index.html output. | Awareness (all visual assets) |
| `video-frames` skill | Extract frames/clips from videos with ffmpeg | Awareness (video repurposing) |
| `openai-whisper-api` skill | Transcribe audio/video via OpenAI Whisper | Awareness (captions, blog from video) |
| `sag` skill (ElevenLabs TTS) | Voice generation via `ELEVENLABS_API_KEY`; AI voiceover for video first-pass | Awareness (video production) |
| `tts` tool | Quick text-to-speech drafts | Awareness (voiceover drafts) |
| `ffmpeg` | Video/audio processing, frame extraction, GIF generation | Awareness (video + demo GIFs) |
| `create-app` skill | Deploy static HTML apps → `<app-name>.max-techera.[REDACTED_PROJECT].app` | Awareness (landing page), Closing (pricing page) |
| `coding-agent` skill | Spawn Claude Code for building features, interactive components | Awareness, Closing (ROI calc, custom components) |
| `github` skill (`gh` CLI) | GitHub CLI authenticated as [REDACTED_HANDLE] — PRs, releases, repos | All deployment stages |
| `browser` tool | Full browser control: navigate, click, screenshot, snapshot | Validate (competitor research), Awareness (screenshots), Lead Capture (tracking verify), Closing (checkout test) |
| `tools/linear.py` | Linear API — create/update/search issues. Teams: MAX (strategic), NEO (agent ops) | All stages (workstream tracking) |
| `orchestrator` skill | Process tasks from kanban board | Strategy, Parallel |
| `sessions_spawn` | Spawn parallel sub-agents — 4+ simultaneously | Parallel Execution (one per workstream) |
| `message` tool (Slack) | Send/read/react/pin messages in Slack channels and DMs | Approval gates, milestone alerts, blockers |
| `tools/lib/notify.py` | Unified notification library (critical/channel/buttons) | Approval gates, blockers |
| `tools/analytics-collector.py` | Collect GA4, GSC, Meta analytics simultaneously | Lead Capture (setup verify), Measure (daily/weekly pulls) |
| `brand-report` skill | Cross-channel analytics report across 7 data sources | Measure (Phase 1 + Phase 2 reports) |
| `tools/lib/analytics_helpers.py` | Date ranges, comparisons, analytics helpers | Measure |
| `tools/lib/meta_api.py` | Full Meta API: IG publish (posts/reels/stories), insights, ads | Awareness (IG distribution), Launch (Wave 4), Measure (IG insights) |
| `tools/gcal.py` | Google Calendar — today/week/free/block/create/update | Strategy (sprint planning), Launch (L-Day block) |
| `tools/gdrive.py` | Google Drive operations | Awareness (asset storage), Nurture (lead magnet hosting) |
| `tools/crm.py` | CRM — contacts, follow-ups, interactions | Launch (supporter outreach), Post-launch (relationship tracking) |
| `cron` tool | Schedule recurring or one-shot jobs | Launch (measurement cadence), Nurture (content drip), Measure (daily/weekly reports) |
| `OPENAI_API_KEY` | GPT-4o (copy generation, research), Whisper (transcription) | AI text + transcription tasks |
| `ANTHROPIC_API_KEY` | Claude Sonnet/Opus — sub-agents, long-form reasoning | All sub-agent workstreams |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS — voice generation | Awareness (video voiceover) |
| `BRAVE_API_KEY` | Brave Search API — powers `web_search` tool | Validate, Strategy, All research |
| `GOOGLE_ACCESS_TOKEN` | Google OAuth — GA4, GSC, Calendar, Drive, Gmail | Analytics, Calendar, Drive |
| Meta API tokens | Instagram/Facebook publishing and insights | Awareness (IG), Measure (IG insights) |
| `LINEAR_ACCESS_TOKEN` | Linear project management API | All stages (workstream tickets) |

---

## Notification Philosophy

**Tell Max about:**
- Stage completions (one-line summary)
- Decisions needed (approval gates)
- Blockers that require his input
- Talent tickets ready for action
- Measure reports
- Kills and final verdicts

**Don't tell Max about:**
- Internal progress within a stage
- Agent-to-agent collaboration details
- Research in progress
- Intermediate findings (save for the report)
- Internal state changes

**Daily digest (only if active runs exist):** One message with one line per active run: what stage, any blockers, any talent tickets pending.

---

---

## Autonomy Stack — Overnight Runs

Ship Engine is designed to run unattended overnight. These three skills enable autonomous execution:

| Skill | Role in Ship Engine | When to Use |
|-------|-------------------|-------------|
| **swarm** (`skills/swarm/skill/SKILL.md`) | Parallel stage execution. Spawn Gemini Flash workers for the 4 parallel stages (Awareness / Lead Capture / Nurture / Closing) simultaneously. 200x cheaper than Opus for mechanical tasks. | STRATEGY → PARALLEL transition. Each of the 4 workstreams = 1 swarm worker. |
| **agent-autonomy-kit** (`skills/agent-autonomy-kit/SKILL.md`) | No-gate blocking. Lets the engine keep working through soft blockers without waiting for a heartbeat. Handles self-continuation logic so overnight runs don't stall. | Wrap any stage sub-agent that runs unattended. Especially VALIDATE and STRATEGY. |
| **gemini-deep-research** (`skills/gemini-deep-research/SKILL.md`) | Deep multi-source market research via Gemini's built-in research agent. Uses for VALIDATE stage to build ICP, pain analysis, competitor landscape. Runs fully async — doesn't need xAI or Perplexity credits. | INTAKE → VALIDATE. Replaces `tools/research.py --deep` when Perplexity/xAI credits are exhausted. |

### Overnight Run Checklist

Before triggering an overnight run:
1. ✅ Ship run initialized (Linear parent ticket labeled `ship-engine` + stage tickets created)
2. ✅ Strategy or Validate stage is the entry point
3. ✅ Sub-agents for parallel stages use `swarm` skill
4. ✅ Each stage agent is wrapped with `agent-autonomy-kit` for no-gate blocking
5. ✅ All agents report to `neo-ship-engine` (-[REDACTED_PHONE]) on completion
6. ✅ Budget approved in `strategy.budget` blackboard key (unless only running Validation Probe under policy)
7. ✅ Critic agent spawned with full run context before every gate

### Tool Selection for Autonomous Stages

| Research Task | Autonomous Tool (overnight) | Interactive Tool (live) |
|--------------|---------------------------|------------------------|
| Market research | `gemini-deep-research` (async, no credits needed) | `tools/research.py --deep` (Perplexity) |
| Fan-out parallel tasks | `swarm` (Gemini Flash, cheap) | `sessions_spawn` (Sonnet) |
| Blocker handling | `agent-autonomy-kit` (self-continue) | Wait for Max input |
| Memory across stages | `SESSION-STATE.md` + `memory_search` | Same |

---

## What Ship Engine Does NOT Do

- **Build the CORE product** — the app itself must exist. But the engine builds everything AROUND it: landing pages, content, email sequences, payment flows, analytics. The product is the prerequisite; everything else is the engine's responsibility.
- **Bypass risk policy for publishing** — low-risk can auto-canary; high-risk requires explicit Max approval before live
- **Spend money outside the Validation Probe policy without approval** — Strategy budget required
- **Make kill/continue decisions** — it recommends with data, Max decides
- **Replace Max's voice** — content drafted in Max's style, he reviews before it goes out
- **Work in isolation** — agents collaborate continuously, not in silos
