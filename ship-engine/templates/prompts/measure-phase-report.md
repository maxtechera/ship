# Measure — Phase Report

Stage: measure
Inputs: analytics_data (GA4, GSC, Meta insights, email metrics — from tools/analytics-collector.py), kpi_analysis (from measure-kpi-analyzer), ship_plan_targets (original success targets), stage9_evidence (deliverable metrics snapshots per blackboard key), phase (Phase 1 daily or Phase 2 weekly), days_since_launch
Output: Synthesized phase report — what's working, what isn't, what to iterate, channel-level breakdown, and a recommendation for Max
Token Budget: ~5,000 tokens
Quality Criteria: Synthesizes across all data sources (not just one channel); comparison to original targets in Ship Plan; identifies highest-ROI iteration opportunities (not generic advice); explicitly separates "signal" from "noise" (early data vs statistically significant trends); recommendation is concrete and actionable; Phase 1 reports are concise and diagnostic; Phase 2 reports are comprehensive with trend analysis and iteration decisions

## System Prompt

You are a growth analyst who synthesizes multi-channel launch data into clear, actionable reports for a solo founder. You separate signal from noise, find the highest-leverage iteration opportunities, and communicate clearly — no jargon, no hedge-everything language.

Rules:
- Phase 1 (first sprint, days 1-7): Daily synthesis. Concise. Focus on: are the systems working? Are we getting any signal? What's the one thing to change right now?
- Phase 2 (subsequent sprints, weeks 2+): Weekly. Comprehensive. Trend analysis. Channel comparisons. Iteration decisions.
- Always compare to original targets — not to what you hope to achieve, but to what was committed in the Ship Plan
- Separate behavioral signal (actual clicks, signups, purchases) from soft signal (comments, DMs, engagement) — weight behavioral heavily
- "Too early to tell" is acceptable for metrics with < 100 data points, but must be noted explicitly — not used as a catch-all excuse
- Channel breakdown must be honest: if Reddit is driving 80% of conversions and LinkedIn is driving 2%, say that clearly and recommend acting on it
- Highlight the one highest-leverage action — the thing that, if done well, would most move the needle in the next sprint
- Phase reports feed directly into the Measure stage verdict — they are not summaries, they are decision inputs

## User Prompt

**Analytics Data (from analytics-collector.py):**
{analytics_data}

**KPI Analysis (from measure-kpi-analyzer):**
{kpi_analysis}

**Original Ship Plan Targets:**
{ship_plan_targets}

**Stage 9 Deliverable Evidence:**
{stage9_evidence}

**Phase:** {phase} (Phase 1 daily | Phase 2 weekly)
**Days Since Launch:** {days_since_launch}
**Report Number:** {report_number} (e.g., Phase 1 Day 3, Phase 2 Week 1)

Generate the phase synthesis report:

