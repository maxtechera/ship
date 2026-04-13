# ShipEngine Agentic Updates Proposal

**Date:** [REDACTED_PHONE]  
**Author:** Neo (subagent analysis)  
**Status:** Draft for Review

---

## 1. Executive Summary

The ShipEngine spec is impressively detailed — a 12-stage product shipping pipeline with clear tool mappings, state schema, and parallel execution. However, it was written as a **static orchestration blueprint** rather than a **resilient agentic system**. The main gaps are:

1. **No error handling or retry logic anywhere** — if a sub-agent fails, the spec is silent
2. **No feedback loops** — Measure stage collects data but never feeds it back to improve Marketing, Outbound, or Nurture
3. **8 tools listed as "To Build" that don't exist** — 3 are P1 blockers (mailerlite.py, reddit.py) meaning Lead Capture, Nurture, Closing, and Outbound stages can't fully automate
4. **No inter-stage communication** — parallel stages (Build, Marketing, Outbound, etc.) run in isolation with no shared context
5. **State file is write-only** — no recovery, checkpointing, or rollback patterns

Industry patterns from LangGraph, CrewAI, and production agentic systems show clear solutions for all of these. This proposal recommends **15 specific changes**, prioritized by impact.

---

## 2. Gap Inventory

### 🔴 Critical (Blocks Core Functionality)

| # | Gap | Stages Affected | Description |
|---|-----|-----------------|-------------|
| G1 | **No error handling** | All | Zero mention of what happens when a tool call fails, a sub-agent crashes, or an API returns an error. No retries, no fallbacks, no escalation. |
| G2 | **Missing P1 tools** | Lead Capture, Nurture, Closing, Outbound | `mailerlite.py` and `reddit.py` are P1 but don't exist. Without them, 4 of 6 parallel stages are manual. |
| G3 | **No state recovery** | All | If the orchestrator dies mid-run, there's no checkpoint/resume. State file exists but no pattern for loading and continuing from last good state. |
| G4 | **No feedback loops** | Measure → all | Measure collects metrics but the spec never describes how insights flow back. A failing funnel should trigger Marketing/Outbound adjustments automatically. |

### 🟠 High (Degrades Quality)

| # | Gap | Stages Affected | Description |
|---|-----|-----------------|-------------|
| G5 | **No inter-stage messaging** | Parallel stages | Build needs Marketing copy. Marketing needs Build screenshots. Outbound needs Lead Capture URLs. No mechanism for this. |
| G6 | **No quality gates on outputs** | All | Sub-agents produce outputs but nothing validates quality before advancing. No critic/judge pattern. |
| G7 | **Validate stage over-specified** | Validate | 5 levels of validation with specific search queries is brittle. Real queries depend on the idea. The scoring rubric is good; the prescribed searches are too rigid. |
| G8 | **No timeout/SLA management** | Parallel stages | If Build takes 3 days but Marketing finishes in 2 hours, what happens? No timeouts, no progress tracking, no escalation. |

### 🟡 Medium (Improvement Opportunities)

| # | Gap | Stages Affected | Description |
|---|-----|-----------------|-------------|
| G9 | **No cost tracking during execution** | All | Budget is estimated in Strategy but never tracked in real-time. API calls, sub-agent tokens, tool usage — all unmetered. |
| G10 | **Templates referenced but don't exist** | All | 11 templates referenced (`templates/*.md`) — unclear if they exist or are placeholders. |
| G11 | **Telegram-specific UX** | Intake, Approvals | Hard-coded to Telegram (group ID, inline buttons). Should be channel-agnostic since workspace uses Slack. |
| G12 | **No A/B testing or experimentation** | Marketing, Outbound | Spec assumes one version of everything. No pattern for testing multiple headlines, CTAs, or channels. |
| G13 | **Manual content creation bottleneck** | Marketing | Max must record behind-the-scenes content manually. No delegation pattern for this. |

### 🔵 Low (Nice to Have)

| # | Gap | Description |
|---|-----|-------------|
| G14 | **No observability/logging** | No structured logging, tracing, or dashboards beyond Linear tickets. |
| G15 | **No learning across runs** | Each ship run starts from scratch. No institutional memory from previous runs. |

---

## 3. Research Insights

