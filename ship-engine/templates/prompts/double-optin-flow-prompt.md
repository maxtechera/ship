# Prompt: Generate Double Opt-In Email Sequence

> Use with: Ship Engine engine · Stage: Lead Capture / Nurture

---

## System Context

You are an email marketing specialist helping a founder write a high-converting double opt-in sequence.

---

## Prompt

```
Write a complete double opt-in email sequence for my product.

**Context:**
- Product: {{product_name}}
- What subscribers signed up for: {{signup_offer}}  
  (e.g., "free GTM checklist", "weekly tips on X", "early access")
- Founder name: {{founder_name}}
- Brand voice: {{brand_voice}}  
  (e.g., "friendly and direct", "professional but warm", "bold and playful")
- Lead magnet / welcome gift: {{lead_magnet}}
- Primary value prop: {{value_prop}}

**Write 3 emails:**

Email 1 — Confirmation request (send immediately)
- Subject line (A/B test: write 2 options)
- Preview text
- Body (plain text style, single CTA)

Email 2 — Follow-up nudge (send 24h later if not confirmed)
- Subject line
- Preview text  
- Body (add urgency + remind them of what they'll get)

Email 3 — Welcome (trigger: confirmation click)
- Subject line
- Preview text
- Body (deliver lead magnet, set expectations, encourage reply)

**For each email:**
- Keep it under 200 words
- One CTA only
- Founder-signed, personal tone
- No images required (plain text converts better for DOI)

Format each email clearly labeled with Send timing, Subject, Preview, and Body.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{signup_offer}}` | What they signed up for | "free launch checklist" |
| `{{founder_name}}` | Your first name | "Max" |
| `{{brand_voice}}` | Tone descriptor | "direct and warm" |
| `{{lead_magnet}}` | The thing you deliver on confirmation | "10-step GTM PDF" |
| `{{value_prop}}` | Core benefit | "launch faster without a big team" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
