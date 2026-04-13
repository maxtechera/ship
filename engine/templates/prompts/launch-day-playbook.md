# Launch — Day Playbook

Stage: launch
Inputs: pre_launch_checklist (all items PASS, readiness verdict READY), ship_plan (channel priorities, wave timing, supporter list), all_launch_content (content packs from awareness agent — per-platform, ready to publish), supporter_list (warm contacts segmented by timezone from launch-supporter-rally)
Output: L-Day execution playbook with wave timing, platform-by-platform action sequence, monitoring protocol, and real-time response SLA
Token Budget: ~4,500 tokens
Quality Criteria: Wave timing is specific (e.g., "12:01 AM PT" not "early morning"); each wave lists specific platforms and specific actions (not "post on social"); monitoring checkpoints are time-boxed; response SLA is defined and actionable; playbook is written to be executed by a non-technical person; includes diagnostic guide for common L-Day failures

## System Prompt

You are a launch strategist who writes L-Day playbooks for solo founders. You know that launch day is high-stakes, fast-moving, and filled with small decisions that compound into big outcomes. Your playbook eliminates guesswork — every hour has a task list, every platform has an action, every problem has a pre-defined response.

Rules:
- Timing is specific: wave times match the Ship Plan's timezone wave strategy. Default to Tuesday-Thursday launch for max engagement.
- Product Hunt is the anchor event if in the plan — all other waves are timed around PH rhythm (submit 12:01 AM PT, peak engagement 8-12 PM PT)
- Every platform action is specific: not "post on Reddit" but "post {specific post title} in r/entrepreneur using {specific copy file}"
- Response SLA is non-negotiable: <15 minutes on all platforms during waves. Include a 15-minute timer protocol.
- Monitoring checkpoints are scheduled: check metrics at +1h, +3h, +6h, +12h, +24h
- Include a "things will go wrong" section with pre-defined responses for common failure modes
- Supporter list is activated via personal outreach (not broadcast) — 3 messages max per wave
- L-Day ends at midnight. Post-day debrief scheduled for the morning after.

## User Prompt

**Product Name:** {product_name}
**Product URL:** {product_url}
**Launch Date:** {launch_date}
**Launch Time Zone:** {timezone} (target: Tuesday-Thursday)

**Ship Plan (channels, wave timing):**
{ship_plan}

**All Launch Content (per platform, ready to publish):**
{all_launch_content}

**Supporter List (segmented by timezone):**
{supporter_list}

**Channels in Plan:** {channels}
**Product Hunt in Plan:** {ph_in_plan} (yes/no)

Generate the complete L-Day playbook:

1. **L-Day Overview** — Timeline at a glance
2. **Pre-Launch (T-60min)** — Final checks before going live
3. **Wave 1 — Seed** — Launch + warm audience activation
4. **Wave 2 — Amplify** — Broader community and email blast
5. **Wave 3 — Peak** — Max visibility, social threads, momentum signals
6. **Wave 4 — Sustain** — Video, communities, retargeting activation (if applicable)
7. **All-Day Protocol** — Continuous monitoring and engagement
8. **Metrics Checkpoints** — What to measure, when
9. **Failure Mode Guide** — Pre-defined responses to common problems
10. **End of Day** — Wrap-up and handoff to Day 2

---

## L-Day Overview

| Time (PT) | Phase | Key Action |
|-----------|-------|-----------|
| T-60 min | Pre-launch | Final check — all systems go |
| 12:01 AM | Wave 1 — Seed | Submit Product Hunt. Notify APAC/EU supporters. |
| 8:00 AM | Wave 2 — Amplify | Reddit posts live. Email blast sent. US/EU supporters notified. |
| 12:00 PM | Wave 3 — Peak | Social threads live. Share live metrics. Maker comment update. |
| 4:00 PM | Wave 4 — Sustain | Video published. Community posts. Retargeting activated (if budget). |
| 11:59 PM | End of Day | Metrics snapshot. Write tomorrow's build-in-public post. |

---

## Pre-Launch (T-60 minutes)

Final go/no-go checks before executing any public action:

```
[ ] Product URL responds: {product_url} → 200 OK
[ ] Landing page loads: {landing_page_url}
[ ] Email capture form works (submit test → subscriber appears)
[ ] Stripe checkout works (test a $0 or $1 transaction if needed)
[ ] GA4 DebugView active (open in another tab to monitor events)
[ ] All platform content files are open and copy-ready
[ ] Supporter message is drafted (personal, genuine — NOT "please upvote")
[ ] Phone and browser notifications for all platforms are ON
[ ] Reply protocol confirmed: <15 min for first 48h. Set a phone timer for monitoring.
[ ] Optional: post a "going live in 1 hour" teaser story on IG
```

If any check fails: fix it or escalate. Do not launch with a broken checkout or non-functional email capture.

---

## Wave 1 — Seed (12:01 AM PT)

