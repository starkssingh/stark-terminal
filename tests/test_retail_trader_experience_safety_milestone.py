from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

HEALTH_ENDPOINTS = [
    "/retail-trader-experience/health",
    "/retail-trader-experience-api/health",
    "/retail-trader-experience-display/health",
]


def test_prompt_59_audit_docs_are_present_and_referenced() -> None:
    for path in [
        "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_BOUNDARY_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
        "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
    ]:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        assert "Prompt 60 Milestone Audit Confirmation" in text


def test_health_endpoints_keep_dangerous_flags_false() -> None:
    for endpoint in HEALTH_ENDPOINTS:
        payload = client.get(endpoint).json()
        assert payload["status"] == "healthy"
        for key in [
            "active_ui_allowed",
            "frontend_components_allowed",
            "desktop_components_allowed",
            "recommendations_allowed",
            "action_generation_allowed",
            "confidence_scoring_allowed",
            "decision_object_generation_allowed",
            "readiness_to_trade_allowed",
            "broker_controls_allowed",
            "execution_allowed",
            "approval_allowed",
            "override_allowed",
            "suitability_profiling_allowed",
        ]:
            assert payload[key] is False, (endpoint, key)
        assert payload["returns_unavailable_by_default"] is True


def test_safety_policy_docs_include_core_phase_rules() -> None:
    text = "\n".join(
        open(path, encoding="utf-8").read().lower()
        for path in [
            "docs/DATA_POLICY.md",
            "docs/SAFETY_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_MILESTONE_AUDIT.md",
        ]
    )
    for phrase in [
        "no experience-as-recommendation",
        "no experience-as-execution-control",
        "no persona-as-suitability-profile",
        "no live data display",
        "no placeholder-as-trader-output",
    ]:
        assert phrase in text
