# Measure — Retrospective

Stage: measure
Inputs: full_run_data (all stage outputs, timelines, and artifacts from the entire ship run), lessons (blockers encountered, workarounds used, what surprised us), final_metrics (final performance data at verdict time), verdict (DOUBLE DOWN / ITERATE / MAINTAIN / KILL)
Output: Structured retrospective document that captures everything worth remembering for future ship runs
Token Budget: ~5,000 tokens
Quality Criteria: Covers all 8 stages with specific observations; includes quantified outcomes (not just feelings); documents what worked AND what didn't with equal honesty; actionable improvements for the engine itself; timeline with actual vs expected durations; cost breakdown actual vs budget

## System Prompt

You are a retrospective facilitator who extracts maximum learning from product launches. You document with brutal honesty — celebrating wins and dissecting failures with equal rigor. Your retrospectives are referenced by future ship runs to avoid repeating mistakes and to replicate successes.

Rules:
- Structure: What happened → What worked → What didn't → What we learned → What we'd change
- Every observation must be SPECIFIC and QUANTIFIED: "Reddit posts converted at 18.6% vs 8.9% on LinkedIn" not "some channels worked better than others"
- Document the ENGINE's performance (process, tools, automation) separately from the PRODUCT's performance (market fit, pricing, conversion)
- Include timeline analysis: which stages took longer than expected? Why? What was the critical path?
- Include cost analysis: budget vs actual spend across all categories
- Document every blocker and how it was resolved (or not)
- Capture "happy accidents" — unexpected things that worked well
- Capture "assumptions that were wrong" — what we believed going in that turned out to be false
- End with concrete, actionable improvements: things to change in the Ship Engine process for next run
- This document becomes part of the institutional memory — write it for someone running the engine 6 months from now

## User Prompt

**Full Run Data:**
{full_run_data}

**Lessons & Blockers:**
{lessons}

**Final Metrics:**
{final_metrics}

**Verdict:** {verdict}

Write a complete retrospective covering:

1. **Run Summary** — Product, dates, verdict, one-paragraph summary
2. **Timeline Analysis** — Actual vs expected duration per stage, critical path
3. **Stage-by-Stage Review** — What happened, what worked, what didn't in each stage
4. **Metrics Summary** — Final numbers vs targets, best/worst performing channels
5. **Cost Analysis** — Budget vs actual across all categories
6. **Top Wins** — 5 things that worked best (quantified)
7. **Top Failures** — 5 things that didn't work (with diagnosis)
8. **Wrong Assumptions** — What we believed that was false
9. **Happy Accidents** — Unexpected wins
10. **Engine Improvements** — Specific changes to Ship Engine process for next run

## Example Output

# Retrospective: {product_name}

**Run:** {ticket_id} | **Dates:** {start_date} → {end_date} ({total_days} days)
**Verdict:** ITERATE 🟡 (62% of targets achieved)

## Summary
{product_name} launched on {launch_date} after a {total_days}-day ship run. Validation was strong (score 4.2/5), but we underestimated the distribution challenge. Funnel conversion rates hit targets, but traffic volume fell short. Reddit emerged as the surprise best channel. Total cost: ${actual_cost} vs ${budgeted_cost} budget.

## Timeline Analysis

| Stage | Expected | Actual | Delta | Notes |
|-------|----------|--------|-------|-------|
| Intake | 1 day | 0.5 days | -0.5d | Max dropped a detailed brief |
| Validate | 3 days | 4 days | +1d | Competitor research took longer — 12 competitors, not expected 5 |
| Strategy | 2 days | 2 days | On track | — |
| Parallel (Awareness) | 5 days | 7 days | +2d | Video production blocked on talent availability |
| Parallel (Lead Capture) | 3 days | 3 days | On track | — |
| Parallel (Nurture) | 3 days | 2 days | -1d | Email templates faster than expected |
| Parallel (Closing) | 4 days | 5 days | +1d | Stripe webhook testing had issues |
| Launch | 1 day | 1 day | On track | — |
| Measure (to verdict) | 14 days | 14 days | On track | — |
| **Total** | **19 days** | **22 days** | **+3d** | Critical path: video production |

## Top 5 Wins
1. **Reddit conversion rate: 18.6%** — 3x higher than any other channel. Value-first posts in r/SaaS drove most qualified traffic.
2. **Email sequence open rate: 47%** — VoC-driven subject lines significantly outperformed industry average (21%).
3. **Landing page conversion: 15%** — Problem-first hero section validated. A/B tested against feature-first, won by 40%.
4. **Activation rate: 50.5%** — "Connect one tool" onboarding CTA was the right move. Previous iteration tried "set up your dashboard" — too vague.
5. **Time to first revenue: 6 hours post-launch** — Founding member pricing drove 3 sales within first 6 hours.

## Top 5 Failures
1. **LinkedIn generated only 45 visitors (3.6% of total)** — Professional tone didn't match ICP's casual online behavior. ICP uses LinkedIn to scroll, not to discover tools.
2. **Video content wasn't ready for launch day** — Talent recording delayed by 3 days. AI first-pass was good for review but not publishable.
3. **Only 2 Reddit posts were live on L-Day** — Should have had 5+ subreddit posts pre-written and staggered. Lost day-1 momentum.
4. **PH rank: #8** — Below target of top 5. Supporter rally started too late (L-1 instead of L-7). Community warming was insufficient.
5. **SEO traffic negligible (20 visitors in 14 days)** — Expected, but blog posts should have been published 2+ weeks pre-launch for indexing.

## Wrong Assumptions
- **"LinkedIn is where our ICP discovers tools"** → FALSE. They discover on Reddit and X, then validate on LinkedIn. Distribution effort was wasted.
- **"5 blog posts is enough for launch SEO"** → FALSE. Need 2-4 weeks of indexing time. Should publish in pre-launch phase.

## Engine Improvements for Next Run
1. **Publish blog posts 2 weeks before launch** — SEO needs indexing time. Move blog production to early parallel phase.
2. **Pre-write all Reddit posts during parallel phase** — Don't write on L-Day. Have 5-8 subreddit posts ready to go.
3. **Start supporter rally at L-7, not L-1** — Warm up supporters with product preview, feedback requests, and build-in-public content.
4. **Add a "channel experiment budget"** — Allocate 10% of time/budget to testing unexpected channels early in parallel phase.
5. **Video production: get talent availability confirmed during Strategy** — Block recording time before parallel phase starts.


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
