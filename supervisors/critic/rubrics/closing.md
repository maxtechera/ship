# Critic Rubric — Closing (Stage 5D)

Applies to: Stripe config, pricing page, objection handling, post-purchase sequence

## Payment Setup Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | Products + prices created | Stripe products.json and prices.json linked (API verified) | Not created |
| 2 | Checkout tested | Test transaction completed in test mode, logged | Not tested |
| 3 | Coupon codes created | At least 1 launch discount code with usage limit + expiry | Missing |
| 4 | Customer Portal configured | Self-service billing portal enabled | Not configured |

## Pricing Page Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 5 | Page live | URL returns 200 | Not deployed |
| 6 | Monthly/annual toggle | Toggle works, prices update dynamically | Broken or missing |
| 7 | Stripe checkout links | Each tier's CTA links to correct Stripe checkout | Broken or wrong links |
| 8 | Mobile responsive | Verified at 375px viewport | Not checked |
| 9 | End-to-end browser test | Agent-logged test: page → tier click → Stripe checkout loads | Not logged |

## Objection Handling Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 10 | ≥3 objections addressed | At least 3 objections from ICP data sourced | <3 or not from ICP data |
| 11 | Landing page FAQ | FAQ entries formatted for embedding | Missing |
| 12 | Email objection copy | Day 7 objection killer email copy handed to Nurture | Missing |
| 13 | ROI framing | At minimum, cost-of-problem vs cost-of-solution stated | No ROI context |

## Post-Purchase Sequence Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 14 | ≥3 emails | At least 3 post-purchase emails (immediate, D3 check-in, D7 testimonial ask) | <3 emails |
| 15 | Trigger configured | Automation fires on purchase event, separate from nurture | Not configured |
| 16 | Test flow verified | Test purchase → correct email delivered → logged | Not tested |

## REVISE output required
List each failing check + specific fix instruction.
