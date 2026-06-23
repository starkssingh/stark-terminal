from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_prompt_52_audit_docs_exist_and_are_referenced() -> None:
    safety_docs = [
        ROOT / "docs/RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_API_BOUNDARY_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_BOUNDARY_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_NO_ACTIVE_UI_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_NO_EXECUTION_AUDIT.md",
    ]
    milestone = (ROOT / "docs/RETAIL_DASHBOARD_SAFETY_MILESTONE_AUDIT.md").read_text(encoding="utf-8")

    for path in safety_docs:
        assert path.exists(), path
    assert "Prompt 52 Retail Dashboard Safety Boundary Audit" in milestone


def test_dangerous_flags_false_across_dashboard_health_endpoints() -> None:
    for endpoint in [
        "/retail-dashboard/health",
        "/retail-dashboard-api/health",
        "/retail-dashboard-display/health",
    ]:
        body = client.get(endpoint).json()
        assert body["active_ui_allowed"] is False
        assert body["recommendations_allowed"] is False
        assert body["action_generation_allowed"] is False
        assert body["confidence_scoring_allowed"] is False
        assert body["decision_object_generation_allowed"] is False
        assert body["readiness_to_trade_allowed"] is False
        assert body["broker_controls_allowed"] is False
        assert body["execution_allowed"] is False
        assert body["approval_allowed"] is False
        assert body["override_allowed"] is False
        assert body["returns_unavailable_by_default"] is True


def test_safety_milestone_rules_are_documented() -> None:
    docs_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETAIL_DASHBOARD_SAFETY_MILESTONE_AUDIT.md",
            "docs/DATA_POLICY.md",
            "docs/SAFETY_AUDIT.md",
        ]
    )
    for phrase in [
        "unavailable-by-default",
        "no dashboard-as-recommendation",
        "no dashboard-as-execution-control",
        "No live data display",
    ]:
        assert phrase in docs_text
