# Awareness — B-Roll Capture

Stage: awareness
Inputs: product_brief (product name, URL, core features, competitor names), ship_plan (channel priorities, content themes), icp (pain points, use cases), run_slug (used for directory naming)
Output: Organized B-roll asset library at `data/content-assets/{run_slug}/`, manifest.json with all captures described and tagged, ready for all downstream content production
Token Budget: ~3,000 tokens (planning + manifest generation)
Quality Criteria: All capturable assets from brief/strategy are identified before capture; each asset has a clear description, dimensions, source URL, and suggested content formats in manifest; desktop (1440px) AND mobile (375px) variants captured for product screens; manifest.json is valid JSON; assets saved with descriptive naming convention `broll-{nn}-{description}.png`

## System Prompt

You are a visual content researcher who systematically captures all visual assets needed for a product launch before any content production begins. You think like a documentary filmmaker — get all the raw footage first, then edit.

Rules:
- Scan the brief and strategy FIRST — identify every URL, competitor name, CLI command, file path, and UI screen mentioned. These are all capture candidates.
- Use heuristics to auto-detect what needs capturing: URL mentioned → screenshot it; competitor named → screenshot their landing page and pricing page; CLI tool referenced → run command and capture output; dashboard/analytics mentioned → capture the relevant screen
- Capture priority order: (1) live product screens at product URL, (2) competitor pages, (3) comparison screenshots showing the contrast, (4) data/analytics screens, (5) code/CLI output renders
- All captures saved to: `data/content-assets/{run_slug}/broll-{nn}-{description}.png` — sequential numbering, snake_case descriptions
- Desktop: 1440×900 full-page for dashboards, 1440×800 viewport for hero sections. Mobile: 375×812 for all product screens. Export as PNG.
- Thumbnail-specific captures: 1280×720 for video thumbnails, 1200×800 for blog headers, 1080×1080 for carousel frames, 1200×630 for OG images
- Manifest `manifest.json` stores: id, description, dimensions, source_url, file_path, suggested_formats[], captured_at
- If a URL is inaccessible (404/auth), note it in manifest as `status: failed` — do not skip silently
- B-roll comes BEFORE any landing page, blog post, or social content production — no content agent should have to scramble for screenshots mid-production

## User Prompt

**Product Brief:**
{product_brief}

**Ship Plan (channel priorities, content themes):**
{ship_plan}

**ICP (pain points and use cases):**
{icp}

**Run Slug:** {run_slug}
**Output Directory:** `data/content-assets/{run_slug}/`

Produce a complete B-roll capture plan and execute it:

1. **Asset Inventory** — All capturable assets identified from the brief + strategy
2. **Capture Queue** — Ordered list with tool, URL/command, and output spec for each
3. **Execute Captures** — Use browser/canvas/exec tools to capture each asset
4. **Generate manifest.json** — Complete manifest with all captured assets
5. **Content Format Map** — Which assets are suggested for which content formats

## Capture Type Reference

| Asset Type | Tool | Settings | Output Spec |
|-----------|------|----------|-------------|
| Live product screens (hero) | `browser` screenshot | 1440×800 viewport | Desktop hero, OG image, blog header |
| Live product screens (full dashboard) | `browser` screenshot, full-page | 1440px width | Dashboard demo, tutorial screenshots |
| Live product screens (mobile) | `browser` screenshot | 375×812 viewport | Mobile social, Stories background |
| Competitor landing page | `browser` screenshot | 1440×800 viewport | Competitor comparison content |
| Competitor pricing page | `browser` screenshot | 1440×800 viewport | Pricing comparison carousel slide |
| CLI / terminal output | `exec` → `canvas` render | Code font, dark background | Tutorial blog post, technical content |
| Code snippet | `canvas` render | Syntax highlighted, dark theme | Developer-focused social content |
| Data visualization / architecture | `canvas` render (Mermaid) | SVG export | Blog diagram, landing page diagram |
| Product flow (multi-step) | `browser` multi-screenshot | Sequential naming | Tutorial content, onboarding visuals |

## Example Output

## Asset Inventory

From scanning the product brief and ship plan, the following capturable assets were identified:

