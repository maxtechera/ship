#!/usr/bin/env python3
"""
Ship Engine — Core orchestration library.

This module provides helper functions for the Ship Engine skill.
The actual orchestration happens via Neo's agent sessions,
but this script handles:
- Linear issue creation (parent + sub-issues)
- State file management
- Stage transitions
- Status formatting
- Talent ticket management (NEO-225)

Usage from agent:
  python3 ship-engine/engine.py create "Idea Name" "description"
  python3 ship-engine/engine.py status [ticket-id]
  python3 ship-engine/engine.py advance <ticket-id> <stage>
  python3 ship-engine/engine.py list
  python3 ship-engine/engine.py kill <ticket-id> "reason"

Talent workflow (NEO-225):
  python3 ship-engine/engine.py talent-ticket <run_id> <stage> <type> "description" ["brief"] ["ai_placeholder"]
  python3 ship-engine/engine.py talent-swap <run_id> <talent_id> <artifact_url>
  python3 ship-engine/engine.py talent-list <run_id> [pending|resolved|all]
  python3 ship-engine/engine.py talent-status <run_id>
  python3 ship-engine/engine.py talent-types
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# Config
_linear_token_path = os.environ.get(
    "LINEAR_TOKEN_PATH",
    str(Path.home() / ".clawdbot" / ".linear_token"),
)
LINEAR_API_KEY = (
    os.environ.get("LINEAR_API_KEY")
    or (open(_linear_token_path).read().strip() if Path(_linear_token_path).exists() else "")
)
MAX_TEAM_ID ="8b52dbf9-7f6d-4bf[REDACTED_PHONE]d37bc"
FALLBACK_LINEAR_PROJECT_ID = "8f7657a9-9ad5-4c0c-9723-178b4d9fc80c"
SHIP_ENGINE_LABEL_ID = "9178d59d-f529-4cfc-bb75-8ad78c9074e7"
_SCRIPT_DIR = Path(__file__).parent
RUNS_DIR = Path(os.environ.get("SHIP_RUNS_DIR", str(_SCRIPT_DIR / "runs")))
ARCHIVE_DIR = Path(os.environ.get("SHIP_ARCHIVE_DIR", str(_SCRIPT_DIR / "archive")))

# MAX team state IDs
STATES = {
    "Backlog": "704b0463-5d02-4fdf-8c82-4395e8bd8a22",
    "Todo": "6bc169de-a[REDACTED_PHONE]a3282ff3e9e",
    "In Progress": "a826c361-c7f[REDACTED_PHONE]a1-e0139f983653",
    "In Review": "24fcf30f-4c94-43dd-[REDACTED_PHONE]a6",
    "Done": "04d5f9db-ac12-45b3-8f07-09f66500ce43",
    "Canceled": "337b84b5-817f-44ad-b008-6fb67e88b165",
}

STAGES = ["validate", "strategy", "awareness", "lead-capture", "nurture", "closing", "launch", "measure"]
STAGE_TITLES = {
    "validate": "Validate",
    "strategy": "Strategy",
    "awareness": "Awareness",
    "lead-capture": "Lead Capture",
    "nurture": "Nurture",
    "closing": "Closing",
    "launch": "Launch",
    "measure": "Measure",
}
# Stages that run concurrently after Strategy (4 parallel agents)
PARALLEL_STAGES = ["awareness", "lead-capture", "nurture", "closing"]

# Stages that require content approval before advancing
# (content-facing stages where human review is mandatory per Decision #16)
APPROVAL_GATED_STAGES = ["awareness", "lead-capture", "nurture", "closing", "launch"]

# --- Measure Feedback Loop ---

# Default thresholds per metric — agents can override per-run via state["custom_thresholds"].
# inverted=True means higher value is worse.
# fmt: "pct" = percentage display, "sec" = seconds display, "raw" = plain number
DEFAULT_METRIC_THRESHOLDS = {
    "landing_conversion": {"warn": 0.02, "critical": 0.01, "inverted": False, "fmt": "pct"},
    "email_open_rate":    {"warn": 0.20, "critical": 0.10, "inverted": False, "fmt": "pct"},
    "email_click_rate":   {"warn": 0.02, "critical": 0.01, "inverted": False, "fmt": "pct"},
    "signup_rate":        {"warn": 0.03, "critical": 0.01, "inverted": False, "fmt": "pct"},
    "trial_to_paid":      {"warn": 0.05, "critical": 0.02, "inverted": False, "fmt": "pct"},
    "bounce_rate":        {"warn": 0.70, "critical": 0.85, "inverted": True,  "fmt": "pct"},
    "page_load_time":     {"warn": 3.0,  "critical": 5.0,  "inverted": True,  "fmt": "sec"},
}

# Default metric-to-stage mapping — agents can override per-run via state["metric_ownership"].
DEFAULT_METRIC_TO_STAGE = {
    "landing_conversion": "awareness",
    "bounce_rate":        "awareness",
    "page_load_time":     "awareness",
    "email_open_rate":    "nurture",
    "email_click_rate":   "nurture",
    "signup_rate":        "lead-capture",
    "trial_to_paid":      "closing",
}


def _get_metric_thresholds(state):
    """Get metric thresholds: custom per-run overrides merged with defaults."""
    thresholds = dict(DEFAULT_METRIC_THRESHOLDS)
    custom = state.get("custom_thresholds", {})
    for metric, overrides in custom.items():
        if metric in thresholds:
            thresholds[metric] = {**thresholds[metric], **overrides}
        else:
            thresholds[metric] = overrides
    return thresholds


def _get_metric_to_stage(state):
    """Get metric-to-stage mapping: custom per-run overrides merged with defaults."""
    mapping = dict(DEFAULT_METRIC_TO_STAGE)
    mapping.update(state.get("metric_ownership", {}))
    return mapping


# Urgency presets for timeout rules (hours: reminder, escalation, auto-pause)
URGENCY_PRESETS = {
    "standard": (24, 48, 72),
    "fast":     (12, 24, 48),
    "urgent":   (6, 12, 24),
    "relaxed":  (48, 96, 168),
}

METRIC_LABELS = {
    "landing_conversion": "Landing Conversion Rate",
    "email_open_rate":    "Email Open Rate",
    "email_click_rate":   "Email Click Rate",
    "signup_rate":        "Signup Rate",
    "trial_to_paid":      "Trial → Paid Conversion",
    "bounce_rate":        "Bounce Rate",
    "page_load_time":     "Page Load Time",
}

METRIC_SUGGESTIONS = {
    "landing_conversion": "Common causes to investigate: hero copy relevance to ICP pain, CTA clarity and placement, page load performance, mobile experience gaps",
    "email_open_rate":    "Common causes to investigate: subject line relevance to recipient segment, send timing alignment with audience timezone, deliverability issues (SPF/DKIM/spam score)",
    "email_click_rate":   "Common causes to investigate: CTA copy and visual prominence, email length relative to content value, link placement and formatting, content-to-offer alignment",
    "signup_rate":        "Common causes to investigate: form complexity vs perceived value, offer stack clarity, social proof presence and placement, friction in signup flow",
    "trial_to_paid":      "Common causes to investigate: onboarding sequence effectiveness, time-to-value during trial, top objection not addressed, urgency mechanism clarity",
    "bounce_rate":        "Common causes to investigate: page load speed, hero message alignment with traffic source expectations, mobile responsiveness, above-fold content relevance",
    "page_load_time":     "Common causes to investigate: unoptimized images, missing CDN caching, render-blocking scripts, third-party script overhead",
}

def gql(query, variables=None, _caller=None):
    """Execute a GraphQL query against Linear API with exponential backoff."""
    import urllib.request
    import urllib.error
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                "https://api.linear.app/graphql",
                data=data,
                headers={
                    "Authorization": LINEAR_API_KEY,
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
            if "errors" in result:
                raise Exception(f"GraphQL Error: {result['errors']}")
            return result["data"]
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2 ** attempt)  # 1s, 2s
    if last_err:
        raise last_err
    raise RuntimeError("Linear GraphQL request failed")


def _log_error(state, func_name, error):
    """Log an error to the run state's errors array."""
    if "errors" not in state:
        state["errors"] = []
    state["errors"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "function": func_name,
        "error": str(error),
    })


def _create_linear_project_for_run(name: str, description: str, priority: int = 3) -> dict[str, str]:
    proj_name = f"Ship: {name}".strip()[:255]
    proj_desc = (description or "").strip()

    resp = gql(
        """
        mutation($input: ProjectCreateInput!) {
          projectCreate(input: $input) {
            success
            project { id name url }
          }
        }
        """,
        {
            "input": {
                "name": proj_name,
                "description": proj_desc,
                "content": proj_desc,
                "priority": int(priority),
                "teamIds": [MAX_TEAM_ID],
            }
        },
    )

    payload = (resp or {}).get("projectCreate") or {}
    if not payload.get("success") or not payload.get("project"):
        raise RuntimeError("Linear projectCreate failed")
    return payload["project"]


def _ensure_run_linear_project(state: dict[str, Any]) -> dict[str, Any]:
    linear = state.get("linear")
    if not isinstance(linear, dict):
        return state

    parent_id = linear.get("parentId")
    if not parent_id:
        return state

    existing = linear.get("projectId")
    if existing and existing != FALLBACK_LINEAR_PROJECT_ID:
        return state

    parent_project = None
    try:
        resp = gql(
            """
            query($id: String!) {
              issue(id: $id) {
                id
                project { id name url }
              }
            }
            """,
            {"id": parent_id},
        )
        parent_project = ((resp or {}).get("issue") or {}).get("project")
    except Exception as e:
        _log_error(state, "ensure_run_project.fetch_parent_project", e)

    desired = None
    if parent_project and parent_project.get("id") and parent_project.get("id") != FALLBACK_LINEAR_PROJECT_ID:
        desired = parent_project
    else:
        try:
            desired = _create_linear_project_for_run(state.get("name") or "", state.get("idea") or "", 3)
        except Exception as e:
            _log_error(state, "ensure_run_project.create_project", e)
            save_run(state)
            return state

    desired_id = (desired or {}).get("id")
    if not desired_id:
        save_run(state)
        return state

    issue_ids = []
    issue_ids.append(parent_id)
    for sub in (linear.get("subIssues") or {}).values():
        if isinstance(sub, dict) and sub.get("id"):
            issue_ids.append(sub["id"])

    seen = set()
    for issue_id in issue_ids:
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        try:
            gql(
                """
                mutation($id: String!, $input: IssueUpdateInput!) {
                  issueUpdate(id: $id, input: $input) {
                    success
                    issue { id }
                  }
                }
                """,
                {"id": issue_id, "input": {"projectId": desired_id}},
            )
        except Exception as e:
            _log_error(state, "ensure_run_project.issue_update", e)

    linear["projectId"] = desired_id
    linear["projectName"] = (desired or {}).get("name")
    linear["projectUrl"] = (desired or {}).get("url")
    state["linear"] = linear
    save_run(state)
    return state


# --- NEO-171: Quality Gates ---

# Default quality rubrics — outcome-based, not tool/count-specific.
# Agents can override per-run via state["quality_criteria"].
DEFAULT_QUALITY_RUBRICS = {
    "validate": {
        "checks": ["ICP document addresses demographics, psychographics, behaviors, and pain triggers",
                    "Pain evidence sourced from real threads/reviews (not assumptions)",
                    "Scoring complete with weighted recommendation",
                    "Voice of Customer bank populated with real quotes"],
        "required_outputs": ["validation_report", "icp"],
    },
    "strategy": {
        "checks": ["Ship plan covers positioning, pricing, and channel strategy",
                    "Success targets defined for post-launch measurement",
                    "Budget estimated and breakdown provided",
                    "Go-to-market summary connects all parallel agents"],
        "required_outputs": ["ship_plan"],
    },
    "awareness": {
        "checks": ["Awareness content addresses top ICP pains",
                    "Landing page deployed with problem-first messaging",
                    "SEO content targets validated pain keywords",
                    "All content uses VoC language from ICP"],
        "required_outputs": [],  # Flex — agent registers outputs as produced
    },
    "lead-capture": {
        "checks": ["Email capture mechanism live and tested",
                    "Offer stack communicates clear value proposition",
                    "Funnel tracking verified end-to-end",
                    "UTM links generated for all active channels"],
        "required_outputs": [],
    },
    "nurture": {
        "checks": ["Nurture sequence covers full buyer journey (welcome → value → proof → offer)",
                    "Automation trigger configured and tested",
                    "Test email verified for deliverability and rendering"],
        "required_outputs": [],
    },
    "closing": {
        "checks": ["Payment flow tested end-to-end",
                    "Pricing page deployed and mobile-verified",
                    "Top objections addressed with evidence-based responses",
                    "Post-purchase onboarding sequence active"],
        "required_outputs": [],
    },
    "launch": {
        "checks": ["All parallel stages complete", "Pre-launch checklist verified", "All URLs live and functional"],
        "required_outputs": ["launch_checklist"],
    },
    "measure": {
        "checks": ["Metrics collection configured for defined success targets",
                    "Post-launch report drafted with data-driven recommendation"],
        "required_outputs": ["post_launch_report"],
    },
}


def quality_gate(run_id, stage, output_path=None):
    """Evaluate quality gate for a stage. Returns (PASS|REVISE|FAIL, feedback).

    Uses custom quality criteria from state["quality_criteria"] if set by Strategy agent,
    falls back to DEFAULT_QUALITY_RUBRICS. Uses custom scoring weights from
    state["scoring_weights"] if set (for validate stage).
    """
    state = load_run(run_id)

    # Custom criteria override defaults
    custom_criteria = state.get("quality_criteria", {}).get(stage)
    if custom_criteria:
        rubric = custom_criteria
    else:
        rubric = DEFAULT_QUALITY_RUBRICS.get(stage, {"checks": [], "required_outputs": []})

    feedback = []
    missing_outputs = []

    # Check required outputs in state (flexible — checks both hardcoded and agent-added keys)
    for out_key in rubric.get("required_outputs", []):
        val = state.get("outputs", {}).get(out_key)
        if not val:
            missing_outputs.append(out_key)
            feedback.append(f"❌ Missing output: {out_key}")
        else:
            feedback.append(f"✅ Output present: {out_key}")

    # Check if output_path exists (deliverable file)
    if output_path and not Path(output_path).exists():
        feedback.append(f"❌ Deliverable file not found: {output_path}")
        missing_outputs.append(output_path)

    # Check run directory for stage artifacts
    run_dir = RUNS_DIR / run_id / stage
    if run_dir.exists():
        artifacts = list(run_dir.iterdir())
        feedback.append(f"📁 {len(artifacts)} artifact(s) in {stage}/ directory")
    else:
        feedback.append(f"⚠️ No {stage}/ artifact directory found")

    # Determine verdict
    if len(missing_outputs) == 0:
        verdict = "PASS"
    elif len(missing_outputs) <= len(rubric.get("required_outputs", [])) // 2:
        verdict = "REVISE"
    else:
        verdict = "FAIL"

    feedback_text = f"**Quality Gate: {STAGE_TITLES.get(stage, stage)}** → {verdict}\n\n" + "\n".join(feedback)
    for check in rubric.get("checks", []):
        feedback_text += f"\n📋 {check}"

    # Post result as Linear comment
    try:
        if stage in state.get("linear", {}).get("subIssues", {}):
            issue_id = state["linear"]["subIssues"][stage]["id"]
        else:
            issue_id = state["linear"]["parentId"]
        gql("""
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
        """, {"issueId": issue_id, "body": feedback_text})
    except Exception as e:
        _log_error(state, "quality_gate", e)
        save_run(state)

    return verdict, feedback_text


# --- NEO-176: Lesson Extraction ---

LEARNINGS_PATH = Path(os.environ.get("SHIP_LEARNINGS_PATH", str(_SCRIPT_DIR / "LEARNINGS.md")))


def extract_lessons(state, reason=None):
    """Extract structured lessons from a run and append to LEARNINGS.md."""
    now = datetime.now(timezone.utc)
    created = state.get("created", "unknown")
    product = state.get("name", "Unknown")
    ticket = state.get("ticket", "???")

    # Calculate time per stage (approximate from updated timestamps)
    quality_scores = {}
    for stage in STAGES:
        out_keys = DEFAULT_QUALITY_RUBRICS.get(stage, {}).get("required_outputs", [])
        filled = sum(1 for k in out_keys if state.get("outputs", {}).get(k))
        total = max(len(out_keys), 1)
        quality_scores[stage] = f"{filled}/{total}"

    errors = state.get("errors", [])
    decision = state.get("decision", reason or "N/A")
    budget = state.get("budget", {})

    entry = f"""
## Run: {product} ({now.strftime('%Y-%m-%d')})

**Ticket:** {ticket}
**Created:** {created[:10] if len(created) >= 10 else created}
**Final Stage:** {state.get('stage', 'unknown')}
**Decision:** {decision}

### Quality Scores
| Stage | Outputs Filled |
|-------|---------------|
"""
    for stage in STAGES:
        entry += f"| {STAGE_TITLES.get(stage, stage)} | {quality_scores[stage]} |\n"

    entry += f"""
### Budget
- Estimated: ${budget.get('estimated', 0)}
- Spent: ${budget.get('spent', 0)}

### Errors ({len(errors)} total)
"""
    if errors:
        for e in errors[-5:]:  # Last 5 errors
            entry += f"- [{e.get('timestamp', '?')[:16]}] {e.get('function', '?')}: {e.get('error', '?')[:100]}\n"
    else:
        entry += "- None recorded\n"

    entry += """
### What Worked
- (To be filled by review)

### What Didn't
- (To be filled by review)

---
"""
    # Append to LEARNINGS.md
    if LEARNINGS_PATH.exists():
        existing = LEARNINGS_PATH.read_text()
    else:
        existing = "# Ship Engine — Learnings\n\nLessons extracted from ship runs.\n\n---\n"
    LEARNINGS_PATH.write_text(existing + entry)
    return entry


# --- NEO-177: Approval Timeout ---

TELEGRAM_MAX_GROUP = "-[REDACTED_PHONE]"


def check_timeouts(run_id):
    """Check if a run in awaiting-* state has timed out. Returns action taken."""
    state = load_run(run_id)
    stage = state.get("stage", "")
    if not stage.startswith("awaiting"):
        return None

    awaiting_since = state.get("awaiting_since")
    if not awaiting_since:
        return None

    since = datetime.fromisoformat(awaiting_since)
    now = datetime.now(timezone.utc)
    elapsed = now - since
    hours = elapsed.total_seconds() / 3600
    product = state.get("name", run_id)

    # Use urgency preset from state, default to "standard"
    urgency = state.get("urgency", "standard")
    reminder_h, escalation_h, pause_h = URGENCY_PRESETS.get(urgency, URGENCY_PRESETS["standard"])

    if hours >= pause_h:
        state["stage"] = "paused"
        state["paused_from"] = stage
        save_run(state)
        return f"auto-paused ({hours:.0f}h) — {product} ({run_id})"
    elif hours >= escalation_h:
        return f"urgent-reminder ({hours:.0f}h) — {product} ({run_id}) awaiting approval"
    elif hours >= reminder_h:
        return f"reminder ({hours:.0f}h) — {product} ({run_id}) awaiting approval"
    return None


def check_all_timeouts():
    """Check all active runs for approval timeouts. Returns list of actions."""
    actions = []
    if not RUNS_DIR.exists():
        return actions
    for f in RUNS_DIR.glob("*.json"):
        state = json.loads(f.read_text())
        ticket = state.get("ticket", f.stem)
        result = check_timeouts(ticket)
        if result:
            actions.append(result)
    return actions


# --- NEO-232: 4-Wave Launch Orchestration ---

# Human-readable channel labels
WAVE_CHANNEL_LABELS = {
    "email": "Email (MailerLite)",
    "dm": "Direct Messages",
    "private_communities": "Private Slack/Discord",
    "reddit": "Reddit",
    "indiehackers": "IndieHackers",
    "discord": "Discord Servers",
    "twitter": "X/Twitter",
    "linkedin": "LinkedIn",
    "product_hunt": "Product Hunt",
    "tiktok": "TikTok",
    "instagram": "Instagram",
    "youtube_shorts": "YouTube Shorts",
    "email_list": "Launch Email Blast",
    "meta_ads": "Meta Ads",
    "blog": "Blog / SEO",
    "all": "All Platforms",
}