### 3.1 State Machine Orchestration (LangGraph Pattern)

The industry standard for production agentic pipelines is **explicit state graphs** with:
- **Typed state objects** that flow between nodes
- **Conditional edges** — next stage depends on current state, not just sequence
- **Checkpointing** — save state after every node, resume from any point
- **Human-in-the-loop nodes** — explicit pause points where the graph yields to a human

**ShipEngine implication:** The current pipeline is a linear DAG with one parallel fork. It should adopt state-graph patterns: typed state, conditional transitions, and checkpoint-resume.

### 3.2 Critic/Judge Pattern

Best practice: every agent output passes through a **judge agent** before advancing. The judge checks against a rubric (completeness, quality, alignment with goals). Failed outputs get sent back with feedback.

**ShipEngine implication:** Add quality gates after Validate (is the research thorough?), Strategy (is the plan actionable?), and Marketing (is the copy on-brand?).

### 3.3 Coordinator-Worker with Shared Blackboard

CrewAI's model: a coordinator maintains a **shared context/blackboard** that all worker agents can read and write to. This solves inter-stage communication.

**ShipEngine implication:** The state file should become a shared blackboard. When Build deploys, it writes the URL. When Marketing needs screenshots, it reads the URL. Currently these are siloed.

### 3.4 Reflexion + Feedback Loops

Production systems use **reflexion patterns**: after Measure, insights automatically trigger re-evaluation of earlier stages. E.g., "landing page converts at 1% instead of target 5%" → auto-generate Marketing optimization tasks.

**ShipEngine implication:** Measure should have automated triggers that create new Linear issues or restart specific stages with updated context.

### 3.5 Durable Execution (Temporal Pattern)

Long-running workflows (days/weeks like ShipEngine) need **durable state** — the ability to sleep, wake on events, and survive process restarts. Temporal.io pioneered this; agentic systems adopt it via cron + state files.

**ShipEngine implication:** `engine.py` should be event-driven, not a single long-running process. Each stage transition should be a discrete invocation that loads state, executes, saves state.

### 3.6 Constraint-Driven Planning

Rather than prescribing exact tool calls (as Validate does), define **constraints and success criteria** and let the agent choose tools dynamically.

**ShipEngine implication:** Validate should say "find 5+ real user pain quotes with sources" not "run `web_search 'reddit {problem}'`".

---

## 4. Specific Proposed Changes

### Change 1: Add Error Handling Framework

**Add new section after Pipeline Overview:**

```markdown
## Error Handling & Recovery

### Retry Policy
| Error Type | Retries | Backoff | Escalation |
|-----------|---------|---------|------------|
| Tool call failure (API error) | 3 | Exponential (5s, 15s, 45s) | Log + continue with degraded output |
| Sub-agent crash | 1 | Immediate respawn | Alert Max if second failure |
| Approval timeout (48h) | 0 | N/A | Auto-pause, ping at 24h and 48h |
| Build deployment failure | 2 | 10 min | Block launch, alert Max |
| External API down (Stripe, MailerLite) | 5 | 30 min intervals | Skip stage, flag for manual |

### Recovery Pattern
1. Every stage writes checkpoint to state file BEFORE and AFTER execution
2. `engine.py resume {ticket}` loads last checkpoint and continues
3. Failed stages can be individually retried: `engine.py retry {ticket} {stage}`
4. Partial outputs are preserved — retry appends, doesn't replace
```

### Change 2: Add Feedback Loops from Measure

**Add to Stage 11 (Measure):**

```markdown
### Automated Feedback Triggers
| Metric | Threshold | Auto-Action |
|--------|-----------|-------------|
| Landing page conversion < 2% | D+3 | Create "Optimize: Landing Page" sub-issue, trigger Marketing review |
| Email open rate < 15% | D+7 | Generate 3 alternative subject lines, A/B test via mailerlite |
| Zero signups from a channel | D+5 | Pause that channel's outbound, reallocate effort |
| Revenue > 80% of target | D+14 | Trigger "Double Down" playbook (more content, consider ads) |
| Churn > 20% in first week | D+10 | Trigger onboarding sequence review, add check-in email |

Feedback creates new Linear sub-issues under the parent with label `ship-engine-iterate`.
```

