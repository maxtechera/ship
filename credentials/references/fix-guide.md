# Credential Fix Guide

Reference for regenerating, fixing, and understanding every credential in the workspace.

---

## Quick Legend

| Symbol | Meaning |
|--------|---------|
| 🧑 Max | Requires Max's action (browser, interactive OAuth, account access) |
| 🤖 Neo | Can be fixed autonomously (file creation, env vars, CLI) |
| ⚠️ Gotcha | Known pitfall — read carefully |

---

## Credentials

### 1. `.github_token` — GitHub Personal Access Token

**Location:** `/data/.clawdbot/.github_token`  
**Used by:** GitHub API calls, `gh` CLI backup auth, repository operations  
**Who fixes:** 🧑 Max (account access required)  
**Check:** `curl -s -H "Authorization: token $(cat /data/.clawdbot/.github_token)" https://api.github.com/user | jq .login`

**Regenerate:**
1. Go to https://github.com/settings/tokens/new
2. Scopes needed: `repo`, `workflow`, `read:org`, `read:user`
3. Copy the `ghp_...` token
4. `echo 'ghp_NEW_TOKEN' > /data/.clawdbot/.github_token && chmod 600 /data/.clawdbot/.github_token`

**Gotchas:**
- Fine-grained tokens have expiry dates — classic tokens are safer for long-term use
- Some tools use `gh` CLI separately; run `gh auth login` after updating the file

---

### 2. `.meta_token` — Facebook/Meta Graph API Token

**Location:** `/data/.clawdbot/.meta_token`  
**Used by:** Meta/Instagram analytics, content publishing, CRM sync  
**Who fixes:** 🧑 Max (Facebook account access required)  
**Check:** `curl -s "https://graph.facebook.com/v21.0/me?access_token=$(cat /data/.clawdbot/.meta_token)" | jq .name`

**Regenerate:**
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app → Generate Access Token
3. Get a **long-lived** token (60 days): Exchange via Graph API OAuth endpoint
4. `echo 'EAA_NEW_TOKEN' > /data/.clawdbot/.meta_token && chmod 600 /data/.clawdbot/.meta_token`

**Gotchas:**
- Short-lived tokens expire in ~1 hour — always use long-lived (60 day) tokens
- Long-lived tokens still expire; set a calendar reminder to renew monthly
- Page tokens and user tokens are different — ensure you have the right one
- Token may need specific permissions: `pages_read_engagement`, `instagram_basic`, etc.

---

### 3. `.linear_token` — Linear API Key

**Location:** `/data/.clawdbot/.linear_token`  
**Used by:** `tools/linear.py`, project/issue management  
**Who fixes:** 🧑 Max (Linear account access, or can share token for Neo to write)  
**Check:** `curl -s -X POST -H "Authorization: $(cat /data/.clawdbot/.linear_token)" -H "Content-Type: application/json" -d '{"query":"{ viewer { name } }"}' https://api.linear.app/graphql | jq .data.viewer.name`

**Regenerate:**
1. Go to https://linear.app/[YOUR_WORKSPACE]/settings/api
2. Create a new Personal API Key
3. `echo 'lin_api_NEW_KEY' > /data/.clawdbot/.linear_token && chmod 600 /data/.clawdbot/.linear_token`

**Gotchas:**
- Linear API keys don't expire but can be revoked
- The token format starts with `lin_api_`
- Workspace-scoped — one token per Linear workspace

---

### 4. `.linear_webhook_secret` — Linear Webhook Secret

**Location:** `/data/.clawdbot/.linear_webhook_secret`  
**Used by:** Linear webhook verification in the command center server  
**Who fixes:** 🤖 Neo (can generate and update, but Max must update Linear settings too)  
**Check:** `cat /data/.clawdbot/.linear_webhook_secret | wc -c` (should be >10)

