---
name: ship-lead-capture-supervisor
description: Own Lead Capture workstream deliverables (Stage 5B). Produces offer stack, lead magnet, forms/list wiring, UTMs, and tracking verification.
---

# Ship Lead Capture Supervisor

Own Lead Capture deliverables during Stage 5 (Parallel Execution).

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/ship-engine/WORKFLOW.md`:
- `Gate Prefill Requirement (Max-Facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `strategy.ship_plan` (offer + channel plan)
- `validate.icp`
- Linear Lead Capture ticket

## Deliverables (Required)
- [ ] Offer stack (copy + structure) linked
- [ ] Lead magnet artifact (downloadable or product-based) linked
- [ ] Capture mechanism wired (forms + list/group + delivery) linked
- [ ] UTM link set created and linked
- [ ] End-to-end tracking test log linked

## Verification
- Signup flow works end-to-end (form -> list -> delivery)
- UTMs resolve correctly and are used in awareness CTAs
- Tracking events verified (logged evidence)
- In `production`, each deliverable is critic-verified (`PASS`) before moving to `verified`/`live`

## Quality Gate (PASS/REVISE)
- PASS: offer + lead magnet + wiring + UTMs + tracking evidence are linked and critic-verified (`PASS` in `production`)
- REVISE: any wiring/test fails, artifacts are missing, or critic verdict `REVISE`

## Writeback Contract
- Blackboard keys:
  - `lead_capture.offer_stack`
  - `lead_capture.lead_magnet`
  - `lead_capture.capture_wiring`
  - `lead_capture.utm_links`
  - `lead_capture.tracking_test_log`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - On each meaningful update, post `status_summary` + `next_steps`
  - For high-risk deliverables, post a prefilled Decision Packet before `live`

## Delegation Map
- Offer: `content-offer` + `content-copy`
- Forms: `content-form`
- Lead magnet assets: `content-offer` + `content-page` + `content-image`

## Failure Policy
- If provider APIs are blocked: produce the artifacts + a manual setup checklist and mark execution as blocked with exact missing access

## Critic Invocation (Required in `production`, per deliverable)
Before advancing any deliverable from `in_production` → `verified`:
1. Spawn `ship-critic` with `check_type=deliverable`, `deliverable_key=lead_capture.{artifact}`
2. Pass context: `intake.product_brief` summary + `validate.icp` VoC phrases + `strategy.ship_plan` offer + the deliverable artifact link/summary
3. Verdict:
   - **PASS** → advance to `verified`; record `critic_verdict=PASS` and `critic_evidence` link in deliverable state
   - **REVISE** → keep in `in_production`; post revision requests on the Lead Capture ticket
4. Write `critic.lead_capture.{artifact}` blackboard key with `verdict`, `comment_url`, `checked_at`

## Done When
- Deliverables exist, are linked, critic-verified in `production`, and verification evidence is recorded
