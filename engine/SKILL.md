---
name: ship
version: "0.2.0"
description: End-to-end GTM automation engine. Validate → Strategy → Awareness → Lead Capture → Nurture → Closing → Launch → Measure.
user-invocable: false
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      env: []
      optionalEnv:
        - LINEAR_API_KEY
        - SHIP_RUNS_DIR
      bins: []
    tags:
      - gtm
      - pipeline
      - orchestration
      - ship
---

> ⚠️ **[IDEATION CANON + COMPATIBILITY LAYER]** `WORKFLOW.md` is canonical for runtime flow, but this file is preserved as the full ideation and user-intent record. Treat it as: (1) why the system exists, (2) historical constraints and requests, (3) compatibility notes that map legacy concepts to the current skill/automation structure.

# Ship ⚡🚢

End-to-end shipping automation. Idea → validated → built → marketed → sold → measured → iterated.

**This is an orchestrator.** It delegates to specialized skills and tools, owns the pipeline state, and ensures nothing falls through the cracks. The Ship Engine doesn't build, doesn't write emails, doesn't post on Reddit — it calls the tools that do.

---

## How To Use This Document Now

- `WORKFLOW.md` defines runtime stage transitions and gate behavior.
- This file defines strategic intent, ideation history, and operational patterns that still matter.
- If a section here conflicts with current runtime flow, do not delete it. Add/maintain a compatibility note that maps it to the current implementation.

### Legacy-to-Current Stage Alignment

Use this map when reading legacy stage language in this document:

| Legacy Concept (this file) | Current Canonical Runtime (`WORKFLOW.md`) |
|---|---|
| MINE + INTAKE | INTAKE + VALIDATE inputs and audience signal ingestion |
| BUILD + MARKETING + OUTBOUND + LEAD CAPTURE + NURTURE + CLOSING | STRATEGY fan-out into AWARENESS + LEAD CAPTURE + NURTURE + CLOSING |
| BETA | Covered by launch readiness checks and staged rollout gates |
| LAUNCH + MEASURE + ITERATE | LAUNCH + MEASURE loop |

### Current Skill Structure (Flat, Agentic)

Primary content asset execution uses flat skills:

- `skills/content-copy/SKILL.md`
- `skills/content-video/SKILL.md`
- `skills/content-image/SKILL.md`
- `skills/content-page/SKILL.md`
- `skills/content-blog/SKILL.md`
- `skills/content-offer/SKILL.md`
- `skills/content-form/SKILL.md`
- `skills/content-distribution/SKILL.md`
- `skills/content-storyboard/SKILL.md`
- `skills/content-broll/SKILL.md`
- `skills/content-research/SKILL.md`
- `skills/content-talent/SKILL.md`

Router: `skills/content-stages/SKILL.md`.

### Automation Capability Notes (Current)

- Fastpath pre-checks are part of cron automation policy: `tools/cron-fastpath.sh` and `tools/cron-fastpath-check.py`.
- Pencil is the default visual execution surface; OpenClaw remains source of truth for workflow state.
- Where this file references older tools/flows, keep the intent and map execution to current tools instead of deleting the requirement.

---

## Core Philosophy

### Audience-First, Not Idea-First

Max's unfair advantage is his audience (IG followers, newsletter, Skool community). The engine doesn't just validate ideas against an audience — it **mines the audience for ideas** in the first place.

Best ideas come FROM the audience:
- DMs asking "do you have a tool for X?"
- Repeated questions in Skool or comments
- Pain points surfacing in community discussions
- Students struggling with the same problem

The engine supports both paths:
1. **Audience signal → Idea** (preferred): a pattern emerges from the audience, engine structures it
2. **Max has an idea → Validate against audience** (classic): test if the audience cares

### Distribution-First Thinking

Before building anything, answer: **"How will buyers find this?"**

The channel determines the product shape, not the other way around:
- If IG is the channel → product needs visual hooks, demo-able in 30 seconds
- If SEO is the channel → product needs to solve a searchable problem
- If community is the channel → product needs word-of-mouth loops
- If newsletter is the channel → product needs an educational angle

Distribution channel is decided in **Strategy**, before Build starts. Build, Marketing, and Outbound all align to that channel choice.

### Adaptive Complexity

Not every idea needs 14 stages. The engine has three tracks:

| Track | When | Stages | Timeline |
|-------|------|--------|----------|
| **🏃 Sprint** | Audience already asking for it, low-risk, <$50 to ship | Intake → Fast Validate → Build → Launch → Measure | 1-3 days |
| **🚀 Standard** | New idea, needs research, moderate investment | Full pipeline | 1-3 weeks |
| **🔬 Deep** | High-risk, high-investment, uncharted territory | Full pipeline + Customer Interviews + Extended Beta | 3-6 weeks |

Track is decided at **Intake** based on risk signals. Can be upgraded mid-run if surprises emerge.

### The Messy Middle

Most products don't succeed on v1 or die on v1. They find product-market fit through iteration. The engine doesn't treat launch as the end — it treats it as the beginning of a feedback loop:

```
Build → Launch → Measure → Iterate → Measure → Iterate → ...
```

The Iterate stage (new) handles post-launch evolution until the product reaches PMF or gets killed.

---

## Pipeline Overview

```
MINE ─→ INTAKE ─→ VALIDATE ─→ STRATEGY ─→ BUILD ─────────────→ BETA ─→ LAUNCH ─→ MEASURE ─→ ITERATE
                     🔒                       ├── MARKETING        │       🔒                    ↺
                                              ├── OUTBOUND         │
                                              ├── LEAD CAPTURE     │
                                              ├── NURTURE          │
                                              └── CLOSING ─────────┘
```

**14 stages.** Build + Marketing + Outbound + Lead Capture + Nurture + Closing run concurrently. Beta waits for Build + Lead Capture. Launch waits for all + Max approval. Iterate loops after Measure.

### New Stages (vs previous version)
- **MINE** — Audience signal detection (passive, always-on)
- **BETA** — Early access testing with existing audience before public launch
- **ITERATE** — Post-launch improvement cycles based on Measure data

---

## Inter-Stage Communication

Stages communicate through **two external systems** — not internal state files. This makes handoffs durable, inspectable, and human-editable.

### Linear (Task State, Handoffs & Documents)
- **Stage transitions** → sub-issue state changes (Todo → In Progress → Done)
- **Handoff data** → comments on sub-issues (e.g., Build posts deploy URL, Marketing posts asset links)
- **Blockers** → sub-issue blocked status + comment explaining what's needed from which stage
- **Cross-stage requests** → mention the target sub-issue in a comment
- **Decision log** → all approvals, kills, pivots recorded as comments on parent issue
- **Attachments** → stage deliverables attached directly to Linear issues (docs, reports, assets)

### Linear Issue Structure & Feature Usage (Current Runtime)

Use this as the canonical field map for what Ship Engine tracks in Linear.

#### 1) Run container (parent issue)

| Field | Purpose | Used by |
|---|---|---|
| `id` | Stable UUID for API updates and joins | webhooks, server, automation tools |
| `identifier` (e.g. `MAX-316`) | Human run reference | comments, wake metadata, operator UX |
| `title` | Run title (`Ship: <offer>`) | dashboard, notifications |
| `description` | High-level run context and links | intake/strategy handoff |
| `state.{id,name,type}` | Run lifecycle state | automation routing, active/inactive checks |
| `labels` (contains `ship-engine`) | Run classification and cron filtering | sweep fastpath, supervisor discovery |
| `project.{id,name,url}` / `team.{id,key}` | Run project container (all run tickets attach here) | creation/query/update tools |
| `priority` | Queue ordering | triage and list views |
| `createdAt`, `updatedAt`, `dueDate` | Scheduling and staleness checks | dashboards, review cadence |

Project contract:
- Each run creates (or adopts) a Linear Project named `Ship: <name>`.
- Parent issue + all stage tickets + any derived tickets must share the run's `projectId`.

#### 2) Stage tickets (children/sub-issues)

Each stage ticket must contain and maintain:

| Contract block | Requirement |
|---|---|
| `Inputs` | Source context and dependencies are explicit |
| `Deliverables` | Concrete checklist of outputs to produce |
| `Verification` | How quality/completeness is proven |
| `Artifacts` | URLs/paths/attachments proving deliverables exist |

Operational behavior:
- Stage tickets do not move to `In Review` before deliverables exist.
- Stage tickets do not move to `Done` before verification evidence and artifact links are recorded.

#### 3) Parent-child linkage tracked in state

Ship Engine run state persists Linear linkage under:

| Key | Value shape |
|---|---|
| `linear.parentId` | Parent issue UUID |
| `linear.parentIdentifier` | Parent issue key (e.g. `MAX-316`) |
| `linear.subIssues.<stage>.id` | Child issue UUID |
| `linear.subIssues.<stage>.identifier` | Child issue key |

#### 4) Comment-level metadata (required writeback)

For meaningful status changes, comments should carry:

| Field | Purpose |
|---|---|
| `status_summary` | One-line status update |
| `next_steps` | Immediate next actions |

For hard gates and high-risk approvals, decision packet comments should include:

| Field | Purpose |
|---|---|
| `recommended_action` | `approve|revise|hold` |
| `recommendation_notes` | Why this decision is recommended |
| `risk_level` | `low|medium|high` |
| `confidence` | Confidence score for decision |
| `owner`, `due_by`, `queue_priority` | Accountability and queueing |
| `evidence_links` | Primary supporting links |
| `kanban_proof_links` | Links for Inputs/Deliverables/Verification/Artifacts |

#### 5) Deliverable lifecycle evidence linked through tickets/comments

Per deliverable, Ship Engine tracks and/or links:

| Field | Purpose |
|---|---|
| `critic_verdict` + `critic_evidence` | Quality gate proof before `verified`/`live` in production |
| `draft_id` | Platform draft OR publish-ready queue reference (calendar draft optional) |
| `approval_record` | Explicit approval reference (required for high risk) |
| `live_id_or_url` | Published asset pointer |
| `metrics_snapshot` | Time-stamped performance evidence |
| `disposition` | `promoted|iterating|killed` outcome |

#### 6) Webhook + wake metadata bound to Linear entities

When Linear events trigger automation, metadata envelope includes:

| Field | Purpose |
|---|---|
| `event_id` | Idempotency/dedupe key |
| `source` | Event origin (e.g. `linear`) |
| `trigger_type` | `webhook` or `cron_sweep` |
| `entity_key` | Target issue identifier |
| `issue_id` / `comment_id` | Target object IDs |
| `event_type` | Linear event class (`Issue.update`, `Comment.create`) |
| `occurred_at` | Event timestamp |
| `bounded_cycle` | Enforces one-safe-cycle behavior |

### Git Repo (Code & Artifacts)
Each ship run lives in its own repo (or monorepo subfolder):
```
{repo}/
├── docs/                # Strategy, research, plans (markdown)
│   ├── idea-brief.md
│   ├── validation-report.md
│   ├── ship-plan.md
│   └── post-launch/
├── marketing/           # Copy, content calendar, email drafts
├── assets/              # Images, logos, screenshots, videos
└── src/                 # Product code
```

**Why not Google Drive + Figma as defaults?**
- Drive and Figma add context switches and friction for a solo operator + AI agent
- Git repo keeps everything colocated with the code
- Linear attachments handle one-off docs that don't need version control
- Pencil is the default visual execution surface for runs
- If design work is needed, use Figma on-demand — not as a default run dependency

**Artifact policy:** Pencil board artifacts must link back to workspace files, deployed URLs, or run checkpoints.

## Content Asset Skills (Externalized)

Ship Engine orchestrates run state and approvals. Content asset creation is delegated to flat content skills:

- `skills/content-stages/SKILL.md` (router)
- `skills/content-copy/SKILL.md`
- `skills/content-video/SKILL.md`
- `skills/content-image/SKILL.md`
- `skills/content-page/SKILL.md`
- `skills/content-blog/SKILL.md`
- `skills/content-offer/SKILL.md`
- `skills/content-form/SKILL.md`
- `skills/content-distribution/SKILL.md`
- `skills/content-storyboard/SKILL.md`
- `skills/content-broll/SKILL.md`
- `skills/content-research/SKILL.md`
- `skills/content-talent/SKILL.md`

When adding new GTM asset types, create or extend flat `content-*` skills first, then update the router and Ship Engine references.

### Handoff Protocol
When a stage produces something another stage needs:
1. **Create the artifact** (commit to repo, attach to Linear, or comment with link)
2. **Post the link** as a comment on the relevant Linear sub-issue
3. **Update parent issue description** with key links (product URL, repo, live URLs)

No implicit handoffs. If it's not linked in Linear, it doesn't exist.

---

## Execution Philosophy

**The engine runs forever.** Once a ship run starts, it loops autonomously through stages until every deliverable passes its quality gate — or Max cancels. There is no "error state." A failed tool call, a bad output, a crashed sub-agent — these are just iterations, not terminal events.

### Core Principles

1. **Deliverables over process.** The engine doesn't care how many attempts it takes. It cares that the Validation Report exists, is verified, and meets the rubric. The journey is invisible; the artifact is everything.

2. **Iterate until done.** If a stage output fails its quality gate, the stage agent gets feedback and tries again. If the agent crashes, a new one spawns with the same context. If a tool is down, try a different tool or try later. The loop never stops on its own.

3. **Graceful degradation, not failure.** If a tool doesn't exist, search manually via `web_search`. If an API is down, draft the deliverable and flag for manual setup. Every "To Build" tool has an implicit fallback: do it with what exists.

4. **Autonomous advancement.** Stages advance automatically when quality gates pass. No human approval needed except at the three hard gates (post-Validation, pre-Launch, and Kill decisions). Everything else flows.

5. **Cancel is the only stop.** The engine doesn't pause, doesn't timeout into failure, doesn't give up. It escalates to Max when stuck (via Linear comment) but keeps the run alive. Only Max saying "kill it" stops a run.

6. **Fewer systems, faster shipping.** Every external dependency is friction. Default to Linear + Git. Add tools only when they earn their complexity.

7. **All channels, automated.** The engine's superpower is parallel execution across every distribution channel simultaneously. A solo human picks 1-2 channels because they're one person. Neo + sub-agents run them ALL — each channel gets a dedicated agent doing it properly. Strategy prioritizes channels (primary, secondary, tertiary) so effort scales with expected ROI, but nothing is skipped.

### Iteration Loop (per stage)
```
┌→ Spawn/resume stage agent with context (Linear + repo)
│       ↓
│  Agent works toward deliverable
│       ↓
│  Quality Gate evaluates output
│       ↓
│  ┌─ PASS → deliverable saved, linked in Linear, advance
│  └─ REVISE → feedback to agent, loop back ↑
│       ↓ (if agent crashes or tool fails)
│  Respawn agent with accumulated context, loop back ↑
└────────────────────────────────────────────────────┘
```

### Escalation (not failure)
When a stage has iterated 3+ times without passing its gate:
- Comment on Linear sub-issue: `⚠️ Stage {name} has attempted {N} iterations. Last feedback: {critic notes}. Continuing to iterate.`
- This is **informational**, not a blocker. The engine keeps going.
- Max can intervene or let it keep trying.

### Tool Resilience
| Situation | Response |
|-----------|----------|
| Tool call returns error | Retry with backoff (3 attempts), then try alternative tool |
| Tool doesn't exist yet | Use manual equivalent (web_search, web_fetch, LLM reasoning) |
| Sub-agent crashes | Respawn with same task + accumulated outputs from repo |
| External API down | Queue the action, continue other work, retry on next iteration |
| Rate limited | Back off, work on a different stage, return later |

### State Persistence
- All work products live in **Linear + Git repo** — not in agent memory
- If the orchestrator restarts, it reads current state from Linear (sub-issue statuses) and repo (existing artifacts)
- Nothing is lost because nothing important lives in ephemeral agent sessions

---

## Quality Gates

Every stage output passes through an automatic quality gate before the pipeline advances. Gates are run by a **critic agent** (lightweight, fast) that validates against stage-specific rubrics. No human involvement unless the gate fails twice.

### Gate Flow
```
Stage Agent produces output
        ↓
   Critic Agent evaluates (rubric + checklist)
        ↓
   ┌─ PASS → advance pipeline, comment ✅ on Linear sub-issue
   ├─ REVISE → feedback sent to stage agent, one retry allowed
   └─ FAIL (after retry) → flag for Max on Linear, block advancement
```

### Stage Rubrics

| Stage | Gate Checks | Pass Criteria |
|-------|------------|---------------|
| **Mine** | Signal has frequency + specificity | ≥3 instances of the same pain from different people |
| **Intake** | Brief is structured, has problem/audience/hypothesis, track assigned | All fields populated, no placeholder text, risk level assessed |
| **Validate (Fast)** | Landing page live, traffic sent, conversion measured | Page deployed, ≥100 visitors driven, conversion rate calculated |
| **Validate (Standard)** | Pain quotes real (URLs resolve), scoring matches evidence, 3+ sources | Sources verified via `web_fetch`, score justification per dimension |
| **Validate (Deep)** | Standard + 5+ customer conversations completed, patterns documented | Interview notes with direct quotes, pattern synthesis |
| **Strategy** | MVP scope is actually minimal, channel strategy specific, timeline dated | Build time ≤ 2 weeks, primary channel identified, calendar events created |
| **Build** | Core feature works, responsive, analytics installed | `web_fetch` returns 200, GA4 firing |
| **Marketing** | Copy is human-readable, assets match brand, all formats for primary channel | Humanizer score ≥ 7/10, OG image exists, primary channel assets complete |
| **Outbound** | 1-2 channels identified with rules documented, outreach is value-first | Communities mapped, sample content passes tone check |
| **Lead Capture** | Form works end-to-end, UTMs configured for primary channel | Test submission succeeds, UTM links resolve |
| **Nurture** | Email sequence complete, timing correct, CTAs present | All emails have subject + body + CTA, no broken links |
| **Closing** | Payment flow works, pricing page accurate | Test checkout succeeds (Stripe test mode) |
| **Beta** | Minimum 5 beta users activated, feedback collected, critical bugs fixed | Beta feedback doc with quotes, bug list with status |
| **Launch** | All pre-launch checklist items green | 100% checklist pass — any red item blocks launch |
| **Measure** | Metrics collecting, baselines established | GA4 + email + revenue data flowing |
| **Iterate** | Specific improvement identified, implemented, measured | Before/after metrics for the change |

### Critic Agent Implementation
- Spawned as a lightweight sub-agent per gate check
- Receives: stage output + rubric + context from Linear/repo
- Returns: `PASS`, `REVISE` (with specific feedback), or `FAIL` (with reason)
- Max token budget: ~2K per gate (keep it cheap)
- Results posted as Linear comments on the sub-issue

### Override
Max can force-advance past a failed gate. Override is logged on the Linear parent issue for traceability.

---

## Linear Data Structure

Each ship run maps to Linear:

```
MAX team → Idea Pipeline project
└── Parent Issue: "Ship: {name}" (label: ship-engine)
    ├── Sub-issue: "Mine: {name}" (if from audience signal)
    ├── Sub-issue: "Validate: {name}"
    ├── Sub-issue: "Strategy: {name}"
    ├── Sub-issue: "Build: {name}"
    ├── Sub-issue: "Marketing: {name}"
    ├── Sub-issue: "Outbound: {name}"
    ├── Sub-issue: "Lead Capture: {name}"
    ├── Sub-issue: "Nurture: {name}"
    ├── Sub-issue: "Closing: {name}"
    ├── Sub-issue: "Beta: {name}"
    ├── Sub-issue: "Launch: {name}"
    ├── Sub-issue: "Measure: {name}"
    └── Sub-issue: "Iterate: {name}" (created post-launch if needed)
```

- Parent issue = the idea (overview, brief, final verdict)
- Sub-issues = stages (move through states independently)
- Parallel stages = multiple sub-issues In Progress simultaneously
- Comments on sub-issues = stage outputs and deliverable links
- `ship-engine` label (orange, ID: `9178d59d-f529-4cfc-bb75-8ad78c9074e7`)

**State mapping:**

| Engine Phase | Parent State | Active Sub-issues |
|---|---|---|
| Mining | Backlog | Mine → In Progress (passive) |
| Intake done | Backlog | Validate → Todo |
| Validating | Todo | Validate → In Progress |
| Validated + approved | In Progress | Strategy → In Progress |
| Building + go-to-market | In Progress | Build, Marketing, Outbound, Lead Capture, Nurture, Closing → In Progress |
| Beta testing | In Progress | Beta → In Progress |
| Ready to launch | In Review | All done except Launch + Measure |
| Launched | In Progress | Launch → Done, Measure → In Progress |
| Iterating | In Progress | Iterate → In Progress, Measure → In Progress |
| Complete | Done | All Done |
| Killed | Canceled | All Canceled |

---

## Stage 0: MINE (Audience Signal Detection)

**Type:** Passive, always-on. Not triggered per-run — feeds INTO runs.

**Goal:** Detect recurring pain signals from Max's audience before they become explicit feature requests.

### Signal Sources
| Source | What to Watch | How |
|--------|--------------|-----|
| IG DMs & Comments | "Do you have...", "How do I...", "I wish..." | Periodic scan of recent DMs/comments |
| Skool Community | Repeated questions, help requests, frustration patterns | Monitor community posts |
| Newsletter replies | Direct responses expressing pain | Gmail scan |
| Course student questions | Where students get stuck repeatedly | Pattern analysis |
| X/Twitter mentions | Questions, complaints in Max's niche | `research.py --x-only` |

### Signal Scoring
A signal becomes an idea candidate when:
- **Frequency**: ≥3 people expressed the same pain independently
- **Specificity**: The pain is concrete, not vague ("I need a tool that does X" > "AI is confusing")
- **Audience fit**: The people expressing pain match Max's buyer profile
- **Monetization signal**: People are already paying for bad alternatives, or spending significant time on manual workarounds

### Output
When a signal crosses threshold:
- Structured signal brief posted to neo-ship-engine
- Includes: pain quotes (with sources), frequency count, audience fit assessment
- Ask Max: **[Ship It] [Park It] [Ignore]**
- "Park It" → goes to Idea Parking Lot (see below)

### Idea Parking Lot
Ideas that score 3.0-4.0 (EXPLORE) or get "Park It" from Max are stored in `skills/engine/parking-lot.md`:
- Idea name, original signal, date parked, reason
- **Revisit trigger**: Every 30 days, scan parking lot against new signals. If an idea accumulates 3+ new signals since parking, resurface to Max.
- Ideas that sit 90 days with no new signals → archive

---

## Stage 1: INTAKE

**Trigger:** Max posts idea (text, voice, image, link) OR Mine surfaces a signal Max approves.

**Automation:**
1. Parse input (transcribe audio via Whisper if needed)
2. Structure intake artifacts:
   - Product Brief (`templates/product-brief.md`)
   - Intake Interview Q&A (`templates/prompts/intake-interview.md`)
   - Research Kickoff Brief (`templates/prompts/intake-research-kickoff.md`)
3. **Assess risk level → assign track:**

| Signal | Sprint 🏃 | Standard 🚀 | Deep 🔬 |
|--------|-----------|-------------|---------|
| Audience already asking for it | ✅ | | |
| Clear comparable exists at higher price | ✅ | | |
| No prior audience signal | | ✅ | |
| Requires new tech or unfamiliar domain | | | ✅ |
| Investment > $200 | | | ✅ |
| Build time > 2 weeks | | | ✅ |
| Max's reputation at stake (public launch) | | | ✅ |