# 4-Wave launch cadence. day_offset is relative to L-Day (0 = launch day).
# Wave 3 has sub-waves for timezone coverage; Wave 4 has sub-waves for amplification days.
LAUNCH_WAVES = {
    "wave1": {
        "number": 1,
        "name": "Inner Circle",
        "day_offset": -7,
        "utc_hour": 12,
        "description": (
            "Warm up your most engaged supporters. Get early feedback. "
            "Build momentum before public launch."
        ),
        "channels": ["email", "dm", "private_communities"],
        "actions": [
            {
                "id": "personal_outreach_supporters",
                "channel": "dm",
                "description": (
                    "Personal outreach to top supporters — invite early access for honest feedback. "
                    "Use supporter list from launch checklist, segment by relationship depth."
                ),
            },
            {
                "id": "email_inner_circle",
                "channel": "email",
                "description": (
                    "Email inner circle subscribers — exclusive early access, 1-week head start. "
                    "Subject: 'Early access before the public launch.'"
                ),
            },
            {
                "id": "share_private_communities",
                "channel": "private_communities",
                "description": (
                    "Share in trusted private Slack/Discord groups — ask for honest feedback. "
                    "Trusted communities only, not asking for upvotes."
                ),
            },
            {
                "id": "gather_testimonials",
                "channel": "dm",
                "description": (
                    "Screenshot reactions and save positive quotes for social proof. "
                    "Store in runs/{run_id}/launch/testimonials.md"
                ),
            },
        ],
        "messaging_angle": "I want your honest feedback before the world sees it.",
        "success_metrics": {
            "early_access_users": 20,
            "feedback_messages": 10,
            "testimonials": 5,
        },
        "blackboard_key": "launch.wave1",
    },
    "wave2": {
        "number": 2,
        "name": "Community",
        "day_offset": -3,
        "utc_hour": 14,
        "description": (
            "Build anticipation in relevant communities. "
            "Seed the product with helpful members who will organically spread it."
        ),
        "channels": ["reddit", "indiehackers", "discord", "twitter", "linkedin"],
        "actions": [
            {
                "id": "reddit_teaser",
                "channel": "reddit",
                "description": (
                    "Teaser post — 'Building something for {pain}' (no product pitch yet). "
                    "Value-first framing only."
                ),
            },
            {
                "id": "indiehackers_build_log",
                "channel": "indiehackers",
                "description": (
                    "Build log update: journey post — what you built, what you learned, what's coming."
                ),
            },
            {
                "id": "discord_community",
                "channel": "discord",
                "description": (
                    "Value-first post in relevant servers — follow each server's rules exactly."
                ),
            },
            {
                "id": "twitter_teaser_thread",
                "channel": "twitter",
                "description": (
                    "Problem-focused thread: the pain, the research, what you found. "
                    "No product reveal yet."
                ),
            },
            {
                "id": "linkedin_build_in_public",
                "channel": "linkedin",
                "description": (
                    "Professional angle — what the market is missing. Storytelling format."
                ),
            },
        ],
        "messaging_angle": (
            "The problem is bigger than I thought — here's what the research showed."
        ),
        "success_metrics": {
            "reddit_upvotes": 20,
            "ih_views": 100,
            "community_engagement": 10,
        },
        "blackboard_key": "launch.wave2",
    },
    "wave3": {
        "number": 3,
        "name": "Public Launch",
        "day_offset": 0,
        "utc_hour": 7,  # 12:01 AM PT ≈ 07:01 UTC (schedules pre-wave cron at this hour)
        "description": (
            "Maximum coordinated distribution across all platforms in synchronized timezone waves."
        ),
        "channels": [
            "product_hunt", "indiehackers", "email_list",
            "reddit", "twitter", "linkedin",
            "tiktok", "instagram", "discord",
        ],
        # Sub-waves fire on L-Day at staggered UTC hours to hit timezone peaks
        "sub_waves": {
            "pre_wave": {
                "utc_hour": 7,
                "label": "Pre-Wave (12:01 AM PT)",
                "channels": ["product_hunt", "indiehackers", "email"],
                "supporter_segment": "apac_eu",
                "actions": [
                    {
                        "id": "submit_product_hunt",
                        "channel": "product_hunt",
                        "description": (
                            "Self-hunt: tagline, description, screenshots, demo video, maker comment. "
                            "Submit at exactly 12:01 AM PT for full 24h window."
                        ),
                    },
                    {
                        "id": "notify_supporters_apac_eu",
                        "channel": "dm",
                        "description": (
                            "Notify APAC/EU supporters — personal message. "
                            "Do NOT ask for upvotes (PH guidelines)."
                        ),
                    },
                    {
                        "id": "post_indiehackers_shipped",
                        "channel": "indiehackers",
                        "description": (
                            "Shipped post: build story + metrics + lessons + link."
                        ),
                    },
                    {
                        "id": "activate_welcome_sequence",
                        "channel": "email",
                        "description": (
                            "Confirm welcome automation is live in MailerLite. "
                            "Trigger fires when subscriber joins group."
                        ),
                    },
                ],
            },
            "morning_wave": {
                "utc_hour": 15,
                "label": "Morning Wave (8–10 AM PT)",
                "channels": ["reddit", "email_list"],
                "supporter_segment": "us_east",
                "actions": [
                    {
                        "id": "post_reddit_launch",
                        "channel": "reddit",
                        "description": (
                            "3-5 subreddits, staggered 30-60 min apart, value-first framing."
                        ),
                    },
                    {
                        "id": "send_launch_email",
                        "channel": "email_list",
                        "description": (
                            "Launch email to full list — founding member access, clear CTA."
                        ),
                    },
                    {
                        "id": "notify_supporters_us_east",
                        "channel": "dm",
                        "description": (
                            "Personal outreach — US East timezone segment."
                        ),
                    },
                    {
                        "id": "update_ph_morning_metrics",
                        "channel": "product_hunt",
                        "description": (
                            "Post first-hours signup count as maker comment on PH post."
                        ),
                    },
                ],
            },
            "midday_wave": {
                "utc_hour": 19,
                "label": "Midday Wave (12–2 PM PT)",
                "channels": ["twitter", "linkedin"],
                "supporter_segment": "us_west",
                "actions": [
                    {
                        "id": "post_twitter_launch_thread",
                        "channel": "twitter",
                        "description": (
                            "5-7 tweet thread. Hook = pain, not product. Pin the thread after posting."
                        ),
                    },
                    {
                        "id": "post_linkedin_launch",
                        "channel": "linkedin",
                        "description": (
                            "Professional storytelling: problem → insight → solution → CTA."
                        ),
                    },
                    {
                        "id": "notify_supporters_us_west",
                        "channel": "dm",
                        "description": (
                            "Final timezone segment — personal outreach to US West contacts."
                        ),
                    },
                    {
                        "id": "cross_post_live_metrics",
                        "channel": "all",
                        "description": (
                            "Update PH + IH with live signup count for real-time social proof."
                        ),
                    },
                ],
            },
            "afternoon_wave": {
                "utc_hour": 23,
                "label": "Afternoon Wave (3–6 PM PT)",
                "channels": ["tiktok", "instagram", "discord"],
                "supporter_segment": None,
                "actions": [
                    {
                        "id": "publish_short_video",
                        "channel": "tiktok",
                        "description": (
                            "Publish to TikTok + IG Reels + YouTube Shorts simultaneously. "
                            "<60s. Problem → demo → result. No slow intros."
                        ),
                    },
                    {
                        "id": "publish_ig_carousel",
                        "channel": "instagram",
                        "description": (
                            "IG carousel via tools/lib/meta_api.py — no manual Instagram step."
                        ),
                    },
                    {
                        "id": "post_discord_communities",
                        "channel": "discord",
                        "description": (
                            "Post to Discord servers — follow each community's rules."
                        ),
                    },
                    {
                        "id": "activate_ads",
                        "channel": "meta_ads",
                        "description": (
                            "Activate Meta/Google ads if budget approved in Strategy stage. "
                            "Small daily spend, test creative first."
                        ),
                    },
                ],
            },
        },
        "messaging_angle": (
            "It's live. Here's what it does, here's the problem it solves, here's how to try it."
        ),
        "success_metrics": {
            "ph_ranking": 5,
            "signups": 50,
            "landing_conversion_pct": 15,
        },
        "blackboard_key": "launch.wave3",
    },
    "wave4": {
        "number": 4,
        "name": "Amplification",
        "day_offset": 3,
        "utc_hour": 10,
        "description": (
            "Capitalize on launch momentum. Activate signups. "
            "Turn early users into social proof for the next wave."
        ),
        "channels": ["all"],
        # Each sub-wave is a post-launch amplification beat
        "sub_waves": [
            {
                "day_offset": 1,
                "utc_hour": 10,
                "id": "d1_tutorial",
                "action": "Tutorial: 'How to get {result} in 5 min'",
                "channels": ["all"],
                "description": "Drive activation — publish tutorial across all platforms adapted per format.",
            },
            {
                "day_offset": 2,
                "utc_hour": 10,
                "id": "d2_bts",
                "action": "Behind-the-scenes: launch metrics + reactions",
                "channels": ["twitter", "indiehackers", "linkedin"],
                "description": "Build in public — share real GA4 screenshots + reaction screenshots.",
            },
            {
                "day_offset": 3,
                "utc_hour": 10,
                "id": "d3_social_proof",
                "action": "'What users are saying after 72 hours'",
                "channels": ["twitter", "reddit"],
                "description": "Post testimonials captured on L-Day as social proof thread.",
            },
            {
                "day_offset": 5,
                "utc_hour": 10,
                "id": "d5_community_push",
                "action": "Second community push — new subreddits or angles",
                "channels": ["reddit", "discord"],
                "description": "Target new audience segments not reached on L-Day.",
            },
            {
                "day_offset": 7,
                "utc_hour": 10,
                "id": "d7_lessons",
                "action": "PH update + 'What I learned launching'",
                "channels": ["product_hunt", "twitter", "indiehackers", "blog"],
                "description": "SEO + build-in-public — post lessons retrospective.",
            },
            {
                "day_offset": 10,
                "utc_hour": 10,
                "id": "d10_spotlight",
                "action": "User spotlight / case study",
                "channels": ["all"],
                "description": "Interview one early user — post across all platforms.",
            },
            {
                "day_offset": 14,
                "utc_hour": 10,
                "id": "d14_report",
                "action": "'Two weeks in — here's the data'",
                "channels": ["twitter", "indiehackers", "linkedin"],
                "description": "Transparent update — real retention and revenue data.",
            },
        ],
        "messaging_angle": "Here's what's happening. Real numbers, real users, real lessons.",
        "success_metrics": {
            "d3_activation_rate_pct": 50,
            "organic_mentions": 5,
            "week1_revenue": 0,
        },
        "blackboard_key": "launch.wave4",
    },
}

# Rollback trigger thresholds — automatically evaluated against state["metrics"]
ROLLBACK_TRIGGERS = {
    "crash_rate": {
        "threshold": 0.15,
        "operator": ">=",
        "description": "Product crashes for >15% of visitors (check GA4 error events)",
        "severity": "critical",
        "action": "pause_all_paid_and_notify",
    },
    "payment_failure_rate": {
        "threshold": 1.0,
        "operator": ">=",
        "description": "Payment flow broken (no successful checkouts, 100% failure rate)",
        "severity": "critical",
        "action": "pause_all_paid_and_notify",
    },
    "landing_conversion": {
        "threshold": 0.02,
        "operator": "<",
        "description": "Landing conversion below 2% (emergency floor threshold)",
        "severity": "critical",
        "action": "pause_paid_ads",
    },
    "ph_ranking": {
        "threshold": 20,
        "operator": ">",
        "description": "PH ranking below #20 after 4 hours — boost supporter engagement",
        "severity": "warning",
        "action": "notify_supporters_second_wave",
    },
}

# Human steps in the rollback runbook (posted to Linear on trigger)
ROLLBACK_STEPS = [
    "Post public acknowledgment immediately: 'We're experiencing issues — investigating now.'",
    "Notify Max via Telegram immediately",
    "Pause all ad spend (if running) — do not spend on broken traffic",
    "Revert deployment to last stable version (Railway/Vercel rollback)",
    "Pause Product Hunt if live — post honest update as maker comment",
    "Email list: 'We're pausing briefly to fix something — back in X hours.'",
    "Fix issue on staging first — verify fix before re-deploying",
    "Re-deploy and verify manually end-to-end before re-enabling traffic",
    "Post public update: 'Fixed. Here's what happened and what we changed.'",
    "Resume PH and re-notify supporters if timing allows",
]

# Timezone segments for supporter notification
SUPPORTER_SEGMENTS = {
    "apac_eu": {
        "label": "APAC + EU",
        "notify_utc_hour": 7,  # 12:01 AM PT = 5–6 PM their time
        "description": "Asia-Pacific and European supporters — notified at midnight PT",
    },
    "us_east": {
        "label": "US East",
        "notify_utc_hour": 15,  # 8 AM PT = 11 AM ET
        "description": "US Eastern timezone supporters — notified at 8 AM PT",
    },
    "us_west": {
        "label": "US West",
        "notify_utc_hour": 19,  # 12 PM PT
        "description": "US Western timezone supporters — notified at noon PT",
    },
    "all": {
        "label": "All Supporters",
        "notify_utc_hour": 12,
        "description": "All supporter segments combined",
    },
}


