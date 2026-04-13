# Win-Back Email Sequence Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Overview

A 3-email win-back sequence targets subscribers or users who have gone inactive. Goal: re-engage or cleanly remove them.

| Field | Value |
|-------|-------|
| **Product / Brand** | |
| **Inactivity threshold** | 90 days (adjust to fit your send cadence) |
| **Segment** | `[inactive-90d]` |
| **From Name** | Founder name (more personal) |

---

## Trigger

**Entry condition:** No email opens AND no product logins for `[X]` days  
**Entry segment:** `inactive-90d`  
**Frequency guard:** Do not re-enter if already completed sequence in last 6 months

---

## Email 1 — The Check-In

**Send:** Day 0 (sequence start)  
**Subject:** `Still interested in [Brand]?`  
**Preview text:** `It's been a while — we miss you.`  
**Tone:** Warm, curious, low pressure

---

**Body:**

```
Hey {{first_name | default: "there"}},

It's been a while since we last heard from you, so I wanted
to check in personally.

A lot has happened at [Brand] since you signed up:
• [New feature / update 1]
• [New feature / update 2]
• [Result a customer recently got — social proof]

Still interested in [core value prop]?

[SEE WHAT'S NEW →]

If now isn't the right time, no worries — just let me know
and I'll pause emails until you're ready.

— [Founder Name]
[Title], [Brand]
```

**Goal:** Soft re-engagement. One click = reactivate.

---

## Email 2 — The Offer

**Send:** Day 7 (if Email 1 not opened or clicked)  
**Subject:** `A gift for coming back 🎁`  
**Preview text:** `We'd love to earn your attention back.`  
**Tone:** Generous, value-forward

---

**Body:**

```
Hey {{first_name | default: "there"}},

I know inboxes are noisy — so I'll make this worth your time.

If you come back and give [Brand] another look this week,
here's what you'll get:

🎁 [Specific offer — e.g., "30-day free trial extension",
    "20% off your first month", "free onboarding call"]

This offer is available until [DATE].

[CLAIM MY OFFER →]

Why are we doing this? Because we built [Brand] for people
like you, and we want to prove it's worth your time.

Talk soon,
[Founder Name]

P.S. Questions? Just reply — I read every message.
```

**Goal:** Overcome friction with a concrete incentive.

---

## Email 3 — The Goodbye

**Send:** Day 14 (if Email 1 + 2 not opened or clicked)  
**Subject:** `Should I let you go? (honest question)`  
**Preview text:** `Last email from us — unless you want to stay.`  
**Tone:** Respectful, honest, FOMO trigger

---

**Body:**

```
Hey {{first_name | default: "there"}},

This is the last email I'll send you for a while.

I don't want to keep filling your inbox if [Brand] isn't
useful to you right now — that's not fair to you.

But before I go:

If there's anything that stopped you from getting value from
[Brand], I'd genuinely love to know. Just hit reply.

If you'd like to stay subscribed, click below — no strings:

[YES, KEEP ME SUBSCRIBED →]

Otherwise, take care, and maybe we'll cross paths again.

— [Founder Name]

---
If you do nothing, we'll remove you from our active list.
You can always resubscribe at [link].
```

**Goal:** Final re-engagement attempt + clean list pruning.

---

## Post-Sequence Actions

| Outcome | Action |
|---------|--------|
| Opened/clicked Email 1–3 | Remove from `inactive-90d`, add to `re-engaged` segment |
| No action after Email 3 | Move to `suppressed`, stop marketing emails |
| Replied | Personal follow-up from founder / support |
| Unsubscribed | Remove from all segments, respect preference |

---

## Metrics

| Metric | Benchmark | Your Baseline |
|--------|-----------|---------------|
| Email 1 open rate | 20–30% | |
| Email 2 open rate | 15–25% | |
| Email 3 open rate | 25–35% (curiosity) | |
| Overall re-engagement rate | 5–15% | |
| Unsubscribe rate | <2% per email | |

---

## Copywriting Tips

- **Use first name** in subject line when possible (+10% open rate)
- **Plain text** performs better than HTML for win-backs (feels personal)
- **Founder voice** beats brand voice for inactive subscribers
- **Single CTA** per email — don't confuse with choices
- **Email 3 subject** with "goodbye" framing typically has 30%+ higher open rate

---

_Template: Ship Engine · NEO-231_