**Goal:** Launch publicly, activate warm audience, start the engagement clock.

### Product Hunt (if in plan)

1. **Submit Product Hunt listing** at exactly 12:01 AM PT
   - Use pre-drafted listing: `launch/ph-submission.md`
   - Tagline: {ph_tagline} (under 40 chars)
   - Upload pre-prepared screenshots (broll-01 through broll-05)
   - Publish maker comment (pre-drafted in ph-submission.md)
   - ⏱️ Set 30-min reminder to check first comments and reply

2. **Share PH link** to APAC/EU supporters:
   - Message format: "Hey [name], we just launched {product_name} on Product Hunt — would love to know what you think: {ph_link}. Any feedback welcome!"
   - DO NOT ask for upvotes. Share the link. Let them engage naturally.
   - Max: {supporter_apac_eu_count} messages. Send within 15 minutes of submission.

### IndieHackers Submission

3. **Post "Shipped" update** to IndieHackers:
   - Use pre-drafted post: `launch/ih-shipped.md`
   - Honest format: metrics from validation, what you built, what you learned, link
   - Target URL: https://www.indiehackers.com/product/{product_slug}/launches

---

## Wave 2 — Amplify (8:00 AM PT)

**Goal:** Reach the US audience at the start of their workday, send launch email.

### Reddit

4. **Post in r/entrepreneur:**
   - Copy: `awareness/social/reddit-posts/entrepreneur-launch.md`
   - Title: "{reddit_title_entrepreneur}"
   - Format: value-first story, product revealed at end. No self-promo opener.
   - ⏱️ Set 15-min timer to check comments and reply to the first one

5. **Post in r/saas (staggered 30 min after entrepreneur):**
   - Copy: `awareness/social/reddit-posts/saas-launch.md`
   - Different title and angle from r/entrepreneur post
   - ⏱️ Monitor both threads simultaneously

6. **Post in r/indiehackers:**
   - Copy: `awareness/social/reddit-posts/indiehackers-launch.md`

### Email Blast

7. **Send launch email to full list:**
   - Subject: {email_blast_subject}
   - Copy: `launch/email-blast.md`
   - Send via email provider — schedule for 8:30 AM PT (after Reddit posts are live, momentum building)
   - Include live metrics if any are available: "Already X signups in the first 8 hours"

### US/EU Supporter Notification

8. **Notify US/EU supporters:**
   - Message format: same template as Wave 1 (personalized, not broadcast)
   - Include PH link (still gaining votes) + product URL
   - Max: {supporter_us_eu_count} messages. Aim to send within 30 minutes.

---

## Wave 3 — Peak (12:00 PM PT)

**Goal:** Maximum visibility. Long-form content. Share live metrics for social proof.

### X/Twitter

9. **Publish launch thread:**
   - Copy: `awareness/social/twitter-threads/launch-thread.md`
   - 6-7 tweets. Hook is the PROBLEM (no product in tweet 1).
   - Schedule to go out at 12:00 PM PT exactly
   - ⏱️ Reply to every reply within 15 minutes for the first 2 hours

### LinkedIn

10. **Publish LinkedIn narrative post:**
    - Copy: `awareness/social/linkedin-posts/launch-narrative.md`
    - 800-1200 words. Opens with pattern interrupt. Story arc.
    - Post at 12:30 PM PT (30 min after X)

### Product Hunt — Share Live Metrics

11. **Update maker comment with live metrics:**
    - Pull numbers from GA4 or email provider
    - Add to maker comment: "Update at {X}h: {Y signups}, {Z} from {channel} — here's what we're seeing in real-time…"
    - This drives PH engagement loop: updates attract new visitors

### Momentum Signal

12. **Share live metrics on IG Story:**
    - Use pre-made metrics card template
    - Update number: "X signups in the first Y hours"
    - Add link sticker to landing page
    - CTA: "Link in bio — still taking early access"

---

## Wave 4 — Sustain (4:00 PM PT)

**Goal:** Capture the late-day audience, push video content, activate remaining channels.

### Short-Form Video

13. **Publish launch video on all short-form platforms simultaneously:**
    - File: `awareness/video/launch-short-form-{final-version}.mp4`
    - IG Reels: publish + add to feed with caption from `awareness/social/ig-caption-launch-reel.md`
    - TikTok (if in plan): same video, adapted caption
    - YouTube Shorts (if in plan): same video, title + description

### Community Posts

14. **Post in Discord/Slack/Facebook communities (if in channel plan):**
    - Check each community's self-promo rules first
    - Value-first format: "I've been solving [problem] for 6 months and today I shipped something — here's what I learned: {link}"
    - Stagger posts 20-30 min apart

### Final Supporter Wave

15. **Notify final timezone segment:**
    - Send to remaining supporters not yet contacted
    - Include latest metrics: "We've had {X} signups so far today"

### Retargeting Activation (if ad budget approved)

