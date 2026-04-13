#!/usr/bin/env python3
"""
Tests for NEO-185: Ship Engine Measure Feedback Loops

Covers:
- DEFAULT_METRIC_THRESHOLDS / METRIC_LABELS / METRIC_SUGGESTIONS completeness
- _get_metric_thresholds (default + custom overrides)
- _get_metric_to_stage (default + custom overrides)
- _fmt_metric (pct / sec / raw)
- measure_feedback — all verdicts: NO_DATA / DOUBLE DOWN / ITERATE / KILL or PIVOT
- Inverted metrics (bounce_rate, page_load_time)
- Partial metric sets (unknown metrics are skipped gracefully)
- Custom per-run thresholds applied during feedback evaluation
- Feedback state persisted to run file (blackboard writeback)
- _create_feedback_ticket — correct gql payload (priority 1 vs 2)

Run with:
    python3 -m pytest skills/ship-engine/tests/test_measure_feedback.py -v
"""

import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
import unittest.mock as _mock_lib
import pytest

# ── Bootstrap: load engine module from file path (hyphen in dir name) ─────────
_tmp_dir = tempfile.mkdtemp()
_tmp_runs = Path(_tmp_dir) / "runs"
_tmp_runs.mkdir()
_tmp_archive = Path(_tmp_dir) / "archive"
_tmp_archive.mkdir()

_ENGINE_PATH = Path(__file__).parent.parent / "engine.py"

_orig_open = open


def _mock_open(path, *args, **kwargs):
    if ".linear_token" in str(path):
        m = MagicMock()
        m.__enter__ = lambda s: s
        m.__exit__ = MagicMock(return_value=False)
        m.read = MagicMock(return_value="fake-token")
        return m
    return _orig_open(path, *args, **kwargs)


with _mock_lib.patch("builtins.open", side_effect=_mock_open):
    spec = importlib.util.spec_from_file_location("engine", _ENGINE_PATH)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)

# Redirect run/archive dirs to tmp
engine.RUNS_DIR = _tmp_runs
engine.ARCHIVE_DIR = _tmp_archive

# Stub gql — no real Linear API calls
engine.gql = MagicMock(return_value={
    "issueCreate": {
        "issue": {"id": "new-issue-uuid", "identifier": "NEO-999", "title": "Test Issue"}
    }
})

# ── Test constants ─────────────────────────────────────────────────────────────
_TEST_RUN_ID = "NEO-185-TEST"

