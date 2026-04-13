#!/usr/bin/env python3
"""
Ship Engine — Content Approval Queue (NEO-228)

Implements the human-in-the-loop content approval workflow described in
WORKFLOW.md Decision #16: "Content approval queue: Canvas + Telegram.
Batch per-stage. Daily digest for stragglers. Delegation via approval rules."

Architecture:
  - Queue state stored in runs/{ticket-id}/approval-queue.json per run
  - Telegram inline buttons: Approve / Reject / Preview
  - Auto-approve rules: configurable per content type (delegate to engine)
  - Daily digest: surfaces all pending approvals across all active runs
  - Batch mode: group all items from one stage into a single review message

State Machine Integration:
  - Approval-gated stages: awareness, lead-capture, nurture, closing, launch
  - Stage advance is blocked while any items in that stage are STATUS_PENDING
  - engine.py advance_stage() calls is_stage_blocked() before allowing transition
  - force=True bypasses the gate (Max override)

Telegram UX:
  - Per-item: title + preview + [✅ Approve] [❌ Reject] [👁 Full Preview] buttons
  - Batch: grouped by stage, each item gets its own approve/reject row
  - Daily digest: all pending items across all runs with stale flags

Callback data format (max 64 bytes):
  ap:{run_id[:10]}:{item_id}  → approve
  rj:{run_id[:10]}:{item_id}  → reject
  pv:{run_id[:10]}:{item_id}  → preview

Usage (CLI):
  python3 approval_queue.py submit <run_id> <stage> <item_type> <title> <preview> [content_path]
  python3 approval_queue.py approve <run_id> <item_id>
  python3 approval_queue.py reject <run_id> <item_id> [reason]
  python3 approval_queue.py pending [run_id] [--stage <stage>]
  python3 approval_queue.py batch <run_id> <stage>
  python3 approval_queue.py digest
  python3 approval_queue.py summary <run_id>
  python3 approval_queue.py rules <run_id> add <item_type> [auto-approve|require-review]
  python3 approval_queue.py rules <run_id> list
  python3 approval_queue.py callback <callback_data>
"""

import json
import os
import sys
import uuid
import time
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

# ─── Constants ────────────────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).parent
RUNS_DIR = Path(os.environ.get("SHIP_RUNS_DIR", str(_SCRIPT_DIR / "runs")))
ARCHIVE_DIR = Path(os.environ.get("SHIP_ARCHIVE_DIR", str(_SCRIPT_DIR / "archive")))

# Telegram channels
NEO_CRON_CHAT_ID = "-5154032048"   # neo-cron: approval requests & digests

# Linear API
LINEAR_TOKEN_PATH = Path(
    os.environ.get("LINEAR_TOKEN_PATH", str(Path.home() / ".clawdbot" / ".linear_token"))
)

# Approval item statuses
STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_AUTO_APPROVED = "auto-approved"

# Content types and their default review policy
# True = auto-approve (low-risk internal artifacts)
# False = require human review (public-facing content)
DEFAULT_AUTO_APPROVE = {
    # Public-facing — always require review
    "email-subject-line": False,
    "ig-caption": False,
    "ig-carousel-slide": False,
    "ig-carousel": False,
    "linkedin-post": False,
    "x-thread": False,
    "blog-post": False,
    "landing-page-copy": False,
    "email-sequence": False,
    "pricing-copy": False,
    "video-script": False,
    # Internal/technical — safe to auto-approve
    "seo-metadata": True,
    "utm-links": True,
    "analytics-setup": True,
    "draft-outline": True,
    "internal-brief": True,
}

# Stale threshold (hours before an item is flagged as stale in digest)
STALE_HOURS = 24

# ─── Queue File I/O ───────────────────────────────────────────────────────────

def _queue_path(run_id: str) -> Path:
    return RUNS_DIR / run_id / "approval-queue.json"


def _load_queue(run_id: str) -> dict:
    path = _queue_path(run_id)
    if path.exists():
        return json.loads(path.read_text())
    return {
        "run_id": run_id,
        "items": [],
        "auto_approve_rules": {},
        "digest_last_sent": None,
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
    }


def _save_queue(run_id: str, queue: dict):
    path = _queue_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    queue["updated"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(queue, indent=2))