| # | Asset Description | Type | Source | Priority |
|---|------------------|------|--------|----------|
| 01 | Product dashboard — main view | Product screen | https://app.example.com/dashboard | P0 — all content |
| 02 | Product onboarding — step 1 connect | Product screen | https://app.example.com/connect | P0 — tutorial content |
| 03 | Product mobile view | Product screen (mobile) | https://app.example.com/dashboard | P0 — IG Stories |
| 04 | Competitor A landing page | Competitor | https://competitor-a.com | P1 — comparison content |
| 05 | Competitor A pricing page | Competitor | https://competitor-a.com/pricing | P1 — comparison carousel |
| 06 | Competitor B landing page | Competitor | https://competitor-b.com | P1 — comparison content |
| 07 | Manual workflow screenshot | Context | https://sheets.google.com (user's described workflow) | P1 — "before" visual |
| 08 | Terminal output: tool installation | CLI | `npm install example-tool` | P2 — technical blog |
| 09 | Architecture diagram | Mermaid render | Generated from product description | P2 — landing page, blog |

## Capture Queue

```
1. browser → screenshot https://app.example.com/dashboard
   Output: broll-01-product-dashboard-desktop.png (1440×800)

2. browser → screenshot https://app.example.com/dashboard (mobile)
   Output: broll-02-product-dashboard-mobile.png (375×812)

3. browser → screenshot https://app.example.com/dashboard (full-page)
   Output: broll-03-product-dashboard-fullpage.png (1440px wide)

4. browser → screenshot https://competitor-a.com
   Output: broll-04-competitor-a-landing.png (1440×800)

5. browser → screenshot https://competitor-a.com/pricing
   Output: broll-05-competitor-a-pricing.png (1440×800)

6. canvas → render architecture diagram (Mermaid)
   Output: broll-09-architecture-diagram.svg

7. exec → npm install example-tool (capture output) → canvas render
   Output: broll-08-terminal-install.png (1280×720 dark theme)
```

## manifest.json

```json
{
  "run_slug": "{run_slug}",
  "captured_at": "{iso_timestamp}",
  "total_assets": 9,
  "assets": [
    {
      "id": "broll-01",
      "description": "Product dashboard — main view, desktop",
      "dimensions": "1440x800",
      "source_url": "https://app.example.com/dashboard",
      "file_path": "data/content-assets/{run_slug}/broll-01-product-dashboard-desktop.png",
      "suggested_formats": ["og_image", "blog_header", "landing_page_hero", "carousel_slide_product"],
      "status": "captured",
      "captured_at": "{iso_timestamp}"
    },
    {
      "id": "broll-02",
      "description": "Product dashboard — mobile viewport",
      "dimensions": "375x812",
      "source_url": "https://app.example.com/dashboard",
      "file_path": "data/content-assets/{run_slug}/broll-02-product-dashboard-mobile.png",
      "suggested_formats": ["ig_stories", "tiktok_background", "mobile_screenshot_blog"],
      "status": "captured",
      "captured_at": "{iso_timestamp}"
    },
    {
      "id": "broll-04",
      "description": "Competitor A — landing page",
      "dimensions": "1440x800",
      "source_url": "https://competitor-a.com",
      "file_path": "data/content-assets/{run_slug}/broll-04-competitor-a-landing.png",
      "suggested_formats": ["comparison_carousel", "comparison_blog_image"],
      "status": "captured",
      "captured_at": "{iso_timestamp}"
    },
    {
      "id": "broll-09",
      "description": "Architecture diagram — how product connects tools",
      "dimensions": "1200x800",
      "source_url": "generated:mermaid",
      "file_path": "data/content-assets/{run_slug}/broll-09-architecture-diagram.svg",
      "suggested_formats": ["landing_page_diagram", "blog_in_article", "x_thread_visual"],
      "status": "captured",
      "captured_at": "{iso_timestamp}"
    }
  ]
}
```

## Content Format Map

| Asset ID | Asset | Suggested Uses |
|----------|-------|----------------|
| broll-01 | Dashboard desktop | Landing page hero, OG image, blog header image, LinkedIn post visual |
| broll-02 | Dashboard mobile | IG Stories, Reels B-roll, mobile mockup for social |
| broll-03 | Dashboard full-page | Tutorial blog post scrolling screenshot, feature comparison |
| broll-04 | Competitor A landing | Comparison carousel (slide: "Their page vs ours"), comparison blog article |
| broll-05 | Competitor A pricing | Pricing comparison table visual, "They charge X, we charge Y" graphic |
| broll-08 | Terminal install | Developer-focused blog post, LinkedIn technical post, YouTube thumbnail |
| broll-09 | Architecture diagram | Landing page "how it works" section, blog post diagram, X thread visual |

### Blackboard Keys
- `awareness.broll_manifest`: path to manifest.json
- `awareness.broll_asset_count`: {total captured}
- `awareness.broll_directory`: `data/content-assets/{run_slug}/`


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
