#!/usr/bin/env python3
"""
Tests for NEO-186: Event-Driven Architecture

Run with: python3 -m pytest skills/ship-engine/tests/test_event_driven.py -v
"""

import copy
import json
import sys
import tempfile
import importlib.util
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

# ── Bootstrap: import engine from file path (works regardless of package name) ──
_ENGINE_PATH = Path(__file__).parent.parent / "engine.py"

_tmp_dir = tempfile.mkdtemp()
_tmp_runs = Path(_tmp_dir) / "runs"
_tmp_runs.mkdir()
_tmp_archive = Path(_tmp_dir) / "archive"
_tmp_archive.mkdir()
_tmp_learnings = Path(_tmp_dir) / "LEARNINGS.md"

_orig_open = open


def _mock_open(path, *args, **kwargs):
    """Stub reads of .linear_token so engine module loads without credentials."""
    if ".linear_token" in str(path):
        m = MagicMock()
        m.__enter__ = lambda s: s
        m.__exit__ = MagicMock(return_value=False)
        m.read = MagicMock(return_value="fake-linear-token")
        return m
    return _orig_open(path, *args, **kwargs)


with patch("builtins.open", side_effect=_mock_open):
    spec = importlib.util.spec_from_file_location("engine", _ENGINE_PATH)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)

# Redirect to temp dirs
engine.RUNS_DIR = _tmp_runs
engine.ARCHIVE_DIR = _tmp_archive
engine.LEARNINGS_PATH = _tmp_learnings

# Stub gql (patched per test, but also set a safe global default)
engine.gql = MagicMock(return_value={})

# ── Test helpers ─────────────────────────────────────────────────────────────
_TEST_RUN_ID = "TEST-EVT-001"

_BASE_STATE = {
    "ticket": _TEST_RUN_ID,
    "name": "Test Product",
    "stage": "validate",
    "created": "2026-02-26T00:00:00+00:00",
    "updated": "2026-02-26T00:00:00+00:00",
    "linear": {
        "projectId": "fake-project",
        "parentId": "fake-parent-uuid",
        "parentIdentifier": _TEST_RUN_ID,
        "subIssues": {
            "validate":    {"id": "fake-validate-uuid",  "identifier": "TEST-EVT-002"},
            "strategy":    {"id": "fake-strategy-uuid",  "identifier": "TEST-EVT-003"},
            "awareness":   {"id": "fake-awareness-uuid", "identifier": "TEST-EVT-004"},
            "lead-capture":{"id": "fake-leadcap-uuid",   "identifier": "TEST-EVT-005"},
            "nurture":     {"id": "fake-nurture-uuid",   "identifier": "TEST-EVT-006"},
            "closing":     {"id": "fake-closing-uuid",   "identifier": "TEST-EVT-007"},
            "launch":      {"id": "fake-launch-uuid",    "identifier": "TEST-EVT-008"},
            "measure":     {"id": "fake-measure-uuid",   "identifier": "TEST-EVT-009"},
        },
    },
    "approvals": {},
    "budget": {"estimated": 0, "approved": None, "spent": 0, "currency": "USD"},
    "outputs": {
        "validation_report": None,
        "icp": None,
        "ship_plan": None,
        "launch_checklist": None,
        "post_launch_report": None,
    },
    "delegations": {},
    "blackboard": {},
    "errors": [],
    "decision": None,
    "urgency": "standard",
}


def _write_state(state=None, run_id=_TEST_RUN_ID):
    s = copy.deepcopy(state or _BASE_STATE)
    s["ticket"] = run_id
    (_tmp_runs / f"{run_id}.json").write_text(json.dumps(s))
    return s


def _read_state(run_id=_TEST_RUN_ID):
    return json.loads((_tmp_runs / f"{run_id}.json").read_text())


def setup_function():
    """Reset test state before each test."""
    _write_state()
    engine.gql.reset_mock()


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestValidEvents:
    """VALID_EVENTS constant has exactly the 4 required events."""

    def test_all_four_events_defined(self):
        assert "stage_complete" in engine.VALID_EVENTS
        assert "approval_received" in engine.VALID_EVENTS
        assert "blocked" in engine.VALID_EVENTS
        assert "timeout" in engine.VALID_EVENTS

    def test_no_extra_events(self):
        assert len(engine.VALID_EVENTS) == 4

    def test_descriptions_not_empty(self):
        for evt, desc in engine.VALID_EVENTS.items():
            assert desc, f"Event '{evt}' has empty description"