def _all_run_ids() -> list:
    if not RUNS_DIR.exists():
        return []
    return [f.stem for f in RUNS_DIR.glob("*.json")]


# ─── Auto-Approve Logic ───────────────────────────────────────────────────────

def _should_auto_approve(item_type: str, rules: dict) -> bool:
    """Decide if an item type should be auto-approved (per-run rules take priority)."""
    if item_type in rules:
        return bool(rules[item_type])
    return DEFAULT_AUTO_APPROVE.get(item_type, False)


# ─── Telegram Notifications ───────────────────────────────────────────────────

def _linear_api_key() -> str:
    return LINEAR_TOKEN_PATH.read_text().strip()


def _send_telegram(chat_id: str, text: str, buttons: list = None) -> dict:
    """
    Send a Telegram message with optional inline keyboard.

    Tries bot token file first, falls back to openclaw CLI.
    """
    try:
        _claw_dir = Path(os.environ.get("CLAWDBOT_DIR", str(Path.home() / ".clawdbot")))
        token_path = _claw_dir / "telegram"
        bot_token = None
        for candidate in [
            token_path / "bot_token",
            token_path / "token",
            _claw_dir / ".telegram_token",
        ]:
            if candidate.exists():
                bot_token = candidate.read_text().strip()
                break

        if not bot_token:
            return _send_via_openclaw(chat_id, text, buttons)

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }
        if buttons:
            payload["reply_markup"] = json.dumps({"inline_keyboard": buttons})

        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[approval_queue] telegram send error: {e}", file=sys.stderr)
        return _send_via_openclaw(chat_id, text, buttons)


