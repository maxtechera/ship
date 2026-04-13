# Critic Rubric — Gate-S (Post-Strategy Lock Gate)

Applies to: Stage 4 Strategy Lock decision packet

## Strategy Lock Pack Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | Hard-gate fields | All required: `status_summary`, `risk_level`, `confidence`, `recommended_action`, `next_steps`, `owner`, `due_by`, `queue_priority`, `evidence_links`, `kanban_proof_links` | Any field missing |
| 2 | ICP link | `validate.icp` linked | Missing |
| 3 | Positioning in packet | One-liner + value prop included or linked | Missing |
| 4 | Offer stack in packet | Offer stack + pricing hypothesis + guarantee included or linked | Missing |
| 5 | Channel priorities | Distribution plan with ≥3 channels | Missing |
| 6 | Winning angles | ≥3 seed angles for first creative batch | Missing |
| 7 | Budget documented | Spend policy (what can/can't spend) + total | Missing |
| 8 | Segment lock | `primary_segment`, `deferred_segment`, `excluded_segments` | Any missing |
| 9 | Kanban proof for parallel | Downstream parallel tickets have Inputs/Deliverables/Verification/Artifacts blocks | Missing |
| 10 | 30-day experiment map | Present with hypothesis/metric/boundary/window/owner | Missing |
| 11 | Ship Plan critic-verified | `strategy.ship_plan.critic_verdict = PASS` | No critic PASS |
| 12 | Recommended action valid | One of: `proceed`, `revise`, `kill` | Invalid or missing |

## REVISE output required
List each failing check + specific fix instruction.
