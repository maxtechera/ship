---
name: content-video
version: "1.0.0"
description: "Create animated and rendered video content — Remotion compositions, code animations, data visualizations."
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Content Video

Create programmatic video content: animated carousels, code animations, terminal demos, data visualizations.

## Composition Types

| Composition | Use Case | Input |
|-------------|----------|-------|
| Animated Carousel | IG carousel → video | Carousel JSON (slides with copy) |
| Code Animation | Animated code typing/highlighting | Code string + language |
| Terminal Demo | Terminal-style command execution | Commands + expected output |
| Data Chart | Animated bar/line charts | Data array + labels |
| Quote Card | Animated quote with attribution | Quote text + author |

## Default Specs

- **Dimensions**: 1080×1350 (4:5 Instagram) for carousels; 1080×1920 (9:16) for reels
- **FPS**: 30
- **Duration**: 5-60 seconds depending on type
- **Style**: Dark background, white text, green accent for code

## Script-to-Video Workflow

1. **Script exists** — hook, problem, solution, CTA with timestamp markers
2. **Identify visual moments** — what's on screen at each timestamp?
3. **B-roll map** — list which sections need supplementary footage
4. **Slide assets** — specify any carousel or text overlay slides
5. **Export spec** — dimensions, format, duration, platform target

## Talking Head Variants (HeyGen / Avatar)

When creating avatar video from script:
- Mark camera directions in script: `[look at camera]`, `[show screen]`, `[gesture left]`
- Mark text overlays: `[overlay: "key stat"]`
- Mark b-roll cuts: `[cut to: screen recording]`
- Deliver: clean script + visual cue markers + b-roll list

## Done Criteria

- [ ] Composition type and specs defined
- [ ] Script includes timestamp markers
- [ ] B-roll slots identified
- [ ] Export spec documented (dimensions, FPS, format)
- [ ] Platform target confirmed (Instagram / TikTok / YouTube)
