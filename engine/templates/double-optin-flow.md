# Double Opt-In Flow Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Overview

Double opt-in (DOI) confirms subscriber intent, reduces spam complaints, and improves list quality. This template covers the full 3-message sequence.

| Field | Value |
|-------|-------|
| **Product / Brand** | |
| **From Name** | |
| **From Email** | |
| **Confirmation Link expiry** | 72 hours |
| **ESP / Tool** | (Mailchimp, Kit, Loops, etc.) |

---

## Trigger

**Source:** Form submission on `[page URL]`  
**Segment added:** `[unconfirmed-subscribers]`  
**Confirmation URL:** `[your-domain.com/confirm?token=...`]

---

## Email 1 — Confirmation Request

**Send:** Immediately on sign-up  
**Subject:** `Please confirm your email → [Brand]`  
**Preview text:** `One click and you're in.`

---

**Body:**

```
Hi {{first_name | default: "there"}},

Thanks for signing up!

We just need to confirm your email address before we send anything.

[CONFIRM MY SUBSCRIPTION →]
(button links to confirmation URL)

This link expires in 72 hours.

If you didn't sign up for [Brand], you can safely ignore this email.

— [Founder Name / Team Name]

---
[Brand] · [Address] · Unsubscribe
```

**Design notes:**
- Single CTA button, high contrast
- No images required (plain text converts well)
- CAN-SPAM / GDPR footer required

---

## Email 2 — Follow-Up Nudge (if not confirmed)

**Send:** 24 hours after Email 1, IF not confirmed  
**Subject:** `Did you mean to sign up? (action needed)`  
**Preview text:** `Your confirmation link is still waiting.`

---

**Body:**

```
Hi {{first_name | default: "there"}},

Just a quick nudge — you signed up for [Brand] yesterday
but haven't confirmed your email yet.

Your spot is reserved for another 48 hours.

[YES, CONFIRM ME →]
(button links to confirmation URL)

If you changed your mind, no worries — just ignore this email
and you won't hear from us again.

— [Founder Name]

P.S. Once confirmed, you'll get [value prop: e.g., "our free
     [Lead Magnet] + weekly tips on [topic]"].
```

---

## Email 3 — Welcome (on confirmation)

**Trigger:** User clicks confirmation link  
**Segment moved to:** `[confirmed-subscribers]`  
**Subject:** `Welcome to [Brand]! Here's what's next 🎉`  
**Preview text:** `You're officially in. Let's get started.`

---

**Body:**

```
Hi {{first_name | default: "there"}},

You're confirmed — welcome to [Brand]! 🎉

Here's what to expect from us:
• [Benefit 1 — e.g., weekly tips on X]
• [Benefit 2 — e.g., early access to new features]
• [Benefit 3 — e.g., member-only resources]

To get you started, here's your free [lead magnet]:

[DOWNLOAD / ACCESS NOW →]

Reply to this email anytime — I read every message.

Talk soon,
[Founder Name]
[Title] at [Brand]

---
[Brand] · [Address] · Unsubscribe
```

**Automation after Email 3:**
- Add to main nurture sequence (Day 2+)
- Tag: `doi-confirmed`, `source:[form-name]`
- Notify CRM / Slack if high-value segment

---

## Automation Flow Diagram

```
[Form submit]
      │
      ▼
[Add to: unconfirmed] ──→ Email 1 (immediate)
      │
      ├─ [Confirmed?] ──YES──→ Email 3 (Welcome) ──→ Nurture
      │                                               sequence
      │
      └─ [24h, not confirmed] ──→ Email 2 (Nudge)
                │
                ├─ [Confirmed?] ──YES──→ Email 3 (Welcome)
                │
                └─ [48h, still not confirmed] ──→ Remove /
                                                  quarantine list
```

---

## Key Metrics to Track

| Metric | Benchmark | Your Baseline |
|--------|-----------|---------------|
| Email 1 open rate | 60–80% | |
| Confirmation rate | 50–70% | |
| Email 2 open rate | 40–60% | |
| Email 2 conversion | 10–25% | |
| Welcome open rate | 70–90% | |

---

## Compliance Checklist

- [ ] Physical address in footer (CAN-SPAM)
- [ ] Unsubscribe link in all emails
- [ ] Consent language on sign-up form
- [ ] Data processor noted (GDPR if EU audience)
- [ ] Confirmation link expiry enforced

---

_Template: Ship Engine · NEO-231_
