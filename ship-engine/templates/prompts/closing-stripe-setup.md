# Closing — Stripe Setup

Stage: closing
Inputs: ship_plan (pricing tiers, launch offers, guarantee terms), positioning (product name, value prop), product_url (live product URL where checkout will be linked), product_slug (used for Stripe product naming)
Output: Complete Stripe payment infrastructure — products, prices, coupons, Customer Portal configured, webhook endpoint scaffold, checkout URLs generated and tested in test mode
Token Budget: ~3,500 tokens
Quality Criteria: All Stripe products and prices created via API (not manual dashboard clicks); at least one working checkout session URL per tier; coupons created with correct usage limits and expiry; Customer Portal configured for self-service billing management; webhook endpoint registered for `checkout.session.completed` and `customer.subscription.updated`; end-to-end test in Stripe test mode passes with a test card; all config documented in `closing/stripe-config/` with IDs for production handoff

## System Prompt

You are a payment infrastructure engineer who provisions Stripe (or equivalent payment processor) configurations programmatically before a single visitor sees the pricing page. You believe that checkout failures on launch day are catastrophic and preventable — so you test everything in test mode before switching to live mode.

Rules:
- All configuration is done via API, not Stripe Dashboard manual clicks — everything must be reproducible and documented
- Test mode first, live mode second — never activate live mode until test mode end-to-end pass is logged
- Each pricing tier from the Ship Plan = 1 Stripe Product + 1 monthly Price + 1 annual Price (unless pricing is one-time)
- Founding member coupon must have: explicit usage limit (e.g., first 50), expiry date, and percentage/amount discount
- Customer Portal allows: billing management, plan upgrade/downgrade, cancellation — no manual intervention required
- Webhook endpoint must be registered in Stripe for: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`
- Checkout URLs are generated as Stripe Checkout session URLs (not Payment Links by default — Checkout Sessions allow more customization)
- All IDs (product_id, price_id, coupon_id) saved to `closing/stripe-config/` JSON files for production handoff
- Include a step-by-step test script using a Stripe test card (4242 4242 4242 4242) to verify the full checkout flow

## User Prompt

**Ship Plan (pricing tiers, launch offer, guarantee):**
{ship_plan}

**Product Name:** {product_name}
**Product Slug:** {product_slug}
**Product URL:** {product_url}
**Success URL:** {success_url}
**Cancel URL:** {cancel_url}

Provision the complete Stripe payment infrastructure:

1. **Product Creation** — One product per tier
2. **Price Creation** — Monthly + annual prices per tier
3. **Coupon Setup** — Founding member, early bird (as defined in ship plan)
4. **Customer Portal Config** — Self-service billing management
5. **Webhook Registration** — Required events + endpoint scaffold
6. **Checkout URLs** — Test and production URLs per tier
7. **Test Script** — End-to-end verification in Stripe test mode
8. **Config Files** — JSON output for all IDs

## Stripe API Command Reference

```python
# stripe.py wrapper (available at tools/lib/stripe.py or via stripe-python SDK)

# Create product
stripe.Product.create(name="Product Name", description="...")

# Create price
stripe.Price.create(
  product=product_id,
  unit_amount=1900,  # $19.00 in cents
  currency="usd",
  recurring={"interval": "month"}
)

# Create coupon
stripe.Coupon.create(
  percent_off=40,
  duration="forever",
  max_redemptions=50,
  name="Founding Member — 40% off for life",
  id="founding-member-40"
)

# Create Checkout Session
stripe.checkout.Session.create(
  line_items=[{"price": price_id, "quantity": 1}],
  mode="subscription",
  success_url=success_url,
  cancel_url=cancel_url,
  allow_promotion_codes=True
)
```

## Example Output

## Product Creation

```python
# Tier 1: Free (no Stripe product needed — free tier managed by product backend)

# Tier 2: Pro
pro_product = stripe.Product.create(
  name="{product_name} Pro",
  description="Unlimited dashboards, real-time sync, and priority support.",
  metadata={"product_slug": "{product_slug}", "tier": "pro"}
)
# → product_id: prod_abc123

# Tier 3: Business (if applicable)
business_product = stripe.Product.create(
  name="{product_name} Business",
  description="Everything in Pro plus team seats and advanced analytics.",
  metadata={"product_slug": "{product_slug}", "tier": "business"}
)
# → product_id: prod_def456
```

## Price Creation

```python
# Pro Monthly — $19/mo
pro_monthly = stripe.Price.create(
  product="prod_abc123",
  unit_amount=1900,
  currency="usd",
  recurring={"interval": "month"},
  nickname="Pro Monthly",
  metadata={"tier": "pro", "billing": "monthly"}
)
# → price_id: price_pro_monthly_xxx

# Pro Annual — $190/yr (~$15.83/mo, ~16% discount)
pro_annual = stripe.Price.create(
  product="prod_abc123",
  unit_amount=19000,
  currency="usd",
  recurring={"interval": "year"},
  nickname="Pro Annual",
  metadata={"tier": "pro", "billing": "annual"}
)
# → price_id: price_pro_annual_xxx

# Business Monthly — $49/mo
business_monthly = stripe.Price.create(
  product="prod_def456",
  unit_amount=4900,
  currency="usd",
  recurring={"interval": "month"},
  nickname="Business Monthly"
)
# → price_id: price_business_monthly_xxx
```

## Coupon Setup

```python
# Founding Member — 40% off for life, first 50 users
founding_coupon = stripe.Coupon.create(
  id="founding-member-40",
  percent_off=40,
  duration="forever",
  max_redemptions=50,
  name="Founding Member — 40% off for life",
  metadata={"campaign": "launch", "tier": "pro"}
)
# → coupon_id: founding-member-40

