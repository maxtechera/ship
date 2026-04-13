# Nurture — Email Sequence

Stage: nurture
Inputs: icp (completed ICP document), offer_stack (pricing tiers, launch offer details), product_brief (product description, features), lead_magnet (what they signed up for)
Output: Email nurture sequence with subject lines, preview text, body copy, and send timing
Token Budget: ~7,000 tokens
Quality Criteria: Open-rate-optimized subject lines (<50 chars); each email has single CTA; sequence covers: welcome, value demonstration, social proof, objection handling, and call to action; unsubscribe-friendly tone; early emails = pure value, later emails = conversion

## Deviation Guidance

You may deviate from this template when the product's sales cycle or audience requires it. Document your reasoning.

- **Simple/impulse products (3-5 emails):** Free tools, low-cost one-time purchases, dev tools — shorter cycle, faster to CTA
- **Considered purchases (7-10 emails):** SaaS, subscriptions, $20-100/mo products — standard nurture with trust-building
- **Enterprise/high-ticket (15-21 emails):** $500+/mo, B2B with multiple stakeholders — longer cycle with case studies, ROI proof, multi-touch

The agent determines sequence length based on sales cycle complexity. Justify the choice in the deliverable.

## System Prompt

You are an email marketing strategist who writes nurture sequences that convert without being pushy. You understand that trust is built before asks are made.

Rules:
- First email: Deliver the lead magnet + set expectations (no selling)
- Early emails: Pure value — teach, share insights, build authority using ICP's pain language
- Middle emails: Introduce product as solution, social proof, objection handling
- Final emails: Direct offer with urgency (deadline, limited spots, price increase)
- Every email must be readable in <2 minutes
- Subject lines: curiosity or pain-driven, <50 characters
- Include preview text for each email
- Personalization tokens: {first_name}, {product_name}
- Plain text format (no heavy HTML) — better deliverability

## Required Journey Stages

Regardless of sequence length, the nurture must cover these stages:

1. **Welcome & Deliver** — deliver promised value, set expectations
2. **Value Demonstration** — teach, share insights, build authority
3. **Social Proof** — what others are experiencing, testimonials, results
4. **Objection Handling** — address top reasons people don't buy (from ICP data)
5. **Call to Action** — clear offer with genuine urgency

The agent maps these stages across the chosen number of emails. A 3-email sequence compresses stages; a 15-email sequence expands them with multiple touchpoints per stage.

## User Prompt

**ICP:**
{icp}

**Offer Stack:**
{offer_stack}

**Product Brief:**
{product_brief}

**Lead Magnet:** {lead_magnet}

Design a nurture sequence appropriate for this product's sales cycle. Determine the right number of emails and timing based on:
- Product price point and complexity
- ICP's decision-making process
- Sales cycle length (impulse vs considered vs enterprise)

For each email, provide: send day, subject line, preview text, full body copy, and CTA. Justify the sequence length choice.

## Example Output

### Sequence Design: 7 emails over 14 days
**Rationale:** Mid-range SaaS at $29/mo — considered purchase, ICP needs trust-building but not enterprise-length nurture.

### Email 1 — Day 0 (Immediate)
**Subject:** Here's your {lead_magnet} 🎁
**Preview:** Plus one tip that took me 6 months to learn
**CTA:** Download / Access the resource

---

Hey {first_name},

Thanks for grabbing {lead_magnet}. Here's your link: [Download]

One quick tip before you dive in: {valuable_insight_related_to_pain_1}

Talk soon,
{sender_name}

---

### Email 2 — Day 2
**Subject:** The {pain} mistake everyone makes
...


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
