# Engagement Scoring Model Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Overview

Engagement scoring assigns a numeric score to each contact based on their behavior. Use scores to prioritize outreach, trigger automations, and segment lists.

| Field | Value |
|-------|-------|
| **Product / Brand** | |
| **Scoring tool / CRM** | (HubSpot, Klaviyo, Loops, custom) |
| **Score range** | 0–100 |
| **Review cadence** | Monthly |

---

## 1. Score Dimensions

Scores are split across two axes:

| Dimension | Description | Weight |
|-----------|-------------|--------|
| **Recency (R)** | How recently they acted | 40% |
| **Frequency (F)** | How often they act | 35% |
| **Monetary/Depth (D)** | Depth of engagement (upgrades, purchases) | 25% |

---

## 2. Action Weights

### Email Engagement

| Action | Points | Notes |
|--------|--------|-------|
| Email opened | +1 | Apply decay after 30d |
| Email clicked | +3 | Strong intent signal |
| Unsubscribed | −10 | Remove from active segments |
| Marked as spam | −20 | Flag for suppression |

### Website / Product Behavior

| Action | Points | Notes |
|--------|--------|-------|
| Page visit | +1 | Max +5/day (prevent gaming) |
| Pricing page visit | +5 | High intent |
| Feature page (core) | +3 | |
| Demo / trial start | +10 | |
| Sign-up completed | +15 | |
| Logged in (active session) | +5 | |
| Invited a teammate | +10 | Viral / sticky signal |
| Integration connected | +8 | |
| File / export created | +3 | Depth of use |

### Sales & Support

| Action | Points | Notes |
|--------|--------|-------|
| Booked a call | +20 | High intent |
| Replied to email | +10 | |
| Submitted support ticket | +2 | Engagement, not necessarily good |
| Left a review (G2, etc.) | +15 | Advocate signal |
| Referred a customer | +25 | |

### Demographic / Fit Bonuses

| Attribute | Points | Notes |
|-----------|--------|-------|
| ICP job title match | +10 | |
| ICP company size match | +5 | |
| ICP industry match | +5 | |
| Decision-maker role | +10 | |

---

## 3. Score Decay

Without decay, old contacts stay artificially high.

| Inactivity Period | Decay |
|-------------------|-------|
| 30 days no action | −5 points |
| 60 days no action | −10 points |
| 90 days no action | −15 points |
| 180 days no action | Reset to 0, move to `re-engagement` segment |

**Decay runs:** Weekly automated job

---

## 4. Score Thresholds & Segments

| Score | Segment | Recommended Action |
|-------|---------|--------------------|
| 80–100 | 🔥 **Hot Lead / Power User** | SDR outreach, upsell, case study ask |
| 60–79 | 🟠 **Warm Lead / Engaged User** | Targeted nurture, feature education |
| 40–59 | 🟡 **Lukewarm** | Standard nurture sequence |
| 20–39 | 🔵 **Cold** | Re-engagement campaign |
| 0–19 | ⚫ **Dormant** | Win-back sequence or suppress |

---

## 5. Automation Triggers

| Trigger | Score threshold | Action |
|---------|----------------|--------|
| Score crosses 80 | ≥ 80 | Notify sales / create CRM task |
| Score drops from 60+ to 40 | Drops −20+ | Enter re-engagement flow |
| Score reaches 0 | = 0 | Add to win-back sequence |
| Pricing page + score ≥ 50 | AND condition | Send personalized outreach |

---

## 6. Implementation Checklist

- [ ] Map all tracked events to your analytics / product platform
- [ ] Configure scoring rules in CRM/ESP
- [ ] Set up decay job (weekly cron)
- [ ] Create segments per threshold table
- [ ] QA: test a sample contact journey from 0 → 100
- [ ] Document edge cases (e.g., bot traffic, internal users)
- [ ] Schedule monthly review to calibrate weights

---

## 7. Monthly Review Questions

1. Are "Hot" leads converting at a higher rate than "Warm"? If not, recalibrate weights.
2. Are any single actions inflating scores artificially?
3. How many contacts are in each segment? (Balance check)
4. Is decay rate too aggressive / too lenient?

---

_Template: Ship Engine · NEO-231_