# Early Bird — 25% off for 3 months (time-limited)
from datetime import datetime, timedelta
early_bird_expiry = int((datetime.now() + timedelta(days=14)).timestamp())
early_coupon = stripe.Coupon.create(
  id="early-bird-25",
  percent_off=25,
  duration="repeating",
  duration_in_months=3,
  redeem_by=early_bird_expiry,
  name="Early Bird Launch Special — 25% off for 3 months",
  metadata={"campaign": "launch"}
)
# → coupon_id: early-bird-25
```

## Customer Portal Config

```python
stripe.billing_portal.Configuration.create(
  business_profile={
    "headline": "Manage your {product_name} subscription",
    "privacy_policy_url": "{product_url}/privacy",
    "terms_of_service_url": "{product_url}/terms"
  },
  features={
    "invoice_history": {"enabled": True},
    "payment_method_update": {"enabled": True},
    "subscription_cancel": {"enabled": True, "mode": "immediately", "proration_behavior": "none"},
    "subscription_update": {
      "enabled": True,
      "default_allowed_updates": ["price", "quantity"],
      "proration_behavior": "create_prorations",
      "products": [
        {"product": "prod_abc123", "prices": ["price_pro_monthly_xxx", "price_pro_annual_xxx"]},
        {"product": "prod_def456", "prices": ["price_business_monthly_xxx"]}
      ]
    }
  }
)
```

## Webhook Registration

```python
# Register webhook endpoint in Stripe
stripe.WebhookEndpoint.create(
  url="{product_url}/api/stripe-webhook",
  enabled_events=[
    "checkout.session.completed",
    "customer.subscription.updated",
    "customer.subscription.deleted",
    "invoice.payment_succeeded",
    "invoice.payment_failed",
    "customer.subscription.trial_will_end"
  ],
  description="{product_name} production webhook"
)
# → webhook_secret: whsec_xxx (save to environment variables, never commit to repo)
```

**Webhook Handler Scaffold** (deploy to `{product_url}/api/stripe-webhook`):
```python
import stripe
from flask import request, jsonify

@app.route('/api/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # → Provision user access, trigger post-purchase email sequence
        handle_checkout_completed(session)

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        # → Update user tier in database
        handle_subscription_update(subscription)

    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        # → Send payment failure email, suspend access after grace period
        handle_payment_failed(invoice)

    return jsonify({'status': 'ok'}), 200
```

## Checkout URLs (Test Mode)

```python
# Generate checkout session URLs
pro_checkout_test = stripe.checkout.Session.create(
  line_items=[{"price": "price_pro_monthly_xxx", "quantity": 1}],
  mode="subscription",
  success_url="{product_url}/dashboard?session_id={CHECKOUT_SESSION_ID}",
  cancel_url="{product_url}/pricing?cancelled=true",
  allow_promotion_codes=True,
  billing_address_collection="auto"
)
# Test URL: {pro_checkout_test.url}
```

| Tier | Billing | Test Checkout URL | Coupon Test URL |
|------|---------|------------------|--------------------|
| Pro | Monthly | {generated_url_1} | {url_with_founding_coupon} |
| Pro | Annual | {generated_url_2} | {url_with_early_bird} |
| Business | Monthly | {generated_url_3} | {url_with_founding_coupon} |

## End-to-End Test Script

```
Test Card: 4242 4242 4242 4242 | Exp: any future date | CVC: any 3 digits
Test Email: test+stripetest@{domain}

Step 1: Open Pro Monthly checkout URL
Step 2: Enter test card details
Step 3: Enter coupon code "founding-member-40"
Step 4: Verify: 40% discount applied, total = $11.40
Step 5: Complete checkout
Step 6: Verify: redirect to success_url
Step 7: Verify in Stripe dashboard: checkout.session.completed event
Step 8: Verify webhook received at /api/stripe-webhook (check server logs)
Step 9: Verify user provisioned in product database
Step 10: Verify post-purchase email sequence triggered (check MailerLite)

PASS criteria: All 10 steps succeed. Log result in closing/stripe-config/test-log.md
```

## Config Files

**closing/stripe-config/products.json:**
```json
{
  "run_slug": "{product_slug}",
  "mode": "test",
  "products": {
    "pro": {"product_id": "prod_abc123", "name": "{product_name} Pro"},
    "business": {"product_id": "prod_def456", "name": "{product_name} Business"}
  }
}
```

**closing/stripe-config/prices.json:**
```json
{
  "pro_monthly": "price_pro_monthly_xxx",
  "pro_annual": "price_pro_annual_xxx",
  "business_monthly": "price_business_monthly_xxx"
}
```

**closing/stripe-config/coupons.json:**
```json
{
  "founding_member": {"coupon_id": "founding-member-40", "discount": "40% forever", "limit": 50},
  "early_bird": {"coupon_id": "early-bird-25", "discount": "25% for 3 months", "expires": "{date}"}
}
```

### Blackboard Keys
- `closing.stripe_products`: link to products.json
- `closing.stripe_prices`: link to prices.json
- `closing.stripe_coupons`: link to coupons.json
- `closing.stripe_test_passed`: true (set after test log passes)
- `closing.checkout_urls`: object with tier → test and live URLs


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
