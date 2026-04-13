# Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes — keep `SKILL.md` and `gemini-extension.json` versions in sync
4. Run `python3 credentials/scripts/check_local.py --help` to confirm scripts still load
5. Open a PR against `main`

All shell scripts must be executable and have a `#!/usr/bin/env bash` shebang. All Python scripts target Python 3.9+ and must avoid non-stdlib imports unless guarded with a fallback.
