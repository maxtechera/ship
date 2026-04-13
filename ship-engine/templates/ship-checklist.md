# 🚢 Ship Checklist: {{PRODUCT_NAME}}

> **Product:** {{PRODUCT_ONE_LINER}}
> **Target:** {{TARGET_AUDIENCE}}
> **Ticket:** {{LINEAR_TICKET}}
> **Created:** {{DATE}}

---

## Stage 1: Intake

### 1.1 Product Brief
- [ ] Product name confirmed
- [ ] URL captured (or "not deployed yet" noted)
- [ ] One-liner: what it does in one sentence
- [ ] Target user: who specifically has the pain (role, context, situation — not just "developers")
- [ ] Current state: idea / MVP built / fully deployed / already has real users
- [ ] Revenue model: free / freemium / paid / subscription / one-time / usage-based
- [ ] Max's angle: how this connects to his brand, audience, and credibility
- [ ] Existing users: if real users exist already, document them — they're the first social proof and interview candidates
- [ ] Sister products: document any related products in the same ecosystem and how this one fits
- [ ] Product type: B2C / B2B / developer tool / content product / infra / marketplace — this affects strategy downstream
- [ ] Buyer vs end user: are they the same person? (B2B: often no — capture both)

### 1.1b Intake Interview + Research Kickoff (research-first)
- [ ] Intake interview completed (`templates/prompts/intake-interview.md`)
- [ ] Run goal and success criteria captured in interview
- [ ] Constraints captured (brand/compliance/timeline/access)
- [ ] Research kickoff brief completed (`templates/prompts/intake-research-kickoff.md`)
- [ ] Unknowns explicitly listed and ranked
- [ ] Search seeds prepared (category/pain/competitors/persona/pricing)
- [ ] Research tasks kicked off before Validate execution
- [ ] Intake artifacts linked in Linear Artifacts section

### 1.2 Naming & Branding
- [ ] Domain availability checked and acquired (if needed)
- [ ] Social handles checked (@name on X, IG, GitHub, LinkedIn)
- [ ] Relationship to parent brand defined (separate, sub-brand, or same brand?)
- [ ] Logo and brand mark: create, commission, or confirm existing
- [ ] Brand colors and typography defined
- [ ] Favicon created

### 1.3 Linear Setup
- [ ] Create "Ship: {{PRODUCT_NAME}}" parent issue
- [ ] Add `ship-engine` label
- [ ] Set priority
- [ ] Sub-issues created for each stage (engine.py handles this automatically)

---

## Stage 2: Validate

*Goal: Go/no-go decision + deep audience intelligence. Every downstream stage pulls from this.*

### Stage 2 prerequisite
- [ ] Intake interview artifact exists and is linked
- [ ] Intake research kickoff artifact exists and is linked

### 2.1 Pain Discovery

**Mine every source before concluding. Real threads, real complaints, real quotes — not assumptions.**

- [ ] Reddit: search 5-10 relevant subreddits for pain threads (complaints, wishes, "is there a tool that...?")
- [ ] X/Twitter: search complaints, "I wish there was...", frustration threads
- [ ] HackerNews: threads where target audience discusses the problem
- [ ] IndieHackers: builders and users discussing the pain space
- [ ] Product Hunt: similar launches, comment sections, reception
- [ ] Google People Also Ask + AlsoAsked.com: actual question trees around the problem
- [ ] Answer the Public: real search queries about the problem
- [ ] Quora: long-form pain descriptions
- [ ] G2 / Capterra / App Store: 1-3 star reviews of alternatives (best copy source)
- [ ] GitHub Issues: issues and discussions on related open-source projects
- [ ] YouTube comments: complaints under tutorials or reviews in the space
- [ ] LinkedIn: posts and comments from professionals describing the pain (critical for B2B)
- [ ] Niche Discord / Slack / Telegram communities: community-specific discussions
- [ ] Job postings: companies hiring to solve this problem manually = strong demand signal (B2B)
- [ ] Existing user interviews: if real users already exist, interview them FIRST before secondary research
- [ ] Document: for each pain point — exact quote, source URL, engagement (upvotes/replies), date
- [ ] Categorize pain points by theme
- [ ] Rank by frequency and intensity

### 2.2 Audience Profiling

- [ ] Who EXACTLY has this pain? (not "developers" — which developers? what stack, company size, job title, career stage?)
- [ ] For B2B: Who is the BUYER? (often different from the end user — document both separately)
- [ ] Where do they hang out? List specific: subreddits, Discord servers, Slack groups, newsletters, podcasts, X accounts, YouTube channels
- [ ] What language do they use? Capture exact words and phrases — this is the copy bank
- [ ] What have they already tried? Existing solutions, workarounds, DIY approaches
- [ ] What makes them switch? Price? Features? UX? Integration? Trust? Compliance?
- [ ] What triggers them to search for a solution? (the specific moment the pain becomes acute)
- [ ] What are they currently paying (in money or time) to deal with this problem?

### 2.3 Competitor Landscape

- [ ] List all direct competitors (same category, same buyer)
- [ ] List indirect competitors (different solution to same problem)
- [ ] Map pricing models: tiers, price points, free vs paid, billing model
- [ ] Document competitor weaknesses from their own users' reviews (1-3 star reviews)
- [ ] Find the gap that exists across all competitors — what is NOBODY doing well?
- [ ] Estimate competitor traffic / user base (SimilarWeb, GitHub stars, social following)
- [ ] Find at least 2-3 failed products in this space — why did they fail?

### 2.4 Demand Signals

- [ ] Google Trends: core keywords — growing / stable / declining?
- [ ] Search volume for top 10 keywords
- [ ] CPC for key terms (high CPC = commercial intent = people paying to reach this audience)
- [ ] GitHub stars on related open-source projects
- [ ] Social conversation volume trends
- [ ] Job postings mentioning the problem domain (B2B demand signal)
- [ ] Community growth rates for relevant subreddits / Discord servers

### 2.5 Willingness to Pay

