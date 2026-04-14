---
name: ship-engine-supervisor
description: Always-on Ship Engine control loop. On wake (webhook/cron/manual), reconciles Ship Engine run tickets, delegates work to stage supervisor skills, verifies deliverables, and keeps the run moving forever.
user-invocable: false
---

# Ship Engine Supervisor (Always-On)

Ship Engine is skills-first. There is no CLI orchestrator.

This supervisor runs as an infinite control loop across wake events:
- Webhook wakes for Linear ticket events
- Cron wakes for reconciliation/backfill
- Manual wakes for “run now”

Each wake executes ONE safe cycle (bounded work) and then exits.

## Inputs
- Linear is the system of record for work: ticket descriptions + comments + attachments
- Orchestrator contract: `https://github.com/maxtechera/orchestrator/blob/main/SKILL.md`
- Canonical workflow: `engine/WORKFLOW.md`
- Named team: `runs/{run-id}/team.json` (created at run start, read on every wake)

## Shared Contracts (DRY)
Use canonical definitions from `engine/WORKFLOW.md`:
- `Gate Prefill Requirement (owner-facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

Do not redefine decision packet shape per supervisor; reuse the canonical template.

## Critic Agent (Required in `production`)
Skill: `supervisors/critic/SKILL.md`

Spawn the critic as a separate sub-agent (not inline) before every hard gate and before any deliverable advances to `verified` in `production`. The critic must return a verdict before the Decision Packet is posted or the deliverable state is advanced.

**Auto-invoke at:**
- Before posting Gate-V Decision Packet → owning supervisor produces Gaps Doc first, sends to critic via `SendMessage to="critic"`, waits for verdict
- Before posting Gate-S Decision Packet → owning supervisor produces Gaps Doc first, sends to critic via `SendMessage to="critic"`, waits for verdict
- Before posting Gate-L Decision Packet → owning supervisor produces Gaps Doc first, sends to critic via `SendMessage to="critic"`, waits for verdict
- Before posting Final Social Push approval package → `ship-launch-supervisor` triggers
- Before any deliverable moves from `in_production` → `verified` (all parallel supervisors)

**On-demand:** Any supervisor or the owner can request a critic review mid-run. Use the same spawn pattern; result is advisory if `run_mode=iteration`.

**Stale verdict rule:** If deliverables were updated after the last critic run (check `checked_at` in `critic.{scope}` blackboard key), re-run the critic before advancing.

**human override:** If the critic returns `REVISE` at a hard gate, the supervisor waits for either:
1. Stage supervisor fixes the flagged issues and re-runs the critic (preferred), or
2. Owner posts `override: approve` on the gate ticket (records override in blackboard)

The supervisor must never silently advance past a `REVISE` verdict without one of the above.

## Core Loop (One Cycle)
1. Find active Ship Engine runs (Linear tickets labeled `ship-engine`)
2. For each run, read `runs/{run-id}/team.json` to get named agent roster. If team not yet created, create it now (see Named Agent Team in `engine/WORKFLOW.md`).
3. Identify the next actionable stage ticket(s)
4. Enforce the orchestrator contract on that ticket (Inputs/Deliverables/Verification/Artifacts)
   - Intake research-first enforcement:
     - Stage 1 must include `intake.product_brief`, `intake.interview`, and `intake.research_kickoff`
     - Validate cannot be treated as actionable until intake research kickoff is linked
5. Delegate to named agent via `SendMessage` first; fall back to stage supervisor skill if agent is not live:
   - `ship-intake-supervisor`
   - `ship-validate-supervisor`
   - `ship-strategy-supervisor`
   - `ship-awareness-supervisor`
   - `ship-lead-capture-supervisor`
   - `ship-nurture-supervisor`
   - `ship-closing-supervisor`
   - `ship-launch-supervisor`
   - `ship-measure-supervisor`
5. In parallel lanes (Awareness + Measure), allow Content Engine collaboration:
   - Draft generation, waterfall bundling, and draft autoscheduling are delegated to Content Engine skills
   - Measurement feedback events can be delegated to Content Engine measurement
5. **Critic Agent gate** — before advancing any deliverable to `verified` or any pipeline gate, invoke `ship-critic`:
   - Deliverable check: invoke skill `ship-critic` using args `--ticket <TICKET-XXX> --stage <stage> --deliverable <type> --run-id <RUN-XXX>`
   - Gate check: invoke skill `ship-critic` using args `--ticket <TICKET-XXX> --gate <gate-v|gate-s|gate-l> --run-id <RUN-XXX>`
   - Cross-check (after parallel workstreams): invoke skill `ship-critic` using args `--run-id <RUN-XXX> --cross-check`
   - **Exit code 0 = PASS** → advance; **exit code 1 = REVISE** → stay in `in_production`, fix list in Linear comment
   - The owner can override a REVISE at gate level only via `decision: approve` + `override_reason` comment
   - Full spec: `supervisors/critic/SKILL.md`
6. Verify deliverables exist, are linked in Linear, and are critic-verified in `production`
6. Reconcile deliverable cards through Stage 9 lifecycle (draft scheduling, approvals when required, live, measurement evidence)
7. Update ticket state to `In Review` or `Done` only when verification evidence exists
8. When human validation is required (hard gates or high-risk deliverables):
   a. Ensure critic has run (spawn `ship-critic` if verdict missing or stale)
   b. If critic PASS (or REVISE with human override recorded): pre-fill the decision packet and notify the run owner
   c. If critic REVISE (no override): do NOT post the decision packet; post revision requests instead
9. Ensure each meaningful status change writes `status_summary` and `next_steps` to Linear/blackboard

## Guardrails
- Never advance past hard gates without owner decision (Post-Validation, Post-Strategy Lock, Pre-Launch)
- Never start Validate without intake interview + research kickoff artifacts
- Never fabricate research evidence
- Never mark a deliverable `verified` (or move it to live) in `production` without a critic `PASS`
- Never move high-risk deliverables to `live` without explicit owner approval
- Draft autoscheduling is allowed; auto-publishing to owner social accounts is not
- **PR Gating**: Code-related deliverables must be submitted via PR. The stage supervisor must create the PR and use workflow states only (no `blocked-by-owner` label). If waiting on the owner, move to `Blocked by Owner` state with explicit unblock requirements.
- **Merge-First Verification**: Verification evidence must be collected ONLY AFTER the PR is merged by the owner. A merged PR triggers transition to `QA`.

- If no actionable work exists, exit without doing LLM-heavy work

## Fastpath
- Before spawning any heavy sub-agent work, run a cheap actionability check (ticket exists, Inputs present, deliverables missing)
- Prefer “one ticket per wake” to avoid overnight spam

## Output
- Updated Linear tickets with linked artifacts
- Blackboard keys written by stage supervisors (as documented in `WORKFLOW.md`)
