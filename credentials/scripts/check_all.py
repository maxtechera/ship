#!/usr/bin/env python3
"""
credentials/scripts/check_all.py

Verify, validate, and optionally fix all workspace credentials and integrations.

Usage:
  python3 check_all.py                  # Full check, report only
  python3 check_all.py --fix            # Check + print fix commands
  python3 check_all.py --only github    # Check a single credential
  python3 check_all.py --quiet          # Only print failures
  python3 check_all.py --json           # Output JSON (for automation)

Exit code: 0 = all pass, 1 = any failures
"""

import argparse
import json
import os
import subprocess
try:
    import requests
except ImportError:
    requests = None
import sys
import sqlite3
from pathlib import Path
from typing import Optional

# ─── Config ────────────────────────────────────────────────────────────────────

CLAWDBOT = Path(os.environ.get("OPENCLAW_CRED_DIR", "/data/.clawdbot"))
WORKSPACE = Path(os.environ.get("WORKSPACE_DIR",
    os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")))
OPENCLAW_JSON = CLAWDBOT / "openclaw.json"

# Try to import shared config for unified credential resolution
try:
    sys.path.insert(0, str(WORKSPACE / "tools"))
    from lib.config import get_credential, get_google_oauth_credentials
    HAS_SHARED_CONFIG = True
except ImportError:
    HAS_SHARED_CONFIG = False
    def get_credential(name, fallback=""):
        return fallback
    def get_google_oauth_credentials():
        return None

# ANSI colours
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

OK   = f"{GREEN}✅{RESET}"
FAIL = f"{RED}❌{RESET}"
WARN = f"{YELLOW}⚠️ {RESET}"

results: list[dict] = []


# ─── Helpers ───────────────────────────────────────────────────────────────────

def read_file(path: Path) -> Optional[str]:
    """Return file contents stripped, or None if missing/empty."""
    try:
        text = path.read_text().strip()
        return text if text else None
    except Exception:
        return None


def curl_json(url: str, headers: list[str] = None, data: str = None,
              method: str = "GET", timeout: int = 10) -> tuple[int, dict]:
    """Run a curl request, return (http_code, parsed_json_or_dict)."""
    cmd = ["curl", "-s", "-o", "/tmp/_cred_resp.json", "-w", "%{http_code}",
           "--max-time", str(timeout), "-X", method]
    if headers:
        for h in headers:
            cmd += ["-H", h]
    if data:
        cmd += ["-d", data]
    cmd.append(url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
        code = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        try:
            body = json.loads(Path("/tmp/_cred_resp.json").read_text())
        except Exception:
            body = {}
        return code, body
    except Exception as e:
        return 0, {"error": str(e)}


def run_cmd(cmd: list[str], cwd: str = None, timeout: int = 15) -> tuple[int, str, str]:
    """Run a command, return (returncode, stdout, stderr)."""
    try:
        env = os.environ.copy()
        # gog uses a file keyring backend in this runtime; non-interactive checks must
        # provide the password explicitly or valid auth will look broken.
        env.setdefault("GOG_KEYRING_PASSWORD", "openclaw")
        r = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=cwd or str(WORKSPACE), timeout=timeout, env=env)
        return r.returncode, _strip_ansi(r.stdout.strip()), _strip_ansi(r.stderr.strip())
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)


def _strip_ansi(s: str) -> str:
    """Remove ANSI escape sequences from a string."""
    import re
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


def record(name: str, status: str, message: str, fix: str = ""):
    """Record a result. status: 'ok', 'fail', 'warn'."""
    results.append({"name": name, "status": status, "message": message, "fix": fix})


def icon(status: str) -> str:
    return {"ok": OK, "fail": FAIL, "warn": WARN}.get(status, WARN)


# ─── Credential Checks ─────────────────────────────────────────────────────────

def check_github():
    name = "github"
    token = get_credential("github") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".github_token")
    if not token:
        record(name, "fail", "File missing or empty: .github_token",
               "echo 'ghp_YOUR_TOKEN' > /data/.clawdbot/.github_token && chmod 600 /data/.clawdbot/.github_token")
        return

    code, body = curl_json("https://api.github.com/user",
                           headers=[f"Authorization: token {token}",
                                    "Accept: application/vnd.github.v3+json"])
    if code == 200 and "login" in body:
        record(name, "ok", f"GitHub authenticated as @{body['login']}")
    elif code == 401:
        record(name, "fail", "GitHub token invalid (401)",
               "# Regenerate at: https://github.com/settings/tokens\n"
               "echo 'ghp_NEW_TOKEN' > /data/.clawdbot/.github_token")
    else:
        record(name, "warn", f"GitHub API returned {code}: {body.get('message', 'unknown')}")


def check_meta():
    name = "meta"
    token = get_credential("meta") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".meta_token")
    if not token:
        record(name, "fail", "File missing or empty: .meta_token",
               "# Get token from: https://developers.facebook.com/tools/explorer/\n"
               "echo 'EAA...' > /data/.clawdbot/.meta_token && chmod 600 /data/.clawdbot/.meta_token")
        return

    code, body = curl_json(f"https://graph.facebook.com/v21.0/me?access_token={token}")
    if code == 200 and "id" in body:
        record(name, "ok", f"Meta Graph authenticated as {body.get('name', body.get('id', '?'))}")
    elif code == 400 or code == 401 or "error" in body:
        err = body.get("error", {}).get("message", "unknown error")
        record(name, "fail", f"Meta token invalid: {err}",
               "# Get new long-lived token from Facebook Developer Console\n"
               "# https://developers.facebook.com/tools/explorer/\n"
               "echo 'EAA_NEW_TOKEN' > /data/.clawdbot/.meta_token")
    else:
        record(name, "warn", f"Meta API returned {code}")


