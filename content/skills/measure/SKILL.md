---
name: content-measure
version: "1.0.0"
description: "Snapshot asset-level performance, score assets against baselines, and emit feedback events."
allowed-tools: Bash, Read, Write, Edit
user-invocable: true
---

# Content Measure

Measurement produces evidence and next actions — not just numbers.

## When to Use

- 24-48 hours after publishing (day-1 snapshot)
- 7 days after publishing (week-1 snapshot)
- When comparing performance across a batch of assets
- To close the feedback loop before the next production cycle

## Inputs Required

- Published asset URLs/permalinks
- Analytics access (GA4, platform native insights, or manual metrics)
- Measurement window (24h / 72h / 7d)

## Required Outputs

- [ ] **Metrics snapshots** per live asset — date range + source table (not estimated)
- [ ] **Asset score** — relative performance vs baseline or prior batch
- [ ] **Winner/loser list** — top 3 performers, bottom 2 underperformers
- [ ] **Feedback events** — what to change next, mapped to a specific action

## Metrics to Capture (by Platform)

| Platform | Key metrics |
|----------|------------|
| Instagram Reel | Views, reach, saves, shares, profile visits, retention % at 3s/midpoint |
| Instagram Carousel | Impressions, reach, saves, link clicks |
| YouTube Short | Views, watch time %, subscribers gained |
| Blog | Sessions, avg time on page, scroll depth, CTA clicks |
| Email | Open rate, click rate, unsubscribes |
| Landing page | Sessions, form submissions, conversion rate |

## Scoring

Score each asset against two baselines:
1. **Your average** — how does this compare to your own past 30 days?
2. **Batch average** — how does this compare to other assets in the same batch?

Score: `above / on-par / below` (qualitative) + the specific metric gap

## Feedback Events Format

```
Asset: [URL or ID]
Result: [metric] [value] ([above/below] [baseline by X%])
Pattern: [what this tells us — specific, not generic]
Action: [what to do differently next time — specific, actionable]
Routed to: [copy approach / hook formula / posting time / format choice]
```

**Example:**
```
Asset: reel/2026-04-10-claude-roi
Result: 3s retention 45% (below batch avg of 62%)
Pattern: Talking-head opener drops retention faster than visual/text opener
Action: Next 3 reels — open with text overlay or screen capture, not face
Routed to: storyboard → hook section → visual-first rule
```

## Rules

- Every number includes date range and source (no "I think it got X views")
- No fabricated metrics — if data isn't available, note what's missing and why
- Feedback events must be executable (mapped to a specific skill or decision)

## Done Criteria

- [ ] Metrics snapshots per asset with date range and source
- [ ] Asset scores (vs your baseline AND batch average)
- [ ] Winner/loser list
- [ ] Feedback events with routing (where the learning goes next)
- [ ] Attribution caveats noted where applicable
