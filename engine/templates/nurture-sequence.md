# Nurture Sequence: {name}

> **Related templates (required before sequence setup):**
> - `skills/engine/templates/segment-definitions.md` — subscriber segments + engagement scoring
> - `skills/engine/templates/behavioral-triggers.md` — trigger map + drip automation wiring

## Email Automation

> **7-email sequence over 14 days.** This is the canonical count per WORKFLOW.md Stage 5C.
> Do not reduce below 7. Do not skip emails. Each email has a distinct conversion job.
> All 7 emails must be imported as live automation before Pre-Launch approval is requested.

**MailerLite automation:** {name} Nurture
**Trigger:** Subscriber joins group "{name}" (wired by Lead Capture Agent)
**Duration:** 14 days
**Goal:** Move subscriber from "interested" → "ready to buy"
**Emails:** 7 (Day 0, 1, 3, 5, 7, 10, 14)

### 7-Email Sequence
| # | Day | Email | Subject | Purpose | CTA |
|---|-----|-------|---------|---------|-----|
| 1 | 0 | Welcome | "{lead magnet title}" | Deliver value, set expectations | Use the tool |
| 2 | 1 | Story | "Why I built {name}" | Emotional connection, trust | Read more |
| 3 | 3 | Tutorial | "Get 10x more from {name}" | Drive activation, show value | Try this feature |
| 4 | 5 | Case study | "{User} saved {X} hours with {name}" | Social proof | Start now |
| 5 | 7 | Objection | "But what about {top doubt}?" | Handle #1 blocker | See pricing |
| 6 | 10 | Urgency | "Early bird ends {date}" | FOMO, drive decision | Buy now |
| 7 | 14 | Last call | "Still thinking about {name}?" | Final push, list hygiene | Buy or unsubscribe |

**Automation import checklist (all 7 required before launch):**
- [ ] Email 1 (Day 0 — Welcome) imported and trigger configured
- [ ] Email 2 (Day 1 — Story) imported with 1-day delay
- [ ] Email 3 (Day 3 — Tutorial) imported with 2-day delay from email 2
- [ ] Email 4 (Day 5 — Case Study) imported with 2-day delay from email 3
- [ ] Email 5 (Day 7 — Objection Killer) imported with 2-day delay from email 4
- [ ] Email 6 (Day 10 — Urgency) imported with 3-day delay from email 5
- [ ] Email 7 (Day 14 — Last Call) imported with 4-day delay from email 6
- [ ] Test email sent to seed address — delivery, rendering, links, and unsubscribe footer verified
- [ ] Automation is LIVE (not paused) in MailerLite before Pre-Launch approval

### Email 0: Welcome
**Subject:** {subject}
**Preview:** {preview text}
**Body outline:**
- Thanks for signing up
- Here's what you got: {lead magnet}
- Here's what to do first: {first action}
- What to expect from these emails

### Email 1: Story
**Subject:** {subject}
**Body outline:**
- The pain that started this
- Failed solutions I tried
- The moment I decided to build it
- What it does now
- CTA: see it in action

### Email 3: Tutorial
**Subject:** {subject}
**Body outline:**
- Most people only use {basic feature}
- Here's the power move: {advanced usage}
- Step-by-step walkthrough
- Result: {what they'll achieve}

### Email 5: Case Study
**Subject:** {subject}
**Body outline:**
- Meet {user/persona}
- Their problem: {specific pain}
- How they use {name}: {workflow}
- Result: {metric improvement}
- CTA: get the same result

### Email 7: Objection Killer
**Subject:** {subject}
**Body outline:**
- I know what you're thinking: "{objection}"
- Here's the truth: {reframe}
- Data/proof: {evidence}
- CTA: try risk-free (guarantee)

### Email 10: Urgency
**Subject:** {subject}
**Body outline:**
- Early bird pricing expires {date}
- {X} people already signed up
- After {date}: price goes to ${Y}
- CTA: lock in your price now

### Email 14: Last Call
**Subject:** {subject}
**Body outline:**
- Quick check: still interested?
- If yes: {final CTA with sweetener}
- If no: no hard feelings, unsubscribe link
- PS: {one more reason}

## Content Drip (Social)
| Content | Platform | Timing | Purpose |
|---------|----------|--------|---------|
| Building journey | IG Story | During build | FOMO + authenticity |
| Value drops | X | 2-3x/week | Authority |
| Community participation | Reddit/forums | Ongoing | Become known expert |
| User wins | IG + X | Post-launch | Social proof |

## Retargeting (if budget)
| Audience | Platform | Creative |
|----------|----------|----------|
| LP visitors, no signup | IG/FB | Pain reminder → signup CTA |
| Signed up, not activated | Email | "Complete your setup" |
| Activated, not paid | Email + IG/FB | Feature unlock → upgrade CTA |

## Metrics
- Email 0 open rate: target >60%
- Sequence completion rate: target >30%
- Click rate per email: target >5%
- Conversion (signup → paid): target >{X}%
- Unsubscribe rate: acceptable <3%
