from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _run_audit():
    spec = importlib.util.spec_from_file_location("audit_foundation", ROOT / "scripts/audit_foundation.py")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.run_audit()


def test_audit_foundation_passes_prompt_41_invariants() -> None:
    failures = [result for result in _run_audit() if not result.passed]

    assert failures == []


def test_verify_foundation_tracks_prompt_36_to_41_artifacts() -> None:
    verifier = _read("scripts/verify_foundation.py")

    for phrase in [
        "docs/DECISION_DESK_MILESTONE_AUDIT.md",
        "docs/DECISION_DESK_BOUNDARY_AUDIT.md",
        "docs/DECISION_EVIDENCE_BOUNDARY_AUDIT.md",
        "docs/DECISION_SAFETY_BOUNDARY_AUDIT.md",
        "docs/DECISION_API_SKELETON_AUDIT.md",
        "docs/DECISION_NO_RECOMMENDATION_AUDIT.md",
        "docs/DECISION_DESK_NEXT_PHASE_PLAN.md",
        "packages/core/stark_terminal_core/decision_desk/planning.py",
        "packages/core/stark_terminal_core/decision_evidence/bundle.py",
        "packages/core/stark_terminal_core/decision_safety/guardrails.py",
        "packages/core/stark_terminal_core/decision_api/requests.py",
        "tests/test_decision_desk_milestone_readiness.py",
    ]:
        assert phrase in verifier


def test_prompt_41_readiness_docs_recommend_prompt_42() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Current Prompt: 44" in north_star
    assert "Decision Desk Milestone Audit completed" in north_star
    assert "Prompt 42 - Decision Desk Readiness API Skeleton" in next_phase
    assert "recommendations, confidence scoring, active DecisionObject generation, approvals, overrides, or execution" in next_phase
    assert "## Prompt 41 - Decision Desk Milestone Audit" in prompt_log

