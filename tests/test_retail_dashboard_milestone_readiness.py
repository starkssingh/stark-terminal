from __future__ import annotations

from pathlib import Path
import sys



ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_foundation import run_audit


def test_retail_dashboard_safety_audit_foundation_checks_pass() -> None:
    results = run_audit()
    failed = [result for result in results if not result.passed]
    assert not failed, [f"{result.name}: {result.detail}" for result in failed]


def test_verify_foundation_includes_prompt_49_through_52_artifacts() -> None:
    verify_text = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")
    for phrase in [
        "RETAIL_DASHBOARD_PLANNING.md",
        "RETAIL_DASHBOARD_API_CONTRACT_SKELETON.md",
        "RETAIL_DASHBOARD_DISPLAY_CONTRACT_SKELETON.md",
        "RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
        "test_retail_dashboard_milestone_readiness.py",
    ]:
        assert phrase in verify_text


def test_retail_dashboard_milestone_readiness_recommends_prompt_53() -> None:
    readiness = (ROOT / "docs/RETAIL_DASHBOARD_MILESTONE_READINESS.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Prompt 53 - Retail Dashboard Milestone Audit" in readiness
    assert "Prompt 53 - Retail Dashboard Milestone Audit" in next_phase
    assert "Current Prompt: 60" in north_star
    assert "Historical verifier reference: Current Prompt: 54" in north_star
    assert "Prompt 52 - Retail Dashboard Safety Boundary Audit" in prompt_log
    assert "Retail Dashboard Milestone Audit only" in readiness


def test_retail_dashboard_milestone_readiness_keeps_trading_controls_forbidden() -> None:
    readiness = (ROOT / "docs/RETAIL_DASHBOARD_MILESTONE_READINESS.md").read_text(encoding="utf-8")
    for phrase in [
        "Active Retail Dashboard UI",
        "frontend implementation",
        "desktop UI implementation",
        "recommendation cards",
        "broker controls",
        "readiness-to-trade",
        "execution APIs",
        "remain forbidden",
    ]:
        assert phrase in readiness
