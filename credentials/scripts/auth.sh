#!/bin/bash
# credentials/scripts/auth.sh
#
# Interactive auth wizard — shows whoami for every service,
# then offers to authenticate any that need it.
#
# Usage:
#   bash credentials/scripts/auth.sh
#   bash credentials/scripts/auth.sh --only linear
#   bash credentials/scripts/auth.sh --list
#
# Credential dir priority:
#   SHIP_CRED_DIR → OPENCLAW_CRED_DIR (legacy) → /data/.clawdbot (container)
#   → ~/.clawdbot (legacy) → ~/.config/ship/credentials (default)

set -uo pipefail

GREEN="\033[92m"
RED="\033[91m"
YELLOW="\033[93m"
CYAN="\033[96m"
BOLD="\033[1m"
DIM="\033[2m"
RESET="\033[0m"

# ── Resolve credential directory ──
if [[ -n "${SHIP_CRED_DIR:-}" ]]; then
  CRED_DIR="$SHIP_CRED_DIR"
elif [[ -n "${OPENCLAW_CRED_DIR:-}" ]]; then
  CRED_DIR="$OPENCLAW_CRED_DIR"
elif [[ -d "/data/.clawdbot" ]]; then
  CRED_DIR="/data/.clawdbot"
elif [[ -d "$HOME/.clawdbot" ]]; then
  CRED_DIR="$HOME/.clawdbot"
else
  CRED_DIR="$HOME/.config/ship/credentials"
fi

# ── Helper: read token from env or file ──
_token() {
  local env_var="$1" file="$2"
  local val="${!env_var:-}"
  [[ -n "$val" ]] && { echo "$val"; return; }
  [[ -f "$file" ]] && cat "$file" 2>/dev/null | tr -d '\n'
}

