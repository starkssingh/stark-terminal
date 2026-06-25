from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _run_audit():
    script_path = ROOT / "scripts/audit_foundation.py"
    spec = importlib.util.spec_from_file_location("audit_foundation_for_prompt_60", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.run_audit()


def test_audit_foundation_includes_prompt_60_artifacts() -> None:
    results = _run_audit()
    failures = [result for result in results if not result.passed]
    assert failures == []


def test_verify_foundation_includes_prompt_56_through_60_artifacts() -> None:
    verify = _read("scripts/verify_foundation.py")
    for artifact in [
        "docs/RETAIL_TRADER_EXPERIENCE_PLANNING.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_CONTRACT_SKELETON.md",
        "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_CONTRACT_SKELETON.md",
        "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT.md",
        "tests/test_retail_trader_experience_next_phase_readiness.py",
    ]:
        assert artifact in verify


def test_next_phase_documents_recommend_prompt_61_only() -> None:
    next_plan = _read("docs/RETAIL_TRADER_EXPERIENCE_NEXT_PHASE_PLAN.md")
    global_next_plan = _read("docs/NEXT_PHASE_PLAN.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Prompt 61 - Retail Trader Experience System Boundary Hardening" in next_plan
    assert "Prompt 61 - Retail Trader Experience System Boundary Hardening" in global_next_plan
    assert "Current Prompt: 60" in north_star
    assert "Prompt 60 - Retail Trader Experience Milestone Audit" in prompt_log


def test_next_phase_keeps_active_trading_controls_forbidden() -> None:
    text = "\n".join(
        _read(path).lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_NEXT_PHASE_PLAN.md",
            "docs/NEXT_PHASE_PLAN.md",
            "docs/NORTH_STAR.md",
        ]
    )
    for phrase in [
        "active ui",
        "recommendation",
        "suitability profiling",
        "broker controls",
        "execution",
        "remain forbidden",
    ]:
        assert phrase in text