def schedule_launch_waves(
    run_id: str,
    launch_date_iso: str,
    run_mode: str = "production",
) -> dict[str, Any]:
    """Schedule cron jobs for all 4 launch waves based on L-Day date (NEO-232).

    Creates one-shot OpenClaw cron jobs for each wave and sub-wave, keyed to
    the exact UTC datetime derived from `launch_date_iso` + each wave's
    `day_offset` / `utc_hour`.

    Args:
        run_id:           Ship run ticket ID (e.g. "MAX-316")
        launch_date_iso:  ISO date for L-Day — "YYYY-MM-DD" or full ISO datetime
        run_mode:         "production" (registers cron jobs) or "dry_run" (plans only)

    Returns:
        Dict with keys: run_id, launch_date, schedule, cron_jobs, total_jobs
    """
    import subprocess

    state = load_run(run_id)

    # Normalise launch date to midnight UTC
    if "T" in launch_date_iso:
        launch_date = datetime.fromisoformat(launch_date_iso)
        if launch_date.tzinfo is None:
            launch_date = launch_date.replace(tzinfo=timezone.utc)
    else:
        launch_date = datetime.fromisoformat(f"{launch_date_iso}T00:00:00+00:00")

    schedule: dict[str, Any] = {}
    cron_jobs: dict[str, Any] = {}

    def _register_cron(job_name: str, wave_dt: datetime, message: str) -> dict[str, Any]:
        """Register a one-shot OpenClaw cron job. Returns status dict."""
        if run_mode != "production":
            return {"status": "dry_run", "would_fire_at": wave_dt.isoformat(), "message": message}
        # Only schedule future waves
        now = datetime.now(timezone.utc)
        if wave_dt <= now:
            return {"status": "skipped_past", "would_fire_at": wave_dt.isoformat()}
        try:
            result = subprocess.run(
                [
                    "openclaw", "cron", "add",
                    "--name", job_name,
                    "--at", wave_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "--message", message,
                    "--session", "isolated",
                    "--delete-after-run",
                    "--json",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return {
                        "status": "scheduled",
                        "job_id": data.get("id"),
                        "fires_at": wave_dt.isoformat(),
                    }
                except Exception:
                    return {"status": "scheduled", "fires_at": wave_dt.isoformat(), "raw": result.stdout.strip()}
            else:
                return {"status": "failed", "error": result.stderr.strip() or result.stdout.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "timeout"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Wave 1 ── Inner Circle (Day -7)
    w1 = LAUNCH_WAVES["wave1"]
    w1_dt = (launch_date + timedelta(days=w1["day_offset"])).replace(hour=w1["utc_hour"], minute=0, second=0)
    schedule["wave1"] = {
        "wave_name": f"Wave 1: {w1['name']}",
        "fires_at": w1_dt.isoformat(),
        "day_offset": w1["day_offset"],
        "channels": w1["channels"],
        "actions": [a["id"] for a in w1["actions"]],
    }
    cron_jobs["wave1"] = _register_cron(
        job_name=f"ship-engine:launch-wave1:{run_id}",
        wave_dt=w1_dt,
        message=(
            f"Ship Engine 4-Wave Launch — Wave 1 (Inner Circle) for run {run_id}.\n"
            f"Execute: python3 ship-engine/engine.py launch-wave {run_id} wave1\n"
            f"Actions: personal supporter outreach, inner-circle email, private community seeding, "
            f"testimonial gathering.\n"
            f"Messaging angle: \"{w1['messaging_angle']}\""
        ),
    )

    # ── Wave 2 ── Community (Day -3)
    w2 = LAUNCH_WAVES["wave2"]
    w2_dt = (launch_date + timedelta(days=w2["day_offset"])).replace(hour=w2["utc_hour"], minute=0, second=0)
    schedule["wave2"] = {
        "wave_name": f"Wave 2: {w2['name']}",
        "fires_at": w2_dt.isoformat(),
        "day_offset": w2["day_offset"],
        "channels": w2["channels"],
        "actions": [a["id"] for a in w2["actions"]],
    }
    cron_jobs["wave2"] = _register_cron(
        job_name=f"ship-engine:launch-wave2:{run_id}",
        wave_dt=w2_dt,
        message=(
            f"Ship Engine 4-Wave Launch — Wave 2 (Community) for run {run_id}.\n"
            f"Execute: python3 ship-engine/engine.py launch-wave {run_id} wave2\n"
            f"Actions: Reddit teaser, IndieHackers build log, Discord community posts, "
            f"X/Twitter teaser thread, LinkedIn build-in-public post.\n"
            f"Messaging angle: \"{w2['messaging_angle']}\""
        ),
    )

    # ── Wave 3 ── Public Launch sub-waves (Day 0, staggered UTC hours)
    w3 = LAUNCH_WAVES["wave3"]
    for sub_key, sub_wave in w3["sub_waves"].items():
        sw_dt = launch_date.replace(hour=sub_wave["utc_hour"], minute=1, second=0)
        full_key = f"wave3_{sub_key}"
        schedule[full_key] = {
            "wave_name": f"Wave 3: {sub_wave['label']}",
            "fires_at": sw_dt.isoformat(),
            "day_offset": 0,
            "channels": sub_wave["channels"],
            "supporter_segment": sub_wave.get("supporter_segment"),
            "actions": [a["id"] for a in sub_wave["actions"]],
        }
        supporter_note = (
            f" Notify segment: {sub_wave['supporter_segment']}."
            if sub_wave.get("supporter_segment") else ""
        )
        cron_jobs[full_key] = _register_cron(
            job_name=f"ship-engine:launch-wave3-{sub_key}:{run_id}",
            wave_dt=sw_dt,
            message=(
                f"Ship Engine 4-Wave Launch — Wave 3 {sub_wave['label']} for run {run_id}.\n"
                f"Execute: python3 ship-engine/engine.py "
                f"launch-wave {run_id} wave3_{sub_key}\n"
                f"Channels: {', '.join(sub_wave['channels'])}.{supporter_note}\n"
                f"Actions: {', '.join(a['id'] for a in sub_wave['actions'])}."
            ),
        )

    # ── Wave 4 ── Amplification sub-waves (Day +1 through +14)
    w4 = LAUNCH_WAVES["wave4"]
    for sw in w4["sub_waves"]:
        sw_dt = (launch_date + timedelta(days=sw["day_offset"])).replace(
            hour=sw["utc_hour"], minute=0, second=0
        )
        full_key = f"wave4_{sw['id']}"
        schedule[full_key] = {
            "wave_name": f"Wave 4: {sw['action']}",
            "fires_at": sw_dt.isoformat(),
            "day_offset": sw["day_offset"],
            "channels": sw["channels"],
            "action_description": sw["description"],
        }
        cron_jobs[full_key] = _register_cron(
            job_name=f"ship-engine:launch-{full_key}:{run_id}",
            wave_dt=sw_dt,
            message=(
                f"Ship Engine 4-Wave Launch — Wave 4 amplification for run {run_id} "
                f"(Day +{sw['day_offset']}).\n"
                f"Execute: python3 ship-engine/engine.py "
                f"launch-wave {run_id} {full_key}\n"
                f"Action: {sw['action']}\n"
                f"Channels: {', '.join(sw['channels'])}.\n"
                f"Description: {sw['description']}"
            ),
        )

    # Persist orchestration plan to run state
    state["launch_orchestration"] = {
        "launch_date": launch_date_iso,
        "run_mode": run_mode,
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        "schedule": schedule,
        "cron_jobs": {k: v for k, v in cron_jobs.items()},
        "waves_executed": {},
        "rollback_triggered": False,
        "rollback_reason": None,
    }
    save_run(state)

    # Post summary to Linear
    try:
        launch_sub = state["linear"]["subIssues"].get("launch", {})
        issue_id = launch_sub.get("id") or state["linear"]["parentId"]
        scheduled_count = sum(
            1 for v in cron_jobs.values()
            if v.get("status") in ("scheduled", "dry_run")
        )
        skipped_count = sum(
            1 for v in cron_jobs.values()
            if v.get("status") == "skipped_past"
        )
        failed_count = sum(
            1 for v in cron_jobs.values()
            if v.get("status") in ("failed", "error", "timeout")
        )
        # Build readable timeline (first 10 entries)
        timeline_rows = []
        for wk, ws in sorted(schedule.items(), key=lambda x: x[1]["fires_at"])[:10]:
            cj = cron_jobs.get(wk, {})
            status_icon = {"scheduled": "✅", "dry_run": "🔍", "skipped_past": "⏭", "failed": "❌"}.get(
                cj.get("status", ""), "⚠️"
            )
            timeline_rows.append(
                f"| {status_icon} | {ws['wave_name']} | {ws['fires_at'][:16]} UTC | "
                f"{', '.join(ws['channels'][:2])} |"
            )
        table = "\n".join(timeline_rows)
        comment_body = f"""### ⚡ 4-Wave Launch Orchestration — Scheduled

**Run:** {run_id} | **L-Day:** {launch_date_iso} | **Mode:** {run_mode}

**status_summary:** {scheduled_count} wave jobs scheduled"
 ({skipped_count} skipped past, {failed_count} failed)

**next_steps:**
- Monitor execution: `engine.py launch-status {run_id}`
- Check rollback triggers daily from Wave 3: `engine.py launch-check-triggers {run_id}`
- Notify supporters manually if needed: `engine.py launch-notify {run_id} <segment>`

#### Wave Timeline (first 10)
| Status | Wave | Fires At (UTC) | Channels |
|--------|------|---------------|----------|
{table}

#### Rollback Triggers Active
{chr(10).join(f'- **{k}**: {v["description"]} ({v["severity"]})' for k, v in ROLLBACK_TRIGGERS.items())}
"""
        gql(
            """
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
            """,
            {"issueId": issue_id, "body": comment_body},
        )
    except Exception as e:
        _log_error(state, "schedule_launch_waves.comment", e)
        save_run(state)

    return {
        "run_id": run_id,
        "launch_date": launch_date_iso,
        "schedule": schedule,
        "cron_jobs": cron_jobs,
        "total_jobs": len(schedule),
        "scheduled": sum(1 for v in cron_jobs.values() if v.get("status") in ("scheduled", "dry_run")),
    }


def execute_wave(run_id: str, wave_key: str) -> dict[str, Any]:
    """Mark a wave as executing and post a channel-specific action plan to Linear.

    Called by the cron-spawned agent at wave fire-time. Records start/completion
    timestamps and writes the action checklist to the blackboard.

    Args:
        run_id:   Ship run ticket ID
        wave_key: One of wave1, wave2, wave3_pre_wave, wave3_morning_wave, etc.

    Returns:
        Dict with wave definition, actions list, and execution record
    """
    state = load_run(run_id)
    now = datetime.now(timezone.utc).isoformat()

    # Resolve the wave definition
    wave_def = None
    sub_wave_def = None

    if wave_key in LAUNCH_WAVES:
        wave_def = LAUNCH_WAVES[wave_key]
        actions = wave_def.get("actions", [])
    elif wave_key.startswith("wave3_"):
        sub_key = wave_key[len("wave3_"):]
        wave_def = LAUNCH_WAVES["wave3"]
        sub_wave_def = wave_def["sub_waves"].get(sub_key)
        if not sub_wave_def:
            raise ValueError(f"Unknown Wave 3 sub-wave: {sub_key}")
        actions = sub_wave_def.get("actions", [])
    elif wave_key.startswith("wave4_"):
        sw_id = wave_key[len("wave4_"):]
        wave_def = LAUNCH_WAVES["wave4"]
        sub_wave_def = next(
            (sw for sw in wave_def["sub_waves"] if sw["id"] == sw_id), None
        )
        if not sub_wave_def:
            raise ValueError(f"Unknown Wave 4 sub-wave: {sw_id}")
        actions = [{"id": sub_wave_def["id"], "description": sub_wave_def["description"],
                    "channel": sub_wave_def["channels"][0]}]
    else:
        raise ValueError(f"Unknown wave_key: {wave_key}")

    wave_name = (
        sub_wave_def.get("label") or sub_wave_def.get("action") or wave_def["name"]
        if sub_wave_def else wave_def["name"]
    )
    channels = (
        sub_wave_def.get("channels", []) or wave_def.get("channels", [])
        if sub_wave_def else wave_def.get("channels", [])
    )

    # Write execution record to blackboard
    bb_key = (
        f"launch.{wave_key}" if not sub_wave_def
        else wave_def.get("blackboard_key", f"launch.{wave_key}")
    )
    execution_record = {
        "wave_key": wave_key,
        "wave_name": wave_name,
        "started_at": now,
        "completed_at": None,
        "actions": {a["id"]: "pending" for a in actions},
        "channels": channels,
        "supporter_segment": (sub_wave_def or {}).get("supporter_segment"),
    }

    orch = state.get("launch_orchestration", {})
    if "waves_executed" not in orch:
        orch["waves_executed"] = {}
    orch["waves_executed"][wave_key] = execution_record
    state["launch_orchestration"] = orch

    # Update blackboard
    if "blackboard" not in state:
        state["blackboard"] = {}
    state["blackboard"][bb_key] = execution_record
    save_run(state)

    # Build Linear comment — channel-specific action checklist
    action_rows = "\n".join(
        f"- [ ] **{a['id']}** ({WAVE_CHANNEL_LABELS.get(a.get('channel', ''), a.get('channel', ''))}): "
        f"{a['description']}"
        for a in actions
    )
    supporter_note = (
        f"\n**Supporter Segment:** {execution_record['supporter_segment']} — "
        f"notify via `engine.py launch-notify {run_id} {execution_record['supporter_segment']}`"
        if execution_record.get("supporter_segment") else ""
    )
    comment_body = f"""### 🚀 Launch Wave Executing: {wave_name}

**Run:** {run_id} | **Wave Key:** {wave_key} | **Started:** {now[:16]} UTC
**Channels:** {', '.join(WAVE_CHANNEL_LABELS.get(c, c) for c in channels)}{supporter_note}

#### Action Checklist
{action_rows}

**Messaging angle:** {(sub_wave_def or wave_def).get('messaging_angle', wave_def.get('messaging_angle', '—')) if not sub_wave_def else wave_def.get('messaging_angle', '—')}

> Reply-within-15-min rule active for all platforms from this wave onward.
"""

    try:
        launch_sub = state["linear"]["subIssues"].get("launch", {})
        issue_id = launch_sub.get("id") or state["linear"]["parentId"]
        gql(
            """
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
            """,
            {"issueId": issue_id, "body": comment_body},
        )
    except Exception as e:
        _log_error(state, "execute_wave.comment", e)
        save_run(state)

    return {
        "wave_key": wave_key,
        "wave_name": wave_name,
        "started_at": now,
        "actions": actions,
        "channels": channels,
    }


def complete_wave_action(run_id: str, wave_key: str, action_id: str, status: str = "done") -> dict[str, Any]:
    """Mark an individual wave action as complete (done/skipped/failed).

    Args:
        run_id:    Ship run ticket ID
        wave_key:  Wave identifier (e.g. "wave3_morning_wave")
        action_id: Action identifier within the wave
        status:    "done", "skipped", or "failed"

    Returns:
        Updated execution record for the wave
    """
    state = load_run(run_id)
    orch = state.get("launch_orchestration", {})
    record = orch.get("waves_executed", {}).get(wave_key)
    if not record:
        raise ValueError(f"Wave '{wave_key}' has not been started for run {run_id}. "
                         f"Call execute_wave first.")
    record["actions"][action_id] = status
    # Check if all actions are resolved
    all_resolved = all(v in ("done", "skipped", "failed") for v in record["actions"].values())
    if all_resolved and not record.get("completed_at"):
        record["completed_at"] = datetime.now(timezone.utc).isoformat()
    orch["waves_executed"][wave_key] = record
    state["launch_orchestration"] = orch
    # Mirror to blackboard
    bb_key = f"launch.{wave_key}"
    if "blackboard" not in state:
        state["blackboard"] = {}
    state["blackboard"][bb_key] = record
    save_run(state)
    return record


def notify_supporters(run_id: str, segment: str = "all") -> dict[str, Any]:
    """Post a supporter notification task to Linear for the given timezone segment.

    This does NOT send messages itself — it creates a Linear task reminding the
    operator to notify supporters personally (no template blasting, per launch rules).

    Args:
        run_id:  Ship run ticket ID
        segment: One of "apac_eu", "us_east", "us_west", "all"

    Returns:
        Dict with segment info and Linear issue created
    """
    state = load_run(run_id)
    seg = SUPPORTER_SEGMENTS.get(segment, SUPPORTER_SEGMENTS["all"])
    product = state.get("name", run_id)

    title = f"[Launch] Notify supporters — {seg['label']} — {product}"
    body = f"""## Supporter Notification Task

**Run:** {product} ({run_id})
**Segment:** {seg['label']}
**Scheduled notify time:** {seg['notify_utc_hour']:02d}:00 UTC

### Rules (mandatory)
- ❌ **Never explicitly ask for upvotes** — violates Product Hunt guidelines
- ✅ Every message must be **personal** — reference something specific about the recipient
- ✅ Send **before** L-Day, not on L-Day (people are busy on L-Day)
- ✅ Maximum 1 follow-up if no response

### Outreach Template (personalise every message — do not copy-paste)
**Pre-launch (Day -7):**
> "Hey [name] — I'm launching {product} next week. You've been following my work on [related topic]
> and I think you'd have a useful perspective. Would you want early access to take a look before
> the public launch?"

**L-Day:**
> "Hey [name] — {product} just went live. Would mean a lot to get your genuine reaction —
> no pressure to say anything nice if it's not your thing!"

### Segment Definition
{seg['description']}

### Action
1. Pull supporter list from `runs/{run_id}/launch/supporter-list.md`
2. Filter for `{segment}` timezone segment
3. Send personal message to each contact
4. Log responses in `runs/{run_id}/launch/supporter-responses.md`

*Auto-created by Ship Engine launch orchestration.*
"""
    # Create a Linear sub-task under the launch sub-issue
    try:
        launch_sub = state["linear"]["subIssues"].get("launch", {})
        parent_id = launch_sub.get("id") or state["linear"]["parentId"]
        issue = gql(
            """
            mutation($input: IssueCreateInput!) {
                issueCreate(input: $input) {
                    issue { id identifier title }
                }
            }
            """,
            {
                "input": {
                    "teamId": MAX_TEAM_ID,
                    "title": title,
                    "description": body,
                    "parentId": parent_id,
                    "projectId": state.get("linear", {}).get("projectId") or FALLBACK_LINEAR_PROJECT_ID,
                    "labelIds": [SHIP_ENGINE_LABEL_ID],
                    "priority": 2,
                    "stateId": STATES["Todo"],
                }
            },
        )
        created_issue = issue["issueCreate"]["issue"]
    except Exception as e:
        _log_error(state, "notify_supporters", e)
        save_run(state)
        created_issue = None

    return {
        "segment": segment,
        "segment_label": seg["label"],
        "product": product,
        "notify_utc_hour": seg["notify_utc_hour"],
        "linear_issue": created_issue,
    }


def check_rollback_triggers(run_id: str) -> dict[str, Any]:
    """Evaluate current run metrics against rollback trigger thresholds.

    Args:
        run_id: Ship run ticket ID

    Returns:
        Dict with triggered list, warning list, and overall verdict
    """
    state = load_run(run_id)
    metrics = state.get("metrics", {})

    triggered = []
    warnings = []

    for trigger_key, trigger in ROLLBACK_TRIGGERS.items():
        value = metrics.get(trigger_key)
        if value is None:
            continue  # Metric not recorded — skip

        threshold = trigger["threshold"]
        operator = trigger["operator"]

        breached = False
        if operator == ">=" and value >= threshold:
            breached = True
        elif operator == "<=" and value <= threshold:
            breached = True
        elif operator == ">" and value > threshold:
            breached = True
        elif operator == "<" and value < threshold:
            breached = True

        entry = {
            "trigger": trigger_key,
            "description": trigger["description"],
            "severity": trigger["severity"],
            "current_value": value,
            "threshold": threshold,
            "action": trigger["action"],
        }
        if breached:
            if trigger["severity"] == "critical":
                triggered.append(entry)
            else:
                warnings.append(entry)

    verdict = "STABLE"
    if triggered:
        verdict = "ROLLBACK"
    elif warnings:
        verdict = "ALERT"

    return {
        "run_id": run_id,
        "verdict": verdict,
        "triggered": triggered,
        "warnings": warnings,
        "metrics_checked": list(metrics.keys()),
    }


def rollback_launch(run_id: str, reason: str = "Manual rollback triggered") -> dict[str, Any]:
    """Execute the launch rollback procedure (NEO-232).

    Posts a Linear incident comment with the full rollback runbook,
    updates the run state to record the rollback event, and notifies
    via the run's blackboard so downstream agents can halt.

    Args:
        run_id: Ship run ticket ID
        reason: Human-readable reason for rollback

    Returns:
        Dict with rollback record
    """
    state = load_run(run_id)
    now = datetime.now(timezone.utc).isoformat()
    product = state.get("name", run_id)

    rollback_record = {
        "triggered_at": now,
        "reason": reason,
        "steps": {i: "pending" for i in range(len(ROLLBACK_STEPS))},
        "completed_at": None,
    }

    # Update orchestration state
    orch = state.get("launch_orchestration", {})
    orch["rollback_triggered"] = True
    orch["rollback_reason"] = reason
    orch["rollback_record"] = rollback_record
    state["launch_orchestration"] = orch

    # Write halt signal to blackboard
    if "blackboard" not in state:
        state["blackboard"] = {}
    state["blackboard"]["launch.rollback"] = {
        "active": True,
        "reason": reason,
        "triggered_at": now,
    }
    state["blackboard"]["launch.halt"] = True
    save_run(state)

    # Build runbook comment
    steps_text = "\n".join(
        f"{i + 1}. [ ] {step}"
        for i, step in enumerate(ROLLBACK_STEPS)
    )
    # Check which triggers fired
    trigger_check = check_rollback_triggers(run_id)
    triggered_text = (
        "\n".join(
            f"- 🔴 **{t['trigger']}**: {t['description']} "
            f"(current: {t['current_value']}, threshold: {t['threshold']})"
            for t in trigger_check.get("triggered", [])
        ) or "*(Manual rollback — no automated trigger fired)*"
    )

    comment_body = f"""## 🚨 LAUNCH ROLLBACK TRIGGERED — {product} ({run_id})

**Triggered at:** {now[:16]} UTC
**Reason:** {reason}

### Triggered Conditions
{triggered_text}

### Rollback Runbook
{steps_text}

### Key Contacts / Resources
- Hosting: Railway/Vercel dashboard
- Domain: Cloudflare/Namecheap dashboard
- Stripe: https://dashboard.stripe.com
- MailerLite: https://dashboard.mailerlite.com

**⚠️ All wave cron jobs should be considered paused until rollback is marked resolved.**
**Resume by updating `launch_orchestration.rollback_triggered = false` in run state.**

*Auto-generated by Ship Engine rollback procedure.*
"""

    try:
        launch_sub = state["linear"]["subIssues"].get("launch", {})
        issue_id = launch_sub.get("id") or state["linear"]["parentId"]

        # Set the launch sub-issue to In Review (blocked)
        if launch_sub.get("id"):
            gql(
                """
                mutation($id: String!, $stateId: String!) {
                    issueUpdate(id: $id, input: { stateId: $stateId }) {
                        issue { id }
                    }
                }
                """,
                {"id": launch_sub["id"], "stateId": STATES["In Review"]},
            )

        gql(
            """
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
            """,
            {"issueId": issue_id, "body": comment_body},
        )
    except Exception as e:
        _log_error(state, "rollback_launch.comment", e)
        save_run(state)

    return rollback_record


def launch_status(run_id: str) -> str:
    """Format wave execution status for display.

    Returns a markdown/text report showing which waves have fired, which are
    pending, and whether a rollback is active.
    """
    state = load_run(run_id)
    orch = state.get("launch_orchestration")

    if not orch:
        return (
            f"⚠️ No launch orchestration scheduled for {run_id}.\n"
            f"Run: engine.py launch-orchestrate {run_id} <YYYY-MM-DD>"
        )

    product = state.get("name", run_id)
    launch_date = orch.get("launch_date", "?")
    run_mode = orch.get("run_mode", "?")
    rollback_active = orch.get("rollback_triggered", False)
    waves_executed = orch.get("waves_executed", {})
    schedule = orch.get("schedule", {})
    cron_jobs = orch.get("cron_jobs", {})

    now = datetime.now(timezone.utc)
    lines = [
        f"⚡ **4-Wave Launch Status — {product}** ({run_id})",
        f"L-Day: **{launch_date}** | Mode: {run_mode}",
    ]
    if rollback_active:
        lines.append(f"🚨 **ROLLBACK ACTIVE** — {orch.get('rollback_reason', '?')}")
    lines.append("")

    # Group entries by wave
    wave_groups = [
        ("Wave 1: Inner Circle", ["wave1"]),
        ("Wave 2: Community", ["wave2"]),
        ("Wave 3: Public Launch", [
            "wave3_pre_wave", "wave3_morning_wave", "wave3_midday_wave", "wave3_afternoon_wave"
        ]),
        ("Wave 4: Amplification", [
            k for k in schedule.keys() if k.startswith("wave4_")
        ]),
    ]

    for group_name, keys in wave_groups:
        lines.append(f"**{group_name}**")
        for wk in keys:
            if wk not in schedule:
                continue
            ws = schedule[wk]
            cj = cron_jobs.get(wk, {})
            exec_rec = waves_executed.get(wk)
            fires_at = ws.get("fires_at", "?")

            if exec_rec:
                if exec_rec.get("completed_at"):
                    icon = "✅"
                    state_label = f"done @ {exec_rec['completed_at'][:16]} UTC"
                else:
                    icon = "🔄"
                    state_label = f"running since {exec_rec['started_at'][:16]} UTC"
            else:
                try:
                    fire_dt = datetime.fromisoformat(fires_at)
                    if fire_dt.tzinfo is None:
                        fire_dt = fire_dt.replace(tzinfo=timezone.utc)
                    if now > fire_dt:
                        icon = "⚠️"
                        state_label = f"MISSED — was due {fires_at[:16]} UTC"
                    else:
                        icon = "⬜"
                        delta = fire_dt - now
                        days = delta.days
                        hours = delta.seconds // 3600
                        state_label = f"scheduled {fires_at[:16]} UTC (in {days}d {hours}h)"
                except Exception:
                    icon = "⬜"
                    state_label = f"scheduled {fires_at[:16]}"

            cj_status = cj.get("status", "?")
            lines.append(f"  {icon} **{ws['wave_name']}** — {state_label} [{cj_status}]")
        lines.append("")

    return "\n".join(lines)


def _drive_api_token():
    """Get a fresh Google Drive API access token using stored OAuth refresh token."""
    import urllib.request, urllib.parse
    token_path = os.environ.get(
        "GOOGLE_ANALYTICS_TOKEN_PATH",
        str(Path.home() / ".clawdbot" / ".google_analytics_token.json"),
    )
    with open(token_path) as f:
        creds = json.load(f)
    data = urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data)
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp['access_token']


def _drive_api_post(url, token, body):
    """Make authenticated Drive API POST request."""
    import urllib.request
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    return json.loads(urllib.request.urlopen(req).read())


def _drive_api_get(url, token):
    """Make authenticated Drive API GET request."""
    import urllib.request
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    return json.loads(urllib.request.urlopen(req).read())


def create_drive_folders(run_id: str, product_name: str) -> dict[str, Any]:
    """Create Google Drive folder tree for a ship run.

    Structure:
        Ship Engine/{product_name}-{run_id}/
            01-Intake/
            02-Validate/
            03-Strategy/
            04-Awareness/
            05-Lead-Capture/
            06-Nurture/
            07-Closing/
            08-Launch/
            09-Measure/
            _prompts/

    Returns dict with root_folder_id and per-subfolder IDs.
    Raises on API error (caller should catch and log gracefully).
    """
    import urllib.parse

    token = _drive_api_token()

    # --- Find or create "Ship Engine" root folder ---
    q = urllib.parse.quote("name='Ship Engine' and mimeType='application/vnd.google-apps.folder' and trashed=false")
    search = _drive_api_get(
        f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id,name)&pageSize=1",
        token,
    )
    files = search.get("files", [])
    if files:
        ship_engine_folder_id = files[0]["id"]
    else:
        resp = _drive_api_post(
            "https://www.googleapis.com/drive/v3/files",
            token,
            {"name": "Ship Engine", "mimeType": "application/vnd.google-apps.folder"},
        )
        ship_engine_folder_id = resp["id"]

    # --- Create run root: {product_name}-{run_id} ---
    safe_name = product_name.replace("/", "-").strip()
    run_folder_name = f"{safe_name}-{run_id}"
    run_resp = _drive_api_post(
        "https://www.googleapis.com/drive/v3/files",
        token,
        {
            "name": run_folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [ship_engine_folder_id],
        },
    )
    root_folder_id = run_resp["id"]

    # --- Create only _prompts/ on init — agents create subfolders as needed via drive-mkdir ---
    folder_ids = {}
    sub_resp = _drive_api_post(
        "https://www.googleapis.com/drive/v3/files",
        token,
        {
            "name": "_prompts",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [root_folder_id],
        },
    )
    folder_ids["_prompts"] = sub_resp["id"]

    return {
        "root_folder_id": root_folder_id,
        "ship_engine_folder_id": ship_engine_folder_id,
        "folders": folder_ids,
    }


def create_drive_subfolder(run_id: str, folder_name: str) -> str:
    """Create a subfolder in a run's Drive folder on demand. Returns folder ID."""
    state = load_run(run_id)
    drive = state.get("drive")
    if not drive:
        raise ValueError(f"No Drive folders found for {run_id}. Run drive-init first.")
    token = _drive_api_token()
    resp = _drive_api_post(
        "https://www.googleapis.com/drive/v3/files",
        token,
        {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [drive["root_folder_id"]],
        },
    )
    folder_id = resp["id"]
    state["drive"]["folders"][folder_name] = folder_id
    save_run(state)
    return folder_id


def create_ship_run(name: str, description: str, priority: int = 3) -> dict[str, Any]:
    """Create a full ship run: parent issue + 7 sub-issues. Returns state dict."""
    now = datetime.now(timezone.utc).isoformat()

    run_project = None
    run_project_id = FALLBACK_LINEAR_PROJECT_ID
    try:
        run_project = _create_linear_project_for_run(name, description, priority)
        run_project_id = run_project.get("id") or run_project_id
    except Exception as e:
        run_project = None
        print(f"⚠️ Linear project creation failed (non-blocking): {e}")

    # Create parent issue
    parent = gql("""
        mutation($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                issue { id identifier title }
            }
        }
    """, {
        "input": {
            "teamId": MAX_TEAM_ID,
            "title": f"Ship: {name}",
            "description": description,
            "projectId": run_project_id,
            "labelIds": [SHIP_ENGINE_LABEL_ID],
            "priority": priority,
            "stateId": STATES["Backlog"],
        }
    })
    parent_issue = parent["issueCreate"]["issue"]

    # Create sub-issues for all 10 stages
    sub_issues = {}
    for stage in STAGES:
        sub = gql("""
            mutation($input: IssueCreateInput!) {
                issueCreate(input: $input) {
                    issue { id identifier title }
                }
            }
        """, {
            "input": {
                "teamId": MAX_TEAM_ID,
                "title": f"{STAGE_TITLES[stage]}: {name}",
                "parentId": parent_issue["id"],
                "projectId": run_project_id,
                "labelIds": [SHIP_ENGINE_LABEL_ID],
                "stateId": STATES["Backlog"],
            }
        })
        sub_issue = sub["issueCreate"]["issue"]
        sub_issues[stage] = {
            "id": sub_issue["id"],
            "identifier": sub_issue["identifier"],
        }

    # Build state file
    state = {
        "ticket": parent_issue["identifier"],
        "name": name,
        "idea": description,
        "stage": "intake",
        "created": now,
        "updated": now,
        "linear": {
            "projectId": run_project_id,
            "projectName": (run_project or {}).get("name"),
            "projectUrl": (run_project or {}).get("url"),
            "parentId": parent_issue["id"],
            "parentIdentifier": parent_issue["identifier"],
            "subIssues": sub_issues,
        },
        "approvals": {
            "validate": None,
            "pre-launch": None,
        },
        "budget": {
            # NEO-224: Budget Tracking & Enforcement
            # Strategy proposes; Max approves; warn at 80%; soft-block at 100% (override).
            "estimated": 0,       # Proposed total (USD) — set by Strategy stage
            "approved": None,     # Max-approved amount (USD); None = pending approval
            "approved_at": None,  # ISO timestamp of approval
            "spent": 0.0,         # Cumulative actual spend across all entries
            "currency": "USD",
            "per_stage": {},      # Stage-level budget breakdown from Strategy proposal
            "notes": "",          # Strategy notes for Max's review
            "entries": [],        # Line-item spend records (see budget_record_spend)
            "overrides": [],      # Audit log of soft-block overrides
            "status": "no_budget",  # no_budget|no_approval|ok|warn|soft_block|override
        },
        # Universal outputs — always expected. Agents add additional keys as they produce artifacts.
        # Schema validated against all 55 prompt templates (NEO-412):
        #   - Dead references removed: marketing_kit, outbound_playbook,
        #     outbound_session, marketing_session (SKILL.md-era, superseded by WORKFLOW.md)
        #   - Added: voc_bank, offer_stack, segment_lock, funnel_map, utm_links,
        #     lead_capture_wiring, awareness_landing_page_url, blog_post_urls,
        #     email_sequence_id, stripe_product_ids (required by prompt templates)
        "outputs": {
            # ── Validate stage ──────────────────────────────────────────────
            "validation_report": None,       # validate-scoring-rubric output
            "icp": None,                     # validate-icp-synthesis output (central artifact)
            "voc_bank": None,                # Voice-of-Customer quotes bank (fills voc-bank.md)
            # ── Strategy stage ──────────────────────────────────────────────
            "ship_plan": None,               # Full GTM strategy document
            "positioning": None,             # strategy-positioning output
            "offer_stack": None,             # lead-capture-offer-stack / strategy-pricing output
            "segment_lock": None,            # strategy-segment-lock output (primary ICP segment)
            # ── Awareness stage ─────────────────────────────────────────────
            "awareness_landing_page_url": None,  # Deployed landing page URL
            "blog_post_urls": None,          # List of published blog post URLs
            # ── Lead Capture stage ──────────────────────────────────────────
            "funnel_map": None,              # lead-capture-funnel-map output
            "utm_links": None,               # lead-capture-utm-generator output
            "lead_capture_wiring": None,     # Form/email group wiring docs (used by analytics-setup)
            "email_sequence_id": None,       # MailerLite automation/group ID for nurture sequence
            # ── Closing stage ───────────────────────────────────────────────
            "stripe_product_ids": None,      # Stripe product/price IDs (closing-stripe-setup output)
            # ── Launch / Measure stage ──────────────────────────────────────
            "launch_checklist": None,        # Pre-launch checklist with READY verdict
            "post_launch_report": None,      # Measure phase final verdict report
        },
        "delegations": {
            # Session IDs for parallel agents (awareness, lead-capture, nurture, closing)
            # Set when start_parallel() activates the 4 concurrent stages
            "awareness_session": None,
            "lead_capture_session": None,
            "nurture_session": None,
            "closing_session": None,
        },
        # Content Approval Queue (NEO-228)
        # Full queue data stored in runs/{ticket-id}/approval-queue.json
        # This section tracks summary stats and configuration
        "content_approval": {
            "enabled": True,                    # Can be disabled per-run for automated testing
            "gated_stages": APPROVAL_GATED_STAGES,
            "auto_approve_rules": {},           # {item_type: bool} — overrides defaults
            "total_pending": 0,
            "total_approved": 0,
            "total_rejected": 0,
        },
        "metrics_targets": {},
        "custom_thresholds": {},     # Agent-configurable metric thresholds (overrides defaults)
        "quality_criteria": {},      # Agent-defined quality gate criteria per stage
        "urgency": "standard",       # Timeout preset: standard|fast|urgent|relaxed
        "scoring_weights": None,     # Agent-proposed validation scoring weights (with justification)
        "metric_ownership": {},      # Agent-defined metric-to-stage mapping
        "decision": None,
        "errors": [],
        "blackboard": {},
        # Talent tickets (NEO-225): keyed by talent_id slug
        # Each entry: { talent_id, stage, deliverable_type, status, ai_placeholder_key,
        #               talent_artifact_url, linear_issue_id, linear_identifier, ... }
        "talent_tickets": {},
    }

    # Save state file
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    state_path = RUNS_DIR / f"{parent_issue['identifier']}.json"
    state_path.write_text(json.dumps(state, indent=2))

    # Create run output directory
    run_dir = RUNS_DIR / parent_issue["identifier"]
    run_dir.mkdir(exist_ok=True)

    # Create Google Drive folder tree (nice-to-have — don't block run on failure)
    try:
        drive = create_drive_folders(parent_issue["identifier"], name)
        state["drive"] = {
            "root_folder_id": drive["root_folder_id"],
            "folders": drive["folders"],
        }
        state_path.write_text(json.dumps(state, indent=2))
        print(f"📁 Drive folder created: https://drive.google.com/drive/folders/{drive['root_folder_id']}")
    except Exception as e:
        _log_error(state, "create_drive_folders", e)
        state_path.write_text(json.dumps(state, indent=2))
        print(f"⚠️ Drive folder creation failed (non-blocking): {e}")

    return state


def load_run(ticket_id: str) -> dict[str, Any]:
    """Load a ship run state file."""
    state_path = RUNS_DIR / f"{ticket_id}.json"
    if not state_path.exists():
        raise FileNotFoundError(f"No ship run found for {ticket_id}")
    state = json.loads(state_path.read_text())
    try:
        return _ensure_run_linear_project(state)
    except Exception as e:
        _log_error(state, "ensure_run_project", e)
        try:
            save_run(state)
        except Exception:
            pass
        return state


def save_run(state: dict[str, Any]):
    """Save a ship run state file."""
    state["updated"] = datetime.now(timezone.utc).isoformat()
    state_path = RUNS_DIR / f"{state['ticket']}.json"
    state_path.write_text(json.dumps(state, indent=2))


def advance_stage(ticket_id: str, to_stage: str, force: bool = False):
    """Advance a ship run to a new stage. Updates Linear + state file.

    If the current stage has pending content approvals and is approval-gated,
    the advance is blocked until approvals are resolved (unless force=True).
    """
    state = load_run(ticket_id)
    old_stage = state["stage"]

    # Content Approval Gate (NEO-228): block advance if pending approvals exist
    if not force and old_stage in APPROVAL_GATED_STAGES:
        try:
            from skills.ship_engine.approval_queue import is_stage_blocked
        except ImportError:
            try:
                sys.path.insert(0, str(Path(__file__).parent.parent.parent))
                from skills.ship_engine.approval_queue import is_stage_blocked
            except ImportError:
                is_stage_blocked = None

        if is_stage_blocked is None:
            # Try local import (same directory)
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    "approval_queue",
                    Path(__file__).parent / "approval_queue.py"
                )
                aq_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(aq_mod)
                is_stage_blocked = aq_mod.is_stage_blocked
            except Exception:
                is_stage_blocked = None

        if is_stage_blocked and is_stage_blocked(ticket_id, old_stage):
            print(
                f"⏳ Content Approval PENDING for stage '{old_stage}' in run {ticket_id}.\n"
                f"   Resolve all pending approvals before advancing.\n"
                f"   Use: python3 skills/ship-engine/approval_queue.py pending {ticket_id}\n"
                f"   Force override: engine.py advance {ticket_id} {to_stage} --force"
            )
            return state

    # Quality gate: check before advancing (skip for non-pipeline stages)
    if old_stage in DEFAULT_QUALITY_RUBRICS:
        verdict, feedback = quality_gate(ticket_id, old_stage)
        if verdict == "FAIL":
            print(f"❌ Quality gate FAILED for {old_stage}. Cannot advance.\n{feedback}")
            return state

    # Track awaiting_since for approval gates
    if to_stage.startswith("awaiting"):
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
    else:
        state.pop("awaiting_since", None)

    # Initialize blackboard when entering parallel state
    if to_stage == "parallel" or to_stage in PARALLEL_STAGES:
        if "blackboard" not in state:
            state["blackboard"] = {}

    # Extract lessons when reaching done
    if to_stage == "done":
        extract_lessons(state, state.get("decision"))

    # Mark old stage sub-issue as Done (if it's a real stage)
    if old_stage in state["linear"]["subIssues"]:
        sub = state["linear"]["subIssues"][old_stage]
        gql("""
            mutation($id: String!, $stateId: String!) {
                issueUpdate(id: $id, input: { stateId: $stateId }) {
                    issue { id }
                }
            }
        """, {"id": sub["id"], "stateId": STATES["Done"]})

    # Move new stage sub-issue to In Progress
    if to_stage in state["linear"]["subIssues"]:
        sub = state["linear"]["subIssues"][to_stage]
        gql("""
            mutation($id: String!, $stateId: String!) {
                issueUpdate(id: $id, input: { stateId: $stateId }) {
                    issue { id }
                }
            }
        """, {"id": sub["id"], "stateId": STATES["In Progress"]})

    # Update parent issue state based on stage
    parent_state = "In Progress"
    if to_stage == "validate":
        parent_state = "Todo"
    elif to_stage == "launch":
        parent_state = "In Review"

    gql("""
        mutation($id: String!, $stateId: String!) {
            issueUpdate(id: $id, input: { stateId: $stateId }) {
                issue { id }
            }
        }
    """, {"id": state["linear"]["parentId"], "stateId": STATES[parent_state]})

    state["stage"] = to_stage
    save_run(state)
    return state


