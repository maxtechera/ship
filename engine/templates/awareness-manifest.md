# Awareness Manifest: {product_name}

> **Stage:** Awareness (Stage 5A)
> **Agent:** Awareness Agent
> **Purpose:** Track every Awareness deliverable from creation to live. Nothing ships without passing through this manifest.
> **Updated:** {date}
>
> **Note:** This is a reference menu. Agent selects which deliverables to produce based on ICP channel fit and product context. Not every section applies to every product. Remove or add sections as appropriate.

---

## Summary Stats

| Category | Total | ✅ Live | 🔄 In Review | 📝 Draft | ⬜ Todo |
|----------|-------|--------|-------------|---------|--------|
| Landing Page sections | 5 | 0 | 0 | 0 | 5 |
| Blog posts | 7 | 0 | 0 | 0 | 7 |
| Social content pack | 6 | 0 | 0 | 0 | 6 |
| Video assets | 4 | 0 | 0 | 0 | 4 |
| SEO metadata | 8 | 0 | 0 | 0 | 8 |
| Media assets | 7 | 0 | 0 | 0 | 7 |
| UTM tracking links | 5 | 0 | 0 | 0 | 5 |
| **TOTAL** | **42** | **0** | **0** | **0** | **42** |

> Update summary stats every time a status changes.
> **Quality score scale:** 1–10. Target: ≥8 before status moves to `approved` or `live`.

---

## Status Key

| Symbol | Status | Meaning |
|--------|--------|---------|
| ⬜ | `todo` | Not started |
| 📝 | `draft` | In progress / first pass created |
| 🔄 | `review` | Ready for Max or critic agent review |
| ✅ | `approved` | Max approved, ready to deploy |
| 🟢 | `live` | Deployed and publicly accessible |
| 🔴 | `blocked` | Needs input or dependency before proceeding |

---

## 1. Landing Page

**Live URL:** {product_url}
**Deploy target:** `{product}.max-techera.[REDACTED_PROJECT].app`
**Last deployed:** {date}

| Section | Status | Assigned | Drive Link | Quality Score | Notes |
|---------|--------|----------|-----------|--------------|-------|
| **Hero section** (headline, subhead, CTA, social proof) | ⬜ | Awareness Agent | — | — | Headline must use VoC language from ICP; problem-first, not feature-first |
| **Benefits section** (3 core outcomes, not features) | ⬜ | Awareness Agent | — | — | Each benefit maps to a validated pain point |
| **Social proof section** (testimonials, user count, logos) | ⬜ | Awareness Agent | — | — | Use captured testimonials from inner circle (Wave 1); skeleton with placeholders until live |
| **CTA section** (primary + secondary CTA, lead magnet offer) | ⬜ | Awareness Agent | — | — | Must match finalized offer stack from Lead Capture Agent |
| **OG image** (1200×630, link preview) | ⬜ | Awareness Agent | — | — | Generated via `content-image` skill (Gemini-first); verify renders correctly in Telegram/iMessage |

**Landing page humanization check:**
- [ ] All copy passed through the `humanize` skill with `channel=blog`
- [ ] Zero AI-sounding phrases ("I hope this finds you well", "In today's fast-paced world", etc.)
- [ ] Headline tested against VoC bank — uses language from validation threads

---

## 2. Blog Posts

**Publish location:** {blog_url} (e.g., [REDACTED_PROJECT].app/blog or product subdomain)
**Drive folder:** {drive_folder_url}

Agent determines post count based on SEO opportunity and ICP channel fit. Below are reference templates — select and adapt as needed.

### Post 1 — Problem Awareness
**Title:** "The {pain_topic} Problem Nobody Talks About"
**Type:** Problem-awareness / organic discovery
**Target keywords:** {keywords}
**Word count target:** 2,000+

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| Outline | ⬜ | Awareness Agent | — | — | |
| First draft | ⬜ | Awareness Agent | — | — | |
| Humanized copy | ⬜ | Awareness Agent | — | — | `humanize` skill with `channel=blog` |
| Hero image (1200×628) | ⬜ | Awareness Agent | — | — | AI-generated, branded |
| SEO metadata | ⬜ | Awareness Agent | — | — | Title <60 chars, description <155 chars |
| FAQ schema (JSON-LD) | ⬜ | Awareness Agent | — | — | Embedded in `<head>` |
| Internal links | ⬜ | Awareness Agent | — | — | Links to other posts + landing page |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

