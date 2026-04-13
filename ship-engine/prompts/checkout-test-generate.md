# Prompt: Generate Checkout Flow Test Plan (with Evidence)

**Objective:** Produce a launch-grade checkout QA plan with explicit pass/fail criteria and screenshot-proof requirements.

## Context
You are a senior QA engineer validating SaaS checkout before launch. A broken payment flow is a launch blocker.

## Inputs
- Product name: `{product_name}`
- Pricing page URL: `{pricing_page_url}`
- Checkout provider: `{checkout_provider}` (Stripe, Mercado Pago, Paddle, etc.)
- Active tiers/plans: `{tiers}`
- Coupon/launch offers: `{coupons}`
- Analytics stack: `{analytics_stack}`
- Webhook endpoint(s): `{webhook_endpoints}`

## Requirements
Create a markdown test plan with these sections:
1. Run Context
2. Success Criteria (checklist)
3. Test Matrix (positive, negative, edge, mobile)
4. Test Data
5. Evidence Checklist
6. Defects/Notes table
7. Final Verdict (GO/NO-GO)

## Minimum Scenarios
- CTA → correct checkout per tier
- Price/currency integrity between pricing page and checkout
- Valid coupon success + invalid coupon handling
- Successful test payment to confirmation
- Declined/failed payment handling
- Interrupted session/abandonment behavior
- Terms + refund links visible and working
- Analytics events (`checkout_start`, `purchase`) verified
- Webhook/fulfillment event verified (`checkout.session.completed` or equivalent)
- Mobile viewport execution

## Output Quality Bar
- Clear reproducible steps for each case
- Expected result is binary and testable
- Every case includes an evidence slot (screenshot/log URL)
- Uses concise, operational language (no filler)
