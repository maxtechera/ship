# Ship Engine: Attribution Model
<!-- NEO-222 | Ship Engine: Measure Stage -->
<!-- Purpose: Map conversions to source channels with confidence scoring -->
<!-- Usage: Fill in actuals per channel each week; reference in Weekly Report Section 2 -->

---

## Attribution Philosophy

Ship Engine uses a **first-touch + last-touch blended model** with manual overrides for known high-intent channels. Multi-touch attribution is aspirational — track what you can, annotate what you can't.

### Model Hierarchy
1. **Direct** → user typed URL or has no referrer (highest-intent proxy)
2. **Organic Search** → Google/Bing via GSC click data
3. **Social (Organic)** → IG, X (Twitter), LinkedIn link-in-bio / Linktree
4. **Email** → MailerLite UTM-tagged clicks
5. **Community** → Skool, Reddit, WhatsApp group links
6. **Paid** → Meta Ads, Google Ads (tracked via UTM `utm_medium=paid`)
7. **Referral** → third-party site links

---

## UTM Parameter Schema

All outbound links MUST use UTMs before publishing. Consistent naming is mandatory.

| Parameter | Convention | Example |
|-----------|-----------|---------|
| `utm_source` | lowercase channel name | `instagram`, `mailerlite`, `skool` |
| `utm_medium` | traffic type | `social`, `email`, `paid`, `organic`, `referral` |
| `utm_campaign` | campaign slug | `launch-w01`, `nurture-seq1`, `beta-close` |
| `utm_content` | asset variant | `reel-01`, `carousel-03`, `cta-button` |
| `utm_term` | keyword (paid) or audience segment (organic) | `freelancers-uy`, `contadores` |

**Builder:** `https://ga4.google.com/utm/create`
**Shortener:** bit.ly or short.io (track click-through independently of GA4)

---

## Weekly Attribution Scorecard

> **Run ID:** {run_id} | **Product:** {product_name} | **Week:** {week_number} ({start_date} → {end_date})

### Conversion Events to Track
- **Micro:** Email signup / lead magnet download / Skool join
- **Macro:** Checkout initiation / Purchase / Upgrade

---

### Channel Performance Table

| Channel | Medium | Sessions | Conv. Events | CVR | Revenue | CAC (Est.) | Notes |
|---------|--------|----------|--------------|-----|---------|------------|-------|
| **Direct** | direct | | | % | | — | High intent; likely branded |
| **Instagram Bio** | social | | | % | | | Link-in-bio clicks |
| **IG Reels / Stories** | social | | | % | | | Story swipe-up or link sticker |
| **X (Twitter)** | social | | | % | | | Profile + tweet links |
| **Email — Broadcast** | email | | | % | | — | Broadcast sends only |
| **Email — Sequence** | email | | | % | | — | Automated nurture |
| **Skool Community** | referral | | | % | | — | Community-driven |
| **Google Organic** | organic | | | % | | — | GSC impressions → clicks |
| **Meta Ads** | paid | | | % | | | Spend ÷ Conv. |
| **Referral (Other)** | referral | | | % | | — | Influencers, press, etc. |
| **TOTAL** | | | | % | | | |

---

### Attribution Confidence Flags

| Flag | Meaning |
|------|---------|
| ✅ UTM-verified | GA4 confirmed source via UTM |
| 🟡 Inferred | No UTM; source inferred from referrer or timing correlation |
| ❓ Unknown | Direct/dark traffic; cannot attribute |
| ❌ UTM missing | Link was published without UTM (fix before next publish) |

---

### Top Performing Assets (by channel)

| Rank | Channel | Asset | Impressions | Clicks | Conv. Events | CVR |
|------|---------|-------|-------------|--------|--------------|-----|
| 1 | | | | | | % |
| 2 | | | | | | % |
| 3 | | | | | | % |

---

## Attribution Rules & Overrides

### Rule 1 — Last-Touch Wins (default)
The conversion is credited to the last UTM-tagged session before the conversion event in GA4.

### Rule 2 — Assisted Credit
If the user had a prior organic/email touch within 7 days, log it in the "Notes" column as `assisted:{channel}`.

### Rule 3 — Manual Override
For high-volume DM-to-sale flows (WhatsApp, Instagram DMs), Max manually attributes conversions in the scorecard. These are marked `🟡 Inferred`.

### Rule 4 — Paid vs Organic Split
Meta Ads spend must be tracked separately. If `utm_medium=paid` is missing from ad URLs, flag for immediate fix.

---

## Quarterly Attribution Audit Checklist

- [ ] All published links use correct UTM schema
- [ ] GA4 → Acquisition → Traffic Acquisition report matches scorecard
- [ ] MailerLite UTM click data reconciled with GA4 sessions
- [ ] Paid channel spend vs revenue ROI computed
- [ ] Dark traffic % < 20% (if higher, investigate referrer data)
- [ ] Top 3 converting assets archived to `skills/ship-engine/templates/voc-bank.md`

---

**Owner:** Ship Engine — Measure Stage
**Data Sources:** GA4, GSC, MailerLite, Meta Ads Manager, Stripe
**Reference:** Linked in Weekly Report → Section 2