def start_parallel(ticket_id: str, stages: list[str]):
    """Start multiple stages in parallel (e.g., build + marketing + content)."""
    state = load_run(ticket_id)
    for stage in stages:
        if stage in state["linear"]["subIssues"]:
            sub = state["linear"]["subIssues"][stage]
            gql("""
                mutation($id: String!, $stateId: String!) {
                    issueUpdate(id: $id, input: { stateId: $stateId }) {
                        issue { id }
                    }
                }
            """, {"id": sub["id"], "stateId": STATES["In Progress"]})
    state["stage"] = stages[0]  # Primary stage
    save_run(state)
    return state


def kill_run(ticket_id: str, reason: str):
    """Kill a ship run. Cancels all sub-issues and parent."""
    state = load_run(ticket_id)

    # Cancel all sub-issues
    for stage, sub in state["linear"]["subIssues"].items():
        try:
            gql("""
                mutation($id: String!, $stateId: String!) {
                    issueUpdate(id: $id, input: { stateId: $stateId }) {
                        issue { id }
                    }
                }
            """, {"id": sub["id"], "stateId": STATES["Canceled"]})
        except Exception:
            pass

    # Cancel parent
    gql("""
        mutation($id: String!, $stateId: String!) {
            issueUpdate(id: $id, input: { stateId: $stateId }) {
                issue { id }
            }
        }
    """, {"id": state["linear"]["parentId"], "stateId": STATES["Canceled"]})

    # Add kill reason as comment
    gql("""
        mutation($issueId: String!, $body: String!) {
            commentCreate(input: { issueId: $issueId, body: $body }) {
                comment { id }
            }
        }
    """, {"issueId": state["linear"]["parentId"], "body": f"🗑 **Killed:** {reason}"})

    state["decision"] = f"KILLED: {reason}"
    extract_lessons(state, reason)
    save_run(state)

    # Move to archive
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    src = RUNS_DIR / f"{ticket_id}.json"
    dst = ARCHIVE_DIR / f"{ticket_id}.json"
    src.rename(dst)

    # Move run dir too
    run_dir = RUNS_DIR / ticket_id
    if run_dir.exists():
        archive_run = ARCHIVE_DIR / ticket_id
        run_dir.rename(archive_run)

    return state


def list_runs() -> list[dict[str, Any]]:
    """List all active ship runs."""
    runs = []
    if not RUNS_DIR.exists():
        return runs
    for f in RUNS_DIR.glob("*.json"):
        try:
            ticket_id = f.stem
            state = load_run(ticket_id)
            updated = state.get("updated") or state.get("created") or ""
            runs.append({
                "ticket": state.get("ticket") or ticket_id,
                "name": state.get("name"),
                "stage": state.get("stage"),
                "updated": str(updated),
            })
        except Exception:
            continue
    return sorted(runs, key=lambda r: r["updated"], reverse=True)


def format_status(ticket_id=None) -> str:
    """Format status for Telegram display."""
    if ticket_id:
        state = load_run(ticket_id)
        stage_icons = {s: "⬜" for s in STAGES}
        current_found = False
        for s in STAGES:
            if s == state["stage"]:
                stage_icons[s] = "🔄"
                current_found = True
            elif not current_found:
                stage_icons[s] = "✅"

        lines = [f"⚡ **Ship: {state['name']}** ({state['ticket']})"]
        lines.append(f"Stage: **{state['stage'].title()}**")
        lines.append("")
        for s in STAGES:
            lines.append(f"{stage_icons[s]} {STAGE_TITLES[s]}")
        if state["decision"]:
            lines.append(f"\nVerdict: **{state['decision']}**")
        return "\n".join(lines)
    else:
        runs = list_runs()
        if not runs:
            return "No active ship runs. Drop an idea to start one! 🚀"
        lines = ["⚡ **Active Ship Runs:**\n"]
        for r in runs:
            lines.append(f"• **{r['name']}** ({r['ticket']}) — {r['stage'].title()}")
        return "\n".join(lines)


def add_comment(ticket_id: str, stage: str, body: str):
    """Add a comment to a stage's sub-issue."""
    state = load_run(ticket_id)
    if stage in state["linear"]["subIssues"]:
        issue_id = state["linear"]["subIssues"][stage]["id"]
    else:
        issue_id = state["linear"]["parentId"]

    gql("""
        mutation($issueId: String!, $body: String!) {
            commentCreate(input: { issueId: $issueId, body: $body }) {
                comment { id }
            }
        }
    """, {"issueId": issue_id, "body": body})


def _fmt_metric(value, fmt):
    """Format a metric value for display based on its type."""
    if fmt == "pct":
        return f"{value:.1%}"
    elif fmt == "sec":
        return f"{value:.1f}s"
    return str(value)


def _create_feedback_ticket(state, parent_id, metric_key, label, value, target, gap, stage, suggestion, priority=2):
    """Create a Linear sub-issue for a metric that's below threshold."""
    product = state.get("name", "Unknown")
    ticket_id = state.get("ticket", "???")
    thresh_cfg = DEFAULT_METRIC_THRESHOLDS.get(metric_key, {})
    fmt = thresh_cfg.get("fmt", "raw")

    priority_label = "🔴 P0 — Critical (KILL or PIVOT)" if priority == 1 else "🟡 P1 — Warning (ITERATE)"
    title = f"[Measure] {label} below target — {STAGE_TITLES.get(stage, stage)} needs attention"
    body = f"""## Metric Alert: {label}

**Run:** {product} ({ticket_id})
**Stage responsible:** {STAGE_TITLES.get(stage, stage)}
**Priority:** {priority_label}

| Metric | Value |
|--------|-------|
| Current | {_fmt_metric(value, fmt)} |
| Target (warn threshold) | {_fmt_metric(target, fmt)} |
| Gap to target | {_fmt_metric(abs(gap), fmt)} |

## Suggested Action
{suggestion}

## Context
This ticket was auto-created by the Ship Engine Measure feedback loop.
Address this before the next iteration cycle."""

    issue = gql("""
        mutation($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                issue { id identifier title }
            }
        }
    """, {
        "input": {
            "teamId": MAX_TEAM_ID,
            "title": title,
            "description": body,
            "parentId": parent_id,
            "projectId": (state.get("linear") or {}).get("projectId") or FALLBACK_LINEAR_PROJECT_ID,
            "labelIds": [SHIP_ENGINE_LABEL_ID],
            "priority": priority,
            "stateId": STATES["Todo"],
        }
    })
    return issue["issueCreate"]["issue"]


def measure_feedback(run_id: str) -> dict[str, Any]:
    """Analyze metrics and create feedback tickets for underperforming areas.

    Works with partial data — only evaluates metrics that have been recorded.
    Returns a summary dict with verdict, healthy/warning/critical lists, and ticket count.
    """
    state = load_run(run_id)
    metrics = state.get("metrics", {})

    if not metrics:
        return {
            "verdict": "NO_DATA",
            "healthy": [],
            "warning": [],
            "critical": [],
            "tickets_created": 0,
        }

    healthy = []
    warning = []
    critical = []
    tickets_created = 0

    # Parent ID for feedback sub-issues: prefer Measure sub-issue, fall back to parent
    measure_parent_id = (
        state["linear"]["subIssues"].get("measure", {}).get("id")
        or state["linear"]["parentId"]
    )

    thresholds = _get_metric_thresholds(state)
    metric_to_stage = _get_metric_to_stage(state)

    for metric_key, value in metrics.items():
        if metric_key not in thresholds:
            continue  # skip unknown metrics gracefully

        thresh = thresholds[metric_key]
        inverted = thresh.get("inverted", False)
        fmt = thresh.get("fmt", "raw")
        label = METRIC_LABELS.get(metric_key, metric_key)
        stage = metric_to_stage.get(metric_key, "unknown")
        suggestion = METRIC_SUGGESTIONS.get(metric_key, "Investigate and optimize")
        warn_thresh = thresh["warn"]
        crit_thresh = thresh["critical"]

        if inverted:
            # Higher value is worse (bounce_rate, page_load_time)
            if value >= crit_thresh:
                status = "critical"
                gap = value - warn_thresh
            elif value >= warn_thresh:
                status = "warning"
                gap = value - warn_thresh
            else:
                status = "healthy"
                gap = 0.0
        else:
            # Lower value is worse (all conversion rates)
            if value <= crit_thresh:
                status = "critical"
                gap = warn_thresh - value
            elif value <= warn_thresh:
                status = "warning"
                gap = warn_thresh - value
            else:
                status = "healthy"
                gap = 0.0

        entry = {
            "metric": metric_key,
            "label": label,
            "value": value,
            "target": warn_thresh,
            "gap": gap,
            "stage": stage,
            "fmt": fmt,
        }

        if status == "healthy":
            healthy.append(entry)
        elif status == "warning":
            warning.append(entry)
            try:
                _create_feedback_ticket(
                    state, measure_parent_id, metric_key, label,
                    value, warn_thresh, gap, stage, suggestion, priority=2,
                )
                tickets_created += 1
            except Exception as e:
                _log_error(state, "measure_feedback", f"P1 ticket for {metric_key}: {e}")
        elif status == "critical":
            critical.append(entry)
            try:
                _create_feedback_ticket(
                    state, measure_parent_id, metric_key, label,
                    value, warn_thresh, gap, stage, suggestion, priority=1,
                )
                tickets_created += 1
            except Exception as e:
                _log_error(state, "measure_feedback", f"P0 ticket for {metric_key}: {e}")

    # Verdict
    if critical:
        verdict = "KILL or PIVOT"
    elif warning:
        verdict = "ITERATE"
    else:
        verdict = "DOUBLE DOWN"

    # Persist feedback summary to state
    state["measure_feedback"] = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "healthy": [e["metric"] for e in healthy],
        "warning": [e["metric"] for e in warning],
        "critical": [e["metric"] for e in critical],
        "tickets_created": tickets_created,
    }
    save_run(state)

    return {
        "verdict": verdict,
        "healthy": healthy,
        "warning": warning,
        "critical": critical,
        "tickets_created": tickets_created,
    }