def check_linear():
    name = "linear"
    token = get_credential("linear") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".linear_token")
    if not token:
        record(name, "fail", "File missing or empty: .linear_token",
               "echo 'lin_api_YOUR_TOKEN' > /data/.clawdbot/.linear_token && chmod 600 /data/.clawdbot/.linear_token")
        return

    query = '{"query":"{ viewer { id name email } }"}'
    auth_header = f"Bearer {token}" if token.startswith("lin_oauth") else token
    code, body = curl_json("https://api.linear.app/graphql",
                           headers=[f"Authorization: {auth_header}",
                                    "Content-Type: application/json"],
                           data=query, method="POST")
    if code == 200 and "data" in body and body["data"] and body["data"].get("viewer"):
        viewer = body["data"]["viewer"]
        record(name, "ok", f"Linear authenticated as {viewer.get('name', '?')} ({viewer.get('email', '?')})")
    elif code == 401 or "errors" in body:
        errs = body.get("errors", [{}])
        msg = errs[0].get("message", "unknown") if errs else "unknown"
        record(name, "fail", f"Linear token invalid: {msg}",
               "# Get token from: https://linear.app/settings/api\n"
               "echo 'lin_api_NEW_TOKEN' > /data/.clawdbot/.linear_token")
    else:
        record(name, "warn", f"Linear API returned {code}")


def check_linear_webhook_secret():
    name = "linear_webhook_secret"
    secret = get_credential("linear_webhook_secret") if HAS_SHARED_CONFIG else None
    if not secret:
        secret = read_file(CLAWDBOT / ".linear_webhook_secret")
    if secret:
        record(name, "ok", f"Linear webhook secret present ({len(secret)} chars)")
    else:
        record(name, "fail", "File missing or empty: .linear_webhook_secret",
               "# Generate a random secret:\n"
               "openssl rand -hex 32 > /data/.clawdbot/.linear_webhook_secret\n"
               "# Then update the webhook in Linear settings to use it")


def check_railway():
    name = "railway"
    token = get_credential("railway") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".railway_token")
    if not token:
        record(name, "fail", "File missing or empty: .railway_token",
               "# Get token from: https://railway.app/account/tokens\n"
               "echo 'YOUR_RAILWAY_TOKEN' > /data/.clawdbot/.railway_token && chmod 600 /data/.clawdbot/.railway_token")
        return

    query = '{"query":"{ me { id name email } }"}'
    code, body = curl_json("https://backboard.railway.app/graphql/v2",
                           headers=[f"Authorization: Bearer {token}",
                                    "Content-Type: application/json"],
                           data=query, method="POST")
    if code == 200 and "data" in body and body["data"] and body["data"].get("me"):
        me = body["data"]["me"]
        record(name, "ok", f"Railway authenticated as {me.get('name', '?')} ({me.get('email', '?')})")
    elif "errors" in body:
        errs = body.get("errors", [{}])
        msg = errs[0].get("message", "unknown") if errs else "unknown"
        record(name, "fail", f"Railway token invalid: {msg}",
               "# Get token from: https://railway.app/account/tokens\n"
               "echo 'NEW_TOKEN' > /data/.clawdbot/.railway_token")
    else:
        record(name, "warn", f"Railway API returned {code}: {body}")


def check_perplexity():
    name = "perplexity"
    token = get_credential("perplexity") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".perplexity_token")
    if not token:
        record(name, "fail", "File missing or empty: .perplexity_token",
               "# Get token from: https://www.perplexity.ai/settings/api\n"
               "echo 'pplx-...' > /data/.clawdbot/.perplexity_token && chmod 600 /data/.clawdbot/.perplexity_token")
        return

    payload = json.dumps({
        "model": "sonar",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    })
    code, body = curl_json("https://api.perplexity.ai/chat/completions",
                           headers=[f"Authorization: Bearer {token}",
                                    "Content-Type: application/json"],
                           data=payload, method="POST")
    if code == 200 and "choices" in body:
        record(name, "ok", "Perplexity API token valid")
    elif code == 401:
        record(name, "fail", "Perplexity token invalid (401)",
               "# Get token from: https://www.perplexity.ai/settings/api\n"
               "echo 'pplx-NEW' > /data/.clawdbot/.perplexity_token")
    else:
        if isinstance(body, dict):
            err = body.get("error", "")
            msg = err.get("message", str(err))[:80] if isinstance(err, dict) else str(err)[:80]
        else:
            msg = str(body)[:80]
        record(name, "warn", f"Perplexity returned {code}: {msg}")


