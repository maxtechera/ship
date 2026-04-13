# Meta Persona Callouts Playbook: {product_name}

> Execution guide for translating the Ship Engine persona hook library into Meta creatives.
> Source of truth: `openclaw-config/skills/engine/templates/persona-hook-library.md`

## Input Contract
- Persona and hook definitions must come from the persona hook library.
- Do not invent new avatars inside ad execution.
- Every creative variant must map to a `Hook ID`.

## Lane Definitions

| Lane | Objective | Audience | Hook source | Reporting bucket |
|------|-----------|----------|-------------|------------------|
| Organic social | Signal discovery + trust | Follower + algorithmic reach | Persona hook library | organic |
| Paid prospecting | New demand capture | Cold audiences | Persona hook library | paid.prospecting |
| Paid retargeting | Conversion recovery | Warm visitors/engagers | Persona hook library | paid.retargeting |

## Creative Rules

| Rule | Requirement |
|------|-------------|
| Hook architecture | Keep `Persona + Pain + Outcome + Mechanism + Proof + CTA` intact |
| Proof depth | Prospecting uses strongest proof first (demo/metric/case) |
| CTA clarity | One CTA per creative, aligned to funnel stage |
| Variant discipline | Change one major variable per test cell |

## Plain-Text Constraint (Required)

- Plain white text creatives are retargeting/brand-equity constrained, not default top-of-funnel.
- For top-of-funnel prospecting, default to richer creative context (visual mechanism + proof signal).

## Workflow Checklist
- [ ] Select avatar band (3-12 active avatars) from persona library.
- [ ] Build variants from existing hook IDs only.
- [ ] Tag each asset with lane: `organic`, `paid.prospecting`, or `paid.retargeting`.
- [ ] Log every variant into the persona-callouts pack test matrix.
- [ ] Keep losing variants out of scale campaigns until rule-based promotion criteria are met.