### Post 2 — Educational / How-To
**Title:** "How to {solve_problem} Without {bad_alternative}"
**Type:** Tutorial / mid-funnel activation
**Target keywords:** {keywords}
**Word count target:** 2,000+

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| Outline | ⬜ | Awareness Agent | — | — | |
| First draft | ⬜ | Awareness Agent | — | — | |
| Humanized copy | ⬜ | Awareness Agent | — | — | |
| Hero image (1200×628) | ⬜ | Awareness Agent | — | — | |
| SEO metadata | ⬜ | Awareness Agent | — | — | |
| FAQ schema (JSON-LD) | ⬜ | Awareness Agent | — | — | |
| Internal links | ⬜ | Awareness Agent | — | — | |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

### Post 3 — Competitor Comparison
**Title:** "{product_name} vs {top_competitor}: An Honest Comparison"
**Type:** Comparison / decision-stage SEO + competitor traffic
**Target keywords:** "{product_name} vs {competitor}", "{competitor} alternative"
**Word count target:** 2,000+

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| Outline | ⬜ | Awareness Agent | — | — | Dual purpose: SEO article + landing page variant at `/{product}-vs-{competitor}` |
| First draft | ⬜ | Awareness Agent | — | — | |
| Humanized copy | ⬜ | Awareness Agent | — | — | |
| Hero image (1200×628) | ⬜ | Awareness Agent | — | — | |
| SEO metadata | ⬜ | Awareness Agent | — | — | |
| FAQ schema (JSON-LD) | ⬜ | Awareness Agent | — | — | |
| Comparison table | ⬜ | Awareness Agent | — | — | Feature-by-feature, pricing, honest weaknesses |
| Internal links | ⬜ | Awareness Agent | — | — | |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

### Post 4 — Step-by-Step Tutorial
**Title:** "Step-by-Step: {core_use_case} in Under 10 Minutes"
**Type:** Tutorial / SEO long-tail + activation
**Target keywords:** {keywords}
**Word count target:** 1,500+

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| Outline | ⬜ | Awareness Agent | — | — | |
| First draft | ⬜ | Awareness Agent | — | — | |
| Humanized copy | ⬜ | Awareness Agent | — | — | |
| Hero image (1200×628) | ⬜ | Awareness Agent | — | — | |
| SEO metadata | ⬜ | Awareness Agent | — | — | |
| FAQ schema (JSON-LD) | ⬜ | Awareness Agent | — | — | |
| Internal links | ⬜ | Awareness Agent | — | — | |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

### Post 5 — Thought Leadership
**Title:** "Why {industry} Is Finally Getting Serious About {problem}"
**Type:** Thought leadership / brand authority + link bait
**Target keywords:** {keywords}
**Word count target:** 2,000+

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| Outline | ⬜ | Awareness Agent | — | — | |
| First draft | ⬜ | Awareness Agent | — | — | |
| Humanized copy | ⬜ | Awareness Agent | — | — | |
| Hero image (1200×628) | ⬜ | Awareness Agent | — | — | |
| SEO metadata | ⬜ | Awareness Agent | — | — | |
| FAQ schema (JSON-LD) | ⬜ | Awareness Agent | — | — | |
| Internal links | ⬜ | Awareness Agent | — | — | |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

### Post 6 — Case Study (post-launch)
**Title:** "How {persona} Used {product_name} to {specific_result}"
**Type:** Case study / deep social proof
**Target keywords:** {keywords}
**Word count target:** 1,500+
**Timing:** Publish L+10 (requires real user story)

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| User interview / story sourced | ⬜ | Awareness Agent | — | — | |
| First draft | ⬜ | Awareness Agent | — | — | |
| Humanized copy | ⬜ | Awareness Agent | — | — | |
| Hero image (1200×628) | ⬜ | Awareness Agent | — | — | |
| SEO metadata | ⬜ | Awareness Agent | — | — | |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

