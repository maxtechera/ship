#!/usr/bin/env python3
"""
credentials/scripts/check_local.py

Local Mac credential & CLI health check.
Uses the same credential registry as OpenClaw (tools/lib/config.py) with
platform-aware defaults (~/.clawdbot on Mac, /data/.clawdbot on container).

Usage:
  python3 check_local.py                  # Full check
  python3 check_local.py --fix            # Check + print fix commands
  python3 check_local.py --only gh        # Check a single CLI or credential
  python3 check_local.py --quiet          # Only print failures
  python3 check_local.py --json           # Output JSON

Exit code: 0 = all pass, 1 = any failures
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ─── Platform-aware credential directory ─────────────────────────────────────

def _default_claw_dir():
    explicit = os.environ.get("OPENCLAW_CRED_DIR")
    if explicit:
        return explicit
    if Path("/data/.clawdbot").exists():
        return "/data/.clawdbot"
    return str(Path.home() / ".clawdbot")

CLAW_DIR = _default_claw_dir()

# ─── Credential registry (mirrors tools/lib/config.py) ──────────────────────

_CREDENTIAL_REGISTRY = {
    "github":                 (["GITHUB_TOKEN", "GH_TOKEN"],                     f"{CLAW_DIR}/.github_token"),
    "meta":                   (["META_ACCESS_TOKEN", "META_TOKEN"],              f"{CLAW_DIR}/.meta_token"),
    "linear_token":           (["LINEAR_ACCESS_TOKEN", "LINEAR_API_KEY"],        f"{CLAW_DIR}/.linear_token"),
    "openai":                 (["OPENAI_API_KEY"],                                f"{CLAW_DIR}/.openai_token"),
    "anthropic":              (["ANTHROPIC_API_KEY"],                              f"{CLAW_DIR}/.anthropic_token"),
    "xai":                    (["XAI_API_KEY"],                                   f"{CLAW_DIR}/.xai_token"),
    "perplexity":             (["PERPLEXITY_KEY", "PERPLEXITY_API_KEY"],         f"{CLAW_DIR}/.perplexity_token"),
    "gemini":                 (["GEMINI_API_KEY", "GOOGLE_AI_API_KEY"],          f"{CLAW_DIR}/.gemini_token"),
    "vercel_token":           (["VERCEL_TOKEN"],                                  f"{CLAW_DIR}/.vercel_token"),
    "railway_token":          (["RAILWAY_TOKEN"],                                 f"{CLAW_DIR}/.railway_token"),
    "twilio":                 (["TWILIO_ACCOUNT_SID"],                            f"{CLAW_DIR}/.twilio_sid"),
    "manychat":               (["MANYCHAT_TOKEN"],                                f"{CLAW_DIR}/.manychat_token"),
    "telegram":               (["TELEGRAM_BOT_TOKEN"],                            f"{CLAW_DIR}/.telegram_bot_token"),
    "elevenlabs":             (["ELEVENLABS_API_KEY"],                             f"{CLAW_DIR}/.elevenlabs_token"),
    "brave":                  (["BRAVE_API_KEY"],                                  f"{CLAW_DIR}/.brave_token"),
    "mailerlite":             (["MAILERLITE_API_KEY"],                            f"{CLAW_DIR}/.mailerlite_token"),
    "posthog":                (["POSTHOG_PERSONAL_API_KEY"],                      f"{CLAW_DIR}/.posthog_token"),
    "google_oauth":           (["GOOGLE_OAUTH_TOKEN_JSON"],                       f"{CLAW_DIR}/.google_analytics_token.json"),
    "zoom":                   (["ZOOM_ACCESS_TOKEN"],                              f"{CLAW_DIR}/.zoom_token"),
}


def get_credential(name):
    """Resolve a credential: env var → file → empty string."""
    entry = _CREDENTIAL_REGISTRY.get(name)
    if not entry:
        return ""
    env_vars, file_path = entry
    for var in env_vars:
        val = os.environ.get(var, "")
        if val:
            return val
    try:
        return Path(file_path).read_text().strip()
    except Exception:
        return ""


def get_credential_source(name):
    """Return (value, source_label) for display."""
    entry = _CREDENTIAL_REGISTRY.get(name)
    if not entry:
        return "", "not in registry"
    env_vars, file_path = entry
    for var in env_vars:
        val = os.environ.get(var, "")
        if val:
            return val, f"env ${var}"
    try:
        val = Path(file_path).read_text().strip()
        if val:
            return val, f"file {file_path}"
    except Exception:
        pass
    tried = ", ".join(f"${v}" for v in env_vars)
    return "", f"not found (tried: {tried}, {file_path})"


# ─── ANSI colours ────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

OK   = f"{GREEN}✅{RESET}"
FAIL = f"{RED}❌{RESET}"
WARN = f"{YELLOW}⚠️ {RESET}"
SKIP = f"{DIM}⏭ {RESET}"

results: list[dict] = []


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _strip_ansi(s: str) -> str:
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


def run_cmd(cmd: list[str], timeout: int = 15) -> tuple[int, str, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, _strip_ansi(r.stdout.strip()), _strip_ansi(r.stderr.strip())
    except FileNotFoundError:
        return 127, "", "command not found"
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)


def http_json(url, headers=None, data=None, method="GET", timeout=10):
    """Minimal HTTP JSON request using urllib (no dependencies)."""
    req = urllib.request.Request(url, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    body_bytes = None
    if data:
        body_bytes = data.encode() if isinstance(data, str) else json.dumps(data).encode()
        if "Content-Type" not in (headers or {}):
            req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, body_bytes, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode() or "{}")
        except Exception:
            body = {}
        return e.code, body
    except Exception as e:
        return 0, {"_error": str(e)}


def record(name: str, status: str, message: str, fix: str = ""):
    results.append({"name": name, "status": status, "message": message, "fix": fix})


def icon(status: str) -> str:
    return {"ok": OK, "fail": FAIL, "warn": WARN, "skip": SKIP}.get(status, WARN)


def _mask(token: str) -> str:
    """Show first 4 and last 4 chars of a token."""
    if len(token) <= 12:
        return token[:4] + "…"
    return token[:4] + "…" + token[-4:]


# ─── CLI Checks (installed + auth) ──────────────────────────────────────────

def check_git():
    rc, out, _ = run_cmd(["git", "--version"])
    if rc == 0:
        record("git", "ok", out)
    else:
        record("git", "fail", "not found", "brew install git")


def check_node():
    rc, out, _ = run_cmd(["node", "--version"])
    if rc == 0:
        record("node", "ok", f"Node.js {out}")
    else:
        record("node", "fail", "not found", "brew install node")


def check_pnpm():
    rc, out, _ = run_cmd(["pnpm", "--version"])
    if rc == 0:
        record("pnpm", "ok", f"pnpm {out}")
    else:
        record("pnpm", "fail", "not found", "npm install -g pnpm")


def check_python():
    rc, out, _ = run_cmd(["python3", "--version"])
    if rc == 0:
        record("python3", "ok", out)
    else:
        record("python3", "fail", "not found", "brew install python3")


def check_gh():
    rc_ver, ver, _ = run_cmd(["gh", "--version"])
    if rc_ver == 127:
        record("gh", "fail", "not installed", "brew install gh")
        return
    rc, out, err = run_cmd(["gh", "auth", "status"])
    combined = (out + " " + err).strip()
    if rc == 0 and "logged in" in combined.lower():
        match = re.search(r'account (\S+)', combined) or re.search(r'as (\S+)', combined)
        user = match.group(1) if match else "authenticated"
        record("gh", "ok", f"authenticated as {user}")
    else:
        record("gh", "fail", f"not authenticated", "gh auth login")


def check_railway_cli():
    rc_ver, _, _ = run_cmd(["railway", "--version"])
    if rc_ver == 127:
        record("railway_cli", "fail", "not installed", "brew install railwayapp/tap/railway")
        return
    rc, out, err = run_cmd(["railway", "whoami"])
    combined = (out + " " + err).strip()
    if rc == 0 and combined and "not logged in" not in combined.lower():
        record("railway_cli", "ok", combined[:100])
    else:
        record("railway_cli", "fail", "not authenticated", "railway login")


def check_vercel_cli():
    rc_ver, _, _ = run_cmd(["vercel", "--version"])
    if rc_ver == 127:
        record("vercel_cli", "warn", "not installed", "pnpm install -g vercel")
        return
    rc, out, err = run_cmd(["vercel", "whoami"])
    combined = (out + " " + err).strip()
    if rc == 0 and combined:
        record("vercel_cli", "ok", combined[:100])
    else:
        record("vercel_cli", "fail", "not authenticated", "vercel login")


def check_linear_cli():
    rc_ver, _, _ = run_cmd(["linear", "--version"])
    if rc_ver == 127:
        record("linear_cli", "warn", "not installed",
               "brew install schpet/tap/linear-cli")
        return
    rc, out, err = run_cmd(["linear", "me"])
    combined = (out + " " + err).strip()
    if rc == 0 and combined and "error" not in combined.lower():
        record("linear_cli", "ok", combined[:100])
    else:
        record("linear_cli", "fail", "not authenticated", "linear auth")


def check_supabase_cli():
    rc_ver, ver, _ = run_cmd(["supabase", "--version"])
    if rc_ver == 127:
        record("supabase_cli", "warn", "not installed",
               "brew install supabase/tap/supabase")
        return
    rc, out, err = run_cmd(["supabase", "projects", "list"], timeout=20)
    combined = (out + " " + err).strip()
    if rc == 0 and "not logged in" not in combined.lower() and "error" not in combined.lower():
        record("supabase_cli", "ok", f"authenticated ({ver.strip()})")
    else:
        record("supabase_cli", "fail", "not authenticated", "supabase login")


def check_render_cli():
    rc_ver, _, _ = run_cmd(["render", "--version"])
    if rc_ver == 127:
        record("render_cli", "warn", "not installed",
               "brew tap render-oss/render && brew install render")
        return
    rc, out, err = run_cmd(["render", "whoami"])
    combined = (out + " " + err).strip()
    if rc == 0 and combined and "not" not in combined.lower():
        record("render_cli", "ok", combined[:100])
    else:
        record("render_cli", "fail", "not authenticated", "render login")


def check_docker():
    rc_ver, ver, _ = run_cmd(["docker", "--version"])
    if rc_ver == 127:
        record("docker", "warn", "not installed", "brew install --cask docker")
        return
    rc, _, _ = run_cmd(["docker", "info"], timeout=10)
    if rc == 0:
        record("docker", "ok", f"running ({ver.split(',')[0]})")
    else:
        record("docker", "warn", "installed but daemon not running",
               "open -a Docker")


# ─── API Credential Checks (whoami via HTTP) ─────────────────────────────────

def check_github_token():
    token, source = get_credential_source("github")
    if not token:
        record("github_token", "skip", f"no token ({source})",
               f"echo 'ghp_...' > {CLAW_DIR}/.github_token && chmod 600 {CLAW_DIR}/.github_token")
        return
    code, body = http_json("https://api.github.com/user",
                           headers={"Authorization": f"token {token}",
                                    "Accept": "application/vnd.github.v3+json"})
    if code == 200 and "login" in body:
        record("github_token", "ok", f"@{body['login']} via {source}")
    elif code == 401:
        record("github_token", "fail", f"token invalid (401) via {source}",
               "# Regenerate: https://github.com/settings/tokens")
    else:
        record("github_token", "warn", f"API returned {code}")


def check_meta_token():
    token, source = get_credential_source("meta")
    if not token:
        record("meta_token", "skip", f"no token ({source})",
               f"echo 'EAA...' > {CLAW_DIR}/.meta_token && chmod 600 {CLAW_DIR}/.meta_token")
        return
    code, body = http_json(f"https://graph.facebook.com/v21.0/me?access_token={token}")
    if code == 200 and "id" in body:
        record("meta_token", "ok", f"{body.get('name', body['id'])} via {source}")
    else:
        err = body.get("error", {}).get("message", f"HTTP {code}")
        record("meta_token", "fail", f"invalid: {err[:80]}",
               "# Regenerate: https://developers.facebook.com/tools/explorer/")


def check_linear_token():
    token, source = get_credential_source("linear_token")
    if not token:
        record("linear_token", "skip", f"no token ({source})",
               f"echo 'lin_api_...' > {CLAW_DIR}/.linear_token && chmod 600 {CLAW_DIR}/.linear_token")
        return
    auth = f"Bearer {token}" if token.startswith("lin_oauth") else token
    code, body = http_json("https://api.linear.app/graphql",
                           headers={"Authorization": auth, "Content-Type": "application/json"},
                           data='{"query":"{ viewer { name email } }"}',
                           method="POST")
    if code == 200 and body.get("data", {}).get("viewer"):
        v = body["data"]["viewer"]
        record("linear_token", "ok", f"{v.get('name', '?')} ({v.get('email', '?')}) via {source}")
    else:
        record("linear_token", "fail", f"invalid (HTTP {code})",
               "# Regenerate: https://linear.app/settings/api")


def check_openai_token():
    token, source = get_credential_source("openai")
    if not token:
        record("openai_token", "skip", f"no key ({source})",
               "export OPENAI_API_KEY='sk-...'")
        return
    code, body = http_json("https://api.openai.com/v1/models",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "data" in body:
        record("openai_token", "ok", f"{len(body['data'])} models available via {source}")
    elif code == 401:
        record("openai_token", "fail", f"key invalid (401) via {source}",
               "# Regenerate: https://platform.openai.com/api-keys")
    else:
        msg = body.get("error", {}).get("message", f"HTTP {code}") if isinstance(body, dict) else str(code)
        record("openai_token", "warn", f"{msg[:80]}")


def check_anthropic_token():
    token, source = get_credential_source("anthropic")
    if not token:
        record("anthropic_token", "skip", f"no key ({source})",
               "export ANTHROPIC_API_KEY='sk-ant-...'")
        return
    code, body = http_json("https://api.anthropic.com/v1/models?limit=1",
                           headers={"x-api-key": token,
                                    "anthropic-version": "2023-06-01"})
    if code == 200 and "data" in body:
        record("anthropic_token", "ok", f"valid via {source}")
    elif code == 401:
        record("anthropic_token", "fail", f"key invalid (401) via {source}",
               "# Regenerate: https://console.anthropic.com/settings/keys")
    else:
        msg = body.get("error", {}).get("message", f"HTTP {code}") if isinstance(body, dict) else str(code)
        record("anthropic_token", "warn", f"{msg[:80]}")


def check_xai_token():
    token, source = get_credential_source("xai")
    if not token:
        record("xai_token", "skip", f"no key ({source})",
               f"echo 'xai-...' > {CLAW_DIR}/.xai_token && chmod 600 {CLAW_DIR}/.xai_token")
        return
    code, body = http_json("https://api.x.ai/v1/models",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "data" in body:
        models = [m.get("id", "") for m in body.get("data", [])][:3]
        record("xai_token", "ok", f"{', '.join(models)} via {source}")
    elif code == 401:
        record("xai_token", "fail", f"key invalid (401)",
               "# Regenerate: https://console.x.ai/")
    else:
        record("xai_token", "warn", f"HTTP {code}")


def check_perplexity_token():
    token, source = get_credential_source("perplexity")
    if not token:
        record("perplexity_token", "skip", f"no key ({source})",
               f"echo 'pplx-...' > {CLAW_DIR}/.perplexity_token && chmod 600 {CLAW_DIR}/.perplexity_token")
        return
    payload = json.dumps({"model": "sonar", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5})
    code, body = http_json("https://api.perplexity.ai/chat/completions",
                           headers={"Authorization": f"Bearer {token}",
                                    "Content-Type": "application/json"},
                           data=payload, method="POST")
    if code == 200:
        record("perplexity_token", "ok", f"valid via {source}")
    elif code == 401:
        record("perplexity_token", "fail", "key invalid (401)",
               "# Regenerate: https://www.perplexity.ai/settings/api")
    else:
        record("perplexity_token", "warn", f"HTTP {code}")


def check_gemini_token():
    token, source = get_credential_source("gemini")
    if not token:
        record("gemini_token", "skip", f"no key ({source})",
               "export GEMINI_API_KEY='...'")
        return
    code, body = http_json(f"https://generativelanguage.googleapis.com/v1beta/models?key={token}")
    if code == 200 and "models" in body:
        record("gemini_token", "ok", f"{len(body['models'])} models via {source}")
    elif code == 400 or code == 403:
        record("gemini_token", "fail", f"key invalid ({code})",
               "# Regenerate: https://aistudio.google.com/apikey")
    else:
        record("gemini_token", "warn", f"HTTP {code}")


def check_vercel_token():
    token, source = get_credential_source("vercel_token")
    if not token:
        record("vercel_token", "skip", f"no token ({source})")
        return
    code, body = http_json("https://api.vercel.com/v2/user",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "user" in body:
        u = body["user"]
        record("vercel_token", "ok", f"{u.get('username', u.get('name', '?'))} via {source}")
    elif code == 401 or code == 403:
        record("vercel_token", "fail", f"token invalid ({code})",
               "# Regenerate: https://vercel.com/account/tokens")
    else:
        record("vercel_token", "warn", f"HTTP {code}")


def check_railway_token():
    token, source = get_credential_source("railway_token")
    if not token:
        record("railway_token", "skip", f"no token ({source})")
        return
    code, body = http_json("https://backboard.railway.app/graphql/v2",
                           headers={"Authorization": f"Bearer {token}",
                                    "Content-Type": "application/json"},
                           data='{"query":"{ me { name email } }"}',
                           method="POST")
    if code == 200 and body.get("data", {}).get("me"):
        me = body["data"]["me"]
        record("railway_token", "ok", f"{me.get('name', '?')} ({me.get('email', '?')}) via {source}")
    else:
        record("railway_token", "fail", f"token invalid (HTTP {code})",
               "# Regenerate: https://railway.app/account/tokens")


def check_twilio():
    """Twilio: prefer CLI (twilio profiles:list), fall back to API token."""
    name = "twilio"
    rc_ver, _, _ = run_cmd(["twilio", "--version"])
    if rc_ver != 127:
        # CLI installed — use it
        rc, out, err = run_cmd(["twilio", "profiles:list"])
        combined = (out + " " + err).strip()
        if rc == 0 and combined and "no profiles" not in combined.lower():
            # Extract active profile
            lines = [l for l in combined.splitlines() if "*" in l or "Active" in l]
            active = lines[0].strip() if lines else combined.splitlines()[0].strip()
            record(name, "ok", f"CLI: {active[:100]}")
        else:
            record(name, "fail", "CLI installed but no profiles configured",
                   "twilio profiles:create")
        return

    # No CLI — fall back to API token
    sid, sid_source = get_credential_source("twilio")
    if not sid:
        record(name, "skip", f"CLI not installed, no SID ({sid_source})",
               "brew tap twilio/brew && brew install twilio\n# Or token: echo 'ACxxx' > {}/{}".format(CLAW_DIR, ".twilio_sid"))
        return
    tok_entry = (["TWILIO_AUTH_TOKEN"], f"{CLAW_DIR}/.twilio_token")
    twilio_tok = ""
    for var in tok_entry[0]:
        twilio_tok = os.environ.get(var, "")
        if twilio_tok:
            break
    if not twilio_tok:
        try:
            twilio_tok = Path(tok_entry[1]).read_text().strip()
        except Exception:
            pass
    if not twilio_tok:
        record(name, "fail", "SID found but auth token missing",
               f"echo 'auth_token' > {CLAW_DIR}/.twilio_token && chmod 600 {CLAW_DIR}/.twilio_token")
        return
    creds = base64.b64encode(f"{sid}:{twilio_tok}".encode()).decode()
    code, body = http_json(f"https://api.twilio.com/2010-04-01/Accounts/{sid}.json",
                           headers={"Authorization": f"Basic {creds}"})
    if code == 200 and "friendly_name" in body:
        record(name, "ok", f"{body['friendly_name']} via token ({sid_source})")
    elif code == 401:
        record(name, "fail", "credentials invalid (401)",
               "# Check: https://console.twilio.com/")
    else:
        record(name, "warn", f"HTTP {code}")


def check_manychat_token():
    token, source = get_credential_source("manychat")
    if not token:
        record("manychat_token", "skip", f"no token ({source})")
        return
    code, body = http_json("https://api.manychat.com/fb/page/getInfo",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and body.get("status") == "success":
        name = body.get("data", {}).get("name", "OK")
        record("manychat_token", "ok", f"{name} via {source}")
    else:
        record("manychat_token", "fail", f"invalid (HTTP {code})",
               "# Regenerate: https://manychat.com/settings/api")


def check_telegram_token():
    token, source = get_credential_source("telegram")
    if not token:
        record("telegram_token", "skip", f"no token ({source})")
        return
    code, body = http_json(f"https://api.telegram.org/bot{token}/getMe")
    if code == 200 and body.get("ok"):
        bot = body.get("result", {})
        record("telegram_token", "ok", f"@{bot.get('username', '?')} via {source}")
    else:
        record("telegram_token", "fail", f"invalid (HTTP {code})",
               "# Regenerate via @BotFather on Telegram")


def check_elevenlabs():
    """ElevenLabs: prefer CLI (elevenlabs auth whoami), fall back to API token."""
    name = "elevenlabs"
    rc_ver, _, _ = run_cmd(["elevenlabs", "--version"])
    if rc_ver != 127:
        rc, out, err = run_cmd(["elevenlabs", "auth", "whoami"])
        combined = (out + " " + err).strip()
        if rc == 0 and combined and "not" not in combined.lower():
            record(name, "ok", f"CLI: {combined[:100]}")
        else:
            record(name, "fail", "CLI installed but not authenticated",
                   "elevenlabs auth login")
        return

    # No CLI — fall back to API token
    token, source = get_credential_source("elevenlabs")
    if not token:
        record(name, "skip", f"CLI not installed, no key ({source})",
               "npm i -g @elevenlabs/cli && elevenlabs auth login\n"
               f"# Or token: echo 'key' > {CLAW_DIR}/.elevenlabs_token")
        return
    code, body = http_json("https://api.elevenlabs.io/v1/user",
                           headers={"xi-api-key": token})
    if code == 200 and "subscription" in body:
        tier = body.get("subscription", {}).get("tier", "?")
        record(name, "ok", f"tier={tier} via token ({source})")
    elif code == 401:
        record(name, "fail", "key invalid (401)",
               "# Regenerate: https://elevenlabs.io/app/settings/api-keys")
    else:
        record(name, "warn", f"HTTP {code}")


def check_brave_token():
    token, source = get_credential_source("brave")
    if not token:
        record("brave_token", "skip", f"no key ({source})")
        return
    code, body = http_json("https://api.search.brave.com/res/v1/web/search?q=test&count=1",
                           headers={"X-Subscription-Token": token,
                                    "Accept": "application/json"})
    if code == 200:
        record("brave_token", "ok", f"valid via {source}")
    elif code == 401 or code == 403:
        record("brave_token", "fail", f"key invalid ({code})",
               "# Regenerate: https://brave.com/search/api/")
    else:
        record("brave_token", "warn", f"HTTP {code}")


def check_mailerlite():
    """MailerLite: prefer CLI (mailerlite account list), fall back to API token."""
    name = "mailerlite"
    rc_ver, _, _ = run_cmd(["mailerlite", "--version"])
    if rc_ver != 127:
        rc, out, err = run_cmd(["mailerlite", "account", "list"], timeout=20)
        combined = (out + " " + err).strip()
        if rc == 0 and combined and "error" not in combined.lower():
            record(name, "ok", f"CLI: {combined[:100]}")
        else:
            record(name, "fail", "CLI installed but not authenticated",
                   "mailerlite login")
        return

    # No CLI — fall back to API token
    token, source = get_credential_source("mailerlite")
    if not token:
        record(name, "skip", f"CLI not installed, no key ({source})",
               "go install github.com/mailerlite/mailerlite-cli@latest\n"
               f"# Or token: echo 'key' > {CLAW_DIR}/.mailerlite_token")
        return
    code, body = http_json("https://connect.mailerlite.com/api/subscribers?limit=1",
                           headers={"Authorization": f"Bearer {token}",
                                    "Accept": "application/json"})
    if code == 200:
        record(name, "ok", f"valid via token ({source})")
    elif code == 401:
        record(name, "fail", "key invalid (401)",
               "# Regenerate: https://dashboard.mailerlite.com/integrations/api")
    else:
        record(name, "warn", f"HTTP {code}")


def check_posthog():
    """PostHog: prefer CLI (posthog-cli), fall back to API token."""
    name = "posthog"
    rc_ver, _, _ = run_cmd(["posthog-cli", "--version"])
    if rc_ver != 127:
        # CLI exists — try a basic command to verify auth
        rc, out, err = run_cmd(["posthog-cli", "query", "SELECT 1"], timeout=20)
        combined = (out + " " + err).strip()
        if rc == 0:
            record(name, "ok", f"CLI: authenticated")
        else:
            record(name, "fail", "CLI installed but not authenticated",
                   "posthog-cli login")
        return

    # No CLI — fall back to API token
    token, source = get_credential_source("posthog")
    if not token:
        record(name, "skip", f"CLI not installed, no key ({source})",
               "npm i -g @posthog/cli && posthog-cli login\n"
               f"# Or token: echo 'key' > {CLAW_DIR}/.posthog_token")
        return
    code, body = http_json("https://us.posthog.com/api/users/@me/",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "email" in body:
        record(name, "ok", f"{body.get('email', '?')} via token ({source})")
    elif code == 401:
        record(name, "fail", "key invalid (401)",
               "# Regenerate: https://us.posthog.com/settings/user-api-keys")
    else:
        record(name, "warn", f"HTTP {code}")


def check_google_oauth():
    """Google OAuth: prefer gog CLI, fall back to token file refresh."""
    name = "google_oauth"
    rc_ver, _, _ = run_cmd(["gog", "--version"])
    if rc_ver != 127:
        # gog CLI installed — use it
        rc, out, err = run_cmd(["gog", "auth", "list"])
        combined = (out + " " + err).strip()
        if rc == 0 and "@" in combined:
            # gog is authenticated — get an access token for sub-checks
            rc2, token_out, _ = run_cmd(["gog", "auth", "token"], timeout=10)
            if rc2 == 0 and token_out.strip():
                os.environ["_GCHECK_ACCESS_TOKEN"] = token_out.strip()
            record(name, "ok", f"gog CLI: {combined[:100]}")
        else:
            record(name, "fail", "gog CLI installed but no accounts",
                   "gog auth credentials ~/path/to/client_secret.json\n"
                   "gog auth add you@gmail.com")
        return

    # No gog CLI — fall back to token file
    token, source = get_credential_source("google_oauth")
    if not token:
        record(name, "skip", f"gog CLI not installed, no token ({source})",
               "brew install gogcli && gog auth add you@gmail.com")
        return
    try:
        data = json.loads(token) if token.startswith("{") else json.loads(Path(
            _CREDENTIAL_REGISTRY["google_oauth"][1]).read_text())
    except Exception:
        record(name, "warn", "token file exists but invalid JSON")
        return

    if "refresh_token" not in data:
        record(name, "warn", "missing refresh_token — re-auth needed")
        return

    client_id = data.get("client_id", os.environ.get("GOOGLE_OAUTH_CLIENT_ID", ""))
    client_secret = data.get("client_secret", os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", ""))
    if not client_id or not client_secret:
        try:
            client_secret = Path(f"{CLAW_DIR}/.google_client_secret").read_text().strip()
        except Exception:
            pass
    if not client_id or not client_secret:
        record(name, "warn", "has refresh_token but missing client_id/client_secret")
        return

    code, body = http_json("https://oauth2.googleapis.com/token",
                           headers={"Content-Type": "application/x-www-form-urlencoded"},
                           data=urllib.parse.urlencode({
                               "client_id": client_id,
                               "client_secret": client_secret,
                               "refresh_token": data["refresh_token"],
                               "grant_type": "refresh_token",
                           }),
                           method="POST")
    if code == 200 and "access_token" in body:
        scopes = data.get("scope", "")
        scope_list = [s.split("/")[-1] for s in scopes.split() if "googleapis" in s]
        scope_str = ", ".join(scope_list[:5]) if scope_list else "unknown scopes"
        record(name, "ok", f"token refresh OK ({scope_str}) via {source}")
        os.environ["_GCHECK_ACCESS_TOKEN"] = body["access_token"]
    else:
        detail = body.get("error_description", body.get("error", f"HTTP {code}"))
        record(name, "fail", f"refresh failed: {detail}",
               "brew install gogcli && gog auth add you@gmail.com")


def _google_access_token():
    """Get a fresh Google access token (set by check_google_oauth)."""
    return os.environ.get("_GCHECK_ACCESS_TOKEN", "")


def check_ga4():
    token = _google_access_token()
    if not token:
        record("ga4", "skip", "no Google access token (google_oauth must pass first)")
        return
    prop_id = os.environ.get("GA4_PROPERTY_ID", "502068431")
    code, body = http_json(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps({"dateRanges": [{"startDate": "yesterday", "endDate": "yesterday"}],
                         "metrics": [{"name": "sessions"}]}),
        method="POST")
    if code == 200:
        rows = body.get("rows", [])
        sessions = rows[0]["metricValues"][0]["value"] if rows else "0"
        record("ga4", "ok", f"GA4 property {prop_id} — {sessions} sessions yesterday")
    elif code == 403:
        record("ga4", "fail", f"GA4 access denied (403) — check property {prop_id} permissions",
               "# Grant Analytics Viewer to the OAuth email on the GA4 property")
    else:
        msg = body.get("error", {}).get("message", f"HTTP {code}") if isinstance(body, dict) else str(code)
        record("ga4", "warn", f"{msg[:80]}")


def check_gsc():
    token = _google_access_token()
    if not token:
        record("gsc", "skip", "no Google access token (google_oauth must pass first)")
        return
    code, body = http_json("https://www.googleapis.com/webmasters/v3/sites",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "siteEntry" in body:
        sites = [s.get("siteUrl", "?") for s in body["siteEntry"]]
        record("gsc", "ok", f"Search Console — {len(sites)} site(s): {', '.join(sites[:3])}")
    elif code == 200:
        record("gsc", "warn", "Search Console accessible but no sites found")
    elif code == 403:
        record("gsc", "fail", "GSC access denied (403)",
               "# Grant Search Console access to the OAuth email")
    else:
        record("gsc", "warn", f"GSC returned HTTP {code}")


def check_gcal():
    token = _google_access_token()
    if not token:
        record("gcal", "skip", "no Google access token (google_oauth must pass first)")
        return
    code, body = http_json("https://www.googleapis.com/calendar/v3/calendars/primary",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "summary" in body:
        record("gcal", "ok", f"Calendar — {body['summary']}")
    elif code == 403 or code == 401:
        record("gcal", "fail", f"Calendar access denied ({code})",
               "# Ensure calendar scope is in OAuth token")
    else:
        record("gcal", "warn", f"Calendar returned HTTP {code}")


def check_gdrive():
    token = _google_access_token()
    if not token:
        record("gdrive", "skip", "no Google access token (google_oauth must pass first)")
        return
    code, body = http_json("https://www.googleapis.com/drive/v3/about?fields=user",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "user" in body:
        user = body["user"]
        record("gdrive", "ok", f"Drive — {user.get('displayName', '?')} ({user.get('emailAddress', '?')})")
    elif code == 403 or code == 401:
        record("gdrive", "fail", f"Drive access denied ({code})",
               "# Ensure drive scope is in OAuth token")
    else:
        record("gdrive", "warn", f"Drive returned HTTP {code}")


def check_gmail():
    token = _google_access_token()
    if not token:
        record("gmail", "skip", "no Google access token (google_oauth must pass first)")
        return
    code, body = http_json("https://gmail.googleapis.com/gmail/v1/users/me/profile",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "emailAddress" in body:
        record("gmail", "ok", f"Gmail — {body['emailAddress']} ({body.get('messagesTotal', '?')} messages)")
    elif code == 403 or code == 401:
        record("gmail", "fail", f"Gmail access denied ({code})",
               "# Ensure gmail.modify scope is in OAuth token")
    else:
        record("gmail", "warn", f"Gmail returned HTTP {code}")


def check_skool():
    """Skool auth chain: Google OAuth → Gmail (read login codes) → Skool cookies.
    No public API — all access via Playwright browser automation with persisted cookies.
    Bot admin account logs in via email code sent to Gmail.
    """
    cookie_path = Path(f"{CLAW_DIR}/cookies/skool-cookies.json")
    ws = os.environ.get("WORKSPACE_DIR", os.environ.get("OPENCLAW_WORKSPACE_DIR", ""))
    alt_path = Path(ws) / "downloads" / "skool-cookies.json" if ws else None
    path = cookie_path if cookie_path.exists() else alt_path if (alt_path and alt_path.exists()) else None

    # Check Gmail dependency (needed for re-login)
    has_gmail = bool(_google_access_token())

    if not path:
        fix = "# Skool has no API — auth via browser cookies + Gmail login codes\n"
        fix += "# 1. Ensure google_oauth + gmail checks pass (needed to read login codes)\n"
        fix += "# 2. Run: python3 tools/skool.py login"
        deps = "gmail: " + ("OK" if has_gmail else "MISSING (google_oauth must pass)")
        record("skool", "skip", f"no cookies ({deps})", fix)
        return

    try:
        cookies = json.loads(path.read_text())
        if not isinstance(cookies, list) or len(cookies) == 0:
            record("skool", "warn", "cookie file exists but empty/invalid",
                   "python3 tools/skool.py login")
            return

        # Check cookie age
        import time
        age_hours = (time.time() - path.stat().st_mtime) / 3600
        age_str = f"{age_hours:.0f}h ago" if age_hours < 48 else f"{age_hours / 24:.0f}d ago"
        gmail_note = "" if has_gmail else " | gmail: MISSING (can't re-login)"

        if age_hours > 168:  # 7 days
            record("skool", "warn",
                   f"cookies stale ({age_str}, {len(cookies)} cookies){gmail_note}",
                   "python3 tools/skool.py login")
        else:
            record("skool", "ok",
                   f"cookies valid ({age_str}, {len(cookies)} cookies){gmail_note}")
    except Exception as e:
        record("skool", "warn", f"cookie parse error: {e}")


def check_zoom():
    token, source = get_credential_source("zoom")
    if not token:
        record("zoom", "skip", f"no token ({source})",
               f"echo 'YOUR_TOKEN' > {CLAW_DIR}/.zoom_token && chmod 600 {CLAW_DIR}/.zoom_token")
        return
    code, body = http_json("https://api.zoom.us/v2/users/me",
                           headers={"Authorization": f"Bearer {token}"})
    if code == 200 and "email" in body:
        record("zoom", "ok", f"{body.get('first_name', '')} {body.get('last_name', '')} ({body['email']}) via {source}")
    elif code == 401:
        record("zoom", "fail", "token invalid/expired (401)",
               "# Zoom OAuth tokens expire quickly — may need refresh\n"
               "# See: https://marketplace.zoom.us/")
    else:
        record("zoom", "warn", f"Zoom returned HTTP {code}")


# ─── Registry ───────────────────────────────────────────────────────────────

CLI_CHECKS = {
    "git":           check_git,
    "node":          check_node,
    "pnpm":          check_pnpm,
    "python3":       check_python,
    "gh":            check_gh,
    "railway_cli":   check_railway_cli,
    "vercel_cli":    check_vercel_cli,
    "linear_cli":    check_linear_cli,
    "supabase_cli":  check_supabase_cli,
    "render_cli":    check_render_cli,
    "docker":        check_docker,
}

API_CHECKS = {
    # ── API tokens (no CLI — token is the interface) ──
    "openai_token":     check_openai_token,
    "anthropic_token":  check_anthropic_token,
    "gemini_token":     check_gemini_token,
    "xai_token":        check_xai_token,
    "perplexity_token": check_perplexity_token,
    "meta_token":       check_meta_token,
    "twilio":           check_twilio,
    "manychat_token":   check_manychat_token,
    "telegram_token":   check_telegram_token,
    "elevenlabs":       check_elevenlabs,
    "brave_token":      check_brave_token,
    "mailerlite":       check_mailerlite,
    "posthog":          check_posthog,
    "zoom":             check_zoom,
    # ── Google suite (gog CLI manages OAuth → per-API verify) ──
    "google_oauth":     check_google_oauth,
    "ga4":              check_ga4,
    "gsc":              check_gsc,
    "gcal":             check_gcal,
    "gdrive":           check_gdrive,
    "gmail":            check_gmail,
    # ── Browser auth ──
    "skool":            check_skool,
}

ALL_CHECKS = {**CLI_CHECKS, **API_CHECKS}


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Local credential & CLI health check.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--fix", action="store_true", help="Print fix commands for failures")
    parser.add_argument("--only", metavar="NAME", help="Check only this CLI or credential")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show failures/warnings")
    parser.add_argument("--json", action="store_true", dest="json_out", help="Output JSON")
    args = parser.parse_args()

    checks = {}
    if args.only:
        key = args.only.lower().replace("-", "_")
        if key not in ALL_CHECKS:
            close = [k for k in ALL_CHECKS if key in k]
            if close:
                print(f"Unknown check '{args.only}'. Did you mean: {', '.join(close)}?")
            else:
                print(f"Unknown check '{args.only}'. Available: {', '.join(ALL_CHECKS.keys())}")
            sys.exit(2)
        checks = {key: ALL_CHECKS[key]}
    else:
        checks = ALL_CHECKS

    if not args.json_out:
        print(f"\n{BOLD}{'═' * 60}{RESET}")
        print(f"{BOLD}  🔐 Local Credential & CLI Health Check{RESET}")
        print(f"{DIM}  Credential dir: {CLAW_DIR}{RESET}")
        claw_exists = Path(CLAW_DIR).exists()
        if not claw_exists:
            print(f"{YELLOW}  ⚠  {CLAW_DIR} does not exist — create it with:{RESET}")
            print(f"{DIM}     mkdir -p {CLAW_DIR} && chmod 700 {CLAW_DIR}{RESET}")
        print(f"{BOLD}{'═' * 60}{RESET}\n")

    # Run CLI checks
    if not args.only:
        if not args.json_out:
            runtime_count = sum(1 for k in checks if k in ("git", "node", "pnpm", "python3"))
            auth_count = len(CLI_CHECKS) - runtime_count
            print(f"{CYAN}  Runtime CLIs ({runtime_count}){RESET}")

    runtime_keys = {"git", "node", "pnpm", "python3"}
    cli_auth_printed = False
    api_printed = False

    for name, fn in checks.items():
        # Section headers
        if not args.json_out and not args.only:
            if name in CLI_CHECKS and name not in runtime_keys and not cli_auth_printed:
                print(f"\n{CYAN}  CLI Auth ({len(CLI_CHECKS) - len(runtime_keys)}){RESET}")
                cli_auth_printed = True
            if name in API_CHECKS and not api_printed:
                print(f"\n{CYAN}  API Credentials ({len(API_CHECKS)}){RESET}")
                api_printed = True
        try:
            fn()
        except Exception as e:
            record(name, "fail", f"check raised exception: {e}")

    if args.json_out:
        print(json.dumps(results, indent=2))
        failed = sum(1 for r in results if r["status"] == "fail")
        sys.exit(1 if failed else 0)

    for r in results:
        if args.quiet and r["status"] in ("ok", "skip"):
            continue
        ico = icon(r["status"])
        label = r["name"]
        print(f"  {ico} {BOLD}{label}{RESET}: {r['message']}")
        if args.fix and r["status"] in ("fail", "warn") and r.get("fix"):
            print(f"     {YELLOW}Fix:{RESET}")
            for line in r["fix"].splitlines():
                print(f"       {line}")
            print()

    total   = len(results)
    passed  = sum(1 for r in results if r["status"] == "ok")
    warned  = sum(1 for r in results if r["status"] == "warn")
    failed  = sum(1 for r in results if r["status"] == "fail")
    skipped = sum(1 for r in results if r["status"] == "skip")

    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"  {OK} {passed} passed  {WARN} {warned} warned  {FAIL} {failed} failed  {SKIP} {skipped} skipped  ({total} checks)")

    if failed == 0 and warned == 0:
        print(f"\n  {GREEN}{BOLD}All checks passed!{RESET}\n")
    elif failed == 0:
        print(f"\n  {YELLOW}Some warnings — check above.{RESET}")
        if not args.fix:
            print(f"  Run with {BOLD}--fix{RESET} for fix commands.\n")
    else:
        print(f"\n  {RED}{BOLD}{failed} check(s) need attention.{RESET}")
        if not args.fix:
            print(f"  Run with {BOLD}--fix{RESET} for fix commands.\n")
        else:
            print()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
