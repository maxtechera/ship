---
name: ship-closing-supervisor
description: Own Closing workstream deliverables (Stage 5D). Produces pricing/checkout readiness, objection handling assets, and post-purchase sequence requirements.
---

# Ship Closing Supervisor

Own Closing deliverables during Stage 5 (Parallel Execution).

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/engine/WORKFLOW.md`:
- `Gate Prefill Requirement (owner-facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `strategy.ship_plan` (pricing hypothesis + guarantee)
- `validate.icp` (objections)
- Linear Closing ticket

## Deliverables (Required)
- [ ] Pricing page / checkout flow artifact linked (or deployment URL)
- [ ] Objection handling pack linked (FAQ + email responses + deck bullets)
- [ ] Post-purchase email sequence outline linked
- [ ] Checkout verification evidence linked (test flow)

## Verification
- Checkout flow tested end-to-end (evidence logged)
- Objection pack uses ICP language and matches offer
- Pricing/guarantee terms consistent across assets
- In `production`, each deliverable is critic-verified (`PASS`) before moving to `verified`/`live`

## Quality Gate (PASS/REVISE)
- PASS: checkout artifacts + objection pack + verification evidence are linked and critic-verified (`PASS` in `production`)
- REVISE: inconsistent terms, missing proof, untested flow, or critic verdict `REVISE`

## Writeback Contract
- Blackboard keys:
  - `closing.pricing_page`
  - `closing.checkout`
  - `closing.objections`
  - `closing.post_purchase`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - On each meaningful update, post `status_summary` + `next_steps`
  - For high-risk deliverables, post a prefilled Decision Packet before `live`

## Delegation Map
- Pricing/offer copy: `content-offer` + `content-copy`
- Pricing page UI: `create-app` + `ui-design` (as needed)
- Visuals: `content-image`

## Failure Policy
- If payment provider access is missing: ship the full set of artifacts + manual provisioning checklist; mark execution blocked

## Critic Invocation (Required in `production`, per deliverable)
Before advancing any deliverable from `in_production` → `verified`:
1. Spawn `ship-critic` with `check_type=deliverable`, `deliverable_key=closing.{artifact}`
2. Pass context: `validate.icp` VoC + objections + `strategy.ship_plan` pricing/offer + the deliverable artifact link/summary
3. Verdict:
   - **PASS** → advance to `verified`; record `critic_verdict=PASS` and `critic_evidence` link in deliverable state
   - **REVISE** → keep in `in_production`; post revision requests on the Closing ticket
4. Write `critic.closing.{artifact}` blackboard key with `verdict`, `comment_url`, `checked_at`

## Done When
- Deliverables exist, are linked, critic-verified in `production`, and verification evidence is recorded
