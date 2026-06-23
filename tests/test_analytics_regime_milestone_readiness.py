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


def test_audit_foundation_passes_prompt_35_invariants() -> None:
    failures = [result for result in _run_audit() if not result.passed]

    assert failures == []


def test_verify_foundation_tracks_prompt_26_to_35_artifacts() -> None:
    verifier = _read("scripts/verify_foundation.py")

    for phrase in [
        "docs/ANALYTICS_REGIME_MILESTONE_AUDIT.md",
        "docs/REGIME_BOUNDARY_AUDIT.md",
        "docs/REGIME_NO_CLASSIFICATION_AUDIT.md",
        "docs/REGIME_FEATURE_PREPARATION_AUDIT.md",
        "docs/ANALYTICS_REGIME_NO_SIGNAL_AUDIT.md",
        "docs/ANALYTICS_REGIME_DEPENDENCY_AUDIT.md",
        "docs/DECISION_DESK_READINESS_PLAN.md",
        "packages/analytics/stark_terminal_analytics/regime_features/contracts.py",
        "apps/api/stark_terminal_api/routes/regime_features.py",
        "tests/test_analytics_regime_milestone_readiness.py",
    ]:
        assert phrase in verifier


def test_prompt_35_readiness_docs_are_preserved_after_prompt_36() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Current Prompt: 36" in north_star
    assert "Prompt 36 - Retail Decision Desk Planning and Guardrails" in next_phase
    assert "Prompt 37 - DecisionObject Evidence Bundle Contracts" in next_phase
    assert "Decision Desk implementation remains forbidden" in next_phase
    assert "## Prompt 35 - Analytics/Regime Milestone Audit" in prompt_log
    assert "## Prompt 36 - Retail Decision Desk Planning and Guardrails" in prompt_log
