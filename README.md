# /ship

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](CHANGELOG.md)

**Run `/ship` once. A coordinator team spawns, the dashboard renders, and work starts moving.**

**Open source first, demo first. Install `/ship`, see the workflow, then join the course waitlist if you want the full operating system.**

Claude Code:
```
/plugin marketplace add maxtechera/ship
```

OpenClaw:
```bash
clawhub install ship
```

Requires [orchestrator](https://github.com/maxtechera/orchestrator) — ship uses orchestrator's agent team coordination, loop mechanics, and verification harness. Ship adds the GTM pipeline, credential gate, and domain roster.

---

A 9-agent GTM team boots on first run. The coordinator reads your Linear tickets, routes each active run to the right specialist by stage, and keeps every agent busy. The critic blocks every gate — fresh context, never sees the executor's work log, 100-pt rubric. The analyst runs pre-publish hook scoring before critic final approval, not just post-launch.

**The pipeline:** idea → validate → strategy → awareness → lead-capture → nurture → closing → launch → measure

**Every deploy is credential-gated.** `check_local.py` covers 30+ integrations. Missing token = blocked run, not a mid-sprint surprise.

---

## Commands

| Command | Description |
|---------|-------------|
| `/ship` | Spawn coordinator team + render live dashboard of all active runs |
| `/ship create "<idea>"` | Create Linear run ticket, preflight credentials, hand off to engine |
| `/ship status [RUN-ID]` | Stage + last update + blocked items for an active run |
| `/ship run <RUN-ID>` | Resume an existing run |

## Install

### Claude Code
```
/plugin marketplace add maxtechera/ship
```

### Update
```
claude plugin update ship@ship
```

### OpenClaw
```bash
clawhub install ship
```

### Manual
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

---

## The Team

Coordination (TeamCreate, zero-idle, loop) is provided by [orchestrator](https://github.com/maxtechera/orchestrator). Ship provides the GTM roster and domain prompts.

Nine pre-defined roles. Coordinator assigns on every loop tick.

| Agent | Coverage | Notes |
|-------|----------|-------|
| `coordinator` | All stages — routes + assigns | Reads Linear, zero-idle |
| `critic` | All gates + verified advances | v3 rubric (100-pt, ≥75 threshold), one-revise-max, fresh context only |
| `strategist` | Intake → Validate → Strategy | Blackboard keys: `intake.*`, `validate.*`, `strategy.*` |
| `content` | Awareness (all 17 sub-skills) | Carousel 1080×1350, reel hook 0-3s, newsletter ≤50 chars |
| `growth` | Lead Capture (UTM, GA4, A/B) | UTM required before campaign; A/B needs ≥400 control recipients |
| `nurture` | Nurture sequences + MailerLite | OSS Nurture Mode for `oss_tool` runs |
| `closer` | Closing (sales/course pages) | OSS Closing Mode for `oss_tool` runs |
| `launcher` | Launch readiness + directories | Runs credentials preflight before every deploy action |
| `analyst` | 3-stream: viral library + hook scoring + post-launch tracking | Pre-publish gate participant, not async-only |

**Dynamic roles** — coordinator spawns as needed: `researcher`, `seo-specialist`, `outreach`, `designer`.

### The analyst 3-stream model

- **Stream 1** (pre-launch): seed viral pattern library per wave before content starts the bundle
- **Stream 2** (pre-publish gate): score every surface hook against library (0-10 pattern match + predicted engagement band). Default step: hook-vocab audit — grep bundle for category-native phrases, flag mismatches. Feed results to critic before final approval.
- **Stream 3** (async post-launch): T+24h / T+7d / T+30d actuals → update Linear ticket, flag underperformers

### The critic v3 rubric

100-pt, 10 categories × 10. Threshold ≥75 to approve. One revise pass max.

| # | Category |
|---|----------|
| 1 | Brand voice |
| 2 | Audience fit |
| 3 | Hook strength (STEPPS ≥3/6, VE ≥100, pattern library match) |
| 4 | CTA + Hormozi two-part rule (Action + Reason-for-now) |
| 5 | Offer framing (value stack, risk reversal, urgency, dream outcome) |
| 6 | Structural completeness |
| 7 | Guide alignment (vs research guide) |
| 8 | Human-sounding (zero Tier-1 AI words, varied sentence length) |
| 9 | Format craft (platform-specific: carousel cadence, reel first-10s, HN no-emoji) |
| 10 | Verbatim/specificity (real numbers, receipts over claims) |

When analyst Stream-2 avg ≥7 and band mid/high, critic uses Stream-2 score ±1 for category 3 — no double-scoring.

---

## Credential Preflight

Every deploy action gates on credential health. Run manually anytime:

```bash
# Check everything
python3 credentials/scripts/check_local.py

# Only failures
python3 credentials/scripts/check_local.py --quiet

# With fix commands
python3 credentials/scripts/check_local.py --fix

# Scope to specific services
python3 credentials/scripts/check_local.py --only "github,railway,vercel,openai,anthropic"

# JSON output for automation
python3 credentials/scripts/check_local.py --json
```

Exit 0 = all pass. Exit 1 = failures — prints `fix_cmd` per failure.

### What gets checked

| Category | Services |
|----------|----------|
| Runtime CLIs (4) | `git`, `node`, `pnpm`, `python3` |
| CLI Auth (7) | `gh`, `railway`, `vercel`, `linear`, `supabase`, `render`, `docker` |
| API Tokens (10) | OpenAI, Anthropic, Gemini, xAI, Perplexity, Meta, ManyChat, Telegram, Brave, Zoom |
| CLI-first + fallback (4) | Twilio, ElevenLabs, MailerLite, PostHog |
| Google Suite (7) | `google_oauth`, `ga4`, `gsc`, `gcal`, `gdrive`, `gmail`, `skool` |

### Credential scripts

```bash
# Install all missing CLIs (idempotent)
python3 credentials/scripts/install.py --all

# Interactive auth wizard — shows status, offers to fix failures
bash credentials/scripts/auth.sh

# Check token expiry + auto-refresh (Meta 60d, MercadoLibre 6h, MercadoPago 180d)
python3 credentials/scripts/refresh.py --check
python3 credentials/scripts/refresh.py
```

**First-time setup:**

```bash
python3 credentials/scripts/install.py --all   # 1. Install CLIs
bash credentials/scripts/auth.sh               # 2. Authenticate
python3 credentials/scripts/check_local.py     # 3. Verify (should exit 0)
```

---

## Configuration

Credentials are read from the first matching location:

| Priority | Path |
|----------|------|
| 1 | `$SHIP_CRED_DIR` |
| 2 | `$OPENCLAW_CRED_DIR` (legacy alias) |
| 3 | `/data/.clawdbot` (existing container) |
| 4 | `~/.clawdbot` (existing legacy) |
| 5 | `~/.config/ship/credentials` (default) |

Set `$SHIP_CRED_DIR` to point anywhere. Token files live inside: `.github_token`, `.openai_token`, `.anthropic_token`, etc.

---

## Extend credentials

Drop a `*.yml` file into `$SHIP_CRED_DIR/extensions/` to register additional checks:

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

---

## What This Repo Contains

```
ship/
  SKILL.md                        # Core skill — the agent reads this
  credentials/
    SKILL.md                      # Credentials sub-skill
    scripts/
      check_local.py              # Preflight runner — JSON output, exit codes, --only filter
      install.py                  # Idempotent CLI installer
      auth.sh                     # Interactive auth wizard
      refresh.py                  # Auto-refresh expiring tokens
    registry/core.yml             # Declarative check index
    extensions/                   # Drop *.yml here to add custom checks
  supervisors/
    engine/SKILL.md               # Always-on control loop — reconciles Linear, delegates stages
    intake/SKILL.md
    validate/SKILL.md
    strategy/SKILL.md
    awareness/SKILL.md
    lead-capture/SKILL.md
    nurture/SKILL.md              # Includes OSS Nurture Mode
    closing/SKILL.md              # Includes OSS Closing Mode
    launch/SKILL.md               # Credential gate before every deploy
    measure/SKILL.md
  content/                        # 17 content sub-skills
```

---

## Demo-first CTA

- **Install `/ship`** to see the GTM pipeline move from intake to launch.
- **Follow the newsletter** for behind-the-scenes breakdowns, launch notes, and operating lessons.
- **Join the $497 course waitlist** if you want the full playbook, templates, and rollout system behind the demo.

## Principles

- Credentials gate before agents start, not mid-sprint
- The coordinator never idles — zero-idle rule applies to every specialist
- The critic never reads the executor's work log — fresh context only
- The analyst gates critic approval, not just post-launch measurement
- One revise pass max — don't block on perfectionism
- `oss_tool` runs follow a different conversion chain: GitHub install → newsletter → course

---

## License

MIT — see [LICENSE](LICENSE).

Maintained by [maxtechera](https://github.com/maxtechera).
