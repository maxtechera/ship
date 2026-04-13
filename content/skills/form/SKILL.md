---
name: content-form
version: "1.0.0"
description: "Design GTM forms (lead capture, onboarding, feedback) with conversion optimization and tracking contracts."
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Content Form

Define form assets that capture leads without funnel friction.

## Types

- Lead capture forms (top-of-funnel, minimal fields)
- Demo/consult booking forms
- Post-signup onboarding forms
- Feedback/NPS forms
- Objection and churn-intent forms

## Inputs Required

- Funnel stage and conversion goal
- Offer and CTA context from landing page
- CRM/email destination (list, group, automation)
- Tracking requirements (GA4 events, UTMs)

## Required Outputs

- **Field schema**: required/optional flags, field types, order
- **Microcopy**: labels, placeholders, helper text, error messages, submit button text
- **Submit behavior**: redirect URL or inline confirmation
- **Event tracking contract**: `view`, `start`, `submit`, `success`, `dropoff`
- **Routing rules**: CRM list, email automation trigger, notification webhook

## Conversion Rules

- Top-of-funnel forms: email only (or email + first name max)
- Mid-funnel forms: email + 1-2 qualifying fields
- Demo/high-intent forms: email + company + use case
- Never ask for phone without explicit reason
- Submit button copy = outcome ("Get Free Guide", not "Submit")

## Event Tracking Contract

```
form_view      → user sees the form
form_start     → user focuses first field
form_submit    → user clicks submit
form_success   → server confirms submission
form_dropoff   → user abandons without submitting
```

All events include: `form_id`, `page_url`, `utm_source`, `utm_medium`, `utm_campaign`

## Integration Wiring

- Email capture → email provider group/list (with tags)
- Lead magnet delivery → automation trigger fires on `form_success`
- CRM sync → contact created/updated with source attribution
- Notification → internal webhook to Slack/Telegram (optional)

## Test Protocol

Before going live:
1. Submit test entry → confirm email received
2. Check UTM attribution passed through
3. Verify GA4 `form_success` event fires
4. Confirm automation trigger fires
5. Log test result with screenshot

## Done Criteria

- [ ] Field schema defined with required/optional
- [ ] Microcopy written (labels, placeholders, errors, submit)
- [ ] Event tracking contract documented
- [ ] Routing rules specified (list, automation, CRM)
- [ ] End-to-end test protocol defined
- [ ] Consent language included where required