4. Create Linear parent issue + sub-issues (adjusted per track)
5. Post structured intake package to neo-ship-engine
6. Kick off deep research tasks from intake brief (research-first handoff)
7. Ask: "Validate this?" with inline buttons: **[Ship It] [Hold] [Park It] [Kill]**

**Sprint track skips:** Full research validation, Outbound, Nurture, Closing, Beta (these happen post-launch if traction emerges)
**Standard track:** Full pipeline as documented
**Deep track adds:** Customer interviews in Validate, extended Beta period

**If Max says Ship It → auto-advance to Stage 2**

---

## Stage 2: VALIDATE

**Philosophy:** Every verdict backed by real evidence. The depth of evidence matches the risk.

### Tiered Validation

#### Fast Validate (Sprint Track 🏃)
**Timeline: 2-4 hours**

For ideas where audience signal already exists. Goal: quantify demand with real behavior, not opinions. The core insight: **make people take an action** (click, sign up, reply) before you build anything.

##### Step 1: Messaging Test (1 hour)

Test whether the value prop resonates before even making a landing page.

**Execution:**
| Platform | Format | What to Post |
|----------|--------|-------------|
| IG Story | Poll or question sticker | "I'm thinking about building [thing that solves pain]. Would this help you?" + "Tell me about your experience with [problem]" |
| IG Post | Carousel or text post | Problem statement → "I'm building a solution" → "Comment [KEYWORD] if you want early access" |
| X/Twitter | Tweet or short thread | "Noticed a lot of [audience] struggle with [problem]. Thinking about building [solution]. Who deals with this?" |
| Skool | Discussion post | "Quick question — how do you currently handle [problem]? Researching this for something I'm working on." |
| Newsletter | Quick email | "Reply to this email if you struggle with [problem] — working on something for you." |

**What to measure:**
| Signal | Weak (fail) | Moderate | Strong (pass) |
|--------|------------|----------|---------------|
| IG Story responses | <5 replies | 5-15 replies | >15 replies |
| IG Post engagement | Below baseline | At baseline | 2x+ baseline saves/shares |
| Comment triggers | <5 "[KEYWORD]" | 5-15 | >15 |
| X engagement | <5 replies | 5-20 replies | >20 replies, quote tweets |
| Email replies | <3 | 3-10 | >10 replies |
| DMs received | 0 | 1-3 | >3 unsolicited DMs asking about it |

**Pass criteria:** At least ONE platform shows strong signal. Any unsolicited DM asking "when can I get this?" = instant pass.

##### Step 2: Fake Door Test (2 hours)

The most powerful pre-sell validation: make a landing page for a product that doesn't exist yet and see if people sign up.

**What "Fake Door" means:** The visitor sees a real product page with a real signup button. They don't know the product isn't built yet. Their willingness to enter their email (or even click "Buy Now") is the purest demand signal you can get.

**Landing Page Structure:**
```
┌─────────────────────────────────────────┐
│ HERO: Problem statement (from pain      │
│ quotes in messaging test or audience     │
│ signals). Not features — the PAIN.       │
│                                          │
│ "Stop wasting 3 hours every week on X"   │
├─────────────────────────────────────────┤
│ VALUE PROP: What this solves, in one     │
│ sentence. Use the audience's own words.  │
├─────────────────────────────────────────┤
│ HOW IT WORKS: 3 steps, dead simple.     │
│ 1. Do X  2. Get Y  3. Result Z          │
├─────────────────────────────────────────┤
│ SOCIAL PROOF: "Built by someone who      │
│ deals with this problem every day"       │
│ (Max's credibility, not fake reviews)    │
├─────────────────────────────────────────┤
│ CTA: [Get Early Access] or              │
│      [Join the Waitlist — It's Free]    │
│      or [Buy Now — $X/mo]              │
│                                          │
│ → Email capture form (MailerLite)        │
├─────────────────────────────────────────┤
│ FAQ: 3-4 real objections from            │
│ validation / audience signals            │
└─────────────────────────────────────────┘
```

**CTA Strategy (pick based on confidence):**
| Confidence Level | CTA | What It Validates |
|-----------------|-----|-------------------|
| Low (testing the waters) | "Join the Waitlist" | Interest: would they give an email? |
| Medium (audience signal exists) | "Get Early Access — $X (50% off launch price)" | Intent: would they commit at a price? |
| High (strong pain signal) | "Buy Now — $X/mo" → checkout page → "Coming soon, you'll be first to know" | Purchase intent: would they click buy? |

**The "coming soon" reveal:** If using a "Buy Now" CTA, the checkout page says: "We're putting the finishing touches on [product]. You're on the early access list — we'll email you the moment it's ready. No charge until then." This is honest (product IS coming) and captures the strongest intent signal.

**Deployment:**
- Use a template landing page (shadcn + Next.js, deployable in <30 min) or Carrd/Typedream for speed
- Domain: subdomain of [REDACTED_HANDLE].dev (`{product}.[REDACTED_HANDLE].dev`) or standalone if branding matters
- MailerLite form embedded for email capture
- GA4 installed for conversion tracking
- UTM links for every traffic source

**Traffic Generation (drive ≥100 visitors in 24 hours):**
| Source | Action | Expected Visitors |
|--------|--------|------------------|
| IG Story | "Link in bio" or direct link sticker → landing page | 30-50 |
| IG Post | CTA in caption → bio link | 20-40 |
| X/Twitter | Tweet with link | 10-30 |
| Skool | Post with link | 10-20 |
| Newsletter | Email blast to relevant segment | 20-50 |
| DM follow-ups | Send link to everyone who engaged in Step 1 | 10-20 |

**Metrics to capture:**
| Metric | How | Threshold |
|--------|-----|-----------|
| Unique visitors | GA4 | Need ≥100 for statistical relevance |
| Email signups | MailerLite | — |
| Conversion rate | Signups / Visitors | ≥5% = strong, 2-5% = moderate, <2% = weak |
| "Buy Now" clicks (if applicable) | GA4 event | Any clicks = extremely strong signal |
| Traffic source breakdown | UTM parameters | Which channel drove the most signups? |
| Time on page | GA4 | >30s = they read it; <10s = messaging missed |
| Scroll depth | GA4 | >50% = engaged; <25% = hero didn't hook them |

##### Step 3: Quick Competitive Scan (30 min)
- What exists? (direct competitors, adjacent tools, workarounds)
- What do they charge? (price anchoring for Strategy)
- Where are the gaps? (what do reviews complain about?)
- What's the moat? (see Competitive Moat section below)

##### Fast Validate Decision
| Result | Messaging Test | Fake Door | Decision |
|--------|---------------|-----------|----------|
| 🟢 Strong | Strong signal on ≥1 platform | ≥5% conversion, ≥100 visitors | **SHIP** — proceed to Strategy |
| 🟡 Mixed | Moderate signal | 2-5% conversion | **Iterate messaging** — try different angle, re-test |
| 🔴 Weak | Below baseline everywhere | <2% conversion | **KILL or PARK** — demand isn't there (yet) |
| 🔥 On fire | DMs flooding in | >10% conversion or "Buy Now" clicks | **SHIP FAST** — sprint track, build this weekend |

**Output:** Fast Validation Brief:
```markdown
## Fast Validation: {Product Name}
**Date:** {date}
**Track:** Sprint 🏃

### Messaging Test Results
| Platform | Metric | Result | vs Baseline |
|----------|--------|--------|-------------|
| IG Story | Replies | {N} | {X}x |
| IG Post | Saves/Shares | {N} | {X}x |
| X | Replies | {N} | — |
| DMs received | Count | {N} | — |

**Strongest signal:** {what and where}
**Best quotes:** "{quote}" / "{quote}"

### Fake Door Results
- **Landing page URL:** {url}
- **Visitors:** {N} (over {X} hours)
- **Signups:** {N}
- **Conversion rate:** {X}%
- **Top traffic source:** {channel} ({N} visitors, {X}% conversion)
- **Buy Now clicks:** {N} (if applicable)
- **Avg time on page:** {X}s
- **Scroll depth >50%:** {X}%

### Competitive Landscape
| Competitor | Price | Gap |
|-----------|-------|-----|
| {name} | ${X}/mo | {weakness} |

### Moat: {type} — {description}

### Verdict: {SHIP 🟢 / ITERATE 🟡 / PARK 🅿️ / KILL 🔴}
**Reasoning:** {1-2 sentences backed by data}
```

#### Standard Validate (Standard Track 🚀)
**Timeline: 1-2 days**

Full desk research. Same as previous spec with these additions:

##### Level 1: Pain Discovery
| Action | Tool | What to find |
|--------|------|-------------|
| Reddit pain threads | `web_search "reddit {problem}"` + `web_fetch` | Threads, upvotes, quotes, sentiment |
| X/Twitter complaints | `research.py "{problem}" --x-only` | "I wish...", "why is there no...", complaint count |
| Forum mining | `web_search "indiehackers\|hackernews {problem}"` + `web_fetch` | Real user quotes, thread counts |
| App store reviews | `web_fetch` G2/Capterra/App Store pages | 1-2 star reviews, top complaints |

##### Level 2: Demand Quantification
| Action | Tool | What to find |
|--------|------|-------------|
| Google Trends | `web_search "{keyword} google trends"` | Growing/stable/declining, seasonality |
| Keyword volume | `research.py "{solution} search volume demand"` | Monthly searches, CPC (= commercial intent) |
| Competitor traffic | `web_search "{competitor} traffic similarweb"` | Est. monthly visits, pricing pages |
| Open-source alternatives | `web_search "github {solution}"` | Stars, issues = demand signal |

##### Level 3: Willingness to Pay
| Action | Tool | What to find |
|--------|------|-------------|
| Payment evidence | `web_search` + `web_fetch` | Threads where people pay for bad alternatives |
| Workaround analysis | `web_search "how to {solve problem} manually"` | DIY solutions, their pain points |
| Price anchoring | `web_fetch` competitor pricing pages | Price range, tier structure |

##### Level 4: Audience-Market Fit
- Does Max's audience (Spanish tech/AI/coding entrepreneurs) have this pain?
- Can Max credibly sell this? Authority check
- Can IG + newsletter + Skool reach buyers directly?
- Can Max make 5+ content pieces about this problem?
- Better in Spanish (less competition) or English (bigger TAM)?

##### Level 5: Messaging Test
**NEW — test positioning before building.**
- Craft the one-liner value prop
- Post on IG (story poll or carousel) and X
- Measure resonance: saves, shares, DMs, engagement vs baseline
- If engagement is 2x+ baseline → strong signal
- If flat → positioning needs work (iterate before building)

##### Level 6: Competitive Moat Analysis
**NEW — what's the defensible advantage?**

| Moat Type | Applies When | Example |
|-----------|-------------|---------|
| **Audience moat** | Max's followers ARE the target market | "Built by someone who teaches this daily" |
| **Content moat** | Max can create better educational content around it | Tutorials, use cases, behind-the-scenes |
| **Speed moat** | First to market in a niche (especially Spanish-speaking) | "Only tool in Spanish for X" |
| **Integration moat** | Ties into Max's existing ecosystem (course, community) | Skool members get it bundled |
| **Data moat** | Gets smarter with usage | User-generated templates, community knowledge |

**Question to answer:** "If someone copied this product tomorrow, why would customers still choose Max's version?"

If the answer is only "they wouldn't" → flag as high-risk in the score card.

