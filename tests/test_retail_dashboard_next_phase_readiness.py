from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_foundation import run_audit


def test_retail_dashboard_milestone_audit_foundation_checks_pass() -> None:
    results = run_audit()
    failed = [result for result in results if not result.passed]
    assert not failed, [f"{result.name}: {result.detail}" for result in failed]


def test_verify_foundation_includes_prompt_49_through_55_artifacts() -> None:
    verify_text = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")
    for phrase in [
        "RETAIL_DASHBOARD_PLANNING.md",
        "RETAIL_DASHBOARD_API_CONTRACT_SKELETON.md",
        "RETAIL_DASHBOARD_DISPLAY_CONTRACT_SKELETON.md",
        "RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
        "RETAIL_DASHBOARD_MILESTONE_AUDIT.md",
        "RETAIL_DASHBOARD_SYSTEM_BOUNDARY_HARDENING.md",
        "RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
        "test_retail_dashboard_next_phase_readiness.py",
        "test_retail_dashboard_api_display_integration_audit_docs.py",
        "test_retail_dashboard_boundary_invariants.py",
    ]:
        assert phrase in verify_text


def test_retail_dashboard_next_phase_plan_recommends_prompt_56() -> None:
    dashboard_next = (ROOT / "docs/RETAIL_DASHBOARD_NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Prompt 56 - Retail Trader Experience Planning and Guardrails" in dashboard_next
    assert "Prompt 56 - Retail Trader Experience Planning and Guardrails" in next_phase
    assert "Current Prompt: 60" in north_star
    assert "Prompt 55 - Retail Dashboard API/Display Integration Readiness Audit" in prompt_log
    assert "Prompt 54 - Retail Dashboard System Boundary Hardening" in prompt_log
    assert "Retail Trader Experience Planning and Guardrails only" in dashboard_next


def test_retail_dashboard_next_phase_keeps_active_surfaces_forbidden() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
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
        assert phrase in text
