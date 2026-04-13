# Prompt: Generate Win-Back Email Sequence

> Use with: Ship Engine engine · Stage: Retention / Re-engagement

---

## System Context

You are an email copywriter specializing in re-engagement for SaaS products.

---

## Prompt

```
Write a 3-email win-back sequence to re-engage inactive subscribers or users.

**Context:**
- Product: {{product_name}}
- Core value prop: {{value_prop}}
- Inactivity threshold: {{inactivity_days}} days
- Segment: {{segment}} (e.g., "trial users who didn't convert", "paying customers who went inactive", "email subscribers who stopped opening")
- Founder name: {{founder_name}}
- New features / updates since they went inactive: {{recent_updates}}
- Re-engagement offer (if any): {{offer}} (e.g., "30-day extension", "20% off", none)
- Brand voice: {{brand_voice}}

**Write 3 emails:**

Email 1 (Day 0) — The Check-In
- No pressure, just curiosity
- Mention what's new
- Single soft CTA

Email 2 (Day 7, if no open/click) — The Offer
- Concrete incentive: {{offer}}
- Urgency without desperation
- One CTA

Email 3 (Day 14, if still no action) — The Goodbye
- Respectful, honest
- "Last email" framing (proven to increase opens 30%+)
- Option to stay OR graceful exit

**For each email:**
- Subject line (2 options per email — test curiosity vs. direct)
- Preview text
- Body (under 200 words, plain text style)
- Post-sequence action logic

Make it feel human, not automated. Founder-signed.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{value_prop}}` | Core benefit | "launch your SaaS without a team" |
| `{{inactivity_days}}` | Days inactive before entry | "90" |
| `{{segment}}` | Who's receiving this | "free trial users who didn't upgrade" |
| `{{founder_name}}` | Your name | "Max" |
| `{{recent_updates}}` | New things since they left | "AI brief generator, team sharing" |
| `{{offer}}` | Re-engagement incentive | "30-day free extension" or "none" |
| `{{brand_voice}}` | Tone | "warm, direct, founder-y" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
