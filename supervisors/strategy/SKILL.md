---
name: ship-strategy-supervisor
description: Own Stage 4 (Strategy). Converts Validate outputs into an executable Ship Plan with deliverable contracts for the parallel workstreams.
---

# Ship Strategy Supervisor

Own Stage 4 (STRATEGY). Produce the Ship Plan that the 4 parallel workstreams execute.

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/engine/WORKFLOW.md`:
- `Gate Prefill Requirement (Max-Facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `validate.validation_report`
- `validate.icp`
- Linear Stage 4 ticket

## Deliverables (Required)
- [ ] Ship Plan doc linked in Linear
- [ ] Parallel workstream tickets created/updated with Inputs/Deliverables/Verification/Artifacts
- [ ] Budget + spend policy recorded
- [ ] Strategy Lock Pack posted as a prefilled Decision Packet for Max approval (to prevent premature fanout)
- [ ] Persona Callout Pack linked (library + Meta playbook + Meta pack)
- [ ] Blackboard key `strategy.ship_plan` written

## Ship Plan (minimum sections)
- Positioning: one-liner, value prop, differentiation
- Offer + pricing hypothesis
- Channel priorities (primary/secondary)
- Content strategy mapped to pain themes (VoC-driven)
- Distribution plan (who/where/how often)
- Persona callout strategy: avatar band (3-12 default), hook families, proof stack, CTA families
- Paid lane split: `paid.prospecting` vs `paid.retargeting` mapped to shared hook IDs
- Success targets (visitor -> lead -> activation -> revenue)
- Dependencies for parallel workstreams

## Verification
- Every parallel workstream has a concrete deliverables checklist
- Channel plan matches ICP channel map
- Targets are measurable (numbers + definitions)
- Persona Callout Pack artifacts are linked from Strategy ticket
- Paid lane split is explicit and tied to hook IDs
- In `production`, Ship Plan is critic-verified (`PASS`) before marking `verified`

## Quality Gate (PASS/REVISE)
- PASS: Ship Plan is linked, critic-verified (`PASS` in `production`), parallel tickets are executable, budget/targets are recorded, and Persona Callout Pack is attached
- REVISE: missing deliverable contracts, channel mismatch, unverifiable targets, missing persona-pack artifacts, or critic verdict `REVISE`

## Writeback Contract
- Blackboard:
  - `strategy.ship_plan`
  - `strategy.budget`
  - `strategy.targets`
  - `strategy.persona_callouts_pack`
  - `strategy.voc_pain_points`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - Stage 4 ticket updated; links in Artifacts
  - Stage 4 comments include `status_summary` + `next_steps` on meaningful updates
  - Strategy Lock decision is posted as a prefilled Decision Packet (canonical template)
  - Parallel tickets created or confirmed

## Delegation Map
- Offer shaping: `content-offer`
- Distribution plan draft: `content-distribution`
- Copy polish: `content-copy`

## Failure Policy
- If Validate is weak: block Strategy completion until Validate artifacts are revised (REVISE)

## Critic Invocation (Required in `production`)
Before posting the Gate-S (Strategy Lock) Decision Packet:
1. Assemble context bundle: `intake.product_brief` (summary) + `validate.icp` (VoC phrases) + `strategy.ship_plan` (positioning, offer, channels)
2. Spawn `ship-critic` with `check_type=gate`, `gate=gate-s`
3. Critic runs stage rubric + cross-consistency check (ICP → Strategy)
4. Wait for verdict:
   - **PASS** → post Strategy Lock Decision Packet
   - **REVISE** → post revision requests; do NOT post Decision Packet; fix and re-run critic
5. Record `critic.gate-s` in blackboard with `verdict`, `verdict_summary`, `comment_url`, `checked_at`
6. On Max override (`override: approve`): record override; post Decision Packet

## Done When
- Ship Plan exists, is linked, critic has returned PASS (or Max override recorded) for Gate-S
- Strategy Lock Pack is posted, and Persona Callout Pack artifacts are attached for Max's Proceed/Revise decision