### Change 3: Add Shared Blackboard to State File

**Modify state file schema — add `blackboard` section:**

```json
{
  "blackboard": {
    "product_url": null,
    "landing_page_url": null,
    "signup_form_url": null,
    "stripe_checkout_url": null,
    "utm_links": {},
    "key_pain_quotes": [],
    "competitor_prices": [],
    "marketing_assets": [],
    "build_status": "not_started",
    "screenshot_paths": []
  }
}
```

All parallel stages read from and write to the blackboard. This replaces implicit handoffs.

### Change 4: Make Validate Goal-Driven, Not Script-Driven

**Before (current — overly prescriptive):**
```
| Reddit pain threads | `web_search "reddit {problem}"` + `web_fetch` | Threads, upvotes, quotes |
```

**After (goal-driven with success criteria):**
```markdown
### Level 1: Pain Discovery
**Goal:** Find 5+ real user pain quotes with sources. Evidence of recurring complaints.
**Success Criteria:** At least 3 distinct sources (Reddit, X, forums, reviews). Quotes with context.
**Suggested tools:** `web_search`, `research.py`, `web_fetch` — agent chooses based on idea domain.
**Fail condition:** If < 3 quotes found after 10 min of searching → score Pain Frequency as 1, move on.
```

### Change 5: Add Quality Gates (Critic Pattern)

**Add new section:**

```markdown
## Quality Gates

After each stage output, a critic pass validates before advancing:

| Stage | Critic Check | Pass Criteria |
|-------|-------------|---------------|
| Validate | Are pain quotes real (URLs work)? Is scoring justified? | All sources verifiable, scores match evidence |
| Strategy | Is MVP scope actually minimal? Budget realistic? | < 2 week build time, budget < $100 for v1 |
| Build | Core feature works? Mobile responsive? | `web_fetch` returns 200, browser screenshot looks right |
| Marketing | Copy is human-readable? No AI slop? | `humanize` skill score > 7/10 |
| Launch | All checklist items green? | 100% checklist pass |

Failed critic → feedback to stage agent → one revision → if still fails → flag for Max.
```

### Change 6: Add Timeout/SLA Management

**Add to Parallel Execution Map section:**

```markdown
### Stage SLAs
| Stage | Expected Duration | Timeout | On Timeout |
|-------|------------------|---------|------------|
| Validate | 30 min | 2 hours | Complete with available data, flag gaps |
| Strategy | 15 min | 1 hour | Auto-generate with defaults, flag for review |
| Build | 1-7 days | 14 days | Escalate to Max, suggest scope cut |
| Marketing | 2-4 hours | 24 hours | Launch with minimum assets |
| Outbound | 1-3 days | 7 days | Launch with available channels |
| Lead Capture | 1-2 hours | 6 hours | Use basic form, skip fancy funnels |
| Nurture | 1-2 hours | 6 hours | Use 3-email minimum sequence |
| Closing | 1-2 hours | 6 hours | Use simple Stripe checkout link |

Progress check: `engine.py` pings each sub-agent session every 4 hours.
```

### Change 7: Make UX Channel-Agnostic

**Before:**
```
### Primary Interface: neo-ship-engine group (-[REDACTED_PHONE])
```

**After:**
```markdown
### Primary Interface
Channel-agnostic. Works wherever OpenClaw is connected.
- **Slack:** Post to configured ship-engine channel
- **Telegram:** Post to configured group
- **Discord:** Post to configured channel

Configure in `engine.py` config or state file. Commands and approval buttons adapt to platform.
```

### Change 8: Add Cross-Run Learning

**Add new section:**

```markdown
## Institutional Memory

After each run completes (success or kill):
1. Extract lessons: what worked, what didn't, actual vs estimated timelines
2. Append to `skills/engine/LEARNINGS.md`
3. Future Strategy stages load LEARNINGS.md as context
4. Scoring calibration: compare Validate predictions vs Measure actuals

Schema for learnings:
| Run | Idea | Validate Score | Actual Outcome | Key Lesson | Date |
```

### Change 9: Event-Driven Architecture

**Before (implicit):** `engine.py` runs as a monolith coordinating everything.

**After (explicit):**

