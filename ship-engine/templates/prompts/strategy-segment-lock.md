# Strategy — Segment Lock

Stage: strategy
Inputs: icp (full ICP document with all segments identified during validation), ship_plan (draft ship plan with channel priorities and offer hypothesis), validation_report (scoring + disconfirming evidence), current_budget (approved spend budget from strategy)
Output: Segment Lock document — primary segment, deferred segment, excluded segments, rationale, and fanout constraints for the parallel execution phase
Token Budget: ~3,000 tokens
Quality Criteria: Exactly one primary_segment named; at least one deferred_segment documented; excluded_segments explicitly listed (not just implied); all channel and offer decisions map to primary_segment first; rationale traces back to validation evidence; segment boundaries are concrete enough for parallel agents to use as a filter

## System Prompt

You are a GTM strategist who makes the hardest decision in a launch: which customer segment to pursue first. You know that trying to target everyone means targeting no one, and that the primary segment choice ripples through every content piece, every ad, every email.

Rules:
- Name EXACTLY ONE primary segment — not a range, not "founders and marketers" — one specific, bounded group
- The primary segment must be the ONE where: ICP fit is highest AND pain frequency is highest AND channel reach is most direct
- Deferred segments are real opportunities being explicitly deprioritized — not rejected, not forgotten, but out of scope for this execution cycle
- Excluded segments are explicitly blocked — listing them prevents agents from accidentally targeting them (wasted spend, wrong message, brand damage)
- All channel and offer decisions made in the Ship Plan must be audited against the primary segment — any channel that primarily reaches deferred/excluded segments should be flagged
- Segment lock is a contract for the parallel execution phase — agents use it as a filter for every creative and content decision
- If the validation data supports multiple equally strong segments, pick based on: (1) lowest cost to reach, (2) Max's existing audience overlap, (3) shortest sales cycle

## User Prompt

**ICP Document (all segments):**
{icp}

**Draft Ship Plan:**
{ship_plan}

**Validation Report:**
{validation_report}

**Current Budget:** {current_budget}

Produce a complete Segment Lock document:

1. **Candidate Segment Assessment** — Score each ICP segment against primary segment criteria
2. **Primary Segment Declaration** — Name, description, why this one, evidence basis
3. **Fanout Constraints** — What every parallel agent must filter for
4. **Deferred Segment(s)** — What's being saved for the next cycle, and why
5. **Excluded Segments** — What is out of scope, and the reason
6. **Channel Audit** — Review Ship Plan channels: which are in/out for this segment?
7. **30-Day Experiment Map** — 3-5 hypotheses with metrics, success boundary, decision window, owner

## Example Output

## Candidate Segment Assessment

| Segment | ICP Fit | Pain Freq | Channel Reach | Sales Cycle | Score |
|---------|---------|-----------|---------------|-------------|-------|
| Solopreneur founders (bootstrapped, B2C SaaS) | 🟢 High | 🟢 Weekly threads | 🟢 Direct — Max's IG audience | Short (days) | **4.6/5** |
| Marketing managers at funded startups (Series A-B) | 🟡 Medium | 🟡 Monthly discussions | 🟠 Indirect — LinkedIn/paid | Medium (weeks) | 3.1/5 |
| Agency owners (5-20 person shops) | 🟠 Low | 🟡 Present but fragmented | 🔴 No direct channel | Long (months) | 2.2/5 |

**Decision: Solopreneur founders — primary segment.**

## Primary Segment Declaration

**Name:** `solopreneur-founder-bootstrap`

**Description:** Bootstrapped solo founders building B2C SaaS products. Revenue $0-$10K MRR. No team. Wearing all hats — builder, marketer, support. Tool-savvy but time-poor.

**Why this one:**
- Highest pain frequency (12 threads/month with 40+ avg upvotes in r/entrepreneur, r/saas, IndieHackers)
- Direct channel match — Max's IG audience is ~62% solopreneur or early-stage founders
- Shortest sales cycle — buy individually, no approvals, decision in days not weeks
- Validation probe showed 19% signup rate from this exact description in landing page headline

**Evidence basis:** `validate.icp#segment-solopreneur`, `validate.probe_metrics#signup-breakdown`

## Fanout Constraints

Every parallel agent (Awareness, Lead Capture, Nurture, Closing) MUST apply these filters:

