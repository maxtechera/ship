# Launch Checklist: {product_name}

> **Stage:** Launch (Stage 7)
> **Gate:** Pre-Launch Approval — Max must sign off before Wave 1 begins
> **Principle:** Launch day is a pipeline builder, not a hype event. Every action routes to capture.

---

## Summary Status

| Area | Ready | Blocker |
|------|-------|---------|
| Product (live, tested, mobile) | ⬜ | |
| Landing page (deployed, OG verified) | ⬜ | |
| Analytics & tracking (end-to-end verified) | ⬜ | |
| Payment / Stripe (tested, live mode) | ⬜ | |
| Email sequences (imported, tested) | ⬜ | |
| All launch content drafted | ⬜ | |
| Product Hunt submission ready | ⬜ | |
| Community posts drafted | ⬜ | |
| Supporter list ready | ⬜ | |
| Directories submitted | ⬜ | |
| Max approved | ⬜ | |

**L-Day target:** {day of week} — aim for Tuesday, Wednesday, or Thursday
**Reply SLA on L-Day:** < 15 minutes across all platforms

---

## Pre-Launch Checklist (complete before Max approval)

### Product
- [ ] Product URL returns 200, no broken pages
- [ ] Core feature works end-to-end (complete the flow manually)
- [ ] Mobile responsive verified at 375px viewport
- [ ] Error handling in place — no crashes on bad input
- [ ] Stripe live mode enabled (not test mode)
- [ ] Access provisioning works immediately on payment
- [ ] Load tested (basic — can it handle 500 concurrent visitors?)
- [ ] Privacy policy page live
- [ ] Terms of service page live

### Landing Page
- [ ] Page deployed to live URL (`{product_url}`)
- [ ] Copy final — no placeholders, no draft sections
- [ ] OG tags rendered correctly (`og:title`, `og:description`, `og:image`)
- [ ] OG image uploaded (1200×630) and preview verified in Telegram/Slack/iMessage
- [ ] Mobile responsive at 375px
- [ ] Page load < 3s
- [ ] All CTAs linked and functional
- [ ] Email capture form live and wired to MailerLite group `{mailerlite_group}`
- [ ] Pricing page live with working Stripe checkout links
- [ ] FAQ section populated with top 5 objections

### Analytics & Tracking
- [ ] GA4 property ID confirmed: `{ga4_property_id}`
- [ ] `sign_up` event firing on form submission (verified via GA4 real-time)
- [ ] `purchase` event firing on Stripe checkout completion
- [ ] UTM parameters captured in GA4 (test with `?utm_source=test&utm_medium=test`)
- [ ] Meta Pixel installed (if running ads): `{meta_pixel_id}`
- [ ] All UTM links batch-generated and stored in `lead-capture/funnels/utm-links.csv`
- [ ] Funnel tracking tested end-to-end via `browser` automation — pass logged in `tracking-test-log.md`
- [ ] GA4 real-time dashboard bookmarked for L-Day monitoring

### Email Sequences
- [ ] Welcome sequence imported into MailerLite automation `{automation_name}`
- [ ] Trigger confirmed: fires when subscriber joins group `{mailerlite_group}`
- [ ] Test email sent to seed address — delivery, rendering, links all verified
- [ ] All 7 emails in nurture sequence accounted for (Day 0, 1, 3, 5, 7, 10, 14)
- [ ] Post-purchase sequence (5 emails) imported as separate automation
- [ ] Post-purchase trigger: fires on `purchase` event / paying customer tag
- [ ] Unsubscribe footer present in all emails
- [ ] From name and reply-to configured correctly

### Content — All Platforms
- [ ] Product Hunt submission drafted (tagline <40 chars, description, maker comment 300 words)
- [ ] PH thumbnail (240×240) + 4-6 screenshots (outcome-first, not feature-first) ready
- [ ] PH demo video (<45 seconds) edited and uploaded
- [ ] IndieHackers "Shipped" post drafted
- [ ] Reddit posts drafted for each target subreddit (value-first, not self-promo):
  - [ ] {subreddit_1} — angle: {angle}
  - [ ] {subreddit_2} — angle: {angle}
  - [ ] {subreddit_3} — angle: {angle}
- [ ] X/Twitter launch thread drafted (5-7 tweets, hook tweet is pain-first)
- [ ] LinkedIn post drafted (professional angle, storytelling format)
- [ ] Launch email to existing list drafted (founding member access, clear CTA)
- [ ] IG carousel (10 slides) ready — slide 1 = pain hook, slide 10 = CTA
- [ ] Short-form video (TikTok/Reels/Shorts) <60 seconds edited and ready to publish
- [ ] All copy humanized via the `humanize` skill — no AI cadence

