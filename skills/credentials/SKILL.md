---
name: credentials
version: "0.3.0"
description: "Health-check 30+ CLIs and API tokens before you deploy. Agent-executed preflight using the ship credentials registry."
argument-hint: ''
allowed-tools: Bash, Read
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
user-invocable: true
triggers:
  - credentials
  - credentials check
  - check credentials
  - check tokens
---

# credentials

Health-check the CLI tools and API tokens your agents depend on. Run before every deploy, before team creation, and before any pipeline stage that needs external access.

## How to run

```bash
python3 credentials/scripts/check_local.py
```

Useful variants:

```bash
python3 credentials/scripts/check_local.py --quiet
python3 credentials/scripts/check_local.py --fix
python3 credentials/scripts/check_local.py --only "github,railway,vercel,openai,anthropic"
```

## Required references

Before acting, read these repo files as needed:

- `credentials/SKILL.md`
- `credentials/registry/core.yml`
- `credentials/scripts/check_local.py`

## Output expectations

- Report missing tools or tokens clearly.
- Prefer actionable fix commands.
- Block deploy work when required credentials are missing.