- [ ] Document what people currently pay for alternatives (exact pricing)
- [ ] Find threads where people discuss paying for solutions or workarounds
- [ ] Calculate workaround cost (time × hourly rate = implicit willingness to pay)
- [ ] Price anchor range identified: "they're paying $X for worse, so they'll pay $Y for better"
- [ ] Find evidence of DIY solutions: someone building this themselves = unmet demand with budget

### 2.6 Max's Angle

- [ ] Does Max's existing audience overlap with target buyers? (direct / adjacent / no overlap)
- [ ] Is there a Spanish-language advantage for this product? (less competition, underserved market)
- [ ] Can Max make 10+ content pieces about this problem authentically?
- [ ] Is there a credibility claim? ("I built this to solve my own problem")
- [ ] Brand fit: does this align with what Max is building publicly?

### 2.7 ICP Document (Standalone Deliverable)

*The ICP is a living document referenced by ALL downstream stages. It is a first-class deliverable.*

- [ ] Demographics: role, experience level, company size, geography, language
- [ ] Psychographics: what they value, what frustrates them, what motivates buying decisions
- [ ] Behaviors: where they spend time online, how they discover tools, how they evaluate and buy
- [ ] Pain triggers: specific moments when the pain is worst
- [ ] Budget: what they're currently spending on this problem (money or time)
- [ ] For B2B products: separate ICP sections for BUYER and END USER
- [ ] ICP Document saved to run directory (`runs/{{TICKET}}/icp.md`)

### 2.8 Voice of Customer (VoC) Bank (Standalone Deliverable)

*The VoC Bank is the copy bank for ALL downstream stages. Every agent pulls from it. No need to invent language.*

- [ ] Top 30+ real quotes from target audience about their pain (with sources)
- [ ] Phrases they use to describe the pain (exact words, not paraphrased)
- [ ] Phrases they use to describe the ideal solution
- [ ] Phrases they use to describe alternatives (what they like and hate)
- [ ] Words they use in reviews, complaints, and wishes
- [ ] Categorize quotes by theme and use-case (e.g., "pain: too expensive", "frustration: complex setup", "desire: team-wide solution")
- [ ] VoC Bank saved to run directory (`runs/{{TICKET}}/voc-bank.md`)

### 2.9 Validation Scorecard

| Signal | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|---------|
| Pain frequency | 25% | — | — |
| Willingness to pay | 25% | — | — |
| Competition gap | 20% | — | — |
| Audience fit | 15% | — | — |
| Market timing | 15% | — | — |
| **Total** | 100% | — | **—** |

- [ ] Scoring: Pain Frequency (1=no threads, 3=monthly moderate engagement, 5=weekly 100+ upvotes)
- [ ] Scoring: Willingness to Pay (1=no evidence, 3=using free workarounds reluctantly, 5=paying $50+/mo for bad alternatives)
- [ ] Scoring: Competition Gap (1=saturated with good options, 3=options exist but poor UX, 5=nothing good exists)
- [ ] Scoring: Audience Fit (1=zero overlap with Max's audience, 3=adjacent, 5=Max's audience IS the target)
- [ ] Scoring: Market Timing (1=declining interest, 3=stable, 5=growing trend or new enabling tech)
- [ ] Validation Report written: evidence, scoring, recommendation
- [ ] ICP Document attached to report
- [ ] VoC Bank attached to report
- [ ] 🔒 **APPROVAL GATE: Max decides — Ship / Explore / Kill**

---

## Stage 3: Strategy

*Takes the validated intelligence and turns it into the go-to-market playbook. Everything parallel stages do flows from this.*

### 3.1 Positioning

- [ ] One-liner tagline: what is this in under 10 words
- [ ] Value proposition: pain → solution → outcome (using VoC language — not invented language)
- [ ] Competitive positioning: "Why us over [X]" for each top 2-3 competitors. Specific — not "we're better" but "they charge $X for Y, we do Z for free"
- [ ] Differentiation: the specific gap we own (from validation)
- [ ] Positioning angle chosen: cost savings / security / simplicity / speed / control / quality
- [ ] Brand voice defined for this product
- [ ] Positioning statement: "For [audience] who [pain], {{PRODUCT_NAME}} is [category] that [benefit] unlike [competitor] because [differentiator]"

### 3.2 Pricing

- [ ] Competitive pricing research: what do alternatives charge? Model, tiers, free vs paid, billing cycle?
- [ ] Audience payment expectations: what did validation reveal about willingness to pay?
- [ ] Pricing model chosen: per-seat / per-unit / usage-based / flat rate / hybrid
- [ ] Tier structure: what's free, what's paid, what triggers upgrade. Name the tiers.
- [ ] Price points set and anchored against competitor research
- [ ] Free vs paid feature gates defined
- [ ] Billing cycle: monthly / annual / both (annual discount %)
- [ ] Launch pricing: special offer for early adopters — what, how much, how long, how many (must be real)
- [ ] Guarantee: money-back period, trial length, refund terms
- [ ] Pricing psychology applied: anchoring, decoy tier, "most popular" designation, founding member framing
- [ ] For B2B products: team/seat pricing tiers, volume discounts, enterprise "contact us" tier
- [ ] For multi-product ecosystems: pricing aligned across product family (no cannibalization)

### 3.3 Channel Strategy

- [ ] Primary acquisition channels chosen (top 2-3 from validation audience data)
- [ ] Content strategy: platforms, formats, themes mapped to pain points from ICP
- [ ] Competitor comparison content planned: "[Product] vs [Competitor]", "[Competitor] alternative", "Best [category] tools" — for SEO and search traffic
- [ ] Community strategy: own community vs participate in others?
- [ ] Partnership / distribution strategy (if applicable)
- [ ] For developer tools: GitHub, Dev.to, Hashnode, HackerNews as primary platforms (conditional)
- [ ] For B2B: LinkedIn as channel for decision-makers
- [ ] For infrastructure/cloud products: cloud marketplace listings (AWS Marketplace, etc.) as medium-term channel (conditional)

### 3.4 Product Readiness

*The engine doesn't build. But the product must be READY before launch. These are pre-launch gates, not build tasks.*