### Supporter & Directory Prep
- [ ] Supporter list built: {N} contacts, segmented by timezone (APAC / EU / US)
- [ ] Personal outreach messages drafted — NOT asking for upvotes, asking for feedback
- [ ] Directory pre-submissions sent (see Directory list below)
- [ ] Product Hunt community engagement done: commented on 10+ launches in category over 2+ weeks

---

## 4-Wave Launch Execution

### Wave 1 — Inner Circle (Day -7)

**Purpose:** Warm up your most engaged supporters. Get early feedback. Build momentum before public launch.

**Channels:** Direct DM, email, private communities
**Timing:** 7 days before L-Day

| Action | Details | Assets Needed | Owner | Done |
|--------|---------|--------------|-------|------|
| Personal outreach to top supporters | "I'm launching {product_name} next week — want early access to give feedback?" | Supporter list, early access link | {owner} | ⬜ |
| Email inner circle subscribers | Exclusive early access, 1-week head start | Early access email draft | {owner} | ⬜ |
| Share in private Slack/Discord groups | Trusted communities only — ask for honest feedback | Landing page URL | {owner} | ⬜ |
| Gather early testimonials | Screenshot reactions, save positive quotes | — | {owner} | ⬜ |

**Messaging angle:** "I want your honest feedback before the world sees it."
**Assets needed:** Early access link, short personal message (not a template blast)

**Success metrics:**
- Early access users: >{N}
- Feedback messages received: >{N}
- Testimonials captured: >{N}
- Bugs/issues surfaced: any is good — fix them now

---

### Wave 2 — Community (Day -3)

**Purpose:** Build anticipation in relevant communities. Seed the product with helpful members who will organically spread it.

**Channels:** Reddit, IndieHackers, targeted Discord/Slack communities
**Timing:** 3 days before L-Day

| Action | Details | Assets Needed | Owner | Done |
|--------|---------|--------------|-------|------|
| Reddit teaser post | "Building something for {pain} — here's what I've learned" (no product pitch) | Teaser post draft | {owner} | ⬜ |
| IndieHackers build log update | Journey post — what you built, what you learned, what's coming | Build log post draft | {owner} | ⬜ |
| Discord/Slack community share | Value-first post in relevant servers — follow each server's rules | Community post drafts | {owner} | ⬜ |
| X/Twitter teaser thread | Problem-focused thread — the pain, the research, what you found | Teaser thread draft | {owner} | ⬜ |
| LinkedIn build-in-public post | Professional angle — what the market is missing | LinkedIn post draft | {owner} | ⬜ |

**Messaging angle:** "The problem is bigger than I thought — here's what the research showed."
**Assets needed:** Teaser content, validation insights to share (no product reveal yet)

**Success metrics:**
- Reddit post upvotes: >{N}
- IH build log views: >{N}
- Community engagement (comments, questions): >{N}
- Profile visits / landing page early traffic: >{N}

---

### Wave 3 — Public Launch (Day 0)

**Purpose:** Maximum coordinated distribution across all platforms in synchronized waves. Route everything to capture.

**Channels:** All platforms simultaneously
**Timing:** Launch day — execute in timezone waves

#### Pre-Wave (12:01 AM PT)
| Action | Details | Assets Needed | Owner | Done |
|--------|---------|--------------|-------|------|
| Submit to Product Hunt | Self-hunt. Tagline, description, screenshots, demo video, maker comment | PH submission package | {owner} | ⬜ |
| Notify APAC/EU supporters | Personal message: "We're live — would love your thoughts" | Supporter list (APAC/EU segment) | {owner} | ⬜ |
| Post to IndieHackers | "Shipped" format: build story + metrics + lessons + link | IH post draft | {owner} | ⬜ |
| Activate email welcome sequence | Confirm automation is live in MailerLite | — | {owner} | ⬜ |

#### Morning Wave (8–10 AM PT)
| Action | Details | Assets Needed | Owner | Done |
|--------|---------|--------------|-------|------|
| Reddit posts | 3-5 subreddits, staggered 30-60 min apart, value-first framing | Reddit post drafts per subreddit | {owner} | ⬜ |
| Launch email to full list | "It's live. Here's your founding member access." | Launch email draft | {owner} | ⬜ |
| Notify US East supporters | Personal outreach, US East timezone segment | Supporter list (US East) | {owner} | ⬜ |
| PH update: first metrics | Comment on own PH post with early numbers | Live signup count | {owner} | ⬜ |

