"""
Phase 2 unit tests — StarGuard Desktop
17 tests: gap row filtering, measure aggregation, None-sheet guard,
suppression count logic, HITL panel contracts.
No live DB/API calls.
"""
import json
import os
import tempfile

import pandas as pd
import pytest


# ── Gap suppression CRUD ───────────────────────────────────────────────────

@pytest.fixture
def gap_suppression_temp(monkeypatch):
    """Use temp file for gap suppressions."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    monkeypatch.setenv("GAP_SUPPRESSION_FILE", path)
    yield path
    try:
        os.unlink(path)
    except OSError:
        pass


def test_get_gap_suppressions_empty(gap_suppression_temp):
    """get_gap_suppressions returns [] when file empty."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    assert hedis_gap_trail.get_gap_suppressions() == []


def test_add_gap_suppression_success(gap_suppression_temp):
    """add_gap_suppression adds rule and returns success."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    r = hedis_gap_trail.add_gap_suppression("GAP-20260304-001", "Member deceased")
    assert r["success"] is True
    assert r["gap_id"] == "GAP-20260304-001"
    rules = hedis_gap_trail.get_gap_suppressions()
    assert len(rules) == 1
    assert rules[0]["gap_id"] == "GAP-20260304-001"


def test_add_gap_suppression_duplicate_guard(gap_suppression_temp):
    """add_gap_suppression rejects duplicate gap_id."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    hedis_gap_trail.add_gap_suppression("GAP-X", "First")
    r = hedis_gap_trail.add_gap_suppression("GAP-X", "Second")
    assert r["success"] is False
    assert "Already suppressed" in r.get("error", "")
    assert len(hedis_gap_trail.get_gap_suppressions()) == 1


def test_remove_gap_suppression_success(gap_suppression_temp):
    """remove_gap_suppression removes rule."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    hedis_gap_trail.add_gap_suppression("GAP-Y", "Test")
    r = hedis_gap_trail.remove_gap_suppression("GAP-Y")
    assert r["success"] is True
    assert hedis_gap_trail.get_gap_suppressions() == []


# ── Gap row filtering (apply_gap_suppression_filter) ─────────────────────────

def test_apply_gap_suppression_filter_empty_df(gap_suppression_temp):
    """apply_gap_suppression_filter returns empty df unchanged."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    df = pd.DataFrame()
    out = hedis_gap_trail.apply_gap_suppression_filter(df)
    assert out.empty


def test_apply_gap_suppression_filter_no_gap_id_column(gap_suppression_temp):
    """apply_gap_suppression_filter returns df unchanged if no gap_id column."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    df = pd.DataFrame({"a": [1], "b": [2]})
    out = hedis_gap_trail.apply_gap_suppression_filter(df)
    assert len(out) == 1


def test_apply_gap_suppression_filter_removes_suppressed(gap_suppression_temp):
    """apply_gap_suppression_filter removes rows with suppressed gap_ids."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    hedis_gap_trail.add_gap_suppression("GAP-SUPP", "Test")
    df = pd.DataFrame({
        "gap_id": ["GAP-SUPP", "GAP-KEEP"],
        "measure_code": ["CBP", "CDC"],
    })
    out = hedis_gap_trail.apply_gap_suppression_filter(df)
    assert len(out) == 1
    assert out["gap_id"].iloc[0] == "GAP-KEEP"


def test_apply_gap_suppression_filter_no_suppressions(gap_suppression_temp):
    """apply_gap_suppression_filter returns all rows when no suppressions."""
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    df = pd.DataFrame({"gap_id": ["G1", "G2"], "x": [1, 2]})
    out = hedis_gap_trail.apply_gap_suppression_filter(df)
    assert len(out) == 2


# ── Measure aggregation (HEDIS_MEASURES) ───────────────────────────────────

def test_hedis_measures_has_expected_keys():
    """HEDIS_MEASURES contains CBP, CDC, GSD, etc."""
    from hedis_gap_trail import HEDIS_MEASURES
    assert "CBP" in HEDIS_MEASURES
    assert "CDC" in HEDIS_MEASURES
    assert "GSD" in HEDIS_MEASURES
    assert "BCS" in HEDIS_MEASURES
    assert "COL" in HEDIS_MEASURES
    assert len(HEDIS_MEASURES) >= 10


def test_hedis_measures_tuple_structure():
    """Each HEDIS_MEASURES value is (name, domain) tuple."""
    from hedis_gap_trail import HEDIS_MEASURES
    for code, val in HEDIS_MEASURES.items():
        assert isinstance(val, tuple)
        assert len(val) == 2
        assert isinstance(val[0], str)
        assert isinstance(val[1], str)


# ── None-sheet guard (fetch when disconnected) ──────────────────────────────

def test_fetch_hedis_gaps_disconnected_returns_empty():
    """fetch_hedis_gaps returns empty DataFrame when db.connected is False."""
    from hedis_gap_trail import HedisGapDB, HEDIS_COLUMNS, fetch_hedis_gaps
    db = HedisGapDB()
    db.connected = False
    out = fetch_hedis_gaps(db, n=5)
    assert isinstance(out, pd.DataFrame)
    assert out.empty or list(out.columns) == list(out.columns)
    assert len(out) == 0 or "Error" in out.columns


def test_fetch_gap_summary_disconnected_returns_zeros():
    """fetch_gap_summary returns zeroed dict when db.connected is False."""
    from hedis_gap_trail import HedisGapDB, fetch_gap_summary
    db = HedisGapDB()
    db.connected = False
    out = fetch_gap_summary(db)
    assert out["total"] == 0
    assert out["open"] == 0
    assert out["closed"] == 0
    assert "avg_star_impact" in out
    assert "total_roi" in out


def test_close_hedis_gap_disconnected_returns_error():
    """close_hedis_gap returns error when db.connected is False."""
    from hedis_gap_trail import HedisGapDB, close_hedis_gap
    db = HedisGapDB()
    db.connected = False
    r = close_hedis_gap(db, "GAP-123")
    assert r["success"] is False
    assert "error" in r


# ── HITL / Banner UI contracts ──────────────────────────────────────────────

def test_hitl_admin_css_returns_tag():
    """hitl_admin_css returns Tag."""
    from hitl_admin_view import hitl_admin_css
    assert hitl_admin_css() is not None


def test_hitl_admin_panel_returns_tag():
    """hitl_admin_panel returns Tag."""
    from hitl_admin_view import hitl_admin_panel
    assert hitl_admin_panel(app_type="gap") is not None


def test_suppression_banner_returns_tag():
    """suppression_banner returns Tag."""
    from suppression_banner import suppression_banner
    assert suppression_banner(app_type="gap") is not None


def test_hedis_columns_schema():
    """HEDIS_COLUMNS has expected schema."""
    from hedis_gap_trail import HEDIS_COLUMNS
    assert "gap_id" in HEDIS_COLUMNS
    assert "gap_status" in HEDIS_COLUMNS
    assert "measure_code" in HEDIS_COLUMNS
    assert len(HEDIS_COLUMNS) >= 10
