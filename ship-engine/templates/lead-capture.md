# Lead Capture Setup: {name}

---

## Hormozi Offer Stack

> **Framework:** Alex Hormozi / acquisition.com value equation.
> The offer's perceived value = (Dream Outcome × Likelihood of Achievement) ÷ (Time Delay × Effort & Sacrifice)
> Maximize the numerator. Minimize the denominator. The offer should feel like stealing.

### Dream Outcome
*What is the ultimate result the ICP most wants? Not the feature — the life change.*

**Primary dream outcome:**
{What does success look like for the customer after using this product? Use their own words from the VoC bank. Be specific — not "save time" but "never manually export CSV files to build a report again."}

**Secondary outcomes:**
- {secondary_outcome_1 — what else becomes possible?}
- {secondary_outcome_2}
- {secondary_outcome_3}

**Dream outcome in a sentence (for copy):**
"{ICP} finally gets {specific result} without {pain they were suffering before}."

---

### Likelihood of Achievement
*What makes the customer believe this will work for them specifically? Remove all doubt.*

**Proof elements:**
| Proof type | Specifics | Where it appears |
|-----------|-----------|-----------------|
| Social proof | {X users, testimonials, logos} | Landing page, email sequence |
| Credibility | {Max's background, credentials, track record} | About section, email 1 |
| Case studies | {"{persona} got {result} in {time}"} | Blog, email Day 5 |
| Demo / trial | {Free tier, money-back guarantee, free trial} | CTA, pricing page |
| Statistics | {data from validation: "X% of {ICP} report {problem}"} | Hero section, PH description |

**Risk reversal (guarantee):**
- **Type:** {money-back / satisfaction / results-based / free trial}
- **Duration:** {N days / first month}
- **Terms:** {exactly what's covered and what's not — be honest}
- **Guarantee copy:** "{If you don't {specific result} in {N days}, {what we'll do}. No questions asked.}"

**Objection pre-emption:**
| Objection | Response | Placement |
|-----------|---------|-----------|
| "Will this work for my situation?" | {response using VoC language} | FAQ, email Day 7 |
| "Is it worth the price?" | {ROI framing — cost of problem vs cost of solution} | Pricing page |
| "Can I trust this?" | {credibility proof, guarantee} | Landing page, email Day 1 |

---

### Time Delay
*How quickly does the customer get the result? Compress perceived time-to-value.*

**Time to first value (onboarding):**
- From signup to first meaningful result: {N minutes / hours / days}
- Specific first action: {exactly what step gets them to aha moment}
- Onboarding copy: "You're 1 step away from {result}"

**Time to full outcome:**
- {When do they see the full dream outcome? Be realistic — don't overpromise}

**Speed elements in copy:**
- "{N}-minute setup"
- "Results in your first session"
- "Your first {output} in under 10 minutes"

**Delivery of lead magnet:**
- Delivery method: {immediate download / instant access / email within 60 seconds}
- Delivery speed copy: "Instant access. No waiting."

---

### Effort & Sacrifice
*How little does the customer have to do? Remove every possible friction.*

**Friction removed:**
| Old way | With {product_name} | Effort saved |
|---------|-------------------|-------------|
| {manual_step_1} | {automated/simplified} | {time/effort saved} |
| {manual_step_2} | {automated/simplified} | {time/effort saved} |
| {manual_step_3} | {automated/simplified} | {time/effort saved} |

**Effort-reduction copy:**
- "No {skill/tool/process} required"
- "Works with your existing {workflow/tool}"
- "Set it up once — it runs itself"
- "{Product} does {heavy task} so you don't have to"

**Signup friction:**
- Form fields: {email only / email + name / other}
- Steps to first result: {N steps max — aim for ≤3}
- Progressive disclosure: ask for more info after first value, never before

---

### Value Stack (assembled offer)

The full offer as presented to the prospect — everything they get when they sign up.

| Component | Value | What it is |
|-----------|-------|-----------|
| Core product | ${estimated_value}/mo | {what the product does} |
| Bonus 1 | ${estimated_value} | {e.g., "Quick-start template pack"} |
| Bonus 2 | ${estimated_value} | {e.g., "30-day onboarding email course"} |
| Bonus 3 | ${estimated_value} | {e.g., "Founding member community access"} |
| Guarantee | Priceless | {N}-day money-back, no questions |
| **Total value** | **${total_value}** | |
| **You pay today** | **${price}** | {X}% off total value |

**Value stack headline:** "Everything you need to {dream outcome} — for less than {relatable comparison}."

---

## Funnels
| Funnel | Flow | UTM | Status |
|--------|------|-----|--------|
| IG → Product | Reel → bio link → landing → signup | `?utm_source=ig&utm_medium=social&utm_campaign={name}` | ⬜ |
| X → Product | Thread → CTA → landing → signup | `?utm_source=twitter&utm_medium=social&utm_campaign={name}` | ⬜ |
| Reddit → Product | Reply → profile → landing → signup | `?utm_source=reddit&utm_medium=community&utm_campaign={name}` | ⬜ |
| SEO → Product | Article → CTA → landing → signup | `?utm_source=google&utm_medium=organic&utm_campaign={name}` | ⬜ |
| Email → Product | Cold/nurture → CTA → landing → signup | `?utm_source=email&utm_medium={type}&utm_campaign={name}` | ⬜ |

## Landing Page Conversion Elements
- [ ] Hero: problem statement (not feature list)
- [ ] Social proof above fold
- [ ] Demo video/GIF (pain → solution in 30 sec)
- [ ] Email capture form (MailerLite embedded)
- [ ] Lead magnet offer
- [ ] Objection-handling FAQ (from validation threads)
- [ ] Exit intent popup (different CTA than main)
- [ ] Mobile optimized
- [ ] Page speed < 3s

## Lead Magnet
- **Type:** {free tier / template / guide / waitlist / tool}
- **Title:** {what they get}
- **Delivery:** {immediate download / email / access grant}

## Email Capture
- **MailerLite group:** {name}
- **Form type:** {embedded / popup / landing page}
- **Form fields:** email (required), name (optional)
- **Confirmation:** {single opt-in for speed / double for quality}
- **Welcome email:** triggers nurture sequence

## Analytics Tracking
- [ ] GA4 installed with property ID
- [ ] Conversion event: `sign_up` configured
- [ ] Conversion event: `purchase` configured (if paid)
- [ ] UTM params on all inbound links
- [ ] Meta Pixel installed (if running ads)
- [ ] Funnel visualization in CC analytics

## Conversion Targets
| Funnel | Expected Traffic | Target Conv % | Target Signups |
|--------|-----------------|---------------|----------------|
| IG | {N}/week | {X}% | {N} |
| X | {N}/week | {X}% | {N} |
| Reddit | {N}/week | {X}% | {N} |
| SEO | {N}/week | {X}% | {N} |
| Cold | {N}/week | {X}% | {N} |
| **Total** | | | **{N}/week** |
