# Prompt: Generate Customer Feedback Survey

> Use with: Ship Engine engine · Stage: Validate / Measure

---

## System Context

You are a customer research specialist helping a founder design a high-response feedback survey.

---

## Prompt

```
Help me design a customer feedback survey for {{product_name}}.

**Context:**
- Product: {{product_name}}
- Survey goal: {{survey_goal}}
  (e.g., "understand why free trials don't convert", "measure NPS baseline", "find top missing features", "understand churn")
- Target segment: {{segment}}
  (e.g., "paying customers", "churned users in last 30d", "free trial users who didn't upgrade", "all subscribers")
- Delivery channel: {{channel}} (e.g., email, in-app, Typeform link)
- Max questions: {{max_questions}} (recommended: 8–12 for email, up to 20 for in-app)
- Key hypotheses I want to test: {{hypotheses}}

**Deliverables:**
1. A tailored survey with {{max_questions}} questions for my {{segment}} audience
2. Question types: mix of NPS (scale), CSAT (multiple choice), PMF signal, and open-text
3. Include a PMF question (Sean Ellis method) if appropriate for my stage
4. Include NPS question with follow-up
5. 3–5 questions specific to my {{survey_goal}}
6. Suggested question order (warm-up → core → open-ended → profile)
7. Subject line + intro email copy to send with the survey link (under 100 words)
8. Analysis guide:
   - How to calculate NPS
   - How to qualitatively code open-text responses
   - What thresholds signal action needed

Format as a complete survey document ready to import into Typeform or similar.
Include answer options for all closed questions.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{survey_goal}}` | Primary research question | "why free trials don't upgrade" |
| `{{segment}}` | Who receives the survey | "trial users who didn't convert in last 60d" |
| `{{channel}}` | How to deliver it | "email with Typeform link" |
| `{{max_questions}}` | Question count limit | "10" |
| `{{hypotheses}}` | What you think the answer is | "pricing too high, missing integrations" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
