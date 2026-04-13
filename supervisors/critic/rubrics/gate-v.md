# Critic Rubric — Gate-V (Post-Validation Gate)

Applies to: Stage 3 gate decision packet

## Decision Packet Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | All hard-gate fields present | `status_summary`, `risk_level`, `confidence`, `recommended_action`, `next_steps`, `owner`, `due_by`, `queue_priority`, `evidence_links`, `kanban_proof_links` — all present | Any required field missing |
| 2 | Evidence links resolve | All evidence_links are valid, linked artifacts | Broken or placeholder links |
| 3 | Kanban proof complete | Inputs/Deliverables/Verification/Artifacts all linked | Any kanban section missing |
| 4 | Validation Report critic-verified | `validate.validation_report.critic_verdict = PASS` on record | No critic PASS for validation report |
| 5 | ICP critic-verified | `validate.icp.critic_verdict = PASS` on record | No critic PASS for ICP |
| 6 | Probe Pack included (first runs) | `validate.probe_pack`, `validate.probe_metrics`, `validate.probe_verdict` linked | First-cycle run missing probe pack links |
| 7 | Recommended action valid | `recommended_action` is one of: `ship`, `explore`, `kill` | Invalid or missing value |
| 8 | Score/recommendation alignment | Recommended action matches score band (≥4.0→ship, 3-3.9→explore, <3→kill) | Mismatch without written justification |
| 9 | Risks documented | ≥2 specific risks with de-risking steps | No risks mentioned |
| 10 | Next steps concrete | `next_steps` describes exactly what runs immediately after decision | Vague or missing next steps |

## REVISE output required
List each failing check + specific fix instruction.
