---
name: ship-measure-supervisor
description: Own Stage 8 (Measure). Produces performance reports, compares against targets, and writes next-iteration actions as deliverable tickets.
---

# Ship Measure Supervisor

Own Stage 8 (MEASURE). Measurement is a deliverable, not a dashboard screenshot.

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/engine/WORKFLOW.md`:
- `Gate Prefill Requirement (Max-Facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `strategy.targets`
- Live URLs + UTMs
- Access to analytics sources (GA4/GSC/Meta/etc)
- Linear Measure ticket

## Deliverables (Required)
- [ ] Phase report linked (daily/weekly depending on run phase)
- [ ] KPI deltas vs targets recorded
- [ ] Reporting split table recorded (`organic`, `paid.prospecting`, `paid.retargeting`)
- [ ] Persona callouts performance logged with kill/iterate/scale decision per hook family
- [ ] Next actions created as tickets with Inputs/Deliverables/Verification
- [ ] Blackboard key `measure.report` written
- [ ] Blackboard key `measure.feedback_events` written (asset-level iteration actions)

## Verification
- Numbers include date range and source
- Attribution caveats are stated (UTMs missing, small sample, etc.)
- Next actions are executable and mapped to owners
- Organic vs paid and paid prospecting vs paid retargeting are reported separately
- Winning/losing assets are traceable to persona hook IDs
- In `production`, reports/recommendations are critic-verified (`PASS`) before marking `verified`

## Quality Gate (PASS/REVISE)
- PASS: report is linked with sources, reporting split is complete, persona hook outcomes are logged, next actions are executable, and critic verdict is `PASS` in `production`
- REVISE: missing sources/date ranges, missing split, untracked hook outcomes, no executable next actions, or critic verdict `REVISE`

## Writeback Contract
- Blackboard keys:
  - `measure.report`
  - `measure.kpi_snapshot`
  - `measure.next_actions`
  - `measure.reporting_split`
  - `measure.persona_callouts`
  - `measure.feedback_events`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - On each meaningful update, post `status_summary` + `next_steps`
  - For high-risk recommendation events, post a prefilled Decision Packet before requesting Max decision

## Delegation Map
- Reporting: `brand-report` skill
- Asset-level social metrics + scoring (day-1 IG): `content-measure`
- Content iteration tickets: route to the relevant supervisor (Awareness/Lead Capture/etc)

## Failure Policy
- If analytics access is missing: produce a manual measurement checklist and instrument plan; do not invent metrics

## Done When
- Report exists, is linked, critic-verified in `production`, split reporting is recorded, and next actions are queued as deliverable tickets
