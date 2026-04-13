# B-Roll Auto-Capture Template

> Visual asset capture guide for the Ship Engine content pipeline. Automatically generates screenshots, code snippets, terminal output, and UI captures as b-roll for content production.

---

## Purpose

Every content piece needs visuals. Instead of manually screenshotting things mid-production, this step runs **before** content creation — capturing all visual assets upfront so production agents have a rich asset library to pull from.

---

## What to Capture Per Content Format

### Reel / Short-Form Video (1280×720)
| Asset Type | Example | Notes |
|-----------|---------|-------|
| Product hero shot | Landing page above-the-fold | Viewport crop, no scroll |
| Feature demo sequence | 3-5 key screens showing core flow | Sequential captures |
| Terminal output | Build/deploy commands running | Dark theme, large font |
| Before/after | Competitor vs product side-by-side | Split-screen ready |
| Dashboard metrics | Analytics, revenue, engagement | Full-page or panel crop |

### Blog Post (1200×800)
| Asset Type | Example | Notes |
|-----------|---------|-------|
| Full-page screenshots | Landing page, pricing page | Full-page capture |
| Code snippets | Key implementation details | Syntax-highlighted, cropped |
| Architecture diagrams | System flow, pipeline visualization | Canvas-rendered |
| Competitor screenshots | Pricing pages, UI comparisons | For comparison articles |
| Step-by-step UI flow | Tutorial walkthrough frames | Sequential, annotated |

### Carousel (1080×1080)
| Asset Type | Example | Notes |
|-----------|---------|-------|
| Product UI crops | Specific features, panels | Square crop, centered |
| Metric highlights | Single KPI or chart | Large text overlay ready |
| Code blocks | Short, impactful snippets | ≤15 lines, readable at mobile size |
| Quote cards | VoC pain quotes from validation | Text on branded background |

### Thread (X/Twitter)
| Asset Type | Example | Notes |
|-----------|---------|-------|
| Product screenshots | Key screens, 1-2 per tweet | 16:9 or 4:3 |
| Terminal GIFs | Build process, deploy output | Can be static fallback |
| Metrics dashboard | Results, analytics | Cropped to relevant panel |
| Comparison tables | Feature grids | Rendered as image for thread |

---

## Asset Types & Capture Methods

### 1. Dashboard Screenshots
**Tool:** `browser` → `screenshot`
```
browser action=navigate targetUrl="https://app.example.com/dashboard"
browser action=screenshot fullPage=true type=png
```
- **Full-page:** dashboards, landing pages, pricing pages
- **Viewport:** specific panels, hero sections, feature areas
- **Resolution:** 1440px desktop, 375px mobile

### 2. Code Snippets
**Tool:** `canvas` → render code block as styled image
- Use syntax highlighting (dark theme preferred for video, light for blog)
- Max 20 lines per capture — crop to the important part
- Include filename header when relevant
- Font: monospace, 14px minimum for readability

### 3. Terminal Output
**Tool:** `exec` → capture command output, then `canvas` → render as styled terminal
```
exec command="npm run build 2>&1 | head -30"
```
- Dark background, green/white text
- Include the command prompt line
- Truncate verbose output — show the interesting part
- Large font for video (18px+), standard for blog (14px)

### 4. Before/After Comparisons
**Tool:** `browser` → screenshot both states
- Capture the "before" (competitor, old way, manual process)
- Capture the "after" (our product, new way, automated)
- Same viewport size for both — enables clean side-by-side

### 5. Telegram/Chat Messages
**Tool:** `browser` → screenshot Telegram Web or `canvas` → render chat mockup
- Capture real user feedback, pain quotes, reactions
- Blur/anonymize usernames if needed
- Crop to the relevant message thread

### 6. Architecture/Flow Diagrams
**Tool:** `canvas` → render Mermaid/SVG diagrams
- Pipeline visualizations, system architecture, user flows
- Clean, branded colors
- Export as PNG at 2x resolution for print quality

