# Ship Engine: Cohort Analysis Framework
<!-- NEO-222 | Ship Engine: Measure Stage -->
<!-- Purpose: Track user behavior across signup cohorts to identify retention patterns -->
<!-- Usage: Update weekly; feed insights into Weekly Report Section 3 and ITERATE stage -->

---

## What This Tracks

A **cohort** = a group of users who performed the same action in the same time window (typically: signed up in the same week).

Track three behaviors per cohort:
1. **Activation** — Did they complete the key first action? (e.g., connect bank, create invoice, or first login)
2. **Retention** — Did they return each subsequent week?
3. **Conversion** — Did they upgrade to paid (if freemium) or complete the primary goal?

---

## Cohort Grid — Weekly Retention

> **Product:** {product_name} | **Run ID:** {run_id} | **Updated:** {date}
> **Activation Event:** {define_event — e.g., "first invoice created", "first login after signup", "connected Stripe"}
> **Retention Event:** {define_event — e.g., "logged in", "sent invoice", "opened email"}

### Grid Format

| Cohort (Signup Week) | Users | Activation % | W0 | W1 | W2 | W3 | W4 | W6 | W8 |
|----------------------|-------|--------------|----|----|----|----|----|----|-----|
| Week -8 (baseline) | | % | 100% | % | % | % | % | % | % |
| Week -7 | | % | 100% | % | % | % | % | % | |
| Week -6 | | % | 100% | % | % | % | % | | |
| Week -5 | | % | 100% | % | % | % | | | |
| Week -4 | | % | 100% | % | % | | | | |
| Week -3 | | % | 100% | % | | | | | |
| Week -2 | | % | 100% | | | | | | |
| **This Week** | | % | 100% | | | | | | |

**Healthy Retention Benchmarks (SaaS / micro-tools):**
- W1: > 40% = Good, > 60% = Excellent
- W4: > 20% = Good, > 35% = Excellent
- W8: > 15% = Good (strong product-market fit signal)

---

## Conversion Cohort Grid

Track when users convert to paid (or hit the macro-conversion goal).

| Cohort (Signup Week) | Users | Paid Conv. Total | Conv. in W0 | Conv. in W1 | Conv. in W2 | Conv. in W3+ | Avg. Days to Conv. |
|----------------------|-------|-----------------|-------------|-------------|-------------|--------------|-------------------|
| Week -4 | | % | % | % | % | % | days |
| Week -3 | | % | % | % | % | % | days |
| Week -2 | | % | % | % | % | | days |
| **This Week** | | % | % | | | | |

---

## Acquisition Channel × Cohort Quality Matrix

Compare cohort quality (activation + W4 retention) broken down by acquisition source.

| Channel | Cohort Size | Activation % | W1 Ret. | W4 Ret. | Paid Conv. | Quality Score |
|---------|-------------|--------------|---------|---------|------------|---------------|
| Instagram | | % | % | % | % | ⬛ |
| Email Nurture | | % | % | % | % | ⬛ |
| Google Organic | | % | % | % | % | ⬛ |
| Direct | | % | % | % | % | ⬛ |
| Community (Skool) | | % | % | % | % | ⬛ |
| Paid (Meta) | | % | % | % | % | ⬛ |

**Quality Score Legend:**
- 🟢 High (Activation > 60% AND W4 > 25%)
- 🟡 Medium (Activation > 40% OR W4 > 15%)
- 🔴 Low (Activation < 40% AND W4 < 15%)

> 🔑 **Key Insight:** High-quality channels deserve budget and effort. Low-quality channels need creative/funnel audit before scaling.

---

## Churn Analysis

### Churn by Stage

| Stage | Churn Point | % of Total Signups Lost | Root Cause Hypothesis | Fix Priority |
|-------|-------------|------------------------|----------------------|--------------|
| Pre-Activation | Signed up but never activated | % | Onboarding friction | 🔴 High |
| Early Churn | Activated but dropped after W1 | % | No "aha moment" | 🔴 High |
| Mid-Cycle | Active W1-W3 but dropped W4 | % | Feature gap / habit not formed | 🟡 Medium |
| Long-Tail | Retained 4+ weeks then churned | % | Competitive / life event | 🟢 Low |

### Qualitative Churn Signals
- **Exit survey responses:** {paste key themes}
- **Support tickets before churn:** {categories}
- **Last action before churning:** {e.g., "viewed pricing page", "failed invoice export"}

---

## Weekly Cohort Summary (for Weekly Report)

Fill this block and paste into Weekly Report → Section 3:

```
Cohort Week:        {current week}
New Signups:        {N}
Activation Rate:    {X}%  [target: >50%]
W1 Retention:       {X}%  [target: >40%]
Best Cohort:        Week {N} — {X}% W4 retention
Weakest Cohort:     Week {N} — {X}% W4 retention
Best Channel:       {channel} — {quality score}
Action:             {one specific improvement for next week}
```

---

## Setup Notes

### Data Sources
- **Activation & Retention:** Use GA4 Explorations → Cohort Exploration (or manual Stripe/DB query)
- **Paid Conversion:** Stripe Dashboard → Customers → filter by `created_at` week + plan
- **Channel Attribution:** Link to Attribution Model scorecard (same run ID)

### Tracking Requirements
- GA4 event `sign_up` must fire on confirmed signup (not form submit)
- GA4 event `activation_complete` must fire on the defined activation event
- `user_id` must be set in GA4 to enable cross-session cohort tracking
- Stripe customer metadata must include `utm_source` and `signup_week`

### Export Process
1. GA4 → Explore → Cohort → Export CSV weekly
2. Paste into cohort grid above
3. Highlight anomalies (>5% WoW change in any cohort metric)
4. Add to Weekly Report and share with Max

---

**Owner:** Ship Engine — Measure Stage
**Data Sources:** GA4 Cohort Exploration, Stripe, MailerLite
**Cadence:** Updated every Monday for the prior week
**Reference:** Linked in Weekly Report → Section 3
