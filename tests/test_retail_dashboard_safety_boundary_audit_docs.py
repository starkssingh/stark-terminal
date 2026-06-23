from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    ROOT / "docs/RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_API_BOUNDARY_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_BOUNDARY_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_NO_ACTIVE_UI_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_NO_EXECUTION_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_MILESTONE_READINESS.md",
]


def test_retail_dashboard_safety_boundary_audit_docs_exist() -> None:
    for path in DOCS:
        assert path.exists(), path


def test_retail_dashboard_safety_boundary_audit_docs_state_required_boundaries() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)

    for phrase in [
        "Prompts 49-51 audited",
        "no active UI",
        "no frontend implementation",
        "no desktop UI implementation",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no execution APIs",
        "Retail Dashboard Milestone Audit",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_retail_dashboard_safety_boundary_audit_docs_are_audit_only() -> None:
    audit = (ROOT / "docs/RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md").read_text(encoding="utf-8")

    for phrase in [
        "consolidation only",
        "adds no active Retail Dashboard UI",
        "ready for Retail Dashboard Milestone Audit only",
    ]:
        assert phrase in audit
