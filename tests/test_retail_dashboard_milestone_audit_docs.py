from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    ROOT / "docs/RETAIL_DASHBOARD_MILESTONE_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_PLANNING_MILESTONE_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_API_MILESTONE_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_MILESTONE_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_SAFETY_MILESTONE_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_PHASE_NO_ACTIVE_UI_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    ROOT / "docs/RETAIL_DASHBOARD_NEXT_PHASE_PLAN.md",
]


def test_retail_dashboard_milestone_audit_docs_exist() -> None:
    for path in DOCS:
        assert path.exists(), path


def test_retail_dashboard_milestone_docs_state_required_boundaries() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)

    for phrase in [
        "Prompts 49-52 audited",
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
        "Retail Dashboard System Boundary Hardening",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_retail_dashboard_milestone_audit_is_audit_only() -> None:
    audit = (ROOT / "docs/RETAIL_DASHBOARD_MILESTONE_AUDIT.md").read_text(encoding="utf-8")

    for phrase in [
        "consolidation only",
        "adds no active Retail Dashboard UI",
        "ready for Retail Dashboard System Boundary Hardening only",
    ]:
        assert phrase in audit