_mask() {
  local t="$1"
  [[ ${#t} -le 8 ]] && { echo "${t:0:4}…"; return; }
  echo "${t:0:4}…${t: -4}"
}

# ── Helper: save token to file ──
_save_token() {
  local file="$1" token="$2"
  mkdir -p "$(dirname "$file")"
  echo -n "$token" > "$file"
  chmod 600 "$file"
}

# ── Prompt for token ──
_prompt_token() {
  local name="$1" file="$2" prefix="$3" url="$4"
  echo -e "  ${DIM}Get from: ${url}${RESET}"
  echo -e "  ${DIM}Will save to: ${file}${RESET}"
  [[ -n "$prefix" ]] && echo -e "  ${DIM}Expected prefix: ${prefix}${RESET}"
  echo ""
  read -p "  Paste token (or 's' to skip): " token
  if [[ "$token" == "s" || "$token" == "S" || -z "$token" ]]; then
    echo -e "  ${YELLOW}Skipped${RESET}"
    return 1
  fi
  _save_token "$file" "$token"
  echo -e "  ✅ Saved $(_mask "$token") → $file"
  return 0
}

# ════════════════════════════════════════════════════════════
# Whoami functions — return "status|identity"
# ════════════════════════════════════════════════════════════

# ── CLI Auth ──

whoami_gh() {
  command -v gh &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(gh auth status 2>&1)
  if echo "$out" | grep -qi "logged in"; then
    local user; user=$(echo "$out" | grep -oP 'account \K\S+' 2>/dev/null || echo "authenticated")
    echo "ok|$user"
  else
    echo "need_auth|not authenticated"
  fi
}

whoami_railway() {
  command -v railway &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(railway whoami 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  echo "$out" | grep -qvi "not logged" && echo "ok|$(echo "$out" | head -1)" || echo "need_auth|not authenticated"
}

whoami_vercel() {
  command -v vercel &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(vercel whoami 2>/dev/null)
  [[ -n "$out" ]] && echo "ok|$out" || echo "need_auth|not authenticated"
}

whoami_linear() {
  command -v linear &>/dev/null || { echo "missing|not installed"; return; }
  local ws; ws=$(linear auth list 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -v '^$' | head -1)
  [[ -n "$ws" ]] && echo "ok|$ws" || echo "need_auth|not authenticated"
}

whoami_supabase() {
  command -v supabase &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(supabase projects list 2>&1)
  echo "$out" | grep -qvi "not logged\|access token" && echo "ok|authenticated" || echo "need_auth|not authenticated"
}

whoami_render() {
  command -v render &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(render whoami 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  if echo "$out" | grep -qvi "run.*login\|failed"; then
    local info; info=$(echo "$out" | grep -iE "Name:|Email:" | head -2 | tr '\n' ' ')
    echo "ok|${info:-authenticated}"
  else
    echo "need_auth|not authenticated"
  fi
}

whoami_twilio() {
  command -v twilio &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(twilio profiles:list 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  if echo "$out" | grep -q "AC" 2>/dev/null; then
    local active; active=$(echo "$out" | grep -E 'true|Active|\*' | head -1 | xargs)
    echo "ok|${active:-profile configured}"
  else
    echo "need_auth|no profiles"
  fi
}

whoami_elevenlabs() {
  command -v elevenlabs &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(elevenlabs auth whoami 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  if echo "$out" | grep -qi "not logged\|unauthenticated\|error"; then
    echo "need_auth|not authenticated"
  elif [[ -n "$out" ]]; then
    echo "ok|$(echo "$out" | head -1)"
  else
    echo "need_auth|not authenticated"
  fi
}

whoami_mailerlite() {
  command -v mailerlite &>/dev/null || { echo "missing|not installed"; return; }
  local out; out=$(mailerlite account list 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  if echo "$out" | grep -qvi "error\|login\|unauthorized" && [[ -n "$out" ]]; then
    echo "ok|$(echo "$out" | head -1)"
  else
    echo "need_auth|not authenticated"
  fi
}

whoami_posthog() {
  command -v posthog-cli &>/dev/null || { echo "missing|not installed"; return; }
  [[ -f "$HOME/.posthog/credentials.json" ]] && echo "ok|credentials at ~/.posthog" || echo "need_auth|no credentials"
}

whoami_gog() {
  command -v gog &>/dev/null || { echo "missing|not installed (brew install gogcli)"; return; }
  local out; out=$(gog auth list 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  if echo "$out" | grep -q "@"; then
    echo "ok|$(echo "$out" | grep "@" | xargs)"
  else
    echo "need_auth|no accounts"
  fi
}

# ── API Token Auth ──

whoami_openai() {
  local t; t=$(_token OPENAI_API_KEY "$CRED_DIR/.openai_token")
  [[ -z "$t" ]] && { echo "need_auth|no key"; return; }
  local code; code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $t" https://api.openai.com/v1/models --max-time 5)
  [[ "$code" == "200" ]] && echo "ok|key valid ($(_mask "$t"))" || echo "need_auth|key invalid ($code)"
}

whoami_anthropic() {
  local t; t=$(_token ANTHROPIC_API_KEY "$CRED_DIR/.anthropic_token")
  [[ -z "$t" ]] && { echo "need_auth|no key"; return; }
  local code; code=$(curl -s -o /dev/null -w "%{http_code}" -H "x-api-key: $t" -H "anthropic-version: 2023-06-01" https://api.anthropic.com/v1/models?limit=1 --max-time 5)
  [[ "$code" == "200" ]] && echo "ok|key valid ($(_mask "$t"))" || echo "need_auth|key invalid ($code)"
}

whoami_gemini() {
  local t; t=$(_token GEMINI_API_KEY "$CRED_DIR/.gemini_token")
  [[ -z "$t" ]] && { echo "need_auth|no key"; return; }
  local code; code=$(curl -s -o /dev/null -w "%{http_code}" "https://generativelanguage.googleapis.com/v1beta/models?key=$t" --max-time 5)
  [[ "$code" == "200" ]] && echo "ok|key valid ($(_mask "$t"))" || echo "need_auth|key invalid ($code)"
}

whoami_xai() {
  local t; t=$(_token XAI_API_KEY "$CRED_DIR/.xai_token")
  [[ -z "$t" ]] && { echo "need_auth|no key"; return; }
  local code; code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $t" https://api.x.ai/v1/models --max-time 5)
  [[ "$code" == "200" ]] && echo "ok|key valid ($(_mask "$t"))" || echo "need_auth|key invalid ($code)"
}

whoami_perplexity() {
  local t; t=$(_token PERPLEXITY_KEY "$CRED_DIR/.perplexity_token")
  [[ -z "$t" ]] && { t=$(_token PERPLEXITY_API_KEY ""); }
  [[ -z "$t" ]] && { echo "need_auth|no key"; return; }
  local code; code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $t" -H "Content-Type: application/json" -d '{"model":"sonar","messages":[{"role":"user","content":"ping"}],"max_tokens":1}' https://api.perplexity.ai/chat/completions --max-time 10)
  [[ "$code" == "200" ]] && echo "ok|key valid ($(_mask "$t"))" || echo "need_auth|key invalid ($code)"
}

whoami_meta() {
  local t; t=$(_token META_ACCESS_TOKEN "$CRED_DIR/.meta_token")
  [[ -z "$t" ]] && { t=$(_token META_TOKEN ""); }
  [[ -z "$t" ]] && { echo "need_auth|no token"; return; }
  local body; body=$(curl -s "https://graph.facebook.com/v21.0/me?access_token=$t" --max-time 5)
  if echo "$body" | grep -q '"name"'; then
    local name; name=$(echo "$body" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','?'))" 2>/dev/null || echo "?")
    echo "ok|$name ($(_mask "$t"))"
  else
    echo "need_auth|token invalid or expired"
  fi
}

whoami_telegram() {
  local t; t=$(_token TELEGRAM_BOT_TOKEN "$CRED_DIR/.telegram_bot_token")
  [[ -z "$t" ]] && { echo "need_auth|no token"; return; }
  local body; body=$(curl -s "https://api.telegram.org/bot${t}/getMe" --max-time 5)
  if echo "$body" | grep -q '"ok":true'; then
    local user; user=$(echo "$body" | python3 -c "import sys,json; print('@'+json.load(sys.stdin)['result']['username'])" 2>/dev/null || echo "bot")
    echo "ok|$user"
  else
    echo "need_auth|token invalid"
  fi
}

whoami_brave() {
  local t; t=$(_token BRAVE_API_KEY "$CRED_DIR/.brave_token")
  [[ -z "$t" ]] && { echo "need_auth|no key"; return; }
  local code; code=$(curl -s -o /dev/null -w "%{http_code}" -H "X-Subscription-Token: $t" "https://api.search.brave.com/res/v1/web/search?q=test&count=1" --max-time 5)
  [[ "$code" == "200" ]] && echo "ok|key valid ($(_mask "$t"))" || echo "need_auth|key invalid ($code)"
}

whoami_manychat() {
  local t; t=$(_token MANYCHAT_TOKEN "$CRED_DIR/.manychat_token")
  [[ -z "$t" ]] && { echo "need_auth|no token"; return; }
  local body; body=$(curl -s -H "Authorization: Bearer $t" "https://api.manychat.com/fb/page/getInfo" --max-time 5)
  if echo "$body" | grep -q '"success"'; then
    echo "ok|page connected ($(_mask "$t"))"
  else
    echo "need_auth|token invalid"
  fi
}

whoami_zoom() {
  local acct cid csec
  acct=$(cat "$CRED_DIR/.zoom_account_id" 2>/dev/null | tr -d '\n')
  cid=$(cat "$CRED_DIR/.zoom_client_id" 2>/dev/null | tr -d '\n')
  csec=$(cat "$CRED_DIR/.zoom_client_secret" 2>/dev/null | tr -d '\n')
  if [[ -z "$acct" || -z "$cid" || -z "$csec" ]]; then
    echo "need_auth|missing credentials (need account_id + client_id + client_secret)"
    return
  fi
  local creds; creds=$(echo -n "${cid}:${csec}" | base64)
  local tok_resp; tok_resp=$(curl -s -X POST "https://zoom.us/oauth/token" \
    -H "Authorization: Basic ${creds}" -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=account_credentials&account_id=${acct}" --max-time 5)
  local access; access=$(echo "$tok_resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)
  if [[ -z "$access" ]]; then
    local err; err=$(echo "$tok_resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('reason','token error'))" 2>/dev/null)
    echo "need_auth|$err"
    return
  fi
  local body; body=$(curl -s -H "Authorization: Bearer $access" "https://api.zoom.us/v2/users/me" --max-time 5)
  if echo "$body" | grep -q '"email"'; then
    local who; who=$(echo "$body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d.get(\"first_name\",\"?\")} {d.get(\"last_name\",\"?\")} ({d.get(\"email\",\"?\")})')" 2>/dev/null)
    echo "ok|$who"
  else
    echo "need_auth|API call failed"
  fi
}

# ── Google sub-services (use gog CLI directly) ──

_gog_access_token() {
  # Get an access token via gog CLI for APIs it doesn't directly wrap (GA4, GSC)
  command -v gog &>/dev/null || return 1
  local email; email=$(gog auth list --plain 2>&1 | awk '{print $1}' | head -1)
  [[ -z "$email" || "$email" == *"error"* ]] && return 1
  local export_file="/tmp/.gog_export_$$.json"
  gog auth tokens export "$email" --out "$export_file" --overwrite </dev/null >/dev/null 2>&1
  [[ ! -f "$export_file" ]] && return 1
  python3 -c "
import json, urllib.request, urllib.parse, os
export = json.load(open('${export_file}'))
creds = json.load(open(os.path.expanduser('~/Library/Application Support/gogcli/credentials.json')))
installed = creds.get('installed', creds.get('web', creds))
data = urllib.parse.urlencode({
    'client_id': installed['client_id'], 'client_secret': installed['client_secret'],
    'refresh_token': export['refresh_token'], 'grant_type': 'refresh_token'
}).encode()
resp = urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token', data), timeout=10)
print(json.loads(resp.read())['access_token'])
" 2>/dev/null
  rm -f "$export_file"
}

whoami_ga4() {
  command -v gog &>/dev/null || { echo "need_auth|gog not installed"; return; }
  gog auth list 2>&1 | grep -q "@" || { echo "need_auth|gog not authenticated"; return; }
  local t; t=$(_gog_access_token)
  [[ -z "$t" ]] && { echo "need_auth|could not get access token"; return; }
  local prop="${GA4_PROPERTY_ID:-}"
  if [[ -z "$prop" ]]; then
    echo "need_auth|set GA4_PROPERTY_ID env var to test"
    return
  fi
  local body; body=$(curl -s -X POST \
    "https://analyticsdata.googleapis.com/v1beta/properties/${prop}:runReport" \
    -H "Authorization: Bearer $t" -H "Content-Type: application/json" \
    -d '{"dateRanges":[{"startDate":"yesterday","endDate":"yesterday"}],"metrics":[{"name":"sessions"}]}' --max-time 5)
  if echo "$body" | grep -q '"rows"\|"rowCount"'; then
    local sessions; sessions=$(echo "$body" | python3 -c "import sys,json; rows=json.load(sys.stdin).get('rows',[]); print(rows[0]['metricValues'][0]['value'] if rows else '0')" 2>/dev/null || echo "?")
    echo "ok|property $prop — $sessions sessions yesterday"
  elif echo "$body" | grep -q "403\|PERMISSION_DENIED"; then
    local acct; acct=$(gog auth list --plain 2>&1 | awk '{print $1}' | head -1)
    echo "need_auth|GA4 403 — add analytics.readonly scope to OAuth client, then: gog auth add ${acct} --force-consent"
  else
    echo "need_auth|GA4 error"
  fi
}

whoami_gsc() {
  command -v gog &>/dev/null || { echo "need_auth|gog not installed"; return; }
  gog auth list 2>&1 | grep -q "@" || { echo "need_auth|gog not authenticated"; return; }
  local t; t=$(_gog_access_token)
  [[ -z "$t" ]] && { echo "need_auth|could not get access token"; return; }
  local body; body=$(curl -s -H "Authorization: Bearer $t" "https://www.googleapis.com/webmasters/v3/sites" --max-time 5)
  if echo "$body" | grep -q "siteEntry"; then
    local sites; sites=$(echo "$body" | python3 -c "import sys,json; print(', '.join(s['siteUrl'] for s in json.load(sys.stdin).get('siteEntry',[])[:3]))" 2>/dev/null || echo "?")
    echo "ok|$sites"
  elif echo "$body" | grep -q "403\|PERMISSION_DENIED"; then
    local acct; acct=$(gog auth list --plain 2>&1 | awk '{print $1}' | head -1)
    echo "need_auth|GSC 403 — add webmasters.readonly scope to OAuth client, then: gog auth add ${acct} --force-consent"
  else
    echo "need_auth|GSC error"
  fi
}

whoami_gcal() {
  command -v gog &>/dev/null || { echo "need_auth|gog not installed"; return; }
  gog auth list 2>&1 | grep -q "@" || { echo "need_auth|gog not authenticated"; return; }
  local out; out=$(gog calendar calendars --max 3 --plain 2>&1 | head -3)
  if [[ -n "$out" ]] && ! echo "$out" | grep -qi "error"; then
    echo "ok|$(echo "$out" | head -1 | sed 's/\x1b\[[0-9;]*m//g')"
  else
    echo "need_auth|calendar access denied"
  fi
}

whoami_gdrive() {
  command -v gog &>/dev/null || { echo "need_auth|gog not installed"; return; }
  gog auth list 2>&1 | grep -q "@" || { echo "need_auth|gog not authenticated"; return; }
  local out; out=$(gog drive ls --max 1 --json 2>&1)
  if echo "$out" | grep -q '"files"'; then
    local name; name=$(echo "$out" | python3 -c "import sys,json; f=json.load(sys.stdin).get('files',[]); print(f[0].get('name','?')[:40] if f else 'empty')" 2>/dev/null || echo "accessible")
    echo "ok|recent: $name"
  else
    echo "need_auth|drive access denied"
  fi
}

whoami_gmail() {
  command -v gog &>/dev/null || { echo "need_auth|gog not installed"; return; }
  gog auth list 2>&1 | grep -q "@" || { echo "need_auth|gog not authenticated"; return; }
  local out; out=$(gog gmail search "is:inbox" --max 1 --json 2>&1)
  if echo "$out" | grep -q '"threads"'; then
    local subj; subj=$(echo "$out" | python3 -c "import sys,json; t=json.load(sys.stdin).get('threads',[]); print(t[0].get('subject','?')[:50] if t else 'empty inbox')" 2>/dev/null || echo "accessible")
    echo "ok|inbox — latest: $subj"
  else
    echo "need_auth|gmail access denied"
  fi
}

whoami_instagram() {
  local t; t=$(_token META_ACCESS_TOKEN "$CRED_DIR/.meta_token")
  [[ -z "$t" ]] && { t=$(_token META_TOKEN ""); }
  [[ -z "$t" ]] && { echo "need_auth|no Meta token (IG uses same token)"; return; }
  local body; body=$(curl -s "https://graph.facebook.com/v21.0/me/accounts?fields=instagram_business_account,name&access_token=$t" --max-time 5)
  if echo "$body" | grep -q "instagram_business_account"; then
    local accounts; accounts=$(echo "$body" | python3 -c "
import sys,json
pages=json.load(sys.stdin).get('data',[])
igs=[p['name'] for p in pages if p.get('instagram_business_account')]
print(f'{len(igs)} account(s): {\", \".join(igs)}')
" 2>/dev/null || echo "connected")
    echo "ok|$accounts"
  elif echo "$body" | grep -q '"data"'; then
    echo "need_auth|Meta token valid but no IG Business accounts linked"
  else
    echo "need_auth|Meta token invalid for IG"
  fi
}

whoami_whatsapp() {
  local t; t=$(_token META_ACCESS_TOKEN "$CRED_DIR/.meta_token")
  [[ -z "$t" ]] && { t=$(_token META_TOKEN ""); }
  [[ -z "$t" ]] && { echo "need_auth|no Meta token (WA uses same token)"; return; }
  local body; body=$(curl -s "https://graph.facebook.com/v21.0/me?fields=businesses&access_token=$t" --max-time 5)
  if echo "$body" | grep -q '"businesses"'; then
    local biz; biz=$(echo "$body" | python3 -c "
import sys,json
d=json.load(sys.stdin)
bs=d.get('businesses',{}).get('data',[])
print(f'{len(bs)} business(es): {\", \".join(b[\"name\"] for b in bs[:3])}')
" 2>/dev/null || echo "connected")
    echo "ok|$biz"
  else
    echo "need_auth|no WhatsApp Business access"
  fi
}

whoami_mercadopago() {
  local t; t=$(_token MERCADOPAGO_ACCESS_TOKEN "$CRED_DIR/.mercadopago_token")
  [[ -z "$t" ]] && { echo "need_auth|no token"; return; }
  local body; body=$(curl -s -H "Authorization: Bearer $t" "https://api.mercadopago.com/users/me" --max-time 5)
  if echo "$body" | grep -q '"nickname"'; then
    local who; who=$(echo "$body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d.get(\"nickname\",\"?\")} ({d.get(\"email\",\"?\")})')" 2>/dev/null)
    echo "ok|$who"
  else
    echo "need_auth|token invalid"
  fi
}

whoami_meta_pixel() {
  local t; t=$(_token META_ACCESS_TOKEN "$CRED_DIR/.meta_token")
  [[ -z "$t" ]] && { t=$(_token META_TOKEN ""); }
  [[ -z "$t" ]] && { echo "need_auth|no Meta token"; return; }
  local body; body=$(curl -s "https://graph.facebook.com/v21.0/me/adaccounts?fields=adspixels.limit(1)\{name,id\},name&limit=10&access_token=$t" --max-time 5)
  local pixels; pixels=$(echo "$body" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pxs=[]
for a in d.get('data',[]):
    for p in a.get('adspixels',{}).get('data',[]):
        pxs.append(p['name'])
if pxs:
    print(f'{len(pxs)} pixel(s): {chr(44).join(pxs[:4])}')
else:
    print('no pixels found')
" 2>/dev/null || echo "parse error")
  if [[ "$pixels" == *"pixel"* ]]; then
    echo "ok|$pixels"
  else
    echo "need_auth|$pixels"
  fi
}

whoami_google_merchant() {
  local t; t=$(_gog_access_token)
  [[ -z "$t" ]] && { echo "need_auth|gog not authenticated"; return; }
  local body; body=$(curl -s -H "Authorization: Bearer $t" "https://merchantapi.googleapis.com/accounts/v1beta/accounts" --max-time 5)
  if echo "$body" | grep -q '"accounts"'; then
    local count; count=$(echo "$body" | python3 -c "import sys,json; accts=json.load(sys.stdin).get('accounts',[]); print(f'{len(accts)} account(s): {\", \".join(a.get(\"accountName\",\"?\") for a in accts[:3])}')" 2>/dev/null)
    echo "ok|$count"
  elif [[ "$body" == "{}" ]]; then
    echo "ok|API accessible (no merchant accounts)"
  elif echo "$body" | grep -q "403"; then
    echo "need_auth|enable Merchant API + add content scope to gog"
  else
    echo "need_auth|API error"
  fi
}

whoami_google_ads() {
  local t; t=$(_gog_access_token)
  [[ -z "$t" ]] && { echo "need_auth|gog not authenticated"; return; }
  local dev_token; dev_token=$(cat "$CRED_DIR/.google_ads_dev_token" 2>/dev/null | tr -d '\n')
  if [[ -z "$dev_token" ]]; then
    # No dev token — check if adwords scope is at least in the OAuth token
    local email; email=$(gog auth list --plain 2>&1 | awk '{print $1}' | head -1)
    local scopes; scopes=$(gog auth tokens export "$email" --out /tmp/.gog_ads_check.json --overwrite >/dev/null 2>&1 && python3 -c "
import json, urllib.request, urllib.parse, os
export = json.load(open('/tmp/.gog_ads_check.json'))
creds = json.load(open(os.path.expanduser('~/Library/Application Support/gogcli/credentials.json')))
installed = creds.get('installed', creds.get('web', creds))
data = urllib.parse.urlencode({'client_id': installed['client_id'], 'client_secret': installed['client_secret'], 'refresh_token': export['refresh_token'], 'grant_type': 'refresh_token'}).encode()
resp = urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token', data), timeout=10)
print('yes' if 'adwords' in json.loads(resp.read()).get('scope','') else 'no')
" 2>/dev/null)
    rm -f /tmp/.gog_ads_check.json
    if [[ "$scopes" == "yes" ]]; then
      echo "ok|OAuth scope ready (need developer token from Google Ads → API Center)"
    else
      echo "need_auth|adwords scope missing — re-auth gog with --extra-scopes"
    fi
    return
  fi
  local body; body=$(curl -s -H "Authorization: Bearer $t" -H "developer-token: $dev_token" \
    "https://googleads.googleapis.com/v20/customers:listAccessibleCustomers" --max-time 5)
  if echo "$body" | grep -q "resourceNames"; then
    local count; count=$(echo "$body" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('resourceNames',[])))" 2>/dev/null)
    echo "ok|$count accessible customer(s)"
  else
    echo "need_auth|dev token invalid or API error"
  fi
}

whoami_mercadolibre() {
  local t=""
  if [[ -f "$CRED_DIR/.mercadolibre.json" ]]; then
    t=$(python3 -c "import json; print(json.load(open('$CRED_DIR/.mercadolibre.json'))['access_token'])" 2>/dev/null)
  fi
  [[ -z "$t" ]] && { echo "need_auth|no token ($CRED_DIR/.mercadolibre.json)"; return; }
  local body; body=$(curl -s -H "Authorization: Bearer $t" "https://api.mercadolibre.com/users/me" --max-time 5)
  if echo "$body" | grep -q '"nickname"'; then
    local who; who=$(echo "$body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"nickname\"]} (site={d.get(\"site_id\",\"?\")})')" 2>/dev/null)
    echo "ok|$who"
  else
    echo "need_auth|token expired — needs refresh"
  fi
}

whoami_notion() {
  command -v notion &>/dev/null || { echo "missing|not installed (brew install 4ier/tap/notion-cli)"; return; }
  local out; out=$(notion auth status 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
  if echo "$out" | grep -qi "authenticated\|connected\|workspace\|logged in\|bot_id\|workspace_name" && ! echo "$out" | grep -qi "not auth\|not logged\|not connected"; then
    local info; info=$(echo "$out" | grep -v '^$' | head -2 | tr '\n' ' ')
    echo "ok|${info:-authenticated}"
    return
  fi
  # CLI not authed — try token fallback
  local t; t=$(_token NOTION_API_KEY "$CRED_DIR/.notion_token")
  if [[ -n "$t" ]]; then
    local body; body=$(curl -s -H "Authorization: Bearer $t" -H "Notion-Version: 2022-06-28" "https://api.notion.com/v1/users/me" --max-time 5)
    if echo "$body" | grep -q '"name"'; then
      local name; name=$(echo "$body" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','?'))" 2>/dev/null || echo "?")
      echo "ok|$name (via token)"
      return
    fi
  fi
  echo "need_auth|not authenticated"
}

# ════════════════════════════════════════════════════════════
# Entry registry
# ════════════════════════════════════════════════════════════

# name;whoami_fn;auth_type;auth_cmd_or_file;description
# auth_type: cli (run command) | token (paste + save to file) | gog | zoom | dep
ENTRIES=(
  # ── Platform CLIs ──
  "gh;whoami_gh;cli;gh auth login;GitHub CLI"
  "railway;whoami_railway;cli;railway login;Railway CLI"
  "vercel;whoami_vercel;cli;vercel login;Vercel CLI"
  "linear;whoami_linear;cli;linear auth login;Linear CLI"
  "supabase;whoami_supabase;cli;supabase login;Supabase CLI"
  "render;whoami_render;cli;render login;Render CLI"
  # ── API CLIs ──
  "twilio;whoami_twilio;cli;twilio profiles:create;Twilio CLI"
  "elevenlabs;whoami_elevenlabs;cli;elevenlabs auth login;ElevenLabs CLI"
  "mailerlite;whoami_mailerlite;cli;mailerlite auth login;MailerLite CLI"
  "posthog;whoami_posthog;cli;posthog-cli login;PostHog CLI"
  # ── Google (gog CLI → sub-services) ──
  "gog;whoami_gog;gog;_;Google OAuth (gog CLI)"
  "ga4;whoami_ga4;dep;gog;Google Analytics 4"
  "gsc;whoami_gsc;dep;gog;Google Search Console"
  "gcal;whoami_gcal;dep;gog;Google Calendar"
  "gdrive;whoami_gdrive;dep;gog;Google Drive"
  "gmail;whoami_gmail;dep;gog;Gmail"
  "google_merchant;whoami_google_merchant;dep;gog;Google Merchant Center"
  "google_ads;whoami_google_ads;dep;gog;Google Ads"
  # ── API Tokens (paste to save) ──
  "openai;whoami_openai;token;$CRED_DIR/.openai_token|sk-|https://platform.openai.com/api-keys;OpenAI"
  "anthropic;whoami_anthropic;token;$CRED_DIR/.anthropic_token|sk-ant-|https://console.anthropic.com/settings/keys;Anthropic"
  "gemini;whoami_gemini;token;$CRED_DIR/.gemini_token||https://aistudio.google.com/apikey;Google Gemini"
  "xai;whoami_xai;token;$CRED_DIR/.xai_token|xai-|https://console.x.ai;xAI / Grok"
  "perplexity;whoami_perplexity;token;$CRED_DIR/.perplexity_token|pplx-|https://www.perplexity.ai/settings/api;Perplexity"
  "meta;whoami_meta;token;$CRED_DIR/.meta_token|EAA|https://developers.facebook.com/tools/explorer;Meta / Facebook"
  "instagram;whoami_instagram;dep;meta;Instagram (via Meta token)"
  "whatsapp;whoami_whatsapp;dep;meta;WhatsApp Business (via Meta token)"
  "meta_pixel;whoami_meta_pixel;dep;meta;Meta Pixel / CAPI (via Meta token)"
  "mercadopago;whoami_mercadopago;token;$CRED_DIR/.mercadopago_token||https://www.mercadopago.com/developers;MercadoPago"
  "mercadolibre;whoami_mercadolibre;token;$CRED_DIR/.mercadolibre.json||https://developers.mercadolibre.com.ar/devcenter;MercadoLibre (OAuth — 6h token + refresh)"
  "telegram;whoami_telegram;token;$CRED_DIR/.telegram_bot_token||@BotFather on Telegram;Telegram Bot"
  "brave;whoami_brave;token;$CRED_DIR/.brave_token||https://brave.com/search/api;Brave Search"
  "manychat;whoami_manychat;token;$CRED_DIR/.manychat_token||https://manychat.com/settings/api;ManyChat"
  "zoom;whoami_zoom;zoom;_;Zoom (S2S OAuth)"
  "notion;whoami_notion;cli;notion auth login;Notion CLI"
)

# ── Parse args ──
ONLY=""
LIST=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --only) ONLY="$2"; shift 2 ;;
    --list) LIST=true; shift ;;
    *) shift ;;
  esac
done

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}  🔑 Auth Status & Wizard${RESET}"
echo -e "${DIM}  Credential dir: ${CRED_DIR}${RESET}"
echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
echo ""

declare -a need_auth_entries=()
ok_count=0
missing_count=0
need_count=0
current_section=""

for entry in "${ENTRIES[@]}"; do
  IFS=';' read -r name whoami_fn auth_type auth_detail desc <<< "$entry"

  if [[ -n "$ONLY" && "$name" != "$ONLY" ]]; then
    continue
  fi

  # Section headers
  case "$name" in
    gh)         [[ "$current_section" != "cli" ]] && { echo -e "  ${CYAN}Platform CLIs${RESET}"; current_section="cli"; } ;;
    twilio)     [[ "$current_section" != "api-cli" ]] && { echo ""; echo -e "  ${CYAN}API CLIs${RESET}"; current_section="api-cli"; } ;;
    gog)        [[ "$current_section" != "google" ]] && { echo ""; echo -e "  ${CYAN}Google Suite${RESET}"; current_section="google"; } ;;
    openai)     [[ "$current_section" != "tokens" ]] && { echo ""; echo -e "  ${CYAN}API Tokens${RESET}"; current_section="tokens"; } ;;
  esac

  result=$($whoami_fn)
  status="${result%%|*}"
  identity="${result#*|}"

  case "$status" in
    ok)
      ((ok_count++))
      echo -e "  ✅ ${BOLD}${name}${RESET} — ${identity}"
      ;;
    need_auth)
      ((need_count++))
      need_auth_entries+=("$entry")
      echo -e "  ❌ ${BOLD}${name}${RESET} — ${RED}${identity}${RESET}"
      ;;
    missing)
      ((missing_count++))
      echo -e "  ${DIM}⏭  ${name} — ${identity}${RESET}"
      ;;
  esac
done

echo ""
echo -e "  ✅ ${ok_count} connected  ❌ ${need_count} need auth  ⏭  ${missing_count} not installed"

if $LIST; then
  echo ""
  exit 0
fi

echo ""

if [[ ${#need_auth_entries[@]} -eq 0 ]]; then
  echo -e "  ${GREEN}${BOLD}All services connected! 🎉${RESET}"
  echo ""
  exit 0
fi

echo -e "  ${BOLD}Authenticate ${#need_auth_entries[@]} service(s)?${RESET}"
echo ""

for entry in "${need_auth_entries[@]}"; do
  IFS=';' read -r name whoami_fn auth_type auth_detail desc <<< "$entry"

  echo -e "  ${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo -e "  ${BOLD}${name}${RESET} — ${desc}"

  case "$auth_type" in
    cli)
      echo -e "  ${DIM}\$ ${auth_detail}${RESET}"
      echo ""
      read -p "  Press Enter to authenticate (or 's' to skip): " choice
      echo ""
      if [[ "$choice" == "s" || "$choice" == "S" ]]; then
        echo -e "  ${YELLOW}Skipped${RESET}"
      else
        eval "$auth_detail" || true
        echo ""
        result=$($whoami_fn)
        local_status="${result%%|*}"
        local_id="${result#*|}"
        [[ "$local_status" == "ok" ]] && echo -e "  ✅ ${GREEN}${name}${RESET} — ${local_id}" || echo -e "  ${YELLOW}⚠  ${name}${RESET} — ${local_id}"
      fi
      ;;
    token)
      IFS='|' read -r file prefix url <<< "$auth_detail"
      echo ""
      if _prompt_token "$name" "$file" "$prefix" "$url"; then
        echo ""
        result=$($whoami_fn)
        local_status="${result%%|*}"
        local_id="${result#*|}"
        [[ "$local_status" == "ok" ]] && echo -e "  ✅ ${GREEN}${name}${RESET} — ${local_id}" || echo -e "  ${YELLOW}⚠  ${name}${RESET} — ${local_id}"
      fi
      ;;
    gog)
      # Check if credentials are loaded
      local has_creds; has_creds=$(gog auth credentials list --json 2>&1 | grep -c "client" 2>/dev/null || echo "0")
      if [[ "$has_creds" -eq 0 ]]; then
        echo -e "  ${BOLD}Step 1:${RESET} Load OAuth client credentials"
        echo -e "  ${DIM}Get from: Google Cloud Console → APIs → Credentials → Desktop app${RESET}"
        echo ""
        read -p "  Path to client_secret.json (or 's' to skip): " cred_path
        if [[ "$cred_path" != "s" && "$cred_path" != "S" && -n "$cred_path" ]]; then
          gog auth credentials "$cred_path" || true
        else
          echo -e "  ${YELLOW}Skipped${RESET}"
          echo ""
          continue
        fi
        echo ""
      fi
      echo -e "  ${BOLD}Step 2:${RESET} Add Google account (with GA4 + GSC extra scopes)"
      echo -e "  ${DIM}Includes: gmail, calendar, drive, sheets, docs, contacts, tasks, GA4, GSC${RESET}"
      read -p "  Email address (or 's' to skip): " email
      if [[ "$email" != "s" && "$email" != "S" && -n "$email" ]]; then
        gog auth add "$email" --force-consent \
          --extra-scopes="https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/content,https://www.googleapis.com/auth/adwords" || true
        echo ""
        result=$($whoami_fn)
        local_status="${result%%|*}"
        local_id="${result#*|}"
        [[ "$local_status" == "ok" ]] && echo -e "  ✅ ${GREEN}${name}${RESET} — ${local_id}" || echo -e "  ${YELLOW}⚠  ${name}${RESET} — ${local_id}"
      else
        echo -e "  ${YELLOW}Skipped${RESET}"
      fi
      ;;
    zoom)
      echo -e "  ${DIM}Zoom uses Server-to-Server OAuth (3 credentials)${RESET}"
      echo -e "  ${DIM}Get from: https://marketplace.zoom.us → your app → App Credentials${RESET}"
      echo ""
      read -p "  Account ID (or 's' to skip): " z_acct
      [[ "$z_acct" == "s" || -z "$z_acct" ]] && { echo -e "  ${YELLOW}Skipped${RESET}"; echo ""; continue; }
      read -p "  Client ID: " z_cid
      read -p "  Client Secret: " z_csec
      _save_token "$CRED_DIR/.zoom_account_id" "$z_acct"
      _save_token "$CRED_DIR/.zoom_client_id" "$z_cid"
      _save_token "$CRED_DIR/.zoom_client_secret" "$z_csec"
      echo -e "  Saved 3 credentials to $CRED_DIR/.zoom_*"
      echo ""
      result=$($whoami_fn)
      local_status="${result%%|*}"
      local_id="${result#*|}"
      [[ "$local_status" == "ok" ]] && echo -e "  ✅ ${GREEN}${name}${RESET} — ${local_id}" || echo -e "  ${YELLOW}⚠  ${name}${RESET} — ${local_id}"
      ;;
    dep)
      echo -e "  ${DIM}Depends on: ${auth_detail} (authenticate that first)${RESET}"
      ;;
  esac
  echo ""
done

echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
echo -e "  Done! Run ${BOLD}python3 credentials/scripts/check_local.py${RESET} for full status."
echo ""
