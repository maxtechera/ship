# Critic Rubric — Validate (Stage 2)

Applies to: `validate.validation_report`, `validate.icp`

## Validation Report Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | Evidence sourced | Every major claim has ≥1 source URL | Any claim without a source URL |
| 2 | Pain quotes real | ≥5 verbatim quotes with source + date | Invented or paraphrased quotes |
| 3 | Evidence breadth | ≥3 independent source types (Reddit, X, reviews, etc.) | <3 source types |
| 4 | Disconfirming evidence | ≥2 disconfirming signals documented | No disconfirming signals at all |
| 5 | Behavioral evidence ratio | `behavioral_evidence_ratio` ≥50%, or confidence capped at 0.79 | Behavioral ratio <50% AND confidence >0.79 without Max override |
| 6 | Scoring arithmetic | Weighted scores correct; weights sum to 100% | Arithmetic error OR missing weight breakdown |
| 7 | Score-evidence consistency | Score ≥4.0 requires ≥3 strong sources per scored dimension | Score 4+ with only 1-2 thin sources per dimension |
| 8 | Recommendation matches score | SHIP if ≥4.0, EXPLORE if 3.0-3.9, KILL if <3.0 | Score and recommendation contradict |
| 9 | Falsifiable assumptions | ≥3 riskiest assumptions listed with test method + kill condition | No falsifiable assumptions listed |
| 10 | Gate-V minimum evidence | Includes ≥2 independent evidence types AND ≥2 disconfirming signals | Evidence mix insufficient for Gate-V |

## ICP Document Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 11 | ICP is specific | Role + seniority + company size + geography named | "Developers" or other vague category |
| 12 | VoC bank populated | ≥10 copy-ready quotes in VoC bank | <10 quotes or paraphrased |
| 13 | Pain triggers described | ≥3 specific trigger moments documented | Generic or missing trigger scenarios |
| 14 | Channel map present | ≥3 specific channels where ICP spends time | No channel map |
| 15 | Competitor analysis | ≥2 competitors with pricing + weaknesses cited | Missing competitors |

## REVISE output required
List each failing check number + specific fix instruction (what content is needed, where to find it).