### Post 7 — Second Competitor Comparison (optional)
**Title:** "{product_name} vs {competitor_2}: Which Is Right for You?"
**Type:** Comparison / competitor SEO
**Target keywords:** "{competitor_2} alternative", "{product_name} vs {competitor_2}"
**Timing:** Publish post-launch if search data shows competitor keyword traffic

| Item | Status | Assigned | Drive Link | Quality Score | Notes |
|------|--------|----------|-----------|--------------|-------|
| Outline | ⬜ | Awareness Agent | — | — | Conditional on search data |
| First draft | ⬜ | Awareness Agent | — | — | |
| Published | ⬜ | Awareness Agent | {url} | — | |

---

## 3. Social Content Pack

One source content piece adapted for all platforms. Created once, formatted per platform.

**Persona callout source-of-truth (required):**
- `openclaw-config/skills/engine/templates/persona-hook-library.md`
- `openclaw-config/skills/engine/templates/meta-persona-callouts-playbook.md`
- `openclaw-config/skills/engine/templates/meta-persona-callouts-pack.md`

| Persona artifact | Status | Link | Notes |
|------------------|--------|------|-------|
| Persona hook library selected | ⬜ | {url} | Avatar band uses 3-12 default unless constrained |
| Meta callouts playbook applied | ⬜ | {url} | Plain white text creatives stay retargeting/brand-equity constrained |
| Meta callouts pack updated | ⬜ | {url} | Matrix includes organic, paid prospecting, paid retargeting |

### Instagram Posts (Feed Carousels)

| Post | Slide 1 Hook | Status | Assigned | Drive Link | Quality Score | Notes |
|------|-------------|--------|----------|-----------|--------------|-------|
| IG Carousel 1 — Pain hook | "{pain_hook}" | ⬜ | Awareness Agent | — | — | 10 slides, 1080×1080, slide 10 = CTA |
| IG Carousel 2 — Tutorial | "How to {use_case} in 3 steps" | ⬜ | Awareness Agent | — | — | Publish via `meta_api.py` |
| IG Carousel 3 — Comparison | "{product} vs {competitor}" | ⬜ | Awareness Agent | — | — | |
| IG Story pack | 3 stories per week | ⬜ | Awareness Agent | — | — | 1080×1920 |

---

### LinkedIn Posts

| Post | Angle | Status | Assigned | Drive Link | Quality Score | Notes |
|------|-------|--------|----------|-----------|--------------|-------|
| LinkedIn 1 — Launch | "I noticed {problem} — built {solution}" | ⬜ | Awareness Agent | — | — | 800–1200 words, professional storytelling |
| LinkedIn 2 — Lessons | "What I learned about {market}" | ⬜ | Awareness Agent | — | — | Thought leadership format |
| LinkedIn 3 — Results | "Two weeks post-launch: here's the data" | ⬜ | Awareness Agent | — | — | Post L+14 |

---

### Twitter / X Threads

| Thread | Hook Tweet | Status | Assigned | Drive Link | Quality Score | Notes |
|--------|-----------|--------|----------|-----------|--------------|-------|
| Thread 1 — Problem | "{pain observation without product mention}" | ⬜ | Awareness Agent | — | — | 5-7 tweets, hook = pain not product |
| Thread 2 — Launch | "We're live. Here's the story." | ⬜ | Awareness Agent | — | — | Publish on L-Day midday wave |
| Thread 3 — Tutorial | "10 things you can do with {product}" | ⬜ | Awareness Agent | — | — | L+1 |
| Thread 4 — Behind-the-scenes | "Launch day: what actually happened" | ⬜ | Awareness Agent | — | — | L+2 |
| Thread 5 — Data | "Week 1 numbers: {metrics}" | ⬜ | Awareness Agent | — | — | L+7 |

---

### YouTube Thumbnail

| Asset | Spec | Status | Assigned | Drive Link | Quality Score | Notes |
|-------|------|--------|----------|-----------|--------------|-------|
| Tutorial video thumbnail | 1280×720, high contrast, big bold text, face if possible | ⬜ | Awareness Agent | — | — | AI-generated via `content-image` skill (Gemini-first) |
| Launch video thumbnail | 1280×720 | ⬜ | Awareness Agent | — | — | |

---

## 4. Video Script + Assets

