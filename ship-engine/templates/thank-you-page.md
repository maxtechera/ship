# Thank You Page Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Purpose

The thank you page appears immediately after signup. Its job is to:
1. Confirm success (reduce anxiety)
2. Deliver or point to first value fast
3. Move the lead into the next meaningful action

---

## Setup

| Field | Value |
|------|------|
| Product / Offer | |
| Audience segment | |
| Primary conversion goal | |
| Secondary conversion goal | |
| URL slug | `/thank-you` |
| Owner | |
| Last updated | |

---

## Above-the-Fold Copy

### Headline
`You're in. Welcome to {product_name}.`

### Confirmation line
`Your signup is confirmed. Check your inbox for the welcome email from {from_name}.`

### Value line
`While you wait, here’s the fastest way to get your first win in the next 5 minutes.`

### Primary CTA
- **Button text:** `{primary_cta_text}`
- **Destination:** `{primary_cta_url}`
- **Intent:** first-value action (onboarding, setup wizard, lead magnet, demo)

### Secondary CTA
- **Button text:** `{secondary_cta_text}`
- **Destination:** `{secondary_cta_url}`
- **Intent:** lower-friction backup action (watch video, join group, book call)

---

## Body Blocks

### 1) What happens next (3 steps max)
1. `{step_1}`
2. `{step_2}`
3. `{step_3}`

### 2) Set expectations
- Email frequency: `{frequency}`
- Content promise: `{content_promise}`
- Reply invitation: `{reply_prompt}`

### 3) Social proof strip
- Logos/testimonial/stat: `{proof_block}`

### 4) Quick-start resource list
- `{resource_1}`
- `{resource_2}`
- `{resource_3}`

---

## Tracking + Attribution

- [ ] Preserve inbound UTM parameters on thank-you URL
- [ ] Fire GA4 event: `generate_lead` (or `sign_up`)
- [ ] Fire CTA click events:
  - `thank_you_primary_cta_click`
  - `thank_you_secondary_cta_click`
- [ ] Add hidden field / cookie handoff into CRM source attribution

Event payload baseline:
- `campaign`
- `source`
- `medium`
- `content`
- `offer_id`
- `segment`

---

## QA Checklist

- [ ] Confirmation copy appears immediately after successful submit
- [ ] Primary CTA is visible above fold on mobile + desktop
- [ ] Welcome email sender info matches page copy
- [ ] CTA links work and include expected UTM params
- [ ] Page loads in <3s on mobile
- [ ] No dead-end state (at least one next action available)

---

## Variants (A/B)

| Variant | Hypothesis | Metric | Winner criteria |
|--------|------------|--------|-----------------|
| A: “Start now” CTA | Higher immediate activation | Primary CTA CTR | +15% CTR |
| B: “Watch 2-min demo” CTA | Better comprehension before action | Activation completion | +10% completions |

---

## Final Copy (ready-to-publish)

### [EN]
- **Headline:**
- **Confirmation line:**
- **Primary CTA text:**
- **Secondary CTA text:**
- **Next steps block:**

### [ES]
- **Titular:**
- **Línea de confirmación:**
- **Texto CTA principal:**
- **Texto CTA secundario:**
- **Bloque de próximos pasos:**


_Template: Ship Engine · NEO-218_
