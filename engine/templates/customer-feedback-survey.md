# Customer Feedback Survey Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Overview

| Field | Value |
|-------|-------|
| **Survey Name** | e.g., "Post-Trial Feedback — Q1 2026" |
| **Product / Brand** | |
| **Target Segment** | (e.g., trial users, paying customers, churned) |
| **Delivery Channel** | Email / In-app / Link |
| **Tool** | (Typeform, Tally, Google Forms, etc.) |
| **Launch Date** | |
| **Close Date** | |
| **Owner** | |

---

## Part A — Core Satisfaction (All Users)

**Q1 — Overall satisfaction**
> How satisfied are you with `[Product Name]` overall?

☐ Very satisfied  
☐ Satisfied  
☐ Neutral  
☐ Dissatisfied  
☐ Very dissatisfied

---

**Q2 — NPS (Net Promoter Score)**
> How likely are you to recommend `[Product Name]` to a friend or colleague?

`[0 — Not at all likely]` ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ `[10 — Extremely likely]`

---

**Q3 — NPS follow-up** _(open text, required)_
> What is the main reason for your score?

`[Open text field]`

---

## Part B — Value & Fit

**Q4 — Value for money**
> `[Product Name]`'s pricing represents good value for what I get.

☐ Strongly agree  
☐ Agree  
☐ Neutral  
☐ Disagree  
☐ Strongly disagree

---

**Q5 — Core use case**
> What do you primarily use `[Product Name]` for? _(Select all that apply)_

☐ `[Use case 1]`  
☐ `[Use case 2]`  
☐ `[Use case 3]`  
☐ `[Use case 4]`  
☐ Other: ___________

---

**Q6 — PMF (Product-Market Fit) signal**
> How would you feel if you could no longer use `[Product Name]`?

☐ Very disappointed  
☐ Somewhat disappointed  
☐ Not disappointed  
☐ I no longer use it

> **Analysis note:** ≥40% "Very disappointed" = strong PMF signal (Sean Ellis benchmark).

---

## Part C — Feature Feedback

**Q7 — Most valuable feature**
> Which feature or capability do you find MOST valuable?

`[Open text field]`

---

**Q8 — Missing features**
> What's the one thing `[Product Name]` is missing that would make it significantly better for you?

`[Open text field]`

---

**Q9 — Feature satisfaction** _(matrix question)_
> Rate your satisfaction with each feature:

| Feature | Very satisfied | Satisfied | Neutral | Dissatisfied | Haven't used |
|---------|---------------|-----------|---------|--------------|--------------|
| `[Feature 1]` | | | | | |
| `[Feature 2]` | | | | | |
| `[Feature 3]` | | | | | |
| `[Feature 4]` | | | | | |

---

## Part D — Acquisition & Competitive

**Q10 — Discovery**
> How did you first hear about `[Product Name]`?

☐ Google search  
☐ Social media (specify: ___)  
☐ Friend / colleague referral  
☐ Online community (Slack, Reddit, Discord, etc.)  
☐ Newsletter / email  
☐ Blog / article  
☐ App store  
☐ Other: ___________

---

**Q11 — Alternatives considered**
> Did you evaluate any alternatives before choosing `[Product Name]`?

☐ No — `[Product Name]` was the only option I considered  
☐ Yes: ___________

---

**Q12 — Why you chose us**
> What was the main reason you chose `[Product Name]` over alternatives?

`[Open text field]`

---

## Part E — Churn Risk (for at-risk or churned users)

> _Only show to segments with low engagement score or who recently cancelled._

**Q13 — Likelihood to renew**
> How likely are you to renew / continue using `[Product Name]`?

☐ Definitely will  
☐ Probably will  
☐ Unsure  
☐ Probably won't  
☐ Definitely won't (I've already cancelled)

---

**Q14 — Reason for leaving** _(show if Q13 = "Probably won't" or "Definitely won't")_
> What is the primary reason you're leaving?

☐ Too expensive  
☐ Missing a feature I need  
☐ Switched to a competitor (which one: ___)  
☐ No longer need this type of tool  
☐ Poor customer support experience  
☐ Too hard to use / onboard  
☐ Other: ___________

---

## Part F — Open-Ended

**Q15 — Biggest frustration**
> What's your biggest frustration with `[Product Name]` right now?

`[Open text field]`

---

**Q16 — Surprise delight**
> Is there anything about `[Product Name]` that pleasantly surprised you?

`[Open text field]`

---

**Q17 — Anything else**
> Is there anything else you'd like us to know?

`[Open text field]`

---

## Part G — Respondent Profile (optional)

**Q18 — Role**
> What best describes your role?

☐ Founder / CEO  
☐ Product Manager  
☐ Marketing  
☐ Sales  
☐ Developer / Engineer  
☐ Designer  
☐ Other: ___________

**Q19 — Company size**
> How many people are in your company?

☐ Just me  ☐ 2–10  ☐ 11–50  ☐ 51–200  ☐ 200+

---

## Analysis Guide

### Scoring

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **NPS** | % Promoters (9–10) − % Detractors (0–6) | B2B SaaS avg: 30–50 |
| **PMF Score** | % "Very disappointed" | ≥40% = strong PMF |
| **CSAT** | % Satisfied + Very Satisfied | ≥80% target |

### Qualitative Coding

1. Export open-text responses to spreadsheet
2. Tag each response with 1–3 themes (e.g., `onboarding`, `pricing`, `missing-feature`)
3. Count tag frequency → priority matrix
4. Surface top 3 themes per segment (trial, paid, churned)

### Actionability Matrix

| Response theme | Frequency | Severity | Action |
|---------------|-----------|----------|--------|
| | High | High | Fix immediately |
| | High | Low | Roadmap |
| | Low | High | Investigate |
| | Low | Low | Monitor |

### Reporting Template

```markdown
## Survey Results — [Period]
- **Responses:** N
- **NPS:** XX (Promoters: XX% | Passives: XX% | Detractors: XX%)
- **PMF Score:** XX% very disappointed
- **Top missing feature:** [theme]
- **Top frustration:** [theme]
- **Discovery channel #1:** [channel]
- **Key action items:**
  1. 
  2. 
  3.
```

---

_Template: Ship Engine · NEO-231_