**Security (must-haves):**
- [ ] Authentication is secure: session management, HttpOnly/Secure cookies, timing-safe comparisons
- [ ] Rate limiting on login, signup, auth callbacks, and all write endpoints
- [ ] Input validation on all user inputs
- [ ] CSRF protection on all state-changing requests
- [ ] SQL injection prevention (parameterized queries)
- [ ] API rate limiting (per-user and per-IP)
- [ ] Environment variable validation at startup (fail fast, not silently)
- [ ] Secrets management: never in code, never in logs, proper rotation
- [ ] Security headers set: HSTS, X-Frame-Options, CSP, X-Content-Type-Options, Referrer-Policy
- [ ] Dependency vulnerability scan (npm audit / Snyk)
- [ ] RBAC / authorization checks on all endpoints
- [ ] Pen test or vulnerability scan run (even self-directed)

**Infrastructure & reliability:**
- [ ] Production environment deployed and stable
- [ ] Monitoring active: health checks, uptime monitoring
- [ ] Error tracking active (Sentry or equivalent)
- [ ] Alerting configured for critical failures
- [ ] Backup system running and tested
- [ ] Status page configured
- [ ] Load test: can it handle launch traffic?
- [ ] Rollback procedure documented and tested

**Testing & QA:**
- [ ] Core user journey tested end-to-end
- [ ] Mobile responsive (test 5 screen sizes)
- [ ] Cross-browser: Chrome, Firefox, Safari, Edge
- [ ] Error states tested (offline, API errors, expired sessions)
- [ ] Payment flow tested end-to-end (if applicable)
- [ ] Signup → onboarding → activation → billing tested end-to-end

**Legal & compliance:**
- [ ] Terms of Service live (even if minimal)
- [ ] Privacy Policy live (must be accurate to actual data practices)
- [ ] Acceptable Use Policy (if applicable)
- [ ] Cookie consent banner (if applicable)
- [ ] Data retention and deletion procedure documented
- [ ] Open-source license compatibility reviewed

**Documentation:**
- [ ] Getting Started guide live (new user to first value in under 10 minutes)
- [ ] FAQ written (from validation pain threads and validation objections)
- [ ] Troubleshooting guide (top 10 issues)
- [ ] For technical products: architecture overview and security documentation (B2B buyers read these)
- [ ] For products with integrations: integration setup guide per provider

**Operational readiness:**
- [ ] Customer support channel defined (email, chat, Discord, or all)
- [ ] Support tiers defined (free: community, paid: email, enterprise: dedicated)
- [ ] Internal support playbook written (common issues → solutions)
- [ ] Per-customer infrastructure cost estimated (unit economics sanity check)

### 3.5 Phased Execution Plan

- [ ] Phase 1: Parallel prep deliverables listed per agent
- [ ] Phase 2: Launch execution plan (pre-launch, L-Day, post-launch)
- [ ] Phase 3: Measure and iterate plan
- [ ] Dependencies between phases made explicit
- [ ] "Done" criteria defined for each phase

### 3.6 Budget

- [ ] All costs estimated: domains, APIs, ad spend, tools, content production
- [ ] Breakdown by category
- [ ] Max approves budget before parallel stages spend anything

### 3.7 Success Targets

- [ ] 7-day targets: visitors, signups, activation, revenue
- [ ] 30-day targets: MRR, users, activation rate, churn
- [ ] "Activation" defined: what action proves a user got value?
- [ ] "Retention" defined: what proves they're staying?
- [ ] Kill criteria defined: what numbers after 30 days mean it's not working?
- [ ] For B2B: team-level metrics defined (seats per team, team activation rate, expansion rate)

### 3.8 Ship Plan Delivery

- [ ] Ship Plan written (single reference document for all parallel agents)
- [ ] ICP and VoC Bank linked in Ship Plan (agents load these as context)
- [ ] Budget included in Ship Plan
- [ ] Success targets included
- [ ] Parallel stages auto-start after Ship Plan delivery

---

## Stage 4: Parallel — Awareness Agent

*Everything that's content, copy, or public-facing flows through here.*

### 4.1 Landing Page Copy