# ── NEO-224: Budget Tracking & Enforcement ────────────────────────────────────

BUDGET_WARN_PCT = 0.80   # 80% → warn
BUDGET_BLOCK_PCT = 1.00  # 100% → soft-block (override possible)

BUDGET_CATEGORIES = ["api", "ad_spend", "tooling", "domain", "other"]

BUDGET_STATUS_ICONS = {
    "no_budget": "⚪",
    "no_approval": "🔶",
    "ok": "✅",
    "warn": "⚠️",
    "soft_block": "🔴",
    "override": "🟠",
}


def _budget_pct(state: dict[str, Any]) -> float:
    """Return spent / approved as a float (0.0 if no approved budget)."""
    budget = state.get("budget", {})
    approved = budget.get("approved")
    spent = budget.get("spent", 0.0)
    if not approved or approved <= 0:
        return 0.0
    return spent / approved


def _budget_status_code(state: dict[str, Any]) -> str:
    """Compute the current budget status code."""
    budget = state.get("budget", {})
    if budget.get("approved") is None:
        proposed = budget.get("estimated", 0)
        return "no_budget" if proposed == 0 else "no_approval"
    pct = _budget_pct(state)
    # Check if currently in override mode
    overrides = budget.get("overrides", [])
    if overrides:
        last_override = overrides[-1]
        if last_override.get("active", False):
            return "override"
    if pct >= BUDGET_BLOCK_PCT:
        return "soft_block"
    if pct >= BUDGET_WARN_PCT:
        return "warn"
    return "ok"