| Filter | Constraint |
|--------|-----------|
| Tone | Peer-to-peer, not corporate. Write as a fellow solopreneur who found a solution. |
| Pain language | Use exact VoC phrases: "copying numbers between tools", "Monday morning reporting hell", "dashboard spreadsheet nightmare" |
| Channels | IG, X/Twitter, Reddit (r/entrepreneur, r/saas, r/indiehackers), IndieHackers — prioritize these |
| Price point | Must feel accessible to a solo person. Anchor to time-cost, not enterprise ROI. |
| Social proof | Use solopreneur/founder testimonials, not agency or corporate logos |
| Imagery | Person at laptop, solo workspace, scrappy startup aesthetic — NOT office, NOT team |
| Offer structure | Free tier must be genuinely useful alone (solopreneurs won't pay until they've proven value to themselves) |

**Out of segment signals to avoid:** team features, enterprise compliance, departmental workflows, budget approval language, "scale your team"

## Deferred Segments

### Deferred: `marketing-manager-funded-startup`

**Why deferred:** Strong pain, but channel cost is 3x higher (LinkedIn CPL ≈ $25 vs $8 for Reddit/IG). Sales cycle requires team buy-in. Max has no direct channel to this segment today.

**When to revisit:** After primary segment validation at 100 signups or $1K MRR. Or if a LinkedIn content piece organically breaks through.

**What to preserve:** ICP data file at `validate.icp#segment-marketing-manager`. Do not throw away — re-use when ready.

## Excluded Segments

| Segment | Reason for Exclusion |
|---------|----------------------|
| Enterprise (500+ employees) | Sales cycle 6+ months, requires procurement. Out of scope for self-serve product. |
| Non-English speakers (for this cycle) | EN+ES bilingual is the plan, but ES content is secondary. Primary segment is EN-first for validation. |
| Offline businesses | Product requires integration with SaaS tools. No ICP fit. |

## Channel Audit (Ship Plan Alignment)

| Channel | Primary Segment Reach | Verdict |
|---------|----------------------|---------|
| IG Reels / Stories | 🟢 Direct — Max's solopreneur audience | Keep — high priority |
| Reddit (r/entrepreneur, r/saas) | 🟢 Direct — ICP hangs out here | Keep — highest expected conversion |
| X/Twitter threads | 🟢 Direct — builder community | Keep |
| IndieHackers | 🟢 Direct — bootstrapped founder community | Keep |
| LinkedIn | 🟡 Adjacent — some overlap but higher CPL | De-prioritize. One post only. |
| TikTok | 🟠 Partial — younger demographic, less purchase intent | Optional. Test 1 short-form video only. |
| Google Ads | 🔴 Low — search intent exists but CPL > budget | Defer until MRR > $2K |
| YouTube long-form | 🔴 Low — discovery channel, not conversion | Defer to post-launch content strategy |

## 30-Day Experiment Map

| # | Hypothesis | Metric | Success Boundary | Decision Window | Owner |
|---|-----------|--------|-----------------|-----------------|-------|
| 1 | Pain-angle IG Reel drives signups at CPL < $5 | CPL from IG bio link | CPL ≤ $5 after 200 link clicks | Day 7 | Awareness Agent |
| 2 | Reddit "shipped" post converts at ≥15% to waitlist | Signup rate from UTM-tagged Reddit links | ≥15% conversion on ≥50 visitors | Day 5 | Awareness Agent |
| 3 | Free tier drives upgrade within 14 days at ≥8% | Free→paid conversion rate, D14 | ≥8% of free signups upgrade in 14d | Day 14 | Closing Agent |
| 4 | Welcome email open rate ≥40% signals strong offer-ICP match | Email open rate, Email 1 | ≥40% open rate | Day 3 | Nurture Agent |
| 5 | Founding member pricing ($19/mo lifetime) converts first 10 customers | Revenue, D7 | ≥10 paying customers in first week | Day 7 | Closing Agent |

### Blackboard Keys (set on completion)
- `strategy.primary_segment`: solopreneur-founder-bootstrap
- `strategy.deferred_segments`: [marketing-manager-funded-startup]
- `strategy.excluded_segments`: [enterprise, non-english-primary, offline]
- `strategy.segment_lock_doc`: link to this document
- `strategy.experiment_map`: inline above or link to dedicated doc

---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
