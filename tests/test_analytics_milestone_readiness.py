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


def test_audit_foundation_passes_prompt_30_invariants() -> None:
    results = _run_audit()
    failures = [result for result in results if not result.passed]
    assert failures == []


def test_verify_foundation_tracks_prompt_26_to_30_artifacts() -> None:
    text = _read("scripts/verify_foundation.py")
    required = [
        "docs/ANALYTICS_MILESTONE_AUDIT.md",
        "docs/ANALYTICS_BOUNDARY_AUDIT.md",
        "docs/ANALYTICS_NO_SIGNAL_AUDIT.md",
        "docs/ANALYTICS_DEPENDENCY_AUDIT.md",
        "docs/ANALYTICS_NEXT_PHASE_PLAN.md",
        "packages/analytics/stark_terminal_analytics/foundation/contracts.py",
        "packages/analytics/stark_terminal_analytics/numerical/contracts.py",
        "packages/analytics/stark_terminal_analytics/returns/calculations.py",
        "packages/analytics/stark_terminal_analytics/rolling/calculations.py",
        "packages/analytics/stark_terminal_analytics/volatility/calculations.py",
        "packages/analytics/stark_terminal_analytics/drawdown/calculations.py",
        "tests/test_analytics_milestone_readiness.py",
    ]
    for phrase in required:
        assert phrase in text


def test_prompt_32_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    analytics_next = _read("docs/ANALYTICS_NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Time-Series Diagnostics Foundation" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 34 - Regime Feature Preparation Contracts" in analytics_next
    assert "## Prompt 30 - Analytics Milestone Audit" in prompt_log
    assert "## Prompt 31 - Correlation and Beta Analytics v0" in prompt_log
    assert "Prompt 30 Analytics Milestone Audit Artifacts" in project_map
    assert "Prompt 31 Correlation and Beta Analytics v0 Artifacts" in project_map


def test_prompt_30_docs_reaffirm_research_only_analytics() -> None:
    text = "\n".join(
        [
            _read("docs/ANALYTICS_MILESTONE_AUDIT.md"),
            _read("docs/ANALYTICS_BOUNDARY_AUDIT.md"),
            _read("docs/ANALYTICS_NO_SIGNAL_AUDIT.md"),
            _read("docs/SAFETY_AUDIT.md"),
            _read("docs/DATA_POLICY.md"),
        ]
    )

    for phrase in [
        "descriptive/research-only",
        "no real ingestion",
        "no external calls",
        "no heavy dependencies",
        "no signals",
        "no recommendations",
        "no DecisionObject generation",
        "no execution APIs",
    ]:
        assert phrase in text