def check_twilio():
    name = "twilio"
    sid = get_credential("twilio_sid") if HAS_SHARED_CONFIG else None
    token = get_credential("twilio_token") if HAS_SHARED_CONFIG else None
    if not sid:
        sid = read_file(CLAWDBOT / ".twilio_sid")
    if not token:
        token = read_file(CLAWDBOT / ".twilio_token")

    if not sid:
        record(name, "fail", "File missing or empty: .twilio_sid",
               "echo 'ACxxxx' > /data/.clawdbot/.twilio_sid && chmod 600 /data/.clawdbot/.twilio_sid")
        return
    if not token:
        record(name, "fail", "File missing or empty: .twilio_token",
               "echo 'YOUR_AUTH_TOKEN' > /data/.clawdbot/.twilio_token && chmod 600 /data/.clawdbot/.twilio_token")
        return

    code, body = curl_json(f"https://api.twilio.com/[REDACTED_PHONE]/Accounts/{sid}.json",
                           headers=[f"Authorization: Basic {_b64(sid + ':' + token)}"])
    if code == 200 and "friendly_name" in body:
        record(name, "ok", f"Twilio authenticated: {body.get('friendly_name', sid)}")
    elif code == 401:
        record(name, "fail", "Twilio credentials invalid (401)",
               "# Get credentials from: https://console.twilio.com/\n"
               "echo 'ACxxxx' > /data/.clawdbot/.twilio_sid\n"
               "echo 'auth_token' > /data/.clawdbot/.twilio_token")
    else:
        record(name, "warn", f"Twilio returned {code}: {body.get('message', '')}")


def _b64(s: str) -> str:
    import base64
    return base64.b64encode(s.encode()).decode()


