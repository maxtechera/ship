# Critic Rubric — Cross-Deliverable Consistency Check

Run after parallel workstreams have produced their first deliverables. Checks that
ICP language, offer, and messaging flow coherently from Validate through every
downstream touchpoint.

## Consistency Checks

| # | From | To | PASS criteria | REVISE trigger |
|---|------|----|--------------|----------------|
| 1 | `validate.icp` — top pain phrase | Landing page hero headline | ≥1 near-verbatim pain phrase in hero | Generic or product-feature headline |
| 2 | `validate.icp` — pain severity ranking | `lead_capture.offer_stack` value framing | Top-ranked pain addressed first in offer | Offer focuses on lower-ranked pain |
| 3 | `strategy.ship_plan` — positioning one-liner | Email subject lines (nurture sequence) | Subject lines reflect positioning angle | Subject lines contradict positioning |
| 4 | `strategy.ship_plan` — pricing tier names + prices | Closing pricing page | Names + prices match exactly | Any mismatch |
| 5 | `lead_capture.offer_stack` — offer description | Nurture email CTAs | CTAs reference same offer wording | Different offer version used |
| 6 | Landing page hero promise | Nurture email #1 (welcome) | Welcome email delivers on hero promise | Welcome doesn't reference what landing page promised |
| 7 | `validate.icp` — VoC language | Blog post copy | ≥3 VoC phrases per article | Generic industry language only |
| 8 | `validate.icp` — competitor weaknesses | Awareness competitor comparison content | Comparison content references real documented weaknesses | Invented weaknesses not from research |
| 9 | `strategy.ship_plan` — channel priorities | Nurture content drip platforms | Drip covers the priority channels from Ship Plan | Missing priority channels |
| 10 | Closing objections (top 5) | Landing page FAQ | FAQ addresses ≥3 of the top 5 objections | <3 objections covered |

## Evaluation Instructions

For each check:
1. Fetch the "From" artifact content (summary or key phrase)
2. Fetch the "To" artifact content
3. Apply the PASS criteria — string/semantic match is fine; exact verbatim not required for language checks
4. If REVISE: cite the specific "From" phrase that should appear in "To" and where to insert it

## Aggregate Result

- All checks pass → `PASS`
- Any check fails → `REVISE` with specific cross-deliverable fix instructions

Cross-check `REVISE` blocks only the affected "To" deliverable, not the entire run.
The check that failed is noted on the "To" deliverable's Linear ticket.