#### Midday Wave (12–2 PM PT)
| Action | Details | Assets Needed | Owner | Done |
|--------|---------|--------------|-------|------|
| X/Twitter launch thread | 5-7 tweets. Hook = pain, not product. Pin thread. | Twitter thread draft | {owner} | ⬜ |
| LinkedIn launch post | Professional storytelling angle | LinkedIn post draft | {owner} | ⬜ |
| Notify US West supporters | Final timezone segment | Supporter list (US West) | {owner} | ⬜ |
| Cross-post updates | Update PH + IH with live metrics for social proof | Live data from GA4 | {owner} | ⬜ |

#### Afternoon Wave (3–6 PM PT)
| Action | Details | Assets Needed | Owner | Done |
|--------|---------|--------------|-------|------|
| Short-form video push | Publish to TikTok, IG Reels, YouTube Shorts simultaneously | Edited <60s video | {owner} | ⬜ |
| IG carousel post | Publish via `tools/lib/meta_api.py` — no manual Instagram step | IG carousel (10 slides) | {owner} | ⬜ |
| Community engagement | Discord/Slack servers — follow each community's rules | Community post drafts | {owner} | ⬜ |
| Activate ads (if budget) | Meta/Google ads — small daily spend, test creative | Ad creative + UTM links | {owner} | ⬜ |

**L-Day Continuous (all day):**
- [ ] Reply to EVERY comment within 15 minutes — all platforms
- [ ] Monitor GA4 real-time — share live milestones publicly ("100 signups!")
- [ ] Fix bugs in real-time — announce fixes publicly (builds trust)
- [ ] Screenshot and save all positive reactions — social proof for Days 2-7
- [ ] Route every reply/DM naturally toward the product

**Messaging angle:** "It's live. Here's what it does, here's the problem it solves, here's how to try it."
**Assets needed:** Full platform content pack (Twitter thread, LinkedIn post, IG carousel, video, Reddit posts, launch email)

**Success metrics (L-Day):**
| Metric | Target | Concerning |
|--------|--------|-----------|
| Product Hunt ranking | Top 5 | Below #10 |
| Signups | >{N} | <10 |
| Landing page conversion | 15–25% visitor→signup | <5% |
| Engagement quality | Questions, feedback, discussion | Silence or only "nice" |
| Revenue (Day 1) | Any — not expected but great signal | — |

---

### Wave 4 — Amplification (Day +3)

**Purpose:** Capitalize on launch momentum. Activate signups. Turn early users into social proof for the next wave.

**Channels:** All platforms, with focus on activation + second community push
**Timing:** Days 3–14 post-launch

| Day | Action | Platform | Purpose | Assets | Done |
|-----|--------|----------|---------|--------|------|
| +1 | Tutorial: "How to get {result} in 5 min" | All platforms (adapted per format) | Drive activation | Tutorial content pack | ⬜ |
| +2 | Behind-the-scenes: launch metrics + reactions | X, IH, LinkedIn | Build in public | GA4 screenshots, reaction screenshots | ⬜ |
| +3 | "What users are saying after 72 hours" | X, Reddit | Social proof | Testimonials captured on L-Day | ⬜ |
| +5 | Second community push — new subreddits or new angles | Reddit, Discord, forums | New audience segments | Community post drafts | ⬜ |
| +7 | PH update + "What I learned launching" | PH, X, IH, blog | SEO + build-in-public | Lessons post draft | ⬜ |
| +10 | User spotlight / case study | All platforms | Deep social proof | Interview one early user | ⬜ |
| +14 | "Two weeks in — here's the data" | X, IH, LinkedIn | Transparent update | GA4 report summary | ⬜ |

**Messaging angle:** "Here's what's happening. Real numbers, real users, real lessons."
**Assets needed:** Captured testimonials from L-Day, activation metrics from GA4, user stories

**Success metrics:**
- D3 activation rate (signups who returned): >50%
- D7 retention: >{N}%
- Week 1 revenue: ${N}
- Organic mentions (others sharing the product unprompted): >{N}
- Inbound requests from directory submissions: >{N}

---

## Product Hunt Submission Checklist

*Complete this section only if launching on PH.*

