# Nurture — Retargeting

Stage: nurture
Inputs: ship_plan (channel plan, approved ad budget), icp (audience segments, purchase behavior, objections), funnel_map (defined funnel stages and drop-off points), lead_capture_wiring (Pixel installed and verified, email group names), positioning (value prop, VoC language)
Output: Retargeting audience definitions and ad creative directions for Meta (and optionally Google Ads), ready to activate if ad budget is approved in strategy
Token Budget: ~3,500 tokens
Quality Criteria: Each audience segment has a specific, actionable definition with pixel event or source data; creative direction is distinct per segment (non-signups see different message than signed-up-but-inactive); audiences are mutually exclusive (no overlap between segments); lookalike seed definition is concrete; budget allocation is realistic for approved spend; all creative copy is humanized; conditional — if no ad budget in strategy, output a "if budget unlocks" placeholder

## System Prompt

You are a performance marketing strategist who designs retargeting campaigns that recapture lost attention without being annoying. You understand that retargeting works because it targets people who already showed interest — your job is to give them the right nudge at the right moment.

Rules:
- Retargeting is CONDITIONAL: only activate if ad budget was approved in Strategy. If no budget: produce the definitions and creative directions as a "ready-to-activate" package, clearly marked as INACTIVE.
- Audiences MUST be mutually exclusive — use exclusions aggressively. Someone who already paid should never see an acquisition ad.
- Each audience gets a DIFFERENT creative angle: non-signups (reminder), signups who haven't activated (tutorial/activation), activated but not paid (upgrade nudge)
- Audience sizes matter: if landing page traffic is <500 visitors, custom audience may be too small for Meta to serve effectively. Note minimum viable traffic thresholds.
- Lookalike audiences seed from your highest-quality data: email list of paying customers > email list of all signups > pixel events
- All ad copy runs through the `humanize` skill before output — no "personalized" ad-speak
- GDPR/CCPA compliance note: Meta Pixel requires cookie consent if targeting EU users. Note this if international audience.
- Budget allocation follows 70/20/10 rule: 70% to proven retargeting segments, 20% to lookalikes, 10% to experimental

## User Prompt

**Ship Plan (channels, approved ad budget):**
{ship_plan}

**ICP (audience segments, purchase behavior):**
{icp}

**Funnel Map (stages, drop-off points):**
{funnel_map}

**Lead Capture Wiring (Pixel events, email groups):**
{lead_capture_wiring}

**Positioning:**
{positioning}

**Ad Budget (from Strategy):** {ad_budget}

Produce the complete retargeting package:

1. **Activation Status** — Is budget approved? Active or placeholder?
2. **Audience Definitions** — Custom audiences with source data and exclusions
3. **Lookalike Audiences** — Seed definition and targeting parameters
4. **Creative Briefs** — Per audience segment (headline, body, CTA, image direction)
5. **Budget Allocation** — Spend split across audiences
6. **Performance Thresholds** — When to scale, when to pause
7. **Exclusion Rules** — Who should never see retargeting ads

## Example Output

## Activation Status

**Ad Budget Approved:** {ad_budget} (from Strategy)
**Retargeting Package Status:** ✅ ACTIVE — ready to activate after Pixel verification and Gate-L approval

*If no budget: "INACTIVE — Retargeting package ready to activate if budget is approved. Pixel and audiences are configured. Estimated activation cost: $X/day."*

## Audience Definitions

### Audience 1: Landing Page Visitors (Non-Signups)
**Definition:** People who visited the landing page but did NOT trigger `lead_signup` event
**Source:** Meta Pixel — `page_view` on {landing_page_url} last 30 days, EXCLUDE `lead_signup` event
**Estimated size:** ~{X} people (depends on traffic volume)
**Minimum viable size:** 500 people for Meta to serve effectively
**Window:** 30-day lookahead
**Goal:** Convert to signup

### Audience 2: Signed Up, Not Activated
**Definition:** Email subscribers who joined `{product_slug}-leads` group but have NOT triggered `onboarding_started` event in product
**Source:** Email provider export (tag: signed-up-not-activated) uploaded as Custom Audience to Meta
**Estimated size:** ~{X}% of signups
**Window:** 14 days since signup
**Goal:** Drive product activation

### Audience 3: Activated, Not Paid (D7+)
**Definition:** Users who triggered `onboarding_started` but NOT `purchase` event, D7+ after activation
**Source:** Meta Pixel `onboarding_started` EXCLUDE `purchase`, date range D0-D7 relative
**Estimated size:** Smaller — focus of spend
**Window:** 14 days since activation
**Goal:** Convert to paid

### Audience 4: Past Customers (Exclusion + Upsell)
**Definition:** Users who triggered `purchase` event
**Source:** Meta Pixel `purchase` event — ALL time
**Use:** EXCLUDE from all acquisition/retargeting audiences; optionally INCLUDE in upsell campaign if second tier exists
**Goal:** Protect paid customers from irrelevant ads

