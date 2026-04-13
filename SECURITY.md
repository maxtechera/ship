# Security

## Reporting

Report security vulnerabilities via GitHub Issues or email.

## Scope

- Scripts run locally with user permissions
- Credentials stay on disk under `$SHIP_CRED_DIR` (default `~/.config/ship/credentials`); nothing is transmitted except the whoami probes each check defines
- Fix-command output prints paths containing `$HOME` — safe to paste into a terminal, but review before running