| Asset | Status | Assigned | Drive Link | Quality Score | Notes |
|-------|--------|----------|-----------|--------------|-------|
| **Short-form video script** (<60 sec, TikTok/Reels/Shorts) | ⬜ | Awareness Agent | — | — | Hook in first 3 words AND first 3 frames |
| **Short-form storyboard** (scene-by-scene, enough for talent execution) | ⬜ | Awareness Agent | — | — | Includes on-screen text, transitions, B-roll notes |
| **AI first-pass video** (complete rough cut — avatar + visuals + music) | ⬜ | Awareness Agent | — | — | Generated via AI video API; talent re-records over this |
| **YouTube long-form script** (full video, timestamped) | ⬜ | Awareness Agent | — | — | With hook, B-roll notes, CTA timing |
| **Talent ticket created** ("Block 30 min — script + storyboard + AI first-pass attached") | ⬜ | Awareness Agent | — | — | Goes to talent queue; batch with other talent tickets |
| **Voiceover first-pass audio** (ElevenLabs TTS via `sag` skill) | ⬜ | Awareness Agent | — | — | Talent replaces with human recording |

**Hook research logged:**
- Research run: `tools/research.py --social "{product category} viral hooks 2026"` ⬜
- Research run: `tools/research.py --x-only "viral {problem} reels shorts"` ⬜
- Top 5 hooks identified and documented: ⬜

---

## 5. SEO Metadata (per page)

All metadata verified before deployment. Run the `humanize` skill on meta descriptions to avoid AI-sounding copy.

| Page | Title (<60 chars) | Description (<155 chars) | OG:title | OG:description | Canonical | Status | Quality Score |
|------|------------------|------------------------|---------|---------------|-----------|--------|--------------|
| Landing page (`/`) | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Blog post 1 | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Blog post 2 | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Blog post 3 — comparison | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Blog post 4 — tutorial | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Blog post 5 — thought leadership | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Pricing page (`/pricing`) | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |
| Comparison page (`/{product}-vs-{competitor}`) | {title} | {description} | {og_title} | {og_description} | {canonical_url} | ⬜ | — |

**Structured data checklist:**
- [ ] FAQ schema (JSON-LD) embedded on landing page
- [ ] FAQ schema (JSON-LD) embedded on each blog post FAQ section
- [ ] Product schema (JSON-LD) on landing page
- [ ] Organization schema (JSON-LD) on landing page
- [ ] Sitemap generated/updated with all new URLs
- [ ] All canonical URLs set correctly

---

## 6. Media Assets

All assets generated programmatically. Output stored in `awareness/assets/`.

### Hero Images (blog post headers)

| Asset | Spec | Status | Assigned | Drive Link | Quality Score | Notes |
|-------|------|--------|----------|-----------|--------------|-------|
| Blog post 1 hero | 1200×628, AI-generated, branded | ⬜ | Awareness Agent | — | — | `content-image` skill (Gemini-first) |
| Blog post 2 hero | 1200×628 | ⬜ | Awareness Agent | — | — | |
| Blog post 3 hero | 1200×628 | ⬜ | Awareness Agent | — | — | |
| Blog post 4 hero | 1200×628 | ⬜ | Awareness Agent | — | — | |
| Blog post 5 hero | 1200×628 | ⬜ | Awareness Agent | — | — | |

### OG Images (link previews)

| Asset | Spec | Status | Assigned | Drive Link | Quality Score | Notes |
|-------|------|--------|----------|-----------|--------------|-------|
| Landing page OG | 1200×630, product mockup style | ⬜ | Awareness Agent | — | — | Verify renders in Telegram + iMessage |
| Blog post 1 OG | 1200×630 | ⬜ | Awareness Agent | — | — | |
| Blog post 2 OG | 1200×630 | ⬜ | Awareness Agent | — | — | |
| Blog post 3 OG | 1200×630 | ⬜ | Awareness Agent | — | — | |
| Blog post 4 OG | 1200×630 | ⬜ | Awareness Agent | — | — | |
| Blog post 5 OG | 1200×630 | ⬜ | Awareness Agent | — | — | |
| Comparison page OG | 1200×630 | ⬜ | Awareness Agent | — | — | |

### Product Screenshots