def check_google_analytics():
    name = "google_analytics"

    # Prefer unified credential resolution; fallback to token file.
    data = None
    source = "file"
    if HAS_SHARED_CONFIG:
        creds = get_google_oauth_credentials()
        if isinstance(creds, dict) and creds:
            data = creds
            source = "shared-config"

    path = CLAWDBOT / ".google_analytics_token.json"
    if data is None:
        if not path.exists():
            record(name, "fail", "File missing: .google_analytics_token.json",
                   "# Requires interactive OAuth — Max must run:\n"
                   "gog auth login --account YOUR_GOOGLE_EMAIL")
            return
        try:
            data = json.loads(path.read_text())
            source = "file"
        except json.JSONDecodeError:
            record(name, "fail", "Token file invalid JSON",
                   "rm /data/.clawdbot/.google_analytics_token.json\n"
                   "gog auth login --account YOUR_GOOGLE_EMAIL")
            return

    if "refresh_token" not in data:
        record(name, "warn", "Google OAuth credentials missing refresh_token — re-auth required",
               "gog auth login --account YOUR_GOOGLE_EMAIL")
        return

    if "client_id" not in data or "client_secret" not in data:
        record(name, "warn", "Google OAuth credentials missing client_id/client_secret — refresh will fail",
               "# Add client_id and client_secret to the token JSON or env config")
        return

    # Actually test refresh + GA4 API call (avoids false positives).
    try:
        if requests is not None:
            resp = requests.post("https://oauth2.googleapis.com/token", data={
                "client_id": data["client_id"],
                "client_secret": data["client_secret"],
                "refresh_token": data["refresh_token"],
                "grant_type": "refresh_token"
            }, timeout=10)
            status = resp.status_code
            body = resp.json() if resp.text else {}
        else:
            import urllib.parse, urllib.request
            payload = urllib.parse.urlencode({
                "client_id": data["client_id"],
                "client_secret": data["client_secret"],
                "refresh_token": data["refresh_token"],
                "grant_type": "refresh_token",
            }).encode()
            req = urllib.request.Request("https://oauth2.googleapis.com/token", data=payload)
            try:
                with urllib.request.urlopen(req, timeout=10) as r:
                    status = r.status
                    body = json.loads(r.read().decode() or "{}")
            except urllib.error.HTTPError as e:
                status = e.code
                try:
                    body = json.loads(e.read().decode() or "{}")
                except Exception:
                    body = {}

        if status != 200:
            detail = ""
            if isinstance(body, dict):
                detail = body.get("error_description") or body.get("error") or ""
            extra = f" ({detail})" if detail else ""
            record(name, "fail", f"Token refresh failed: {status}{extra}",
                   "# Token may be expired/revoked — Max needs to re-auth")
            return

        access = body.get("access_token", "") if isinstance(body, dict) else ""
        if not access:
            record(name, "fail", "Token refresh succeeded but no access_token returned",
                   "# Re-auth Google OAuth and try again")
            return

        ga_property = os.environ.get("GA4_PROPERTY_ID", "502068431")
        ga_url = f"https://analyticsdata.googleapis.com/v1beta/properties/{ga_property}:runReport"

        if requests is not None:
            ga = requests.post(
                ga_url,
                headers={"Authorization": f"Bearer {access}"},
                json={"dateRanges": [{"startDate": "yesterday", "endDate": "yesterday"}], "metrics": [{"name": "sessions"}]},
                timeout=10,
            )
            ga_status = ga.status_code
        else:
            import urllib.request
            req = urllib.request.Request(
                ga_url,
                data=json.dumps({"dateRanges": [{"startDate": "yesterday", "endDate": "yesterday"}], "metrics": [{"name": "sessions"}]}).encode(),
                headers={"Authorization": f"Bearer {access}", "Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as r:
                    ga_status = r.status
            except urllib.error.HTTPError as e:
                ga_status = e.code

        services = "GA4" + (" ✅" if ga_status == 200 else f" ❌({ga_status})")
        scopes = data.get("scope", "")
        scope_list = [s.split("/")[-1] for s in scopes.split() if "googleapis" in s]
        record(name, "ok", f"Google OAuth working via {source} ({services}, scopes: {', '.join(scope_list)})")
    except Exception as e:
        record(name, "warn", f"Google OAuth credentials present but API test failed: {e}")


def check_manychat():
    name = "manychat"
    token = get_credential("manychat") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".manychat_token")
    if not token:
        record(name, "fail", "File missing or empty: .manychat_token",
               "# Get token from: https://manychat.com/settings/api\n"
               "echo 'YOUR_TOKEN' > /data/.clawdbot/.manychat_token && chmod 600 /data/.clawdbot/.manychat_token")
        return

    code, body = curl_json("https://api.manychat.com/fb/page/getInfo",
                           headers=[f"Authorization: Bearer {token}"])
    if code == 200 and body.get("status") == "success":
        page = body.get("data", {})
        record(name, "ok", f"ManyChat authenticated: {page.get('name', 'page info OK')}")
    elif code == 401 or body.get("status") == "error":
        msg = body.get("message", "invalid token")
        record(name, "fail", f"ManyChat token invalid: {msg}",
               "# Get token from: https://manychat.com/settings/api\n"
               "echo 'NEW_TOKEN' > /data/.clawdbot/.manychat_token")
    else:
        record(name, "warn", f"ManyChat returned {code}: {str(body)[:80]}")


def check_youtube_cookies():
    name = "youtube_cookies"
    cookie_val = get_credential("youtube_cookies") if HAS_SHARED_CONFIG else None
    if cookie_val:
        lines = [l for l in cookie_val.splitlines() if not l.startswith("#") and l.strip()]
        record(name, "ok", f"YouTube cookies via env/config ({len(lines)} entries)")
        return
    path = CLAWDBOT / "cookies" / "youtube.txt"
    if not path.exists():
        record(name, "fail", "File missing: cookies/youtube.txt",
               "# Export cookies from a logged-in YouTube session:\n"
               "# Use 'Get cookies.txt LOCALLY' browser extension\n"
               "# Save to: /data/.clawdbot/cookies/youtube.txt")
        return

    content = path.read_text().strip()
    if not content:
        record(name, "fail", "cookies/youtube.txt is empty",
               "# Re-export cookies from browser:\n"
               "# Use 'Get cookies.txt LOCALLY' extension → save to /data/.clawdbot/cookies/youtube.txt")
        return

    lines = [l for l in content.splitlines() if not l.startswith("#") and l.strip()]
    record(name, "ok", f"YouTube cookies file present ({len(lines)} cookie entries)")


def check_openai():
    name = "openai"
    token = get_credential("openai") if HAS_SHARED_CONFIG else None
    if not token:
        token = os.environ.get("OPENAI_API_KEY", "")
    if not token:
        try:
            ocjson = json.loads(OPENCLAW_JSON.read_text())
            token = ocjson.get("env", {}).get("vars", {}).get("OPENAI_API_KEY", "")
        except Exception:
            pass

    if not token:
        record(name, "fail", "OPENAI_API_KEY not found in env or openclaw.json",
               "# Add to openclaw.json env.vars or set in shell:\n"
               "export OPENAI_API_KEY='sk-proj-...'")
        return

    code, body = curl_json("https://api.openai.com/v1/models",
                           headers=[f"Authorization: Bearer {token}"])
    if code == 200 and "data" in body:
        count = len(body.get("data", []))
        record(name, "ok", f"OpenAI API key valid ({count} models available)")
    elif code == 401:
        record(name, "fail", "OpenAI API key invalid (401)",
               "# Get key from: https://platform.openai.com/api-keys\n"
               "# Update in openclaw.json env.vars.OPENAI_API_KEY")
    else:
        msg = body.get("error", {}).get("message", str(body)[:80]) if isinstance(body, dict) else ""
        record(name, "warn", f"OpenAI returned {code}: {msg}")


def check_xai():
    name = "xai"
    token = get_credential("xai") if HAS_SHARED_CONFIG else None
    if not token:
        token = os.environ.get("XAI_API_KEY", "")
    if not token:
        try:
            ocjson = json.loads(OPENCLAW_JSON.read_text())
            token = ocjson.get("env", {}).get("vars", {}).get("XAI_API_KEY", "")
        except Exception:
            pass
    if not token:
        token = read_file(CLAWDBOT / ".xai_token")

    if not token:
        record(name, "fail", "xAI key not found (env XAI_API_KEY, openclaw.json, or .xai_token)",
               "echo 'xai-...' > /data/.clawdbot/.xai_token\n"
               "# Or add to openclaw.json env.vars.XAI_API_KEY")
        return

    # Use models list endpoint — no model-name dependency
    code, body = curl_json("https://api.x.ai/v1/models",
                           headers=[f"Authorization: Bearer {token}"])
    if code == 200 and "data" in body:
        models = [m.get("id", "") for m in body.get("data", [])]
        record(name, "ok", f"xAI API key valid ({len(models)} models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''})")
    elif code == 401:
        record(name, "fail", "xAI key invalid (401)",
               "# Get key from: https://console.x.ai/\n"
               "echo 'xai-NEW' > /data/.clawdbot/.xai_token")
    else:
        if isinstance(body, dict):
            err = body.get("error", "")
            msg = err.get("message", str(err))[:80] if isinstance(err, dict) else str(err)[:80]
        else:
            msg = str(body)[:80]
        record(name, "warn", f"xAI returned {code}: {msg}")


def check_telegram():
    name = "telegram"
    bot_token = ""
    try:
        ocjson = json.loads(OPENCLAW_JSON.read_text())
        channels = ocjson.get("channels", {})
        tg = channels.get("telegram", {})
        bot_token = tg.get("botToken", "")
    except Exception:
        pass

    if not bot_token:
        # Not a failure on non-Telegram instances (e.g. Slack/Discord)
        record(name, "warn", "Telegram not configured (openclaw.json channels.telegram.botToken missing)",
               "# Skip if using Slack/Discord. Otherwise add to openclaw.json:\n"
               '# "channels": { "telegram": { "botToken": "YOUR_BOT_TOKEN" } }')
        return

    code, body = curl_json(f"https://api.telegram.org/bot{bot_token}/getMe")
    if code == 200 and body.get("ok"):
        bot = body.get("result", {})
        record(name, "ok", f"Telegram bot valid: @{bot.get('username', '?')} ({bot.get('first_name', '?')})")
    else:
        desc = body.get("description", "invalid token")
        record(name, "fail", f"Telegram bot token invalid: {desc}",
               "# Get new bot token from @BotFather on Telegram\n"
               "# Update openclaw.json channels.telegram.botToken")


# ─── Integration Checks ────────────────────────────────────────────────────────

def check_google_oauth():
    name = "google_oauth"
    # Use the installed gog CLI directly. `npx gog` is stale/noisy in this runtime and
    # can report false auth failures even when the real gog keyring is healthy.
    rc, out, err = run_cmd(["gog", "auth", "list", "--check", "--no-input"], timeout=20)
    combined = (out + " " + err).lower()

    # Detect various failure modes
    error_phrases = ["not installed", "no accounts", "not logged", "auth not", "command not found"]
    has_error = any(p in combined for p in error_phrases)
    has_email = "@" in out

    if rc == 0 and has_email and not has_error:
        record(name, "ok", f"Google OAuth (gog): {out[:120]}")
    elif "not installed" in combined:
        record(name, "warn", "gog auth module not installed — Google OAuth status unknown",
               "# Max must run interactively (requires browser):\n"
               "gog auth login --account YOUR_GOOGLE_EMAIL\n"
               "# ⚠️  NOTE: Container reprovision loses gog auth — must re-run after each reprovision")
    elif "no accounts" in combined or (rc == 0 and not out.strip()):
        record(name, "fail", "No Google accounts authenticated with gog CLI",
               "# Max must run interactively (requires browser):\n"
               "gog auth login --account YOUR_GOOGLE_EMAIL\n"
               "# ⚠️  NOTE: Container reprovision loses gog auth — must re-run after each reprovision")
    else:
        out_display = (out + err)[:200]
        record(name, "warn", f"gog auth list returned rc={rc}: {out_display}",
               "gog auth login --account YOUR_GOOGLE_EMAIL")


def check_github_cli():
    name = "github_cli"
    rc, out, err = run_cmd(["gh", "auth", "status"], timeout=15)
    combined = (out + err).strip()
    if rc == 0:
        record(name, "ok", f"GitHub CLI authenticated: {combined[:100]}")
    elif "not logged in" in combined.lower() or rc != 0:
        record(name, "fail", f"GitHub CLI not authenticated: {combined[:100]}",
               "gh auth login\n"
               "# Or: export GH_TOKEN=$(cat /data/.clawdbot/.github_token)")
    else:
        record(name, "warn", f"GitHub CLI status unclear (rc={rc}): {combined[:100]}")


def check_crm_db():
    name = "crm_db"
    db_path = WORKSPACE / "data" / "crm.db"
    if not db_path.exists():
        record(name, "fail", "CRM database not found: data/crm.db",
               "python3 tools/crm.py import gmail --days 90\n"
               "# Or: python3 tools/crm.py add --name 'Test' --email '[REDACTED_EMAIL]'")
        return

    rc, out, err = run_cmd(["python3", "tools/crm.py", "stats"], timeout=20)
    if rc == 0:
        record(name, "ok", f"CRM DB healthy: {out[:120]}")
    else:
        record(name, "warn", f"CRM stats returned rc={rc}: {(out+err)[:120]}",
               "python3 tools/crm.py import gmail")


def check_finance_db():
    name = "finance_db"
    db_path = WORKSPACE / "data" / "finance.db"
    # finance-v2 may use a different path
    alt_path = WORKSPACE / "finance" / "finance.db"
    if not db_path.exists() and not alt_path.exists():
        # Try to find it
        rc2, out2, _ = run_cmd(["find", str(WORKSPACE), "-name", "finance*.db", "-maxdepth", "3"],
                               cwd=str(WORKSPACE), timeout=5)
        if not out2:
            record(name, "fail", "Finance database not found",
                   "python3 tools/finance-v2.py scan --days 90")
            return

    rc, out, err = run_cmd(["python3", "tools/finance-v2.py", "stats"], timeout=20)
    if rc == 0:
        record(name, "ok", f"Finance DB healthy: {out[:120]}")
    else:
        record(name, "warn", f"Finance stats returned rc={rc}: {(out+err)[:120]}",
               "python3 tools/finance-v2.py scan")


def check_analytics_db():
    name = "analytics_db"
    # Primary analytics DB lives in max-techera/data/, fallback to data/
    db_path = WORKSPACE / "max-techera" / "data" / "analytics.db"
    if not db_path.exists():
        db_path = WORKSPACE / "data" / "analytics.db"
    if not db_path.exists():
        record(name, "fail", "Analytics database not found",
               "python3 tools/analytics-collector.py --collect")
        return

    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        if tables:
            # Count rows in key table
            row_count = conn.execute("SELECT COUNT(*) FROM ga4_daily").fetchone()[0] if "ga4_daily" in tables else 0
            conn.close()
            record(name, "ok", f"Analytics DB OK ({len(tables)} tables, {row_count} ga4_daily rows) @ {db_path.relative_to(WORKSPACE)}")
        else:
            conn.close()
            record(name, "warn", "Analytics DB exists but has no tables",
                   "python3 tools/analytics-collector.py --collect")
    except Exception as e:
        record(name, "fail", f"Analytics DB error: {e}",
               "python3 tools/analytics-collector.py --collect")


def check_search_db():
    name = "search_db"
    db_path = WORKSPACE / "data" / "search.db"
    if not db_path.exists():
        record(name, "fail", "Search database not found: data/search.db",
               "# Run content pipeline to populate search index:\n"
               "python3 tools/content-engine.py pitch 'topic' --research")
        return

    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        # Try to count rows in first table
        count = 0
        if tables:
            try:
                row = conn.execute(f"SELECT COUNT(*) FROM '{tables[0]}'").fetchone()
                count = row[0] if row else 0
            except Exception:
                pass
        conn.close()
        if tables:
            record(name, "ok", f"Search DB OK ({len(tables)} tables, ~{count} rows in '{tables[0]}')")
        else:
            record(name, "warn", "Search DB exists but empty",
                   "python3 tools/content-engine.py pitch 'topic' --research")
    except Exception as e:
        record(name, "fail", f"Search DB error: {e}")


def check_research_queue():
    name = "research_queue"
    db_path = WORKSPACE / "data" / "research-queue.db"
    if not db_path.exists():
        record(name, "warn", "Research queue DB not found: data/research-queue.db",
               "python3 tools/research-queue.py status")
        return

    rc, out, err = run_cmd(["python3", "tools/research-queue.py", "status"], timeout=20)
    if rc == 0:
        record(name, "ok", f"Research queue OK: {out[:120]}")
    else:
        record(name, "warn", f"Research queue status rc={rc}: {(out+err)[:120]}")


def check_ytdlp():
    name = "yt_dlp"
    rc, out, err = run_cmd(["yt-dlp", "--version"], timeout=10)
    if rc == 0 and out:
        record(name, "ok", f"yt-dlp version: {out.strip()}")
    else:
        rc2, out2, _ = run_cmd(["python3", "-m", "yt_dlp", "--version"], timeout=10)
        if rc2 == 0:
            record(name, "ok", f"yt-dlp (module) version: {out2.strip()}")
        else:
            record(name, "fail", "yt-dlp not found",
                   "pip install yt-dlp\n# Or: pipx install yt-dlp")


# ─── Additional Credential Checks ─────────────────────────────────────────────

def check_anthropic():
    name = "anthropic"
    token = get_credential("anthropic") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".anthropic_token")
    if not token:
        record(name, "warn", "No Anthropic key found",
               "echo 'sk-ant-...' > /data/.clawdbot/.anthropic_token && chmod 600 /data/.clawdbot/.anthropic_token")
        return
    code, body = curl_json("https://api.anthropic.com/v1/models?limit=1",
                           headers=[f"x-api-key: {token}", "anthropic-version: 2023-06-01"])
    if code == 200:
        record(name, "ok", "Anthropic API key valid")
    elif code == 401:
        record(name, "fail", "Anthropic key invalid (401)",
               "# Regenerate: https://console.anthropic.com/settings/keys")
    else:
        record(name, "warn", f"Anthropic returned {code}")