##### Score Card
| Signal | Weight | Scoring Guide |
|--------|--------|---------------|
| Pain frequency | 20% | 1=no threads, 3=monthly threads, 5=weekly threads with 100+ upvotes |
| Willingness to pay | 20% | 1=no evidence, 3=people use free workarounds, 5=people paying $50+/mo for bad alternatives |
| Competition gap | 15% | 1=saturated, 3=exists but poor UX, 5=nothing exists for this niche |
| Audience fit | 20% | 1=no overlap, 3=adjacent, 5=Max's audience IS the target user |
| Build feasibility | 10% | 1=months, 3=weeks, 5=weekend |
| Moat strength | 15% | 1=no defensibility, 3=audience/content moat, 5=multi-layer moat |

- **> 4.0** → SHIP 🟢
- **3.0-4.0** → EXPLORE 🟡 (park it, flag risks, suggest de-risking steps)
- **< 3.0** → KILL 🔴 (with data, note revisit conditions)

**Output:** Validation Report (see `templates/validation-report.md`)
**Post to neo-ship-engine.** 🔒 **Max approves, explores, or kills.**

#### Deep Validate (Deep Track 🔬)
**Timeline: 3-5 days**

Everything in Standard PLUS customer interviews. This is for high-risk ideas where desk research isn't enough — you need to hear real people describe the problem in their own words.

##### Customer Interviews (5-10 conversations)

**Why:** Reddit threads tell you people complain. Interviews tell you what they'd actually pay to fix, how they currently solve it, and what words they use to describe the pain (which becomes your marketing copy).

###### Recruitment (Day 1)
Target: 10-15 outreach messages to get 5-10 interviews.

| Source | How to Recruit | Expected Response Rate |
|--------|---------------|----------------------|
| **IG engaged followers** | DM people who liked/saved pain-related content: "Hey, I'm researching [problem area]. Would you be down for a 15-min chat? I'll give you early access to what I build." | 20-30% |
| **Skool members** | Post in community: "Working on something for [problem]. Looking for 5 people to chat with — DM me if you deal with this." | 30-40% |
| **Newsletter subscribers** | Quick email: "Reply to this if you struggle with [problem] — I want to hear your story." | 5-10% |
| **X/Reddit commenters** | DM people who posted about the pain in public threads | 10-15% |
| **Warm referrals** | Ask first 2 interviewees: "Know anyone else who deals with this?" | 40-50% |

**Scheduling:** Calendly link with 15-min slots. Or just DM back and forth. Don't over-formalize.

###### Interview Execution (Days 2-4)
**Format:** Video call (Zoom/Google Meet), voice call, or async voice messages. Whatever the person prefers. Record if they consent.

**The Script** (see full version at `templates/customer-interview.md`):

| Phase | Duration | Questions | Purpose |
|-------|----------|-----------|---------|
| **Warm-up** | 2 min | "What do you do? How does [problem area] come up in your work?" | Context, build rapport |
| **Current behavior** | 8 min | "Walk me through the last time you dealt with [problem]. Step by step." / "What did you try first?" / "How long did that take?" / "What tools did you use?" | Understand the real workflow, not the idealized one |
| **Pain depth** | 5 min | "What's the most frustrating part?" / "What does this cost you — time, money, missed opportunities?" / "Have you tried to solve this before? What happened?" | Quantify the pain, find the emotional core |
| **Willingness to pay** | 3 min | "Have you ever paid for something to help with this?" / "If something solved [specific pain they described], what would that be worth to you?" / "What would you compare it to price-wise?" | Real price anchoring from their perspective |
| **Close** | 2 min | "If I build something for this, would you want early access?" (Note: polite "sure" = weak signal. "When can I get it?" = 🔥) | Gauge real intent |

**Critical anti-patterns:**
- ❌ NEVER describe your solution before hearing their problem
- ❌ NEVER ask "Would you use X?" (100% say yes, 5% actually would)
- ❌ NEVER lead with "Don't you think it would be better if..."
- ❌ NEVER argue with their preferences or workflow
- ❌ NEVER pitch during the interview — this is research, not sales
- ✅ DO shut up and let them talk. Silence is your friend.
- ✅ DO ask "Tell me more about that" when they mention something interesting
- ✅ DO write down their exact words — these become marketing copy

###### Documentation (Per Interview)
```markdown
## Interview: {Name} — {Date}
**Role/Context:** {what they do, how they relate to the problem}
**Channel:** {video call / voice / async}

### Current Behavior
- {Step-by-step of how they currently handle the problem}
- {Tools they use, time spent, frequency}

### Pain Quotes (Verbatim)
- "{Exact quote}" — on {topic}
- "{Exact quote}" — on {topic}

### Willingness to Pay
- Currently pays: {what they pay for, how much}
- Stated value: "{what they said}" → ${X}/mo estimated
- Enthusiasm level: {1-5, where 5 = "when can I get it?"}

### Activation Signal
- {Did they ask when it would be ready? Did they offer to beta test? Did they refer someone?}

### Surprising Insights
- {Anything unexpected that challenges assumptions}
```

###### Pattern Synthesis (Day 4-5)
After all interviews, create the synthesis:

```markdown
## Interview Synthesis: {Idea Name}
**Interviews completed:** {N} of {N} planned
**Date range:** {start} → {end}

### Common Patterns (≥3 people independently)
1. {Pattern}: {N} people described this
   - "{Quote}" — {Person A}
   - "{Quote}" — {Person B}
   - "{Quote}" — {Person C}

2. {Pattern}: {N} people described this
   - ...

### Top 5 Pain Quotes (for marketing copy)
1. "{Quote}" — {Context}
2. "{Quote}" — {Context}
3. "{Quote}" — {Context}
4. "{Quote}" — {Context}
5. "{Quote}" — {Context}

### Current Workflows (how people solve it today)
| Approach | # People | Tools Used | Time Spent | Pain Level |
|----------|----------|-----------|------------|------------|
| {approach} | {N} | {tools} | {time} | {1-5} |

### Willingness to Pay
| Person | Currently Pays | Stated Value | Enthusiasm |
|--------|---------------|-------------|------------|
| {name} | {what/how much} | ${X}/mo | {1-5} |
**Median stated value:** ${X}/mo
**Median enthusiasm:** {X}/5

### Surprising Insights
- {Things that challenge the original hypothesis}

### Demand Confidence: {HIGH / MEDIUM / LOW}
**Reasoning:** {1-2 sentences}

### Recommendation
- {SHIP / EXPLORE / KILL with specific reasoning from interview data}
- {If SHIP: which pain quotes to use in marketing, what feature to build first}
- {If KILL: what specifically killed it, conditions for revisit}
```

**Output:** Deep Validation Report (Standard report + interview synthesis + direct quotes + pattern analysis)

---

## Stage 3: STRATEGY

**Automation:**
1. **Positioning** — one-liner, tagline, value prop (based on validation pain quotes)
2. **Monetization** — model + price point (anchored against competitor pricing from validation)
3. **MVP scope** — ruthless minimum:

### MVP Definition Framework
| Level | What It Is | When to Use |
|-------|-----------|-------------|
| **Landing page only** | Describes the product, captures emails, no product | Unproven demand, testing positioning |
| **Concierge MVP** | Max manually delivers the value, no automation | High-touch, need to understand the job deeply |
| **Wizard of Oz** | Looks automated to the user, Max/Neo does it behind the scenes | Test the experience before building the tech |
| **Single-feature MVP** | One core feature, nothing else | Validated demand, clear value prop |
| **Full MVP** | Core feature + onboarding + payment | High confidence from Deep validation |

**Default to the lightest option.** Only go heavier if validation data supports it.

4. **Distribution channels** — ALL of them, prioritized by expected ROI.

### Channel Priority Framework

Every channel gets worked. But effort is allocated by tier — primary channels get deeper execution, tertiary channels get automated baseline.

| Channel | Max's Advantage | Tier Criteria |
|---------|----------------|---------------|
| **IG (organic)** | 3.5K followers, proven engagement | Primary if product is visual/demo-able |
| **SEO / Blog** | Existing site with authority | Primary if problem is searchable |
| **Newsletter** | Existing list (growing) | Always Tier 1 — direct access to warm audience |
| **Skool community** | 35 members, direct access | Always Tier 1 — built-in beta testers + buyers |
| **X/Twitter** | Growing presence | Primary if target = English-speaking devs |
| **Reddit / Communities** | Credibility in niche spaces | Tier 1-2 depending on subreddit activity |
| **Cold outreach** | Toptal credibility, enterprise background | Primary if B2B / high-ticket |
| **Product Hunt** | One-time launch event | Always included for launch day |
| **Paid ads (Meta/Google)** | Meta API integrated, retargeting ready | Tier 2-3, activated post-launch if organic shows signal |

**Tier allocation:**
- **Tier 1 (Primary):** Deep execution — custom content, active engagement, dedicated sub-agent
- **Tier 2 (Secondary):** Solid execution — adapted content, scheduled posting, monitoring
- **Tier 3 (Tertiary):** Automated baseline — cross-posted content, minimal customization

Each channel gets its own sub-agent running in parallel. The engine doesn't choose channels — it prioritizes effort across ALL of them.

5. **Success targets** — 7-day and 30-day measurable goals (specific numbers, not "growth")
6. **Timeline** — milestones with dates → calendar events created
7. **Budget** — domains, APIs, ad spend, tools. Total estimated cost.
8. **Growth loops** — how does usage generate more users? (see Growth Loops section)

### Growth Loop Design
**NEW — designed into the product, not bolted on after.**

| Loop Type | How It Works | Example |
|-----------|-------------|---------|
| **Content loop** | Using product → generates shareable content → attracts new users | "Built with [tool]" watermark, shareable reports |
| **Referral loop** | Happy user → invites others → both get value | "Invite 3 friends, unlock premium feature" |
| **SEO loop** | User-generated content → indexed → attracts searchers | Public profiles, templates, galleries |
| **Community loop** | Users help each other → reduces support → increases retention | Forum, Discord, shared templates |
| **Embed loop** | Product appears on other sites → drives traffic back | Widgets, badges, "powered by" links |

**Strategy must identify at least ONE growth loop** for the product. If none exist naturally, that's a moat weakness (flag in validation).

**Output:** Ship Plan (see `templates/ship-plan.md`) → Linear comment
**Auto-advance to parallel stages**

---

## Stage 4: BUILD (Delegated)

**Owner:** Builder sub-agent. Ship Engine monitors, doesn't own tech.

1. Create GitHub repo: `gh repo create [REDACTED_HANDLE]/{name} --private`
2. Spawn builder via `sessions_spawn`:
   ```
   Task: Build MVP for {name}.
   Spec: {mvp_scope from ship plan}
   Tech: Opinionated stack (Next.js 15, pnpm, shadcn/ui, Vercel)
   Repo: [REDACTED_HANDLE]/{name}
   Growth loop: {loop from strategy — build it in from day 1}
   Done when: Deployed to Vercel, core feature working, GA4 tracking installed.
   ```
3. Track via `sessions_list` / `sessions_history`
4. Ship Engine provides: copy, assets, domain config, API keys as needed

**Includes by default:**
- Privacy policy + Terms of Service (minimal, template-based)
- Cookie consent (if applicable)
- GA4 tracking with conversion events
- Growth loop mechanics built into the product

**Tools:** `coding-agent`, `github`, `sessions_spawn`

---

## Stage 5: MARKETING

**Goal:** All marketing assets ready for the **primary distribution channel** before launch day.

**Every channel gets assets.** Sub-agents produce channel-specific content in parallel. Tier 1 channels get custom content; Tier 2-3 get adapted versions.

### 5.1 Landing Page (Always)
| Task | Details |
|------|---------|
| Hero copy (problem-first, not feature-first) | From validation pain quotes |
| Social proof section | Beta tester quotes (from Beta stage), or "Built by someone with this exact problem" |
| Demo video/GIF | Core flow in 15 seconds |
| FAQ from validation pain threads | Real objections, real answers |
| SEO: meta title, description, keywords | From validation keyword data |

