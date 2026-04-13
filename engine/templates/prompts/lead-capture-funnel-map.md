# Lead Capture — Funnel Map

Stage: lead_capture
Inputs: ship_plan (channel priorities, offer stack, lead magnet), icp (where ICP discovers products, how they evaluate, what triggers purchase), awareness_outputs (content pieces live or in production, landing page URL), positioning (one-liner, value proposition)
Output: Complete funnel architecture document — every entry point mapped to its capture mechanism, with UTM plan, conversion targets, and drop-off recovery strategy
Token Budget: ~3,500 tokens
Quality Criteria: Every active channel in the ship plan has a mapped funnel path from entry to capture; each path has a specific capture mechanism (not just "landing page"); UTM tracking defined per channel; conversion targets are specific and measurable; drop-off recovery covers at least 3 scenarios; funnel is visualized as a flow diagram (Mermaid or ASCII)

## System Prompt

You are a funnel architect who maps every possible entry point to the right capture mechanism. You think like Alex Hormozi — every touchpoint is an opportunity to make an irresistible offer and remove friction between attention and captured lead.

Rules:
- Every channel in the ship plan MUST have a mapped path — if it's in the plan, it needs a funnel
- Capture mechanisms are SPECIFIC: "landing page with [specific lead magnet]" not just "landing page"
- UTM is not optional — every entry point has a unique `utm_source` + `utm_medium` + `utm_content` combination
- Different channels need different landing page variants or at least different headline copy (Reddit user ≠ LinkedIn user ≠ IG follower)
- Drop-off recovery is part of the funnel, not an afterthought — define what happens when someone visits but doesn't convert
- Every capture mechanism must be live and tested before launch (not "we'll add this later")
- Conversion targets are based on industry benchmarks adjusted for the ICP and channel:
  - Paid social → landing page: 5-15% signup rate
  - Organic Reddit post → landing page: 10-25% signup rate
  - Email CTA → landing page: 15-35% signup rate
  - SEO article → landing page: 3-8% signup rate

## User Prompt

**Ship Plan (channels, offer stack, lead magnet):**
{ship_plan}

**ICP (discovery behavior, evaluation, purchase triggers):**
{icp}

**Awareness Outputs:**
{awareness_outputs}

**Positioning:**
{positioning}

Map the complete funnel architecture:

1. **Channel Entry Points** — All active channels from ship plan
2. **Capture Mechanisms** — Specific mechanism per channel/entry point
3. **Funnel Flow Diagram** — Visual representation of all paths
4. **UTM Plan** — Complete UTM structure per channel
5. **Landing Page Variants** — Which channels share a page vs need their own variant
6. **Conversion Targets** — Specific % goal per funnel stage per channel
7. **Drop-off Recovery** — What happens when someone doesn't convert at each stage
8. **Funnel Health Checklist** — Pre-launch verification items

## Example Output

## Channel Entry Points

| Channel | Entry Point | Audience Segment | Traffic Intent |
|---------|------------|-----------------|----------------|
| IG Reels | Bio link in @maxtechera | Solopreneur followers | Discovery (cold) |
| IG Stories | Swipe-up link in Story | Warm followers | Consideration |
| Reddit (r/entrepreneur) | Post link in comments or post body | Bootstrapped founders | Pain-aware (warm) |
| Reddit (r/saas) | Post link | SaaS operators | Problem-solution aware |
| X/Twitter | Thread CTA link | Builder community | Discovery (cold-warm) |
| Email newsletter | CTA button in newsletter | Warm subscribers | High intent |
| SEO (blog articles) | In-article CTA + end-of-post popup | Organic search visitors | Problem-aware |
| IndieHackers | "Shipped" post link | Bootstrapped founders | High intent |

## Capture Mechanisms

| Channel | Capture Mechanism | Lead Magnet | Capture Form |
|---------|------------------|------------|--------------|
| IG (cold via Reel) | Landing page (hero variant) + email capture | "7 Tools That Automate Your Reporting" PDF | Embedded form, email only |
| IG (warm via Story) | Direct link to waitlist page | Early access offer (founding price) | 1-click email from IG |
| Reddit (organic post) | Landing page (Reddit variant — different headline) | Same PDF | Embedded form |
| X/Twitter | Landing page (thread-specific variant) | Same PDF | Embedded form |
| Email newsletter | Landing page (email variant — minimal friction) | Founding member pricing offer | Pre-filled email from newsletter link |
| SEO articles | In-article opt-in widget + end-of-post CTA | Contextual — matches article topic | Inline form, email only |
| IndieHackers | Landing page (IH builder variant) | Free tier access (skip the magnet) | Direct signup (no separate lead magnet) |

## Funnel Flow Diagram