def _send_via_openclaw(chat_id: str, text: str, buttons: list = None) -> dict:
    """Fallback: use openclaw CLI to send the message."""
    try:
        args = [
            "openclaw", "message", "send",
            "--channel", "telegram",
            "--target", chat_id,
            "--message", text,
        ]
        if buttons:
            args += ["--buttons", json.dumps(buttons)]
        result = subprocess.run(args, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return {"ok": True, "result": {"message_id": None}}
    except Exception as e:
        print(f"[approval_queue] openclaw fallback error: {e}", file=sys.stderr)
    return {}


def _gql(query: str, variables: dict = None) -> dict:
    """Execute a Linear GraphQL query."""
    api_key = _linear_api_key()
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        "https://api.linear.app/graphql",
        data=data,
        headers={"Authorization": api_key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if "errors" in result:
        raise RuntimeError(f"Linear GraphQL error: {result['errors']}")
    return result.get("data", {})


# ─── Core Queue Operations ────────────────────────────────────────────────────

def submit_content(
    run_id: str,
    stage: str,
    item_type: str,
    title: str,
    preview: str,
    content_path: Optional[str] = None,
    tags: Optional[list] = None,
    notify: bool = True,
) -> dict:
    """
    Submit a content item for approval.

    If the item_type matches an auto-approve rule, it is approved immediately
    without sending a Telegram message. Otherwise it enters STATUS_PENDING and
    a Telegram message is sent with Approve / Reject / Preview inline buttons.

    Returns the queue item dict (with its assigned id and status).
    """
    queue = _load_queue(run_id)
    item_id = str(uuid.uuid4())[:8]

    item = {
        "id": item_id,
        "run_id": run_id,
        "stage": stage,
        "item_type": item_type,
        "title": title,
        "preview": preview[:800],
        "content_path": content_path,
        "tags": tags or [],
        "status": STATUS_PENDING,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "decided_at": None,
        "decided_by": None,
        "rejection_reason": None,
        "telegram_message_id": None,
    }

    if _should_auto_approve(item_type, queue.get("auto_approve_rules", {})):
        item["status"] = STATUS_AUTO_APPROVED
        item["decided_at"] = datetime.now(timezone.utc).isoformat()
        item["decided_by"] = "auto-approve-rule"
        print(f"[approval_queue] auto-approved [{item_id}] {title}")
    else:
        if notify:
            msg_id = _send_item_approval_request(item)
            item["telegram_message_id"] = msg_id
        _post_linear_approval_comment(run_id, item)

    queue["items"].append(item)
    _save_queue(run_id, queue)
    return item


def _send_item_approval_request(item: dict) -> Optional[int]:
    """
    Send a Telegram message with Approve / Reject / Preview inline buttons
    for a single content item. Returns the Telegram message_id or None.
    """
    run_id = item["run_id"]
    item_id = item["id"]
    stage = item["stage"].upper()
    item_type = item["item_type"]
    title = item["title"]
    preview = item["preview"]

    # Callback_data must be <= 64 bytes
    short_run = run_id[:10]
    approve_cb = f"ap:{short_run}:{item_id}"[:64]
    reject_cb = f"rj:{short_run}:{item_id}"[:64]
    preview_cb = f"pv:{short_run}:{item_id}"[:64]

    text = (
        f"\U0001f4cb *Content Approval Request*\n"
        f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
        f"\U0001f3f7 *Run:* `{run_id}`\n"
        f"\U0001f535 *Stage:* {stage}\n"
        f"\U0001f4c1 *Type:* `{item_type}`\n"
        f"\U0001f4dd *Title:* {title}\n\n"
        f"*Preview:*\n"
        f"```\n{preview[:500]}\n```\n"
        f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
        f"_Approve or reject before the pipeline can advance._"
    )

    buttons = [
        [
            {"text": "\u2705 Approve", "callback_data": approve_cb},
            {"text": "\u274c Reject", "callback_data": reject_cb},
        ],
        [
            {"text": "\U0001f441 Full Preview", "callback_data": preview_cb},
        ],
    ]

    resp = _send_telegram(NEO_CRON_CHAT_ID, text, buttons)
    return (resp.get("result") or {}).get("message_id")


def _post_linear_approval_comment(run_id: str, item: dict):
    """Post a pending-approval comment on the Linear stage sub-issue."""
    try:
        run_state_path = RUNS_DIR / f"{run_id}.json"
        if not run_state_path.exists():
            return
        state = json.loads(run_state_path.read_text())
        stage = item["stage"]
        sub_issues = state.get("linear", {}).get("subIssues", {})
        issue_id = (sub_issues.get(stage) or {}).get("id") or state["linear"]["parentId"]

        body = (
            f"\u23f3 **Content Approval Pending** \u2014 Item `{item['id']}`\n\n"
            f"**Type:** {item['item_type']}\n"
            f"**Title:** {item['title']}\n"
            f"**Status:** Awaiting human review via Telegram\n\n"
            f"_Stage cannot advance until this item is approved or rejected._"
        )
        _gql(
            """
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
            """,
            {"issueId": issue_id, "body": body},
        )
    except Exception as e:
        print(f"[approval_queue] linear comment error: {e}", file=sys.stderr)


def process_decision(
    run_id: str,
    item_id: str,
    decision: str,
    reason: Optional[str] = None,
    decided_by: str = "human",
) -> dict:
    """
    Record an approve or reject decision for a queue item.

    Updates the queue JSON, posts a Linear comment, and sends a Telegram
    confirmation. Returns the updated item dict.
    Raises KeyError if item_id not found in this run's queue.
    """
    queue = _load_queue(run_id)
    item = next((i for i in queue["items"] if i["id"] == item_id), None)
    if item is None:
        raise KeyError(f"Item {item_id} not found in run {run_id} approval queue")

    now = datetime.now(timezone.utc).isoformat()
    if decision == "approve":
        item["status"] = STATUS_APPROVED
        item["decided_at"] = now
        item["decided_by"] = decided_by
        status_text = "APPROVED"
        status_emoji = "\u2705"
    elif decision == "reject":
        item["status"] = STATUS_REJECTED
        item["decided_at"] = now
        item["decided_by"] = decided_by
        item["rejection_reason"] = reason or "No reason provided"
        status_text = f"REJECTED \u2014 {item['rejection_reason']}"
        status_emoji = "\u274c"
    else:
        raise ValueError(f"Invalid decision: {decision!r} (must be 'approve' or 'reject')")

    _save_queue(run_id, queue)
    _post_linear_decision_comment(run_id, item, decision, reason)

    confirm = (
        f"{status_emoji} *Decision recorded*\n"
        f"Run: `{run_id}` | Item: `{item_id}`\n"
        f"*{item['title']}* \u2192 _{status_text}_"
    )
    _send_telegram(NEO_CRON_CHAT_ID, confirm)
    return item


def _post_linear_decision_comment(run_id: str, item: dict, decision: str, reason: Optional[str]):
    """Post the approval/rejection decision back to Linear."""
    try:
        run_state_path = RUNS_DIR / f"{run_id}.json"
        if not run_state_path.exists():
            return
        state = json.loads(run_state_path.read_text())
        stage = item["stage"]
        sub_issues = state.get("linear", {}).get("subIssues", {})
        issue_id = (sub_issues.get(stage) or {}).get("id") or state["linear"]["parentId"]

        if decision == "approve":
            body = (
                f"\u2705 **Content Approved** \u2014 Item `{item['id']}`\n\n"
                f"**Type:** {item['item_type']}\n"
                f"**Title:** {item['title']}\n"
                f"**Approved by:** {item['decided_by']}\n"
                f"**At:** {item['decided_at'][:16]} UTC\n\n"
                f"_Stage may now proceed._"
            )
        else:
            body = (
                f"\u274c **Content Rejected** \u2014 Item `{item['id']}`\n\n"
                f"**Type:** {item['item_type']}\n"
                f"**Title:** {item['title']}\n"
                f"**Rejected by:** {item['decided_by']}\n"
                f"**Reason:** {reason or 'No reason provided'}\n"
                f"**At:** {item['decided_at'][:16]} UTC\n\n"
                f"_Content must be revised and resubmitted._"
            )
        _gql(
            """
            mutation($issueId: String!, $body: String!) {
                commentCreate(input: { issueId: $issueId, body: $body }) {
                    comment { id }
                }
            }
            """,
            {"issueId": issue_id, "body": body},
        )
    except Exception as e:
        print(f"[approval_queue] linear decision comment error: {e}", file=sys.stderr)


# ─── Batch & Digest ───────────────────────────────────────────────────────────

def send_batch_for_stage(run_id: str, stage: str) -> list:
    """
    Send a single batched Telegram message for all pending items in a stage.

    Sends one message with inline approve/reject buttons for each item.
    Returns the list of items included in the batch.
    """
    queue = _load_queue(run_id)
    pending = [
        i for i in queue["items"]
        if i["stage"] == stage and i["status"] == STATUS_PENDING
    ]
    if not pending:
        print(f"[approval_queue] no pending items for {run_id}/{stage}")
        return []

    lines = [
        f"\U0001f4e6 *Content Batch \u2014 {stage.upper()}*",
        f"Run: `{run_id}` | {len(pending)} item(s) awaiting approval",
        "\u2501" * 20,
    ]
    buttons = []

    for idx, item in enumerate(pending, 1):
        item_id = item["id"]
        short_run = run_id[:10]
        approve_cb = f"ap:{short_run}:{item_id}"[:64]
        reject_cb = f"rj:{short_run}:{item_id}"[:64]

        lines.append(f"\n*{idx}. {item['title']}*")
        lines.append(f"   Type: `{item['item_type']}`")
        if item["preview"]:
            snippet = item["preview"][:120].replace("\n", " ")
            lines.append(f"   _{snippet}..._")

        buttons.append([
            {"text": f"\u2705 #{idx} Approve", "callback_data": approve_cb},
            {"text": f"\u274c #{idx} Reject", "callback_data": reject_cb},
        ])

    lines.append("\n" + "\u2501" * 20)
    lines.append("_Approve or reject each item to unblock the pipeline._")

    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:3990] + "\n_...(truncated)_"

    resp = _send_telegram(NEO_CRON_CHAT_ID, text, buttons)
    msg_id = (resp.get("result") or {}).get("message_id")

    for item in pending:
        item["telegram_message_id"] = msg_id
    _save_queue(run_id, queue)
    return pending


def send_daily_digest(target_chat_id: str = NEO_CRON_CHAT_ID) -> dict:
    """
    Send a daily digest of all pending content approvals across all active runs.

    Skips items pending < 1 hour (too fresh). Flags items pending > STALE_HOURS.
    Returns a summary dict: {pending, stale, runs}.
    """
    now = datetime.now(timezone.utc)
    cutoff_1h = now - timedelta(hours=1)
    cutoff_stale = now - timedelta(hours=STALE_HOURS)

    all_pending = []
    stale_count = 0

    for run_id in _all_run_ids():
        queue = _load_queue(run_id)
        for item in queue["items"]:
            if item["status"] != STATUS_PENDING:
                continue
            submitted = datetime.fromisoformat(item["submitted_at"])
            if submitted > cutoff_1h:
                continue
            all_pending.append((run_id, item, submitted))
            if submitted < cutoff_stale:
                stale_count += 1

    if not all_pending:
        _send_telegram(
            target_chat_id,
            "\u2705 *Daily Digest* \u2014 No pending content approvals. All clear!"
        )
        return {"pending": 0, "stale": 0, "runs": []}

    by_run: dict = {}
    for run_id, item, submitted in all_pending:
        by_run.setdefault(run_id, []).append((item, submitted))

    lines = [
        f"\U0001f4ec *Daily Approval Digest*",
        f"{len(all_pending)} pending \u2022 {stale_count} stale (>{STALE_HOURS}h)",
        "\u2501" * 20,
    ]
    buttons = []

    for run_id, items_and_times in by_run.items():
        lines.append(f"\n\U0001f3f7 *Run `{run_id}`* ({len(items_and_times)} pending)")
        for item, submitted in items_and_times:
            age_h = (now - submitted).total_seconds() / 3600
            stale_flag = " \U0001f534 STALE" if age_h >= STALE_HOURS else ""
            lines.append(f"  \u2022 {item['title']} [{item['stage']}] \u2014 {age_h:.0f}h ago{stale_flag}")

            item_id = item["id"]
            short_run = run_id[:10]
            approve_cb = f"ap:{short_run}:{item_id}"[:64]
            reject_cb = f"rj:{short_run}:{item_id}"[:64]
            buttons.append([
                {"text": f"\u2705 {item['title'][:20]}", "callback_data": approve_cb},
                {"text": f"\u274c Reject", "callback_data": reject_cb},
            ])

    lines.append("\n" + "\u2501" * 20)
    lines.append("_Use buttons or:_ `engine.py approve-item <run_id> <item_id>`")

    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:3990] + "\n_...(truncated \u2014 use CLI to see all)_"

    _send_telegram(target_chat_id, text, buttons[:10])

    for run_id in by_run:
        queue = _load_queue(run_id)
        queue["digest_last_sent"] = now.isoformat()
        _save_queue(run_id, queue)

    return {
        "pending": len(all_pending),
        "stale": stale_count,
        "runs": list(by_run.keys()),
    }