def budget_propose(
    run_id: str,
    total_usd: float,
    per_stage: dict[str, float] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """
    Strategy stage records a proposed budget for Max's approval.
    Sets budget.estimated and budget.per_stage. Clears prior approval.

    Args:
        run_id:     Run ticket ID (e.g. MAX-316)
        total_usd:  Total estimated spend in USD
        per_stage:  Optional per-stage breakdown, e.g. {"awareness": 50.0, "ad_spend": 120.0}
        notes:      Free-form notes for Max's review
    """
    state = load_run(run_id)
    budget = state.setdefault("budget", {})
    budget["estimated"] = float(total_usd)
    budget["approved"] = None
    budget["approved_at"] = None
    budget["currency"] = "USD"
    budget["per_stage"] = per_stage or {}
    budget["notes"] = notes
    budget.setdefault("spent", 0.0)
    budget.setdefault("entries", [])
    budget.setdefault("overrides", [])
    budget["status"] = "no_approval"
    save_run(state)

    # Post Linear comment requesting Max approval
    ticket = state.get("ticket", run_id)
    per_stage_lines = ""
    if per_stage:
        per_stage_lines = "\n" + "\n".join(
            f"  - {stage}: ${amt:.2f}" for stage, amt in per_stage.items()
        )
    comment_body = (
        f"💰 **Budget Proposal — Approval Required**\n\n"
        f"strategy proposes: **${total_usd:.2f} USD**\n"
        f"{per_stage_lines}\n"
        f"{'Notes: ' + notes if notes else ''}\n\n"
        f"Thresholds: warn at 80%, soft-block at 100% (override available).\n"
        f"To approve: `engine.py budget approve {run_id} {total_usd}`"
    )
    try:
        gql(
            """
            mutation CreateComment($issueId: String!, $body: String!) {
              commentCreate(input: { issueId: $issueId, body: $body }) {
                success
              }
            }
            """,
            {"issueId": state["linear"]["parentId"], "body": comment_body},
            _caller="budget_propose",
        )
    except Exception:
        pass

    return {
        "run_id": run_id,
        "estimated": total_usd,
        "per_stage": per_stage or {},
        "status": "no_approval",
        "message": f"Budget of ${total_usd:.2f} proposed. Awaiting Max approval.",
    }


def budget_approve(run_id: str, approved_amount: float | None = None) -> dict[str, Any]:
    """
    Max approves the budget for a run.

    Args:
        run_id:           Run ticket ID
        approved_amount:  Approved amount in USD. Defaults to the proposed estimate.
    """
    state = load_run(run_id)
    budget = state.setdefault("budget", {})
    estimated = budget.get("estimated", 0.0)
    amount = float(approved_amount) if approved_amount is not None else estimated
    budget["approved"] = amount
    budget["approved_at"] = datetime.now(timezone.utc).isoformat()
    budget["status"] = "ok"
    save_run(state)

    # Post Linear confirmation
    ticket = state.get("ticket", run_id)
    comment_body = (
        f"✅ **Budget Approved — ${amount:.2f} USD**\n\n"
        f"Run is cleared to spend up to ${amount:.2f}.\n"
        f"Warnings trigger at ${amount * BUDGET_WARN_PCT:.2f} (80%). "
        f"Soft-block at ${amount * BUDGET_BLOCK_PCT:.2f} (100%)."
    )
    try:
        gql(
            """
            mutation CreateComment($issueId: String!, $body: String!) {
              commentCreate(input: { issueId: $issueId, body: $body }) {
                success
              }
            }
            """,
            {"issueId": state["linear"]["parentId"], "body": comment_body},
            _caller="budget_approve",
        )
    except Exception:
        pass

    return {
        "run_id": run_id,
        "approved": amount,
        "status": "ok",
        "message": f"Budget of ${amount:.2f} approved.",
    }


def budget_record_spend(
    run_id: str,
    amount: float,
    category: str,
    stage: str = "",
    description: str = "",
) -> dict[str, Any]:
    """
    Record actual spend for a run. Triggers warn/soft-block logic.

    Args:
        run_id:      Run ticket ID
        amount:      Amount spent in USD (positive)
        category:    One of: api, ad_spend, tooling, domain, other
        stage:       Ship Engine stage that incurred this cost
        description: Human-readable description (e.g. "OpenAI tokens for awareness copy")

    Returns dict with: status, pct, warn, soft_block, message
    """
    if amount <= 0:
        raise ValueError(f"Spend amount must be positive (got {amount})")
    if category not in BUDGET_CATEGORIES:
        raise ValueError(f"Unknown category '{category}'. Use: {', '.join(BUDGET_CATEGORIES)}")

    state = load_run(run_id)
    budget = state.setdefault("budget", {})
    budget.setdefault("entries", [])
    budget.setdefault("spent", 0.0)
    budget.setdefault("overrides", [])

    entry = {
        "id": f"spend-{int(time.time() * 1000)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "amount": float(amount),
        "category": category,
        "stage": stage,
        "description": description,
    }
    budget["entries"].append(entry)
    budget["spent"] = round(budget["spent"] + float(amount), 4)

    # Determine new status
    status_code = _budget_status_code(state)
    budget["status"] = status_code
    save_run(state)

    approved = budget.get("approved")
    spent = budget["spent"]
    pct = _budget_pct(state)

    result: dict[str, Any] = {
        "run_id": run_id,
        "entry_id": entry["id"],
        "amount": amount,
        "category": category,
        "total_spent": spent,
        "approved": approved,
        "pct": round(pct * 100, 1),
        "status": status_code,
        "warn": status_code in ("warn", "soft_block", "override"),
        "soft_block": status_code == "soft_block",
        "message": "",
    }

    # Post Linear comment on threshold crossings
    comment_body = None
    if status_code == "soft_block" and approved:
        result["message"] = (
            f"🔴 SOFT-BLOCK: Budget exhausted (${spent:.2f} / ${approved:.2f}, {pct*100:.0f}%). "
            f"Use 'budget override' to continue with Max acknowledgement."
        )
        comment_body = (
            f"🔴 **Budget Soft-Block — {run_id}**\n\n"
            f"Total spent: ${spent:.2f} / ${approved:.2f} ({pct*100:.0f}%)\n"
            f"Latest entry: {description or category} — ${amount:.2f}\n\n"
            f"The run is soft-blocked. To continue:\n"
            f"`engine.py budget override {run_id} \"<reason>\"`"
        )
    elif status_code == "warn" and approved:
        result["message"] = (
            f"⚠️  Budget warning: ${spent:.2f} / ${approved:.2f} ({pct*100:.0f}%). "
            f"Approaching limit."
        )
        comment_body = (
            f"⚠️  **Budget Warning — {run_id}**\n\n"
            f"Spent ${spent:.2f} of ${approved:.2f} ({pct*100:.0f}%). "
            f"80% threshold crossed.\n"
            f"Latest: {description or category} — ${amount:.2f}"
        )
    else:
        result["message"] = f"Recorded ${amount:.2f} ({category}). Total: ${spent:.2f}."

    if comment_body:
        try:
            gql(
                """
                mutation CreateComment($issueId: String!, $body: String!) {
                  commentCreate(input: { issueId: $issueId, body: $body }) {
                    success
                  }
                }
                """,
                {"issueId": state["linear"]["parentId"], "body": comment_body},
                _caller="budget_record_spend",
            )
        except Exception:
            pass

    return result


def budget_check(run_id: str) -> dict[str, Any]:
    """
    Return current budget status without mutating state.
    Used by stage agents before incurring costs.

    Returns dict with: status, pct, warn, soft_block, approved, spent, message
    """
    state = load_run(run_id)
    budget = state.get("budget", {})
    approved = budget.get("approved")
    spent = budget.get("spent", 0.0)
    pct = _budget_pct(state)
    status_code = _budget_status_code(state)

    messages = {
        "no_budget": "No budget proposed yet. Strategy stage must call budget_propose first.",
        "no_approval": f"Budget of ${budget.get('estimated', 0):.2f} proposed but not yet approved by Max.",
        "ok": f"Budget OK — ${spent:.2f} / ${approved or 0:.2f} ({pct*100:.0f}%).",
        "warn": f"⚠️ Budget warning — ${spent:.2f} / ${approved or 0:.2f} ({pct*100:.0f}%). Approaching limit.",
        "soft_block": f"🔴 Budget soft-block — ${spent:.2f} / ${approved or 0:.2f} ({pct*100:.0f}%). "
                      f"Override required to continue spending.",
        "override": f"🟠 Budget override active — ${spent:.2f} / ${approved or 0:.2f} ({pct*100:.0f}%). "
                    f"Spending continues with Max acknowledgement.",
    }

    return {
        "run_id": run_id,
        "status": status_code,
        "approved": approved,
        "spent": spent,
        "pct": round(pct * 100, 1),
        "warn": status_code in ("warn", "soft_block"),
        "soft_block": status_code == "soft_block",
        "can_spend": status_code in ("ok", "warn", "override", "no_budget", "no_approval"),
        "message": messages.get(status_code, ""),
    }


def budget_override(run_id: str, reason: str) -> dict[str, Any]:
    """
    Max explicitly acknowledges the budget overrun and allows the run to continue.
    Clears soft-block. Adds an override entry to the audit log.

    Args:
        run_id: Run ticket ID
        reason: Why spending is continuing past the limit
    """
    state = load_run(run_id)
    budget = state.setdefault("budget", {})
    approved = budget.get("approved", 0.0)
    spent = budget.get("spent", 0.0)
    pct = _budget_pct(state)

    override_entry = {
        "id": f"override-{int(time.time() * 1000)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "spent_at_override": spent,
        "approved_at_override": approved,
        "pct_at_override": round(pct * 100, 1),
        "active": True,
    }
    budget.setdefault("overrides", [])
    # Deactivate any prior overrides
    for o in budget["overrides"]:
        o["active"] = False
    budget["overrides"].append(override_entry)
    budget["status"] = "override"
    save_run(state)

    # Post Linear comment
    comment_body = (
        f"🟠 **Budget Override — {run_id}**\n\n"
        f"Spent: ${spent:.2f} / Approved: ${approved:.2f} ({pct*100:.0f}%)\n"
        f"Reason: {reason}\n\n"
        f"Run continues. All future spend will be logged."
    )
    try:
        gql(
            """
            mutation CreateComment($issueId: String!, $body: String!) {
              commentCreate(input: { issueId: $issueId, body: $body }) {
                success
              }
            }
            """,
            {"issueId": state["linear"]["parentId"], "body": comment_body},
            _caller="budget_override",
        )
    except Exception:
        pass

    return {
        "run_id": run_id,
        "override_id": override_entry["id"],
        "status": "override",
        "spent": spent,
        "approved": approved,
        "message": f"Override applied. Run continues at ${spent:.2f} ({pct*100:.0f}%). Reason: {reason}",
    }


def budget_status(run_id: str) -> str:
    """Return a formatted budget status block for display in Telegram or Linear comments."""
    state = load_run(run_id)
    budget = state.get("budget", {})
    approved = budget.get("approved")
    estimated = budget.get("estimated", 0.0)
    spent = budget.get("spent", 0.0)
    pct = _budget_pct(state)
    status_code = _budget_status_code(state)
    icon = BUDGET_STATUS_ICONS.get(status_code, "❓")
    entries = budget.get("entries", [])
    overrides = budget.get("overrides", [])
    per_stage = budget.get("per_stage", {})
    notes = budget.get("notes", "")
    approved_at = budget.get("approved_at", "")

    lines = [
        f"💰 Budget — {run_id}",
        "=" * 38,
        f"Status:   {icon} {status_code.upper().replace('_', ' ')}",
        f"Proposed: ${estimated:.2f} USD",
        f"Approved: {'${:.2f}'.format(approved) if approved else '(pending)'}",
    ]
    if approved_at:
        lines.append(f"Approved at: {approved_at[:10]}")
    lines.append(f"Spent:    ${spent:.2f} ({pct*100:.0f}%)")

    if approved:
        bar_len = 20
        filled = int(min(pct, 1.0) * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        lines.append(f"          [{bar}]")
        lines.append(f"          Warn at ${approved * BUDGET_WARN_PCT:.2f} | Block at ${approved * BUDGET_BLOCK_PCT:.2f}")

    if per_stage:
        lines.append("\nPer-Stage Estimates:")
        for stage, amt in per_stage.items():
            lines.append(f"  {stage}: ${amt:.2f}")

    if notes:
        lines.append(f"\nNotes: {notes}")

    if entries:
        lines.append(f"\nSpend Log ({len(entries)} entries):")
        for e in entries[-10:]:
            ts = e.get("timestamp", "")[:10]
            cat = e.get("category", "?")
            amt = e.get("amount", 0)
            desc = e.get("description", "") or e.get("stage", "")
            lines.append(f"  [{ts}] {cat:<10} ${amt:.2f}  {desc[:40]}")
        if len(entries) > 10:
            lines.append(f"  ... ({len(entries) - 10} more entries)")

    # Category breakdown
    if entries:
        by_cat: dict[str, float] = {}
        for e in entries:
            cat = e.get("category", "other")
            by_cat[cat] = by_cat.get(cat, 0.0) + e.get("amount", 0.0)
        lines.append("\nBy Category:")
        for cat, total in sorted(by_cat.items(), key=lambda x: -x[1]):
            lines.append(f"  {cat:<12} ${total:.2f}")

    if overrides:
        lines.append(f"\nOverrides ({len(overrides)}):")
        for o in overrides:
            ts = o.get("timestamp", "")[:10]
            reason = o.get("reason", "")
            active = " [ACTIVE]" if o.get("active") else ""
            lines.append(f"  [{ts}]{active} {reason[:60]}")

    return "\n".join(lines)



# --- NEO-186: Event-Driven Architecture ---

# Valid events and their descriptions
VALID_EVENTS = {
    "stage_complete": (
        "Current stage finished producing deliverables. "
        "Triggers quality gate, then advances to the next stage if gate passes."
    ),
    "approval_received": (
        "A human approval gate was resolved. "
        "Records who approved, what they approved, and unblocks the pipeline "
        "if the run is in an awaiting-approval state."
    ),
    "blocked": (
        "A stage is blocked and cannot proceed without external input. "
        "Records the block reason, sets awaiting_since, and posts a "
        "'Blocked by Max' comment to the Linear issue."
    ),
    "timeout": (
        "Manually trigger the timeout-check logic for this run. "
        "Evaluates elapsed time since awaiting_since and takes action "
        "(reminder / escalation / auto-pause) based on urgency preset."
    ),
}

# Stage advancement map — what stage comes after each stage
NEXT_STAGE_MAP: dict[str, "str | list[str]"] = {
    "intake":                       "validate",
    "validate":                     "awaiting-validate-approval",
    "awaiting-validate-approval":   "strategy",
    "strategy":                     PARALLEL_STAGES,   # fan-out: list means start_parallel
    "awareness":                    "launch",
    "lead-capture":                 "launch",
    "nurture":                      "launch",
    "closing":                      "launch",
    "launch":                       "awaiting-launch-approval",
    "awaiting-launch-approval":     "measure",
    "measure":                      "done",
}


def _log_event(state: dict, event_type: str, payload: dict, result: dict) -> None:
    """Append an event record to state['event_log']."""
    if "event_log" not in state:
        state["event_log"] = []
    state["event_log"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        "payload": payload or {},
        "result": result,
    })


def _resolve_issue_id(state: dict, stage: str | None = None) -> str:
    """Get the Linear issue ID for the current stage (sub-issue), or parent."""
    linear = state.get("linear", {})
    stage = stage or state.get("stage", "")
    sub_issues = linear.get("subIssues", {})
    if stage in sub_issues:
        return sub_issues[stage]["id"]
    return linear.get("parentId", "")


def _post_event_comment(state: dict, body: str, stage: str | None = None) -> bool:
    """Post a Linear comment on the current (or named) stage issue. Returns True on success."""
    try:
        issue_id = _resolve_issue_id(state, stage)
        if not issue_id:
            return False
        gql(
            """
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
            """,
            {"issueId": issue_id, "body": body},
        )
        return True
    except Exception as e:
        _log_error(state, "_post_event_comment", e)
        return False


def _handle_stage_complete(state: dict, payload: dict) -> dict:
    """Handle the 'stage_complete' event.

    Runs the quality gate for the current stage. If it PASSES, advances the run
    to the next stage (or starts parallel stages). If it FAILS, posts a FAIL
    comment and leaves the run in the current stage for agent intervention.

    Payload keys (all optional):
        output_path (str): Path to main deliverable file for gate check.
        notes (str):       Human notes to attach to the gate comment.
        force (bool):      Skip gate check and force advancement (default False).
    """
    run_id = state["ticket"]
    current_stage = state.get("stage", "")
    output_path = payload.get("output_path")
    notes = payload.get("notes", "")
    force = payload.get("force", False)

    result: dict = {
        "event": "stage_complete",
        "stage": current_stage,
        "verdict": None,
        "advanced_to": None,
        "error": None,
    }

    # Run quality gate (skip if forced or stage not in rubric)
    verdict = "PASS"
    gate_feedback = ""
    if not force and current_stage in DEFAULT_QUALITY_RUBRICS:
        try:
            verdict, gate_feedback = quality_gate(run_id, current_stage, output_path)
        except Exception as e:
            _log_error(state, "_handle_stage_complete.quality_gate", e)
            verdict = "PASS"  # Don't block on gate errors
            gate_feedback = f"Warning: Quality gate check failed (non-blocking): {e}"

    result["verdict"] = verdict

    if verdict == "FAIL" and not force:
        comment_body = (
            f"### Warning stage_complete --- Quality Gate FAILED: "
            f"{STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} | **Stage:** {current_stage}\n"
            f"**Status:** BLOCKED --- stage did not pass quality gate. Manual review required.\n\n"
            f"{gate_feedback}\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"**Next steps:**\n"
            f"- Review missing outputs above\n"
            f"- Produce required deliverables\n"
            f"- Re-emit `stage_complete` or use "
            f"`engine.py advance {run_id} <stage> --force`\n"
        )
        _post_event_comment(state, comment_body, current_stage)
        result["error"] = "Quality gate FAIL --- run not advanced"
        return result

    # Determine next stage
    next_stage_spec = NEXT_STAGE_MAP.get(current_stage)
    if next_stage_spec is None:
        comment_body = (
            f"### stage_complete --- {STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} | **Gate:** {verdict}\n"
            f"{gate_feedback}\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"No automatic next stage configured for '{current_stage}'. "
            f"Pipeline at terminal state.\n"
        )
        _post_event_comment(state, comment_body, current_stage)
        result["advanced_to"] = "terminal"
        return result

    if isinstance(next_stage_spec, list):
        try:
            start_parallel(run_id, next_stage_spec)
        except Exception as e:
            _log_error(state, "_handle_stage_complete.start_parallel", e)
            result["error"] = str(e)
            return result
        advanced_to = f"parallel({', '.join(next_stage_spec)})"
        comment_body = (
            f"### stage_complete to Parallel: "
            f"{STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} | **Gate:** {verdict}\n"
            f"{gate_feedback}\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"**Parallel stages activated:** "
            f"{', '.join(STAGE_TITLES.get(s, s) for s in next_stage_spec)}\n\n"
            f"**status_summary:** {current_stage} complete. Parallel execution started.\n"
            f"**next_steps:** Each parallel agent should work autonomously and "
            f"emit `stage_complete` when done.\n"
        )
    elif next_stage_spec.startswith("awaiting"):
        try:
            state["stage"] = next_stage_spec
            state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
            save_run(state)
        except Exception as e:
            _log_error(state, "_handle_stage_complete.set_awaiting", e)
            result["error"] = str(e)
            return result
        advanced_to = next_stage_spec
        gate_name = next_stage_spec.replace("awaiting-", "").replace("-approval", "")
        comment_body = (
            f"### stage_complete to Awaiting Approval: "
            f"{STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} | **Gate:** {verdict}\n"
            f"{gate_feedback}\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"Approval Required --- {gate_name} approval gate is now open.\n"
            f"Emit `approval_received` when Max approves to unblock the pipeline.\n\n"
            f"**status_summary:** {current_stage} complete. Awaiting {gate_name} approval.\n"
            f"**next_steps:** Max reviews deliverables and approves/rejects via "
            f"`engine.py event {run_id} approval_received`\n"
        )
    else:
        try:
            advance_stage(run_id, next_stage_spec, force=force)
        except Exception as e:
            _log_error(state, "_handle_stage_complete.advance_stage", e)
            result["error"] = str(e)
            return result
        advanced_to = next_stage_spec
        comment_body = (
            f"### stage_complete to {STAGE_TITLES.get(next_stage_spec, next_stage_spec)}: "
            f"{STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} | **Gate:** {verdict}\n"
            f"{gate_feedback}\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"Pipeline advanced to: **{STAGE_TITLES.get(next_stage_spec, next_stage_spec)}**\n\n"
            f"**status_summary:** {current_stage} complete. {next_stage_spec} is now active.\n"
            f"**next_steps:** {STAGE_TITLES.get(next_stage_spec, next_stage_spec)} "
            f"agent should begin work.\n"
        )

    _post_event_comment(state, comment_body, current_stage)
    result["advanced_to"] = advanced_to
    return result


def _handle_approval_received(state: dict, payload: dict) -> dict:
    """Handle the 'approval_received' event.

    Records the approval in state['approvals'] and unblocks the pipeline if
    the run is currently in an awaiting-*-approval stage.

    Payload keys:
        gate (str):     Which gate was approved. Defaults to current awaiting gate.
        approver (str): Who approved (default 'Max').
        notes (str):    Approval notes/conditions.
        verdict (str):  'approved' | 'rejected' (default 'approved').
    """
    run_id = state["ticket"]
    current_stage = state.get("stage", "")
    gate = payload.get("gate") or current_stage.replace("awaiting-", "").replace("-approval", "")
    approver = payload.get("approver", "Max")
    notes = payload.get("notes", "")
    verdict_str = payload.get("verdict", "approved").lower()
    now = datetime.now(timezone.utc).isoformat()

    result: dict = {
        "event": "approval_received",
        "gate": gate,
        "verdict": verdict_str,
        "advanced_to": None,
        "error": None,
    }

    # Record approval in state
    if "approvals" not in state:
        state["approvals"] = {}
    state["approvals"][gate] = {
        "verdict": verdict_str,
        "approver": approver,
        "notes": notes,
        "timestamp": now,
    }

    if verdict_str == "rejected":
        prev_stage = gate
        state["stage"] = prev_stage
        state.pop("awaiting_since", None)
        save_run(state)
        comment_body = (
            f"### approval_received REJECTED: {gate}\n\n"
            f"**Run:** {run_id} | **Gate:** {gate}\n"
            f"**Approver:** {approver} | **Verdict:** REJECTED\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"Approval rejected. Pipeline returned to "
            f"**{STAGE_TITLES.get(prev_stage, prev_stage)}** for revision.\n\n"
            f"**status_summary:** {gate} approval rejected by {approver}.\n"
            f"**next_steps:** Address rejection notes, re-produce deliverables, "
            f"and emit `stage_complete` again.\n"
        )
        _post_event_comment(state, comment_body, prev_stage)
        result["advanced_to"] = prev_stage
        return result

    # Approval: determine next stage
    expected_awaiting = f"awaiting-{gate}-approval"
    if current_stage == expected_awaiting or current_stage.startswith("awaiting"):
        next_stage_spec = NEXT_STAGE_MAP.get(current_stage) or NEXT_STAGE_MAP.get(expected_awaiting)
    else:
        next_stage_spec = NEXT_STAGE_MAP.get(expected_awaiting)

    state.pop("awaiting_since", None)

    if next_stage_spec is None:
        save_run(state)
        comment_body = (
            f"### approval_received Approved: {gate}\n\n"
            f"**Run:** {run_id} | **Approver:** {approver}\n"
            f"{('**Notes:** ' + notes) if notes else ''}\n\n"
            f"Approval recorded. No automatic pipeline advancement configured for gate '{gate}'.\n"
        )
        _post_event_comment(state, comment_body)
        result["advanced_to"] = "none"
        return result

    # Flush state before advancing so mutations persist even if advance_stage is stubbed
    save_run(state)

    if isinstance(next_stage_spec, list):
        try:
            start_parallel(run_id, next_stage_spec)
        except Exception as e:
            _log_error(state, "_handle_approval_received.start_parallel", e)
            result["error"] = str(e)
            return result
        advanced_to = f"parallel({', '.join(next_stage_spec)})"
    else:
        try:
            advance_stage(run_id, next_stage_spec, force=True)
        except Exception as e:
            _log_error(state, "_handle_approval_received.advance_stage", e)
            result["error"] = str(e)
            return result
        advanced_to = next_stage_spec

    comment_body = (
        f"### approval_received Approved: {gate}\n\n"
        f"**Run:** {run_id} | **Approver:** {approver}\n"
        f"{('**Notes:** ' + notes) if notes else ''}\n\n"
        f"Pipeline unblocked to **{advanced_to}**\n\n"
        f"**status_summary:** {gate} approved by {approver}. Pipeline resumed.\n"
        f"**next_steps:** {advanced_to} agent should begin work immediately.\n"
    )
    _post_event_comment(state, comment_body)
    result["advanced_to"] = advanced_to
    return result


def _handle_blocked(state: dict, payload: dict) -> dict:
    """Handle the 'blocked' event.

    Records the block reason in state and posts a 'Blocked by Max' comment.

    Payload keys:
        reason (str):    What is blocking the stage (required).
        stage (str):     Which stage is blocked (defaults to current stage).
        needs (str):     What Max needs to provide/decide to unblock.
        urgency (str):   Urgency preset: standard|fast|urgent|relaxed.
    """
    run_id = state["ticket"]
    current_stage = payload.get("stage") or state.get("stage", "")
    reason = payload.get("reason") or "No reason specified"
    needs = payload.get("needs", "")
    urgency = payload.get("urgency")
    now = datetime.now(timezone.utc).isoformat()

    result: dict = {
        "event": "blocked",
        "stage": current_stage,
        "reason": reason,
        "error": None,
    }

    state["stage"] = f"awaiting-{current_stage}" if not current_stage.startswith("awaiting") else current_stage
    state["awaiting_since"] = now
    if urgency and urgency in URGENCY_PRESETS:
        state["urgency"] = urgency

    if "blocks" not in state:
        state["blocks"] = []
    state["blocks"].append({
        "timestamp": now,
        "stage": current_stage,
        "reason": reason,
        "needs": needs,
    })

    # Try to set Linear issue state to "Blocked by Max"
    try:
        issue_id = _resolve_issue_id(state, current_stage)
        if issue_id:
            states_resp = gql(
                """
                query($teamId: String!) {
                    team(id: $teamId) {
                        states { nodes { id name } }
                    }
                }
                """,
                {"teamId": MAX_TEAM_ID},
            )
            team_states = (states_resp or {}).get("team", {}).get("states", {}).get("nodes", [])
            blocked_state = next(
                (s for s in team_states if s["name"].lower() == "blocked by max"), None
            )
            if blocked_state:
                gql(
                    """
                    mutation($id: String!, $stateId: String!) {
                        issueUpdate(id: $id, input: { stateId: $stateId }) {
                            issue { id }
                        }
                    }
                    """,
                    {"id": issue_id, "stateId": blocked_state["id"]},
                )
    except Exception as e:
        _log_error(state, "_handle_blocked.set_linear_state", e)

    save_run(state)

    urgency_label = state.get("urgency", "standard")
    reminder_h, escalation_h, pause_h = URGENCY_PRESETS.get(urgency_label, URGENCY_PRESETS["standard"])

    comment_body = (
        f"### blocked: {STAGE_TITLES.get(current_stage, current_stage)}\n\n"
        f"**Run:** {run_id} | **Stage:** {current_stage}\n"
        f"**Blocked at:** {now[:16]} UTC | **Urgency:** {urgency_label}\n\n"
        f"**Reason:** {reason}\n"
        f"{('**What is needed:** ' + needs) if needs else ''}\n\n"
        f"Timeout schedule ({urgency_label}):\n"
        f"- {reminder_h}h reminder ping\n"
        f"- {escalation_h}h escalation\n"
        f"- {pause_h}h auto-pause run\n\n"
        f"**status_summary:** {current_stage} blocked --- {reason}\n"
        f"**next_steps:** Max to resolve block and emit `approval_received` or "
        f"`engine.py event {run_id} approval_received`.\n"
    )
    _post_event_comment(state, comment_body, current_stage)
    return result


def _handle_timeout(state: dict, payload: dict) -> dict:
    """Handle the 'timeout' event.

    Evaluates elapsed time since awaiting_since and takes action based on urgency.

    Payload keys:
        force_action (str): Override action: 'reminder' | 'escalation' | 'pause'.
    """
    run_id = state["ticket"]
    force_action = payload.get("force_action")

    result: dict = {
        "event": "timeout",
        "run_id": run_id,
        "action_taken": None,
        "elapsed_hours": None,
        "error": None,
    }

    awaiting_since = state.get("awaiting_since")
    if not awaiting_since and not force_action:
        result["action_taken"] = "skipped"
        result["error"] = "Run is not in an awaiting state (awaiting_since not set)"
        return result

    now = datetime.now(timezone.utc)
    if awaiting_since:
        since_dt = datetime.fromisoformat(awaiting_since)
        if since_dt.tzinfo is None:
            since_dt = since_dt.replace(tzinfo=timezone.utc)
        hours = (now - since_dt).total_seconds() / 3600
    else:
        hours = 0.0
    result["elapsed_hours"] = round(hours, 1)

    urgency = state.get("urgency", "standard")
    reminder_h, escalation_h, pause_h = URGENCY_PRESETS.get(urgency, URGENCY_PRESETS["standard"])
    current_stage = state.get("stage", "unknown")
    product = state.get("name", run_id)

    if force_action:
        action = force_action
    elif hours >= pause_h:
        action = "pause"
    elif hours >= escalation_h:
        action = "escalation"
    elif hours >= reminder_h:
        action = "reminder"
    else:
        action = "no_action"
        result["action_taken"] = "no_action"
        result["message"] = f"Only {hours:.1f}h elapsed (reminder threshold: {reminder_h}h)"
        return result

    result["action_taken"] = action

    if action == "pause":
        state["paused_from"] = current_stage
        state["stage"] = "paused"
        save_run(state)
        comment_body = (
            f"### timeout AUTO-PAUSED: {STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} ({product}) | **Elapsed:** {hours:.1f}h "
            f"(pause threshold: {pause_h}h)\n\n"
            f"Run auto-paused after {hours:.1f}h without approval ({urgency} urgency).\n\n"
            f"**status_summary:** Run auto-paused at {current_stage}.\n"
            f"**next_steps:** Max to resume via `engine.py event {run_id} approval_received`.\n"
        )
    elif action == "escalation":
        comment_body = (
            f"### timeout ESCALATION: {STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} ({product}) | **Elapsed:** {hours:.1f}h "
            f"(escalation threshold: {escalation_h}h)\n\n"
            f"Urgent: This run has been waiting {hours:.1f}h. Auto-pause at {pause_h}h.\n\n"
            f"**status_summary:** Escalation at {current_stage} --- {hours:.1f}h waiting.\n"
            f"**next_steps:** Max to approve/unblock immediately.\n"
        )
    else:
        comment_body = (
            f"### timeout REMINDER: {STAGE_TITLES.get(current_stage, current_stage)}\n\n"
            f"**Run:** {run_id} ({product}) | **Elapsed:** {hours:.1f}h "
            f"(reminder threshold: {reminder_h}h)\n\n"
            f"Reminder: this run has been waiting {hours:.1f}h for approval.\n\n"
            f"**status_summary:** Reminder at {current_stage} --- {hours:.1f}h waiting.\n"
            f"**next_steps:** Approve/unblock when ready. Escalation at {escalation_h}h.\n"
        )

    _post_event_comment(state, comment_body, current_stage)
    if action != "no_action":
        save_run(state)

    return result


def dispatch_event(
    run_id: str,
    event_type: str,
    payload: dict | None = None,
) -> dict:
    """Dispatch an event to the Ship Engine for a given run.

    This is the main entry point for event-driven orchestration. It routes
    events to the appropriate handler, logs them in the run state, and
    returns a structured result dict.

    Args:
        run_id:     Ship run ticket ID (e.g. "MAX-316").
        event_type: One of: stage_complete, approval_received, blocked, timeout.
        payload:    Optional dict of event-specific parameters.

    Returns:
        Dict with at minimum: event, run_id, timestamp, and handler-specific fields.

    Raises:
        ValueError: If event_type is not recognized.
        FileNotFoundError: If the run state file does not exist.
    """
    if event_type not in VALID_EVENTS:
        raise ValueError(
            f"Unknown event type '{event_type}'. "
            f"Valid events: {', '.join(VALID_EVENTS.keys())}"
        )

    state = load_run(run_id)
    payload = payload or {}

    handlers = {
        "stage_complete":    _handle_stage_complete,
        "approval_received": _handle_approval_received,
        "blocked":           _handle_blocked,
        "timeout":           _handle_timeout,
    }

    result = handlers[event_type](state, payload)

    # Reload state after handler (handlers save internally; reload to get latest)
    try:
        state = load_run(run_id)
    except Exception:
        pass

    _log_event(state, event_type, payload, result)
    save_run(state)

    return {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **result,
    }


def revisit_stage_status(run_id: str) -> str:
    """Return a formatted status string for any active revisit request."""
    state = load_run(run_id)
    request = state.get("revisit_request")
    history = state.get("revisit_history", [])

    lines = [f"🔄 Stage Revisit Status — {run_id} (current: {state['stage']})"]

    if request and request.get("status") == "pending":
        lines.append(f"\n⏳ PENDING REQUEST:")
        lines.append(f"   Target: {request['target_stage']} (from: {request['from_stage']})")
        lines.append(f"   Reason: {request['reason']}")
        lines.append(f"   Risk: {request.get('risk_level', '?')} | Confidence: {request.get('confidence', 0):.0%}")
        lines.append(f"   Requested: {request['requested_at'][:16]} UTC")
        url = request.get("decision_comment_url", "")
        if url:
            lines.append(f"   Decision comment: {url}")
        lines.append(f"\n   Awaiting Max decision: decision: approve|reject")
    elif not request:
        lines.append("\n✅ No pending revisit request.")

    if history:
        lines.append(f"\n📋 Revisit History ({len(history)} entries):")
        for i, h in enumerate(history[-5:], 1):  # show last 5
            icon = "✅" if h.get("status") == "approved" else "❌"
            lines.append(
                f"   {icon} [{h.get('executed_at', '?')[:10]}] "
                f"{h.get('from_stage', '?')} → {h.get('target_stage', '?')} "
                f"({h.get('status', '?')})"
            )

    versions = state.get("artifact_versions", {})
    if versions:
        lines.append(f"\n📦 Versioned Artifacts:")
        for stage, v_list in versions.items():
            lines.append(f"   {stage}: {len(v_list)} version(s) archived")

    return "\n".join(lines)


# ── End NEO-226: Stage Revisit / Rollback Mechanism ──────────────────────────


# ── NEO-225: Talent Ticket System ────────────────────────────────────────────
#
# Design (Decision #13 from WORKFLOW.md):
#   - When a stage deliverable requires Max's on-camera talent (recordings, scripts,
#     live demos), create a dedicated Linear ticket on the same run board.
#   - Telegram-notify Max immediately so it enters his queue.
#   - AI placeholder is generated and stored in the blackboard so the pipeline
#     doesn't block waiting for talent delivery.
#   - When Max delivers the real asset, swap the placeholder — no stage re-run needed.
#
# State schema (per-run, stored under state["talent_tickets"][talent_id]):
#   {
#     "talent_id":           str   — stable slug used as blackboard key prefix
#     "stage":               str   — which pipeline stage requested the ticket
#     "deliverable_type":    str   — e.g. "reel_script", "demo_recording", "voiceover"
#     "description":         str   — what Max needs to deliver (human-readable)
#     "brief":               str   — full production brief (from content-talent skill)
#     "status":              str   — "pending" | "in_progress" | "delivered" | "resolved"
#     "ai_placeholder_key":  str   — blackboard key holding the AI stand-in
#     "talent_artifact_url": str | null — filled when Max delivers
#     "linear_issue_id":     str
#     "linear_identifier":   str
#     "created_at":          str   — ISO8601
#     "resolved_at":         str | null
#   }
#
# Telegram notification text is returned by create_talent_ticket() — the
# orchestrating agent sends it via the message tool (engine.py is CLI-only).
#
# ─────────────────────────────────────────────────────────────────────────────

# Deliverable types supported in talent workflow
TALENT_DELIVERABLE_TYPES = {
    "reel_script":        "Short-form reel script (30–90s, for IG/TikTok/YT Shorts)",
    "long_form_script":   "Long-form video script (3–20 min, for YouTube/course)",
    "demo_recording":     "Product demo screen+face recording",
    "voiceover":          "Voice-only narration (for b-roll or explainer)",
    "testimonial_prompt": "Prompted testimonial or story segment",
    "talking_head":       "Talking-head segment (no demo, direct-to-camera)",
    "carousel_narration": "Narration track synced to a carousel/slide deck",
    "other":              "Custom / uncategorized talent deliverable",
}


def _talent_ticket_id(run_id: str, stage: str, deliverable_type: str, created_at: str) -> str:
    """Generate a stable slug for a talent ticket (used as dict key + blackboard prefix)."""
    ts = created_at[:16].replace(":", "").replace("-", "").replace("T", "")
    return f"talent-{stage}-{deliverable_type}-{ts}"


def create_talent_ticket(
    run_id: str,
    stage: str,
    deliverable_type: str,
    description: str,
    brief: str = "",
    ai_placeholder: str = "",
    urgency: str = "standard",
) -> dict[str, Any]:
    """Create a talent delivery ticket and wire up the AI placeholder.

    Creates a Linear sub-issue under the run's stage issue (same board/project),
    stores the ticket in run state, and returns structured data the orchestrating
    agent can use to:
      - Post the AI placeholder to the blackboard
      - Send the Telegram notification to Max

    Args:
        run_id:           Ship run ticket ID (e.g. "MAX-316")
        stage:            Pipeline stage requesting talent (e.g. "awareness")
        deliverable_type: One of TALENT_DELIVERABLE_TYPES keys (or "other")
        description:      What Max needs to deliver — concise, action-oriented
        brief:            Full production brief (from content-talent skill)
        ai_placeholder:   AI-generated stand-in content for this deliverable
        urgency:          standard | fast | urgent | relaxed (matches URGENCY_PRESETS)

    Returns:
        Dict with: talent_id, linear_issue, blackboard_key, telegram_text
    """
    state = load_run(run_id)
    now = datetime.now(timezone.utc).isoformat()
    product = state.get("name", run_id)

    talent_id = _talent_ticket_id(run_id, stage, deliverable_type, now)
    bb_key = f"talent.{talent_id}.deliverable"
    type_label = TALENT_DELIVERABLE_TYPES.get(deliverable_type, deliverable_type)

    # ── Resolve parent issue for the Linear sub-issue ──
    # Prefer the stage sub-issue; fall back to run parent
    sub_issues = state.get("linear", {}).get("subIssues", {})
    parent_issue_id = sub_issues.get(stage, {}).get("id") or state["linear"]["parentId"]
    project_id = state.get("linear", {}).get("projectId") or FALLBACK_LINEAR_PROJECT_ID

    urgency_r, _, _ = URGENCY_PRESETS.get(urgency, URGENCY_PRESETS["standard"])
    due_by_dt = (datetime.now(timezone.utc) + timedelta(hours=urgency_r * 3))
    due_by_str = due_by_dt.strftime("%Y-%m-%d")

    # ── Build the Linear issue body ──
    brief_section = f"\n## Production Brief\n\n{brief.strip()}\n" if brief.strip() else ""
    placeholder_section = (
        f"\n## AI Placeholder (active until talent delivers)\n\n"
        f"```\n{ai_placeholder.strip()}\n```\n\n"
        f"_Blackboard key: `{bb_key}`_\n"
        if ai_placeholder.strip() else ""
    )

    issue_body = f"""## Inputs
- Run: **{product}** ({run_id})
- Stage: `{stage}`
- Deliverable type: {type_label}
- Urgency: {urgency}
- Due by: {due_by_str}

## Deliverables
- [ ] {description}
- [ ] Upload/link final asset in Artifacts section below

## Verification
- Asset matches deliverable type: `{deliverable_type}`
- File accessible at linked URL or attached to this issue
- Format matches platform requirements for `{stage}` stage
{brief_section}
## AI Placeholder
Pipeline continues with AI-generated stand-in while talent delivers.
Swap in: `python3 skills/ship-engine/engine.py talent-swap {run_id} {talent_id} <artifact_url>`
{placeholder_section}
## Artifacts
- [ ] Final asset URL / attachment link:
"""

    # ── Create Linear issue ──
    try:
        result = gql("""
            mutation($input: IssueCreateInput!) {
                issueCreate(input: $input) {
                    issue { id identifier title url }
                }
            }
        """, {
            "input": {
                "teamId": MAX_TEAM_ID,
                "title": f"[Talent] {type_label} — {product} ({stage})",
                "description": issue_body,
                "parentId": parent_issue_id,
                "projectId": project_id,
                "labelIds": [SHIP_ENGINE_LABEL_ID],
                "priority": 2,  # High priority — Max's time is the bottleneck
                "stateId": STATES["Todo"],
            }
        })
        linear_issue = result["issueCreate"]["issue"]
        linear_issue_id = linear_issue["id"]
        linear_identifier = linear_issue["identifier"]
        linear_url = linear_issue.get("url", "")
    except Exception as e:
        _log_error(state, "create_talent_ticket.linear", e)
        save_run(state)
        linear_issue_id = None
        linear_identifier = None
        linear_url = ""
        linear_issue = {}

    # ── Write AI placeholder to blackboard ──
    if "blackboard" not in state:
        state["blackboard"] = {}
    state["blackboard"][bb_key] = ai_placeholder or f"[AI_PLACEHOLDER:{deliverable_type}]"
    state["blackboard"][f"talent.{talent_id}.status"] = "pending"

    # ── Store talent ticket in run state ──
    if "talent_tickets" not in state:
        state["talent_tickets"] = {}

    ticket_record = {
        "talent_id": talent_id,
        "stage": stage,
        "deliverable_type": deliverable_type,
        "type_label": type_label,
        "description": description,
        "brief": brief,
        "status": "pending",
        "urgency": urgency,
        "ai_placeholder_key": bb_key,
        "ai_placeholder_value": ai_placeholder,
        "talent_artifact_url": None,
        "linear_issue_id": linear_issue_id,
        "linear_identifier": linear_identifier,
        "linear_url": linear_url,
        "created_at": now,
        "resolved_at": None,
    }
    state["talent_tickets"][talent_id] = ticket_record
    save_run(state)

    # ── Build Telegram notification text (returned for agent to send) ──
    telegram_text = (
        f"🎬 *Talent ticket created* — {product}\n\n"
        f"*Stage:* {stage} | *Type:* {type_label}\n"
        f"*Deliverable:* {description}\n"
        f"*Due by:* {due_by_str}\n"
        f"*Linear:* {linear_identifier or 'see run'} — {linear_url}\n\n"
        f"📌 AI placeholder is active ({bb_key}). Pipeline continues without blocking.\n"
        f"When ready: `engine.py talent-swap {run_id} {talent_id} <url>`"
    )

    # ── Post status comment to parent stage issue ──
    try:
        comment_body = (
            f"### 🎬 Talent Ticket Created\n\n"
            f"**status_summary:** Talent delivery ticket raised for `{stage}` "
            f"({type_label}). AI placeholder active, pipeline unblocked.\n\n"
            f"**Ticket:** {linear_identifier} — {linear_url}\n"
            f"**Deliverable:** {description}\n"
            f"**Due by:** {due_by_str}\n"
            f"**Blackboard key:** `{bb_key}`\n\n"
            f"**next_steps:**\n"
            f"- Max records/delivers: {description}\n"
            f"- Upload asset and link in ticket Artifacts section\n"
            f"- Agent swaps deliverable: `engine.py talent-swap {run_id} {talent_id} <url>`\n"
        )
        gql("""
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
        """, {"issueId": parent_issue_id, "body": comment_body})
    except Exception as e:
        _log_error(state, "create_talent_ticket.comment", e)
        save_run(state)

    return {
        "talent_id": talent_id,
        "linear_issue": linear_issue,
        "blackboard_key": bb_key,
        "ai_placeholder": state["blackboard"][bb_key],
        "telegram_text": telegram_text,
        "telegram_group": TELEGRAM_MAX_GROUP,
        "status": "pending",
    }


def resolve_talent_ticket(
    run_id: str,
    talent_id: str,
    artifact_url: str,
) -> dict[str, Any]:
    """Swap the AI placeholder with the real talent deliverable.

    Updates the blackboard so all downstream stages see the real asset,
    marks the Linear ticket as Done, and records the swap in run state.

    Args:
        run_id:       Ship run ticket ID
        talent_id:    Talent ticket slug (from create_talent_ticket)
        artifact_url: URL or file path of the delivered asset

    Returns:
        Dict with updated blackboard key, old placeholder, new artifact URL.
    """
    state = load_run(run_id)

    tickets = state.get("talent_tickets", {})
    if talent_id not in tickets:
        raise ValueError(
            f"Talent ticket '{talent_id}' not found in run {run_id}. "
            f"Valid IDs: {list(tickets.keys())}"
        )

    ticket = tickets[talent_id]
    if ticket["status"] == "resolved":
        raise RuntimeError(
            f"Talent ticket '{talent_id}' is already resolved "
            f"(artifact: {ticket['talent_artifact_url']}). Nothing to swap."
        )

    now = datetime.now(timezone.utc).isoformat()
    bb_key = ticket["ai_placeholder_key"]
    old_placeholder = state.get("blackboard", {}).get(bb_key, "")

    # ── Swap the blackboard value ──
    if "blackboard" not in state:
        state["blackboard"] = {}
    state["blackboard"][bb_key] = artifact_url
    state["blackboard"][f"talent.{talent_id}.status"] = "resolved"
    state["blackboard"][f"talent.{talent_id}.artifact_url"] = artifact_url

    # ── Update ticket record ──
    ticket["status"] = "resolved"
    ticket["talent_artifact_url"] = artifact_url
    ticket["resolved_at"] = now
    state["talent_tickets"][talent_id] = ticket
    save_run(state)

    # ── Mark Linear issue Done ──
    if ticket.get("linear_issue_id"):
        try:
            gql("""
                mutation($id: String!, $stateId: String!) {
                    issueUpdate(id: $id, input: { stateId: $stateId }) {
                        issue { id }
                    }
                }
            """, {"id": ticket["linear_issue_id"], "stateId": STATES["Done"]})

            gql("""
                mutation($issueId: String!, $body: String!) {
                    commentCreate(input: { issueId: $issueId, body: $body }) {
                        comment { id }
                    }
                }
            """, {
                "issueId": ticket["linear_issue_id"],
                "body": (
                    f"### ✅ Talent Delivered — Placeholder Swapped\n\n"
                    f"**status_summary:** Talent asset delivered and swapped into pipeline.\n\n"
                    f"**Asset URL:** {artifact_url}\n"
                    f"**Blackboard key:** `{bb_key}`\n"
                    f"**Resolved at:** {now[:16]} UTC\n\n"
                    f"**next_steps:** Downstream stage agents will use the real asset on "
                    f"next execution. No stage re-run required."
                ),
            })
        except Exception as e:
            _log_error(state, "resolve_talent_ticket.linear", e)
            save_run(state)

    return {
        "talent_id": talent_id,
        "stage": ticket["stage"],
        "deliverable_type": ticket["deliverable_type"],
        "blackboard_key": bb_key,
        "old_placeholder": old_placeholder,
        "new_artifact_url": artifact_url,
        "resolved_at": now,
    }


def list_talent_tickets(run_id: str, status_filter: str = "all") -> list[dict[str, Any]]:
    """List talent tickets for a run, optionally filtered by status.

    Args:
        run_id:        Ship run ticket ID
        status_filter: "pending" | "resolved" | "all" (default: "all")

    Returns:
        List of talent ticket dicts, newest-first.
    """
    state = load_run(run_id)
    tickets = state.get("talent_tickets", {})

    if not tickets:
        return []

    all_tickets = sorted(
        tickets.values(),
        key=lambda t: t.get("created_at", ""),
        reverse=True,
    )

    if status_filter == "all":
        return all_tickets
    return [t for t in all_tickets if t["status"] == status_filter]


def format_talent_status(run_id: str) -> str:
    """Format talent ticket status for display (Telegram-friendly)."""
    state = load_run(run_id)
    product = state.get("name", run_id)
    tickets = state.get("talent_tickets", {})

    if not tickets:
        return f"🎬 No talent tickets for {product} ({run_id})."

    pending = [t for t in tickets.values() if t["status"] == "pending"]
    resolved = [t for t in tickets.values() if t["status"] == "resolved"]

    lines = [f"🎬 *Talent Tickets — {product}* ({run_id})"]
    lines.append(f"Pending: {len(pending)} | Resolved: {len(resolved)} | Total: {len(tickets)}")

    if pending:
        lines.append("\n⏳ *Pending:*")
        for t in sorted(pending, key=lambda x: x["created_at"]):
            age_h = (
                (datetime.now(timezone.utc) - datetime.fromisoformat(t["created_at"])).total_seconds() / 3600
            )
            lines.append(
                f"  • `{t['talent_id']}`\n"
                f"    Stage: {t['stage']} | Type: {t['type_label']}\n"
                f"    Task: {t['description']}\n"
                f"    Linear: {t.get('linear_identifier', '?')} | Age: {age_h:.0f}h"
            )

    if resolved:
        lines.append("\n✅ *Resolved:*")
        for t in sorted(resolved, key=lambda x: x.get("resolved_at", ""), reverse=True)[:5]:
            lines.append(
                f"  • `{t['talent_id']}` — {t['type_label']} ({t['stage']})"
                f"\n    Asset: {t['talent_artifact_url']}"
            )

    return "\n".join(lines)


# ── End NEO-225: Talent Ticket System ─────────────────────────────────────────


# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: engine.py <command> [args]")
        print("Commands: create, status, advance, parallel, list, kill, comment, retry, check-all,")
        print("          blackboard, quality-check, drive, drive-init, drive-mkdir, measure, urgency,")
        print("          launch-orchestrate, launch-wave, launch-wave-done, launch-notify,")
        print("          launch-rollback, launch-status, launch-check-triggers,")
        print("          event (stage_complete|approval_received|blocked|timeout),")
        print("          budget (propose|approve|spend|check|status|override),")
        print("          talent-ticket, talent-swap, talent-list, talent-status, talent-types")
        sys.exit(1)

    cmd = sys.argv[1]


    if cmd == "event":
        if len(sys.argv) < 4:
            print("Usage: engine.py event <run_id> <event_type> [payload_json]")
            print("")
            print("Event types:")
            for etype, desc in VALID_EVENTS.items():
                print(f"  {etype:<22} {desc[:70]}")
            print("")
            print("Payload examples:")
            print('  stage_complete:    \'{"output_path": "runs/MAX-316/validate/icp.md"}\'')
            print('  approval_received: \'{"gate": "validate", "approver": "Max"}\'')
            print('  blocked:           \'{"reason": "Need API keys from Max"}\'')
            print('  timeout:           \'{"force_action": "reminder"}\'')
            sys.exit(1)

        run_id = sys.argv[2]
        event_type = sys.argv[3]
        payload = {}
        if len(sys.argv) > 4:
            try:
                payload = json.loads(sys.argv[4])
                if not isinstance(payload, dict):
                    raise ValueError("Payload must be a JSON object")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"❌ Invalid payload JSON: {e}")
                sys.exit(1)

        try:
            result = dispatch_event(run_id, event_type, payload)
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"❌ Run not found: {e}")
            sys.exit(1)

        event_icons = {
            "stage_complete": "✅", "approval_received": "✅",
            "blocked": "🚧", "timeout": "⏱",
        }
        icon = event_icons.get(event_type, "📋")
        print(f"{icon} Event dispatched: {event_type} → {run_id}")
        print(f"   Timestamp: {result.get('timestamp', '?')[:19]} UTC")

        if event_type == "stage_complete":
            verdict = result.get("verdict", "?")
            advanced = result.get("advanced_to")
            err = result.get("error")
            verdict_icon = {"PASS": "✅", "REVISE": "⚠️", "FAIL": "❌"}.get(verdict, "📋")
            print(f"   Gate verdict: {verdict_icon} {verdict}")
            if advanced:
                print(f"   Advanced to: {advanced}")
            if err:
                print(f"   ⚠️  {err}")
        elif event_type == "approval_received":
            gate = result.get("gate", "?")
            verdict_str = result.get("verdict", "?")
            advanced = result.get("advanced_to")
            print(f"   Gate: {gate} | Verdict: {verdict_str}")
            if advanced:
                print(f"   Pipeline advanced to: {advanced}")
        elif event_type == "blocked":
            stage = result.get("stage", "?")
            reason = result.get("reason", "?")
            print(f"   Stage: {stage}")
            print(f"   Reason: {reason}")
            print("   Linear issue updated to Blocked by Max state (if available)")
        elif event_type == "timeout":
            action = result.get("action_taken", "?")
            elapsed = result.get("elapsed_hours")
            msg = result.get("message", "")
            action_icon = {
                "pause": "⛔", "escalation": "⚠️", "reminder": "🔔",
                "no_action": "💤", "skipped": "⏭",
            }.get(action, "📋")
            print(f"   Action: {action_icon} {action}")
            if elapsed is not None:
                print(f"   Elapsed: {elapsed}h")
            if msg:
                print(f"   {msg}")

        err = result.get("error")
        if err and event_type not in ("stage_complete",):
            print(f"   ⚠️  {err}")

    elif cmd == "create":
        if len(sys.argv) < 4:
            print("Usage: engine.py create <name> <description> [priority]")
            sys.exit(1)
        name = sys.argv[2]
        desc = sys.argv[3]
        priority = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        state = create_ship_run(name, desc, priority)
        print(json.dumps(state, indent=2))

    elif cmd == "status":
        ticket_id = sys.argv[2] if len(sys.argv) > 2 else None
        print(format_status(ticket_id))

    elif cmd == "advance":
        if len(sys.argv) < 4:
            print("Usage: engine.py advance <ticket-id> <stage>")
            sys.exit(1)
        state = advance_stage(sys.argv[2], sys.argv[3])
        print(f"Advanced {state['ticket']} to {state['stage']}")

    elif cmd == "parallel":
        if len(sys.argv) < 3:
            print("Usage: engine.py parallel <ticket-id> [stage1,stage2,...]")
            sys.exit(1)
        stages = sys.argv[3].split(",") if len(sys.argv) > 3 else PARALLEL_STAGES
        state = start_parallel(sys.argv[2], stages)
        print(f"Started parallel: {', '.join(stages)}")

    elif cmd == "list":
        runs = list_runs()
        if not runs:
            print("No active ship runs.")
        else:
            for r in runs:
                print(f"{r['ticket']}: {r['name']} [{r['stage']}] (updated: {r['updated'][:10]})")

    elif cmd == "kill":
        if len(sys.argv) < 4:
            print("Usage: engine.py kill <ticket-id> <reason>")
            sys.exit(1)
        state = kill_run(sys.argv[2], sys.argv[3])
        print(f"Killed {state['ticket']}: {sys.argv[3]}")

    elif cmd == "comment":
        if len(sys.argv) < 5:
            print("Usage: engine.py comment <ticket-id> <stage> <body>")
            sys.exit(1)
        add_comment(sys.argv[2], sys.argv[3], sys.argv[4])
        print("Comment added.")

    elif cmd == "retry":
        if len(sys.argv) < 3:
            print("Usage: engine.py retry <ticket-id>")
            sys.exit(1)
        state = load_run(sys.argv[2])
        errors = state.get("errors", [])
        if not errors:
            print("No errors recorded for this run.")
        else:
            last = errors[-1]
            print(f"Last error: [{last.get('timestamp', '?')[:16]}] {last['function']}: {last['error']}")
            print("Retry by re-running the failed operation manually.")

    elif cmd == "check-all":
        actions = check_all_timeouts()
        if not actions:
            print("No timeout actions needed.")
        else:
            for a in actions:
                print(a)

    elif cmd == "blackboard":
        if len(sys.argv) < 4:
            print("Usage: engine.py blackboard <ticket-id> get <key>")
            print("       engine.py blackboard <ticket-id> set <key> <value>")
            sys.exit(1)
        state = load_run(sys.argv[2])
        bb = state.get("blackboard", {})
        sub = sys.argv[3]
        if sub == "get":
            key = sys.argv[4] if len(sys.argv) > 4 else None
            if key:
                print(bb.get(key, f"(not set: {key})"))
            else:
                print(json.dumps(bb, indent=2))
        elif sub == "set":
            if len(sys.argv) < 6:
                print("Usage: engine.py blackboard <ticket-id> set <key> <value>")
                sys.exit(1)
            key, value = sys.argv[4], sys.argv[5]
            if "blackboard" not in state:
                state["blackboard"] = {}
            state["blackboard"][key] = value
            save_run(state)
            print(f"Set blackboard[{key}] = {value}")
        else:
            print(f"Unknown blackboard sub-command: {sub}")

    elif cmd == "quality-check":
        if len(sys.argv) < 4:
            print("Usage: engine.py quality-check <ticket-id> <stage> [output-path]")
            sys.exit(1)
        output_path = sys.argv[4] if len(sys.argv) > 4 else None
        verdict, feedback = quality_gate(sys.argv[2], sys.argv[3], output_path)
        print(feedback)

    elif cmd == "drive":
        if len(sys.argv) < 3:
            print("Usage: engine.py drive <ticket-id>")
            sys.exit(1)
        state = load_run(sys.argv[2])
        drive = state.get("drive")
        if not drive:
            print(f"⚠️ No Drive folders found for {sys.argv[2]}. Run 'engine.py drive-init {sys.argv[2]}' to create them.")
        else:
            root_id = drive["root_folder_id"]
            print(f"📁 Root: https://drive.google.com/drive/folders/{root_id}")
            for subfolder, fid in drive.get("folders", {}).items():
                print(f"   {subfolder}: https://drive.google.com/drive/folders/{fid}")

    elif cmd == "drive-init":
        if len(sys.argv) < 3:
            print("Usage: engine.py drive-init <ticket-id>")
            sys.exit(1)
        state = load_run(sys.argv[2])
        if state.get("drive"):
            print(f"Drive folders already exist for {sys.argv[2]}.")
            root_id = state["drive"]["root_folder_id"]
            print(f"📁 Root: https://drive.google.com/drive/folders/{root_id}")
        else:
            try:
                drive = create_drive_folders(sys.argv[2], state["name"])
                state["drive"] = {
                    "root_folder_id": drive["root_folder_id"],
                    "folders": drive["folders"],
                }
                save_run(state)
                root_id = drive["root_folder_id"]
                print(f"✅ Drive folders created.")
                print(f"📁 Root: https://drive.google.com/drive/folders/{root_id}")
                for subfolder, fid in drive["folders"].items():
                    print(f"   {subfolder}: https://drive.google.com/drive/folders/{fid}")
            except Exception as e:
                print(f"❌ Drive folder creation failed: {e}")
                sys.exit(1)

    elif cmd == "measure":
        if len(sys.argv) < 3:
            print("Usage: engine.py measure <run_id>")
            print("       engine.py measure <run_id> set <metric> <value>")
            print("       engine.py measure <run_id> threshold <metric> <warn> <critical>")
            print("       engine.py measure <run_id> owner <metric> <stage>")
            print(f"Available metrics: {', '.join(DEFAULT_METRIC_THRESHOLDS.keys())}")
            sys.exit(1)

        run_id = sys.argv[2]

        if len(sys.argv) >= 6 and sys.argv[3] == "set":
            # Record a metric value: engine.py measure <run_id> set <metric> <value>
            metric = sys.argv[4]
            try:
                value = float(sys.argv[5])
            except ValueError:
                print(f"❌ Value must be a number (got: {sys.argv[5]})")
                sys.exit(1)
            if metric not in DEFAULT_METRIC_THRESHOLDS:
                print(f"⚠️  Unknown metric '{metric}'. Known: {', '.join(DEFAULT_METRIC_THRESHOLDS.keys())}")
            state = load_run(run_id)
            if "metrics" not in state:
                state["metrics"] = {}
            state["metrics"][metric] = value
            save_run(state)
            label = METRIC_LABELS.get(metric, metric)
            fmt = DEFAULT_METRIC_THRESHOLDS.get(metric, {}).get("fmt", "raw")
            print(f"✅ Recorded {label} = {_fmt_metric(value, fmt)}")

        elif len(sys.argv) >= 6 and sys.argv[3] == "threshold":
            # Set custom threshold: engine.py measure <run_id> threshold <metric> <warn> <critical>
            metric = sys.argv[4]
            try:
                warn_val = float(sys.argv[5])
                crit_val = float(sys.argv[6]) if len(sys.argv) > 6 else None
            except (ValueError, IndexError):
                print("Usage: engine.py measure <run_id> threshold <metric> <warn> <critical>")
                sys.exit(1)
            state = load_run(run_id)
            if "custom_thresholds" not in state:
                state["custom_thresholds"] = {}
            override = {"warn": warn_val}
            if crit_val is not None:
                override["critical"] = crit_val
            state["custom_thresholds"][metric] = override
            save_run(state)
            print(f"✅ Custom threshold for {metric}: warn={warn_val}, critical={crit_val}")

        elif len(sys.argv) >= 6 and sys.argv[3] == "owner":
            # Set metric ownership: engine.py measure <run_id> owner <metric> <stage>
            metric = sys.argv[4]
            stage_name = sys.argv[5]
            state = load_run(run_id)
            if "metric_ownership" not in state:
                state["metric_ownership"] = {}
            state["metric_ownership"][metric] = stage_name
            save_run(state)
            print(f"✅ Metric {metric} → owned by {stage_name}")

        else:
            # Run measure feedback loop
            result = measure_feedback(run_id)
            verdict = result["verdict"]
            healthy = result["healthy"]
            warning = result["warning"]
            critical = result["critical"]
            tickets = result["tickets_created"]

            if verdict == "NO_DATA":
                print(f"⚠️  No metrics recorded for {run_id}.")
                print(f"Record metrics first:")
                for k, cfg in DEFAULT_METRIC_THRESHOLDS.items():
                    label = METRIC_LABELS.get(k, k)
                    print(f"  engine.py measure {run_id} set {k} <value>  # {label}")
                sys.exit(0)

            print(f"\n📊 Measure Report — {run_id}")
            print("=" * 42)

            if healthy:
                print(f"\n✅ HEALTHY ({len(healthy)}):")
                for m in healthy:
                    print(f"  • {m['label']}: {_fmt_metric(m['value'], m['fmt'])}")

            if warning:
                print(f"\n⚠️  WARNING ({len(warning)}) — improvement tickets created:")
                for m in warning:
                    print(f"  • {m['label']}: {_fmt_metric(m['value'], m['fmt'])} "
                          f"(target ≥ {_fmt_metric(m['target'], m['fmt'])}, "
                          f"gap: {_fmt_metric(m['gap'], m['fmt'])})")

            if critical:
                print(f"\n🔴 CRITICAL ({len(critical)}) — escalation tickets created:")
                for m in critical:
                    print(f"  • {m['label']}: {_fmt_metric(m['value'], m['fmt'])} "
                          f"(target ≥ {_fmt_metric(m['target'], m['fmt'])}, "
                          f"gap: {_fmt_metric(m['gap'], m['fmt'])})")

            print(f"\n{'=' * 42}")
            verdict_icons = {
                "DOUBLE DOWN": "🚀",
                "ITERATE": "🔄",
                "KILL or PIVOT": "⛔",
            }
            icon = verdict_icons.get(verdict, "📋")
            print(f"{icon}  Verdict: {verdict}")
            if tickets:
                print(f"🎫 {tickets} feedback ticket(s) created in Linear")
            if verdict == "KILL or PIVOT":
                print("⚠️  Critical metrics detected — escalate to Max for decision")

    elif cmd == "urgency":
        if len(sys.argv) < 4:
            print("Usage: engine.py urgency <run_id> <preset>")
            print(f"Presets: {', '.join(URGENCY_PRESETS.keys())}")
            sys.exit(1)
        run_id = sys.argv[2]
        preset = sys.argv[3]
        if preset not in URGENCY_PRESETS:
            print(f"❌ Unknown preset '{preset}'. Available: {', '.join(URGENCY_PRESETS.keys())}")
            sys.exit(1)
        state = load_run(run_id)
        state["urgency"] = preset
        save_run(state)
        r, e, p = URGENCY_PRESETS[preset]
        print(f"✅ Urgency set to '{preset}' — reminder {r}h, escalation {e}h, auto-pause {p}h")

    elif cmd == "drive-mkdir":
        if len(sys.argv) < 4:
            print("Usage: engine.py drive-mkdir <run_id> <folder_name>")
            sys.exit(1)
        run_id = sys.argv[2]
        folder_name = sys.argv[3]
        try:
            folder_id = create_drive_subfolder(run_id, folder_name)
            print(f"✅ Created folder '{folder_name}': https://drive.google.com/drive/folders/{folder_id}")
        except Exception as e:
            print(f"❌ Failed: {e}")
            sys.exit(1)

    # ── NEO-232: 4-Wave Launch Orchestration ──────────────────────────────────

    elif cmd == "launch-orchestrate":
        if len(sys.argv) < 4:
            print("Usage: engine.py launch-orchestrate <run_id> <launch_date_iso> [dry_run|production]")
            print("  launch_date_iso: YYYY-MM-DD format (L-Day)")
            print("  run_mode: 'production' (default) registers cron jobs; 'dry_run' plans only")
            sys.exit(1)
        run_id = sys.argv[2]
        launch_date_iso = sys.argv[3]
        run_mode = sys.argv[4] if len(sys.argv) > 4 else "production"
        result = schedule_launch_waves(run_id, launch_date_iso, run_mode)
        scheduled = result.get("scheduled", 0)
        total = result.get("total_jobs", 0)
        print(f"✅ 4-Wave Launch Orchestration scheduled for {run_id}")
        print(f"   L-Day: {launch_date_iso} | Mode: {run_mode}")
        print(f"   {scheduled}/{total} wave jobs registered")
        # Print wave timeline
        print("\nWave Timeline:")
        cj = result.get("cron_jobs", {})
        for wk, ws in sorted(result["schedule"].items(), key=lambda x: x[1]["fires_at"]):
            status = cj.get(wk, {}).get("status", "?")
            icon = {"scheduled": "✅", "dry_run": "🔍", "skipped_past": "⏭", "failed": "❌"}.get(status, "⚠️")
            print(f"  {icon} [{wk}] {ws['wave_name']:<40} {ws['fires_at'][:16]} UTC")

    elif cmd == "launch-wave":
        if len(sys.argv) < 4:
            print("Usage: engine.py launch-wave <run_id> <wave_key>")
            print("  wave_key examples: wave1, wave2, wave3_pre_wave, wave3_morning_wave,")
            print("                     wave3_midday_wave, wave3_afternoon_wave,")
            print("                     wave4_d1_tutorial, wave4_d3_social_proof, ...")
            sys.exit(1)
        run_id = sys.argv[2]
        wave_key = sys.argv[3]
        try:
            result = execute_wave(run_id, wave_key)
            print(f"🚀 Wave executing: {result['wave_name']} ({wave_key})")
            print(f"   Started: {result['started_at'][:16]} UTC")
            print(f"   Channels: {', '.join(result['channels'])}")
            print("\n   Actions:")
            for a in result["actions"]:
                ch_label = WAVE_CHANNEL_LABELS.get(a.get("channel", ""), a.get("channel", ""))
                print(f"   ☐ [{ch_label}] {a['id']}: {a['description'][:80]}")
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif cmd == "launch-wave-done":
        # Mark a specific action within a wave as complete
        if len(sys.argv) < 5:
            print("Usage: engine.py launch-wave-done <run_id> <wave_key> <action_id> [done|skipped|failed]")
            sys.exit(1)
        run_id = sys.argv[2]
        wave_key = sys.argv[3]
        action_id = sys.argv[4]
        status = sys.argv[5] if len(sys.argv) > 5 else "done"
        try:
            record = complete_wave_action(run_id, wave_key, action_id, status)
            remaining = sum(1 for v in record["actions"].values() if v == "pending")
            print(f"✅ Marked {action_id} as '{status}' in wave {wave_key}")
            if record.get("completed_at"):
                print(f"   Wave complete! Completed at: {record['completed_at'][:16]} UTC")
            else:
                print(f"   {remaining} action(s) still pending")
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif cmd == "launch-notify":
        if len(sys.argv) < 4:
            print("Usage: engine.py launch-notify <run_id> <segment>")
            print(f"  segments: {', '.join(SUPPORTER_SEGMENTS.keys())}")
            sys.exit(1)
        run_id = sys.argv[2]
        segment = sys.argv[3]
        if segment not in SUPPORTER_SEGMENTS:
            print(f"❌ Unknown segment '{segment}'. Available: {', '.join(SUPPORTER_SEGMENTS.keys())}")
            sys.exit(1)
        result = notify_supporters(run_id, segment)
        seg_label = result["segment_label"]
        issue = result.get("linear_issue")
        if issue:
            print(f"✅ Supporter notification task created for segment: {seg_label}")
            print(f"   Linear: {issue.get('identifier')} — {issue.get('title')}")
        else:
            print(f"⚠️  Notification task created (Linear issue creation may have failed)")
        print(f"   Notify at: {result['notify_utc_hour']:02d}:00 UTC")

    elif cmd == "launch-rollback":
        if len(sys.argv) < 3:
            print("Usage: engine.py launch-rollback <run_id> [reason]")
            sys.exit(1)
        run_id = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "Manual rollback triggered"
        record = rollback_launch(run_id, reason)
        print(f"🚨 ROLLBACK TRIGGERED for {run_id}")
        print(f"   Reason: {reason}")
        print(f"   Triggered at: {record['triggered_at'][:16]} UTC")
        print("\n   Rollback runbook:")
        for i, step in enumerate(ROLLBACK_STEPS):
            print(f"   {i + 1}. {step}")

    elif cmd == "launch-status":
        if len(sys.argv) < 3:
            print("Usage: engine.py launch-status <run_id>")
            sys.exit(1)
        run_id = sys.argv[2]
        print(launch_status(run_id))

    elif cmd == "launch-check-triggers":
        if len(sys.argv) < 3:
            print("Usage: engine.py launch-check-triggers <run_id>")
            sys.exit(1)
        run_id = sys.argv[2]
        result = check_rollback_triggers(run_id)
        verdict = result["verdict"]
        triggered = result["triggered"]
        warnings = result["warnings"]
        checked = result["metrics_checked"]

        verdict_icon = {"STABLE": "✅", "ALERT": "⚠️", "ROLLBACK": "🔴"}.get(verdict, "❓")
        print(f"\n{verdict_icon} Rollback Check — {run_id}: **{verdict}**")
        print(f"   Metrics evaluated: {', '.join(checked) if checked else '(none recorded yet)'}")

        if triggered:
            print(f"\n🔴 CRITICAL ({len(triggered)}) — rollback recommended:")
            for t in triggered:
                print(f"   • {t['trigger']}: {t['description']}")
                print(f"     Current: {t['current_value']}  Threshold: {t['threshold']}")
                print(f"     Action: {t['action']}")
            print(f"\n   Run: engine.py launch-rollback {run_id} '<reason>'")
        if warnings:
            print(f"\n⚠️  WARNING ({len(warnings)}) — investigate:")
            for w in warnings:
                print(f"   • {w['trigger']}: {w['description']}")
                print(f"     Current: {w['current_value']}  Threshold: {w['threshold']}")
        if not triggered and not warnings:
            print("   All checked metrics within acceptable range.")

    # ── NEO-224: Budget Tracking & Enforcement ────────────────────────────────

    elif cmd == "budget":
        if len(sys.argv) < 4:
            print("Usage: engine.py budget <sub-command> <run_id> [args]")
            print("Sub-commands:")
            print("  propose  <run_id> <total_usd> [stage=amount,...] [notes]")
            print("  approve  <run_id> [approved_amount]")
            print("  spend    <run_id> <amount> <category> [stage] [description]")
            print(f"           categories: {', '.join(BUDGET_CATEGORIES)}")
            print("  check    <run_id>")
            print("  status   <run_id>")
            print("  override <run_id> <reason>")
            sys.exit(1)

        sub = sys.argv[2]
        run_id = sys.argv[3]

        if sub == "propose":
            # engine.py budget propose <run_id> <total_usd> [stage=amount,...] [notes]
            if len(sys.argv) < 5:
                print("Usage: engine.py budget propose <run_id> <total_usd> [stage=amount,...] [notes]")
                sys.exit(1)
            try:
                total = float(sys.argv[4])
            except ValueError:
                print(f"❌ total_usd must be a number (got: {sys.argv[4]})")
                sys.exit(1)
            per_stage: dict[str, float] = {}
            notes = ""
            for arg in sys.argv[5:]:
                if "=" in arg:
                    k, v = arg.split("=", 1)
                    try:
                        per_stage[k.strip()] = float(v.strip())
                    except ValueError:
                        print(f"⚠️  Skipping invalid stage budget: {arg}")
                else:
                    notes = arg
            result = budget_propose(run_id, total, per_stage or None, notes)
            print(result["message"])
            if per_stage:
                for s, a in per_stage.items():
                    print(f"  {s}: ${a:.2f}")

        elif sub == "approve":
            # engine.py budget approve <run_id> [approved_amount]
            amount = None
            if len(sys.argv) > 4:
                try:
                    amount = float(sys.argv[4])
                except ValueError:
                    print(f"❌ approved_amount must be a number (got: {sys.argv[4]})")
                    sys.exit(1)
            result = budget_approve(run_id, amount)
            print(f"✅ {result['message']}")

        elif sub == "spend":
            # engine.py budget spend <run_id> <amount> <category> [stage] [description]
            if len(sys.argv) < 6:
                print("Usage: engine.py budget spend <run_id> <amount> <category> [stage] [description]")
                print(f"Categories: {', '.join(BUDGET_CATEGORIES)}")
                sys.exit(1)
            try:
                amount = float(sys.argv[4])
            except ValueError:
                print(f"❌ amount must be a number (got: {sys.argv[4]})")
                sys.exit(1)
            category = sys.argv[5]
            stage = sys.argv[6] if len(sys.argv) > 6 else ""
            description = sys.argv[7] if len(sys.argv) > 7 else ""
            try:
                result = budget_record_spend(run_id, amount, category, stage, description)
            except ValueError as e:
                print(f"❌ {e}")
                sys.exit(1)
            icon = BUDGET_STATUS_ICONS.get(result["status"], "")
            print(f"{icon} {result['message']}")
            if result["soft_block"]:
                print(f"   Run 'engine.py budget override {run_id} \"<reason>\"' to unblock.")
                sys.exit(2)  # Non-zero exit so callers know they're blocked

        elif sub == "check":
            # engine.py budget check <run_id>
            result = budget_check(run_id)
            icon = BUDGET_STATUS_ICONS.get(result["status"], "")
            print(f"{icon} {result['message']}")
            print(f"   Spent: ${result['spent']:.2f}  Approved: {'${:.2f}'.format(result['approved']) if result['approved'] else 'N/A'}  ({result['pct']:.1f}%)")
            if result["soft_block"]:
                sys.exit(2)

        elif sub == "status":
            # engine.py budget status <run_id>
            print(budget_status(run_id))

        elif sub == "override":
            # engine.py budget override <run_id> <reason>
            if len(sys.argv) < 5:
                print("Usage: engine.py budget override <run_id> <reason>")
                sys.exit(1)
            reason = sys.argv[4]
            result = budget_override(run_id, reason)
            print(f"🟠 {result['message']}")

        else:
            print(f"❌ Unknown budget sub-command: '{sub}'")
            print("Use: propose | approve | spend | check | status | override")
            sys.exit(1)

    # ── NEO-225: Talent Ticket CLI ────────────────────────────────────────────

    elif cmd == "talent-types":
        # List all supported deliverable types
        print("🎬 Supported talent deliverable types:\n")
        for key, label in TALENT_DELIVERABLE_TYPES.items():
            print(f"  {key:<24} {label}")

    elif cmd == "talent-ticket":
        # Create a talent ticket with AI placeholder
        # Usage: engine.py talent-ticket <run_id> <stage> <deliverable_type> "description"
        #                                ["brief"] ["ai_placeholder"] [--urgency standard]
        if len(sys.argv) < 6:
            print("Usage: engine.py talent-ticket <run_id> <stage> <deliverable_type> <description>")
            print("         [<brief>] [<ai_placeholder>] [--urgency standard|fast|urgent|relaxed]")
            print()
            print(f"  Stages: {', '.join(STAGES)}")
            print(f"  Types:  {', '.join(TALENT_DELIVERABLE_TYPES.keys())}")
            print()
            print("Example:")
            print(f"  engine.py talent-ticket MAX-316 awareness reel_script \\")
            print(f"    'Record 60s reel: problem hook + product demo' \\")
            print(f"    'Hook: Start with pain statement. Demo: screen share in second half.' \\")
            print(f"    'AI PLACEHOLDER: [script text here]'")
            sys.exit(1)

        run_id          = sys.argv[2]
        stage           = sys.argv[3]
        deliverable_type = sys.argv[4]
        description     = sys.argv[5]
        brief           = sys.argv[6] if len(sys.argv) > 6 else ""
        ai_placeholder  = sys.argv[7] if len(sys.argv) > 7 else ""

        # Parse --urgency flag
        urgency = "standard"
        args_rest = sys.argv[8:]
        for i, arg in enumerate(args_rest):
            if arg == "--urgency" and i + 1 < len(args_rest):
                urgency = args_rest[i + 1]
                break

        if deliverable_type not in TALENT_DELIVERABLE_TYPES:
            print(f"⚠️  Unknown deliverable type '{deliverable_type}'.")
            print(f"   Valid types: {', '.join(TALENT_DELIVERABLE_TYPES.keys())}")
            print("   Use 'other' for custom types.")

        try:
            result = create_talent_ticket(
                run_id, stage, deliverable_type, description,
                brief=brief, ai_placeholder=ai_placeholder, urgency=urgency,
            )
            print(f"✅ Talent ticket created for {run_id}")
            print(f"   ID:         {result['talent_id']}")
            issue = result.get("linear_issue") or {}
            if issue.get("identifier"):
                print(f"   Linear:     {issue['identifier']} — {issue.get('url', '')}")
            print(f"   Blackboard: {result['blackboard_key']}")
            print(f"   Status:     {result['status']}")
            print()
            print("📣 Telegram notification (send via message tool):")
            print(f"   Group: {result['telegram_group']}")
            print(f"   Text:  {result['telegram_text']}")
            print()
            print(f"   When talent delivers, run:")
            print(f"   engine.py talent-swap {run_id} {result['talent_id']} <artifact_url>")
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif cmd == "talent-swap":
        # Swap AI placeholder with real talent deliverable
        # Usage: engine.py talent-swap <run_id> <talent_id> <artifact_url>
        if len(sys.argv) < 5:
            print("Usage: engine.py talent-swap <run_id> <talent_id> <artifact_url>")
            print()
            print("  Replaces the AI placeholder on the blackboard with the real asset.")
            print("  Marks the Linear talent ticket as Done.")
            print()
            print("Example:")
            print("  engine.py talent-swap MAX-316 talent-awareness-reel_script-202602251230 \\")
            print("    https://drive.google.com/file/d/abc123/view")
            sys.exit(1)

        run_id       = sys.argv[2]
        talent_id    = sys.argv[3]
        artifact_url = sys.argv[4]

        try:
            result = resolve_talent_ticket(run_id, talent_id, artifact_url)
            print(f"✅ Talent placeholder swapped for {run_id}")
            print(f"   Talent ID:    {result['talent_id']}")
            print(f"   Stage:        {result['stage']}")
            print(f"   Blackboard:   {result['blackboard_key']}")
            print(f"   Old value:    {str(result['old_placeholder'])[:80]}{'...' if len(str(result['old_placeholder'])) > 80 else ''}")
            print(f"   New artifact: {result['new_artifact_url']}")
            print(f"   Resolved at:  {result['resolved_at'][:16]} UTC")
        except (ValueError, RuntimeError) as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif cmd == "talent-list":
        # List talent tickets for a run
        # Usage: engine.py talent-list <run_id> [pending|resolved|all]
        if len(sys.argv) < 3:
            print("Usage: engine.py talent-list <run_id> [pending|resolved|all]")
            sys.exit(1)

        run_id        = sys.argv[2]
        status_filter = sys.argv[3] if len(sys.argv) > 3 else "all"

        if status_filter not in ("pending", "resolved", "all"):
            print(f"❌ Unknown filter '{status_filter}'. Use: pending | resolved | all")
            sys.exit(1)

        try:
            tickets = list_talent_tickets(run_id, status_filter)
            if not tickets:
                filter_label = f" [{status_filter}]" if status_filter != "all" else ""
                print(f"No talent tickets{filter_label} for {run_id}.")
            else:
                state_for_name = load_run(run_id)
                product = state_for_name.get("name", run_id)
                print(f"🎬 Talent tickets for {product} ({run_id})"
                      + (f" — filter: {status_filter}" if status_filter != "all" else ""))
                print(f"{'─' * 60}")
                for t in tickets:
                    status_icon = {"pending": "⏳", "in_progress": "🔄", "resolved": "✅"}.get(
                        t["status"], "❓"
                    )
                    print(f"\n{status_icon} {t['talent_id']}")
                    print(f"   Stage:    {t['stage']} | Type: {t['type_label']}")
                    print(f"   Task:     {t['description']}")
                    print(f"   Linear:   {t.get('linear_identifier', '?')} {t.get('linear_url', '')}")
                    print(f"   Created:  {t['created_at'][:16]} UTC")
                    if t["status"] == "resolved":
                        print(f"   Asset:    {t['talent_artifact_url']}")
                        print(f"   Resolved: {t.get('resolved_at', '?')[:16]} UTC")
                    else:
                        print(f"   BB key:   {t['ai_placeholder_key']}")
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif cmd == "talent-status":
        # Show formatted talent status (Telegram-ready)
        # Usage: engine.py talent-status <run_id>
        if len(sys.argv) < 3:
            print("Usage: engine.py talent-status <run_id>")
            sys.exit(1)
        run_id = sys.argv[2]
        try:
            print(format_talent_status(run_id))
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)

    # ── End NEO-225: Talent Ticket CLI ────────────────────────────────────────

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