class TestNextStageMap:
    """NEXT_STAGE_MAP covers the full pipeline."""

    def test_validate_leads_to_awaiting(self):
        assert engine.NEXT_STAGE_MAP["validate"] == "awaiting-validate-approval"

    def test_awaiting_validate_leads_to_strategy(self):
        assert engine.NEXT_STAGE_MAP["awaiting-validate-approval"] == "strategy"

    def test_strategy_fans_out_to_parallel(self):
        next_stage = engine.NEXT_STAGE_MAP["strategy"]
        assert isinstance(next_stage, list)
        assert "awareness" in next_stage
        assert "lead-capture" in next_stage

    def test_measure_leads_to_done(self):
        assert engine.NEXT_STAGE_MAP["measure"] == "done"


class TestDispatchEventUnknown:
    """dispatch_event raises ValueError for unknown event types."""

    def test_unknown_event_raises(self):
        import pytest
        with pytest.raises(ValueError, match="Unknown event type"):
            engine.dispatch_event(_TEST_RUN_ID, "not_a_real_event")

    def test_missing_run_raises(self):
        import pytest
        with pytest.raises(FileNotFoundError):
            engine.dispatch_event("NONEXISTENT-999", "stage_complete")


class TestStageComplete:
    """stage_complete event: quality gate + advance."""

    def test_stage_complete_force_advances_strategy(self):
        """With force=True at strategy stage, run fans out to parallel."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "strategy"
        _write_state(state)

        with patch.object(engine, "start_parallel", return_value=state) as mock_par, \
             patch.object(engine, "_post_event_comment", return_value=True):

            result = engine.dispatch_event(
                _TEST_RUN_ID,
                "stage_complete",
                {"force": True, "notes": "Approved by test"},
            )

        assert result["event"] == "stage_complete"
        assert result["advanced_to"].startswith("parallel(")
        mock_par.assert_called_once()

    def test_stage_complete_validate_moves_to_awaiting(self):
        """validate → stage_complete should set stage to awaiting-validate-approval."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "validate"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(
                _TEST_RUN_ID,
                "stage_complete",
                {"force": True},
            )

        assert result["advanced_to"] == "awaiting-validate-approval"
        saved = _read_state()
        assert saved["stage"] == "awaiting-validate-approval"
        assert "awaiting_since" in saved

    def test_stage_complete_event_logged(self):
        """dispatch_event appends to event_log."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "measure"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True), \
             patch.object(engine, "extract_lessons", return_value=""):

            engine.dispatch_event(
                _TEST_RUN_ID,
                "stage_complete",
                {"force": True},
            )

        saved = _read_state()
        assert "event_log" in saved
        assert len(saved["event_log"]) >= 1
        assert saved["event_log"][0]["event"] == "stage_complete"

    def test_stage_complete_result_has_verdict(self):
        """Result dict always contains a 'verdict' key."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "validate"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "stage_complete", {"force": True})

        assert "verdict" in result

    def test_stage_complete_result_has_run_id(self):
        """Result dict contains run_id and timestamp."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "validate"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "stage_complete", {"force": True})

        assert result["run_id"] == _TEST_RUN_ID
        assert "timestamp" in result


class TestApprovalReceived:
    """approval_received event: records approval + unblocks pipeline."""

    def test_approval_received_unblocks_awaiting(self):
        """Approval received while awaiting should advance to next stage."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
        _write_state(state)

        with patch.object(engine, "advance_stage", return_value=state) as mock_adv, \
             patch.object(engine, "_post_event_comment", return_value=True):

            result = engine.dispatch_event(
                _TEST_RUN_ID,
                "approval_received",
                {"gate": "validate", "approver": "Max", "notes": "LGTM"},
            )

        assert result["event"] == "approval_received"
        assert result["verdict"] == "approved"
        assert result["advanced_to"] is not None
        mock_adv.assert_called_once()

    def test_approval_received_records_in_state(self):
        """Approval is stored in state['approvals']."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
        _write_state(state)

        with patch.object(engine, "advance_stage", return_value=state), \
             patch.object(engine, "_post_event_comment", return_value=True):

            engine.dispatch_event(
                _TEST_RUN_ID,
                "approval_received",
                {"gate": "validate", "approver": "Max"},
            )

        saved = _read_state()
        assert "validate" in saved["approvals"]
        assert saved["approvals"]["validate"]["approver"] == "Max"
        assert saved["approvals"]["validate"]["verdict"] == "approved"

    def test_rejection_returns_to_previous_stage(self):
        """Rejected approval sends run back to the stage for revision."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(
                _TEST_RUN_ID,
                "approval_received",
                {"gate": "validate", "verdict": "rejected", "notes": "Needs more VoC"},
            )

        assert result["verdict"] == "rejected"
        saved = _read_state()
        # Stage should be reverted to 'validate'
        assert saved["stage"] == "validate"
        # awaiting_since should be cleared
        assert "awaiting_since" not in saved

    def test_approval_clears_awaiting_since(self):
        """Successful approval clears awaiting_since from state."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = "2026-02-20T00:00:00+00:00"
        _write_state(state)

        with patch.object(engine, "advance_stage", return_value=state), \
             patch.object(engine, "_post_event_comment", return_value=True):

            engine.dispatch_event(
                _TEST_RUN_ID,
                "approval_received",
                {"gate": "validate"},
            )

        saved = _read_state()
        assert "awaiting_since" not in saved

    def test_approval_default_approver_is_max(self):
        """Default approver is 'Max' when not specified."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
        _write_state(state)

        with patch.object(engine, "advance_stage", return_value=state), \
             patch.object(engine, "_post_event_comment", return_value=True):

            engine.dispatch_event(
                _TEST_RUN_ID,
                "approval_received",
                {"gate": "validate"},
            )

        saved = _read_state()
        assert saved["approvals"]["validate"]["approver"] == "Max"


