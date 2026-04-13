---
name: content-image
version: "1.0.0"
description: "Generate static visual assets — carousel slides, thumbnails, OG images, social share variants."
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Content Image

Create static visual assets: Instagram carousels, YouTube thumbnails, blog hero images, OG images, social share variants.

## Asset Types and Specs

| Asset | Dimensions | Use |
|-------|-----------|-----|
| Instagram carousel slide | 1080×1080 (1:1) or 1080×1350 (4:5) | Carousel posts |
| Instagram story | 1080×1920 (9:16) | Stories, vertical reels |
| YouTube thumbnail | 1280×720 (16:9) | Video thumbnails |
| OG image | 1200×630 | Blog/link previews |
| Twitter/X card | 1200×628 | Social share |

## Visual Brand System

### Dark Style (Default for Carousels)
- Background: Pure black
- Text: White primary, gray secondary
- Accent: Green for code/metrics, red for urgency
- Font: Large, bold, system sans-serif
- Profile header on slide 1: Avatar + handle + verified badge

### Thumbnail Style (YouTube)
- Hormozi-inspired: bold text, high contrast, face prominent if available
- Max 5 words visible at thumbnail size
- Readable on mobile (small screen)

### OG Images (Blog/Social)
- Brand background with content type badge
- Content types: Blog (blue), Guide (green), Tutorial (orange)
- Headline ≤8 words, readable without zoom

## Process

1. **Define asset type and dimensions** from brief
2. **Write copy for the visual** — headline, sub, CTA (max 5 words)
3. **Apply crop safety** — main content in center 80% of frame
4. **Specify layout** — foreground/background elements, text positioning
5. **Create batch manifest** for multi-slide assets

## Batch Manifest Format (Carousels)

```json
[
  { "slide": 1, "type": "hook", "headline": "...", "sub": "...", "cta": null },
  { "slide": 2, "type": "problem", "headline": "...", "body": "..." },
  ...
  { "slide": 8, "type": "cta", "headline": "...", "cta": "..." }
]
```

## Done Criteria

- [ ] Asset dimensions specified for each platform
- [ ] Copy is ≤5 words for thumbnails, appropriate length for carousels
- [ ] Crop safety verified (center 80% safe area)
- [ ] OG image includes title, description, branding
- [ ] Batch manifest linked for carousel assets