def check_gemini():
    name = "gemini"
    token = get_credential("gemini") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".gemini_token")
    if not token:
        record(name, "warn", "No Gemini key found",
               "echo 'key' > /data/.clawdbot/.gemini_token && chmod 600 /data/.clawdbot/.gemini_token")
        return
    code, body = curl_json(f"https://generativelanguage.googleapis.com/v1beta/models?key={token}")
    if code == 200 and "models" in body:
        record(name, "ok", f"Gemini key valid ({len(body.get('models',[]))} models)")
    else:
        record(name, "fail", f"Gemini key invalid ({code})",
               "# Regenerate: https://aistudio.google.com/apikey")


def check_elevenlabs():
    name = "elevenlabs"
    token = get_credential("elevenlabs") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".elevenlabs_token")
    if not token:
        record(name, "warn", "No ElevenLabs key found")
        return
    code, body = curl_json("https://api.elevenlabs.io/v1/user",
                           headers=[f"xi-api-key: {token}"])
    if code == 200 and "subscription" in body:
        tier = body.get("subscription", {}).get("tier", "?")
        record(name, "ok", f"ElevenLabs valid (tier={tier})")
    elif code == 401:
        record(name, "fail", "ElevenLabs key invalid (401)")
    else:
        record(name, "warn", f"ElevenLabs returned {code}")