1. **Executive Summary** (3 lines max — what happened, main finding, recommended action)
2. **Scorecard vs Targets** (actual vs target with % achievement and trend)
3. **Signal vs Noise Analysis** (what's statistically meaningful vs too early to tell)
4. **Channel Breakdown** (performance per channel — which is working, which isn't)
5. **Funnel Diagnosis** (where is the biggest drop-off?)
6. **Deliverable Performance** (Stage 9 — what's live, what's converting)
7. **Top Iteration Opportunity** (the one highest-leverage action)
8. **Full Recommendations** (max 5 specific, ordered by impact)
9. **Anomalies** (anything unexpected — positive or negative)
10. **Next Sprint Targets** (adjusted targets if data warrants revision)

---

## Example Output (Phase 1, Day 5)

## Executive Summary

Day 5 post-launch. Traffic is 68% of target — distribution is the bottleneck. Funnel conversion is excellent (18% signup rate, above target). Reddit is the standout channel at 2.3x better conversion than PH. **Recommended action: Double Reddit posting cadence immediately.**

---

## Scorecard vs Targets — Day 5

| Metric | Actual | Target | % Achieved | Trend | Status |
|--------|--------|--------|------------|-------|--------|
| Unique visitors | 1,470 | 2,000 | 73.5% | ↑ (+12% D/D) | 🟡 |
| Signups | 265 | 300 | 88% | ↑ (+8% D/D) | 🟡 |
| Signup rate | 18% | 15% | 120% | ↑ | 🟢 |
| Activation (D1) | 148 | 150 | 98.7% | ↑ | 🟢 |
| Activation rate | 55.8% | 50% | 112% | → | 🟢 |
| Revenue | $285 | $500 | 57% | ↑ (+$95/day) | 🟡 |
| MRR | $285 | — | — | — | — |
| Email open rate (sequence) | 49% | 40% | 123% | → | 🟢 |
| Email click rate | 9.1% | 8% | 114% | → | 🟢 |

**Overall: 5/8 metrics hitting or above target. Traffic is the gap.**

---

## Signal vs Noise Analysis

**Statistically meaningful (≥100 data points):**
- Landing page conversion rate: 18% on 1,470 visitors → STRONG signal. Offer and page are working.
- Reddit conversion vs. PH: 264 Reddit visitors → 54 signups (20.5%) vs 580 PH visitors → 71 signups (12.2%) → Reddit is clearly outperforming PH.
- Email sequence open rates on 265 subscribers → meaningful enough to act on.

**Too early to tell (<100 data points):**
- LinkedIn conversion: 48 visitors, 4 signups (8.3%) — could be noise. Need 2x more data before deprioritizing.
- SEO organic: 15 visitors — too early, expected at this stage.
- Free → paid conversion: 15 paying customers out of 265 signups (5.7%) — directionally concerning, but sample is too small for D5. Check again at D10.

---

## Channel Breakdown

| Channel | Visitors | Signups | Conv. Rate | Revenue | Notes |
|---------|----------|---------|------------|---------|-------|
| Reddit | 264 | 54 | 20.5% | $76 | 🟢 Best channel. r/entrepreneur post still generating visits. |
| Product Hunt | 580 | 71 | 12.2% | $133 | 🟡 Declining (expected). PH spike fading. |
| X/Twitter | 180 | 35 | 19.4% | $57 | 🟢 Strong. Thread engagement ongoing. |
| Email newsletter | 120 | 45 | 37.5% | $57 | 🟢 Best conversion rate. Small but high-quality audience. |
| Instagram | 240 | 42 | 17.5% | $19 | 🟡 Good conversion, low post-signup revenue — organic reach check needed. |
| LinkedIn | 48 | 4 | 8.3% | $19 | 🔴 Underperforming. Too early for decision but deprioritize for now. |
| Organic Search | 38 | 14 | 36.8% | $0 | 🟡 High conversion — early SEO signal. Blog posts may be indexing. |

**Key insight:** Reddit and X are the engines. Email newsletter has the highest conversion rate — focus on list growth. LinkedIn is the underperformer.

---

## Funnel Diagnosis

```
1,470 Visitors → 265 Signups (18%) → 148 Activated (55.8%) → 15 Paid (5.7% of activated)
                   ✅ HEALTHY           ✅ HEALTHY          ⚠️ WATCH
```

**Diagnosis:** Top and middle funnel are healthy. The conversion rate from activation to payment (5.7% at D5) is below the 10% target. This is early data (15 paying customers), but worth monitoring. The Day 7 Objection Killer email hasn't sent yet for most subscribers — wait for that signal before intervening.

**Primary bottleneck:** Traffic volume. Conversion rates are good; we just need more visitors.

---

## Deliverable Performance (Stage 9)

| Deliverable | Status | Live Since | Conversions | Notes |
|------------|--------|-----------|-------------|-------|
| Landing page | live | D0 | 265 signups | Converting at 18% — no changes needed |
| Blog post: "Pain Problem Nobody Talks About" | live | D2 | 38 organic visitors | Too early for SEO signal |
| Email sequence (7 emails) | live | D0 | 49% avg open rate | Strong. Day 5 social proof email sent. |
| IG Reels launch video | live | D0 | 42 signups via IG bio | Healthy. Consider second Reel. |
| Reddit post (r/entrepreneur) | live | D0 | 54 signups | Best performer — post more Reddit content. |
| Lead magnet PDF | live | D0 | 187 downloads | High engagement — consider a follow-up offer |
| Pricing page | live | D0 | 15 purchases | Low conversion rate — Day 7 email may move this |

---

## Top Iteration Opportunity

**Double Reddit posting cadence.**

Reddit is converting at 20.5% — the highest of any channel. We've only posted in r/entrepreneur. There are 5 more relevant subreddits from the channel plan (r/saas, r/startups, r/smallbusiness, r/nocode, r/entrepreneur) where the same type of post would likely perform similarly.

**Specific action:** Post in r/saas TODAY, r/startups TOMORROW, stagger one per day for the next 5 days. Use a different angle per sub (already drafted in `awareness/social/reddit-posts/`).

Expected impact: +200-400 visitors from Reddit alone. At 20.5% conversion: +40-80 signups.

---

## Full Recommendations (ordered by expected impact)

1. **Immediately: Post in r/saas, r/startups, r/smallbusiness this week** — use pre-drafted content. Reddit is clearly the engine. 1 post per day.

2. **Tomorrow: Publish second X/Twitter thread** — "What I learned from the first 5 days" with real metrics. Thread with real numbers performs well. Thread 1 is still driving traffic.

3. **Day 7: Watch free→paid conversion after Objection Killer email** — if it doesn't move the needle, consider adding a demo video or a direct outreach to the 10 most-engaged free users.

4. **Monitor organic search at Day 14** — 36.8% conversion rate on organic visitors is exceptional. If blog posts are indexing, this will compound. Check GSC for keyword data.

5. **Deprioritize LinkedIn for now** — 8.3% conversion with 48 visitors isn't enough to act on. Pause LinkedIn content production until D14 when more data is available.

---

## Anomalies

**Positive:**
- Organic search conversion rate (36.8%) — higher than any paid channel. Pain-keyword blog post may already be indexing. Check GSC at D7.
- Email click rate (9.1%) is above SaaS benchmark (typically 2-4%) — strong indication of ICP resonance.

**Negative:**
- IG → Revenue is disproportionately low ($19 revenue from 42 signups, vs $57 from 35 X signups). IG audience may be more browse-oriented than purchase-intent. Monitor closely.

---

## Next Sprint Targets (Day 7 Checkpoint)

| Metric | Day 5 Actual | Day 7 Target | Rationale |
|--------|-------------|-------------|----------|
| Unique visitors | 1,470 | 2,200 | +5 Reddit posts this week |
| Signups | 265 | 380 | Maintain 17%+ conversion |
| Activation | 148 | 215 | 56%+ activation rate |
| Revenue | $285 | $475 | Day 7 email should drive conversions |
| Free→paid rate | 5.7% | 8%+ | Day 7 Objection Killer email effect |

**Report Delivery:** This Phase 1 report delivered internally. Post a public version (real numbers, honest reflection) on X and IndieHackers for transparency + social proof.

---

### Blackboard Keys
- `measure.phase_report_{N}`: link to this report
- `measure.report_date`: {report_date}
- `measure.phase`: {phase}
- `measure.overall_verdict_current`: DOUBLE DOWN | ITERATE | MAINTAIN | KILL (preliminary, based on this report)


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
