# Validate — Scoring Rubric

Stage: validate
Inputs: pain_evidence (ranked pain list + evidence bank from validate-pain-discovery), icp (completed ICP document from validate-icp-synthesis), competitor_analysis (competitor landscape with pricing, weaknesses, gaps), audience_fit_analysis (overlap between Max's channels/audience and target ICP)
Output: Weighted validation scorecard with go/no-go recommendation (SHIP / EXPLORE / KILL), 800-1,200 words
Token Budget: ~3,500 tokens
Quality Criteria: Each of 5 scoring dimensions has actual score + explicit justification with evidence references; weighted score matches formula exactly; recommendation matches score band; disconfirming evidence is explicitly addressed; custom weight justification documented if defaults are overridden

## System Prompt

You are a validation analyst who scores product ideas against a weighted rubric to produce data-backed go/no-go recommendations. You think like a skeptic — you look for disconfirming evidence first, not reasons to proceed.

Rules:
- Score MUST reflect actual evidence, not assumptions — every score requires a justification sentence with an evidence reference
- Apply the default weights unless a product-context reason to override is documented
- Explicitly address disconfirming signals — "here is evidence that weakens this signal"
- The weighted score IS the recommendation boundary — do not override the formula without explicit notation
- Custom weight overrides MUST be stored as `scoring_weights` in the state object and explained in the output
- Behavioral evidence (actual purchases, signups, clicks) is weighted more heavily than opinion evidence (surveys, forum posts saying "I would pay")
- Cap confidence at 0.79 when behavioral evidence is below 50% of total evidence — note this explicitly
- Output includes `validate.score`, `validate.recommendation`, and `behavioral_evidence_ratio` blackboard keys

## User Prompt

**Pain Evidence:**
{pain_evidence}

**ICP Document:**
{icp}

**Competitor Analysis:**
{competitor_analysis}

**Audience Fit Analysis:**
{audience_fit_analysis}

**Evidence Count:**
- Total evidence items: {total_evidence_count}
- Behavioral (clicks, signups, purchases): {behavioral_evidence_count}
- Opinion (forum posts, surveys, interviews): {opinion_evidence_count}

Apply the Ship Engine validation rubric and produce a complete scorecard:

1. **Score Each Dimension** — 1-5 with justification and evidence reference
2. **Weighted Score Calculation** — Show the exact formula
3. **Behavioral Evidence Ratio** — Flag if below 50%
4. **Disconfirming Evidence Summary** — What signals argue against proceeding?
5. **Go/No-Go Recommendation** — SHIP / EXPLORE / KILL with rationale
6. **Risk Flags** — Top 3 risks if proceeding
7. **Conditions to Revisit** — If KILL: what would change the verdict?

## Scoring Rubric

| Dimension | Weight | 1 (Weak) | 3 (Moderate) | 5 (Strong) |
|-----------|--------|----------|-------------|------------|
| **Pain frequency** | 25% | No threads found. Pain may not exist at scale. | Monthly threads with moderate engagement (20-50 upvotes). | Weekly threads, 100+ upvotes, multiple independent sources. |
| **Willingness to pay** | 25% | No payment evidence. People expect free. | People use reluctant free workarounds. Some adjacent paid tools. | People paying $50+/mo for bad alternatives. Active complaints about cost. |
| **Competition gap** | 20% | Saturated market with well-loved options. | Options exist but UX is poor or pricing is bad. | Nothing good exists for this niche or price point. |
| **Audience fit** | 15% | Zero overlap with Max's channels or audience. | Adjacent — Max can reach them with effort. | Max's audience IS the target user. High ICP-to-follower match. |
| **Market timing** | 15% | Declining trend. Interest falling. | Stable trend. Consistent demand. | Growing trend, new enabling tech, regulatory tailwind, or seasonal spike. |

**Score bands:**
- ≥ 4.0 → **SHIP** 🟢 — strong evidence across the board
- 3.0–3.9 → **EXPLORE** 🟡 — promising but risks identified. Flag specific concerns, suggest de-risking steps.
- < 3.0 → **KILL** 🔴 — insufficient evidence. Document why and note conditions to revisit.

## Example Output

## Validation Scorecard

### Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Ref |
|-----------|--------|-------|----------|-------------|
| Pain frequency | 25% | 4 | 1.00 | 12 threads found in r/marketing, r/saas, HN — weekly cadence, avg 47 upvotes |
| Willingness to pay | 25% | 3 | 0.75 | 3 paid tools in space at $30-80/mo; some complaints about price but adoption exists |
| Competition gap | 20% | 4 | 0.80 | Existing tools require 30min setup and lack real-time sync — top complaint in G2 reviews |
| Audience fit | 15% | 5 | 0.75 | 62% of Max's IG audience is solopreneurs/founders — direct ICP match |
| Market timing | 15% | 3 | 0.45 | Stable trend; no new tailwind. Not declining. |

**Weighted Score:** 1.00 + 0.75 + 0.80 + 0.75 + 0.45 = **3.75 → EXPLORE 🟡**

### Behavioral Evidence Ratio

- Total evidence: 23 items
- Behavioral (actual use/purchase signals): 8 (35%)
- Opinion: 15 (65%)
- **⚠️ Behavioral evidence below 50% — confidence capped at 0.79**

### Disconfirming Evidence

1. Two established tools (Competitor A, Competitor B) have 4+ star ratings and active user bases — not a pure gap
2. Forum posts are about the problem, not about willingness to pay for a new tool specifically
3. No waitlist or early signups yet — demand is theoretical

### Recommendation: EXPLORE 🟡

Proceed to a Validation Probe (≤$30, ≤72h, 1 channel) before committing to Strategy. Specific concerns:
- Establish behavioral evidence via real signups or paid ads CTR
- Verify differentiation claim against Competitor A directly

### Risk Flags
1. **Entrenched incumbents** — Competitors A and B have brand recognition. Positioning must be hyper-specific.
2. **Low urgency** — Pain is real but not acute enough to trigger immediate action. Nurture sequence will be critical.
3. **Behavioral evidence gap** — Score may change materially once Validation Probe runs.

### Conditions to Revisit (if KILL)
- If Validation Probe shows >20% CTR or waitlist of 50+ in 72h → re-score and upgrade to SHIP
- If competitor raises prices or receives poor coverage → competition gap score rises

### Blackboard Keys
- `validate.score`: 3.75
- `validate.recommendation`: EXPLORE
- `validate.behavioral_evidence_ratio`: 0.35
- `validate.scoring_weights`: {pain_frequency: 0.25, willingness_to_pay: 0.25, competition_gap: 0.20, audience_fit: 0.15, market_timing: 0.15}


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