**Regenerate:**
```bash
# Neo generates new secret
openssl rand -hex 32 > /data/.clawdbot/.linear_webhook_secret
chmod 600 /data/.clawdbot/.linear_webhook_secret
cat /data/.clawdbot/.linear_webhook_secret
# Max then updates Linear webhook settings with this secret:
# https://linear.app/[WORKSPACE]/settings/api → Webhooks → Edit → Secret
```

**Gotchas:**
- Must match the secret configured in Linear's webhook settings exactly
- After changing, restart the webhook server (Railway redeploy)

---

### 5. `.railway_token` — Railway API Token

**Location:** `/data/.clawdbot/.railway_token`  
**Used by:** Railway deployment management, `tools/railway.py`  
**Who fixes:** 🧑 Max (Railway account access required)  
**Check:** Uses GraphQL API — run `check_all.py --only railway`

**Regenerate:**
1. Go to https://railway.app/account/tokens
2. Create a new token (give it a descriptive name like "workspace-neo")
3. `echo 'YOUR_TOKEN' > /data/.clawdbot/.railway_token && chmod 600 /data/.clawdbot/.railway_token`

**Gotchas:**
- Railway tokens have no expiry but can be revoked
- Token has full account access — treat like a password

---

### 6. `.perplexity_token` — Perplexity API Key

**Location:** `/data/.clawdbot/.perplexity_token`  
**Used by:** `tools/research.py`, web-augmented AI queries  
**Who fixes:** 🧑 Max (Perplexity account, billing setup needed)  
**Check:** Run `check_all.py --only perplexity`

**Regenerate:**
1. Go to https://www.perplexity.ai/settings/api
2. Generate new API key (`pplx-...`)
3. `echo 'pplx-NEW_KEY' > /data/.clawdbot/.perplexity_token && chmod 600 /data/.clawdbot/.perplexity_token`

**Gotchas:**
- Perplexity API requires a paid subscription (Pro or API plan)
- Rate limits are per-minute — research tools have built-in backoff

---

### 7. `.twilio_sid` + `.twilio_token` — Twilio Credentials

**Location:** `/data/.clawdbot/.twilio_sid` and `/data/.clawdbot/.twilio_token`  
**Used by:** Wake-up calls, SMS notifications  
**Who fixes:** 🧑 Max (Twilio account access)  
**Check:** Run `check_all.py --only twilio`

**Regenerate:**
1. Go to https://console.twilio.com/
2. Find "Account SID" and "Auth Token" on the dashboard
3. `echo 'ACxxxxxxxxxxxxx' > /data/.clawdbot/.twilio_sid && chmod 600 /data/.clawdbot/.twilio_sid`
4. `echo 'your_auth_token' > /data/.clawdbot/.twilio_token && chmod 600 /data/.clawdbot/.twilio_token`

**Gotchas:**
- Auth token can be rotated in the console — rotate only if compromised
- Trial accounts have limited numbers and verification requirements
- Phone number in tools must match a verified Twilio number

---

### 8. `.google_analytics_token.json` — Google OAuth Token

**Location:** `/data/.clawdbot/.google_analytics_token.json`  
**Used by:** `tools/gcal.py`, `tools/gdrive.py`, GA4 analytics collection, GSC  
**Who fixes:** 🧑 Max (interactive browser OAuth required)  
**Check:** `cat /data/.clawdbot/.google_analytics_token.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if 'refresh_token' in d else 'MISSING refresh_token')"`

**Regenerate:**
```bash
# Max must run interactively (opens browser):
gog auth login --account YOUR_GOOGLE_EMAIL
```

**Gotchas:**
- ⚠️ **Container reprovision loses gog auth** — this is the most commonly broken credential
- After any container reprovision, Max must re-run `gog auth login`
- The token file is symlinked by gog — don't move or rename it
- Multiple Google accounts: use `--account [REDACTED_EMAIL]` flag
- Refresh tokens expire if unused for 6 months or if OAuth consent is revoked

---

### 9. `.manychat_token` — ManyChat API Token

