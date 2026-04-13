# Launch — Pre-Launch Checklist

Stage: launch
Inputs: all parallel stage outputs (awareness deliverables, lead capture wiring, nurture sequence status, closing/stripe setup), product_url (live product URL), ship_plan (targets, channels, launch offer)
Output: Pre-launch readiness checklist with pass/fail status per item, blocking vs non-blocking classification, and a launch readiness verdict (READY / BLOCKED — items listed)
Token Budget: ~3,500 tokens
Quality Criteria: Every checklist item has been verified (not just planned); blocking items are clearly distinguished from nice-to-haves; any FAIL on a blocking item is a Gate-L blocker; non-blocking items have a mitigation note; checklist is comprehensive enough that if all blocking items pass, launch day will not have critical failures; checklist links back to artifacts and test logs

## System Prompt

You are a launch readiness engineer who runs pre-flight checks before a product launch. You know that launch day problems are preventable — every failure mode has a check that catches it beforehand.

Rules:
- Every item must be VERIFIED, not assumed. "Landing page is live" means you visited the URL and saw the page. "Email sequence is active" means you sent a test email and it arrived. "Stripe checkout works" means you ran a test purchase.
- Blocking items are those that would cause launch day failure or create a bad first impression for actual users. Everything else is non-blocking.
- Non-blocking items have a mitigation note: "If this isn't done, the impact is X and the workaround is Y."
- Tier 3 deliverables (AI-Starter — e.g., human video recording pending) are non-blocking by default — mark as `[AI-Starter, upgrade pending]` and confirm AI version is live
- Verdict is READY only if ALL blocking items pass. Any blocking FAIL = BLOCKED with the specific items listed.
- Use automation where possible: `browser` tool to verify live URLs, test forms, check OG tags; `exec` to run link validators
- Output includes a one-line status summary for the Gate-L Decision Packet

## User Prompt

**Product URL:** {product_url}
**Landing Page URL:** {landing_page_url}
**All parallel stage outputs and test logs:** {stage_artifacts_summary}

Run the full pre-launch checklist:

1. **Product** — Is the app live, working, and mobile-responsive?
2. **Landing Page** — Is the page deployed, copy final, and OG tags correct?
3. **Analytics** — Is tracking verified end-to-end?
4. **Email Capture** — Are forms live and tested?
5. **Email Sequence** — Is the nurture sequence active and verified?
6. **Payment / Checkout** — Is Stripe live and tested?
7. **Post-Purchase** — Is the onboarding sequence active?
8. **Content** — Is launch content drafted for all platforms?
9. **Directories** — Have pre-launch submissions been sent?
10. **Stage 9** — Are draft queues healthy and high-risk approvals resolved?

## Checklist Format

For each item:
```
[✅ PASS | ❌ FAIL | ⚠️ PARTIAL | 🔵 NON-BLOCKING] Item description
  Verification: how it was checked
  Evidence: link or log reference
  Mitigation (if non-blocking): workaround if still not done
```

## Full Checklist

---

### PRODUCT

**[BLOCKING]**

```
[ ] Product URL is live and returns 200
  Verification: browser navigate {product_url}
  Evidence: screenshot of landing/home screen

[ ] Core feature works (primary use case completes without error)
  Verification: manual or automated walkthrough of primary user flow
  Evidence: browser session log or screenshot of completed flow

[ ] Product is mobile-responsive (375px viewport)
  Verification: browser screenshot at 375px
  Evidence: mobile screenshot saved to broll directory

[ ] Error states handle gracefully (no raw stack traces visible to users)
  Verification: trigger common error paths (wrong password, bad input)
  Evidence: note of error message seen

[ ] Sign-up / account creation works
  Verification: create test account end-to-end
  Evidence: confirmation email received by test account
```

---

### LANDING PAGE

**[BLOCKING]**

