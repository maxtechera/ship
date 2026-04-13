# Nurture — Content Drip

Stage: nurture
Inputs: icp (audience profile, pain points, content preferences, platforms), ship_plan (channel priorities, content themes), awareness_content_bank (blog posts, social content, video scripts already produced by Awareness Agent), positioning (one-liner, value prop, VoC language), nurture_email_sequence (the 14-day email sequence from nurture-email-sequence template)
Output: 14-day post-launch content drip schedule — ready-to-publish posts per platform per day, `content-drip/schedule.csv`, hero images brief for each post, managed via `tools/content-engine.py`
Token Budget: ~5,000 tokens
Quality Criteria: Every day D0-D14 has at least one scheduled post; each post is platform-native (different copy for IG, X, Reddit, LinkedIn); copy adapts Awareness Agent content rather than repeating it verbatim; all copy humanized; schedule.csv is complete with day/platform/copy/image_path/status columns; posts coordinate with email sequence timing (email and social reinforce each other on key days)

## System Prompt

You are a content strategist who sequences post-launch content to maintain momentum after the launch spike fades. You know that traffic drops 60-75% by day 3 and that sustained growth comes from a consistent presence, not another launch blast.

Rules:
- Content must be VARIED — no two consecutive days post the same angle on the same platform
- Posts adapt from Awareness Agent's content bank — repurpose, don't repeat. Same insight, different format.
- Platform-native means: IG gets carousel structure or storytelling caption, X gets thread structure, Reddit gets community-first value post, LinkedIn gets narrative long-form
- Content and email coordinate: on days when the nurture email is about social proof, social posts should also be social proof. Reinforce the narrative.
- All copy runs through the `humanize` skill with `channel={platform}` before output — no AI-sounding cadence
- Hero images are a brief (description + suggested b-roll asset by manifest ID), not the actual image — `content-image` skill generates the images
- Volume scales down: D0-D3 high intensity (1-2 posts/day), D4-D7 medium (1 post/day), D8-D14 cadence posts (every other day)
- Include at least 2 "build in public" posts sharing real metrics (signups, reactions, early results)
- Include at least 1 community engagement post per platform (answer a pain thread, don't just broadcast)
- Schedule via `tools/content-engine.py add` — each post gets a content-engine entry

## User Prompt

**ICP (audience, content preferences):**
{icp}

**Ship Plan (channels, content themes):**
{ship_plan}

**Awareness Content Bank (already produced):**
{awareness_content_bank}

**Positioning:**
{positioning}

**Nurture Email Sequence (for coordination):**
{nurture_email_sequence}

**Launch Date:** {launch_date}

Produce the complete 14-day content drip:

1. **Schedule Overview** — Day-by-day narrative of the content arc
2. **Post-by-Post Content** — Full copy for each post, per platform, per day
3. **schedule.csv** — Complete CSV ready for content-engine.py
4. **Hero Image Briefs** — Description + b-roll ID per post that needs an image
5. **Email-Social Coordination Map** — Which days email and social reinforce each other
6. **Community Engagement Slots** — Pre-identified threads/conversations to engage in

## Schedule Overview

| Phase | Days | Goal | Tone |
|-------|------|------|------|
| Launch burst | D0-D2 | Maximize initial visibility, capture announcement wave | Excited, genuine |
| Early social proof | D3-D5 | Show that people are using it and loving it | Testimonial, transparent |
| Tutorial & activation | D5-D8 | Drive non-activated signups to first value | Helpful, educational |
| Community depth | D8-D11 | Build presence in communities beyond the launch post | Contributing, not promoting |
| Momentum & closing | D11-D14 | Convert warm leads to paying; use urgency when real | Confident, direct |

## Example Output (selected days)

---

### Day 0 — Launch Day

**Email coordination:** Day 0 welcome email (deliver lead magnet, set expectations)

**IG Post (Launch Announcement):**
```
[EN]
Caption:
It's live. 🚀

For the past 6 months, I've been building the tool I always wanted as a solo founder.

The problem: every Monday I was copying numbers between 4 different tools. 3+ hours. Every. Single. Week.

{product_name} fixes that. 2-click setup, real-time sync, and your dashboard just... works.

Early access is open right now — link in bio. First 50 people get founding member pricing.

What tool do you most wish would just sync automatically? Drop it below 👇

[ES]
Caption:
Está live. 🚀

...
[Complete ES version with adapted VoC language]
```
**Hashtags:** #solopreneur #bootstrapped #buildinpublic #saas #productlaunch #founders #nocode
**Image brief:** B-roll broll-01 (dashboard desktop) + excitement overlay text "IT'S LIVE" — 1080×1080 branded
**content-engine entry:** `add --day 0 --platform instagram --copy "..." --image pending`

---

**X/Twitter Thread (Launch Day):**
```
[EN]
Tweet 1: I just launched {product_name}. Here's what 6 months of building solo looked like. 🧵

Tweet 2: The problem: Every Monday I lost 3+ hours copying data between dashboards. 4 tools. 4 exports. 1 massive spreadsheet. Repeat.

Tweet 3: I tried Zapier (too many zaps for my workflow), custom scripts (broke every 2 weeks), BI tools (overkill and expensive). None of it worked cleanly.

Tweet 4: So I built what I actually needed: connect your tools in 2 clicks → real-time dashboard → never manually update anything again.

Tweet 5: Today it's live. Free tier available. Founding member pricing for the first 50 (40% off for life).

Tweet 6: Link: {product_url}?utm_source=twitter&utm_medium=thread&utm_campaign=launch&utm_content=thread-launch-day

I'm replying to every comment for the first 48h. What do you sync manually right now? 👇
[ES version follows]
```
**content-engine entry:** `add --day 0 --platform twitter --copy "..." --image none`

---

### Day 2 — Early Social Proof

**Email coordination:** No email on Day 2. Give space between Day 0 welcome and Day 3 tutorial.

**X/Twitter (Metrics post):**
```
[EN]
48 hours since launch.

Here's the data:
→ 312 visitors
→ 67 signups (21.5% conversion)
→ 8 paying customers
→ One email: "This is exactly what I needed, where has this been?"

The Reddit post in r/entrepreneur drove 2x more signups than Product Hunt.

Building in public because I think you deserve to know what actually works.

Still interested? {product_url}?utm_source=twitter&utm_medium=organic&utm_campaign=launch&utm_content=48h-metrics

[ES version follows]
```
**content-engine entry:** `add --day 2 --platform twitter --copy "..." --image none`

**LinkedIn (Narrative post):**
```
[EN]
What happens when you solve your own problem and launch it publicly?

48 hours ago, I shipped {product_name}. Here's what surprised me...

[800-word LinkedIn narrative — 5 paragraphs: problem → build → launch → early results → what's next]

What would you ship if you just... started? 👇
[ES version follows]
```

---

### Day 5 — Tutorial / Activation Push

**Email coordination:** Day 3 tutorial email just went out. Reinforce with a visual tutorial on social.

**IG Carousel (Tutorial):**
```
[EN]
Slide 1: How to get your first automated dashboard in under 5 minutes 👇 (swipe)
Slide 2: Step 1 — Connect your first tool (screenshot: broll-02)
Slide 3: Step 2 — Pick the metrics you care about (screenshot: broll-03)
Slide 4: Step 3 — Name your dashboard
Slide 5: That's it. It's syncing. Your Monday just got free.
Slide 6: CTA — Try it free: {product_url} (link in bio)
Caption: The #1 question from new users: "Wait, is it really this simple?" Yes. 5 minutes to a dashboard that actually stays updated. 🎯
[ES version follows]
```
**Image brief:** Tutorial carousel — each slide uses broll-02/03/04 (onboarding screens) + minimal text overlay
**content-engine entry:** `add --day 5 --platform instagram --type carousel --copy "..." --image pending`

---

## schedule.csv

```csv
day,platform,type,copy_en,copy_es,image_path,image_brief,status,utm_params,email_coordination
0,instagram,post,"[Day 0 IG caption EN]","[Day 0 IG caption ES]",tbd,"broll-01 + launch overlay 1080x1080",draft,utm_source=instagram&utm_medium=post&utm_campaign=launch&utm_content=launch-day,welcome-email
0,twitter,thread,"[Day 0 thread full EN]","[Day 0 thread full ES]",none,none,draft,utm_source=twitter&utm_medium=thread&utm_campaign=launch&utm_content=thread-launch,welcome-email
0,reddit,post,"[Day 0 Reddit r/entrepreneur post EN]","[ES version]",none,none,draft,utm_source=reddit&utm_medium=post&utm_campaign=launch&utm_content=entrepreneur-launch,none
1,instagram,story,"[Day 1 IG Story — 24h update EN]","[ES]",tbd,"metrics card 1080x1920",draft,utm_source=instagram&utm_medium=story&utm_campaign=launch&utm_content=day1-story,none
2,twitter,post,"[48h metrics post EN]","[ES]",none,none,draft,utm_source=twitter&utm_medium=organic&utm_campaign=launch&utm_content=48h-metrics,none
2,linkedin,post,"[Day 2 LinkedIn narrative EN]","[ES]",none,none,draft,utm_source=linkedin&utm_medium=post&utm_campaign=launch&utm_content=linkedin-narrative,none
3,instagram,carousel,"[Tutorial carousel EN]","[ES]",tbd,"tutorial carousel broll-02/03/04",draft,utm_source=instagram&utm_medium=carousel&utm_campaign=nurture&utm_content=tutorial,tutorial-email
5,twitter,thread,"[Tutorial thread EN]","[ES]",none,none,draft,utm_source=twitter&utm_medium=thread&utm_campaign=nurture&utm_content=tutorial-thread,tutorial-email
7,reddit,post,"[Day 7 — community pain thread reply/post EN]","[ES]",none,none,draft,utm_source=reddit&utm_medium=organic&utm_campaign=nurture&utm_content=community-engage,objection-email
10,instagram,post,"[User spotlight / testimonial EN]","[ES]",tbd,"testimonial card 1080x1080",draft,utm_source=instagram&utm_medium=post&utm_campaign=nurture&utm_content=social-proof,urgency-email
14,twitter,post,"[Two weeks update — data + lessons EN]","[ES]",none,none,draft,utm_source=twitter&utm_medium=organic&utm_campaign=nurture&utm_content=2week-report,lastcall-email
```

## Email-Social Coordination Map

| Day | Email | Social Theme | Coordination |
|-----|-------|-------------|-------------|
| D0 | Welcome — deliver lead magnet | Launch announcement | Announce everywhere same day |
| D3 | Tutorial — get to first value | Tutorial carousel (IG) | Social shows the visual tutorial email describes |
| D5 | Social proof — what others are experiencing | Testimonial post | Mirror the proof — social proof in both channels |
| D7 | Objection killer | Community engagement post (Reddit) | Reddit post addresses the #1 objection directly |
| D10 | Urgency — early bird ending | User spotlight | Social proof reinforces email urgency |
| D14 | Last call | 2-week data report | Transparency on both channels — "this is real" |

## Community Engagement Slots

| Day | Platform | Thread/Sub | Engagement Strategy |
|-----|----------|-----------|---------------------|
| D1 | Reddit | r/entrepreneur — any "how do you track metrics?" thread from last 48h | Helpful reply, mention product at end naturally |
| D4 | Reddit | r/saas — pain thread about manual workflows | Answer the pain comprehensively, no product mention in first comment |
| D7 | IndieHackers | "Ask IH" — post "What did your first paying customers teach you?" | Build-in-public engagement, not product promotion |
| D10 | Reddit | r/entrepreneur — "What did you launch last week?" thread | Share 2-week update with transparent metrics |

---
**Bilingual Output (MANDATORY per Decision #9):** All copy above must be generated in full for both EN and ES. Use VoC language adapted authentically for Latin American Spanish-speaking solopreneurs — do NOT machine-translate. Label each copy block: `[EN]` and `[ES]`.
