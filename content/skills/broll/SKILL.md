---
name: content-broll
version: "1.0.0"
description: "Source and create supplementary footage — screen recordings, code demos, stock footage, AI visuals."
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Content B-Roll

Create and source supplementary visual assets that support the main content.

## B-Roll Categories

### 1. Screen Recordings
Capture real tool usage, code editing, terminal commands.
- **Use cases**: VS Code demo, terminal commands, browser workflow, dashboard walkthrough
- **Rules**: Clean desktop, relevant tabs only, zoom into important areas, no personal data visible
- **Spec**: 1920×1080 minimum, export as MP4

### 2. Code Visuals
Programmatic code animations — not screen recordings, but designed visuals.
- **Use cases**: Syntax-highlighted code snippets, terminal sequences, before/after code
- **Rules**: Max 15 lines visible, language-appropriate highlighting, readable at mobile size

### 3. Data Visualizations
Charts, metrics, before/after comparisons.
- **Use cases**: Performance metrics, comparison charts, growth graphs, cost breakdowns
- **Rules**: One data point per visual, clear labels, brand colors, animate the reveal

### 4. AI-Generated Images
Custom illustrations, concept art, backgrounds.
- **Fallback**: Use `content-image` skill for static AI images when video not needed

### 5. Stock Footage
Real-world context clips for abstract concepts.
- **Sources**: Pexels, Pixabay (license-free), Unsplash video
- **Rules**: Verify license before use, prefer authentic over generic

## B-Roll Manifest Format

Document every captured asset:

```json
{
  "assets": [
    {
      "id": "broll-001",
      "type": "screen_recording",
      "description": "Terminal: running pnpm dev",
      "duration_sec": 12,
      "file": "broll-001-pnpm-dev.mp4",
      "use_at": "section: demo",
      "notes": "Zoom to 150% during command execution"
    }
  ]
}
```

## Rules

- Organize assets by topic/section, not chronology
- Every asset gets an ID for easy reference in the edit
- Screen recordings: no personal data, no irrelevant tabs
- Stock footage: always verify license
- Minimum 3 b-roll assets per video piece

## Done Criteria

- [ ] B-roll manifest created with all assets documented
- [ ] Assets organized by section/topic
- [ ] Licenses verified for any stock footage
- [ ] File format and dimensions confirmed (MP4, correct aspect ratio)
- [ ] No personal data visible in screen recordings