```
[ ] Landing page is deployed at {landing_page_url} and loads correctly
  Verification: browser navigate, screenshot
  Evidence: screenshot broll-lp-desktop.png

[ ] OG tags are correct (title, description, image)
  Verification: paste URL into https://www.opengraph.xyz/ or browser social preview
  Evidence: screenshot of social preview

[ ] Landing page is mobile-responsive (375px)
  Verification: browser screenshot at 375px
  Evidence: screenshot broll-lp-mobile.png

[ ] Signup form is visible and works
  Verification: submit test email, verify in email provider
  Evidence: email provider shows test signup

[ ] CTA button routes to correct destination (signup form or checkout)
  Verification: click CTA, verify destination
  Evidence: browser screenshot of destination

[ ] Page load time < 3s
  Verification: browser DevTools Network tab or GTmetrix
  Evidence: load time noted
```

**[NON-BLOCKING]**

```
[ ] FAQ section populated (not empty placeholder)
  Mitigation: empty FAQ is visible — add top 3 objections if not done. Impact: reduced trust signals.

[ ] Social proof section has content (testimonials or "join X users")
  Mitigation: use signup count if no testimonials yet. "Join 47 early users" is fine.
```

---

### ANALYTICS

**[BLOCKING]**

```
[ ] GA4 tracking verified end-to-end (page_view and lead_signup events fire)
  Verification: tracking-test-log.md all P0 events PASS
  Evidence: link to tracking-test-log.md

[ ] UTM parameters appear correctly in GA4 session source/medium
  Verification: UTM verification section of analytics-setup.md
  Evidence: GA4 Traffic Acquisition screenshot with UTM source visible

[ ] Meta Pixel fires correctly (if Meta in channel plan)
  Verification: Pixel Helper browser extension or Events Manager
  Evidence: screenshot of events confirmed
```

---

### EMAIL CAPTURE

**[BLOCKING]**

```
[ ] Email capture form works on landing page (submit → subscriber appears in email provider)
  Verification: end-to-end form test, check email provider group
  Evidence: screenshot of new subscriber in group

[ ] Lead magnet delivery confirmed (download link in welcome email works)
  Verification: submit form with test email, open welcome email, click download
  Evidence: PDF or asset downloaded successfully

[ ] Email provider group exists: {product_slug}-leads
  Verification: check email provider dashboard
  Evidence: group name and ID noted
```

---

### NURTURE SEQUENCE

**[BLOCKING]**

```
[ ] Welcome sequence imported into email provider as live automation
  Verification: check automation panel — status ACTIVE
  Evidence: screenshot of active automation

[ ] Automation trigger configured: fires when subscriber joins {product_slug}-leads group
  Verification: trigger test (add subscriber to group manually, confirm Day 0 email sends)
  Evidence: test email received with correct content

[ ] Test email sent and received for all 7 emails in sequence
  Verification: email-sequence test log
  Evidence: link to test log

[ ] Unsubscribe footer present and functional in all emails
  Verification: click unsubscribe in test email, confirm removal from group
  Evidence: unsubscribe confirmed working
```

---

### PAYMENT / CHECKOUT

**[BLOCKING]**

```
[ ] Stripe products and prices created in LIVE mode (not just test mode)
  Verification: Stripe Dashboard → Products → confirm live mode products exist
  Evidence: closing/stripe-config/products.json with live IDs

[ ] Checkout flow tested end-to-end in LIVE mode with a $0 or $1 test charge
  Verification: stripe-test-log.md — all steps PASS in live mode
  Evidence: link to test log, Stripe transaction ID

[ ] Pricing page deployed and shows correct pricing
  Verification: browser navigate to /pricing, screenshot
  Evidence: screenshot of pricing page with correct tier names and prices

[ ] Pricing page "Get Started" buttons route to correct Stripe checkout per tier
  Verification: click each CTA, verify correct tier loads in Stripe
  Evidence: browser screenshots of Stripe checkout screens per tier

[ ] Founding member coupon "founding-member-40" is active (live mode)
  Verification: apply coupon in Stripe checkout, verify discount shows
  Evidence: screenshot with discount applied
```

