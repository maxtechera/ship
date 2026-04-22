# ship

[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Claude_Code-supported-7C3AED)](#quick-start)
[![Platform: OpenClaw](https://img.shields.io/badge/OpenClaw-supported-111827)](#quick-start)
[![Platform: Gemini CLI](https://img.shields.io/badge/Gemini_CLI-supported-2563EB)](#quick-start)
[![Platform: Codex CLI](https://img.shields.io/badge/Codex_CLI-supported-059669)](#quick-start)

Ship is an open source GTM operating system for teams running launches, content, and conversion work through one agentic pipeline. It is built for operators who want real stage ownership, credential-gated execution, and reviewer-visible proof instead of loose prompt chains.

It boots a coordinator-led team that reads active work, routes specialists by stage, blocks risky deploys when credentials are missing, and keeps every run moving from idea to measurement.

## What you get

- A coordinator that keeps GTM work moving across the full pipeline
- Stage supervisors for intake, validation, strategy, awareness, lead capture, nurture, closing, launch, and measure
- A credential gate that checks 30+ integrations before deploy actions
- A critic and analyst review path so assets do not advance on vibes alone
- Content sub-skills for the actual production layer, not just orchestration

## Quick start

```bash
clawhub install ship
/credentials
/ship
```

What those three commands do:

1. Install the skill suite
2. Verify the credentials you need before work starts
3. Boot the ship dashboard and coordinator team

## Core commands

| Command | What it does |
|---|---|
| `/ship` | Launch the dashboard and coordinator team |
| `/ship create "<idea>"` | Create a new run, check credentials, and hand work to the engine |
| `/ship status [RUN-ID]` | Show stage, recent updates, and blockers |
| `/ship run <RUN-ID>` | Resume an existing run |

## Three concrete use cases

### 1. Turn a rough launch idea into an active GTM run

**Before**

```text
"We should probably launch the new AI automation workshop next week."
```

**After**

```bash
/ship create "Launch the AI automation workshop for founders who want SOP-backed agents"
```

Ship creates the run, checks credentials, routes strategy work first, and gives you a tracked pipeline instead of a loose brainstorm.

### 2. Keep content production connected to review and launch

**Before**

```text
Docs live in one place, assets in another, approvals happen in chat, and nobody knows what is actually ready.
```

**After**

```text
idea → validate → strategy → awareness → lead-capture → nurture → closing → launch → measure
```

Each stage has an owner, proof requirements, and a gate before the run advances.

### 3. Catch broken deploy readiness before it burns a sprint

**Before**

```bash
python3 credentials/scripts/check_local.py --quiet
# failures show up only after work is already blocked downstream
```

**After**

```bash
/ship
# launcher and credential preflight stop the run before a deploy action starts
```

That means missing tokens, expired auth, or absent CLIs are surfaced early, when they are still cheap to fix.

## Skill map

| Layer | Path | What it owns |
|---|---|---|
| Credentials | `credentials/` | Preflight checks, CLI installs, auth helpers, token refresh |
| Engine | `engine/` | Dashboard loop, routing logic, active run orchestration |
| Supervisors | `supervisors/` | Stage-specific execution across intake to measure |
| Content | `content/` | Production skills for assets, copy, and channel outputs |
| Critic | `orchestrator` composition + ship review contract | Approval gates, proof expectations, stage advancement discipline |

## Team structure

Coordination comes from [orchestrator](https://github.com/maxtechera/orchestrator). Ship adds the GTM roster, stage logic, credential system, and content production surface.

| Role | Coverage | Notes |
|---|---|---|
| `coordinator` | All stages | Reads active runs, routes work, keeps zero-idle flow |
| `critic` | All gates | Fresh-context review, rubric-based approval |
| `strategist` | Intake, validate, strategy | Research, ICP, positioning, offer design |
| `content` | Awareness | Produces content assets across sub-skills |
| `growth` | Lead capture | UTM wiring, GA4, experiments |
| `nurture` | Nurture | Email flows, segmentation, automation |
| `closer` | Closing | Sales pages, objections, conversion assets |
| `launcher` | Launch | Readiness, deploy gating, final preflight |
| `analyst` | Measure | Hook scoring, performance tracking, learnings |

## Install options

### Claude Code

```bash
claude plugin marketplace add maxtechera/ship
claude plugin install ship@ship
```

### OpenClaw

```bash
clawhub install ship
```

### Gemini CLI

```bash
gemini extensions install maxtechera/ship
```

### Codex CLI

```bash
git clone https://github.com/maxtechera/ship.git ~/.agents/skills/ship
```

### Manual

```bash
git clone https://github.com/maxtechera/ship.git ~/.claude/skills/ship
```

## Credential preflight

Run this any time you want a direct health check:

```bash
python3 credentials/scripts/check_local.py
```

Useful variants:

```bash
python3 credentials/scripts/check_local.py --quiet
python3 credentials/scripts/check_local.py --fix
python3 credentials/scripts/check_local.py --json
python3 credentials/scripts/check_local.py --only "github,railway,vercel,openai,anthropic"
```

Ship checks runtime tools, CLI auth, API tokens, and Google-suite integrations before deploy actions. Missing credentials block the run early, not halfway through launch week.

## Repository map

```text
ship/
  SKILL.md
  credentials/
  engine/
  supervisors/
  content/
```

## Principles

- Practitioner-first, not prompt-theater
- Proof before advancement
- Fresh-context review for critic decisions
- Credential gating before deploy work
- One pipeline from idea to measurement

## License

MIT. See [LICENSE](LICENSE).