### 5.2 Visual Assets
| Asset | Spec |
|-------|------|
| OG image | 1200x630, product mockup style |
| Logo/icon | Brand-consistent, simple |
| IG assets | Carousel frames (1080x1350), story (1080x1920), reel cover |
| X/Twitter assets | Header image, thread visuals |
| Blog hero | 1200x630 |
| Screenshots | Once build is live |
| Demo GIF | Core flow in 15 sec |
| Product Hunt assets | Gallery images (1270x760), logo, tagline |

### 5.3 Content Per Channel (All Channels, Parallel)

Each channel gets a dedicated content package produced by its own sub-agent:

**IG:**
| Piece | Format |
|-------|--------|
| Launch carousel or reel | Hook → demo → CTA |
| D-3 teaser story | "Building something..." |
| D-1 sneak peek | Screenshot + countdown |
| D+1 tutorial reel | How to use it in 60s |
| D+7 lessons learned | Carousel |

**X/Twitter:**
| Piece | Format |
|-------|--------|
| Launch thread | 5-7 tweets: problem → solution → demo → CTA |
| Build-in-public thread | Journey thread during build |
| D+3 early results thread | Numbers + user quotes |

**SEO/Blog:**
| Piece | Format |
|-------|--------|
| Pain keyword article | Problem → solution → CTA |
| Comparison article | "X vs Y vs [our product]" |
| Tutorial article | Step-by-step guide |

**Newsletter:**
| Piece | Format |
|-------|--------|
| Teaser email | "I'm building something for [pain]" |
| Launch email | Full announcement + CTA |
| Tutorial email | How to get first value |

**Reddit / Communities:**
| Piece | Format |
|-------|--------|
| Value post per community | Genuinely helpful, product mentioned naturally |
| Show HN / Launch post | For HackerNews if applicable |

**Product Hunt:**
| Piece | Format |
|-------|--------|
| Listing | Tagline, description, gallery, maker comment |

### 5.4 Content-Product Flywheel Design
**NEW — ongoing content, not just launch burst.**

Plan the first 30 days of content post-launch:
| Content Type | Frequency | Purpose |
|-------------|-----------|---------|
| User stories | Weekly | Social proof, shows real usage |
| Tips & tricks | 2x/week | Drive activation, show depth |
| Behind-the-scenes | Weekly | Authenticity, build connection |
| Results/metrics | Bi-weekly | Credibility, attract similar users |
| Community highlights | Weekly (if community exists) | Retention, belonging |

The flywheel: product usage → generates content → content drives signups → more usage → more content.

**Output:** Marketing Kit (see `templates/marketing-kit.md`)

---

## Stage 6: OUTBOUND

**Goal:** Put the solution in front of people who have the pain — across ALL channels simultaneously. Each channel gets its own sub-agent.

### All Channels Run in Parallel

Each outbound channel is a sub-agent with a clear playbook. They run concurrently. Tier determines depth of execution.

#### Community Engagement (Reddit, forums, Discord, Skool groups)
| Action | Details |
|--------|---------|
| Find 5-10 communities | Subreddits, Discord servers, Skool groups, FB groups |
| Map rules per community | What's allowed? Self-promo policy? |
| Provide genuine value first | Answer questions, share insights, be helpful for 1-2 weeks before mentioning product |
| Soft launch in community | "I built this to solve [problem]. Happy to give early access to anyone here." |
| Track engagement per community | Clicks, signups, conversations |

#### X/Twitter Engagement
| Action | Details |
|--------|---------|
| Find pain tweets | Complaints, wishes, frustrations in the niche |
| Engage authentically | Value-first replies, not product pitches |
| Build in public thread | Share the building journey, attract followers with similar pain |
| DM high-intent users | For people who explicitly expressed the pain |

#### Cold Outreach (scales with ticket value)
| Action | Details |
|--------|---------|
| Lead list: 20-50 targeted people | From competitor reviews, job boards, relevant forums |
| 3-email sequence | Value → story → ask. Via Gmail. |
| Track opens, replies, conversions | Per-lead attribution |

#### Influencer/Creator Seeding
| Action | Details |
|--------|---------|
| 5-10 micro-influencers (1K-50K) | In the exact niche |
| Free access + personal note | "Built this for people like your audience. Thoughts?" |
| Track responses | Follow up at day 3 and 7 |

#### Product Hunt Launch
| Action | Details |
|--------|---------|
| Schedule for launch day | 00:01 PST |
| Maker comment prepared | Authentic story, not marketing copy |
| Activate network for upvotes | Newsletter, IG story, X post pointing to PH |

**Output:** Outbound Playbook (see `templates/outbound-playbook.md`) — all channels with per-channel metrics.

---

## Stage 7: LEAD CAPTURE

**Goal:** Turn attention into contacts. Every eyeball hits a capture mechanism.

### 7.1 Funnels Per Channel (All Tracked)
Every channel gets its own funnel with UTM tracking. All funnels converge on the same landing page.

| Channel | Funnel | UTM |
|---------|--------|-----|
| IG | Reel/carousel → bio link → landing page → email capture | `utm_source=instagram&utm_medium=social` |
| SEO | Pain keyword article → in-content CTA → landing page → email capture | `utm_source=google&utm_medium=organic` |
| Newsletter | Email → landing page → signup/purchase | `utm_source=newsletter&utm_medium=email` |
| Reddit/Communities | Value post → profile/bio → landing page → email capture | `utm_source={community}&utm_medium=community` |
| X | Thread → last tweet CTA → landing page → email capture | `utm_source=twitter&utm_medium=social` |
| Cold email | Email CTA → landing page → email capture | `utm_source=email&utm_medium=cold` |
| Product Hunt | Listing → landing page → email capture | `utm_source=producthunt&utm_medium=launch` |
| Influencers | Creator post/mention → landing page → email capture | `utm_source={creator}&utm_medium=influencer` |

Every funnel tracked independently → Measure stage knows exactly which channels convert.

### 7.2 Lead Magnets (pick one)
| Type | Best When |
|------|-----------|
| Free tier | Product has clear free/paid line |
| Template/resource | Adjacent to the pain, quick win |
| Waitlist + early bird pricing | Pre-launch or limited capacity |
| Free trial | SaaS with activation metric |
| Mini-course | Educational product funnel |

### 7.3 Email Capture Setup
- Create MailerLite group for product
- Create signup form
- Embed on landing page
- Test end-to-end (submit → receive welcome email)

### 7.4 Analytics
- GA4 conversion events: signup, activation, purchase
- UTM tracking for primary channel
- Funnel from landing page → signup → activation → revenue

**Output:** Lead Capture Setup doc (see `templates/lead-capture.md`)

---

## Stage 8: NURTURE

**Goal:** Warm leads from "interested" to "ready to buy" through automated sequences.

### Email Sequence (5-7 emails, 14 days)
| Day | Email | Purpose |
|-----|-------|---------|
| 0 | Welcome | Deliver lead magnet, set expectations |
| 1 | Story | "Why I built {name}" — connect emotionally |
| 3 | Quick win | "Get your first result in 5 min" — drive activation |
| 5 | Social proof | Beta tester quote or early result |
| 7 | Objection killer | Handle #1 objection from validation data |
| 10 | Urgency | Early bird pricing / limited offer |
| 14 | Last call | Final push, clean list |

### Content Drip (aligned to primary channel)
| Content | Timing | Purpose |
|---------|--------|---------|
| Building journey | During build | FOMO + authenticity |
| Value drops | 2-3x/week | Authority building |
| Community participation | Ongoing | Become the known expert |

**Output:** Nurture Sequence doc (see `templates/nurture-sequence.md`)

---

## Stage 9: CLOSING

**Goal:** Convert warm leads into paying customers.

### 9.1 Pricing Strategy
| Decision | Source |
|----------|--------|
| Model (free/freemium/paid/subscription) | Strategy stage |
| Price point | Anchored vs competitors (from Validation) |
| Launch pricing | Default: 50% off first 50 customers |
| Guarantee | Default: 30-day money-back |

### 9.2 Pricing Validation
**NEW — test before committing.**
- If Beta stage is running: ask 3-5 beta users "What would you pay for this?"
- Compare their answer vs Strategy's price point
- If delta > 2x in either direction → revisit pricing

### 9.3 Payment Setup
- Stripe product + prices
- Checkout flow (hosted Stripe or in-app)
- Webhook for fulfillment
- Revenue tracking

### 9.4 Objection Handling
| Objection | Response | Where |
|-----------|----------|-------|
| "Too expensive" | ROI calculator or comparison to time spent on workaround | Landing page, email |
| "I can build this myself" | Time cost analysis | FAQ |
| "What if it doesn't work" | Money-back guarantee + beta testimonials | Pricing page |
| "I'll do it later" | Early bird expiration | Email sequence |

### 9.5 Post-Purchase Flow
| Action | Timing |
|--------|--------|
| Onboarding email (first value in <5 min) | Immediate |
| Check-in: "How's it going?" | Day 3 |
| Ask for testimonial | Day 7 |
| Referral program prompt | Day 14 |

**Output:** Closing Strategy doc (see `templates/closing-strategy.md`)

---

## Stage 10: BETA (New)

**Goal:** Real users using the real product before public launch. Fix critical issues, collect testimonials, validate pricing.

### Beta Recruitment
| Source | How | Target |
|--------|-----|--------|
| Skool community | Post: "Building [tool] — looking for 10 beta testers" | 5-10 people |
| Newsletter subscribers | Email: "Early access to [tool] — your feedback shapes it" | 5-10 people |
| IG engaged followers | DM people who engaged with teaser content | 3-5 people |
| Validation interviewees | "Remember that problem we discussed? I built something." | Anyone from Deep validation |

**Target: 10-20 beta users minimum.**

### Beta Protocol
| Day | Action |
|-----|--------|
| 0 | Invite beta users, provide access + quick start guide |
| 1 | Check: did they activate? (reached first value moment) |
| 3 | Async check-in: "What's working? What's broken?" |
| 7 | Structured feedback form: NPS, feature requests, pricing willingness |
| 7+ | Fix critical bugs, implement top feedback |

### Beta Outputs
- **Bug list** with severity and fix status
- **Feature request list** (prioritized)
- **Testimonial quotes** (for Marketing and Landing page)
- **Pricing validation** (what would they pay? see Closing 9.2)
- **Activation rate** (% who reached first value moment)
- **NPS score** (detractors are kill signals, promoters are launch fuel)

### Beta → Launch Gate
| Metric | Must Pass |
|--------|-----------|
| Critical bugs | 0 open |
| Activation rate | ≥50% of beta users reached first value |
| NPS | ≥7 average (or qualitative equivalent) |
| At least 3 usable testimonials | Real quotes from real users |

**Sprint track:** Beta is optional. If audience signal is extremely strong and product is simple (template, resource, micro-tool), go straight to Launch.

---

## Stage 11: LAUNCH

**🔒 HARD GATE: Max must approve.**

### Pre-Launch Checklist
| Category | Check |
|----------|-------|
| Product | URL live, core feature works, mobile responsive |
| Analytics | GA4 events firing, UTMs working |
| Legal | Privacy policy, terms of service, cookie consent |
| Marketing | OG tags, share preview, primary channel assets ready |
| Email | Welcome sequence active, form working |
| Payment | Checkout working, webhook verified |
| Content | D0 posts drafted |
| Outbound | Primary channel outreach ready |
| Beta | All critical bugs fixed, testimonials collected |
| Support | Help/FAQ page live, support email/channel configured (see Ops) |