_BASE_STATE = {
    "ticket": _TEST_RUN_ID,
    "name": "Test Product",
    "stage": "measure",
    "created": "2026-01-01T00:00:00+00:00",
    "updated": "2026-01-01T00:00:00+00:00",
    "linear": {
        "parentId": "parent-uuid-123",
        "parentIdentifier": _TEST_RUN_ID,
        "projectId": "project-uuid-123",
        "subIssues": {},
    },
    "metrics": {},
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _write_state(extra=None):
    """Write a fresh test state to the tmp runs dir."""
    state = copy.deepcopy(_BASE_STATE)
    if extra:
        for k, v in extra.items():
            if isinstance(v, dict) and isinstance(state.get(k), dict):
                state[k] = {**state[k], **v}
            else:
                state[k] = v
    path = _tmp_runs / f"{_TEST_RUN_ID}.json"
    path.write_text(json.dumps(state))
    return state


@pytest.fixture(autouse=True)
def _reset_state_and_gql():
    """Reset run state file and gql mock before every test (works for both functions and methods)."""
    _write_state()
    engine.gql.reset_mock()
    engine.gql.side_effect = None
    engine.gql.return_value = {
        "issueCreate": {
            "issue": {"id": "new-issue-uuid", "identifier": "NEO-999", "title": "Test Issue"}
        }
    }
    yield


# ── Constants integrity ───────────────────────────────────────────────────────

class TestMetricConstants:
    def test_all_thresholds_have_required_keys(self):
        for name, cfg in engine.DEFAULT_METRIC_THRESHOLDS.items():
            assert "warn" in cfg, f"{name} missing 'warn'"
            assert "critical" in cfg, f"{name} missing 'critical'"
            assert "inverted" in cfg, f"{name} missing 'inverted'"
            assert "fmt" in cfg, f"{name} missing 'fmt'"

    def test_fmt_values_are_valid(self):
        valid_fmts = {"pct", "sec", "raw"}
        for name, cfg in engine.DEFAULT_METRIC_THRESHOLDS.items():
            assert cfg["fmt"] in valid_fmts, f"{name} has unknown fmt '{cfg['fmt']}'"

    def test_labels_cover_all_thresholds(self):
        for key in engine.DEFAULT_METRIC_THRESHOLDS:
            assert key in engine.METRIC_LABELS, f"METRIC_LABELS missing entry for '{key}'"

    def test_suggestions_cover_all_thresholds(self):
        for key in engine.DEFAULT_METRIC_THRESHOLDS:
            assert key in engine.METRIC_SUGGESTIONS, f"METRIC_SUGGESTIONS missing entry for '{key}'"

    def test_metric_to_stage_covers_all_thresholds(self):
        for key in engine.DEFAULT_METRIC_THRESHOLDS:
            assert key in engine.DEFAULT_METRIC_TO_STAGE, (
                f"DEFAULT_METRIC_TO_STAGE missing entry for '{key}'"
            )

    def test_metric_to_stage_values_are_valid_stages(self):
        valid_stages = set(engine.STAGES)
        for metric, stage in engine.DEFAULT_METRIC_TO_STAGE.items():
            assert stage in valid_stages, (
                f"DEFAULT_METRIC_TO_STAGE['{metric}'] = '{stage}' is not a known stage"
            )

    def test_inverted_metrics_have_higher_critical_than_warn(self):
        """For inverted metrics (higher = worse), critical > warn."""
        for name, cfg in engine.DEFAULT_METRIC_THRESHOLDS.items():
            if cfg["inverted"]:
                assert cfg["critical"] > cfg["warn"], (
                    f"Inverted metric '{name}': critical ({cfg['critical']}) "
                    f"should be > warn ({cfg['warn']})"
                )

    def test_non_inverted_metrics_have_lower_critical_than_warn(self):
        """For normal metrics (lower = worse), critical < warn."""
        for name, cfg in engine.DEFAULT_METRIC_THRESHOLDS.items():
            if not cfg["inverted"]:
                assert cfg["critical"] < cfg["warn"], (
                    f"Normal metric '{name}': critical ({cfg['critical']}) "
                    f"should be < warn ({cfg['warn']})"
                )


# ── _get_metric_thresholds ────────────────────────────────────────────────────

class TestGetMetricThresholds:
    def test_returns_defaults_when_no_custom(self):
        state = _write_state()
        thresholds = engine._get_metric_thresholds(state)
        assert thresholds == engine.DEFAULT_METRIC_THRESHOLDS

    def test_custom_overrides_existing_metric(self):
        state = _write_state({"custom_thresholds": {
            "landing_conversion": {"warn": 0.05, "critical": 0.02}
        }})
        thresholds = engine._get_metric_thresholds(state)
        assert thresholds["landing_conversion"]["warn"] == 0.05
        assert thresholds["landing_conversion"]["critical"] == 0.02
        # Non-overridden fields preserved from default
        assert thresholds["landing_conversion"]["fmt"] == "pct"

    def test_custom_adds_new_metric(self):
        state = _write_state({"custom_thresholds": {
            "custom_metric": {"warn": 100, "critical": 50, "inverted": False, "fmt": "raw"}
        }})
        thresholds = engine._get_metric_thresholds(state)
        assert "custom_metric" in thresholds
        assert thresholds["custom_metric"]["warn"] == 100

    def test_does_not_mutate_global_defaults(self):
        """Custom overrides must not modify DEFAULT_METRIC_THRESHOLDS in place."""
        original_defaults = copy.deepcopy(engine.DEFAULT_METRIC_THRESHOLDS)
        state = _write_state({"custom_thresholds": {
            "landing_conversion": {"warn": 0.99}
        }})
        engine._get_metric_thresholds(state)
        assert engine.DEFAULT_METRIC_THRESHOLDS == original_defaults


# ── _get_metric_to_stage ─────────────────────────────────────────────────────

class TestGetMetricToStage:
    def test_returns_defaults_when_no_custom(self):
        state = _write_state()
        mapping = engine._get_metric_to_stage(state)
        assert mapping == engine.DEFAULT_METRIC_TO_STAGE

    def test_custom_overrides_stage(self):
        state = _write_state({"metric_ownership": {"signup_rate": "awareness"}})
        mapping = engine._get_metric_to_stage(state)
        assert mapping["signup_rate"] == "awareness"

    def test_does_not_mutate_global_defaults(self):
        original = copy.deepcopy(engine.DEFAULT_METRIC_TO_STAGE)
        state = _write_state({"metric_ownership": {"signup_rate": "closing"}})
        engine._get_metric_to_stage(state)
        assert engine.DEFAULT_METRIC_TO_STAGE == original


# ── _fmt_metric ───────────────────────────────────────────────────────────────

class TestFmtMetric:
    def test_pct_format(self):
        assert engine._fmt_metric(0.045, "pct") == "4.5%"

    def test_pct_format_zero(self):
        assert engine._fmt_metric(0.0, "pct") == "0.0%"

    def test_pct_format_one(self):
        assert engine._fmt_metric(1.0, "pct") == "100.0%"

    def test_sec_format(self):
        assert engine._fmt_metric(2.5, "sec") == "2.5s"

    def test_sec_format_one_decimal(self):
        assert engine._fmt_metric(1.0, "sec") == "1.0s"

    def test_raw_format_int(self):
        assert engine._fmt_metric(42, "raw") == "42"

    def test_raw_format_float(self):
        result = engine._fmt_metric(3.14, "raw")
        assert "3.14" in result


# ── measure_feedback: NO_DATA ─────────────────────────────────────────────────

class TestMeasureFeedbackNoData:
    def test_returns_no_data_when_metrics_empty(self):
        _write_state({"metrics": {}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "NO_DATA"
        assert result["healthy"] == []
        assert result["warning"] == []
        assert result["critical"] == []
        assert result["tickets_created"] == 0

    def test_no_data_does_not_call_gql(self):
        _write_state({"metrics": {}})
        engine.measure_feedback(_TEST_RUN_ID)
        engine.gql.assert_not_called()

    def test_no_data_when_metrics_key_missing(self):
        """State with no 'metrics' key at all also returns NO_DATA."""
        state = copy.deepcopy(_BASE_STATE)
        del state["metrics"]
        (_tmp_runs / f"{_TEST_RUN_ID}.json").write_text(json.dumps(state))
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "NO_DATA"


# ── measure_feedback: DOUBLE DOWN (all healthy) ───────────────────────────────

class TestMeasureFeedbackDoubleDown:
    def test_all_healthy_returns_double_down(self):
        _write_state({"metrics": {
            "landing_conversion": 0.05,   # > 0.02 warn → healthy
            "email_open_rate": 0.35,       # > 0.20 → healthy
            "signup_rate": 0.08,           # > 0.03 → healthy
        }})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "DOUBLE DOWN"
        assert len(result["healthy"]) == 3
        assert result["warning"] == []
        assert result["critical"] == []
        assert result["tickets_created"] == 0

    def test_healthy_does_not_create_tickets(self):
        _write_state({"metrics": {"signup_rate": 0.10}})
        engine.measure_feedback(_TEST_RUN_ID)
        engine.gql.assert_not_called()

    def test_healthy_entry_has_zero_gap(self):
        _write_state({"metrics": {"signup_rate": 0.10}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["healthy"][0]
        assert entry["gap"] == 0.0
        assert entry["metric"] == "signup_rate"

    def test_healthy_entry_has_correct_value(self):
        _write_state({"metrics": {"landing_conversion": 0.05}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["healthy"][0]
        assert entry["value"] == 0.05

    def test_healthy_entry_has_stage(self):
        _write_state({"metrics": {"email_open_rate": 0.30}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["healthy"][0]
        assert entry["stage"] == "nurture"


# ── measure_feedback: ITERATE (warning only) ─────────────────────────────────

class TestMeasureFeedbackIterate:
    def test_warning_metric_returns_iterate(self):
        # email_open_rate: warn=0.20, critical=0.10 → 0.15 is between → warning
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "ITERATE"
        assert len(result["warning"]) == 1
        assert result["critical"] == []

    def test_warning_creates_priority_2_ticket(self):
        _write_state({"metrics": {"email_open_rate": 0.15}})
        engine.measure_feedback(_TEST_RUN_ID)
        engine.gql.assert_called_once()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["priority"] == 2

    def test_warning_ticket_has_correct_stage(self):
        """email_open_rate belongs to nurture stage."""
        _write_state({"metrics": {"email_open_rate": 0.15}})
        engine.measure_feedback(_TEST_RUN_ID)
        variables = engine.gql.call_args[0][1]
        body = variables["input"]["description"]
        assert "nurture" in body.lower() or "Nurture" in body

    def test_warning_gap_calculated_correctly(self):
        # warn=0.20, actual=0.15 → gap = 0.20 - 0.15 = 0.05
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["warning"][0]
        assert abs(entry["gap"] - 0.05) < 1e-9

    def test_multiple_warnings_create_multiple_tickets(self):
        _write_state({"metrics": {
            "email_open_rate": 0.15,   # warning
            "signup_rate": 0.02,       # warning (between 0.01 critical and 0.03 warn)
        }})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["tickets_created"] == 2
        assert engine.gql.call_count == 2

    def test_warning_entry_has_label(self):
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["warning"][0]
        assert entry["label"] == engine.METRIC_LABELS["email_open_rate"]

    def test_warning_entry_has_fmt(self):
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["warning"][0]
        assert entry["fmt"] == "pct"


# ── measure_feedback: KILL or PIVOT (critical) ───────────────────────────────

class TestMeasureFeedbackKillOrPivot:
    def test_critical_metric_returns_kill_or_pivot(self):
        # email_open_rate critical=0.10 → 0.05 is below → critical
        _write_state({"metrics": {"email_open_rate": 0.05}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "KILL or PIVOT"
        assert len(result["critical"]) == 1
        assert result["warning"] == []

    def test_critical_creates_priority_1_ticket(self):
        _write_state({"metrics": {"email_open_rate": 0.05}})
        engine.measure_feedback(_TEST_RUN_ID)
        engine.gql.assert_called_once()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["priority"] == 1

    def test_critical_gap_calculated_correctly(self):
        # warn=0.20, actual=0.05 → gap = 0.20 - 0.05 = 0.15
        _write_state({"metrics": {"email_open_rate": 0.05}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["critical"][0]
        assert abs(entry["gap"] - 0.15) < 1e-9

    def test_critical_entry_has_target(self):
        _write_state({"metrics": {"email_open_rate": 0.05}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["critical"][0]
        # target is the warn threshold
        assert entry["target"] == engine.DEFAULT_METRIC_THRESHOLDS["email_open_rate"]["warn"]


# ── Inverted metrics (bounce_rate, page_load_time) ────────────────────────────

class TestInvertedMetrics:
    def test_bounce_rate_healthy_below_warn(self):
        # bounce_rate: warn=0.70, critical=0.85 (inverted)
        # actual=0.50 → below warn → healthy
        _write_state({"metrics": {"bounce_rate": 0.50}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "DOUBLE DOWN"
        assert any(e["metric"] == "bounce_rate" for e in result["healthy"])

    def test_bounce_rate_exactly_at_warn_threshold_is_warning(self):
        # actual=0.70 → >= 0.70 warn threshold → warning
        _write_state({"metrics": {"bounce_rate": 0.70}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "ITERATE"
        assert any(e["metric"] == "bounce_rate" for e in result["warning"])

    def test_bounce_rate_warning_between_warn_and_critical(self):
        # actual=0.75 → >= 0.70 warn, < 0.85 critical → warning
        _write_state({"metrics": {"bounce_rate": 0.75}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "ITERATE"
        assert any(e["metric"] == "bounce_rate" for e in result["warning"])

    def test_bounce_rate_critical_at_or_above_critical_threshold(self):
        # actual=0.90 → >= 0.85 critical → critical
        _write_state({"metrics": {"bounce_rate": 0.90}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "KILL or PIVOT"
        assert any(e["metric"] == "bounce_rate" for e in result["critical"])

    def test_page_load_time_warning(self):
        # page_load_time: warn=3.0, critical=5.0 (inverted)
        # actual=3.5 → warning
        _write_state({"metrics": {"page_load_time": 3.5}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "ITERATE"

    def test_page_load_time_critical(self):
        # actual=6.0 → >= 5.0 critical → critical
        _write_state({"metrics": {"page_load_time": 6.0}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "KILL or PIVOT"

    def test_page_load_time_healthy_below_warn(self):
        # actual=2.0 → < 3.0 warn → healthy
        _write_state({"metrics": {"page_load_time": 2.0}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "DOUBLE DOWN"

    def test_inverted_warning_gap_is_positive(self):
        # bounce_rate=0.75, warn=0.70 → gap = 0.75 - 0.70 = 0.05
        _write_state({"metrics": {"bounce_rate": 0.75}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["warning"][0]
        assert entry["gap"] > 0

    def test_inverted_healthy_gap_is_zero(self):
        _write_state({"metrics": {"bounce_rate": 0.40}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        entry = result["healthy"][0]
        assert entry["gap"] == 0.0


# ── Mixed metric set ──────────────────────────────────────────────────────────

class TestMixedMetrics:
    def test_any_critical_makes_verdict_kill_or_pivot(self):
        _write_state({"metrics": {
            "email_open_rate": 0.25,  # healthy
            "signup_rate": 0.02,      # warning
            "trial_to_paid": 0.005,   # critical (< 0.02 critical threshold)
        }})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "KILL or PIVOT"
        assert len(result["healthy"]) == 1
        assert len(result["warning"]) == 1
        assert len(result["critical"]) == 1

    def test_total_tickets_matches_warning_plus_critical(self):
        _write_state({"metrics": {
            "email_open_rate": 0.15,    # warning
            "signup_rate": 0.005,       # critical
            "landing_conversion": 0.03, # healthy
        }})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["tickets_created"] == 2
        assert result["tickets_created"] == len(result["warning"]) + len(result["critical"])

    def test_healthy_plus_warning_is_iterate(self):
        _write_state({"metrics": {
            "landing_conversion": 0.10, # healthy
            "email_open_rate": 0.15,    # warning
        }})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "ITERATE"


# ── Unknown / unrecognised metrics ────────────────────────────────────────────

class TestUnknownMetrics:
    def test_unknown_metric_is_skipped_gracefully(self):
        """Metrics not in DEFAULT_METRIC_THRESHOLDS must not cause errors."""
        _write_state({"metrics": {
            "unknown_custom_metric": 999,
            "email_open_rate": 0.30,  # healthy
        }})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "DOUBLE DOWN"
        # Only the known metric contributes
        assert len(result["healthy"]) == 1
        assert result["healthy"][0]["metric"] == "email_open_rate"

    def test_all_unknown_metrics_returns_double_down_with_no_tickets(self):
        """If all provided metrics are unknown, no evaluation — DOUBLE DOWN, 0 tickets."""
        _write_state({"metrics": {"completely_custom": 1.0}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "DOUBLE DOWN"
        assert result["tickets_created"] == 0

    def test_unknown_metric_does_not_create_ticket(self):
        _write_state({"metrics": {"unknown_thing": 0.5}})
        engine.measure_feedback(_TEST_RUN_ID)
        engine.gql.assert_not_called()


# ── Custom thresholds applied at runtime ─────────────────────────────────────

class TestCustomThresholds:
    def test_custom_warn_threshold_changes_classification_to_warning(self):
        """Raising landing_conversion warn to 0.10 should push 0.04 into warning."""
        _write_state({
            "metrics": {"landing_conversion": 0.04},  # default warn=0.02 → healthy
            # custom: warn=0.10, critical=0.02 → 0.04 is between critical(0.02) and warn(0.10) → warning
            "custom_thresholds": {"landing_conversion": {"warn": 0.10, "critical": 0.02}},
        })
        result = engine.measure_feedback(_TEST_RUN_ID)
        # 0.04 > 0.02 critical but < 0.10 warn → warning
        assert len(result["warning"]) == 1
        assert result["warning"][0]["metric"] == "landing_conversion"

    def test_custom_critical_threshold_promotes_to_critical(self):
        """Raising critical threshold should push a warning metric to critical."""
        _write_state({
            "metrics": {"email_open_rate": 0.12},  # default: warn=0.20, critical=0.10 → warning
            "custom_thresholds": {"email_open_rate": {"critical": 0.15}},
        })
        result = engine.measure_feedback(_TEST_RUN_ID)
        # 0.12 < 0.15 custom critical → critical
        assert len(result["critical"]) == 1

    def test_custom_metric_ownership_reflected_in_ticket_body(self):
        """Custom metric_ownership must appear in the generated ticket body."""
        _write_state({
            "metrics": {"signup_rate": 0.02},  # warning
            "metric_ownership": {"signup_rate": "awareness"},  # override from lead-capture
        })
        engine.measure_feedback(_TEST_RUN_ID)
        variables = engine.gql.call_args[0][1]
        body = variables["input"]["description"]
        assert "awareness" in body.lower() or "Awareness" in body


# ── Blackboard writeback / state persistence ──────────────────────────────────

class TestStateWriteback:
    def test_measure_feedback_key_written_to_state(self):
        _write_state({"metrics": {"email_open_rate": 0.15}})
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert "measure_feedback" in state

    def test_state_feedback_verdict_matches_return(self):
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert state["measure_feedback"]["verdict"] == result["verdict"]

    def test_state_contains_run_at_timestamp(self):
        _write_state({"metrics": {"email_open_rate": 0.15}})
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert "run_at" in state["measure_feedback"]
        # ISO format check
        assert "T" in state["measure_feedback"]["run_at"]

    def test_state_lists_healthy_metric_names(self):
        _write_state({"metrics": {"email_open_rate": 0.30}})
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert "email_open_rate" in state["measure_feedback"]["healthy"]

    def test_state_lists_warning_metric_names(self):
        _write_state({"metrics": {
            "email_open_rate": 0.25,   # healthy
            "signup_rate": 0.02,       # warning
        }})
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        fb = state["measure_feedback"]
        assert "email_open_rate" in fb["healthy"]
        assert "signup_rate" in fb["warning"]
        assert fb["critical"] == []

    def test_state_contains_tickets_created_count(self):
        _write_state({"metrics": {"email_open_rate": 0.05}})  # critical
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert state["measure_feedback"]["tickets_created"] == 1

    def test_state_persists_double_down_verdict(self):
        _write_state({"metrics": {"email_open_rate": 0.30}})
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert state["measure_feedback"]["verdict"] == "DOUBLE DOWN"


# ── _create_feedback_ticket: Linear issue shape ───────────────────────────────

class TestCreateFeedbackTicket:
    def _run_warning(self):
        _write_state({"metrics": {"signup_rate": 0.02}})
        return engine.measure_feedback(_TEST_RUN_ID)

    def _run_critical(self):
        _write_state({"metrics": {"email_open_rate": 0.05}})
        return engine.measure_feedback(_TEST_RUN_ID)

    def test_ticket_uses_correct_team_id(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["teamId"] == engine.MAX_TEAM_ID

    def test_ticket_uses_ship_engine_label(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        assert engine.SHIP_ENGINE_LABEL_ID in variables["input"]["labelIds"]

    def test_ticket_state_is_todo(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["stateId"] == engine.STATES["Todo"]

    def test_warning_ticket_priority_is_2(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["priority"] == 2

    def test_critical_ticket_priority_is_1(self):
        self._run_critical()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["priority"] == 1

    def test_ticket_uses_project_id_from_state(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["projectId"] == "project-uuid-123"

    def test_ticket_falls_back_to_parent_id_when_no_measure_sub_issue(self):
        """Without a Measure sub-issue in state, ticket is parented to the run root."""
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["parentId"] == "parent-uuid-123"

    def test_ticket_prefers_measure_sub_issue_as_parent(self):
        """When a Measure sub-issue exists in state, it is preferred as parent."""
        _write_state({
            "metrics": {"signup_rate": 0.02},
            "linear": {
                "parentId": "parent-uuid-123",
                "parentIdentifier": _TEST_RUN_ID,
                "projectId": "project-uuid-123",
                "subIssues": {
                    "measure": {"id": "measure-sub-uuid", "identifier": "NEO-MEASURE"}
                },
            },
        })
        engine.measure_feedback(_TEST_RUN_ID)
        variables = engine.gql.call_args[0][1]
        assert variables["input"]["parentId"] == "measure-sub-uuid"

    def test_ticket_body_contains_formatted_metric_value(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        body = variables["input"]["description"]
        # signup_rate=0.02 → formatted as "2.0%"
        assert "2.0%" in body

    def test_ticket_body_contains_suggested_action_section(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        body = variables["input"]["description"]
        assert "Suggested Action" in body

    def test_ticket_title_contains_metric_label(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        title = variables["input"]["title"]
        assert "Signup Rate" in title

    def test_ticket_title_contains_responsible_stage(self):
        """signup_rate → lead-capture stage → 'Lead Capture' in title."""
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        title = variables["input"]["title"]
        assert "Lead Capture" in title

    def test_ticket_body_contains_run_product_name(self):
        self._run_warning()
        variables = engine.gql.call_args[0][1]
        body = variables["input"]["description"]
        assert "Test Product" in body


# ── gql failure resilience ───────────────────────────────────────────────────

class TestGqlFailureResilience:
    def test_gql_exception_does_not_raise(self):
        """If Linear ticket creation fails, measure_feedback must not raise."""
        engine.gql.side_effect = Exception("Linear API down")
        _write_state({"metrics": {"email_open_rate": 0.15}})
        # Should not raise
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["verdict"] == "ITERATE"

    def test_gql_exception_zeros_ticket_count(self):
        """On gql failure, tickets_created should be 0."""
        engine.gql.side_effect = Exception("Linear API down")
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert result["tickets_created"] == 0

    def test_gql_failure_still_writes_state(self):
        """Even if ticket creation fails, blackboard state must be persisted."""
        engine.gql.side_effect = Exception("Linear API down")
        _write_state({"metrics": {"email_open_rate": 0.15}})
        engine.measure_feedback(_TEST_RUN_ID)
        state = engine.load_run(_TEST_RUN_ID)
        assert "measure_feedback" in state
        assert state["measure_feedback"]["verdict"] == "ITERATE"

    def test_gql_failure_metric_still_in_warning_list(self):
        """The warning/critical classification still happens even if ticket creation fails."""
        engine.gql.side_effect = Exception("Linear API down")
        _write_state({"metrics": {"email_open_rate": 0.15}})
        result = engine.measure_feedback(_TEST_RUN_ID)
        assert len(result["warning"]) == 1

    # Note: gql side_effect is reset by the module-level autouse fixture before each test
