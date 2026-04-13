# Changelog

## [Unreleased]

## [0.1.0] — 2026-04-13

Initial release. Ships the `credentials` preflight skill extracted from Max Techera's private workspace.

- Declarative check registry (`credentials/registry/core.yml`) covering 30+ integrations
- `SHIP_CRED_DIR` / `SHIP_EXTENSIONS_DIR` configuration
- Fallback chain for existing OpenClaw workspaces (`OPENCLAW_CRED_DIR`, `/data/.clawdbot`, `~/.clawdbot`)
- Python 3.9+ stdlib-only `check_local.py`; container-aware `check_all.py`
- Install/auth wizards (`install.py`, `auth.sh`)
- Extension pattern with Kumello example under `docs/extensions/`
