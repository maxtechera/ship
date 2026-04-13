---
name: credentials
description: Verify, validate, and fix local credentials for CLIs and APIs. 30+ checks (runtime CLIs, CLI auth, API tokens, Google OAuth). Includes install and auth wizards. Part of the ship skill pack.
---

# Credentials

Health-check, install, and auth wizard for the CLI tools and API tokens your agents depend on.

Covers 30+ common integrations out of the box — GitHub, Vercel, Railway, Render, Linear, Supabase, Twilio, ElevenLabs, MailerLite, PostHog, Meta, ManyChat, Telegram, Brave, Perplexity, OpenAI, Anthropic, Gemini, xAI, Google OAuth (via `gog`), and more. Workspace-specific services add on via YAML extensions.

## Scripts

| Script | Purpose |
|---|---|
| `check_local.py` | Full local credential health check (32 checks on Mac) |
| `check_all.py` | Container/server variant — adds service-specific checks (Stripe, Shopify, Notion, Discord, Gamma, gateway) |
| `install.py` | Interactive wizard to install missing CLIs via brew/npm |
| `auth.sh` | Interactive auth wizard for all CLIs |
| `refresh.py` | Refresh rotating tokens (where supported) |

## Quick Start

```bash
# Check everything
python3 ~/.claude/skills/credentials/scripts/check_local.py

# Only failures
python3 ~/.claude/skills/credentials/scripts/check_local.py --quiet

# With fix commands
python3 ~/.claude/skills/credentials/scripts/check_local.py --fix

# Check a single service
python3 ~/.claude/skills/credentials/scripts/check_local.py --only google_oauth

# JSON (automation-friendly)
python3 ~/.claude/skills/credentials/scripts/check_local.py --json

# Install missing CLIs (interactive wizard)
python3 ~/.claude/skills/credentials/scripts/install.py

# Install everything missing
python3 ~/.claude/skills/credentials/scripts/install.py --all

# Auth all CLIs interactively
bash ~/.claude/skills/credentials/scripts/auth.sh

# Show auth status
bash ~/.claude/skills/credentials/scripts/auth.sh --list
```

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

Directory selected by first match:

1. `$SHIP_CRED_DIR`
2. `$OPENCLAW_CRED_DIR` (legacy alias, still honoured)
3. `/data/.clawdbot` (existing OpenClaw container)
4. `~/.clawdbot` (existing legacy Mac)
5. `~/.config/ship/credentials` (default — auto-created on first write)

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
├── .shopify.json               # {shop, access_token, client_id, client_secret}
├── .stripe_token
├── .discord_token
├── .notion_token
├── .gamma_token
├── .manychat_token
├── .telegram_bot_token
├── .elevenlabs_token
├── .brave_token
├── .mailerlite_token
├── .posthog_token
├── .zoom_account_id + .zoom_client_id + .zoom_client_secret
├── .twitter_* + .linkedin_* + .tiktok_* + .youtube_*
└── cookies/
    ├── youtube.txt             # Netscape cookies for yt-dlp
    └── skool-cookies.json
```

## Extending

Drop a `*.yml` file into `$SHIP_CRED_DIR/extensions/` (or the directory named by `$SHIP_EXTENSIONS_DIR`) to register additional checks. See [`extensions/README.md`](extensions/README.md) for the schema and [`../docs/extensions/my-service.yml.example`](../docs/extensions/my-service.yml.example) for a working sample.

## Exit codes

- `0` — all checks pass
- `1` — at least one check failed

## Structure

```
credentials/
├── SKILL.md                    # this file
├── scripts/
│   ├── check_local.py
│   ├── check_all.py
│   ├── install.py
│   ├── auth.sh
│   └── refresh.py
├── registry/
│   └── core.yml                # declarative check index (documentation)
├── extensions/                 # drop your own *.yml here
│   └── README.md
└── references/
    └── fix-guide.md            # per-credential fix instructions
```
