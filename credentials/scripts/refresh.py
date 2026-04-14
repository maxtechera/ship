#!/usr/bin/env python3
"""
credentials/scripts/refresh.py

Auto-refresh expiring tokens. Run via cron or manually.
Handles: Meta (60d→extend), MercadoLibre (6h→refresh), MercadoPago (180d→check).

Usage:
  python3 refresh.py              # Refresh all expiring tokens
  python3 refresh.py --only meta  # Refresh single token
  python3 refresh.py --check      # Check expiry without refreshing
  python3 refresh.py --json       # JSON output for automation

Exit code: 0 = all ok, 1 = any failures
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ─── Config ──────────────────────────────────────────────────────────────────

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

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

results = []


def record(name, status, message):
    results.append({"name": name, "status": status, "message": message})


def http_post(url, data, headers=None):
    """POST with form data or JSON, return (status, body_dict)."""
    if isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode()
    elif isinstance(data, str):
        data = data.encode()
    req = urllib.request.Request(url, data)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode() or "{}")
        except Exception:
            body = {}
        return e.code, body
    except Exception as e:
        return 0, {"_error": str(e)}


def http_get(url, headers=None):
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode() or "{}")
        except Exception:
            body = {}
        return e.code, body
    except Exception as e:
        return 0, {"_error": str(e)}


# ─── Meta Token Refresh ─────────────────────────────────────────────────────

def check_meta():
    """Check Meta token expiry."""
    token_path = Path(CRED_DIR) / ".meta_token"
    token = token_path.read_text().strip() if token_path.exists() else ""
    if not token:
        return {"status": "missing", "days_left": -1}

    code, body = http_get(
        f"https://graph.facebook.com/debug_token?input_token={token}&access_token={token}")
    if code != 200:
        return {"status": "error", "days_left": -1}

    data = body.get("data", {})
    expires = data.get("expires_at", 0)
    if not expires:
        return {"status": "never_expires", "days_left": 999}

    days_left = (expires - time.time()) / 86400
    return {"status": "ok", "days_left": int(days_left), "expires_at": expires}


def refresh_meta(check_only=False):
    """Extend Meta token to long-lived (60 days)."""
    name = "meta"
    info = check_meta()

    if info["status"] == "missing":
        record(name, "skip", "no token")
        return
    if info["status"] == "never_expires":
        record(name, "ok", "token never expires")
        return

    days = info["days_left"]
    if days > 14:
        record(name, "ok", f"{days} days remaining — no refresh needed")
        return

    if check_only:
        if days <= 0:
            record(name, "fail", f"EXPIRED ({days} days)")
        elif days <= 7:
            record(name, "warn", f"{days} days remaining — refresh soon")
        else:
            record(name, "ok", f"{days} days remaining")
        return

    # Attempt to extend
    app_secret_path = Path(CRED_DIR) / ".meta_app_secret"
    app_id_path = Path(CRED_DIR) / ".meta_app_id"
    app_secret = app_secret_path.read_text().strip() if app_secret_path.exists() else ""
    app_id = app_id_path.read_text().strip() if app_id_path.exists() else ""

    if not app_secret or not app_id:
        record(name, "fail",
               f"{days} days left — cannot refresh without .meta_app_id + .meta_app_secret")
        return

    token = (Path(CRED_DIR) / ".meta_token").read_text().strip()
    code, body = http_get(
        f"https://graph.facebook.com/v21.0/oauth/access_token?"
        f"grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}"
        f"&fb_exchange_token={token}")

    if code == 200 and "access_token" in body:
        new_token = body["access_token"]
        token_path = Path(CRED_DIR) / ".meta_token"
        token_path.write_text(new_token)
        token_path.chmod(0o600)
        new_info = check_meta()
        record(name, "ok", f"refreshed — {new_info['days_left']} days remaining")
    else:
        err = body.get("error", {}).get("message", str(body)[:80])
        record(name, "fail", f"refresh failed: {err}")


# ─── MercadoLibre Token Refresh ─────────────────────────────────────────────

def check_mercadolibre():
    """Check ML token — always needs refresh (6h)."""
    ml_path = Path(CRED_DIR) / ".mercadolibre.json"
    if not ml_path.exists():
        return {"status": "missing"}
    data = json.loads(ml_path.read_text())
    token = data.get("access_token", "")
    if not token:
        return {"status": "missing"}
    # Test the token
    code, body = http_get("https://api.mercadolibre.com/users/me",
                          headers={"Authorization": f"Bearer {token}"})
    if code == 200:
        return {"status": "ok", "user": body.get("nickname", "?")}
    return {"status": "expired"}


def refresh_mercadolibre(check_only=False):
    """Refresh MercadoLibre token using refresh_token."""
    name = "mercadolibre"
    ml_path = Path(CRED_DIR) / ".mercadolibre.json"
    if not ml_path.exists():
        record(name, "skip", "no .mercadolibre.json")
        return

    data = json.loads(ml_path.read_text())
    info = check_mercadolibre()

    if info["status"] == "ok" and check_only:
        record(name, "ok", f"token valid ({info.get('user', '?')})")
        return
    elif info["status"] == "ok":
        record(name, "ok", f"token still valid ({info.get('user', '?')})")
        return

    refresh_token = data.get("refresh_token", "")
    client_id = data.get("client_id", "")
    client_secret = data.get("client_secret", "")

    if not refresh_token:
        record(name, "fail", "expired — no refresh_token (re-auth needed via OAuth)")
        return

    if check_only:
        record(name, "warn", "token expired — has refresh_token, run without --check to refresh")
        return

    code, body = http_post("https://api.mercadolibre.com/oauth/token", {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    })

    if code == 200 and "access_token" in body:
        data["access_token"] = body["access_token"]
        data["refresh_token"] = body.get("refresh_token", "")
        data["expires_in"] = body.get("expires_in")
        json.dump(data, open(str(ml_path), "w"), indent=2)
        ml_path.chmod(0o600)
        record(name, "ok", f"refreshed — {body.get('expires_in', 0) // 3600}h")
    else:
        err = body.get("message", body.get("error", str(body)[:80]))
        record(name, "fail", f"refresh failed: {err}")


# ─── MercadoPago Token Check ────────────────────────────────────────────────

def refresh_mercadopago(check_only=False):
    """Check MP token validity (180 day tokens, rarely expire)."""
    name = "mercadopago"
    token_path = Path(CRED_DIR) / ".mercadopago_token"
    if not token_path.exists():
        record(name, "skip", "no token")
        return

    token = token_path.read_text().strip()
    code, body = http_get("https://api.mercadopago.com/users/me",
                          headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "nickname" in body:
        record(name, "ok", f"valid ({body['nickname']})")
    elif code == 401:
        record(name, "fail", "expired — re-auth at mercadopago.com/developers")
    else:
        record(name, "warn", f"HTTP {code}")


# ─── Registry ───────────────────────────────────────────────────────────────

REFRESHABLE = {
    "meta": refresh_meta,
    "mercadolibre": refresh_mercadolibre,
    "mercadopago": refresh_mercadopago,
}


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auto-refresh expiring tokens.")
    parser.add_argument("--only", metavar="NAME", help="Refresh single token")
    parser.add_argument("--check", action="store_true", help="Check expiry only, don't refresh")
    parser.add_argument("--json", action="store_true", dest="json_out", help="JSON output")
    args = parser.parse_args()

    targets = REFRESHABLE
    if args.only:
        key = args.only.lower()
        if key not in REFRESHABLE:
            print(f"Unknown: {args.only}. Available: {', '.join(REFRESHABLE.keys())}")
            sys.exit(2)
        targets = {key: REFRESHABLE[key]}

    if not args.json_out:
        print(f"\n{BOLD}{'═' * 55}{RESET}")
        print(f"{BOLD}  🔄 Token Refresh{'  (check only)' if args.check else ''}{RESET}")
        print(f"{DIM}  Credential dir: {CRED_DIR}{RESET}")
        print(f"{BOLD}{'═' * 55}{RESET}\n")

    for name, fn in targets.items():
        try:
            fn(check_only=args.check)
        except Exception as e:
            record(name, "fail", f"exception: {e}")

    if args.json_out:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            ico = {"ok": f"{GREEN}✅{RESET}", "fail": f"{RED}❌{RESET}",
                   "warn": f"{YELLOW}⚠️ {RESET}", "skip": f"{DIM}⏭ {RESET}"}.get(r["status"], "?")
            print(f"  {ico} {BOLD}{r['name']}{RESET}: {r['message']}")

        failed = sum(1 for r in results if r["status"] == "fail")
        print(f"\n{BOLD}{'─' * 55}{RESET}")
        if failed:
            print(f"  {RED}{failed} token(s) need attention{RESET}\n")
        else:
            print(f"  {GREEN}All tokens healthy{RESET}\n")

    sys.exit(1 if any(r["status"] == "fail" for r in results) else 0)


if __name__ == "__main__":
    main()
