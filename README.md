# /credentials

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](CHANGELOG.md)

**Your deployment just failed because a token expired. /credentials catches that before you push.**

```
/plugin marketplace add maxtechera/ship
```
```bash
clawhub install ship
```

Zero config. GitHub, Railway, Vercel, and Supabase CLI checks work immediately. Run once and the setup wizard configures the rest in 30 seconds.

---

Agents fail silently on bad credentials. A missing `ANTHROPIC_API_KEY`, an expired GitHub token, a Railway login that timed out — any one of these can block a deploy, and you won't know until it's already failing in production.

/credentials checks all of it before you push. 30+ integrations, colored ✅/❌/⚠️ output, and fix commands for everything that's broken.

```
python3 ~/.claude/skills/ship/credentials/scripts/check_local.py
```

## What it catches

### Runtime CLIs (4)
`git`, `node`, `pnpm`, `python3` — version probe.

### CLI Auth (7) — checked via whoami
`gh`, `railway`, `vercel`, `linear`, `supabase`, `render`, `docker`

### API Tokens (10) — live HTTP check
OpenAI, Anthropic, Gemini, xAI, Perplexity, Meta, ManyChat, Telegram, Brave, Zoom

### CLI-first with API fallback (4)
Twilio, ElevenLabs, MailerLite, PostHog

### Google Suite (7) — gog CLI manages OAuth
`google_oauth`, `ga4`, `gsc`, `gcal`, `gdrive`, `gmail`, `skool`

## What people use it for

**Before a deploy.** `python3 credentials/scripts/check_local.py --quiet` — only shows failures. 3 seconds, no noise. Know your stack is clean before CI starts.

**When a pipeline breaks.** `python3 credentials/scripts/check_local.py --fix` — prints the exact shell commands to regenerate every expired token. Copy, paste, done.

**When setting up a new machine.** `python3 credentials/scripts/install.py --all` — installs every missing CLI via brew/npm without asking. Then `bash credentials/scripts/auth.sh` to re-auth all of them interactively.

**When one thing is broken.** `python3 credentials/scripts/check_local.py --only github` — scope to a single check. `--json` for automation.

## How it works

1. **Run the check.** `check_local.py` reads credentials from `$SHIP_CRED_DIR` (default: `~/.config/ship/credentials`).
2. **Colored output.** ✅ pass, ❌ fail, ⚠️ warning — one line per check.
3. **Get fix commands.** `--fix` prints the exact command to regenerate each failing credential.
4. **Add your own checks.** Drop a `*.yml` file into `$SHIP_CRED_DIR/extensions/` to add workspace-specific integrations. No code required.

## Install

### Claude Code
```
/plugin marketplace add maxtechera/ship
```

### ClawHub
```bash
clawhub install ship
```

### Manual (Claude Code)
```bash
git clone https://github.com/maxtechera/ship.git ~/.claude/skills/ship
```

### Gemini CLI
```bash
gemini extensions install maxtechera/ship
```

### Codex CLI
```bash
git clone https://github.com/maxtechera/ship.git ~/.agents/skills/ship
```

## Configuration

Credentials are read from the first matching location:

| Priority | Path |
|---|---|
| 1 | `$SHIP_CRED_DIR` |
| 2 | `$OPENCLAW_CRED_DIR` (legacy alias) |
| 3 | `/data/.clawdbot` (existing container) |
| 4 | `~/.clawdbot` (existing legacy) |
| 5 | `~/.config/ship/credentials` (default) |

Set `$SHIP_CRED_DIR` to point anywhere. Token files live inside: `.github_token`, `.openai_token`, `.anthropic_token`, etc.

## Extend

Drop a `*.yml` file into `$SHIP_CRED_DIR/extensions/` to add workspace-specific checks:

```yaml
version: 1
checks:
  - id: my_service
    category: api-token
    detect:
      env: MY_SERVICE_TOKEN
      token_file: .my_service_token
      whoami:
        url: https://api.my-service.com/me
        auth: "header:Bearer"
    fix:
      summary: "Paste new My Service token"
      template: "echo 'tok_...' > {cred_dir}/.my_service_token && chmod 600 {cred_dir}/.my_service_token"
```

See [docs/extensions/my-service.yml.example](docs/extensions/my-service.yml.example) for a working sample.

## ship-engine (v0.2 — in progress)

Not yet published. When it lands: `ship start "<idea>"` kicks off the full GTM pipeline — Intake → Validate → Strategy → Awareness → Lead Capture → Nurture → Closing → **Launch** → Measure. LAUNCH invokes credentials preflight before deploy.

## Open source

MIT. No tracking. No analytics. Your credentials stay on your machine.

See [CHANGELOG.md](CHANGELOG.md) for version history.