def check_brave():
    name = "brave"
    token = get_credential("brave") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".brave_token")
    if not token:
        record(name, "warn", "No Brave key found")
        return
    code, body = curl_json("https://api.search.brave.com/res/v1/web/search?q=test&count=1",
                           headers=[f"X-Subscription-Token: {token}", "Accept: application/json"])
    if code == 200:
        record(name, "ok", "Brave Search key valid")
    else:
        record(name, "fail", f"Brave key invalid ({code})")


def check_vercel():
    name = "vercel"
    token = get_credential("vercel") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".vercel_token")
    if not token:
        record(name, "warn", "No Vercel token found")
        return
    code, body = curl_json("https://api.vercel.com/v2/user",
                           headers=[f"Authorization: Bearer {token}"])
    if code == 200 and "user" in body:
        u = body["user"]
        record(name, "ok", f"Vercel: {u.get('username', u.get('name', '?'))}")
    else:
        record(name, "fail", f"Vercel token invalid ({code})")


def check_mailerlite():
    name = "mailerlite"
    token = get_credential("mailerlite") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".mailerlite_token")
    if not token:
        record(name, "warn", "No MailerLite key found")
        return
    code, body = curl_json("https://connect.mailerlite.com/api/subscribers?limit=1",
                           headers=[f"Authorization: Bearer {token}", "Accept: application/json"])
    if code == 200:
        record(name, "ok", "MailerLite key valid")
    elif code == 401:
        record(name, "fail", "MailerLite key invalid (401)")
    else:
        record(name, "warn", f"MailerLite returned {code}")


