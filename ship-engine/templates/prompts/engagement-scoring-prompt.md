# Prompt: Design Engagement Scoring Model

> Use with: Ship Engine engine · Stage: Nurture / CRM

---

## System Context

You are a growth engineer helping a founder set up behavioral engagement scoring for their SaaS product.

---

## Prompt

```
Help me design an engagement scoring model for my product.

**Context:**
- Product: {{product_name}}
- Business model: {{business_model}} (e.g., B2B SaaS, freemium, PLG)
- CRM / ESP tool: {{crm_tool}} (e.g., HubSpot, Loops, Klaviyo, custom)
- Core user actions in-product: {{key_actions}}
  (list 5–10 key things users do, e.g., "create project", "invite teammate", "export CSV")
- Sales-assisted or self-serve: {{motion}}
- ICP characteristics: {{icp}}

**Deliverables:**
1. Scoring dimensions (Recency / Frequency / Depth) with weights
2. Complete action weight table:
   - Email engagement actions (5 items)
   - Product behavior actions (8–10 items based on my {{key_actions}})
   - Sales/support actions (4 items)
   - Demographic fit bonuses (3 items)
3. Decay schedule (what happens at 30/60/90/180 days of inactivity)
4. Score threshold segments (at least 5 tiers) with recommended actions for each
5. Top 3 automation triggers based on score changes
6. Implementation checklist for my specific {{crm_tool}}
7. Monthly review questions

Make weights realistic for a {{business_model}} product with {{motion}} motion.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{business_model}}` | Revenue model | "B2B SaaS freemium" |
| `{{crm_tool}}` | CRM or ESP being used | "HubSpot" |
| `{{key_actions}}` | Core product actions | "create launch, invite team, publish page" |
| `{{motion}}` | Sales model | "self-serve PLG" |
| `{{icp}}` | Ideal customer profile | "solo founders, <10 employees" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