## Lookalike Audiences

### Lookalike 1: Customers (Highest quality)
**Seed:** Email list of paying customers (upload as CSV to Meta)
**Similarity:** 1-2% lookalike (tightest match)
**Geography:** {target_countries}
**Goal:** Find new users most likely to pay

### Lookalike 2: Signups (Volume)
**Seed:** Email list of all signups (upload as CSV to Meta)
**Similarity:** 3-5% lookalike (broader reach)
**Geography:** {target_countries}
**Goal:** Expand reach to users likely to sign up

*Note: Lookalike audiences require minimum 100 seed records for Meta to generate. Use Lookalike 1 only when ≥100 paying customers exist.*

## Creative Briefs

### Audience 1: Non-Signups — "You Were Just Here"

**Headline:** Still thinking about it? Here's why it's worth 5 minutes.
**Body:** You stopped by {product_name} and didn't sign up. Totally fair. But if manual dashboard updates are still eating your Mondays — the free tier is still there waiting.
**CTA:** Try it free
**Image:** Product dashboard screenshot (broll-01) — clean, inviting. No text overlay. Familiarity-based.
**Format:** Single image + link, 1200×628

**Humanize channel:** `--channel blog` (calm, not pushy)

### Audience 2: Signed Up, Not Activated — "One Step Away"

**Headline:** You signed up for {product_name}. Here's your first 5 minutes.
**Body:** You joined the waitlist / signed up. The hardest part is already done. Log in and connect your first tool — takes 2 minutes. Most people hit their first "aha moment" in under 5.
**CTA:** Pick up where you left off
**Image:** Tutorial step 1 screenshot (broll-02 onboarding screen). Arrow pointing to "connect" button.
**Format:** Single image + link, 1200×628

**Humanize channel:** `--channel blog`

### Audience 3: Activated, Not Paid — "Ready to Remove the Limit?"

**Headline:** You're hitting the {product_name} free tier limit.
**Body:** You've synced {X} dashboards on the free plan. The paid plan is $19/mo — less than 1 hour of your time if you bill at $20+/hr. Founding member pricing is still available for a few more days.
**CTA:** Upgrade for $19/mo
**Image:** Pricing page screenshot showing free vs paid comparison. Highlight the paid plan.
**Format:** Single image + link or carousel (slide 1: free limit, slide 2: what paid unlocks, slide 3: CTA)

**Humanize channel:** `--channel blog`

### Lookalike 1 & 2 — Cold Audience (Awareness)

**Headline:** Stop spending Monday mornings copying dashboard numbers.
**Body:** {product_name} syncs your tools automatically — 2-minute setup, real-time data. Free to start.
**CTA:** See how it works
**Image:** Split visual — stressed person with spreadsheet vs clean dashboard. Pain → solution contrast.
**Format:** Single image + link, 1200×628

## Budget Allocation

**Total approved ad budget:** {ad_budget}

| Audience | Share | Daily Budget | Rationale |
|----------|-------|-------------|-----------|
| Audience 1: Non-signups (retarget) | 35% | ${X}/day | Largest pool, warm signal |
| Audience 2: Signup → activate (retarget) | 25% | ${X}/day | High intent, small pool |
| Audience 3: Activate → pay (retarget) | 20% | ${X}/day | Smallest pool, highest value per conversion |
| Lookalike 1: Customers (cold) | 15% | ${X}/day | Find new buyers |
| Lookalike 2: Signups (cold) | 5% | ${X}/day | Exploratory, expand reach |
| **Total** | **100%** | **${total}/day** | |

## Performance Thresholds

| Audience | Pause if | Scale if |
|---------|---------|--------|
| Non-signups | CPL > $15 after $30 spend | CPL < $5 and CTR > 1.5% |
| Signup → activate | CPA (activation) > $8 | CPA < $3 and conversion > 30% |
| Activate → pay | CPA (purchase) > $40 | CPA < $15 and ROAS > 1.5x |
| Lookalike 1 | CPL > $20 after $30 spend | CPL < $8 and 3+ conversions |
| Lookalike 2 | CTR < 0.5% after $20 spend | CTR > 1% and CPL < $12 |

## Exclusion Rules (Always Apply)

1. **Exclude all past customers** from all acquisition and retargeting campaigns
2. **Exclude Audience 2** from Audience 1 (don't show "you were just here" to people who signed up)
3. **Exclude Audience 3** from Audience 1 and 2 (don't show activation ads to paying users)
4. **Frequency cap:** Max 3 impressions per person per day across all retargeting audiences
5. **EU compliance:** If targeting EU users, Pixel requires active cookie consent — implement consent banner before activating Meta Pixel

### Blackboard Keys
- `nurture.retargeting`: link to this document
- `nurture.retargeting_status`: ACTIVE | INACTIVE
- `nurture.retargeting_budget`: {ad_budget}


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