**Location:** `/data/.clawdbot/.manychat_token`  
**Used by:** ManyChat automation, subscriber management  
**Who fixes:** 🧑 Max (ManyChat account access)  
**Check:** Run `check_all.py --only manychat`

**Regenerate:**
1. Go to https://manychat.com/settings/api
2. Generate a new API token
3. `echo 'NEW_TOKEN' > /data/.clawdbot/.manychat_token && chmod 600 /data/.clawdbot/.manychat_token`

**Gotchas:**
- ManyChat tokens are tied to a specific page/account
- Regenerating invalidates the old token immediately

---

### 10. `cookies/youtube.txt` — YouTube Session Cookies

**Location:** `/data/.clawdbot/cookies/youtube.txt`  
**Used by:** yt-dlp for authenticated YouTube downloads (age-restricted, private, membership)  
**Who fixes:** 🧑 Max (requires logged-in browser session)  
**Check:** `wc -l /data/.clawdbot/cookies/youtube.txt`

**Regenerate:**
1. Install browser extension: "Get cookies.txt LOCALLY" (Chrome/Firefox)
2. Log into YouTube in the browser
3. Click the extension → Export cookies for youtube.com
4. Save to `/data/.clawdbot/cookies/youtube.txt`
5. Verify Netscape cookie format (starts with `# Netscape HTTP Cookie File`)

**Gotchas:**
- Cookies expire with Google sessions — may need refresh every few months
- Using cookies from a real account risks session invalidation by Google
- Consider using a secondary Google account dedicated to this purpose

---

### 11. OpenAI API Key — `OPENAI_API_KEY`

**Location:** `openclaw.json` → `env.vars.OPENAI_API_KEY` (also in shell env)  
**Used by:** OpenAI completions, embeddings, via OpenClaw and tools  
**Who fixes:** 🧑 Max (billing account access), 🤖 Neo (can update the config file)  
**Check:** Run `check_all.py --only openai`

**Regenerate:**
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Update `openclaw.json` env.vars.OPENAI_API_KEY
4. Or: `openclaw config set env.vars.OPENAI_API_KEY 'sk-proj-NEW_KEY'`

**Gotchas:**
- Keys from different projects have different rate limits
- Organization ID may also be needed for some APIs
- `sk-proj-` prefix = project key (preferred); `sk-` = legacy key

---

### 12. xAI API Key — `XAI_API_KEY`

**Location:** `openclaw.json` → `env.vars.XAI_API_KEY` or `/data/.clawdbot/.xai_token`  
**Used by:** Grok model access via xAI API  
**Who fixes:** 🧑 Max (xAI account), 🤖 Neo (can update files)  
**Check:** Run `check_all.py --only xai`

**Regenerate:**
1. Go to https://console.x.ai/
2. API Keys → Create new key
3. Update `openclaw.json` env.vars.XAI_API_KEY or:
4. `echo 'xai-NEW_KEY' > /data/.clawdbot/.xai_token`

**Gotchas:**
- xAI API is in early access — availability may change
- The key starts with `xai-`

---

### 13. Telegram Bot Token

**Location:** `openclaw.json` → `channels.telegram.botToken`  
**Used by:** All Telegram messaging — this is the core communication channel  
**Who fixes:** 🧑 Max (Telegram account, @BotFather)  
**Check:** Run `check_all.py --only telegram`

**Regenerate:**
1. Open Telegram → search for @BotFather
2. Send `/token` and select your bot
3. Copy the new token
4. Update `openclaw.json`: `channels.telegram.botToken`
5. Restart the gateway: `openclaw gateway restart`

**Gotchas:**
- Changing the bot token invalidates all existing webhook registrations
- After token change, OpenClaw may need to re-register the webhook
- The bot username and ID stay the same — only the token changes

---

## Integrations

### Google OAuth (gog CLI)

**Check:** `gog auth list`
**Who fixes:** 🧑 Max

```bash
# Re-authenticate:
gog auth login --account YOUR_GOOGLE_EMAIL

# List authenticated accounts:
gog auth list

# Remove an account:
gog auth logout --account YOUR_GOOGLE_EMAIL
```