16. **Activate Meta retargeting audiences:**
    - Turn ON Campaign: "Retargeting — Non-Signups"
    - Starting budget: ${daily_retargeting_budget}/day
    - Monitor CPL at the 6h mark — pause if CPL > $15 from day 1

---

## All-Day Protocol

**Response SLA (non-negotiable):**
- 0-48h after launch: reply to every comment within **15 minutes**
- 48-72h: reply within **2 hours**
- 72h+: reply within **24 hours**

**15-minute monitoring protocol:**
```
Every 15 minutes during Waves 1-3:
  1. Check all platform notifications (PH comments, Reddit replies, X mentions, IG DMs)
  2. Reply to any new comments
  3. Screenshot any especially positive reactions (social proof capture)
  4. Note any feature requests or bugs in a running list
```

**Bug response protocol:**
```
If a user reports a bug:
  1. Fix immediately (if < 30 min fix time)
  2. Reply publicly: "Great catch! Fixed in {X} minutes — try again?"
  3. Update status page or add note to landing page FAQ if it was widespread
```

**Testimonial capture protocol:**
```
When a user says something positive in comments/DMs:
  1. Screenshot immediately
  2. Save to: data/content-assets/{run_slug}/testimonials/
  3. If Twitter/X: note handle for potential social proof card
  4. If email reply: save to testimonials directory
```

---

## Metrics Checkpoints

Pull data via `tools/analytics-collector.py` at each checkpoint:

| Checkpoint | When | What to Check | Action if Off-Track |
|-----------|------|---------------|---------------------|
| 1h check | 1h post-launch | Visitors, PH position (if applicable), first signups | If 0 signups: check if form is actually working |
| 3h check | 3h post-launch | Signup rate from landing page (target: 15%+), top channel | If < 10% conversion: check landing page OG image (is it showing?) |
| 6h check | 6h post-launch | Total signups, channel breakdown, email open rate | If email open rate < 20%: subject line may need A/B |
| 12h check | 12h post-launch | Revenue (any paying customers?), activation rate | If 0 revenue: founding offer may not be compelling enough |
| 24h check | 24h post-launch | Full day metrics vs targets. Post metrics publicly. | Run full analysis — see Failure Mode Guide |

**Share 24h metrics publicly** (X, IndieHackers, IG Story):
```
"24 hours since launch:
→ {X} visitors
→ {Y} signups ({Z}% conversion)
→ {W} paying customers
→ Best channel: {channel} at {rate}% conversion

Lessons learned 🧵..."
```

---

## Failure Mode Guide

| Problem | Diagnosis | Response |
|---------|----------|---------|
| High traffic, < 5% signup conversion | Landing page / offer issue | A/B test hero headline immediately. Change to most direct pain-first copy. Check if form is visible on mobile. |
| Low traffic (< 100 visitors after 6h) | Distribution issue | Check if Reddit posts are visible (not shadow-banned). Manually share link in 2 more relevant communities. Send email blast if not done. |
| Email not arriving after signup | Email delivery issue | Check spam folder. Check email provider automation is triggered. Check domain DNS (SPF/DKIM). |
| Stripe checkout error | Payment issue | Check Stripe dashboard for error. Common: price ID mismatch. Fix and test before more users arrive. |
| Product crashing for new users | Critical bug | Triage immediately. Post honest update: "We're seeing an issue — fixing now. Back in {X} min." Fix, then announce it's resolved. |
| Reddit post removed | Subreddit rules | Don't repost the same content. Engage in the comments of existing pain threads instead. Move Reddit spend to X/IH. |
| PH position declining | PH algorithm | Don't panic. Share PH link in your next community post. Post a mid-day metrics update in maker comment. |
| 0 paying customers by end of day | Conversion issue | Check if checkout is working. Review pricing page — is the CTA visible? Is the founding offer compelling? Send direct email to top-engaged signups. |

---

## End of Day (11:59 PM PT)

1. **Pull full-day metrics:**
   - `tools/analytics-collector.py --range today`
   - Screenshot GA4 summary, Stripe dashboard, email provider signup count

2. **Save testimonials and social proof captures** to Drive

3. **Write D+1 "build in public" post draft:**
   - What happened today (real numbers)
   - What surprised you
   - What you're fixing tomorrow
   - This goes live tomorrow morning — honest, transparent, builds trust

4. **Update pre-launch checklist** with actual L-Day results

5. **Set Day 2 alarm** (content drip schedule begins — see nurture-content-drip.md)

6. **Post final PH comment** (if in top 10): "What a day — thanks everyone for the support. Here's what we saw…"

---

### Blackboard Keys
- `launch.playbook`: link to this document
- `launch.launch_date`: {launch_date}
- `launch.wave_log`: time-stamped log of each wave execution (filled during L-Day)
- `launch.24h_metrics`: link to metrics snapshot from 24h checkpoint


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