| Item | Spec | Status |
|------|------|--------|
| Tagline | <40 characters, benefit-first | ⬜ |
| Description | 260 characters max — problem → solution → CTA | ⬜ |
| Thumbnail | 240×240px, brand-consistent | ⬜ |
| Gallery screenshots | 4-6 images, 1270×952px — outcome-first, not feature list | ⬜ |
| Demo video | <45 seconds. Problem → demo → result. No slow intros. | ⬜ |
| Maker comment | 300 words: pain story → who it's for → why you built it → CTA | ⬜ |
| Topics/tags | 3 relevant PH topics selected | ⬜ |
| Hunter | Self-hunt or trusted hunter with audience | ⬜ |
| PH profile | Photo, bio, links up-to-date | ⬜ |
| Community warm-up | Commented on 10+ launches in category over 2+ weeks | ⬜ |
| Submission time | 12:01 AM PT for full 24h window | ⬜ |

**PH URL (after submission):** {ph_url}

---

## Directory Submissions List

Submit to these before launch day — many have review queues. Check status for each.

| Directory | URL | Category | Submitted | Live | Backlink |
|-----------|-----|---------|-----------|------|---------|
| Product Hunt | producthunt.com | All | ⬜ | ⬜ | DA 91 |
| BetaList | betalist.com | Startups/Beta | ⬜ | ⬜ | DA 66 |
| SaaSHub | saashub.com | SaaS | ⬜ | ⬜ | DA 63 |
| LaunchingNext | launchingnext.com | Startups | ⬜ | ⬜ | DA 42 |
| MicroLaunch | microlaunch.net | Indie/Micro SaaS | ⬜ | ⬜ | DA 38 |
| Uneed | uneed.best | Tools/Apps | ⬜ | ⬜ | DA 35 |
| AlternativeTo | alternativeto.net | SaaS alternatives | ⬜ | ⬜ | DA 78 |
| GetApp | getapp.com | SaaS | ⬜ | ⬜ | DA 74 |
| SaaSWorthy | saasworthy.com | SaaS reviews | ⬜ | ⬜ | DA 55 |
| Capterra | capterra.com | B2B SaaS | ⬜ | ⬜ | DA 85 |
| G2 | g2.com | B2B SaaS | ⬜ | ⬜ | DA 91 |
| ToolFinder | toolfinder.co | Tools | ⬜ | ⬜ | DA 32 |
| IndieHackers | indiehackers.com | Indie SaaS | ⬜ | ⬜ | DA 73 |
| HackerNews "Show HN" | news.ycombinator.com | Dev/tech | ⬜ | ⬜ | DA 92 |
| There's An AI For That | theresanaiforthat.com | AI tools | ⬜ | ⬜ | DA 64 |
| Future Tools | futuretools.io | AI tools | ⬜ | ⬜ | DA 58 |
| AI Tools Directory | aitoolsdirectory.com | AI tools | ⬜ | ⬜ | DA 45 |
| Toolify | toolify.ai | AI tools | ⬜ | ⬜ | DA 52 |
| DevHunt | devhunt.org | Dev tools | ⬜ | ⬜ | DA 30 |
| Startups.fyi | startups.fyi | Startups | ⬜ | ⬜ | DA 28 |
| Killer Startups | killerstartups.com | Startups | ⬜ | ⬜ | DA 51 |
| Startup Stash | startupstash.com | Tools for startups | ⬜ | ⬜ | DA 48 |
| {niche_directory_1} | {url} | {category} | ⬜ | ⬜ | DA {N} |
| {niche_directory_2} | {url} | {category} | ⬜ | ⬜ | DA {N} |

**Directory submission notes:**
- BetaList: submit 2-4 weeks before launch (they have a queue)
- G2/Capterra: require 1-2 weeks for approval
- AlternativeTo: add the product AND link to direct competitors
- HN "Show HN": post on weekday morning PT for max visibility

---

## Supporter Rally Plan

**Goal:** 150–300 genuine supporters who know the product and will engage naturally on L-Day.

### Building the List (pre-launch)
| Source | How to find them | Size | Action |
|--------|-----------------|------|--------|
| Email subscribers | Existing list | {N} | Segment engaged openers |
| Twitter followers | People who engaged with problem threads | {N} | DM personally |
| Reddit community members | People who upvoted or replied to your posts | {N} | DM or follow-up comment |
| Personal network | Colleagues, friends, peers who understand the space | {N} | Direct outreach |
| Discord/Slack connections | Members who engaged in community discussions | {N} | DM personally |

**Total supporter list target:** {N} contacts

### Segmentation by Timezone
| Segment | Size | PH Notify Time |
|---------|------|---------------|
| APAC (Asia-Pacific) | {N} | 12:01 AM PT (5-6 PM their time) |
| EU (Europe) | {N} | 12:01 AM PT (8-9 AM their time) |
| US East | {N} | 8 AM PT (11 AM ET) |
| US West | {N} | 12 PM PT |

