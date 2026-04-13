---
name: credentials
description: Verify, validate, and fix workspace credentials and integrations. 32 checks (11 CLI + 21 API). Includes install wizard, auth wizard, and per-service whoami. Uses platform-aware ~/.clawdbot on Mac, /data/.clawdbot on container.
---

# Credentials Skill

Health-check, install, and auth wizard for all workspace credentials.

## Scripts

| Script | Purpose |
|---|---|
| `check_local.py` | 32 checks: 11 CLI + 21 API whoami (local Mac) |
| `check_all.py` | 21 checks: container credentials + integrations |
| `install.py` | Idempotent installer with interactive wizard |
| `auth.sh` | Interactive auth wizard for all CLIs |

## Quick Start

```bash
# Check everything
python3 ~/.claude/skills/credentials/scripts/check_local.py

# Only failures
python3 ~/.claude/skills/credentials/scripts/check_local.py --quiet

# With fix commands
python3 ~/.claude/skills/credentials/scripts/check_local.py --fix

# Check single service
python3 ~/.claude/skills/credentials/scripts/check_local.py --only google_oauth

# Install missing CLIs (interactive wizard)
python3 ~/.claude/skills/credentials/scripts/install.py

# Install everything missing
python3 ~/.claude/skills/credentials/scripts/install.py --all

# Auth all CLIs interactively
bash ~/.claude/skills/credentials/scripts/auth.sh

# Show auth status
bash ~/.claude/skills/credentials/scripts/auth.sh --list
```

## What Gets Checked (32)

### Runtime CLIs (4)

| Check | Validation |
|-------|------------|
| `git` | `--version` |
| `node` | `--version` |
| `pnpm` | `--version` |
| `python3` | `--version` |

### CLI Auth (7) — checked via CLI whoami

| Check | CLI command | Install |
|-------|------------|---------|
| `gh` | `gh auth status` | `brew install gh` |
| `railway_cli` | `railway whoami` | `brew install railwayapp/tap/railway` |
| `vercel_cli` | `vercel whoami` | `npm install -g vercel` |
| `linear_cli` | `linear me` | `brew install schpet/tap/linear` |
| `supabase_cli` | `supabase projects list` | `brew install supabase/tap/supabase` |
| `render_cli` | `render whoami` | `brew tap render-oss/render && brew install render` |
| `docker` | `docker info` | `brew install --cask docker` |

### API Tokens (10) — no CLI, live HTTP whoami

| Check | Env var | File | Whoami |
|-------|---------|------|--------|
| `openai_token` | `OPENAI_API_KEY` | `.openai_token` | `GET /v1/models` |
| `anthropic_token` | `ANTHROPIC_API_KEY` | `.anthropic_token` | `GET /v1/models` |
| `gemini_token` | `GEMINI_API_KEY` | `.gemini_token` | `GET /v1beta/models` |
| `xai_token` | `XAI_API_KEY` | `.xai_token` | `GET /v1/models` |
| `perplexity_token` | `PERPLEXITY_KEY` | `.perplexity_token` | `POST /chat/completions` |
| `meta_token` | `META_ACCESS_TOKEN` | `.meta_token` | `GET /v21.0/me` |
| `manychat_token` | `MANYCHAT_TOKEN` | `.manychat_token` | `GET /fb/page/getInfo` |
| `telegram_token` | `TELEGRAM_BOT_TOKEN` | `.telegram_bot_token` | `GET /bot{token}/getMe` |
| `brave_token` | `BRAVE_API_KEY` | `.brave_token` | `GET /web/search` |
| `zoom` | `ZOOM_ACCESS_TOKEN` | `.zoom_token` | `GET /v2/users/me` |

### CLI-first (prefer CLI, fall back to API token) (4)

| Check | CLI whoami | Fallback |
|-------|-----------|----------|
| `twilio` | `twilio profiles:list` | API token check |
| `elevenlabs` | `elevenlabs auth whoami` | API token check |
| `mailerlite` | `mailerlite account list` | API token check |
| `posthog` | `posthog-cli query` | API token check |

