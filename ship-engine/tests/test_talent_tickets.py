#!/usr/bin/env python3
"""Tests for NEO-225: Talent Ticket System."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

# Patch Linear API so tests never make real network calls
def _mock_gql(query, variables=None, **_):
    """Fake Linear API — returns minimal valid shapes."""
    if "issueCreate" in query:
        return {"issueCreate": {"issue": {"id": "mock-id-123", "identifier": "NEO-TEST", "title": "test", "url": "https://linear.app/test"}}}
    if "issueUpdate" in query:
        return {"issueUpdate": {"issue": {"id": "mock-id-123"}}}
    if "commentCreate" in query:
        return {"commentCreate": {"comment": {"id": "comment-123", "url": "https://linear.app/comment/123"}}}
    if "projectCreate" in query:
        return {"projectCreate": {"success": True, "project": {"id": "proj-123", "name": "Ship: Test", "url": ""}}}
    return {}

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import importlib.util
ENGINE_PATH = Path(__file__).parent.parent / "engine.py"
spec = importlib.util.spec_from_file_location("engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
# Patch gql before loading
engine_globals = {}


def _build_engine():
    """Import engine with gql patched to avoid network calls."""
    spec = importlib.util.spec_from_file_location("engine", ENGINE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.gql = _mock_gql
    return mod


ENG = _build_engine()


def _make_tmp_run(tmp_dir: Path, ticket: str = "MAX-999", stage: str = "awareness") -> dict:
    """Create a minimal run state file and directory for testing."""
    ENG.RUNS_DIR = tmp_dir
    run_dir = tmp_dir / ticket
    run_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "ticket": ticket,
        "name": "Test Product",
        "idea": "A test product",
        "stage": stage,
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "linear": {
            "projectId": "proj-123",
            "parentId": "parent-id-123",
            "parentIdentifier": ticket,
            "subIssues": {
                "awareness": {"id": "sub-id-awareness", "identifier": f"{ticket}-2"},
            },
        },
        "outputs": {},
        "blackboard": {},
        "talent_tickets": {},
        "errors": [],
    }
    state_path = tmp_dir / f"{ticket}.json"
    state_path.write_text(json.dumps(state, indent=2))
    return state


class TestTalentTicketCreate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp)
        ENG.RUNS_DIR = self.tmp_path
        _make_tmp_run(self.tmp_path)

    def test_creates_ticket_record_in_state(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record 60s reel about product pain",
            brief="Hook: start with pain",
            ai_placeholder="[AI SCRIPT HERE]",
        )
        state = ENG.load_run("MAX-999")
        self.assertIn(result["talent_id"], state["talent_tickets"])

    def test_ticket_has_correct_stage_and_type(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "demo_recording",
            "Record product demo",
        )
        state = ENG.load_run("MAX-999")
        ticket = state["talent_tickets"][result["talent_id"]]
        self.assertEqual(ticket["stage"], "awareness")
        self.assertEqual(ticket["deliverable_type"], "demo_recording")
        self.assertEqual(ticket["status"], "pending")

    def test_ai_placeholder_written_to_blackboard(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record reel",
            ai_placeholder="This is the AI placeholder content",
        )
        state = ENG.load_run("MAX-999")
        bb_key = result["blackboard_key"]
        self.assertEqual(state["blackboard"][bb_key], "This is the AI placeholder content")

    def test_fallback_placeholder_when_none_given(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record reel",
            ai_placeholder="",
        )
        state = ENG.load_run("MAX-999")
        bb_key = result["blackboard_key"]
        self.assertIn("AI_PLACEHOLDER", state["blackboard"][bb_key])

    def test_returns_telegram_text(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record 60s reel",
        )
        self.assertIn("Talent ticket created", result["telegram_text"])
        self.assertIn("MAX-999", result["telegram_text"])
        self.assertEqual(result["telegram_group"], ENG.TELEGRAM_MAX_GROUP)

    def test_status_written_to_blackboard(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record reel",
        )
        state = ENG.load_run("MAX-999")
        status_key = f"talent.{result['talent_id']}.status"
        self.assertEqual(state["blackboard"][status_key], "pending")

    def test_linear_issue_details_stored(self):
        result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record reel",
        )
        state = ENG.load_run("MAX-999")
        ticket = state["talent_tickets"][result["talent_id"]]
        self.assertEqual(ticket["linear_issue_id"], "mock-id-123")
        self.assertEqual(ticket["linear_identifier"], "NEO-TEST")

    def test_multiple_tickets_coexist(self):
        r1 = ENG.create_talent_ticket("MAX-999", "awareness", "reel_script", "Reel 1")
        r2 = ENG.create_talent_ticket("MAX-999", "awareness", "demo_recording", "Demo")
        state = ENG.load_run("MAX-999")
        self.assertEqual(len(state["talent_tickets"]), 2)
        self.assertIn(r1["talent_id"], state["talent_tickets"])
        self.assertIn(r2["talent_id"], state["talent_tickets"])


class TestTalentTicketResolve(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp)
        ENG.RUNS_DIR = self.tmp_path
        _make_tmp_run(self.tmp_path)
        # Create a talent ticket to work with
        self.result = ENG.create_talent_ticket(
            "MAX-999", "awareness", "reel_script",
            "Record 60s reel",
            ai_placeholder="[AI PLACEHOLDER]",
        )
        self.talent_id = self.result["talent_id"]

    def test_swap_updates_blackboard(self):
        artifact = "https://drive.google.com/file/d/real-asset"
        ENG.resolve_talent_ticket("MAX-999", self.talent_id, artifact)
        state = ENG.load_run("MAX-999")
        bb_key = self.result["blackboard_key"]
        self.assertEqual(state["blackboard"][bb_key], artifact)

    def test_swap_updates_ticket_status(self):
        artifact = "https://drive.google.com/file/d/real-asset"
        ENG.resolve_talent_ticket("MAX-999", self.talent_id, artifact)
        state = ENG.load_run("MAX-999")
        ticket = state["talent_tickets"][self.talent_id]
        self.assertEqual(ticket["status"], "resolved")
        self.assertEqual(ticket["talent_artifact_url"], artifact)
        self.assertIsNotNone(ticket["resolved_at"])

    def test_swap_updates_blackboard_status_key(self):
        artifact = "https://drive.google.com/file/d/real-asset"
        ENG.resolve_talent_ticket("MAX-999", self.talent_id, artifact)
        state = ENG.load_run("MAX-999")
        status_key = f"talent.{self.talent_id}.status"
        self.assertEqual(state["blackboard"][status_key], "resolved")

    def test_swap_returns_old_placeholder(self):
        artifact = "https://drive.google.com/file/d/real-asset"
        result = ENG.resolve_talent_ticket("MAX-999", self.talent_id, artifact)
        self.assertEqual(result["old_placeholder"], "[AI PLACEHOLDER]")

    def test_swap_returns_new_url(self):
        artifact = "https://drive.google.com/file/d/real-asset"
        result = ENG.resolve_talent_ticket("MAX-999", self.talent_id, artifact)
        self.assertEqual(result["new_artifact_url"], artifact)

    def test_double_swap_raises(self):
        artifact = "https://drive.google.com/file/d/real-asset"
        ENG.resolve_talent_ticket("MAX-999", self.talent_id, artifact)
        with self.assertRaises(RuntimeError):
            ENG.resolve_talent_ticket("MAX-999", self.talent_id, "another-url")

    def test_unknown_talent_id_raises(self):
        with self.assertRaises(ValueError):
            ENG.resolve_talent_ticket("MAX-999", "nonexistent-talent-id", "http://x")


class TestTalentTicketList(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp)
        ENG.RUNS_DIR = self.tmp_path
        _make_tmp_run(self.tmp_path)

    def test_empty_list_when_no_tickets(self):
        result = ENG.list_talent_tickets("MAX-999")
        self.assertEqual(result, [])

    def test_list_returns_all_tickets(self):
        ENG.create_talent_ticket("MAX-999", "awareness", "reel_script", "Reel")
        ENG.create_talent_ticket("MAX-999", "awareness", "demo_recording", "Demo")
        result = ENG.list_talent_tickets("MAX-999")
        self.assertEqual(len(result), 2)

    def test_filter_pending_only(self):
        r1 = ENG.create_talent_ticket("MAX-999", "awareness", "reel_script", "Reel")
        r2 = ENG.create_talent_ticket("MAX-999", "awareness", "demo_recording", "Demo")
        ENG.resolve_talent_ticket("MAX-999", r1["talent_id"], "https://asset.url")
        pending = ENG.list_talent_tickets("MAX-999", status_filter="pending")
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["talent_id"], r2["talent_id"])

    def test_filter_resolved_only(self):
        r1 = ENG.create_talent_ticket("MAX-999", "awareness", "reel_script", "Reel")
        ENG.create_talent_ticket("MAX-999", "awareness", "demo_recording", "Demo")
        ENG.resolve_talent_ticket("MAX-999", r1["talent_id"], "https://asset.url")
        resolved = ENG.list_talent_tickets("MAX-999", status_filter="resolved")
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["talent_id"], r1["talent_id"])

    def test_newest_first_ordering(self):
        import time
        r1 = ENG.create_talent_ticket("MAX-999", "awareness", "reel_script", "First")
        time.sleep(0.01)  # ensure distinct timestamps
        r2 = ENG.create_talent_ticket("MAX-999", "awareness", "demo_recording", "Second")
        result = ENG.list_talent_tickets("MAX-999")
        # Newest first = r2 should be first
        self.assertEqual(result[0]["talent_id"], r2["talent_id"])


class TestTalentStateSchema(unittest.TestCase):
    """Verify create_ship_run initialises talent_tickets in state."""
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp)
        ENG.RUNS_DIR = self.tmp_path
        # Patch Drive to avoid real API calls
        ENG.create_drive_folders = lambda *a, **k: (_ for _ in ()).throw(Exception("drive-mocked"))

    def test_create_ship_run_includes_talent_tickets(self):
        state = ENG.create_ship_run("Test App", "A test GTM run")
        self.assertIn("talent_tickets", state)
        self.assertIsInstance(state["talent_tickets"], dict)
        self.assertEqual(len(state["talent_tickets"]), 0)


class TestTalentDeliverableTypes(unittest.TestCase):
    def test_all_types_have_labels(self):
        for key, label in ENG.TALENT_DELIVERABLE_TYPES.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(label, str)
            self.assertGreater(len(label), 5)

    def test_other_type_exists(self):
        self.assertIn("other", ENG.TALENT_DELIVERABLE_TYPES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