# ─── Auto-Approve Rule Management ────────────────────────────────────────────

def set_auto_approve_rule(run_id: str, item_type: str, auto_approve: bool):
    """Set a per-run auto-approve rule for a content type."""
    queue = _load_queue(run_id)
    queue.setdefault("auto_approve_rules", {})[item_type] = auto_approve
    _save_queue(run_id, queue)
    policy = "auto-approve" if auto_approve else "require-review"
    print(f"[approval_queue] rule set: {item_type} -> {policy} (run: {run_id})")


def get_pending_items(run_id: Optional[str] = None, stage: Optional[str] = None) -> list:
    """Get all pending approval items, optionally filtered by run and/or stage."""
    results = []
    run_ids = [run_id] if run_id else _all_run_ids()
    for rid in run_ids:
        queue = _load_queue(rid)
        for item in queue["items"]:
            if item["status"] == STATUS_PENDING:
                if stage and item["stage"] != stage:
                    continue
                results.append(item)
    return results


def is_stage_blocked(run_id: str, stage: str) -> bool:
    """
    Returns True if the stage has any pending (unresolved) approval items.
    engine.py advance_stage() calls this before allowing a transition.
    """
    return len(get_pending_items(run_id, stage)) > 0


def get_queue_summary(run_id: str) -> dict:
    """Return a summary of queue state for a run."""
    queue = _load_queue(run_id)
    items = queue.get("items", [])
    summary = {
        "total": len(items),
        "pending": sum(1 for i in items if i["status"] == STATUS_PENDING),
        "approved": sum(1 for i in items if i["status"] == STATUS_APPROVED),
        "rejected": sum(1 for i in items if i["status"] == STATUS_REJECTED),
        "auto_approved": sum(1 for i in items if i["status"] == STATUS_AUTO_APPROVED),
        "by_stage": {},
    }
    for item in items:
        s = item["stage"]
        entry = summary["by_stage"].setdefault(s, {"pending": 0, "approved": 0, "rejected": 0})
        if item["status"] == STATUS_PENDING:
            entry["pending"] += 1
        elif item["status"] in (STATUS_APPROVED, STATUS_AUTO_APPROVED):
            entry["approved"] += 1
        elif item["status"] == STATUS_REJECTED:
            entry["rejected"] += 1
    return summary


