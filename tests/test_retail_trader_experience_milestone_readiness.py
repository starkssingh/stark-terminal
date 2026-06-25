from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_59_artifacts_are_registered_with_verifier_and_audit_scripts() -> None:
    verify = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    for artifact in [
        "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md",
        "tests/test_retail_trader_experience_safety_boundary_audit_docs.py",
        "tests/test_retail_trader_experience_api_boundary_audit.py",
        "tests/test_retail_trader_experience_display_boundary_audit.py",
        "tests/test_retail_trader_experience_no_active_ui_audit.py",
        "tests/test_retail_trader_experience_no_recommendation_audit.py",
        "tests/test_retail_trader_experience_no_execution_audit.py",
        "tests/test_retail_trader_experience_no_suitability_profiling_audit.py",
        "tests/test_retail_trader_experience_api_surface_safety.py",
        "tests/test_retail_trader_experience_milestone_readiness.py",
    ]:
        assert artifact in verify or artifact in audit


def test_prompt_59_status_docs_recommend_prompt_60() -> None:
    milestone = _read("docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Prompt 60 - Retail Trader Experience Milestone Audit" in milestone
    assert "Prompt 60 - Retail Trader Experience Milestone Audit" in next_phase
    assert "Current Prompt: 60" in north_star
    assert "Completed Prompts: 61 after completion" in north_star
    assert "Retail Trader Experience Planning Phase - Milestone Audit completed" in north_star
    assert "Prompt 59 - Retail Trader Experience Safety Boundary Audit" in prompt_log


def test_milestone_readiness_keeps_active_surfaces_forbidden() -> None:
    text = "\n".join(
        _read(path).lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md",
            "docs/NEXT_PHASE_PLAN.md",
            "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md",
        ]
    )

    for phrase in [
        "retail trader experience milestone audit",
        "system boundary hardening",
        "active ui",
        "recommendations",
        "suitability profiling",
        "broker controls",
        "execution",
        "remain forbidden",
    ]:
        assert phrase in text
