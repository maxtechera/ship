---
name: ship
version: "0.1.0"
description: "Credentials preflight and GTM pipeline for AI agents. Check 30+ CLIs and API tokens before you deploy."
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
      bins:
        - python3
    primaryEnv: ""
    files:
      - "credentials/scripts/*"
    tags:
      - credentials
      - preflight
      - gtm
      - launch
      - deploy
      - ship
---

# ship

Credentials preflight and GTM pipeline for AI agents. Part of the maxtechera skill suite.

## Sub-skills

- **[credentials](credentials/SKILL.md)** — health-check, install, and auth wizard for 30+ CLIs and API tokens. Run before every deploy.
- **ship-engine** (v0.2, coming) — full idea → validate → build → market → sell → measure pipeline.

## Quick start

```bash
python3 ~/.claude/skills/ship/credentials/scripts/check_local.py
```

See [credentials/SKILL.md](credentials/SKILL.md) for full documentation.