# ─── Callback Parsing (for webhook integration) ───────────────────────────────

def parse_callback(callback_data: str) -> Optional[dict]:
    """
    Parse a Telegram callback_data string into an action dict.

    Returns None if format doesn't match ap:/rj:/pv: pattern.
    """
    parts = callback_data.split(":")
    if len(parts) != 3:
        return None
    action_code, run_id_short, item_id = parts
    action_map = {"ap": "approve", "rj": "reject", "pv": "preview"}
    action = action_map.get(action_code)
    if not action:
        return None
    return {"action": action, "run_id_short": run_id_short, "item_id": item_id}


def resolve_run_id(run_id_short: str) -> Optional[str]:
    """Find the full run_id from its first-10-char prefix."""
    for rid in _all_run_ids():
        if rid[:10] == run_id_short or rid.startswith(run_id_short):
            return rid
    return None


def handle_callback(callback_data: str, decided_by: str = "telegram-button") -> Optional[dict]:
    """
    Handle a Telegram inline button callback.

    Called by the webhook handler when a callback_query arrives.
    Returns the updated item dict, or None if not recognized.
    """
    parsed = parse_callback(callback_data)
    if parsed is None:
        return None

    action = parsed["action"]
    run_id = resolve_run_id(parsed["run_id_short"])
    if not run_id:
        print(f"[approval_queue] cannot resolve run: {parsed['run_id_short']}", file=sys.stderr)
        return None

    item_id = parsed["item_id"]

    if action == "approve":
        return process_decision(run_id, item_id, "approve", decided_by=decided_by)
    elif action == "reject":
        _send_telegram(
            NEO_CRON_CHAT_ID,
            f"\u274c Rejection recorded for `{item_id}` (run: `{run_id}`)\n"
            f"Add reason: `engine.py reject-item {run_id} {item_id} \"reason\"`",
        )
        return process_decision(
            run_id, item_id, "reject",
            reason="Rejected via Telegram button",
            decided_by=decided_by,
        )
    elif action == "preview":
        queue = _load_queue(run_id)
        item = next((i for i in queue["items"] if i["id"] == item_id), None)
        if item:
            preview_text = (
                f"\U0001f441 *Full Preview*\n"
                f"Run: `{run_id}` | Item: `{item_id}`\n"
                f"Title: {item['title']}\n"
                f"Path: `{item.get('content_path', 'N/A')}`\n\n"
                f"```\n{item['preview']}\n```"
            )
            if len(preview_text) > 4000:
                preview_text = preview_text[:3990] + "\n\u2026```"
            _send_telegram(NEO_CRON_CHAT_ID, preview_text)
        return item

    return None


