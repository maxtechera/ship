---
name: ship
version: "0.2.0"
description: "GTM pipeline with team mode. /ship spawns coordinator + executor + critic team, renders live dashboard of all active runs, loops every 10m. /ship create starts a new run."
argument-hint: 'ship (dashboard + team), ship create "<idea>", ship status, ship run <RUN-ID>'
allowed-tools: Bash, Read, Write
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
user-invocable: true
triggers:
  - ship
  - ship create
  - ship status
  - ship run
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env: []
      optionalEnv:
        - SHIP_CRED_DIR
        - SHIP_EXTENSIONS_DIR
        - SHIP_RUNS_DIR
        - LINEAR_API_KEY
      bins: []
    primaryEnv: ""
    files:
      - "credentials/registry/core.yml"
      - "engine/WORKFLOW.md"
    tags:
      - credentials
      - preflight
      - gtm
      - launch
      - deploy
      - ship
      - pipeline
---

# ship

Run `/ship` once. A coordinator team spawns, the dashboard renders, and work starts moving.

The team reads all active ship runs from Linear, assigns stage work to the executor, sends deliverables to the critic before every gate, and keeps a live dashboard refreshing every 10 minutes. You review the critic's verdict, approve gates, and watch runs advance to Done.

## Commands

| Command | Description |
|---------|-------------|
| `/ship` | Spawn coordinator team + render live dashboard of all active runs |
| `/ship create "<idea>"` | Create Linear run ticket, preflight credentials, hand off to engine supervisor |
| `/ship status [RUN-ID]` | Read active run from Linear, print stage + last update + blocked items |
| `/ship run <RUN-ID>` | Resume an existing run (re-triggers engine supervisor for that ticket) |

## /ship (default — team mode)

Called with no arguments. Spawns the ship coordinator team and renders the live dashboard. Stays running via `/loop`.

### 1. Preflight

```bash
python3 credentials/scripts/check_local.py --only "linear" --json
```

If exit 1 → print `fix_cmd` per failure. Do not spawn team until credentials pass.

### 2. Pull state from all data sources (parallel)

| Source | What to read | How |
|--------|-------------|-----|
| Linear | All tickets labeled `ship-engine` (any state) | Linear API or `linear` CLI |
| GitHub | Open PRs + CI state for ship-project repos | `gh pr list --repo <repo>` |
| Memory | Last session digest + recent decisions | Read `MEMORY.md` router |

Group Linear tickets by: run ID → stage → state (in_progress / pending / blocked / done).

### 3. Render dashboard

Print the dashboard to the user before spawning the team. Format:

```
## Ship Dashboard  [2026-04-14 14:32]

Active Runs (<N>)
  <RUN-ID>  <product-name>          <current-stage>  <state>   [<wave>]
  ...

Pipeline Metrics (30d)
  Assets shipped:     N/M
  Critic approvals:   N/M (avg score)
  Conversions:        N
  Metrics captures:   N (M awaiting first publish)

Blocked
  <RUN-ID>  <reason>  [fix_cmd if credentials]
  ...

Team
  coordinator — spawning
  critic      — idle
  strategist  — idle
  content     — idle
  growth      — idle
  nurture     — idle
  closer      — idle
  launcher    — idle
  analyst     — idle
```

If no active runs → print "No active ship runs. Use /ship create \"<idea>\" to start one."

### 4. Spawn team

Spawn the full pre-defined GTM team. Every role starts at boot — coordinator assigns work as stages become actionable.

