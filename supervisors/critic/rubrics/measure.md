# Critic Rubric — Measure (Stage 8)

Applies to: analytics report, asset scores, feedback events, retrospective

## Analytics Report Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | Report window defined | Start + end date explicit | Missing or vague window |
| 2 | Key metrics present | Sessions, conversions, signups, revenue — all sourced from GA4/PostHog | Any key metric missing |
| 3 | Comparison baseline | Current period vs prior period or launch baseline | No comparison baseline |
| 4 | Top performers identified | ≥3 best-performing assets or channels with data | Vague or missing |
| 5 | Underperformers identified | ≥2 underperforming assets with specific metrics | Missing |

## Asset Score Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 6 | Score methodology consistent | Same scoring formula used across all assets | Mixed or ad-hoc scoring |
| 7 | Engagement data sourced | Clicks, opens, or plays from real analytics (not estimated) | Estimated or missing |
| 8 | Score → action mapped | Each underperformer has a proposed fix or archive decision | Scores without action |

## Feedback Loop Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 9 | Patterns extracted | ≥3 patterns documented (what worked + why, what didn't + why) | No patterns or vague observations |
| 10 | Patterns routed | Each pattern filed to correct destination (AGENTS.md, MEMORY.md, Obsidian, rubric update) | Patterns noted but not routed |
| 11 | Next cycle seeded | ≥1 concrete hypothesis or experiment for next cycle generated | Missing forward-looking output |

## REVISE output required
List each failing check + specific fix instruction.
