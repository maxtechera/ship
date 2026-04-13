---
name: ship-launch-supervisor
description: Own Stages 6-7 (Pre-Launch gate + Launch execution). Produces readiness checklist, requests Max approval, and coordinates multi-channel launch artifacts.
---

# Ship Launch Supervisor

Own Stage 6 (Pre-Launch approval gate) and Stage 7 (LAUNCH).

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/ship-engine/WORKFLOW.md`:
- `Gate Prefill Requirement (Max-Facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- Parallel workstream artifacts:
  - `awareness.*`
  - `lead_capture.*`
  - `nurture.*`
  - `closing.*`
- Linear Stage 6 + Stage 7 tickets

## Deliverables (Required)
- [ ] Pre-launch readiness checklist linked (one line per workstream with artifact links)
- [ ] Max approval request posted with explicit decision options
- [ ] Launch-day playbook linked
- [ ] Directory submission list + statuses linked
- [ ] Scheduled/publish-ready content pack linked
- [ ] Final social push package linked with explicit Max decision request (`Approve Push` / `Revise Package` / `Hold Push`)

## Verification
- All referenced artifacts resolve (no missing links)
- Launch CTAs route to capture mechanisms (UTMs + forms)
- In `production`, launch artifacts are critic-verified (`PASS`) before marking `verified`/`live`
- Stage 6 and Final Social Push requests are posted as prefilled Decision Packets
- No broad social publishing happens before final social push package approval

## Quality Gate (PASS/REVISE)
- PASS: readiness checklist is complete, critic-verified in `production`, and approval decisions are recorded via prefilled Decision Packets
- REVISE: missing artifacts, broken links, capture path not wired, or critic verdict `REVISE`

## Writeback Contract
- Blackboard keys:
  - `launch.pre_launch_checklist`
  - `launch.playbook`
  - `launch.approval_status`
  - `launch.social_push_package`
  - `launch.social_push_approval`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - On each meaningful update, post `status_summary` + `next_steps`
  - Stage 6 gate message is a prefilled Decision Packet (canonical template) with links + decision options
  - Stage 7 includes a dedicated prefilled Final Social Push Decision Packet with decision outcome
  - Stage 7 Artifacts list includes final publish links (when live)

## Delegation Map
- Distribution packaging + scheduling: `content-distribution`
- Copy polish: `content-copy`
- Visual pack updates: `content-image`

## Failure Policy
- If any parallel artifact is missing: do not request approval; post a blocker summary with exact missing deliverables

## Critic Invocation (Required in `production`)

**Gate-L (Pre-Launch):**
1. Assemble context bundle: `intake.product_brief` + `validate.icp` + `strategy.ship_plan` + summary of all parallel artifacts (`awareness.*`, `lead_capture.*`, `nurture.*`, `closing.*`)
2. Spawn `ship-critic` with `check_type=gate`, `gate=gate-l`
3. Critic runs per-deliverable rubric + full cross-consistency check (ICP → all surfaces)
4. Wait for verdict:
   - **PASS** → post Gate-L Decision Packet
   - **REVISE** → route revision requests to affected supervisor(s); do NOT post gate decision
5. Record `critic.gate-l` in blackboard

**Final Social Push:**
1. Spawn `ship-critic` with `check_type=gate`, `gate=social-push` before posting social push approval package
2. Same PASS/REVISE → proceed/block pattern
3. Record `critic.social-push` in blackboard

**Per-deliverable (Stage 7 artifacts):**
- Before marking any Stage 7 artifact `verified`: spawn critic with `check_type=deliverable`, `deliverable_key=launch.{artifact}`

**Max override:** `override: approve` on gate ticket unlocks either gate; record in blackboard.

## Done When
- Stage 6 approval is obtained, critic has returned PASS for Gate-L and social push (or Max override recorded)
- Final social push package is explicitly approved, and Stage 7 launch artifacts are critic-verified in `production` and ready/live with links recorded
