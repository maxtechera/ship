# Prompt: Generate A/B Test Plan

> Use with: Ship Engine engine · Stage: Measure / Optimize

---

## System Context

You are a conversion optimization specialist helping a founder design a rigorous A/B test.

---

## Prompt

```
I need to design an A/B test for my product. Help me fill out a complete test plan.

**Context:**
- Product: {{product_name}}
- What I want to test: {{what_to_test}}  
  (e.g., "homepage headline", "pricing page CTA", "onboarding step 2")
- Current baseline metric: {{current_metric}}  
  (e.g., "3.2% conversion rate on signup page")
- My hypothesis: {{hypothesis}}  
  (e.g., "adding social proof will increase signups")
- Weekly traffic to this page/step: {{weekly_traffic}}

**Deliverables:**
1. Refine my hypothesis using the format:  
   "We believe [change] will result in [outcome] for [audience] because [reasoning]"
2. Define the primary KPI and 2–3 secondary KPIs
3. Design Control (A) and Variant B — describe exactly what changes
4. Calculate required sample size (assuming 95% confidence, 80% power, MDE of +15%)
5. Estimate test duration in days
6. List 5 QA checks before launch
7. Define the decision criteria (when to call a winner / loser)
8. Suggest 2 follow-up tests based on the outcome

Format as a structured test plan document.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Name of your product | "LaunchKit" |
| `{{what_to_test}}` | Page / element / flow step to test | "signup page headline" |
| `{{current_metric}}` | Baseline conversion rate or metric | "3.2% signup rate" |
| `{{hypothesis}}` | Your belief about the change | "testimonials increase trust" |
| `{{weekly_traffic}}` | Approximate weekly unique visitors | "500 visitors/week" |

---

## Output Format

Ask the AI to return:
- A filled-in version of `templates/a-b-test-plan.md`
- OR a structured response matching that template's sections

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
