# Critic Rubric — Gate-L (Pre-Launch Gate)

Applies to: Stage 6 pre-launch decision packet

## Scale Readiness Checklist Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | Hard-gate fields | All required: `status_summary`, `risk_level`, `confidence`, `recommended_action`, `next_steps`, `owner`, `due_by`, `queue_priority`, `evidence_links`, `kanban_proof_links` | Any field missing |
| 2 | Landing page live | Awareness confirms URL + screenshots | Missing |
| 3 | Email capture wired | Lead Capture confirms form + email group tested | Missing |
| 4 | Nurture sequence live | Nurture confirms automation imported + test email passed | Missing |
| 5 | Stripe checkout tested | Closing confirms end-to-end test logged | Missing |
| 6 | Pricing page deployed | Closing confirms URL + mobile verify | Missing |
| 7 | Analytics tracking verified | Lead Capture confirms events firing + UTMs working | Missing |
| 8 | All parallel critic verdicts | Awareness, Lead Capture, Nurture, Closing deliverables all have `PASS` from critic | Any workstream with `REVISE` outstanding |
| 9 | Rollback plan | Rollback steps documented | Missing |
| 10 | Stage 9 health | Draft queue has ≥1 publish-ready deliverable; no high-risk approvals blocking | Empty queue or unresolved blocks |
| 11 | Recommended action valid | One of: `launch`, `fix`, `kill` | Invalid or missing |

## REVISE output required
List each failing check + specific fix instruction.
