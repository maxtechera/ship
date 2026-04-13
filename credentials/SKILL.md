---
name: credentials
version: "0.2.0"
description: "Health-check 30+ CLIs and API tokens before you deploy. Agent-executed preflight using registry/core.yml."
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
metadata:
  openclaw:
    emoji: "🔑"
    requires:
      env: []
      optionalEnv:
        - SHIP_CRED_DIR
        - SHIP_EXTENSIONS_DIR
      bins: []
    primaryEnv: ""
    files:
      - "registry/core.yml"
    tags:
      - credentials
      - preflight
      - auth
      - cli
      - api-token
      - health-check
      - deploy
---

# Credentials

Health-check the CLI tools and API tokens your agents depend on. Run before every deploy, before `TeamCreate`, before any pipeline stage that needs external access.

Covers 30+ integrations out of the box — GitHub, Vercel, Railway, Render, Linear, Supabase, Twilio, ElevenLabs, MailerLite, PostHog, Meta, ManyChat, Telegram, Brave, Perplexity, OpenAI, Anthropic, Gemini, xAI, Google OAuth (via `gog`), and more.

## How to Run a Credential Check

```bash
# Check everything
python3 credentials/scripts/check_local.py

# Only failures
python3 credentials/scripts/check_local.py --quiet

# With fix commands
python3 credentials/scripts/check_local.py --fix

# Check specific services (automation-friendly)
python3 credentials/scripts/check_local.py --only "github,railway,vercel,openai,anthropic"

# JSON output for parsing in Claude Code
python3 credentials/scripts/check_local.py --json

# Check a single service
python3 credentials/scripts/check_local.py --only google_oauth
```

Exit 0 if all pass. Exit 1 if any fail — prints `fix_cmd` per failure.

## What Gets Checked

### Runtime CLIs (4)
`git`, `node`, `pnpm`, `python3` — `--version` probe.

### CLI Auth (7) — checked via CLI whoami
`gh`, `railway`, `vercel`, `linear`, `supabase`, `render`, `docker`.

### API Tokens (10) — live HTTP whoami
OpenAI, Anthropic, Gemini, xAI, Perplexity, Meta, ManyChat, Telegram, Brave, Zoom.

### CLI-first (prefer CLI, fall back to API token) (4)
Twilio, ElevenLabs, MailerLite, PostHog.

### Google Suite (7) — gog CLI manages OAuth
`google_oauth`, `ga4`, `gsc`, `gcal`, `gdrive`, `gmail`, `skool`.

## Credential Directory

Token files are resolved by first match:

1. `$SHIP_CRED_DIR`
2. `$OPENCLAW_CRED_DIR` (legacy alias)
3. `~/.clawdbot` (existing Mac/container default)
4. `~/.config/ship/credentials` (new default — auto-created on first write)

Files inside (`chmod 700` recommended):

```
$SHIP_CRED_DIR/
├── .github_token               # ghp_...
├── .meta_token                 # EAA... (Meta/Instagram)
├── .linear_token               # lin_api_...
├── .openai_token               # sk-...
├── .anthropic_token            # sk-ant-...
├── .xai_token                  # xai-...
├── .gemini_token
├── .perplexity_token
├── .railway_token
├── .vercel_token
├── .twilio_sid + .twilio_token
├── .mailerlite_token
├── .posthog_token
├── .manychat_token
├── .telegram_bot_token
├── .elevenlabs_token
├── .brave_token
└── cookies/
    └── youtube.txt             # Netscape cookies for yt-dlp
```

## Team Credential Profiles

Validate only the tokens a specific team needs before spawning it.

| Team | Required check IDs |
|------|--------------------|
| GTM team | `github,openai,anthropic,meta_token,mailerlite` |
| Engineering team | `github,railway,vercel,supabase,openai,anthropic` |
| Content team | `openai,anthropic,perplexity` |
| Full ship-engine | `github,railway,vercel,openai,anthropic,meta_token,mailerlite` |

**Pattern — credential gate before TeamCreate:**

```bash
# Returns exit 0 if all pass, exit 1 if any fail
python3 credentials/scripts/check_local.py \
  --only "github,railway,vercel,openai,anthropic" \
  --json
```

This is the LAUNCH gate. Missing tokens surface before agents start, not mid-sprint.

## Extending

Drop a `*.yml` file into `$SHIP_CRED_DIR/extensions/` (or `$SHIP_EXTENSIONS_DIR`) to register additional checks. See [`extensions/README.md`](extensions/README.md) for the schema.

## Structure

```
credentials/
├── SKILL.md                    # this file — agent instructions
├── scripts/
│   └── check_local.py          # stdlib-only runner — JSON output, exit codes, --only filter
├── registry/
│   └── core.yml                # declarative check index (verify_cmd, fix_cmd per service)
├── extensions/                 # drop your own *.yml check definitions here
│   └── README.md
└── references/
    └── fix-guide.md            # per-credential fix instructions
```
