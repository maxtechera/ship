# Ship

End-to-end GTM pipeline + credentials preflight. Opensource Claude Code skill.

**v0.1** ships the `credentials` preflight — a zero-dependency Python health check for your local CLI auth and API tokens. **v0.2** will add `ship-engine` (the full idea → validate → build → market → sell → measure pipeline) and its 9 stage supervisors.

If you're here for the credential check, jump to [Credentials](#credentials).

---

## Install

**Claude Code**

```
/plugin marketplace add maxtechera/ship
/plugin install ship@ship
```

**Manual**

```bash
git clone https://github.com/maxtechera/ship.git ~/.claude/skills/ship-src
ln -s ~/.claude/skills/ship-src/credentials ~/.claude/skills/credentials
```

**OpenCode / ClawHub**

```bash
git clone https://github.com/maxtechera/ship.git ~/.agents/skills/ship-src
ln -s ~/.agents/skills/ship-src/credentials ~/.agents/skills/credentials
```

**Gemini CLI**

```bash
gemini extensions install maxtechera/ship
```

---

## Credentials

A declarative health check for the CLIs and API tokens your agents rely on. Covers 30+ common integrations out of the box — GitHub, Vercel, Railway, Render, Linear, Supabase, Twilio, ElevenLabs, MailerLite, PostHog, Meta, ManyChat, Brave, Perplexity, OpenAI, Anthropic, Gemini, xAI, Google OAuth (via `gog`), and more.

### Quick start

```bash
python3 ~/.claude/skills/credentials/scripts/check_local.py
```

You'll see colored ✅/❌/⚠️ for each check. Run with `--fix` to print shell commands that regenerate missing credentials. `--json` outputs machine-readable for automation. `--only <id>` scopes to one check.

### Configure

Credentials are read from a local directory — default `~/.config/ship/credentials` — containing token files (`.github_token`, `.meta_token`, etc.). Override with:

```bash
export SHIP_CRED_DIR="$HOME/.my-creds"
```

### Extend

Drop a `YAML` file into `$SHIP_CRED_DIR/extensions/` (or `$SHIP_EXTENSIONS_DIR/`) to add workspace-specific checks. See [`credentials/extensions/README.md`](credentials/extensions/README.md) and [`docs/extensions/my-service.yml.example`](docs/extensions/my-service.yml.example).

---

## Ship-engine (v0.2 — in progress)

Not yet published. When it lands:

- `ship start "<idea>"` — kick off the intake supervisor
- Stages: Intake → Validate → Strategy → Awareness → Lead Capture → Nurture → Closing → **Launch** → Measure
- LAUNCH stage invokes credentials preflight before allowing deploy

---

## License

MIT — see [LICENSE](LICENSE).