```
TeamCreate team_name="ship"

# ── Control ──────────────────────────────────────────────────

Agent name="coordinator" team_name="ship" run_in_background=true
  prompt: "Read ship/SKILL.md + supervisors/engine/SKILL.md. Pull all Linear tickets
  labeled ship-engine. For each active run identify the next actionable stage and route
  to the correct specialist via SendMessage. Zero-idle: always queue a secondary task.
  Loop: /loop 10m /ship"

Agent name="critic" team_name="ship" run_in_background=true
  prompt: "Read supervisors/critic/SKILL.md. Receive review requests via SendMessage.
  Never read the executor's work log — fresh context only. Score on v3 rubric (100-pt,
  10 cats x 10): brand voice, audience fit, hook strength, CTA + Hormozi two-part rule,
  offer framing, structural, guide alignment, human-sounding (zero Tier-1 AI words),
  format craft (platform-specific), verbatim/specificity (real numbers, no claims).
  Threshold ≥75 APPROVE. One revise pass max — then ship, escalate to coordinator.
  When measure-analyst Stream-2 avg ≥7 and band mid/high: cat #3 = Stream-2 score ±1
  (do not re-score independently). Required before every gate and every verified state advance."

# ── GTM specialists ───────────────────────────────────────────

Agent name="strategist" team_name="ship" run_in_background=true
  prompt: "GTM strategy specialist. Handles: intake research, ICP definition, positioning,
  offer design, pricing, channel selection. Reads supervisors/intake/SKILL.md,
  supervisors/validate/SKILL.md, supervisors/strategy/SKILL.md. Receives stage ticket
  from coordinator. Writes blackboard keys: intake.*, validate.*, strategy.*
  Posts completion to coordinator."

Agent name="content" team_name="ship" run_in_background=true
  prompt: "Content production specialist. Handles: copy, carousels, reels, blog posts,
  newsletters, landing pages, offer pages, storyboards. Reads ship/content/SKILL.md
  (all 17 sub-skills). Receives asset brief from coordinator. Enforces format specs
  (carousel 1080x1350, reel hook 0-3s, newsletter subject ≤50 chars). Posts artifacts
  + live URLs to coordinator."

Agent name="growth" team_name="ship" run_in_background=true
  prompt: "Growth + lead capture specialist. Handles: lead capture pages, UTM wiring,
  GA4 conversion events, A/B test setup, referral mechanics. Reads
  supervisors/lead-capture/SKILL.md. UTM required before any campaign goes live.
  A/B test requires control variant ≥400 recipients. Posts wiring evidence to coordinator."

Agent name="nurture" team_name="ship" run_in_background=true
  prompt: "Nurture + email sequence specialist. Handles: welcome sequences, drip schedules,
  MailerLite tag triggers, segmentation. Reads supervisors/nurture/SKILL.md (including
  OSS Nurture Mode for oss_tool runs). Writes blackboard keys: nurture.*
  Posts sequence screenshots + send-test evidence to coordinator."

Agent name="closer" team_name="ship" run_in_background=true
  prompt: "Closing + conversion specialist. Handles: sales pages, course pages, objection
  packs, checkout flows, post-purchase sequences. Reads supervisors/closing/SKILL.md
  (including OSS Closing Mode for oss_tool runs). Writes blackboard keys: closing.*
  Posts page URL + checkout test evidence to coordinator."

Agent name="launcher" team_name="ship" run_in_background=true
  prompt: "Launch coordinator. Handles: pre-launch readiness checklist, social push
  scheduling, directory submissions, final credentials preflight. Reads
  supervisors/launch/SKILL.md. Runs: python3 credentials/scripts/check_local.py --json
  before any deploy action — exit 1 halts launch. Posts launch package to coordinator."

Agent name="analyst" team_name="ship" run_in_background=true
  prompt: "Metrics + analytics specialist. Operates a 3-stream model. Reads
  supervisors/measure/SKILL.md. Stream 1 (pre-launch): build viral-patterns-library
  per wave — top posts, hook formulas, CTAs, format specifics, anti-patterns — before
  the content agent starts the bundle. Stream 2 (pre-publish gate): after content drops
  bundle, score each surface hook against library (0-10 pattern match + predicted
  engagement band low/mid/high). Default step: hook-vocab audit — grep bundle for 3-5
  category-native phrases, flag mismatches, propose 1-2 native alternates. Output:
  metrics/<run>-hook-predictions.md. Ping critic with avg score before final approval.
  Stream 3 (async post-launch): record publish timestamp + URLs, pull GA4/GSC/platform
  actuals at T+24h/T+7d/T+30d, update Linear ticket, flag coordinator if underperforming
  (pageviews <200 at T+7d, stars delta 0). Promote hits / retire misses in library.
  Every metric must cite source + date range. Runs /memory sync after each scorecard."
```

