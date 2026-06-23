from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    ROOT / "docs/DECISION_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    ROOT / "docs/DECISION_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    ROOT / "docs/DECISION_API_DISPLAY_BOUNDARY_AUDIT.md",
    ROOT / "docs/DECISION_BOUNDARY_INTEGRATION_AUDIT.md",
    ROOT / "docs/DECISION_INTEGRATION_NO_RECOMMENDATION_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_READINESS_PLAN.md",
]


def test_prompt_48_api_display_integration_audit_docs_exist() -> None:
    for path in DOCS:
        assert path.exists(), path


def test_prompt_48_api_display_integration_audit_docs_state_required_boundaries() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)

    for phrase in [
        "Prompts 40-47",
        "Decision Desk API Contract Skeleton",
        "Decision Desk Readiness API Skeleton",
        "Decision Desk Display Contract Skeleton",
        "Decision Evidence Bundle Validation v0",
        "Decision Human Review Workflow Skeleton",
        "Decision Desk System Boundary Hardening",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no approvals",
        "no overrides",
        "no active workflow",
        "no active UI",
        "no readiness-to-trade",
        "no execution APIs",
        "Retail Dashboard Planning and Guardrails only",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text