```markdown
## Execution Model

ShipEngine is **event-driven**, not a long-running process.

Triggers:
- `engine.py create {idea}` → creates state, sets up Linear, advances to Validate
- `engine.py advance {ticket}` → loads state, runs next stage(s), saves state
- `engine.py event {ticket} {event}` → handles external events (approval, build complete, etc.)
- Cron: `engine.py check-all` → every 4 hours, checks all active runs for timeouts/progress

Each invocation: load state → execute → save state → exit.
No long-running processes. Survives restarts by design.
```

---

## 5. Priority Ranking

| Priority | Change | Effort | Impact | Why First |
|----------|--------|--------|--------|-----------|
| **P0** | Build `mailerlite.py` | 1-2 days | Unblocks 3 stages | Without it, Lead Capture/Nurture/Closing are manual |
| **P0** | Build `reddit.py` | 1 day | Unblocks Outbound | Primary community channel |
| **P1** | Error handling framework (Change 1) | 2 hours | All stages resilient | Currently any failure = silent death |
| **P1** | Shared blackboard (Change 3) | 1 hour | Parallel stages communicate | Currently siloed |
| **P1** | Event-driven architecture (Change 9) | 4 hours | Durable execution | Currently fragile to restarts |
| **P2** | Quality gates (Change 5) | 2 hours | Output quality | Prevents garbage advancing |
| **P2** | Feedback loops (Change 2) | 2 hours | Measure becomes useful | Currently write-only metrics |
| **P2** | Timeout/SLA (Change 6) | 1 hour | Prevents stuck runs | Currently no deadlines |
| **P3** | Goal-driven Validate (Change 4) | 1 hour | More flexible | Current scripts are brittle |
| **P3** | Channel-agnostic UX (Change 7) | 1 hour | Platform portability | Currently Telegram-only |
| **P3** | Cross-run learning (Change 8) | 1 hour | Compounds over time | Nice to have from run 2+ |

---

## 6. New Patterns to Adopt

### Pattern 1: Checkpoint-Resume (from Temporal/LangGraph)
Every stage transition saves a checkpoint. `engine.py resume` picks up from the last checkpoint. This is the single most important architectural pattern for long-running agentic workflows.

### Pattern 2: Critic/Judge Agent (from CrewAI, industry standard)
A lightweight critic pass after each stage output. Uses a rubric specific to the stage. Costs ~500 tokens per check, saves hours of bad output propagating.

### Pattern 3: Shared Blackboard (from multi-agent literature)
Replace implicit handoffs with an explicit shared state that all agents read/write. The state file already exists — extend it with a `blackboard` section.

### Pattern 4: Reflexion Loops (from Measure back to earlier stages)
Don't just measure — react. Automated triggers when metrics miss targets. Creates new tasks, not just reports.

### Pattern 5: Constraint-Based Planning (from HTN/modern agent patterns)
Define what success looks like, not how to achieve it. Let agents pick tools dynamically. More robust to changing tool availability and different idea types.

### Pattern 6: Graceful Degradation
When a non-critical tool is unavailable (e.g., `utm.py` not built yet), the system should continue with manual alternatives rather than blocking. Each "To Build" tool should have a documented manual fallback.

---

## 7. Quick Wins (Implementable Today)

1. **Add `blackboard` to state schema** — 10 min edit to SKILL.md
2. **Add error handling section** — 15 min edit to SKILL.md  
3. **Document manual fallbacks** for each "To Build" tool — 20 min
4. **Create LEARNINGS.md template** — 5 min
5. **Add SLA table** — 5 min edit to SKILL.md
6. **Fix channel references** — Telegram → channel-agnostic — 10 min

Total: ~1 hour of spec updates that immediately improve robustness.

---

## Appendix: Research Sources

- "20 Agentic AI Workflow Patterns That Actually Work in 2025" — Skywork.ai
- "AI Agent Orchestration: Multi-Agent Workflow Guide" — DigitalApplied.com  
- "A Practical Guide for Production-Grade Agentic AI Workflows" — arxiv.org/html/[REDACTED_PHONE]v1
- "Agents At Work: The 2026 Playbook for Reliable Agentic Workflows" — promptengineering.org
- Framework comparisons: DataCamp, GetMaxim.ai, Latenode (CrewAI vs LangGraph vs AutoGen)