**[NON-BLOCKING]**

```
[ ] Annual pricing toggle works on pricing page
  Mitigation: if toggle broken, show monthly only. Annual offer can be communicated in email.

[ ] Customer Portal configured (self-service billing management)
  Mitigation: without Portal, cancellations require manual email. Acceptable for first week.
  Due: must be live before first 10 paying customers.
```

---

### POST-PURCHASE

**[BLOCKING]**

```
[ ] Post-purchase email sequence exists and is ACTIVE (separate from nurture sequence)
  Verification: email provider automation panel — post-purchase automation ACTIVE
  Evidence: screenshot

[ ] Post-purchase automation triggered by Stripe purchase (or correct webhook event)
  Verification: test purchase → verify Day 0 onboarding email fires
  Evidence: test email received with "You're in" subject line

[ ] User gets product access immediately after payment (provisioning works)
  Verification: test purchase → verify account is in paid tier
  Evidence: dashboard screenshot showing paid tier status
```

---

### CONTENT

**[NON-BLOCKING — but must be PARTIAL or better]**

```
[ ] Launch announcement copy drafted for: IG, X/Twitter, Reddit, LinkedIn, Email blast
  Verification: awareness/social/ directory has files for each platform
  Evidence: file list

[ ] Product Hunt submission drafted (tagline, description, screenshots, maker comment)
  Verification: launch/ph-submission.md exists
  Evidence: file path

[ ] IndieHackers "Shipped" post drafted
  Verification: launch/ih-shipped.md exists
  Evidence: file path
```

**Tier 3 deliverables (AI-Starter):**
```
[ ] [AI-Starter, upgrade pending] Launch announcement video — AI version is live, talent recording may be pending
  Mitigation: AI video is the launch version. Human recording swaps in when ready. Non-blocking.

[ ] [AI-Starter, upgrade pending] Founder headshot / about page photo
  Mitigation: AI portrait is live. Professional photo deferred.
```

---

### DIRECTORIES

**[NON-BLOCKING]**

```
[ ] Pre-launch submissions sent to: BetaList, SaaSHub, LaunchingNext, MicroLaunch, Unued
  Mitigation: directories have 1-2 week review queues. Submit immediately if not done.
  Impact: delayed but compounding SEO backlinks. Not launch-blocking.

[ ] Product Hunt submission drafted and scheduled
  Verification: PH submission form saved as draft
  Note: Do NOT submit PH until launch day 12:01 AM PT
```

---

### STAGE 9

**[BLOCKING]**

```
[ ] All high-risk deliverables resolved (not in awaiting_max_approval limbo)
  Verification: review Stage 9 blackboard — no high-risk items in pending state
  Evidence: list of approved vs deferred items

[ ] No blocking critic REVISE verdicts unresolved
  Verification: check critic comment log for any open REVISE verdicts
  Evidence: critic verdict summary

[ ] Draft queue healthy — all launch content is in draft_scheduled or verified
  Verification: content-engine.py today output shows correct queue
  Evidence: content-engine queue screenshot
```

---

## Verdict

```
READY ✅ — All blocking items passed. Launch Day can proceed.
  Non-blocking items: [list]
  Tier 3 items pending: [list]
  Recommended launch window: [date/time]

--- OR ---

BLOCKED ❌ — The following blocking items failed:
  1. [Item name] — [what failed] — [how to fix]
  2. ...
  Estimated time to resolve: [X hours]
  Re-run checklist after fixes.
```

## Gate-L Status Summary (one line for Decision Packet)

```
status_summary: Pre-launch checklist {X}/{Y} blocking items PASS — [READY | BLOCKED: {items}]
```

### Blackboard Keys
- `launch.pre_launch_checklist`: link to this document
- `launch.readiness_verdict`: READY | BLOCKED
- `launch.blocking_failures`: [] (empty if READY)
- `launch.non_blocking_items`: [list of non-blocking items and mitigations]


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
