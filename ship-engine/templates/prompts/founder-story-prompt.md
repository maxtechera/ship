# Prompt: Generate Founder Story

> Use with: Ship Engine engine · Stage: Awareness / Brand

---

## System Context

You are a brand storyteller and copywriter helping a founder craft their authentic origin story.

---

## Prompt

```
Help me write my founder story for {{product_name}}.

**Background:**
- My name: {{founder_name}}
- My relevant background / experience: {{background}}
- Country / context: {{country_context}}

**The Problem:**
- The specific problem I kept running into: {{problem}}
- When I first noticed it: {{problem_origin}} (specific moment, date, situation)
- How I validated it wasn't just me: {{validation}} (e.g., "talked to 20 founders", "saw it in communities")

**The Insight:**
- What I realized that others hadn't: {{insight}}
- Why existing solutions failed: {{why_others_failed}}

**What I Built:**
- Product name: {{product_name}}
- What it does in plain language: {{product_description}}
- How it solves the problem: {{solution_mechanism}}

**Traction / Social Proof:**
- Current metrics: {{metrics}} (customers, MRR, users, etc.)
- Best testimonial: {{testimonial}}
- Press / community mentions: {{press}}

**Mission:**
- Why this matters beyond the product: {{mission}}

**Target formats needed:**
{{formats}}
(e.g., "short bio (2 sentences), About page (3 paragraphs), LinkedIn summary (150 words)")

Write each format in first person, founder voice. Be specific — avoid generic startup language. 
Ground the story in real moments. End each format with a subtle CTA appropriate to the context.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{founder_name}}` | Your name | "Max" |
| `{{product_name}}` | Product name | "LaunchKit" |
| `{{background}}` | Your relevant experience | "10 years in product, 3 startups" |
| `{{problem}}` | The pain you experienced | "spending 80% of time on decks not customers" |
| `{{problem_origin}}` | Specific moment it clicked | "Tuesday in Feb 2023, after my 4th failed launch" |
| `{{insight}}` | Your unique realization | "the bottleneck isn't ideas, it's structured execution" |
| `{{product_description}}` | Plain-language description | "a GTM checklist that runs itself" |
| `{{metrics}}` | Traction proof | "47 customers, $3k MRR" |
| `{{formats}}` | Output formats needed | "Twitter bio, About page, podcast bio" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
