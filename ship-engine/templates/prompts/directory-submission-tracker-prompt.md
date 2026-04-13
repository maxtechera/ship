# Prompt: Generate Directory Submission List

> Use with: Ship Engine engine · Stage: Awareness / Distribution

---

## System Context

You are a growth researcher specializing in product distribution for early-stage startups.

---

## Prompt

```
Generate a prioritized list of directories and communities where I should submit my product.

**Context:**
- Product name: {{product_name}}
- Product URL: {{product_url}}
- Category: {{category}} (e.g., "SaaS", "AI tool", "developer tool", "no-code", "B2B productivity")
- Target audience: {{icp}}
- Business model: {{business_model}} (e.g., freemium, paid, open source)
- Stage: {{stage}} (e.g., pre-launch, just launched, post-launch)
- Budget for paid listings: {{budget}} (0 = free only)

**Deliverables:**
1. Top 10 FREE high-DA directories (name, URL, DA, why it fits my category, submission tips)
2. Top 5 niche directories specific to {{category}}
3. Top 3 paid listings worth considering (if {{budget}} > 0)
4. 3 communities/forums where I should post (Reddit, Indie Hackers, Slack groups, etc.)
5. Submission asset checklist (what I need to prepare)
6. Quick-win tips: which directories tend to approve fastest

For each directory, provide:
- Name + URL
- Domain Authority estimate
- Cost (Free / Freemium / Paid)
- Time to get listed (typical)
- Submission tips specific to my product category

Sort by: High DA + Free + Fast first.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{product_url}}` | Website URL | "launchkit.io" |
| `{{category}}` | Product category | "AI writing tool for founders" |
| `{{icp}}` | Target customer | "solo SaaS founders" |
| `{{business_model}}` | Revenue model | "freemium" |
| `{{stage}}` | Launch stage | "just launched (3 weeks ago)" |
| `{{budget}}` | USD/month for paid | "0" or "100" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
