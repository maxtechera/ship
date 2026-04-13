---
name: ship
version: "0.2.0"
description: "Credentials preflight + GTM pipeline. Health-check 30+ CLIs/tokens, then execute idea → validate → market → sell → measure."
argument-hint: ''
allowed-tools: Bash, Read, Write
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
user-invocable: false
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env: []
      optionalEnv:
        - SHIP_CRED_DIR
        - SHIP_EXTENSIONS_DIR
        - SHIP_RUNS_DIR
        - SHIP_ARCHIVE_DIR
        - LINEAR_API_KEY
        - LINEAR_TOKEN_PATH
        - GOOGLE_ANALYTICS_TOKEN_PATH
        - CLAWDBOT_DIR
      bins:
        - python3
    primaryEnv: ""
    files:
      - "credentials/scripts/*"
      - "ship-engine/engine.py"
      - "ship-engine/approval_queue.py"
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

Credentials preflight and GTM pipeline for AI agents. Part of the maxtechera skill suite.

## Sub-skills

- **[credentials](credentials/SKILL.md)** — health-check, install, and auth wizard for 30+ CLIs and API tokens. Run before every deploy.
- **[ship-engine](ship-engine/SKILL.md)** — full idea → validate → strategy → awareness → lead-capture → nurture → closing → launch → measure pipeline.
- **[supervisors/engine](supervisors/engine/SKILL.md)** — always-on control loop. Reconciles Linear run tickets, delegates to stage supervisors, enforces critic gates.

## Team Credential Gate

Before spawning an agent team, validate every token the team needs:

```bash
python3 ~/.claude/skills/ship/credentials/scripts/check_local.py \
  --only "github,railway,vercel,openai,anthropic" \
  --json | jq '.failed | length == 0'
```

In Claude Code, call this before `TeamCreate`:

```
# 1. Preflight — block team spawn on missing credentials
python3 credentials/scripts/check_local.py --only "<required-tokens>" --json

# 2. If all pass → spawn team
TeamCreate team_name="<project>"
Agent name="builder" team_name="<project>" isolation="worktree" run_in_background=true
...

# 3. If any fail → print fix commands, halt
python3 credentials/scripts/check_local.py --only "<required-tokens>" --fix
```

This is the LAUNCH gate. Missing tokens surface before agents start, not mid-sprint.

## Quick start

```bash
python3 ~/.claude/skills/ship/credentials/scripts/check_local.py
```

See [credentials/SKILL.md](credentials/SKILL.md) for full documentation.
