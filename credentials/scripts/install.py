#!/usr/bin/env python3
"""
credentials/scripts/install.py

Idempotent installer for all credential CLIs and dependencies.
Interactive wizard lets you pick what to install, or --all to install everything.

Usage:
  python3 install.py              # Interactive wizard
  python3 install.py --all        # Install everything missing
  python3 install.py --list       # Show what's installed vs missing
  python3 install.py --only node  # Install a single item

Exit code: 0 = success, 1 = any failures
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# ─── ANSI ────────────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

OK   = f"{GREEN}✅{RESET}"
MISS = f"{RED}❌{RESET}"
SKIP = f"{DIM}⏭ {RESET}"


# ─── Credential directory ────────────────────────────────────────────────────

def _default_cred_dir() -> str:
    """Resolve credential directory with priority:
    SHIP_CRED_DIR → OPENCLAW_CRED_DIR (legacy) → /data/.clawdbot (container)
    → ~/.clawdbot (legacy) → ~/.config/ship/credentials (default)
    """
    explicit = os.environ.get("SHIP_CRED_DIR")
    if explicit:
        return explicit
    legacy = os.environ.get("OPENCLAW_CRED_DIR")
    if legacy:
        return legacy
    if Path("/data/.clawdbot").exists():
        return "/data/.clawdbot"
    legacy_home = Path.home() / ".clawdbot"
    if legacy_home.exists():
        return str(legacy_home)
    return str(Path.home() / ".config" / "ship" / "credentials")

CRED_DIR = _default_cred_dir()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def is_installed(cmd: str) -> bool:
    try:
        r = subprocess.run(["which", cmd], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def run(cmd: str, desc: str) -> bool:
    print(f"  {CYAN}→{RESET} {desc}")
    print(f"    {DIM}$ {cmd}{RESET}")
    r = subprocess.run(cmd, shell=True, timeout=300)
    if r.returncode == 0:
        print(f"    {OK} done")
        return True
    else:
        print(f"    {RED}failed (exit {r.returncode}){RESET}")
        return False


# ─── Install Registry ────────────────────────────────────────────────────────
# Each entry: (name, check_cmd, install_cmd, description, category)

REGISTRY = [
    # ── Runtime ──
    ("node",         "node",         "brew install node",
     "Node.js runtime", "runtime"),
    ("pnpm",         "pnpm",         "npm install -g pnpm",
     "Fast Node package manager", "runtime"),
    ("python3",      "python3",      "brew install python3",
     "Python runtime", "runtime"),

    # ── CLI Auth (platform CLIs) ──
    ("gh",           "gh",           "brew install gh",
     "GitHub CLI", "cli"),
    ("railway",      "railway",      "brew install railwayapp/tap/railway",
     "Railway CLI", "cli"),
    ("vercel",       "vercel",       "npm install -g vercel",
     "Vercel CLI", "cli"),
    ("linear",       "linear",       "brew install schpet/tap/linear",
     "Linear CLI", "cli"),
    ("supabase",     "supabase",     "brew install supabase/tap/supabase",
     "Supabase CLI", "cli"),
    ("render",       "render",       "brew tap render-oss/render && brew install render",
     "Render CLI", "cli"),
    ("docker",       "docker",       "brew install --cask docker",
     "Docker Desktop", "cli"),

    # ── CLI Auth (API CLIs with whoami) ──
    ("twilio",       "twilio",       "brew tap twilio/brew && brew install twilio",
     "Twilio CLI", "api-cli"),
    ("elevenlabs",   "elevenlabs",   "npm install -g @elevenlabs/cli",
     "ElevenLabs CLI", "api-cli"),
    ("mailerlite",   "mailerlite",   "go install github.com/mailerlite/mailerlite-cli@latest",
     "MailerLite CLI (requires Go)", "api-cli"),
    ("posthog-cli",  "posthog-cli",  "npm install -g @posthog/cli",
     "PostHog CLI", "api-cli"),

    ("notion",       "notion",       "brew install 4ier/tap/notion-cli",
     "Notion CLI", "cli"),
    ("stripe",       "stripe",       "brew install stripe/stripe-cli/stripe",
     "Stripe CLI", "cli"),
    ("shopify",      "shopify",      "npm install -g @shopify/cli",
     "Shopify CLI", "cli"),

    # ── AI CLIs ──
    ("codex",        "codex",        "brew install --cask codex",
     "OpenAI Codex CLI", "api-cli"),
    ("gemini",       "gemini",       "brew install gemini-cli",
     "Google Gemini CLI", "api-cli"),

    # ── Google (gog CLI manages OAuth for GA4/GSC/Calendar/Drive/Gmail) ──
    ("gog",          "gog",          "brew install gogcli",
     "Google OAuth CLI (Gmail, Calendar, Drive, Sheets, Contacts)", "google"),

    # ── Credential directory ──
    ("cred-dir",     None,           None,
     f"Credential store directory ({CRED_DIR})", "setup"),
]


def check_item(name, check_cmd):
    """Return True if installed/exists."""
    if name == "cred-dir":
        return Path(CRED_DIR).exists()
    if check_cmd:
        return is_installed(check_cmd)
    return False


def install_item(name, install_cmd) -> bool:
    """Install a single item. Returns True on success."""
    if name == "cred-dir":
        cred = Path(CRED_DIR)
        cred.mkdir(mode=0o700, parents=True, exist_ok=True)
        (cred / "cookies").mkdir(mode=0o700, exist_ok=True)
        print(f"  {OK} Created {cred} (mode 700)")
        return True

    if not install_cmd:
        print(f"  {RED}No install command for {name}{RESET}")
        return False

    # Check dependencies
    if name == "pnpm" and not is_installed("npm"):
        print(f"  {YELLOW}Skipping pnpm — npm not available (install node first){RESET}")
        return False
    if name in ("vercel", "elevenlabs", "posthog-cli") and not is_installed("npm"):
        print(f"  {YELLOW}Skipping {name} — npm not available (install node first){RESET}")
        return False
    if name == "mailerlite" and not is_installed("go"):
        print(f"  {YELLOW}Skipping mailerlite — Go not installed (brew install go){RESET}")
        return False

    return run(install_cmd, f"Installing {name}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Install credential CLIs and dependencies.")
    parser.add_argument("--all", action="store_true", help="Install everything missing")
    parser.add_argument("--list", action="store_true", help="List install status")
    parser.add_argument("--only", metavar="NAME", help="Install a single item")
    args = parser.parse_args()

    # Build status
    items = []
    for name, check_cmd, install_cmd, desc, cat in REGISTRY:
        installed = check_item(name, check_cmd)
        items.append({
            "name": name, "check": check_cmd, "install": install_cmd,
            "desc": desc, "cat": cat, "installed": installed,
        })

    # ── List mode ──
    if args.list:
        print(f"\n{BOLD}{'═' * 55}{RESET}")
        print(f"{BOLD}  📦 Credential CLI Install Status{RESET}")
        print(f"{DIM}  Credential dir: {CRED_DIR}{RESET}")
        print(f"{BOLD}{'═' * 55}{RESET}\n")
        current_cat = None
        for it in items:
            if it["cat"] != current_cat:
                current_cat = it["cat"]
                labels = {"runtime": "Runtime", "cli": "Platform CLIs",
                          "api-cli": "API CLIs", "google": "Google", "setup": "Setup"}
                print(f"\n  {CYAN}{labels.get(current_cat, current_cat)}{RESET}")
            ico = OK if it["installed"] else MISS
            print(f"  {ico} {BOLD}{it['name']:<16}{RESET} {it['desc']}")

        installed = sum(1 for i in items if i["installed"])
        missing = len(items) - installed
        print(f"\n{BOLD}{'─' * 55}{RESET}")
        print(f"  {OK} {installed} installed  {MISS} {missing} missing  ({len(items)} total)\n")
        return

    # ── Only mode ──
    if args.only:
        key = args.only.lower().replace("-", "").replace("_", "")
        match = None
        for it in items:
            if it["name"].replace("-", "").replace("_", "").replace("cred", "creddir") == key or \
               it["name"].replace("-", "").replace("_", "") == key:
                match = it
                break
        if not match:
            names = [i["name"] for i in items]
            print(f"Unknown: '{args.only}'. Available: {', '.join(names)}")
            sys.exit(2)
        if match["installed"]:
            print(f"{OK} {match['name']} already installed")
            return
        ok = install_item(match["name"], match["install"])
        sys.exit(0 if ok else 1)

    # ── All mode ──
    if args.all:
        missing = [i for i in items if not i["installed"]]
        if not missing:
            print(f"\n{OK} Everything is already installed!\n")
            return
        print(f"\n{BOLD}{'═' * 55}{RESET}")
        print(f"{BOLD}  📦 Installing {len(missing)} missing items{RESET}")
        print(f"{BOLD}{'═' * 55}{RESET}\n")
        ok = 0
        fail = 0
        for it in missing:
            success = install_item(it["name"], it["install"])
            if success:
                ok += 1
            else:
                fail += 1
            print()
        print(f"{BOLD}{'─' * 55}{RESET}")
        print(f"  {OK} {ok} installed  {MISS} {fail} failed\n")
        sys.exit(0 if fail == 0 else 1)

    # ── Interactive wizard ──
    missing = [i for i in items if not i["installed"]]
    installed_items = [i for i in items if i["installed"]]

    print(f"\n{BOLD}{'═' * 55}{RESET}")
    print(f"{BOLD}  📦 Credential CLI Install Wizard{RESET}")
    print(f"{DIM}  Credential dir: {CRED_DIR}{RESET}")
    print(f"{BOLD}{'═' * 55}{RESET}\n")

    if installed_items:
        print(f"  {DIM}Already installed:{RESET}")
        for it in installed_items:
            print(f"  {OK} {it['name']}")
        print()

    if not missing:
        print(f"  {GREEN}{BOLD}Everything is already installed!{RESET}\n")
        return

    print(f"  {BOLD}Missing ({len(missing)}):{RESET}\n")
    for idx, it in enumerate(missing):
        print(f"  [{idx + 1}] {it['name']:<16} {DIM}{it['desc']}{RESET}")

    print(f"\n  [a] Install all missing")
    print(f"  [q] Quit\n")

    try:
        choice = input(f"  {BOLD}Select (numbers separated by space, or 'a'):{RESET} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n  Cancelled.")
        return

    if choice == "q" or not choice:
        print("  Cancelled.")
        return

    if choice == "a":
        selected = missing
    else:
        indices = []
        for part in choice.replace(",", " ").split():
            try:
                idx = int(part) - 1
                if 0 <= idx < len(missing):
                    indices.append(idx)
            except ValueError:
                pass
        selected = [missing[i] for i in indices]

    if not selected:
        print("  No valid selection.")
        return

    print(f"\n  Installing {len(selected)} item(s)...\n")
    ok = 0
    fail = 0
    for it in selected:
        success = install_item(it["name"], it["install"])
        if success:
            ok += 1
        else:
            fail += 1
        print()

    print(f"{BOLD}{'─' * 55}{RESET}")
    print(f"  {OK} {ok} installed  {MISS} {fail} failed\n")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