### Outreach Message Template
*(Do NOT use as a template — personalize every message)*

**Pre-launch (Day -7):**
"Hey {name} — I'm launching {product_name} next week. You've been following my work on [related topic] and I think you'd have a useful perspective. Would you want early access to take a look before the public launch?"

**L-Day:**
"Hey {name} — {product_name} just went live on [platform]. Would mean a lot to get your genuine reaction — no pressure to say anything nice if it's not your thing!"

**Rules:**
- Never explicitly ask for upvotes — that violates PH guidelines
- Every message must be personal — reference something specific about them
- Send BEFORE L-Day, not on L-Day (people are busy on L-Day)
- Maximum 1 follow-up if no response

---

## Emergency Rollback Checklist

*If something goes critically wrong on L-Day — use this.*

### Rollback Decision Triggers
- [ ] Product crashes for >15% of visitors (check GA4 error events)
- [ ] Payment flow broken (no successful Stripe checkouts, errors in Stripe logs)
- [ ] Data loss or security issue discovered
- [ ] Misleading content published that must be retracted

### Rollback Steps
1. [ ] Post public acknowledgment immediately: "We're experiencing issues — investigating now." (Honest, no hiding)
2. [ ] Notify Max via Telegram immediately
3. [ ] Pause all ad spend (if running) — do not spend on broken traffic
4. [ ] Revert deployment to last stable version (via Railway/Vercel rollback)
5. [ ] Pause Product Hunt if submission is live — comment on PH post with honest update
6. [ ] Email list: "We're pausing briefly to fix something — we'll be back in X hours."
7. [ ] Fix the issue on staging first — verify fix before re-deploying
8. [ ] Re-deploy and verify manually end-to-end before re-enabling traffic
9. [ ] Post public update: "Fixed. Here's what happened and what we changed." (Transparency wins)
10. [ ] Resume PH, re-notify supporters if timing allows

**Key contacts:**
- Hosting: {Railway/Vercel dashboard URL}
- Domain: {Cloudflare/Namecheap URL}
- Stripe: dashboard.stripe.com
- MailerLite: dashboard.mailerlite.com

---

## Post-Launch Monitoring Checklist

### 24-Hour Check (L+1)
- [ ] Total signups (target: >{N})
- [ ] Landing page conversion rate (target: 15-25%)
- [ ] GA4: top traffic sources — what channels drove the most signups?
- [ ] GA4: bounce rate (>70% = landing page problem)
- [ ] Email sequence: Day 0 welcome email open rate (target: >60%)
- [ ] Stripe: any successful payments? Log first paying customer
- [ ] Product Hunt: final day ranking and vote count
- [ ] Reddit: post performance, any replies to engage with
- [ ] Fix any bugs surfaced by first users
- [ ] Screenshot and save all positive testimonials
- [ ] Activation rate: of Day 0 signups, how many used the core feature?

### 48-Hour Check (L+2)
- [ ] Total signups (cumulative)
- [ ] Day 1 activation rate: signups who returned on Day 2 (target: >50%)
- [ ] Email open rate: Day 1 origin story email
- [ ] Top converting channel: which UTM source is driving best quality signups?
- [ ] Community sentiment: any negative feedback patterns emerging?
- [ ] Directory submission status: check pending approvals
- [ ] PH follow-up comment: add "first 48 hours" update with metrics
- [ ] IH build log: post "24 hours later" update

### 1-Week Check (L+7)
- [ ] Total signups (target: >{N})
- [ ] Revenue (target: ${N})
- [ ] D7 retention: what % of Day 0 signups are still active?
- [ ] Email sequence performance: open rates per email (Day 0-5 emails sent by now)
- [ ] Activation rate: what % of total signups have used the core feature?
- [ ] Top 3 traffic sources by signup conversion (not just visits)
- [ ] Organic mentions: is anyone sharing the product without prompting?
- [ ] Competitor mentions: has anyone in target communities referenced the product?
- [ ] Blog / SEO: any search impressions in GSC for target keywords?
- [ ] Directory listings live: how many approved so far?
- [ ] Paid conversion: any paying customers? Revenue vs target?
- [ ] Churn: any refunds or cancellations? Flag reason.
- [ ] 1-week measure report delivered to Max
- [ ] Decision: double down, iterate, or pivot based on data?

---

*Ready to launch when all pre-launch checks are ✅ and Max approves.*