### Launch Execution (all channels, orchestrated)
| Action | Timing |
|--------|--------|
| Product Hunt listing live | D0 00:01 PST |
| IG launch post (carousel/reel) | D0 morning |
| X/Twitter launch thread | D0 morning |
| Newsletter launch email | D0 morning |
| Reddit / community posts | D0 staggered throughout day |
| Influencer DMs with live link | D0 |
| Cold email sequence activated | D0 |
| Activate paid ads (if budget approved) | D0 |
| Monitor real-time (GA4, Stripe, email signups, PH) | D0 all day |
| Respond to comments/questions across all platforms | D0-D3 |
| Post to neo-events | D0 |

### Post-Launch Content (from Marketing flywheel plan)
| Day | Action |
|-----|--------|
| D+1 | Tutorial on primary channel |
| D+3 | Early results or user story |
| D+7 | Lessons learned / behind-the-scenes |

**Output:** Launch Checklist (see `templates/launch-checklist.md`)

---

## Stage 12: MEASURE

**Automated via cron (daily for 7 days, weekly for 30 days, monthly after).**

### Metrics Dashboard
| Category | Metric | Source |
|----------|--------|--------|
| Traffic | Visitors, sources, UTM breakdown | GA4 |
| Conversion | Signups, signup rate by channel | GA4 + email provider |
| Activation | Users reaching first value moment | GA4 events |
| Revenue | MRR, transactions, ARPU | Stripe |
| Engagement | Email open/click rates | MailerLite |
| Social | Post reach, engagement per channel | Platform analytics (IG, X, Reddit, PH) |
| Retention | Day 1/7/30 return rate | GA4 |

### Decision Framework
| Score vs Targets | Verdict | Action |
|---|---|---|
| >80% of targets | **DOUBLE DOWN** 🟢 | → Iterate: scale channels, add features |
| 40-80% | **ITERATE** 🟡 | → Iterate: A/B test positioning, fix funnel leaks |
| 10-40% | **PIVOT** 🟠 | → Iterate: change channel, reposition, simplify |
| <10% after 30 days | **KILL** 🔴 | Kill process (see below) |

### Kill Decision Framework
**NEW — metrics aren't the only signal.**

Before killing, also consider:
| Factor | Kill Signal | Continue Signal |
|--------|------------|----------------|
| **Metrics** | <10% of targets after 30 days | Any positive trend, even if below targets |
| **Qualitative** | Users sign up but never come back | Users love it but few know about it (distribution problem, not product problem) |
| **Effort** | Requires >10 hours/week to maintain | Runs itself after initial setup |
| **Opportunity cost** | Blocking better ideas in the pipeline | Nothing better in the parking lot |
| **Max's energy** | Max lost interest, doesn't want to talk about it | Max keeps bringing it up, uses it himself |

**Pivot vs Kill:** If the PRODUCT has signal but the CHANNEL doesn't, pivot the channel first. Only kill if the core value prop isn't resonating.

### Measure Reports
| Report | Timing | Destination |
|--------|--------|-------------|
| Daily snapshot | Days 1-7 | Repo `docs/post-launch/` |
| 7-day report | D+7 | Linear parent comment |
| 30-day report | D+30 | Linear parent comment |
| Kill/Continue/Iterate decision | D+30 | Linear parent comment, 🔒 Max decides |

---

## Stage 13: ITERATE (New)

**Goal:** Improve the product based on real usage data until it hits PMF or gets killed. This is where most products actually succeed — not on launch day, but through disciplined iteration afterward.

**Why this stage exists:** The old engine treated launch as the finish line. In reality, v1 almost never nails product-market fit. The iteration loop is where you find PMF by systematically fixing the biggest leak in the funnel, measuring the impact, and repeating.

### The Iteration Loop
```
┌─→ DIAGNOSE: What's the #1 problem? (Measure data)
│       ↓
│   HYPOTHESIZE: "If we change X, metric Y improves by Z%"
│       ↓
│   BUILD: Smallest possible change to test this
│       ↓
│   MEASURE: Wait for data (3-7 days minimum)
│       ↓
│   DECIDE: Keep? Revert? Pivot?
│       ↓
│   ┌─ Improvement → back to DIAGNOSE (next problem) ↑
│   ├─ No change → try different hypothesis ↑
│   └─ 3 fails in a row → evaluate: pivot or kill
└─────────────────────────────────────────────────────┘
```

### The Pirate Metrics Funnel (Priority Order)

Fix from top to bottom. No point optimizing revenue if nobody's activating.

```
AWARENESS → ACQUISITION → ACTIVATION → RETENTION → REVENUE → REFERRAL
    ↓            ↓            ↓            ↓          ↓          ↓
  "Do they    "Do they     "Do they     "Do they   "Do they   "Do they
   know we    visit/       get first    come        pay?"     tell
   exist?"    sign up?"    value?"      back?"                others?"
```

| Level | Key Question | Metrics to Watch | Common Fixes |
|-------|-------------|-----------------|-------------|
| **1. Activation** | Do users reach "first value" within 5 minutes? | Activation rate, time-to-value, drop-off step | Simplify onboarding, remove steps, add guidance, change the "aha moment" |
| **2. Retention** | Do users come back after day 1? Day 7? Day 30? | D1/D7/D30 retention curves, session frequency | Fix core loop, add notifications/reminders, improve the daily use case |
| **3. Acquisition** | Are visitors converting to signups? | Visitor→signup rate per channel, bounce rate, time on landing page | Rewrite hero copy (use customer interview quotes), fix CTA, improve social proof, A/B test headlines |
| **4. Revenue** | Are free users converting to paid? | Free→paid rate, trial→paid rate, ARPU, churn | Adjust pricing, improve upgrade prompts, add feature gating, offer annual discount |
| **5. Referral** | Are users bringing other users? | Referral rate, viral coefficient, NPS | Add share features, referral incentives, "powered by" branding, invite flows |
| **6. Awareness** | Do enough people know this exists? | Traffic volume, impressions, brand mentions | Scale channels that work (from Measure data), try new channels, content marketing |

**Rule: Only work on ONE level per iteration.** Fix the biggest leak first.

### Iteration Sprint Protocol

Each iteration is a focused mini-sprint. The engine manages these autonomously.

#### Step 1: Diagnose (1 day max)
**Input:** Measure stage data (daily/weekly reports)

The engine analyzes the funnel and identifies the single biggest leak:

```markdown
## Iteration Diagnosis: {Product Name} — Sprint #{N}
**Date:** {date}
**Days since launch:** {N}

### Funnel Analysis
| Stage | Current | Target | Gap | Status |
|-------|---------|--------|-----|--------|
| Awareness (visitors/week) | {N} | {target} | {-N%} | 🟢/🟡/🔴 |
| Acquisition (signups/week) | {N} | {target} | {-N%} | 🟢/🟡/🔴 |
| Activation (% first value) | {N}% | {target}% | {-N%} | 🟢/🟡/🔴 |
| Retention (D7 return) | {N}% | {target}% | {-N%} | 🟢/🟡/🔴 |
| Revenue (MRR) | ${N} | ${target} | {-N%} | 🟢/🟡/🔴 |
| Referral (viral coeff) | {N} | {target} | {-N} | 🟢/🟡/🔴 |

### Biggest Leak: {LEVEL}
**Why:** {explanation with data — e.g., "200 visitors but only 4 signups (2%) — landing page isn't converting"}

### Supporting Data
- {Specific data point}
- {User feedback if available}
- {Comparison to benchmarks}
```

#### Step 2: Hypothesize (1 hour)
Write a specific, testable hypothesis:

**Format:** "If we [specific change], then [metric] will improve from [current] to [target] because [reasoning]."

**Good hypotheses:**
- "If we rewrite the hero to use customer quote 'I waste 3 hours every week on X', then landing page conversion will improve from 2% to 5% because it matches the exact language our audience uses."
- "If we add a 3-step onboarding wizard, activation rate will improve from 30% to 60% because users currently don't know what to do first."
- "If we add a 'Share your results' button, referral rate will improve from 0% to 5% because the output is inherently shareable."

**Bad hypotheses:**
- ❌ "If we improve the product, more people will use it" (not specific)
- ❌ "If we redesign everything, it'll be better" (too big)
- ❌ "If we add 5 new features, retention will improve" (not minimal)

**One hypothesis per sprint. One change at a time.** Otherwise you can't attribute results.

#### Step 3: Build (1-3 days)
Spawn a sub-agent for the specific change:
- Smallest possible implementation that tests the hypothesis
- Deploy to production (not a staging branch that sits there)
- Ensure tracking is in place to measure the specific metric

**Common iteration builds:**
| Hypothesis Area | Typical Change | Build Time |
|----------------|---------------|------------|
| Landing page copy | Rewrite hero, change CTA text | 2 hours |
| Onboarding flow | Add/remove steps, change order | 1 day |
| Pricing page | New tiers, different pricing, new copy | 4 hours |
| Growth loop | Add share button, referral system | 1-2 days |
| Email sequence | Rewrite subject lines, change timing | 2 hours |
| Feature gating | Move features behind paywall | 4 hours |
| Notification/reminder | Add email/push reminders for retention | 1 day |

#### Step 4: Measure (3-7 days)
**Minimum measurement period:** 3 days (for high-traffic products) to 7 days (for lower traffic).

**What to track:**
- The specific metric from the hypothesis
- Any secondary metrics that might be affected (positive or negative)
- Sample size: need ≥100 events to draw conclusions (e.g., ≥100 landing page visitors to measure conversion change)

**If not enough traffic for statistical significance:** Extend measurement period or drive more traffic via outbound.

#### Step 5: Decide (1 hour)

| Result | Action |
|--------|--------|
| Metric improved ≥20% | ✅ **KEEP** — ship it, document the win, move to next leak |
| Metric improved <20% | 🟡 **KEEP but note** — marginal win, consider compounding with another change |
| No change | ⚪ **REVERT or KEEP** — the change didn't hurt, but didn't help. Try a different hypothesis for the same level. |
| Metric got worse | 🔴 **REVERT** — roll back immediately, document what didn't work |

**Document every iteration:**
```markdown
## Iteration #{N}: {Hypothesis Summary}
**Date:** {start} → {end}
**Level:** {Activation/Retention/etc.}
**Hypothesis:** "{If we X, then Y because Z}"
**Change:** {What was built/changed}
**Result:** {Metric before} → {Metric after} ({+/-}%)
**Decision:** KEEP / REVERT
**Learning:** {What we learned, even if it failed}
**Next:** {What to try next}
```

### Iteration History (on parent Linear issue)

The engine maintains a running log of all iterations as comments on the parent issue:

```
📊 Iteration #1 (D+3 → D+10): Rewrote hero copy with customer quotes
   Conversion: 2.1% → 4.8% (+129%) ✅ KEPT

📊 Iteration #2 (D+10 → D+17): Added 3-step onboarding wizard
   Activation: 31% → 58% (+87%) ✅ KEPT

📊 Iteration #3 (D+17 → D+24): Changed pricing from $19 to $29/mo
   Free→Paid: 8% → 7.2% (-10%) 🔴 REVERTED

📊 Iteration #4 (D+24 → D+31): Added annual plan at 2mo free
   Free→Paid: 8% → 11% (+38%) ✅ KEPT
```

This history is invaluable for LEARNINGS.md and future runs.

### Pivot Protocol

Sometimes iterations reveal that the problem isn't a metric leak — it's a fundamental positioning or product issue.

**Pivot signals (from 3+ failed iterations):**
| Signal | What It Means | Pivot Option |
|--------|--------------|-------------|
| Lots of traffic, zero signups despite copy changes | Positioning is wrong — visitors don't see this as their problem | Reposition: change target audience or reframe the value prop |
| Good signups, zero activation | Product doesn't deliver on the promise | Rebuild core feature or simplify drastically |
| Good activation, zero retention | Problem isn't recurring — it's a one-time need | Change model: one-time purchase instead of subscription |
| Good retention, zero revenue | Users love it free but won't pay | Freemium model, or find a different monetization (ads, sponsorship, data) |
| Everything works but too small | Market is too niche | Expand the problem scope or target a bigger adjacent market |

