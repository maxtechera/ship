# Welcome Email Template (Immediate)

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Purpose

Send immediately after signup to deliver promised value, build trust, and drive first activation.

---

## Setup

| Field | Value |
|------|------|
| Product / Offer | |
| Trigger | Signup completed |
| Send timing | Immediate (0-2 min) |
| From name | |
| From email | |
| Reply-to | |
| Segment/tag | |

---

## Messaging Strategy

- **Job #1:** Keep the promise made on the capture page.
- **Job #2:** Create an instant “small win.”
- **Job #3:** Set expectations for future emails.

Tone: clear, human, direct, low-hype.

---

## Subject Line Options

1. `{first_name}, you’re in — here’s your {lead_magnet}`
2. `Welcome to {product_name} (start here)`
3. `Your {lead_magnet} is ready`

**Preview text:** `Quick win in 5 minutes. Let’s go.`

---

## Email Body (Plain Text)

```
Hi {{first_name | default: "there"}},

You’re officially in — welcome to {product_name}. 🎉

As promised, here’s your {lead_magnet}:
{primary_link}

If you only do one thing today, do this:
{first_action}

It should take about {time_to_value} and gets you {specific_outcome}.

Over the next {n_days} days, I’ll send you {what_they_get}.
No fluff — just practical steps.

If you reply with "{reply_keyword}", I’ll send you the fastest path for your situation.

— {founder_name}
{title}
{brand}

P.S. If the link doesn’t work, reply and I’ll send it manually.
```

---

## Dynamic Fields

- `{lead_magnet}`
- `{primary_link}`
- `{first_action}`
- `{time_to_value}`
- `{specific_outcome}`
- `{n_days}`
- `{what_they_get}`
- `{reply_keyword}`

---

## Automation Rules

- [ ] Trigger: successful signup form submit
- [ ] Delay: 0 minutes
- [ ] Exclusion: already in customer segment
- [ ] Tag on send: `welcome-sent`
- [ ] Track events:
  - `welcome_email_sent`
  - `welcome_email_opened`
  - `welcome_email_clicked`
  - `welcome_email_replied`

---

## QA Checklist

- [ ] Subject line renders on mobile (<50 chars preferred)
- [ ] All merge tags resolve safely (fallback defaults)
- [ ] Main link works and is tracked with UTM
- [ ] One clear CTA only
- [ ] Email lands in primary inbox in seed test
- [ ] Reply-to inbox monitored

---

## Final Production Copy

### [EN]
- Subject:
- Preview:
- Body:

### [ES]
- Asunto:
- Preheader:
- Cuerpo:


_Template: Ship Engine · NEO-218_