| Asset | Spec | Status | Assigned | Drive Link | Quality Score | Notes |
|-------|------|--------|----------|-----------|--------------|-------|
| Desktop screenshot (core screen) | 1440px wide, `browser` automation | ⬜ | Awareness Agent | — | — | Real product, not mockup |
| Mobile screenshot (core screen) | 375px wide, `browser` automation | ⬜ | Awareness Agent | — | — | |
| Dashboard / main view screenshot | 1440px | ⬜ | Awareness Agent | — | — | |
| Onboarding / first-use screenshot | 1440px | ⬜ | Awareness Agent | — | — | |

### Demo GIF

| Asset | Spec | Status | Assigned | Drive Link | Quality Score | Notes |
|-------|------|--------|----------|-----------|--------------|-------|
| Core product flow demo GIF | Auto-looping, `browser` automation records real flow | ⬜ | Awareness Agent | — | — | Signup → first value moment |
| Feature highlight GIF | Short focused demo of hero feature | ⬜ | Awareness Agent | — | — | |

---

## 7. UTM Tracking Links

All links batch-generated and stored in `lead-capture/funnels/utm-links.csv`. Track in the table below.

| Source | Medium | Campaign | Content | Full URL | Drive Link | Status |
|--------|--------|---------|---------|---------|-----------|--------|
| instagram | social | {product_slug}_launch | carousel_pain | {full_utm_url} | — | ⬜ |
| twitter | social | {product_slug}_launch | thread_launch | {full_utm_url} | — | ⬜ |
| linkedin | social | {product_slug}_launch | post_launch | {full_utm_url} | — | ⬜ |
| reddit | community | {product_slug}_launch | {subreddit} | {full_utm_url} | — | ⬜ |
| email | email | {product_slug}_launch | welcome_sequence | {full_utm_url} | — | ⬜ |
| producthunt | referral | {product_slug}_launch | ph_listing | {full_utm_url} | — | ⬜ |
| google | organic | {product_slug}_seo | blog_post_1 | {full_utm_url} | — | ⬜ |
| indiehackers | community | {product_slug}_launch | ih_shipped | {full_utm_url} | — | ⬜ |

**UTM verification:**
- [ ] All UTM parameters capture correctly in GA4 (test via GA4 real-time)
- [ ] CSV file saved to `lead-capture/funnels/utm-links.csv`
- [ ] Short links created (if using a URL shortener)

---

## Quality Gates

Before moving any item to `approved` status, verify:

| Gate | Check |
|------|-------|
| ✍️ Humanization | Copy passed through the `humanize` skill with correct channel flag |
| 🔍 VoC alignment | Language traces back to validated pain quotes in `voc-bank.md` |
| 📱 Mobile check | All landing page and blog content renders correctly at 375px |
| 🖼️ OG preview | OG image renders correctly in Telegram, iMessage, and Slack |
| 🔗 Links | All CTAs and internal links are functional |
| 📊 Analytics | UTM parameters tracked in GA4, conversion events verified |
| 📝 SEO | Meta title <60 chars, description <155 chars, canonical set |
| 🎯 Offer alignment | All CTAs point to the same offer stack (from Lead Capture Agent) |
| 🧠 Persona hook integrity | Social/ad hooks map to Ship Engine hook IDs; no ad-only persona drift |
| 📈 Split reporting readiness | Outputs are separable by `organic`, `paid.prospecting`, `paid.retargeting` |

---

## Drive Folder Structure

```
{product_name} — Awareness/
├── landing-page/
│   ├── copy-drafts/
│   └── deployed-screenshots/
├── blog-posts/
│   ├── post-1-problem-awareness/
│   ├── post-2-how-to/
│   ├── post-3-comparison/
│   ├── post-4-tutorial/
│   └── post-5-thought-leadership/
├── social/
│   ├── instagram-carousels/
│   ├── twitter-threads/
│   ├── linkedin-posts/
│   └── video-scripts/
├── assets/
│   ├── og-images/
│   ├── hero-images/
│   ├── screenshots/
│   └── demo-gifs/
└── utm-links/
    └── utm-links.csv
```

**Drive folder URL:** {drive_folder_url}

---

*Manifest updated as deliverables progress. Awareness Agent owns all items unless reassigned.*