**Pivot process:**
1. Document the pivot decision on the Linear parent issue
2. Update Strategy (new positioning, channel, or pricing)
3. Restart relevant stages (Build, Marketing, etc.)
4. Reset Measure baselines
5. Continue iterating

**A pivot is NOT a kill.** It's an informed direction change based on real data.

### When to Stop Iterating
| Signal | Action |
|--------|--------|
| Product hits >80% of 30-day targets | **Maintenance mode** — monthly check-ins, quarterly iterations |
| 3 consecutive iterations with no metric improvement on the SAME level | **Evaluate pivot** — the current approach isn't working for this specific problem |
| Pivot attempted + 3 more failed iterations | **Kill** — the market isn't there, or the product isn't the right solution |
| Max says stop | **Stop** — park or kill based on current data |
| Opportunity cost too high | **Park it** — a better idea has stronger signal, put this in parking lot |
| Product generates enough revenue to sustain itself | **Maintenance + Growth mode** — keep iterating but lower cadence |

### Iteration Cadence
| Phase | Cadence | Focus |
|-------|---------|-------|
| D+1 to D+14 | Every 3 days | Rapid fixes — activation and conversion |
| D+14 to D+30 | Weekly | Retention and revenue |
| D+30 to D+90 | Bi-weekly | Growth loops and scaling |
| D+90+ | Monthly | Maintenance and optimization |

---

## Stage 14: OPS (Post-Launch Operations)

**What happens when real users exist.** This is the stage most indie builders forget — they ship, celebrate, and then the first user emails "it's broken" and there's no process for handling it.

This isn't a pipeline stage with a start and end — it's an ongoing system that activates at Launch and runs as long as the product lives. The engine sets it up automatically during the Build/Launch stages.

### Why Ops Matters for Solo Builders

| Without Ops | With Ops |
|------------|---------|
| User emails about bug → sits in inbox for days | User reports bug → Linear ticket created automatically → Neo triages → fix deployed |
| User asks "how do I X?" → Max writes custom reply every time | FAQ page answers 80% of questions → Max only handles edge cases |
| Site goes down at 3am → nobody notices until morning | Uptime cron alerts immediately → auto-restart or escalate |
| User churns silently | Feedback triggers catch declining usage → proactive outreach |
| Refund request feels awkward | Automated process: refund + survey → learn why |

### Setup (Built During Launch Prep)

These are non-negotiable items that the Build stage includes by default:

#### 1. Support Channel
**Options (pick one based on product type):**

| Product Type | Support Channel | Setup |
|-------------|----------------|-------|
| SaaS / Web tool | In-app feedback widget + support email | `support@{product}.com` → forwards to Max's Gmail (Neo monitors) |
| Info product / Course | Community (Skool/Discord) + email | Existing Skool community, dedicated channel |
| Template / Download | Email only | Contact form on landing page → Gmail |
| B2B / Consulting | Direct email + Calendly for calls | Max's business email |

**Automated support flow:**
```
User submits issue
       ↓
  Neo receives (via Gmail scan or webhook)
       ↓
  ┌─ FAQ match? → Auto-reply with link to answer
  ├─ Bug report? → Create Linear ticket, reply "We're looking into it"
  ├─ Feature request? → Log in Linear, reply "Great idea, noted!"
  ├─ Billing/refund? → Process in Stripe, reply with confirmation
  └─ Complex/unclear? → Flag for Max with summary
```

#### 2. Help Documentation
**Start small, grow from real questions.**

```
/help or /docs page
├── Getting Started (first 5 minutes)
│   ├── Quick start guide (3-5 steps to first value)
│   └── Video walkthrough (60s, from Marketing assets)
├── FAQ (grown from real support tickets)
│   ├── {Question from user #1}
│   ├── {Question from user #2}
│   └── ... (add every unique question)
├── Troubleshooting
│   ├── Common errors + fixes
│   └── "Still stuck? Contact support"
└── Billing
    ├── How to upgrade/downgrade
    ├── How to cancel
    └── Refund policy
```

**Rule:** Every support question that gets asked twice becomes a FAQ entry. Neo does this automatically — when answering a support email, also updates the docs page.

#### 3. Bug Reporting & Tracking
**In-product:** "Report a bug" link in the footer/menu → opens a form or mailto link with template:
```
Subject: Bug Report: {product name}
Body:
What happened:
What you expected:
Steps to reproduce:
Browser/device:
Screenshot (optional):
```

**Processing flow:**
- Bug reports → Linear ticket (label: `bug`, parent: ship run parent issue)
- Severity assessment: P1 (broken for everyone) → fix within 24 hours. P2 (broken for some) → fix within 1 week. P3 (cosmetic/minor) → batch in next iteration.
- User gets notified when fixed: "Good news — we fixed the issue you reported!"

#### 4. Uptime Monitoring
**Cron job (setup during Launch):**
```
Schedule: Every 30 minutes
Action: HTTP GET to product URL
If response != 200:
  → Alert to neo-events (Telegram)
  → Create P1 Linear ticket
  → Attempt auto-restart if applicable (Vercel/Railway auto-heals)
  → If still down after 2 checks (1 hour): alert Max directly
```

**Additional monitoring (if product has backend):**
| Check | Frequency | Alert When |
|-------|-----------|-----------|
| HTTP 200 check | Every 30 min | Non-200 response |
| SSL certificate | Weekly | Expires within 14 days |
| Error rate | Daily | >5% of requests returning 5xx |
| Database size | Weekly | >80% of free tier limit |
| API rate limits | Daily | >70% of quota used |

#### 5. Feedback Collection
**Automated touchpoints:**
| Trigger | Action | Tool |
|---------|--------|------|
| User signs up (D+0) | Welcome email with "reply if you need help" | MailerLite |
| User activates (first value) | "How's it going?" check-in (D+3) | MailerLite |
| User is active for 7 days | NPS survey: "How likely to recommend?" | In-product or email |
| User hasn't returned in 7 days | "We miss you" email with new feature highlight | MailerLite |
| User cancels/churns | Exit survey: "What could we have done better?" | MailerLite or in-product |
| User submits refund | Refund + survey: "What went wrong?" | Stripe + email |

**Feedback → Iteration pipeline:**
All feedback feeds directly into the ITERATE stage:
- NPS detractors (0-6) → diagnose why, create iteration hypothesis
- Churn survey responses → pattern analysis, fix top reason
- Feature requests (≥3 people asking) → add to next iteration
- Bug reports → fix based on severity

### Support Playbook (Detailed)

| Scenario | Neo's Response | Escalate to Max? |
|----------|---------------|-----------------|
| **"How do I...?"** | Check FAQ. If answer exists → send link. If not → answer + add to FAQ. | Never |
| **"It's broken / I got an error"** | "Thanks for reporting! I've logged this and our team is looking into it. I'll update you when it's fixed." → Create Linear P2 ticket | Only if P1 (everyone affected) |
| **"Can you add X feature?"** | "Great idea! I've added it to our roadmap. We'll consider it for an upcoming update." → Log in Linear | Only if it's a fundamental direction question |
| **"I want a refund"** | Process immediately in Stripe. "Refund processed — you'll see it in 3-5 business days. Quick question: what could we have done better?" | Never (within 30-day window) |
| **"I can't log in / access issues"** | Troubleshoot (reset password, check subscription status, test their access). Fix and confirm. | Only if it's a systemic auth issue |
| **"Your competitor does X better"** | "Thanks for the feedback — that's useful context. What specifically would make our product better for you?" → Log in Linear | Only if it reveals a critical gap |
| **"I love this!"** | "That means a lot! Would you mind sharing a quick testimonial? [link]" → Feed to Marketing | Never (but share the joy) |
| **Angry/frustrated user** | Acknowledge the frustration, apologize, solve the problem fast. "I completely understand your frustration. Let me fix this right now." | If they're threatening public complaints |
| **Spam / irrelevant** | Ignore | Never |

**Response time targets:**
| Severity | First Response | Resolution |
|----------|---------------|-----------|
| P1 (everyone affected) | <1 hour | <24 hours |
| P2 (some affected) | <4 hours | <1 week |
| P3 (cosmetic) | <24 hours | Next iteration batch |
| Feature request | <24 hours | Acknowledge only |
| Billing | <2 hours | Same day |

### Ops Scaling Playbook

| User Count | Support Model | Tools | Neo's Role |
|-----------|--------------|-------|-----------|
| **0-50** | Manual: Max + Neo handle everything | Email + Linear | Answer every email, create every ticket, fix every bug personally |
| **50-200** | Semi-automated: FAQ handles 80%, Neo handles rest | Email + Linear + FAQ page + feedback automation | Monitor inbox, update FAQ from patterns, escalate only edge cases to Max |
| **200-500** | Community-assisted: Users help each other | Discord/Skool community + email for billing | Moderate community, pin answers, step in for complex issues, manage community health |
| **500+** | Dedicated support flow: Help center + community + email tiers | Help center (Intercom/Crisp/self-hosted) + community + email | Neo manages the system, not individual tickets. Build self-service. Consider hiring. |

### Ops Metrics (Tracked by Measure stage)
| Metric | Target | Why |
|--------|--------|-----|
| First response time | <4 hours (business hours) | Users who get fast responses churn 50% less |
| Resolution time | <48 hours | Unresolved issues = churn |
| FAQ deflection rate | >60% | If FAQ handles most questions, support is scalable |
| NPS score | ≥7 | Below 7 = product/support problem |
| Uptime | >99.5% | <99% = users lose trust |
| Bug fix time (P1) | <24 hours | Critical bugs left open = churn + bad reviews |

### Ops Cost
| Item | Cost | Notes |
|------|------|-------|
| Support email | $0 | Gmail forwarding |
| FAQ page | $0 | Static page on existing site |
| Uptime monitoring | $0 | Cron job via OpenClaw |
| Linear (bug tracking) | $0 | Already in use |
| Help widget (optional) | $0-$50/mo | Crisp free tier or Tawk.to |
| Community (optional) | $0 | Skool/Discord free tier |

**Total ops cost: $0 for the first 200 users.** Ops should never be an excuse not to ship.

---

## Parallel Execution Map

```
MINE ──→ INTAKE ──→ VALIDATE ──→ STRATEGY
  (always-on)          🔒              │
                              ┌────────┼──────────────────┐
                              ▼        ▼     ▼     ▼     ▼    ▼
                            BUILD    MKTG   OUT  LEADS  NURT  CLOSE
                              │        │     │     │     │     │
                              └────────┴─────┴─────┴─────┴─────┘
                                               │
                                               ▼
                                             BETA
                                               │
                                               ▼
                                            LAUNCH ← OPS starts here
                                              🔒
                                               │
                                               ▼
                                           MEASURE
                                               │
                                               ▼
                                           ITERATE ──→ (loops back to MEASURE)
                                               ↺
```

6 stages run concurrently. Beta waits for Build + Lead Capture minimum. Launch waits for all + Max. Iterate loops until PMF or kill.

---

## Product Type Templates

**NEW — not every product needs the same pipeline.**

### SaaS / Web Tool (Full Pipeline)
All stages apply. Standard or Deep track depending on risk.

### Info Product / Course
| Stage | Adaptation |
|-------|-----------|
| Build | Content creation, not code. Platform = Skool/Teachable/Gumroad |
| Marketing | Heavy — content IS the product, marketing is preview content |
| Lead Capture | Free chapter/lesson as lead magnet |
| Nurture | Educational sequence leading to purchase |
| Closing | Stripe checkout or platform native |
| Beta | Free access to first 10 students for testimonials |
| Ops | Student support, community management |

