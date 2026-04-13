# Prompt: Generate Funnel Visualization Spec

> Use with: Ship Engine engine · Stage: Measure / Optimize

---

## System Context

You are a data analyst and growth strategist helping a founder map, visualize, and diagnose their conversion funnel.

---

## Prompt

```
Help me design and analyze my conversion funnel for {{product_name}}.

**Context:**
- Product: {{product_name}}
- Business model: {{business_model}}
- Primary acquisition channel: {{main_channel}} (e.g., organic SEO, paid ads, community, referral)
- Analytics tool: {{analytics_tool}} (e.g., PostHog, Mixpanel, GA4, none)

**Current funnel data (fill what you know, leave blank otherwise):**
- Monthly unique visitors: {{visitors}}
- Engaged visitors (>60s or 2+ pages): {{engaged}}
- Trial / demo signups: {{trials}}
- Activated users: {{activated}} (define activation: {{activation_event}})
- Paid customers: {{paid}}
- Month-2 retained: {{retained}}

**Deliverables:**
1. Validated funnel stage definitions for my {{business_model}} model
2. Step-by-step conversion rates from the data above
3. ASCII funnel diagram (for docs/chat)
4. Identification of the biggest drop-off stage + hypothesized causes
5. 3 experiments to fix the top drop-off
6. Dashboard spec: what charts to build and in what tool ({{analytics_tool}})
7. Segmented funnel breakdowns I should run (traffic source, device, persona)
8. Weekly/monthly reporting template

For the ASCII diagram: show absolute numbers and % conversion at each step.
Flag the biggest drop-off with ⚠️.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{business_model}}` | Revenue model | "B2B SaaS, self-serve" |
| `{{main_channel}}` | Primary traffic source | "organic SEO" |
| `{{analytics_tool}}` | Your analytics platform | "PostHog" |
| `{{visitors}}` | Monthly unique visitors | "8,500" |
| `{{trials}}` | Monthly trial signups | "170" |
| `{{activation_event}}` | What counts as activated | "created first launch plan" |
| `{{paid}}` | Monthly new paying customers | "22" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
