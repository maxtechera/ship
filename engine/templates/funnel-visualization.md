# Funnel Visualization Spec Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Overview

| Field | Value |
|-------|-------|
| **Product / Brand** | |
| **Funnel Name** | e.g., "Acquisition Funnel — Organic" |
| **Period** | e.g., Jan 2026 |
| **Data source** | (PostHog, Mixpanel, GA4, custom) |
| **Owner** | |

---

## 1. Funnel Stages

Define your stages before visualizing. Customize to your GTM model.

### Standard SaaS Funnel

| Stage | Name | Description | Entry event |
|-------|------|-------------|-------------|
| 0 | **Awareness** | Visitor discovers the product | First page view |
| 1 | **Interest** | Engages with content / site | >1 page view OR pricing visit |
| 2 | **Consideration** | Starts trial / demo request | Trial signup OR book-a-demo form |
| 3 | **Intent** | Activates (uses core feature) | Activation event (define below) |
| 4 | **Conversion** | Becomes paying customer | First payment |
| 5 | **Retention** | Uses product repeatedly | Active in month 2+ |
| 6 | **Advocacy** | Refers others | Referral sent OR review posted |

**Your activation event (Stage 3):**  
> _"A user has activated when they [specific action] within [X] days of signing up."_  
> Example: "Connected first integration within 7 days."

---

## 2. Stage Metrics

| Stage | Key Metric | Formula | Benchmark | Yours |
|-------|-----------|---------|-----------|-------|
| Awareness | Unique visitors | Sessions (deduplicated) | — | |
| Interest | Engaged visitors | Visitors > 60s OR 2+ pages | 20–40% of visitors | |
| Consideration | Trial/demo rate | Trials / Unique visitors | 2–8% | |
| Intent | Activation rate | Activated / Trials | 30–60% | |
| Conversion | Trial-to-paid | Paid / Trials | 15–30% | |
| Retention | Month-2 retention | MAU month 2 / Month 1 | 30–50% | |
| Advocacy | Referral rate | Referrals / Customers | 5–15% | |

---

## 3. Conversion Rates (Step-to-Step)

| Transition | Rate | Formula | Your Rate |
|------------|------|---------|-----------|
| Awareness → Interest | | Interest / Awareness | |
| Interest → Consideration | | Consideration / Interest | |
| Consideration → Intent | | Intent / Consideration | |
| Intent → Conversion | | Conversion / Intent | |
| Conversion → Retention | | Retention / Conversion | |
| Retention → Advocacy | | Advocacy / Retention | |
| **Overall (Awareness → Paid)** | | Paid / Visitors | |

---

## 4. Visual Layout Spec

### ASCII / Text Funnel (for docs/Telegram)

```
Awareness       [███████████████████████] 10,000 visitors
                         ↓ 25%
Interest        [██████████████]          2,500 engaged
                         ↓ 8%
Consideration   [████████]                200 trials
                         ↓ 50%
Intent          [████]                    100 activated
                         ↓ 30%
Conversion      [█]                       30 paying customers
                         ↓ 60%
Retention       [█]                       18 retained (M2)
```

### Chart Spec (for dashboards)

| Property | Value |
|----------|-------|
| **Chart type** | Vertical funnel / horizontal bar / Sankey |
| **Color scheme** | Top: blue gradient → bottom: green (or brand colors) |
| **Labels** | Show absolute numbers + % conversion on each step |
| **Comparison** | Period-over-period (current vs. prior 30d) |
| **Highlight** | Biggest drop-off stage (red annotation) |
| **Tool** | Figma / Excalidraw / PostHog / Metabase / Google Sheets |

### Figma/Excalidraw Frame Dimensions

- Width: 1200px (dashboard) / 800px (slide)
- Height: auto (based on stage count × 80px min)
- Padding: 40px
- Font: Inter / system-ui

---

## 5. Drop-Off Analysis

For each major drop-off, document:

| Drop-off Point | Current Rate | Hypothesized Cause | Experiment |
|---------------|-------------|-------------------|------------|
| Awareness → Interest | | | |
| Consideration → Intent | | | |
| Intent → Conversion | | | |

---

## 6. Segmented Funnels

Run the funnel separately for:

| Dimension | Segments |
|-----------|----------|
| Traffic source | Organic / Paid / Social / Direct / Referral |
| Device | Desktop / Mobile |
| Geography | Top 3 markets |
| Persona | ICP vs. non-ICP |
| Cohort | Week of signup |

---

## 7. Reporting Cadence

| Funnel View | Cadence | Owner | Audience |
|-------------|---------|-------|----------|
| Full funnel snapshot | Weekly | | Team |
| Conversion rate trends | Monthly | | Founder |
| Segmented breakdown | Monthly | | Marketing |
| Anomaly alerts | Real-time | | On-call |

---

## 8. Funnel Health Checklist

- [ ] All stages have clean event tracking (no sampling, no gaps)
- [ ] Activation event is defined and logged
- [ ] Funnel excludes internal traffic (employee IPs)
- [ ] Timezone is consistent across all tools
- [ ] Period comparison is same-length windows (no 28d vs. 31d)
- [ ] Attribution model documented (first touch / last touch / linear)

---

_Template: Ship Engine · NEO-231_
