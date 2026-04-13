---
name: content-waterfall
version: "1.0.0"
description: "Turn one pillar draft into a 10+ platform bundle with hook variants and a draft scheduling plan."
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Content Waterfall

Generate a multi-platform bundle from a single pillar asset.

## Inputs Required

- Pillar draft asset (from `content-compose` or existing piece)
- Research refs used for grounding
- Offer/CTA rules for the run
- Channel cadence constraints (which platforms, which days)

## Derivative Matrix

From 1 pillar, produce all applicable derivatives:

| Derivative | Platform | Notes |
|-----------|----------|-------|
| Reel script | Instagram / TikTok | Hook + problem + solution + CTA, ≤60s |
| IG caption | Instagram | 150-300 words, 5-10 hashtags |
| IG carousel | Instagram | 8-10 slides, hook slide + value slides + CTA slide |
| X/Twitter thread | Twitter/X | 6-10 tweets, hook tweet first |
| LinkedIn post | LinkedIn | Professional angle, metrics-led, longer form |
| Newsletter block | Email | Personal angle, conversational |
| YouTube description | YouTube | SEO-structured, chapters if long-form |
| TikTok caption | TikTok | 100-150 words, 3-5 hashtags |
| Avatar script | HeyGen / Synthesia | Script + visual cue markers |
| CTA variants (3) | All | Cold / warm / hot temperatures |
| Comment reply pack (5) | All | Seed replies for engagement |
| Hook variants (5) | All | Per-platform alternatives for testing |

## Hook Engine

Before finalizing the bundle, generate per-platform hook variants:
- 5 hook options per primary platform
- Select 1 primary + 2 alternates per platform for A/B testing
- Hooks must use VoC language — never generic claims

## Draft Schedule Plan

Suggest a posting schedule that fills calendar gaps:

```
Day 0: Primary reel (anchor piece)
Day 1: Carousel (expands on key point from reel)
Day 2: Thread (data/proof angle)
Day 4: LinkedIn (professional framing)
Day 7: Newsletter block
Day 10: Republish variant (short format)
```

## Verification

- Per-platform formatting is correct (character limits, aspect ratios, hashtag counts)
- CTAs align with run offer and do not contradict strategy
- No generic AI filler; hooks are specific and grounded in evidence
- Lineage is documented: which claim in each derivative came from the pillar

## Required Outputs

- [ ] All applicable derivatives (platform-formatted)
- [ ] Hook variants (5 per primary platform)
- [ ] CTA variants (3 temperatures)
- [ ] Draft schedule plan
- [ ] Comment reply pack (5)

## Handoff to Distribution

After waterfall completes:
→ Pass bundle + UTM requirements to `content-distribution`
→ Distribution generates UTM manifest and publishes