# ─── CLI Interface ────────────────────────────────────────────────────────────

def _print_item(item: dict):
    icons = {
        STATUS_PENDING: "\u23f3",
        STATUS_APPROVED: "\u2705",
        STATUS_REJECTED: "\u274c",
        STATUS_AUTO_APPROVED: "\U0001f916",
    }
    icon = icons.get(item["status"], "?")
    age = ""
    if item.get("submitted_at"):
        delta = datetime.now(timezone.utc) - datetime.fromisoformat(item["submitted_at"])
        age = f"{delta.total_seconds()/3600:.0f}h ago"
    print(f"  {icon} [{item['id']}] {item['title']} ({item['item_type']}) — {item['stage']} — {age}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "submit":
        if len(args) < 6:
            print("Usage: approval_queue.py submit <run_id> <stage> <item_type> <title> <preview> [content_path]")
            sys.exit(1)
        run_id, stage, item_type, title, preview = args[1], args[2], args[3], args[4], args[5]
        content_path = args[6] if len(args) > 6 else None
        item = submit_content(run_id, stage, item_type, title, preview, content_path)
        status_text = "Auto-approved" if item["status"] == STATUS_AUTO_APPROVED else "Submitted for approval"
        print(f"[{item['id']}] {status_text}: {title}")

    elif cmd == "approve":
        if len(args) < 3:
            print("Usage: approval_queue.py approve <run_id> <item_id>")
            sys.exit(1)
        item = process_decision(args[1], args[2], "approve")
        print(f"\u2705 Approved: [{item['id']}] {item['title']}")

    elif cmd == "reject":
        if len(args) < 3:
            print("Usage: approval_queue.py reject <run_id> <item_id> [reason]")
            sys.exit(1)
        reason = args[3] if len(args) > 3 else "No reason provided"
        item = process_decision(args[1], args[2], "reject", reason=reason)
        print(f"\u274c Rejected: [{item['id']}] {item['title']}")

    elif cmd == "pending":
        run_id = None
        stage = None
        i = 1
        while i < len(args):
            if args[i] == "--stage" and i + 1 < len(args):
                stage = args[i + 1]
                i += 2
            elif not run_id and not args[i].startswith("-"):
                run_id = args[i]
                i += 1
            else:
                i += 1
        items = get_pending_items(run_id, stage)
        if not items:
            print("\u2705 No pending approval items.")
        else:
            print(f"\u23f3 {len(items)} pending item(s):")
            for item in items:
                _print_item(item)

    elif cmd == "batch":
        if len(args) < 3:
            print("Usage: approval_queue.py batch <run_id> <stage>")
            sys.exit(1)
        items = send_batch_for_stage(args[1], args[2])
        print(f"\U0001f4e6 Batch sent: {len(items)} item(s)")

    elif cmd == "digest":
        result = send_daily_digest()
        print(f"\U0001f4ec Digest: {result['pending']} pending, {result['stale']} stale, {len(result['runs'])} run(s)")

    elif cmd == "summary":
        if len(args) < 2:
            print("Usage: approval_queue.py summary <run_id>")
            sys.exit(1)
        s = get_queue_summary(args[1])
        print(f"\U0001f4ca Queue — {args[1]}")
        print(f"  Pending:       {s['pending']}")
        print(f"  Approved:      {s['approved']}")
        print(f"  Rejected:      {s['rejected']}")
        print(f"  Auto-approved: {s['auto_approved']}")
        print(f"  Total:         {s['total']}")
        if s["by_stage"]:
            print("  By stage:")
            for stage_name, counts in s["by_stage"].items():
                print(f"    {stage_name}: \u2705{counts['approved']} \u23f3{counts['pending']} \u274c{counts['rejected']}")

    elif cmd == "rules":
        if len(args) < 3:
            print("Usage: approval_queue.py rules <run_id> list")
            print("       approval_queue.py rules <run_id> add <item_type> [auto-approve|require-review]")
            sys.exit(1)
        run_id = args[1]
        sub = args[2]
        if sub == "list":
            queue = _load_queue(run_id)
            rules = queue.get("auto_approve_rules", {})
            effective = {**DEFAULT_AUTO_APPROVE, **rules}
            print(f"\U0001f4cb Rules for {run_id}:")
            for itype, auto in sorted(effective.items()):
                source = "(run override)" if itype in rules else "(default)"
                policy = "\U0001f916 auto-approve" if auto else "\U0001f441 require-review"
                print(f"  {itype}: {policy} {source}")
        elif sub == "add":
            if len(args) < 4:
                print("Usage: approval_queue.py rules <run_id> add <item_type> [auto-approve|require-review]")
                sys.exit(1)
            item_type = args[3]
            policy = args[4] if len(args) > 4 else "require-review"
            set_auto_approve_rule(run_id, item_type, policy == "auto-approve")
        else:
            print(f"Unknown rules sub-command: {sub}")
            sys.exit(1)

    elif cmd == "callback":
        if len(args) < 2:
            print("Usage: approval_queue.py callback <callback_data>")
            sys.exit(1)
        result = handle_callback(args[1])
        if result:
            print(f"\u2705 Callback handled: {result.get('status')} for {result.get('id')}")
        else:
            print(f"Warning: callback not recognized: {args[1]}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