def check_posthog():
    name = "posthog"
    token = get_credential("posthog") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".posthog_token")
    if not token:
        record(name, "warn", "No PostHog key found")
        return
    code, body = curl_json("https://us.posthog.com/api/users/@me/",
                           headers=[f"Authorization: Bearer {token}"])
    if code == 200 and "email" in body:
        record(name, "ok", f"PostHog: {body.get('email', '?')}")
    else:
        record(name, "fail", f"PostHog key invalid ({code})")


def check_notion():
    name = "notion"
    token = get_credential("notion") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".notion_token")
    if not token:
        record(name, "warn", "No Notion token found")
        return
    code, body = curl_json("https://api.notion.com/v1/users/me",
                           headers=[f"Authorization: Bearer {token}", "Notion-Version: 2022-06-28"])
    if code == 200 and "name" in body:
        record(name, "ok", f"Notion: {body.get('name', '?')}")
    else:
        record(name, "fail", f"Notion token invalid ({code})")


def check_discord():
    name = "discord"
    token = read_file(CLAWDBOT / ".discord_token")
    if not token:
        record(name, "warn", "No Discord token found")
        return
    code, body = curl_json("https://discord.com/api/v10/users/@me",
                           headers=[f"Authorization: Bot {token}"])
    if code == 200 and "username" in body:
        record(name, "ok", f"Discord bot: {body.get('username', '?')}#{body.get('discriminator', '0')}")
    else:
        record(name, "fail", f"Discord token invalid ({code})")


def check_gamma():
    name = "gamma"
    token = read_file(CLAWDBOT / ".gamma_token")
    if not token:
        record(name, "warn", "No Gamma token found")
        return
    # Gamma doesn't have a public whoami endpoint — just check file exists
    record(name, "ok", f"Gamma token present ({len(token)} chars)")


def check_shopify():
    name = "shopify"
    path = CLAWDBOT / ".shopify.json"
    if not path.exists():
        record(name, "warn", "No Shopify credentials found")
        return
    try:
        data = json.loads(path.read_text())
        shop = data.get("shop", "?")
        token = data.get("access_token", data.get("token", ""))
        if token:
            record(name, "ok", f"Shopify: {shop} (token present)")
        else:
            record(name, "fail", "Shopify JSON missing access_token")
    except Exception as e:
        record(name, "fail", f"Shopify JSON parse error: {e}")


def check_kumello():
    name = "kumello"
    token = get_credential("kumello") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".kumello_api_key")
    if not token:
        record(name, "warn", "No Kumello API key found")
        return
    record(name, "ok", f"Kumello API key present ({len(token)} chars)")


def check_stripe():
    name = "stripe"
    token = get_credential("stripe") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".stripe_token")
    if not token:
        token = os.environ.get("STRIPE_API_KEY", "") or os.environ.get("STRIPE_SECRET_KEY", "")
    if not token:
        record(name, "warn", "No Stripe key found")
        return
    code, body = curl_json("https://api.stripe.com/v1/balance",
                           headers=[f"Authorization: Bearer {token}"])
    if code == 200 and "available" in body:
        record(name, "ok", f"Stripe key valid (balance accessible)")
    elif code == 401:
        record(name, "fail", "Stripe key invalid (401)",
               "# Get key from: https://dashboard.stripe.com/apikeys")
    else:
        record(name, "warn", f"Stripe returned {code}")


