# Segment Definitions: {product_name}

> **Template version:** 1.0 — Ship Engine Nurture Stage (5C)
> **Owner:** `ship-nurture-supervisor`
> **Inputs required:** ICP document (`validate.icp`), Lead Capture group name, Email provider (MailerLite)
> **Outputs:** Populated segment table + engagement scoring config ready for automation

---

## Overview

Subscriber segmentation enables personalized nurture paths, engagement-based throttling, and precise retargeting. Every subscriber is always in exactly one **primary segment** and may carry one or more **engagement tags**.

Segment assignment is automatic — driven by behavioral signals, not manual tagging.

---

## Primary Segments

| Segment | Label | Entry Criteria | Nurture Path | Priority |
|---------|-------|----------------|--------------|----------|
| **New Subscriber** | `seg:new` | Joined within last 24h; no opens/clicks yet | Welcome sequence — Day 0 trigger | Highest |
| **Engaged — Active** | `seg:engaged-active` | Opened ≥2 emails OR clicked ≥1 link in last 14 days | Standard nurture sequence | High |
| **Engaged — Warm** | `seg:engaged-warm` | Opened ≥1 email; no click; no purchase signal in 14 days | Soft re-engagement at Day 7 | Medium |
| **Engaged — Cold** | `seg:engaged-cold` | No open in last 14 days; subscribed >7 days ago | Re-engagement sub-sequence (3 emails) | Low |
| **Converter** | `seg:converter` | Made a purchase / activated paid plan | Exit nurture → enter post-purchase sequence | — |
| **Dormant** | `seg:dormant` | No open in last 30 days | Sunset sequence (1-2 emails) → suppress or unsub | — |
| **Unsubscribed** | `seg:unsub` | Unsubscribed; keep for suppression only | Suppression list only | — |

### Segment Transition Rules

```
New Subscriber
  → Opens email #1          → Engaged — Active
  → No open in 7 days       → Engaged — Cold

Engaged — Active
  → No open in 14 days      → Engaged — Warm
  → No open in 30 days      → Engaged — Cold → Dormant

Engaged — Cold
  → Opens re-engagement email → Engaged — Active
  → No open after 3 attempts → Dormant

Dormant
  → Opens sunset email        → Engaged — Warm (re-enter nurture)
  → No response to sunset     → Unsubscribed (list hygiene)

Converter
  → Separate post-purchase sequence (not re-segmented into nurture)
```

---

## Engagement Scoring Rules

Engagement score (0–100) determines send frequency, upgrade eligibility, and content depth. Score decays daily if no activity.

### Scoring Events

| Event | Points | Notes |
|-------|--------|-------|
| Email opened | +5 | Deduped per email send (one open event per email) |
| Link clicked | +15 | Any tracked link in email body |
| CTA clicked (primary) | +25 | Main CTA button clicked |
| Landing page visited (from email) | +20 | UTM-tracked visit |
| Product activated (free/trial) | +40 | Signup completed, app accessed |
| Upgrade / Purchase | +100 | Triggers Converter segment |
| Unsubscribe | -100 | Hard exit |
| Email soft-bounced | -10 | Per bounce event |
| Email hard-bounced | -100 | Suppress immediately |
| No activity (daily decay) | -2/day | After 7 days of no opens |

### Score Bands

| Score | Band | Interpretation | Action |
|-------|------|----------------|--------|
| 80–100 | 🔥 Hot | High intent; likely evaluating | Accelerate CTA cadence; surface urgency email early |
| 50–79 | ✅ Warm | Engaged; building trust | Standard sequence; no changes |
| 20–49 | ⚡ Lukewarm | Passive reader; low click intent | Inject re-engagement hook at next email |
| 1–19 | ❄️ Cold | Nearly dormant | Trigger re-engagement sub-sequence |
| 0 | 💀 Dead | No activity | Dormant segment; sunset sequence |

### Score-Based Sequence Modifications

- **Hot (80+):** Skip Day 10 urgency email — show urgency in Day 7. Pull forward Last Call to Day 12.
- **Cold (1–19) after Day 5:** Pause standard sequence. Trigger 3-email re-engagement path before resuming.
- **Score unchanged for 21 days:** Move to Dormant; send sunset sequence; suppress if no response.

---

## ICP Micro-Segments

Micro-segments enable copy personalization within the same nurture sequence. Derived from lead capture form fields, UTM source, or behavioral signals.

| Micro-Segment | Identifier | Entry Signal | Personalization Hint |
|---------------|------------|--------------|----------------------|
| **{persona_A}** | `ms:persona-a` | {form_field or UTM tag} | {pain language, CTA copy direction} |
| **{persona_B}** | `ms:persona-b` | {form_field or UTM tag} | {pain language, CTA copy direction} |
| **IG Referral** | `ms:ig-referral` | UTM source=instagram | Reference IG content that drove signup |
| **Newsletter Referral** | `ms:newsletter-referral` | UTM source=newsletter | Acknowledge newsletter context |
| **High-Intent Visitor** | `ms:high-intent` | Visited pricing page before signup | Pull forward offer CTA by 2 days |
| **No-Context** | `ms:no-context` | No form data, no UTM | Default sequence; no personalization tokens |

> **Agent note:** Fill in `{persona_A}`, `{persona_B}` and their signals from the ICP document (`validate.icp`). Persona names must match ICP segment names exactly.

---

## Suppression Rules

Apply before every send — suppression is non-negotiable:

1. **Hard bounced** (`email.bounced = hard`) → Never send again
2. **Unsubscribed** → Suppressed globally (GDPR/CAN-SPAM)
3. **Converter** → Excluded from nurture sends; post-purchase sequence only
4. **Complaint** (`spam_report = true`) → Suppress immediately
5. **Dormant > 60 days** → Suppressed until re-opt-in confirmed

---

## MailerLite Implementation Checklist

- [ ] Segment `seg:new` auto-created via group join trigger (Lead Capture Agent wires this)
- [ ] Segment `seg:engaged-active` built with open/click filters (last 14 days)
- [ ] Segment `seg:engaged-cold` built with no-open filter (14+ days)
- [ ] Engagement score field (`custom_field: engagement_score`) created in MailerLite
- [ ] Scoring automation created: event → field increment (use MailerLite automation steps)
- [ ] Score decay: daily automation step `-2` if `last_open_date` > 7 days ago
- [ ] Converter segment wired to purchase webhook (via MailerLite API or Zapier bridge)
- [ ] Suppression list imported and active before first send
- [ ] Micro-segment tags applied at lead capture (UTM → tag mapping in Lead Capture Agent)

---

## Handoff Notes

**→ To Nurture Agent (email sequence):** Use `seg:engaged-active` as primary delivery target. Use score band to modify CTA timing. Use micro-segment tags for copy personalization tokens.

**→ To Closing Agent:** Share score band distribution after Day 7 send. Hot subscribers (80+) may be ready for direct outreach or offer upgrade.

**→ To Awareness Agent (retargeting):** Export `seg:engaged-cold` and `seg:dormant` to Meta custom audience for retargeting ads (if ad budget approved in Strategy).

---

*Generated by `ship-nurture-supervisor` | Template: `skills/engine/templates/segment-definitions.md`*