---

## File Naming Convention

```
content-assets/{brief-slug}/broll-{nn}-{description}.png
```

| Component | Format | Example |
|-----------|--------|---------|
| `{brief-slug}` | Kebab-case product/run name | `[REDACTED_PROJECT]-cc`, `ship-engine-v3` |
| `{nn}` | Zero-padded sequence number | `01`, `02`, `15` |
| `{description}` | Kebab-case short description | `landing-hero`, `terminal-deploy`, `dashboard-metrics` |

**Examples:**
```
data/content-assets/[REDACTED_PROJECT]-cc/broll-01-landing-hero-desktop.png
data/content-assets/[REDACTED_PROJECT]-cc/broll-02-landing-hero-mobile.png
data/content-assets/[REDACTED_PROJECT]-cc/broll-03-dashboard-sessions.png
data/content-assets/[REDACTED_PROJECT]-cc/broll-04-terminal-build-output.png
data/content-assets/[REDACTED_PROJECT]-cc/broll-05-competitor-pricing.png
data/content-assets/[REDACTED_PROJECT]-cc/broll-06-code-snippet-api.png
data/content-assets/[REDACTED_PROJECT]-cc/broll-07-before-after-workflow.png
```

---

## Quality Settings

| Use Case | Width | Height | Mode | Format |
|----------|-------|--------|------|--------|
| Video thumbnail / reel | 1280 | 720 | Viewport | PNG |
| Blog hero image | 1200 | 800 | Viewport | PNG |
| Full-page dashboard | 1440 | auto | Full-page | PNG |
| Mobile screenshot | 375 | 812 | Viewport | PNG |
| Carousel slide | 1080 | 1080 | Viewport crop | PNG |
| OG / social share | 1200 | 630 | Viewport | PNG |

---

## Asset Manifest

After capture, generate a JSON manifest at:
```
content-assets/{brief-slug}/manifest.json
```

**Schema:**
```json
{
  "brief_slug": "[REDACTED_PROJECT]-cc",
  "captured_at": "[REDACTED_PHONE]T16:00:00Z",
  "total_assets": 7,
  "assets": [
    {
      "id": "broll-01",
      "file": "broll-01-landing-hero-desktop.png",
      "type": "dashboard",
      "source_url": "https://cc.[REDACTED_HANDLE].dev",
      "description": "Landing page hero section — desktop viewport",
      "dimensions": "1440x900",
      "formats": ["blog", "reel", "carousel"],
      "tags": ["hero", "landing", "desktop"]
    }
  ]
}
```

The manifest enables downstream production agents to browse available assets without filesystem scanning.

---

## Post-Capture Mockup Pass (Gemini)

After raw screenshots are captured, generate mockup derivatives for marketing use.

- Canonical inputs: `screen-core-desktop.png`, `screen-core-mobile.png`
- Generator: `content-image` (Gemini-first)
- Outputs: `hero` (1200x628), `og` (1200x630), `yt-thumb` (1280x720), `ig` (1080x1080)
- Rules: preserve UI fidelity; stylize environment/device frame only; center-safe crop; no gibberish text

---

## Auto-Detection Heuristics

The b-roll agent scans the brief and strategy documents to auto-detect capturable assets:

| Pattern in Brief | Asset to Capture |
|-----------------|-----------------|
| URL mentioned | Screenshot that URL (desktop + mobile) |
| Competitor named | Screenshot competitor's landing/pricing page |
| "dashboard" or "analytics" | Capture the product's dashboard |
| Code file path | Render code snippet from that file |
| CLI command | Run command, capture terminal output |
| "deploy" or "build" | Capture build/deploy terminal sequence |
| Pricing mentioned | Screenshot pricing page/section |
| "before/after" or "comparison" | Capture both states for side-by-side |
| Community/forum link | Screenshot the thread/discussion |