class TestBlocked:
    """blocked event: records block, sets awaiting state, posts comment."""

    def test_blocked_sets_awaiting_stage(self):
        """blocked event should set stage to awaiting-{current_stage}."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "nurture"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(
                _TEST_RUN_ID,
                "blocked",
                {"reason": "Need MailerLite API key"},
            )

        assert result["event"] == "blocked"
        assert result["stage"] == "nurture"
        saved = _read_state()
        assert saved["stage"] == "awaiting-nurture"
        assert "awaiting_since" in saved

    def test_blocked_records_reason(self):
        """blocked event records reason in state['blocks'] list."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "closing"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(
                _TEST_RUN_ID,
                "blocked",
                {"reason": "Stripe account needed", "needs": "Stripe secret key from Max"},
            )

        saved = _read_state()
        assert "blocks" in saved
        assert len(saved["blocks"]) == 1
        assert saved["blocks"][0]["reason"] == "Stripe account needed"
        assert saved["blocks"][0]["needs"] == "Stripe secret key from Max"

    def test_blocked_sets_urgency_if_provided(self):
        """blocked event applies urgency preset when provided."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awareness"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(
                _TEST_RUN_ID,
                "blocked",
                {"reason": "Urgent: launch delay risk", "urgency": "urgent"},
            )

        saved = _read_state()
        assert saved["urgency"] == "urgent"

    def test_blocked_multiple_blocks_accumulated(self):
        """Multiple blocked events accumulate in the blocks list."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "launch"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(_TEST_RUN_ID, "blocked", {"reason": "Block 1"})

        # Reset stage to allow second block
        s = _read_state()
        s["stage"] = "launch"
        _write_state(s)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(_TEST_RUN_ID, "blocked", {"reason": "Block 2"})

        saved = _read_state()
        assert len(saved["blocks"]) == 2

    def test_blocked_no_reason_still_records(self):
        """blocked event without reason payload still records with default text."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "strategy"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "blocked", {})

        saved = _read_state()
        assert "blocks" in saved
        assert saved["blocks"][0]["reason"]  # not empty


class TestTimeout:
    """timeout event: evaluates elapsed time and takes action."""

    def _state_awaiting(self, hours_ago: float, urgency: str = "standard"):
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        since = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
        state["awaiting_since"] = since.isoformat()
        state["urgency"] = urgency  # standard: reminder=24h, escalation=48h, pause=72h
        return state

    def test_timeout_no_action_before_threshold(self):
        """No action taken if elapsed < reminder threshold."""
        _write_state(self._state_awaiting(hours_ago=1.0))

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        assert result["action_taken"] == "no_action"

    def test_timeout_reminder_at_24h(self):
        """Reminder action at >= 24h (standard urgency)."""
        _write_state(self._state_awaiting(hours_ago=25.0))

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        assert result["action_taken"] == "reminder"
        assert result["elapsed_hours"] >= 24.0

    def test_timeout_escalation_at_48h(self):
        """Escalation action at >= 48h (standard urgency)."""
        _write_state(self._state_awaiting(hours_ago=50.0))

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        assert result["action_taken"] == "escalation"

    def test_timeout_pause_at_72h(self):
        """Auto-pause at >= 72h (standard urgency). Stage becomes 'paused'."""
        _write_state(self._state_awaiting(hours_ago=75.0))

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        assert result["action_taken"] == "pause"
        saved = _read_state()
        assert saved["stage"] == "paused"
        assert saved.get("paused_from") == "awaiting-validate-approval"

    def test_timeout_force_action_reminder(self):
        """force_action=reminder bypasses threshold check."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()  # just now
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(
                _TEST_RUN_ID, "timeout", {"force_action": "reminder"}
            )

        assert result["action_taken"] == "reminder"

    def test_timeout_skipped_if_not_awaiting(self):
        """No awaiting_since → timeout is skipped (run not in approval state)."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "strategy"
        # No awaiting_since
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        assert result["action_taken"] == "skipped"

    def test_timeout_fast_urgency_has_lower_thresholds(self):
        """Fast urgency triggers reminder at 12h instead of 24h."""
        _write_state(self._state_awaiting(hours_ago=13.0, urgency="fast"))

        with patch.object(engine, "_post_event_comment", return_value=True):
            result = engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        # 13h > 12h (fast reminder threshold)
        assert result["action_taken"] in ("reminder", "escalation", "pause")


class TestEventLog:
    """Event log is correctly maintained across multiple events."""

    def test_event_log_accumulates(self):
        """Multiple events are all recorded in event_log."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "validate"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(_TEST_RUN_ID, "stage_complete", {"force": True})

        s = _read_state()
        s["stage"] = "awaiting-validate-approval"
        s["awaiting_since"] = datetime.now(timezone.utc).isoformat()
        _write_state(s)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        saved = _read_state()
        event_types = [e["event"] for e in saved.get("event_log", [])]
        assert "stage_complete" in event_types
        assert "timeout" in event_types

    def test_event_log_has_timestamps(self):
        """Each event log entry has a timestamp."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "awaiting-validate-approval"
        state["awaiting_since"] = datetime.now(timezone.utc).isoformat()
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(_TEST_RUN_ID, "timeout", {})

        saved = _read_state()
        for entry in saved.get("event_log", []):
            assert "timestamp" in entry
            datetime.fromisoformat(entry["timestamp"])  # valid ISO string

    def test_event_log_has_payload(self):
        """Event log stores the payload for each event."""
        state = copy.deepcopy(_BASE_STATE)
        state["stage"] = "closing"
        _write_state(state)

        with patch.object(engine, "_post_event_comment", return_value=True):
            engine.dispatch_event(
                _TEST_RUN_ID, "blocked", {"reason": "Test block", "needs": "API key"}
            )

        saved = _read_state()
        blocked_entries = [e for e in saved.get("event_log", []) if e["event"] == "blocked"]
        assert len(blocked_entries) >= 1
        assert blocked_entries[0]["payload"]["reason"] == "Test block"


class TestHelpers:
    """Helper functions work correctly."""

    def test_resolve_issue_id_returns_sub_issue(self):
        """_resolve_issue_id returns sub-issue ID for known stage."""
        _write_state()
        state = engine.load_run(_TEST_RUN_ID)
        issue_id = engine._resolve_issue_id(state, "validate")
        assert issue_id == "fake-validate-uuid"

    def test_resolve_issue_id_falls_back_to_parent(self):
        """_resolve_issue_id returns parent ID for unknown stage."""
        _write_state()
        state = engine.load_run(_TEST_RUN_ID)
        issue_id = engine._resolve_issue_id(state, "unknown-stage")
        assert issue_id == "fake-parent-uuid"

    def test_log_event_appends(self):
        """_log_event appends correctly and initialises list if missing."""
        state = copy.deepcopy(_BASE_STATE)
        assert "event_log" not in state
        engine._log_event(state, "test_event", {"a": 1}, {"result": "ok"})
        assert "event_log" in state
        assert len(state["event_log"]) == 1
        assert state["event_log"][0]["event"] == "test_event"
        assert state["event_log"][0]["payload"] == {"a": 1}

    def test_log_event_second_call_appends(self):
        """_log_event appends a second entry without overwriting the first."""
        state = copy.deepcopy(_BASE_STATE)
        engine._log_event(state, "event_one", {}, {})
        engine._log_event(state, "event_two", {}, {})
        assert len(state["event_log"]) == 2


# ── Run directly ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--tb=short"])
