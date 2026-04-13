# Changelog

## [Unreleased]

## [0.2.0] — 2026-04-13

ship-engine GTM pipeline migrated from private workspace.

- `engine/` — full 8-stage GTM pipeline: validate → strategy → awareness → lead-capture → nurture → closing → launch → measure
- `engine/SKILL.md` — ship skill definition (name: ship, triggers, metadata)
- `engine/WORKFLOW.md` — canonical pipeline spec (decisions, gate logic, blackboard protocol)
- `supervisors/` — 10 supervisor SKILL.md files (engine + 9 stage supervisors)
- All hardcoded `/data/` paths replaced with env-var-first lookups (`LINEAR_API_KEY`, `SHIP_RUNS_DIR`, `CLAWDBOT_DIR`, etc.)
- `.env.example` added for all configurable variables
- Credentials preflight wires into team spawn gate (see SKILL.md § Team Credential Gate)

## [0.1.0] — 2026-04-13

Initial release. Ships the `credentials` preflight skill extracted from Max Techera's private workspace.

- Declarative check registry (`credentials/registry/core.yml`) covering 30+ integrations
- `SHIP_CRED_DIR` / `SHIP_EXTENSIONS_DIR` configuration
- Fallback chain for existing OpenClaw workspaces (`OPENCLAW_CRED_DIR`, `/data/.clawdbot`, `~/.clawdbot`)
- Python 3.9+ stdlib-only `check_local.py`; container-aware `check_all.py`
- Install/auth wizards (`install.py`, `auth.sh`)
- Extension pattern with Kumello example under `docs/extensions/`
