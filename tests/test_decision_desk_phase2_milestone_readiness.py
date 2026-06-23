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


def test_audit_foundation_passes_prompt_46_invariants() -> None:
    failures = [result for result in _run_audit() if not result.passed]

    assert failures == []


def test_verify_foundation_tracks_prompt_42_to_46_artifacts() -> None:
    verifier = _read("scripts/verify_foundation.py")

    for phrase in [
        "docs/DECISION_DESK_MILESTONE_AUDIT_2.md",
        "docs/DECISION_READINESS_API_BOUNDARY_AUDIT.md",
        "docs/DECISION_DISPLAY_BOUNDARY_AUDIT.md",
        "docs/DECISION_EVIDENCE_VALIDATION_BOUNDARY_AUDIT.md",
        "docs/DECISION_HUMAN_REVIEW_WORKFLOW_BOUNDARY_AUDIT.md",
        "docs/DECISION_NO_APPROVAL_WORKFLOW_AUDIT.md",
        "docs/DECISION_DESK_NEXT_PHASE_PLAN_2.md",
        "packages/core/stark_terminal_core/decision_readiness_api/requests.py",
        "packages/core/stark_terminal_core/decision_display/contracts.py",
        "packages/core/stark_terminal_core/decision_evidence_validation/validators.py",
        "packages/core/stark_terminal_core/decision_human_review/workflow.py",
        "tests/test_decision_desk_phase2_milestone_readiness.py",
    ]:
        assert phrase in verifier


def test_prompt_46_readiness_docs_recommend_prompt_47() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Current Prompt: 46" in north_star
    assert "Decision Desk Milestone Audit 2 completed" in north_star
    assert "Prompt 47 - Decision Desk System Boundary Hardening" in next_phase
    assert "active UI, active workflow, readiness-to-trade, and execution remain forbidden" in next_phase
    assert "## Prompt 46 - Decision Desk Milestone Audit 2" in prompt_log