### Google Suite (7) — gog CLI manages OAuth

| Check | What's tested |
|-------|---------------|
| `google_oauth` | `gog auth list --check` |
| `ga4` | GA4 Data API sessions report |
| `gsc` | Search Console site list |
| `gcal` | Calendar primary info |
| `gdrive` | Drive user info |
| `gmail` | Gmail profile |
| `skool` | Cookie file + age + gmail dependency |

## Credential Directory

Platform-aware: `$OPENCLAW_CRED_DIR` > `/data/.clawdbot` (container) > `~/.clawdbot` (Mac)

```
~/.clawdbot/                        # chmod 700
├── .github_token                   # ghp_...
├── .meta_token                     # EAA... (Meta/Instagram)
├── .linear_token                   # lin_api_...
├── .linear_webhook_secret          # Linear webhook HMAC
├── .openai_token                   # sk-...
├── .anthropic_token                # sk-ant-...
├── .xai_token                      # xai-...
├── .gemini_token                   # AI Studio key
├── .perplexity_token               # pplx-...
├── .railway_token
├── .vercel_token
├── .twilio_sid + .twilio_token
├── .google_analytics_token.json    # Legacy — gog CLI manages tokens now
├── .google_client_secret           # Legacy — gog stores client creds
├── .shopify.json                   # {shop, access_token, client_id, client_secret}
├── .stripe_token                   # sk_live_... or sk_test_...
├── .discord_token                  # Bot token (MTQ3...)
├── .notion_token                   # ntn_...
├── .kumello_token                  # Kumello API key
├── .gamma_token                    # Gamma API key
├── .manychat_token
├── .telegram_bot_token
├── .elevenlabs_token
├── .brave_token
├── .mailerlite_token
├── .posthog_token
├── .zoom_account_id + .zoom_client_id + .zoom_client_secret
├── .twitter_api_key + .twitter_api_secret  # Twitter/X OAuth
├── .twitter_access_token + .twitter_access_secret
├── .twitter_bearer_token
├── .linkedin_access_token + .linkedin_person_urn
├── .tiktok_access_token
├── .youtube_access_token + .youtube_refresh_token  # YouTube upload OAuth
├── .youtube_client_id + .youtube_client_secret
├── .openclaw_gateway_token         # Gateway/webhook auth
└── cookies/
    ├── youtube.txt                 # Netscape cookies for yt-dlp
    └── skool-cookies.json
```

## Auth Methods by Service

| Service | Primary auth | Fallback |
|---------|-------------|----------|
| GitHub | `gh` CLI | token file |
| Railway | `railway` CLI | token file |
| Vercel | `vercel` CLI | token file |
| Linear | `linear` CLI | token file |
| Google (GA4/GSC/Cal/Drive/Gmail) | `gog` CLI | token file |
| Shopify | `shopify.py` CLI | `.shopify.json` |
| Twilio | `twilio` CLI | token file |
| ElevenLabs | `elevenlabs` CLI | token file |
| MailerLite | `mailerlite` CLI | token file |
| PostHog | `posthog-cli` | token file |
| Skool | browser cookies + Gmail (for login codes) | — |
| Discord | bot token (config) | token file |
| Stripe | token file / env var | — |
| Twitter/X | 5-part OAuth (API key/secret + access token/secret + bearer) | token files |
| LinkedIn | access token + person URN | token files |
| TikTok | access token | token file |
| YouTube (uploads) | OAuth (client ID/secret + refresh token) | token files |
| Zoom | 3-part S2S (account ID + client ID + client secret) | token files |
| OpenAI, Anthropic, Gemini, xAI, Perplexity, Meta, ManyChat, Telegram, Brave, Notion, Kumello, Gamma | token file / env var | — |

## Skill Structure

```
skills/credentials/
├── SKILL.md                        # This file
├── scripts/
│   ├── check_local.py              # 32 local Mac checks
│   ├── check_all.py                # 21 container checks
│   ├── install.py                  # CLI installer wizard
│   └── auth.sh                     # Interactive auth wizard
└── references/
    └── fix-guide.md                # Per-credential fix instructions
```