### 5. Loop

```
/loop 10m /ship
```

Each tick: re-pull all data sources, re-render dashboard, identify newly actionable stages, route to correct specialist if idle. Dashboard `Team` row updates to show which agent is active.

### Pre-defined team roster

| Agent | Stage coverage | Isolation |
|-------|---------------|-----------|
| `coordinator` | All — routes + assigns | none |
| `critic` | All gates + verified advances | none |
| `strategist` | Intake → Validate → Strategy | none |
| `content` | Awareness (all asset types) | none |
| `growth` | Lead Capture (UTM, GA4, A/B) | none |
| `nurture` | Nurture (sequences, MailerLite) | none |
| `closer` | Closing (sales/course pages) | none |
| `launcher` | Launch (readiness, push, directories) | none |
| `analyst` | Measure (GA4, Stripe, scorecards) | none |

**Dynamic roles** — coordinator spawns these as stage complexity demands:

| Agent | When to spawn | Prompt reference |
|-------|--------------|-----------------|
| `researcher` | Intake requires deep ICP / competitor research | `supervisors/intake/SKILL.md` |
| `seo-specialist` | Run includes SEO blog deliverable | `skills/seo/SKILL.md` |
| `outreach` | Run includes B2B cold email sequence | `skills/sales-outreach/SKILL.md` |
| `designer` | Run requires visual asset creation (not copy) | `ship/content/skills/image/SKILL.md` |

Coordinator spawns dynamic roles via `Agent name="<role>" team_name="ship" run_in_background=true` when the stage ticket specifies a deliverable that the pre-defined roster doesn't cover.

**Zero-idle rule:** coordinator always has a queued secondary task for every active specialist. When a stage completes, next assignment is sent immediately — no agent ever waits.

## /ship create

Steps the agent follows verbatim:

1. **Parse `<idea>` string.** If it contains "open source", "github", "tool", "CLI", or "library" → default `product_type: oss_tool`. Otherwise prompt the user to confirm: `saas | course | service | oss_tool`.
2. **Credentials preflight.** Run `python3 credentials/scripts/check_local.py --only "linear" --json`. If exit 1 → print `fix_cmd` for each failure, halt. Do not create the ticket until credentials pass.
3. **Create Linear ticket.** Title = idea string. Label = `ship-engine`. Fill the orchestrator contract sections with stage-1 defaults:
   - Inputs: `product_type`, idea string
   - Deliverables: complete ship run (all stages PASS)
   - Verification: all stages pass critic gates, credentials preflight passes at launch
   - Artifacts: ship run ID, final stage URLs
4. **Post the Linear ticket URL** to the user.
5. **Hand off to `supervisors/engine/SKILL.md`** with the new ticket ID.

## Sub-skills

- **[credentials](credentials/SKILL.md)** — health-check, install, and auth wizard for 30+ CLIs and API tokens. Run before every deploy.
- **[engine](engine/SKILL.md)** — full idea → validate → strategy → awareness → lead-capture → nurture → closing → launch → measure pipeline.
- **[supervisors/engine](supervisors/engine/SKILL.md)** — always-on control loop. Reconciles Linear run tickets, delegates to stage supervisors, enforces critic gates.

## Team Credential Gate

Before spawning an agent team, validate every token the team needs:

```bash
python3 credentials/scripts/check_local.py \
  --only "github,railway,vercel,openai,anthropic" \
  --json
```

In Claude Code, call this before `TeamCreate`:

```
# 1. Preflight — run check_local.py --only "<required-tokens>" --json
# 2. If all pass (exit 0) → spawn team
TeamCreate team_name="<project>"
Agent name="builder" team_name="<project>" isolation="worktree" run_in_background=true
...
# 3. If any fail (exit 1) → print fix_cmd for each failure, halt
```

This is the LAUNCH gate. Missing tokens surface before agents start, not mid-sprint.

## Quick start

```bash
python3 credentials/scripts/check_local.py
```

See [credentials/SKILL.md](credentials/SKILL.md) for full documentation.
