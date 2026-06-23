from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/retail_dashboard",
    ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
    ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
    ROOT / "packages/core/stark_terminal_core/retail_dashboard_boundary",
]


def _module_text() -> str:
    files = []
    for package in PACKAGES:
        files.extend(package.glob("*.py"))
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def test_retail_dashboard_modules_do_not_generate_recommendations_or_decisionobjects() -> None:
    text = _module_text()
    forbidden_names = [
        "def generate_dashboard_recommendation",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "DecisionObject(",
        "recommendation_generated=True",
        "action_generated=True",
        "confidence_generated=True",
        "decision_object_generated=True",
    ]
    for name in forbidden_names:
        assert name not in text


def test_retail_dashboard_boundary_recommendation_rejection_is_blocking_only() -> None:
    from stark_terminal_core.retail_dashboard_boundary.invariants import (
        reject_dashboard_recommendation_boundary_violation,
    )

    result = reject_dashboard_recommendation_boundary_violation()
    assert result.passed is False
    assert result.blockers
    assert result.recommendations_allowed is False
    assert result.execution_allowed is False