def check_gateway_token():
    name = "openclaw_gateway"
    token = get_credential("openclaw_gateway") if HAS_SHARED_CONFIG else None
    if not token:
        token = read_file(CLAWDBOT / ".openclaw_gateway_token")
    if not token:
        record(name, "warn", "No gateway token found")
        return
    record(name, "ok", f"Gateway token present ({len(token)} chars)")


# ─── Registry ──────────────────────────────────────────────────────────────────

CREDENTIAL_CHECKS = {
    "github":                 check_github,
    "meta":                   check_meta,
    "linear":                 check_linear,
    "linear_webhook_secret":  check_linear_webhook_secret,
    "railway":                check_railway,
    "perplexity":             check_perplexity,
    "twilio":                 check_twilio,
    "google_analytics":       check_google_analytics,
    "manychat":               check_manychat,
    "youtube_cookies":        check_youtube_cookies,
    "openai":                 check_openai,
    "xai":                    check_xai,
    "telegram":               check_telegram,
    "anthropic":              check_anthropic,
    "gemini":                 check_gemini,
    "elevenlabs":             check_elevenlabs,
    "brave":                  check_brave,
    "vercel":                 check_vercel,
    "mailerlite":             check_mailerlite,
    "posthog":                check_posthog,
    "notion":                 check_notion,
    "discord":                check_discord,
    "gamma":                  check_gamma,
    "shopify":                check_shopify,
    "kumello":                check_kumello,
    "stripe":                 check_stripe,
    "openclaw_gateway":       check_gateway_token,
}

INTEGRATION_CHECKS = {
    "google_oauth":   check_google_oauth,
    "github_cli":     check_github_cli,
    "crm_db":         check_crm_db,
    "finance_db":     check_finance_db,
    "analytics_db":   check_analytics_db,
    "search_db":      check_search_db,
    "research_queue": check_research_queue,
    "yt_dlp":         check_ytdlp,
}

ALL_CHECKS = {**CREDENTIAL_CHECKS, **INTEGRATION_CHECKS}


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check all workspace credentials and integrations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--fix", action="store_true", help="Print fix commands for failures")
    parser.add_argument("--only", metavar="NAME", help="Check only this credential/integration")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show failures/warnings")
    parser.add_argument("--json", action="store_true", dest="json_out", help="Output JSON")
    args = parser.parse_args()

    checks_to_run = {}

    if args.only:
        key = args.only.lower().replace("-", "_")
        if key not in ALL_CHECKS:
            close = [k for k in ALL_CHECKS if key in k]
            if close:
                print(f"Unknown check '{args.only}'. Did you mean: {', '.join(close)}?")
            else:
                print(f"Unknown check '{args.only}'. Available: {', '.join(ALL_CHECKS.keys())}")
            sys.exit(2)
        checks_to_run = {key: ALL_CHECKS[key]}
    else:
        checks_to_run = ALL_CHECKS

    if not args.json_out:
        print(f"\n{BOLD}{'═'*60}{RESET}")
        print(f"{BOLD}  🔐 Credential & Integration Health Check{RESET}")
        print(f"{BOLD}{'═'*60}{RESET}\n")

        if not args.only:
            print(f"{CYAN}  Credentials ({len(CREDENTIAL_CHECKS)}){RESET}")

    for name, fn in checks_to_run.items():
        if not args.json_out and name == "google_oauth" and not args.only:
            print(f"\n{CYAN}  Integrations ({len(INTEGRATION_CHECKS)}){RESET}")
        try:
            fn()
        except Exception as e:
            record(name, "fail", f"Check raised exception: {e}")

    if args.json_out:
        print(json.dumps(results, indent=2))
        failed = sum(1 for r in results if r["status"] == "fail")
        sys.exit(1 if failed else 0)

    # Print results
    for r in results:
        if args.quiet and r["status"] == "ok":
            continue
        ico = icon(r["status"])
        label = r["name"].replace("_", " ").title()
        print(f"  {ico} {BOLD}{label}{RESET}: {r['message']}")
        if args.fix and r["status"] in ("fail", "warn") and r.get("fix"):
            print(f"     {YELLOW}Fix:{RESET}")
            for line in r["fix"].splitlines():
                print(f"       {line}")
            print()

    # Summary
    total   = len(results)
    passed  = sum(1 for r in results if r["status"] == "ok")
    warned  = sum(1 for r in results if r["status"] == "warn")
    failed  = sum(1 for r in results if r["status"] == "fail")

    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"  Summary: {OK} {passed} passed  {WARN} {warned} warned  {FAIL} {failed} failed  (of {total} checks)")

    if failed == 0 and warned == 0:
        print(f"\n  {GREEN}{BOLD}All credentials and integrations are healthy! 🎉{RESET}\n")
    elif failed == 0:
        print(f"\n  {YELLOW}Some warnings — check details above.{RESET}")
        if not args.fix:
            print(f"  Run with {BOLD}--fix{RESET} to see fix commands.\n")
    else:
        print(f"\n  {RED}{BOLD}{failed} credential(s) need attention.{RESET}")
        if not args.fix:
            print(f"  Run with {BOLD}--fix{RESET} to see fix commands.\n")
        else:
            print()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