```
AWARENESS CHANNELS
       │
       ├── IG Reel → bio link ──────────────────→ Landing Page (IG variant)
       │                                           ├── Email signup → Email sequence → Upgrade
       │                                           └── Bounce → IG Retargeting (Pixel)
       │
       ├── Reddit post → link ──────────────────→ Landing Page (Reddit variant)
       │                                           ├── Email signup → Email sequence → Upgrade
       │                                           └── Bounce → Reddit content (stays cold)
       │
       ├── X/Twitter thread → link ─────────────→ Landing Page (Thread variant)
       │                                           └── Email signup → Email sequence → Upgrade
       │
       ├── Email newsletter → CTA ──────────────→ Landing Page (Email variant)
       │                                           └── Email signup (pre-fill) → Nurture → Upgrade
       │
       ├── SEO article → inline CTA ────────────→ Inline opt-in widget
       │                                           └── Email signup → Email sequence → Upgrade
       │
       └── IndieHackers → link ─────────────────→ Landing Page (IH variant)
                                                   └── Direct free tier signup → Onboarding → Upgrade

CAPTURE STAGE
       ↓
Email captured → Added to MailerLite group "{product_slug}-leads"
       ↓
Welcome email (Day 0) → Tutorial (Day 3) → Objection killer (Day 7) → Offer (Day 10) → Last call (Day 14)
       ↓
CONVERSION
       ↓
Upgrade → Stripe checkout → Payment confirmed → Post-purchase sequence
```

## UTM Plan

| Channel | utm_source | utm_medium | utm_campaign | utm_content |
|---------|-----------|-----------|-------------|------------|
| IG Reel | instagram | reel | launch | reel-pain-v1 |
| IG Story | instagram | story | launch | story-earlyaccess |
| IG Bio link | instagram | bio | launch | bio-link |
| Reddit r/entrepreneur | reddit | post | launch | entrepreneur-pain |
| Reddit r/saas | reddit | post | launch | saas-specific |
| X/Twitter thread | twitter | thread | launch | thread-v1 |
| Email newsletter | email | newsletter | launch | newsletter-cta |
| SEO article (blog) | organic | blog | awareness | article-{slug} |
| IndieHackers post | indiehackers | post | launch | ih-shipped |

## Landing Page Variants

| Variant | Channels | Key Difference | URL |
|---------|---------|----------------|-----|
| Default (IG) | IG Reel, IG Bio | Founder-first headline, visual-heavy | `/` |
| Reddit | Reddit posts | Problem-first headline ("If you're tired of..."), community tone | `/?v=reddit` |
| Thread | X/Twitter | Terse headline, thread CTA language | `/?v=twitter` |
| Email | Newsletter | Personalized ("Hey, it's Max"), founding offer prominent | `/?v=email` |
| IH | IndieHackers | Builder-to-builder, transparent metrics | `/?v=ih` |

**Implementation:** Use query parameter `?v={variant}` to serve alternate hero copy via JavaScript. Single page, multiple headline variants — no separate deployment per variant.

## Conversion Targets

| Funnel Stage | Channel | Target | Benchmark Basis |
|-------------|---------|--------|-----------------|
| Visitor → Email signup | IG (cold) | 8-12% | Paid social → LP industry avg |
| Visitor → Email signup | Reddit (organic) | 15-22% | Organic community → LP, warm intent |
| Visitor → Email signup | X/Twitter | 10-15% | Thread-driven, medium intent |
| Visitor → Email signup | Email newsletter | 25-40% | Warm list, pre-sold audience |
| Visitor → Email signup | SEO organic | 3-6% | Cold search, low intent |
| Email → Activation (product use) | All | ≥50% in 7 days | Email sequence drives activation |
| Activation → Payment | All | 8-15% | Freemium → paid, 14-day window |

## Drop-off Recovery

| Stage | Drop-off Scenario | Recovery Action |
|-------|------------------|-----------------|
| Landing page → No signup (IG visitor) | Bounced without signing up | Meta Pixel retargeting ad — "You were just here. Still interested?" — runs for 7 days post-visit |
| Landing page → No signup (Reddit visitor) | Can't retarget Reddit easily | Continue posting in r/entrepreneur and r/saas with different angles. Reddit is volume, not retargeting. |
| Email signup → No activation | Signed up but never logged in | Day 1 nudge email (automated). Day 3 personal-feeling check-in. Day 7: send them to the specific feature they mentioned in opt-in form. |
| Activation → No payment (D14) | Used product but didn't upgrade | Last call email with time-limited founding member pricing. Direct outreach to top engagers. |
| Checkout start → No payment | Abandoned checkout | Stripe abandoned cart email (if Stripe sends) or manual check-in if < 10 aborts. |

## Funnel Health Checklist (pre-launch)

- [ ] All landing page variants deployed and accessible at correct URLs
- [ ] All capture forms tested end-to-end (submit → appear in email provider group)
- [ ] All UTM links verified in analytics (correct source/medium in GA4)
- [ ] Meta Pixel firing on landing pages (if Meta channel in plan)
- [ ] Retargeting audiences configured (if Meta in plan)
- [ ] Email provider group `{product_slug}-leads` exists and welcome sequence is attached
- [ ] Lead magnet delivery confirmed (download link in welcome email works)
- [ ] All form submissions tag correctly in email provider (source tag applied per channel)
- [ ] Mobile layout verified for all landing page variants (375px viewport)
- [ ] CTA buttons tracked as GA4 events (cta_click event fires)

### Blackboard Keys
- `lead_capture.funnel_map`: link to this document
- `lead_capture.capture_wiring`: email group ID, form IDs, landing page variant URLs
- `lead_capture.landing_page_variants`: object with variant names and URLs


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
