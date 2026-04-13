---
name: content
version: "1.0.0"
description: "Content creation skill suite — 17 specialized skills covering copy, video, image, distribution, analytics, and the feedback loop."
argument-hint: 'content copy, content blog, content video, content waterfall, content measure'
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
user-invocable: true
triggers:
  - content
  - content copy
  - content blog
  - content video
  - content waterfall
  - content measure
  - content distribution
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env: []
      optionalEnv: []
      bins: []
    tags:
      - content
      - copy
      - video
      - blog
      - distribution
      - analytics
---

# Content

17-skill content creation suite. From idea to publish to measurement.

Collocated inside ship — extract to its own repo if the family grows too large.

---

## Skill Map

| Skill | Use For |
|-------|---------|
| [copy](skills/copy/SKILL.md) | Voice-constrained copy for any platform |
| [page](skills/page/SKILL.md) | Landing, pricing, comparison, thank-you pages |
| [image](skills/image/SKILL.md) | Carousels, thumbnails, OG images, social visuals |
| [video](skills/video/SKILL.md) | Animated video, Remotion compositions, code demos |
| [blog](skills/blog/SKILL.md) | SEO posts, comparison posts, launch narratives |
| [offer](skills/offer/SKILL.md) | Offer stack, guarantees, objection handling |
| [form](skills/form/SKILL.md) | Lead capture forms, spec + integration wiring |
| [distribution](skills/distribution/SKILL.md) | Publish + schedule across platforms, UTM generation |
| [broll](skills/broll/SKILL.md) | B-roll sourcing, screen recordings, visual assets |
| [storyboard](skills/storyboard/SKILL.md) | Shot-by-shot planning before production |
| [talent](skills/talent/SKILL.md) | Talent handoff — script + storyboard + recording brief |
| [compose](skills/compose/SKILL.md) | Pillar draft with research evidence and voice constraints |
| [waterfall](skills/waterfall/SKILL.md) | 1 pillar → 10+ platform derivatives + hook variants |
| [repurposing](skills/repurposing/SKILL.md) | Viral pattern analysis + multi-format derivation |
| [multiplication](skills/multiplication/SKILL.md) | Long-form → Shorts + Reels + carousel + thread + newsletter |
| [measure](skills/measure/SKILL.md) | Analytics query → asset score → feedback events |
| [feedback-loop](skills/feedback-loop/SKILL.md) | Ship → Measure → Log → Apply, pattern extraction |

Production orchestration: [engine/SKILL.md](engine/SKILL.md) — queue management and scheduling.

---

## Routing Rules

- Start with `compose` when source material exists but needs a pillar draft
- Use `waterfall` immediately after `compose` to multiply across platforms
- Use `offer` + `page` + `form` together for conversion asset packages
- Use `copy` + `image` + `video` for standalone content production
- Use `distribution` only after asset QA is complete
- Use `storyboard` and `broll` before final video rendering
- Use `measure` → `feedback-loop` to close the learning cycle after publish

---

## Ship Engine Integration

Content skills are called by ship-engine's Awareness, Lead Capture, and Measure stages.
Stage supervisors delegate asset creation here — ship-engine handles orchestration and gate logic.

The critic (`supervisors/critic/`) evaluates content output before deliverables move to `verified`.
