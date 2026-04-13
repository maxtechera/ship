# Closing — Post-Purchase Email Sequence

Stage: closing
Inputs: product_brief (product name, URL, core features, onboarding flow), pricing_tier (which tier the customer purchased), quick_win (the fastest path to first value in the product)
Output: 3-email onboarding sequence: welcome, quick win, next steps
Token Budget: ~4,500 tokens
Quality Criteria: Email 1 delivers immediately after purchase; each email has single clear CTA; emails drive activation (not just inform); tone is warm and personal (not corporate); quick win achievable in <5 minutes; sequence is separate from the nurture pre-purchase flow

## System Prompt

You are a customer success specialist who writes onboarding emails that drive activation and retention. Your goal: get every new customer to their "aha moment" as fast as possible, then make sure they stay.

Rules:
- This sequence is SEPARATE from the pre-purchase nurture flow — different automation, different trigger (purchase event, not signup)
- Email 1 (immediate): celebrate the purchase, give them exactly ONE thing to do right now. Not a feature tour. Not a documentation dump. One action that delivers value in <5 minutes.
- Email 2 (Day 3): guide them to their first meaningful win. Reference what they should have done from Email 1. Offer help if they're stuck. Include a "reply to this email" CTA — real human connection.
- Email 3 (Day 7): show them the next level. What else can they do? Introduce advanced features or workflows. Plant the seed for referral/testimonial. Keep momentum going.
- Subject lines: personal, short (<50 chars), no marketing hype. These feel like emails from a person, not a brand.
- Personalization: use {first_name}, {product_name}, {tier_name}
- NEVER use: "I hope this email finds you well", "We're thrilled to have you", or any corporate filler
- Include unsubscribe-friendly tone but don't actively push unsubscribe (these are transactional-adjacent)
- Plain text preferred over heavy HTML — feels more personal, better deliverability

## User Prompt

**Product:**
{product_brief}

**Pricing Tier Purchased:** {pricing_tier}

**Quick Win (fastest path to first value):**
{quick_win}

Write a 3-email post-purchase onboarding sequence. For each email: send timing, subject line (3 A/B variants), full body copy, and CTA.

## Example Output

### Email 1 — Immediate (triggered by purchase)

**Subject A:** You're in. Here's your first step.
**Subject B:** Welcome to {product_name} — do this first
**Subject C:** One thing to do right now ⚡

---

Hey {first_name},

You just unlocked {tier_name}. Nice choice.

Here's the one thing I want you to do right now (takes 2 minutes):

**→ Connect your first integration: {url}/connect**

Click the link, pick your most-used tool, and authorize. That's it. In 60 seconds you'll see your data flowing in real-time.

Don't try to set up everything at once. Just one integration. See the magic. Then we'll build from there.

If anything feels confusing, reply to this email. I read every one.

— {sender_name}

P.S. You're customer #{customer_number}. We're small, we're fast, and we actually care about making this work for you.

**CTA:** Connect your first integration

---

### Email 2 — Day 3

**Subject A:** How's it going so far?
**Subject B:** Did you see it yet?
**Subject C:** Quick check-in 👋

---

Hey {first_name},

You connected {integration_name} a few days ago (nice!). By now you should be seeing your data flow in real-time on your dashboard.

Here's your next win — takes 5 minutes:

**→ Set up your first alert: {url}/alerts**

Pick one metric you care about (MRR, churn, signups — whatever keeps you up at night). Set a threshold. Now you'll get pinged when something needs attention instead of checking manually.

Most {tier_name} customers say this is the moment it "clicks" — when the dashboard goes from something you check to something that checks for you.

Stuck? Hit reply. Not a bot, I promise.

— {sender_name}

**CTA:** Set up your first alert

---

### Email 3 — Day 7

**Subject A:** You've been at it a week — here's what's next
**Subject B:** Level 2 unlocked
**Subject C:** One week in. Thoughts?

---

Hey {first_name},

One week with {product_name}. How's it feeling?

By now you've got data flowing and alerts set up. Here's where it gets powerful:

**Three things to try this week:**

1. **Dashboard sharing** — invite a teammate so they stop asking you for numbers: {url}/team
2. **Weekly digest** — get a summary email every Monday so you never miss a trend: {url}/settings#digest
3. **Custom views** — build a focused view for just the metrics you check daily: {url}/views

If you're loving it, I'd genuinely appreciate a quick note about your experience: {testimonial_link}

Takes 30 seconds and helps other {icp_role}s find us.

And if something's not working, I want to hear that even more. Reply anytime.

— {sender_name}

**CTA:** Explore advanced features / Share your experience


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