- [ ] Hero section: problem-first, not feature-first (uses VoC language directly)
- [ ] How It Works section: 3-step visual, outcome-focused
- [ ] Features section: each feature tied to a user outcome (not just a feature description)
- [ ] "Who It's For" section: speaks directly to ICP
- [ ] Social proof section: testimonials, logos, numbers, quotes (use real users if they exist)
- [ ] Pricing section: clear tier comparison (copy points to Closing Agent's pricing)
- [ ] FAQ section: pulled from validation pain threads and common objections
- [ ] CTA section: clear primary action, low friction
- [ ] For B2B products: "Book a Demo" CTA alongside self-service signup
- [ ] SEO: target keywords in title, H1, meta description, URL slugs
- [ ] OG meta tags: title, description, image (test share preview)
- [ ] Twitter Card meta tags
- [ ] Structured data: Organization, Product, FAQ schema
- [ ] All copy uses VoC language — no invented language, no AI-sounding text
- [ ] All copy humanized (run through the `humanize` skill)

### 4.2 Visual Assets

- [ ] OG image (1200×630) for link previews — reflects product value at a glance
- [ ] Social share images adapted per platform (Twitter, LinkedIn, Facebook)
- [ ] Product screenshots: polished, real data, show the actual aha moment
- [ ] Demo GIF: core flow in under 30 seconds
- [ ] Architecture or workflow diagram (for technical products: this IS marketing)
- [ ] Logo in formats: SVG, PNG light/dark, favicon
- [ ] Video thumbnail (1280×720)

### 4.3 Video Content

- [ ] Demo video script: hook → problem → solution → demo → CTA. Under 3 minutes.
- [ ] Short-form script (<60s): hook → problem → result → CTA. For TikTok/Reels/Shorts.
- [ ] Hooks written for each video: visual hook, verbal hook, narrative hook (research 2026 viral patterns)
- [ ] Storyboards: enough detail for talent to execute — key scenes, transitions, what appears on screen
- [ ] AI first pass: fully AI-generated video using AI avatar, images, or animation as a reference cut
- [ ] Talent ticket created: "Record this video. Script, storyboard, AI first-pass attached. [estimated time]"
- [ ] All talent tickets added to the Talent Tickets Queue (see Meta section)

### 4.4 Content Pieces

*Created once, adapted for all platforms.*

- [ ] Launch announcement: the story — why this exists, who it's for, CTA
- [ ] Product demo/tutorial: show getting to the aha moment
- [ ] Origin/behind-the-scenes story: what inspired this, the building journey
- [ ] Competitor comparison: "{{PRODUCT_NAME}} vs [Top Competitor]" (for SEO + positioning)
- [ ] "Alternative to [Competitor]" piece (targets competitor search traffic)
- [ ] Pain-keyword article: educational deep-dive on the problem (for SEO)
- [ ] "How I achieved [outcome] with {{PRODUCT_NAME}}" tutorial
- [ ] For developer/technical products: architecture walkthrough, technical deep-dive (conditional)
- [ ] All content runs through VoC Bank — no paraphrasing, use their exact language
- [ ] All copy humanized before publishing

### 4.5 Platform Adaptations

*One piece of content → all platforms. Adapt format, not message.*

- [ ] IG carousel: hook → problem → solution → CTA (slide by slide)
- [ ] X/Twitter thread: 5-7 tweets, hook tweet about the pain (not the product), build to CTA
- [ ] LinkedIn post: professional angle, storytelling format, industry insight framing
- [ ] TikTok/Reels/Shorts: hook-driven, <60s, subtitles, problem → solution → CTA
- [ ] YouTube video: full demo or educational (5-15 min)
- [ ] Blog post: long-form, SEO-optimized, pain → solution → tutorial
- [ ] Reddit post: value-first format, problem description, solution mentioned naturally
- [ ] HackerNews: "Show HN" format — what it is, why you built it, technical credibility (conditional: developer/technical products)
- [ ] Dev.to / Hashnode article: technical depth, developer-first framing (conditional: developer products)

### 4.6 Build-in-Public Pre-Launch Content

*Generates anticipation. Every post is also audience research — see what resonates.*

- [ ] Origin story post: "Why I built this" — the problem I had, what I tried, what I built
- [ ] Early screenshots / previews: "This is what [X] looks like in {{PRODUCT_NAME}}"
- [ ] Process post: "One insight I discovered while building this"
- [ ] Problem poll: "How does your team currently deal with [X]?" — generates signal + audience
- [ ] Teaser: "Building something for people who [pain]. Launching soon."
- [ ] "X problems I discovered while researching this" — validation data as content
- [ ] At least 2 weeks of pre-launch content published before L-Day

### 4.7 Community Presence

- [ ] List all communities from validation where ICP hangs out
- [ ] Map self-promo rules for each community (before posting)
- [ ] Community playbook: per-community engagement strategy (how to engage, what to post, rules)
- [ ] Identify top 20 existing pain threads to reply to (genuine value, no product mention)
- [ ] Start engaging 2+ weeks before launch (be a known, trusted member before mentioning product)
- [ ] Draft community posts and replies for approval (all public-facing content needs Max review)

### 4.8 Platform-Specific Pre-Launch Prep

- [ ] **Product Hunt:** Profile complete (photo, bio, links). Comment thoughtfully on 10+ launches in your category over 2+ weeks. Engage with makers. Build recognition before your own launch.
- [ ] **Reddit:** Accounts have 100+ karma in relevant subreddits. Post valuable content (not product) in target subs for 2+ weeks. Be a known, helpful member before mentioning any product.
- [ ] **IndieHackers:** Build log / journey updates posted. Engaging in discussions. Credibility established.
- [ ] **X/Twitter:** Thread about the problem space. Share insights from validation research. Audience around the pain (not the product).
- [ ] **LinkedIn:** Professional perspective on the problem. Connected with ICP-matching people. (B2B)
- [ ] **HackerNews:** 2-3 thoughtful comments on AI tooling / developer tool threads. (conditional: developer products)
- [ ] **Dev.to / Hashnode:** 1-2 educational articles published under Max's byline. (conditional: developer products)
- [ ] **GitHub:** Repository exists with quality README. Star-worthy. (conditional: open-source component)

### 4.9 Directory Pre-Submissions

*Submit BEFORE launch day. Most have review queues of days to weeks.*

**Universal (submit all):**
- [ ] BetaList
- [ ] SaaSHub
- [ ] LaunchingNext
- [ ] MicroLaunch
- [ ] Uneed
- [ ] AlternativeTo (add as alternative to top 3 competitors)
- [ ] SaaSWorthy

**If AI-related:**
- [ ] There's An AI For That
- [ ] Futurepedia
- [ ] AI Tools Directory
- [ ] ToolFinder

**If developer/infra tool:**
- [ ] Dev Hunt
- [ ] Awesome [category] GitHub list (open a PR to be included)
- [ ] AWS Marketplace (medium-term, requires partner enrollment)

**If productivity/B2B tool:**
- [ ] G2 (create product listing)
- [ ] Capterra
- [ ] GetApp

- [ ] Track submission status for each directory (many take 1-2 weeks to review)
- [ ] Follow up on pending submissions after 5 days

### 4.10 SEO

- [ ] Competitor comparison pages planned: "{{PRODUCT_NAME}} vs [Competitor 1]", "{{PRODUCT_NAME}} vs [Competitor 2]"
- [ ] "[Competitor] alternative" page planned
- [ ] "Best [category] tools" article planned
- [ ] Pain-keyword articles planned (from validation keyword research)
- [ ] Landing page SEO: title, H1, meta description, URL slugs — all optimized for primary keywords
- [ ] Internal linking structure planned

### 4.11 Content Calendar

- [ ] D-14 to D-7: Build-in-public posts (2-3/week across platforms)
- [ ] D-7: Teaser: "Building something for [pain]. Launching [timeframe]."
- [ ] D-5: First SEO article published
- [ ] D-3: Sneak peek: screenshot or GIF preview
- [ ] D-2: Second article / content published
- [ ] D-1: "Tomorrow" teaser across all platforms
- [ ] D0: All launch content live (see Launch stage)
- [ ] D+1 through D+14: Post-launch content cadence (see Launch stage)
- [ ] D+14+: Sustained distribution content (see Launch stage)

### 4.12 Collaboration Outputs

- [ ] Share resonating messaging and community feedback → Lead Capture Agent
- [ ] All content available for Nurture Agent to repurpose for email sequences
- [ ] All talent tickets created and added to queue

---

## Stage 5: Parallel — Lead Capture Agent

*Turn attention into captured leads. Hormozi/acquisition.com style offer engineering.*

### 5.1 Offer Engineering

*If acquisition.com was our lead capture company — that's the level.*

- [ ] **Value stack:** List every deliverable/feature/outcome. Assign perceived value to each. Total = "you're getting $X worth of value."
- [ ] **Lead magnet design:** What free thing is so valuable it feels like stealing? Guide, template, tool, free tier, checklist, audit, mini-course. The lead magnet must be intrinsically valuable — not "download our brochure."
- [ ] **Risk reversal:** What removes all risk? Money-back guarantee, free trial, "keep the bonuses even if you cancel."
- [ ] **Irresistible offer construction:** Price anchoring (value $X, price $Y), value-to-price ratio clearly communicated, urgency/scarcity that is REAL.
- [ ] **Offer stacking:** How do bonuses, guarantees, features, and pricing layer to make the offer feel like a no-brainer?
- [ ] Launch pricing defined: what is the early adopter special? Who qualifies? How long does it last? How many spots?
- [ ] Free tier defined (if applicable): what can someone get for free that still makes them a real user?

### 5.2 Lead Magnets (create 2-3)

- [ ] Lead magnet #1: High-value free resource (guide, checklist, template, tool)
- [ ] Lead magnet #2: Free tier or trial of the actual product (most powerful for SaaS)
- [ ] Lead magnet #3: Exclusive or bonus content (reserved for early adopters)
- [ ] Each lead magnet: delivery mechanism defined, landing page or gate configured
- [ ] Track which lead magnet converts best

### 5.3 Funnel Architecture

*Every entry point must have a clear capture mechanism.*

- [ ] Social (X, IG, LinkedIn, TikTok) → bio link / post CTA → landing page → signup
- [ ] Search (SEO article) → in-content CTA → landing page → signup
- [ ] Communities (Reddit, HN, Discord) → helpful reply → profile → landing page → signup
- [ ] Email (existing list) → campaign CTA → landing page → signup/purchase
- [ ] Product Hunt / directories → landing page → signup
- [ ] Word of mouth / referral → landing page → signup
- [ ] For B2B products: decision-maker funnel → "Book a Demo" path → assisted onboarding
- [ ] For developer tools: GitHub README → landing page / signup
- [ ] For open-source components: GitHub stars → interested users → email capture

### 5.4 UTM Tracking

- [ ] UTM link created for every channel: `?utm_source=&utm_medium=&utm_campaign=`
- [ ] UTM naming convention documented and consistent
- [ ] UTM links embedded in all published content before launch
- [ ] UTM tracking verified in analytics (events firing correctly)

### 5.5 Email Capture

- [ ] Dedicated email list/group created for this product
- [ ] Signup form on landing page: tested, mobile-friendly, GDPR-compliant
- [ ] Lead magnet delivery mechanism configured
- [ ] Anti-spam protection (reCAPTCHA or honeypot)
- [ ] Form error handling tested

### 5.6 Analytics & Tracking

- [ ] GA4 property created (or existing property confirmed for this product)
- [ ] Key conversion events configured: signup_start, signup_complete, activation, payment, demo_request
- [ ] Google Search Console verified
- [ ] Funnel visualization set up: where are people dropping off?
- [ ] All GA4 events tested and verified firing before launch
- [ ] Real-time analytics dashboard confirmed working

### 5.7 Product Hunt Supporter List

- [ ] Build a list of 150-300 supporters segmented by timezone (APAC / EU / US)
- [ ] Warm them up: ask for product feedback (NOT asking for upvotes — that gets flagged)
- [ ] Day-of: they'll engage naturally because they care about the product
- [ ] List organized: name, Slack/DM contact, timezone

### 5.8 Collaboration Outputs

- [ ] Finalized offer stack shared → Awareness Agent (all content points to the same offer)
- [ ] Lead magnet context shared → Nurture Agent (email #1 must deliver on the promise)
- [ ] Funnel architecture shared → Closing Agent (maps where paid conversion happens)

---

## Stage 6: Parallel — Nurture Agent

*Move leads from "just signed up" to "ready to buy."*

### 6.1 Email Welcome Sequence

| Email | Day | Purpose |
|-------|-----|---------|
| Welcome | 0 | Deliver promised lead magnet. Set expectations. Get to first value immediately. |
| Origin Story | 1 | Why this exists, the pain that inspired it. Build personal connection. |
| Tutorial | 3 | Show how to get maximum value. Drive activation. |
| Social Proof | 5 | What others experience. Testimonials and results. Make it real. |
| Objection Killer | 7 | Address the #1 reason people don't buy (from ICP data + VoC Bank). |
| Urgency | 10 | Early bird ending, limited spots, price increasing — whatever's real. |
| Last Call | 14 | Final push. Clear CTA. After this: regular newsletter cadence. |

- [ ] Each email: subject line, preview text, body copy, CTA
- [ ] All email copy uses VoC language (pulled from VoC Bank by Awareness Agent)
- [ ] All email copy humanized
- [ ] Sequence logic defined: triggers, timing, conditions
- [ ] Automation configured and tested
- [ ] A/B test subject lines on emails 1, 3, and 6
- [ ] Unsubscribe link tested
- [ ] Deliverability confirmed (SPF/DKIM/DMARC for sending domain)
- [ ] Test send to Gmail, Outlook, Yahoo (check rendering)

### 6.2 Sequence Logic

- [ ] Welcome email triggered immediately on signup
- [ ] Subsequent emails on schedule
- [ ] Condition: if user converts to paid, stop urgency emails
- [ ] Condition: if user unsubscribes, stop all emails
- [ ] After day 14: transition to regular newsletter cadence (not abandoned)

### 6.3 Content Drip (Social — between launch and D+14)

- [ ] What to post on which platforms to maintain awareness while email does heavy nurturing
- [ ] Content repurposed from Awareness Agent (not new creation)
- [ ] Maintains launch momentum without creating new content from scratch

### 6.4 Retargeting (conditional: if ad budget exists)

- [ ] Audience #1: visited landing page, didn't sign up → reminder ad
- [ ] Audience #2: signed up, never activated → activation prompt ad
- [ ] Audience #3: activated, didn't pay → conversion push ad
- [ ] Ad creative direction defined per audience
- [ ] Budget caps set

### 6.5 Collaboration Outputs

- [ ] Objection data from email replies → Closing Agent (what objections are coming up?)
- [ ] Drop-off points in sequence → Closing Agent (where are leads stalling?)
- [ ] Content pieces available → Awareness Agent (high-performing email content can become social content)

---

## Stage 7: Parallel — Closing Agent

*Convert warm leads into paying customers. Remove every friction point.*

### 7.1 Pricing Implementation

- [ ] Final pricing tiers confirmed (from Strategy)
- [ ] Tiers named
- [ ] Launch pricing configured: discount amount, duration, limit (must be real scarcity)
- [ ] Guarantee terms finalized: duration, conditions, process
- [ ] Annual vs monthly: both options available? Annual discount shown clearly?
- [ ] Pricing page copy direction given to Awareness Agent

### 7.2 Payment Flow

- [ ] Stripe products and prices created per tier
- [ ] Checkout experience defined: what the user sees, clicks, and receives
- [ ] Receipt and confirmation flow tested
- [ ] Access provisioning: how does a paying user get access immediately (no manual steps)?
- [ ] Webhook handling: subscription created, updated, canceled, payment_failed
- [ ] Billing portal available (Stripe Customer Portal or equivalent)
- [ ] Coupon / promo code support for launch offer
- [ ] Monthly subscription tested end-to-end
- [ ] Annual subscription tested end-to-end
- [ ] Upgrade/downgrade tested
- [ ] Cancel and refund tested
- [ ] Failed payment → dunning → recovery tested
- [ ] International currencies tested (if applicable)

### 7.3 Conversion Triggers

- [ ] Free tier limit: in-product upgrade prompt designed and built
- [ ] Feature gating: premium features clearly marked, upgrade prompt designed
- [ ] Trial expiry: in-product notification + email notification
- [ ] Social proof trigger: "X people using this" or recent user activity (builds FOMO)
- [ ] Urgency: countdown or limited spots shown (only if real)
- [ ] Each trigger: where it appears, what it says, what it links to

### 7.4 Objection Handling

- [ ] Top 3-5 objections from ICP data and competitor reviews documented (pull from VoC Bank)
- [ ] Response for each objection written
- [ ] Where each response appears: FAQ, pricing page, email, in-product
- [ ] ROI framing: "this problem costs you $X/month → solution costs $Y/month"
- [ ] Objections shared with Awareness Agent (for landing page FAQ)
- [ ] Objections shared with Nurture Agent (for email sequence)

### 7.5 Post-Purchase Flow

- [ ] Day 0 (immediate): onboarding email — how to get to first value in <5 minutes
- [ ] Day 0 (in-product): first-run experience that leads to aha moment (2 steps max)
- [ ] Day 1: check if setup is working. If not activated → nudge email with direct path.
- [ ] Day 3: check-in email — "How's it going? Reply if you need help." (personal-feeling)
- [ ] Day 7: testimonial / review ask
- [ ] Day 14: referral program invitation or upsell (if tiers exist)
- [ ] Day 30: retention check — usage report or expansion nudge
- [ ] For B2B: admin onboarding guide (team setup, user invitation, configuration)
- [ ] For B2B: check-in at team level, not just individual user

### 7.6 Collaboration Outputs

- [ ] Testimonials and early results → Awareness Agent (feeds social proof content loop)
- [ ] Objection data from purchases and support → Nurture Agent (for objection killer email)

---

## Approval Gate: Pre-Launch 🔒

*Max reviews readiness before launch execution begins.*

| Area | Status | Key check |
|------|--------|----------|
| Product | ⬜ | App live, working, mobile-responsive? |
| Security | ⬜ | All must-fix security issues resolved? |
| Awareness | ⬜ | All content and assets ready? Community presence built? Talent recordings done? |
| Lead Capture | ⬜ | Offer stack engineered? Funnels live? Tracking working? |
| Nurture | ⬜ | Email sequence ready? Automation configured? |
| Closing | ⬜ | Payment flow working? Pricing live? Post-purchase configured? |
| Legal | ⬜ | ToS and Privacy Policy live? |
| Documentation | ⬜ | Getting Started and FAQ live? |
| Analytics | ⬜ | GA4 events verified? UTMs working? |
| Supporters | ⬜ | Supporter list ready, segmented by timezone? |

- [ ] 🔒 **APPROVAL GATE: Max decides — Launch / Fix Issues / Kill**

---

## Stage 8: Launch

### Phase 1: Pre-Launch Warm-Up (Before L-Day)

*Parallel agents have already built assets. This phase is about anticipation and priming.*

- [ ] Build-in-public content published for at least 2 weeks
- [ ] Waitlist / early access open (if applicable) — waitlist size is a demand signal
- [ ] PH profile and pre-launch engagement complete (10+ comments over 2+ weeks)
- [ ] Reddit karma and community standing established
- [ ] IndieHackers build log published
- [ ] X/Twitter audience built around the problem space
- [ ] LinkedIn network primed (B2B)
- [ ] HackerNews recognition built in relevant threads (conditional: developer products)
- [ ] All directory submissions sent (with tracking spreadsheet)
- [ ] Supporter list ready with timezone segments

**Pre-Launch Final Checklist:**

| Check | Status |
|-------|--------|
| Product URL live, core feature works, mobile responsive | ⬜ |
| Landing page copy final, OG tags working, share preview correct | ⬜ |
| Analytics tracking verified (GA4 events firing, UTMs working) | ⬜ |
| Payment / checkout flow tested end-to-end | ⬜ |
| Email capture forms live and tested | ⬜ |
| Welcome email sequence active and tested | ⬜ |
| All launch content drafted per platform | ⬜ |
| Product Hunt submission drafted (tagline, description, images, maker comment) | ⬜ |
| HackerNews Show HN post drafted (conditional: developer/technical products) | ⬜ |
| Reddit posts drafted per subreddit (value-first, not self-promo) | ⬜ |
| IndieHackers "Shipped" post drafted | ⬜ |
| X/LinkedIn launch content drafted | ⬜ |
| Dev.to / Hashnode article ready to publish (conditional: developer products) | ⬜ |
| Video content recorded and edited (from talent tickets) | ⬜ |
| Launch email to existing list drafted | ⬜ |
| Directory submissions sent | ⬜ |
| Supporter list ready with timezone segments | ⬜ |
| <15 min response capability confirmed for L-Day | ⬜ |
| Legal: ToS, Privacy Policy live | ⬜ |
| Documentation live (Getting Started, FAQ, Troubleshooting) | ⬜ |
| Status page green | ⬜ |
| Support channel ready | ⬜ |
| Backup and monitoring verified | ⬜ |

### Phase 2: Launch Day (L-Day)

*Best days: Tuesday, Wednesday, Thursday.*

**Wave 1 — Night Launch (12:01 AM PT / 03:01 AM ET / 08:01 AM UTC)**

- [ ] Submit Product Hunt: tagline under 40 chars, contextual thumbnail, 4-6 outcome-first screenshots, <45s demo video, 300-word maker comment (pain → who it's for → why you built it → CTA)
- [ ] Notify APAC/EU supporters: personal message, "we're live — let me know what you think"
- [ ] Post to IndieHackers: "Shipped" format — build story, metrics from validation, what you learned, link

**Wave 2 — Morning (8-10 AM PT / 11 AM-1 PM ET)**

- [ ] Reddit posts: post in 3-5 relevant subreddits, value-first format, staggered 30-60 min apart
- [ ] HackerNews Show HN post (conditional: developer/technical products) — monitor and respond immediately
- [ ] Launch email blast: to existing list + waitlist — "it's live, here's your founding member access"
- [ ] Notify US East supporters

**Wave 3 — Midday (12-2 PM PT / 3-5 PM ET)**

- [ ] X/Twitter launch thread: 5-7 tweets, hook about the pain (not the product), build to CTA, pin the thread
- [ ] LinkedIn post: professional angle, storytelling, value insight (B2B)
- [ ] Cross-post updates: add comment to PH with live metrics, update IH with early reactions
- [ ] Notify US West supporters

**Wave 4 — Afternoon/Evening (3-6 PM PT / 6-9 PM ET)**

- [ ] Short-form video push: TikTok, IG Reels, YouTube Shorts — simultaneously
- [ ] Community engagement: Discord, Slack communities, Facebook groups (follow each community's rules)
- [ ] IG carousel / post: hook slide → problem → solution → CTA
- [ ] Dev.to / Hashnode article published (conditional: developer products)
- [ ] Activate ad campaigns (conditional: if budget allocated in Strategy)

**Throughout L-Day — Continuous:**

- [ ] Reply to EVERY comment within 15 minutes (drives algorithmic boost + converts visitors to advocates)
- [ ] Share live metrics: "just hit 100 signups" — creates FOMO and social proof
- [ ] Fix issues in real-time, announce fixes publicly: "Great catch by @user — fixed in 10 minutes"
- [ ] Capture testimonials: screenshot positive comments, DMs, reactions
- [ ] Route every interaction toward capture: every reply, every DM naturally points to the product
- [ ] Monitor infrastructure health throughout L-Day

### Phase 3: Post-Launch Momentum (L+1 to L+14)

*Traffic drops 60-75% by day 3. Normal. Capture the long tail and activate signups.*

**Content cadence:**

| Day | Content | Platform | Purpose |
|-----|---------|----------|---------|
| L+1 | Tutorial: "How to get [result] in 5 minutes" | All (adapted) | Drive activation |
| L+2 | Behind-the-scenes: launch day metrics + reactions | X, IH, LinkedIn | Build in public |
| L+3 | Early results: "What users say after 72 hours" | X, Reddit | Social proof |
| L+5 | Second community engagement round | Reddit, Discord | New angles, new subs |
| L+7 | "What I learned launching {{PRODUCT_NAME}}" | All (long-form) | SEO + reflection |
| L+10 | User spotlight / case study | All | Deep social proof |
| L+14 | "Two weeks in — here's the data" | X, IH, LinkedIn | Transparent update |

**Activation push (most critical window):**

- [ ] Onboarding email (immediate on signup): get to first value in <5 minutes, pre-filled examples, minimal steps
- [ ] Day 1 nudge: if signed up but not activated — "you're 1 click away from [result]"
- [ ] Day 3 check-in: personal-feeling "how's it going? hit reply if you need help"
- [ ] Day 7 internal report: what % of signups activated? If <50%, onboarding is broken — fix before more awareness spend
- [ ] Support tickets monitored: every ticket is a signal about what's broken in onboarding

**Platform follow-up:**

- [ ] Product Hunt: "first update" post after 7 days — what you built/fixed based on PH feedback
- [ ] Reddit: continue being helpful in pain threads (don't re-post product, let profile do the work)
- [ ] IndieHackers: Week 1 milestone update ("X signups, Y revenue, here's what I learned")
- [ ] Directories: check pending submissions, follow up, update listings with post-launch info
- [ ] HackerNews: if Show HN got traction, write a follow-up about what you learned (conditional)

**SEO compounding:**
- [ ] Competitor comparison articles and pain-keyword articles are live
- [ ] Directory backlinks are accumulating
- [ ] Monitor Google Search Console for which keywords are getting first impressions
- [ ] This is the start of the organic flywheel — it compounds over weeks and months

### Phase 4: Sustained Distribution (L+14 onwards)

- [ ] Ongoing content engine running: weekly content mapped to pain keywords from ICP
- [ ] Content repurposing loop: launch content → new formats (blog → carousel → thread → reel)
- [ ] Community participation ongoing (not a launch tactic — a growth habit)
- [ ] User stories and testimonials as a regular content type
- [ ] Growth loops active:
  - [ ] Referral program → new users (from Closing Agent post-purchase flow)
  - [ ] SEO content → organic traffic → signups (compounds monthly)
  - [ ] Community presence → organic mentions → signups
  - [ ] Email list → nurture → conversion → testimonial → content → list growth
- [ ] Re-launch criteria defined: what milestone triggers a mini-launch?
- [ ] Transition to Measure: once L+14 content is published and all systems running

---

## Stage 9: Measure

### 9.1 Metrics Tracking

**What gets tracked:**

| Category | Metrics |
|----------|---------|
| Traffic | Visitors, source breakdown, UTM performance per channel |
| Conversion | Signups, signup rate, signup rate by channel |
| Activation | Users reaching first value moment (product-specific) |
| Revenue | Total revenue, MRR, transactions, ARPU |
| Email | Open rates, click rates, unsubscribe rates per email in sequence |
| Social | Reach, engagement rate, link clicks per platform |
| Community | Engagement effectiveness, traffic driven |
| Retention | Return rate over time |
| For B2B: | Teams deployed, seats per team, team activation rate, expansion revenue |

- [ ] Phase 1 (first sprint post-launch): daily tracking — internal, not posted unless anomaly
- [ ] Phase 1 checkpoint: report with early read on what's working and what's not
- [ ] Phase 2 (subsequent sprints): weekly tracking, adjust based on Phase 1 learnings
- [ ] Phase 2 checkpoint: final report with recommendation

### 9.2 Funnel Diagnostics

- [ ] Identify biggest drop-off point in the funnel
- [ ] Low traffic → distribution problem → revisit Awareness
- [ ] High traffic, low signup → landing page / offer problem → revisit Lead Capture
- [ ] High signup, low activation → onboarding problem → revisit Closing
- [ ] High activation, low payment → pricing / value problem → revisit Closing + Strategy
- [ ] A/B test the biggest drop-off point first

### 9.3 Decision Framework

| Performance vs targets | Verdict | Action |
|----------------------|---------|--------|
| ≥80% | **DOUBLE DOWN** 🟢 | More content, paid ads, new features, new channels |
| 40-79% | **ITERATE** 🟡 | A/B test, fix funnel leaks, try different channels |
| 10-39% | **MAINTAIN** 🟠 | Keep alive with minimal effort, see if it compounds |
| <10% | **KILL** 🔴 | Archive, extract lessons, move on |

*For B2B products: 30-day window may be too short (enterprise sales cycles are 30-90 days). Adjust kill criteria based on product type and sales motion.*

- [ ] 🔒 **Max confirms final verdict: Double Down / Iterate / Maintain / Kill**

### 9.4 If Killed

- [ ] Stop all active activities (email sequences, ads, scheduled content)
- [ ] Archive all assets
- [ ] Extract lessons to MEMORY.md
- [ ] Close tracking and Linear ticket
- [ ] Document what conditions would make this worth revisiting

---

## Meta: Talent Tickets Queue

*All talent tickets from all agents are batched here. Batchable — "here are 4 videos to record, block 2 hours and knock them all out."*

- [ ] Talent tickets collected from all parallel agents
- [ ] Each ticket includes: format, script, storyboard, AI first-pass, estimated time
- [ ] Tickets batched by type (video recording, voiceover, review/approval)
- [ ] Max allocates time block to knock them out
- [ ] Recordings delivered back to agents for final production

---

## Meta: Agent Collaboration Interfaces

*Shared state between agents — what's been committed, what's been learned.*

| From | To | What | When |
|------|-----|------|------|
| Awareness | Lead Capture | Messaging resonating in communities | As engagement data comes in |
| Lead Capture | Awareness | Finalized offer stack | When offer is defined |
| Lead Capture | Nurture | Lead magnet context, ICP segment | When capture mechanism is defined |
| Nurture | Closing | Objection data from email replies, drop-off points | As sequence runs |
| Closing | Awareness | Testimonials and results for social proof | Post-purchase |
| Awareness | Nurture | Content pieces for email repurposing | As content is created |

- [ ] Shared context files updated by each agent as they complete their work
- [ ] ICP and VoC Bank loaded by every agent (no agent works without these)
- [ ] Ship Plan referenced by every agent (no agent contradicts the strategy)

---

## Meta: Ship Engine Management

### Approval Gates (2 mandatory)
1. **Post-Validation** (Stage 2): Ship / Explore / Kill
2. **Pre-Launch** (Stage 8): Launch / Fix Issues / Kill

### Parallel Execution (auto-starts after Strategy)
Stages 4-7 run concurrently:
- **Awareness** (Stage 4)
- **Lead Capture** (Stage 5)
- **Nurture** (Stage 6)
- **Closing** (Stage 7)

**Launch** waits for all 4 parallel stages.

### Template Variables

| Variable | Description |
|----------|-------------|
| `{{PRODUCT_NAME}}` | Product name |
| `{{PRODUCT_ONE_LINER}}` | One-line description |
| `{{TARGET_AUDIENCE}}` | Primary target customer |
| `{{LINEAR_TICKET}}` | Parent Linear ticket (e.g., MAX-XXX) |
| `{{DATE}}` | Checklist creation date |

---

*Template version: 2.0*
*Aligned with WORKFLOW.md v2 (8 stages: Intake → Validate → Strategy → Parallel → Launch → Measure)*
*Parallel stages: Awareness, Lead Capture, Nurture, Closing*