**⚠️ Gotcha:** Lost on every container reprovision. Max must re-run after each reprovision. Consider adding to workspace setup checklist.

---

### GitHub CLI (`gh`)

**Check:** `gh auth status`  
**Who fixes:** 🤖 Neo (if `.github_token` is valid)  

```bash
# Auth using existing token file:
export GH_TOKEN=$(cat /data/.clawdbot/.github_token)
gh auth status

# Or interactive login:
gh auth login --with-token < /data/.clawdbot/.github_token
```

---

### CRM Database

**Location:** `data/crm.db`  
**Check:** `python3 tools/crm.py stats`  
**Who fixes:** 🤖 Neo  

```bash
# Initialize/rebuild:
python3 tools/crm.py import gmail --days 90
python3 tools/crm.py import whatsapp --file /path/to/export.txt

# Check schema:
sqlite3 data/crm.db ".schema"
```

---

### Finance Database

**Location:** Varies — check `tools/finance-v2.py` for DB_PATH  
**Check:** `python3 tools/finance-v2.py stats`  
**Who fixes:** 🤖 Neo  

```bash
# Scan for transactions:
python3 tools/finance-v2.py scan
python3 tools/finance-v2.py stats
```

---

### Analytics Database

**Location:** `data/analytics.db`  
**Check:** `sqlite3 data/analytics.db ".tables"`  
**Who fixes:** 🤖 Neo  

```bash
# Collect new data:
python3 tools/analytics-collector.py --collect

# Check tables:
sqlite3 data/analytics.db ".tables"
sqlite3 data/analytics.db "SELECT COUNT(*) FROM pageviews" 2>/dev/null
```

---

### Search Database

**Location:** `data/search.db`  
**Check:** `sqlite3 data/search.db ".tables"`  
**Who fixes:** 🤖 Neo  

```bash
# Rebuild index:
python3 tools/content-engine.py pitch "topic" --research
# or:
python3 tools/content-pipeline-search.py rebuild
```

---

### Research Queue

**Location:** `data/research-queue.db`  
**Check:** `python3 tools/research-queue.py status`  
**Who fixes:** 🤖 Neo  

```bash
# Check queue:
python3 tools/research-queue.py status

# Add item:
python3 tools/research-queue.py add "topic to research"

# Process queue:
python3 tools/research-queue.py process
```

---

### yt-dlp

**Check:** `yt-dlp --version`  
**Who fixes:** 🤖 Neo  

```bash
# Install:
pip install yt-dlp
# Or:
pipx install yt-dlp
# Or:
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
chmod +x /usr/local/bin/yt-dlp

# Update:
yt-dlp -U

# Test with cookies:
yt-dlp --cookies /data/.clawdbot/cookies/youtube.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --print title
```

---

## Common Failure Scenarios

### "Container was reprovisioned"
After a container reprovision, you lose:
- Google OAuth (gog auth) — **must re-run `gog auth login`**
- Any env vars not in `openclaw.json`
- `/tmp` files

You keep:
- Everything in `/data/` (persistent volume)
- `openclaw.json` config
- All credential files in `/data/.clawdbot/`

### "Token worked yesterday, broken today"
Likely causes:
1. Meta token expired (60-day limit) → regenerate
2. YouTube cookies expired → re-export from browser
3. Google OAuth revoked (6-month inactivity) → re-auth

### "Symlinks broken after git operations"
Some tools use symlinks. After git ops:
```bash
ls -la /data/.clawdbot/ | grep "^l"  # Check for broken symlinks
```

### "API key works in curl but not in tool"
Check for:
- Trailing newlines in token files: `cat -A /data/.clawdbot/.token | tail -1`
- Wrong env var name in tool code
- Tool reading from wrong location

Fix trailing newlines:
```bash
# Most credential files are written correctly, but to check:
python3 -c "t=open('/data/.clawdbot/.github_token').read(); print(repr(t[-3:]))"
```