### Template / Resource / Digital Download
| Stage | Adaptation |
|-------|-----------|
| Build | Create the resource. No app to deploy. |
| Marketing | The resource IS a lead magnet; sell the premium version |
| Lead Capture | Free sample → email → upsell |
| Outbound | Share the free version in communities |
| Nurture | Short sequence (3 emails, not 7) |
| Closing | Simple checkout, no subscription |
| Beta | Skip — just launch |
| Ops | Minimal — download and done |

### Consulting / Service Offer
| Stage | Adaptation |
|-------|-----------|
| Build | Skip (the product is Max's time/expertise) |
| Marketing | Case studies, credentials, social proof |
| Lead Capture | "Book a call" CTA, Calendly embed |
| Outbound | Heavy — cold outreach, LinkedIn, referrals |
| Nurture | Value-heavy emails establishing expertise |
| Closing | Sales call, custom proposal |
| Beta | Do 2-3 engagements at discount for testimonials |
| Ops | Client management, deliverable tracking |

---

## Tool & Skill Registry

### Existing (ready to use)

| Tool | Used In |
|------|---------|
| `research.py` | Validate (Perplexity + xAI research) |
| `web_search` / `web_fetch` | Validate, Outbound (communities, competitors) |
| `coding-agent` | Build |
| `github` skill | Build (repo, PRs, CI/CD) |
| `content-image` | Marketing (OG images, social assets) |
| `brand-report` skill | Measure (GA4 + GSC + IG analytics) |
| `gog` | Strategy (calendar), Nurture (email) |
| Meta API | Marketing (IG publish), Measure (ad metrics) |
| `sessions_spawn` | All stages (parallel sub-agents) |
| `cron` | Measure (scheduled checks), Ops (uptime monitoring) |
| `linear.py` | All stages (ticket management) |
| `humanize` skill | Marketing (humanize AI copy) |

### To Build (prioritized)

| Tool | Used In | Priority |
|------|---------|----------|
| `mailerlite.py` | Lead Capture, Nurture, Closing | P1 🔴 |
| `stripe.py` | Closing, Measure | P1 🔴 |
| `reddit.py` | Validate, Outbound | P1 🔴 |
| `utm.py` | Lead Capture, Measure | P2 🟠 |
| `x-outreach.py` | Outbound (X/Twitter engagement) | P2 🟠 |
| `cold-email.py` | Outbound (cold sequences) | P2 🟠 |
| `landing-page-template` | Validate (fake door tests) | P2 🟠 |
| `producthunt.py` | Launch (PH listing automation) | P3 🟡 |
| `testimonials.py` | Beta, Closing, Marketing | P3 🟡 |

**Note:** All tools have manual fallbacks (web_search, browser automation, LLM reasoning). Don't block shipping on tool availability — the sub-agent adapts.

---

## State File Schema

```json
{
  "ticket": "MAX-XX",
  "name": "ProductName",
  "idea": "description",
  "track": "sprint|standard|deep",
  "productType": "saas|info-product|template|consulting",
  "stage": "outbound",
  "created": "ISO",
  "updated": "ISO",
  "linear": {
    "parentId": "uuid",
    "parentIdentifier": "MAX-XX",
    "subIssues": {
      "validate": { "id": "uuid", "identifier": "MAX-XX" },
      "strategy": { "id": "uuid", "identifier": "MAX-XX" },
      "build": { "id": "uuid", "identifier": "MAX-XX" },
      "marketing": { "id": "uuid", "identifier": "MAX-XX" },
      "outbound": { "id": "uuid", "identifier": "MAX-XX" },
      "lead-capture": { "id": "uuid", "identifier": "MAX-XX" },
      "nurture": { "id": "uuid", "identifier": "MAX-XX" },
      "closing": { "id": "uuid", "identifier": "MAX-XX" },
      "beta": { "id": "uuid", "identifier": "MAX-XX" },
      "launch": { "id": "uuid", "identifier": "MAX-XX" },
      "measure": { "id": "uuid", "identifier": "MAX-XX" },
      "iterate": { "id": "uuid", "identifier": "MAX-XX" }
    }
  },
  "approvals": {
    "validate": null,
    "pre-launch": null
  },
  "distribution": {
    "primaryChannel": null,
    "secondaryChannel": null,
    "growthLoop": null
  },
  "moat": {
    "type": null,
    "description": null
  },
  "budget": {
    "estimated": 0,
    "approved": null,
    "spent": 0,
    "currency": "USD"
  },
  "outputs": {
    "signal_brief": null,
    "idea_brief": null,
    "validation_report": null,
    "ship_plan": null,
    "marketing_kit": null,
    "outbound_playbook": null,
    "lead_capture_setup": null,
    "nurture_sequence": null,
    "closing_strategy": null,
    "beta_report": null,
    "launch_checklist": null,
    "post_launch_report": null
  },
  "external": {
    "repo_url": null,
    "product_url": null,
    "landing_page_url": null,
    "stripe_checkout_url": null
  },
  "beta": {
    "users_invited": 0,
    "users_activated": 0,
    "nps_score": null,
    "testimonials_collected": 0,
    "critical_bugs_open": 0
  },
  "iterations": [],
  "parking_lot_ref": null,
  "metrics_targets": {
    "7d_visitors": 0,
    "7d_signups": 0,
    "7d_activation_rate": 0,
    "30d_revenue": 0,
    "30d_retention": 0
  },
  "decision": null
}
```

---

## Cost Awareness

Before parallel stages begin, estimate and report:
| Item | Default | Notes |
|------|---------|-------|
| Domain | ~$12/yr | If needed |
| Hosting | $0 | Vercel free tier |
| APIs | Varies | List all paid APIs + estimated cost |
| Email tool | $0 | MailerLite free tier (up to 1K subs) |
| Stripe fees | 2.9% + $0.30 | Per transaction |
| Ad spend | $0 default | Recommend budget if applicable |
| **Total** | | Max approves in Strategy |

**Budget is scaled to track:**
- Sprint: <$50 total
- Standard: <$200 total
- Deep: Max approves custom budget in Strategy

---

## Cross-Run Evolution

The Ship Engine **gets smarter with every run.** Each completed or killed run feeds lessons back into the engine itself.

### LEARNINGS.md

`skills/engine/LEARNINGS.md` is the engine's institutional memory.

**After every run completes (Done or Killed), the engine appends:**

```markdown
## {ticket-id}: {name} — {outcome: SHIPPED | KILLED | MAINTAINING | ITERATING}
**Date:** {date}
**Track:** {sprint|standard|deep}
**Product Type:** {saas|info-product|template|consulting}
**Validate Score:** {score} | **Actual Outcome:** {revenue/users/verdict}
**Prediction Accuracy:** {how close was Validate to reality}
**Primary Channel:** {channel} | **Channel Effectiveness:** {assessment}
**Moat:** {type} | **Moat Held?:** {yes/no/too-early}

### What Worked
- {specific tactic, channel, or approach that delivered results}

### What Didn't Work
- {specific thing that underperformed, with data}

### Timing
| Stage | Estimated | Actual | Delta |
|-------|-----------|--------|-------|
| Validate | 30 min | {actual} | {delta} |
| Build | {est} | {actual} | {delta} |
| ... | ... | ... | ... |

### Iteration History
- Iteration 1: {hypothesis} → {result}
- Iteration 2: {hypothesis} → {result}

### Patterns Discovered
- {reusable insight for future runs}

### Engine Improvements Applied
- {specific change made to SKILL.md, templates, or tooling based on this run}
```

### How Learnings Feed Forward

| Stage | How LEARNINGS.md is Used |
|-------|-------------------------|
| **Mine** | Which audience signals actually predicted success? Calibrate signal scoring. |
| **Validate** | Compare past scores vs actual outcomes. Adjust scoring weights. |
| **Strategy** | Timing estimates from actual durations. Budget from real costs. Channel effectiveness data. |
| **Marketing** | Which channels actually converted? Reuse winning patterns. |
| **Outbound** | Which communities responded? Which outreach worked? |
| **Beta** | How many beta users needed for meaningful feedback? |
| **Closing** | What price points worked? Which objection handlers converted? |
| **Measure** | Refine metric thresholds based on past baselines. |
| **Iterate** | Which iteration types moved metrics? How many iterations to PMF? |

### Self-Modification Protocol

After accumulating 3+ runs of data, the engine should **propose spec updates** via PR:
1. Identify patterns across runs
2. Propose concrete changes to SKILL.md
3. Create PR via git worktree
4. Max reviews and merges

---

## User Interaction

### Channel-Agnostic Interface

The Ship Engine communicates through **whatever channels are available** via OpenClaw's messaging tools. It doesn't hardcode channel IDs — it uses the `message` tool with channel routing.

**Channel usage by purpose:**
| Purpose | How |
|---------|-----|
| Idea intake | Any DM or group where Max sends a message |
| Approval gates | DM to Max (most reliable) |
| Stage completions | Configured notification channel |
| Blockers/escalations | DM to Max + Linear comment |
| Deliverable links | Linear comments |

**Submitting ideas:**
- `ship: [description]` — explicit trigger (any channel)
- Voice message — auto-transcribed
- Link — auto-fetched and analyzed
- Image/screenshot — analyzed and structured

**Commands:**
| Command | Action |
|---|---|
| `ship: [idea]` | Start new ship run |
| `status` | All active runs overview |
| `status [MAX-XX]` | Detail on specific run |
| `kill [MAX-XX]` | Stop and archive |
| `skip [MAX-XX] to [stage]` | Jump to stage |
| `park [MAX-XX]` | Move to parking lot |
| `parking lot` | List parked ideas |
| `iterate [MAX-XX]` | Start new iteration cycle |

**Approval buttons** (adapted per platform):
```
[✅ Approve] [✏️ Changes] [🅿️ Park It] [🗑 Kill]
```

**Three mandatory gates:** Post-Validation, Pre-Launch, and Kill decisions (D+30).
**Default on no response:** Ping at 24h, 48h, then daily. Engine keeps other runs moving.

**Notification rules:**
- ✅ Stage completions, approval requests, blockers, beta results
- ❌ Internal sub-agent progress, tool calls, intermediate steps
- 📋 Daily digest if active runs exist

---

## Kill Process

1. Archive GitHub repo
2. Stop all crons (measure, ops monitoring)
3. Pause email sequences
4. Close Linear ticket with post-mortem comment
5. Extract lessons → `LEARNINGS.md`
6. Update MEMORY.md with key takeaway
7. Move state file to `archive/`
8. Consider: is there a pivot worth testing? If yes → park the pivot idea.

---

## File Structure

```
skills/engine/
├── SKILL.md                        # This file (the spec — evolves over time)
├── LEARNINGS.md                    # Institutional memory (grows with every run)
├── parking-lot.md                  # Parked ideas awaiting new signals
├── engine.py                       # CLI orchestrator
├── runs/                           # Active ship runs
│   ├── {ticket-id}.json            # State file
│   └── {ticket-id}/               # Run artifacts
│       ├── idea-brief.md
│       ├── validation-report.md
│       ├── ship-plan.md
│       ├── beta-report.md
│       ├── marketing/
│       ├── outbound/
│       └── metrics/
├── templates/
│   ├── ship-checklist.md           # Master checklist
│   ├── idea-brief.md
│   ├── validation-report.md
│   ├── customer-interview.md       # NEW: interview script + guide
│   ├── ship-plan.md
│   ├── marketing-kit.md
│   ├── outbound-playbook.md
│   ├── lead-capture.md
│   ├── nurture-sequence.md
│   ├── closing-strategy.md
│   ├── content-calendar.md
│   ├── launch-checklist.md
│   ├── beta-report.md              # NEW: beta testing results
│   └── post-launch-report.md
└── archive/                        # Completed/killed runs
    └── {ticket-id}/
```
