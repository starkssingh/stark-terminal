from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_core.retail_trader_experience_display.badges import (
    default_retail_trader_experience_display_badges,
)
from stark_terminal_core.retail_trader_experience_display.contracts import (
    default_retail_trader_experience_display_contract_metadata,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    default_retail_trader_experience_display_widget_placeholders,
)


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

DISPLAY_ENDPOINTS = [
    "/retail-trader-experience-display/health",
    "/retail-trader-experience-display/contracts",
    "/retail-trader-experience-display/unavailable-template",
    "/retail-trader-experience-display/placeholder-experience",
]


def test_retail_trader_experience_display_remains_contract_skeleton_only() -> None:
    metadata = default_retail_trader_experience_display_contract_metadata()
    assert metadata.returns_unavailable_by_default is True
    assert metadata.stage.value == "DISPLAY_CONTRACT_SKELETON"

    for flag in [
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
        assert getattr(metadata, flag) is False


def test_display_widgets_and_badges_are_not_active_surfaces() -> None:
    for widget in default_retail_trader_experience_display_widget_placeholders():
        assert widget.display_contract_only is True
        assert widget.active_ui is False
        assert widget.rendered_now is False
        assert widget.recommendation_widget is False
        assert widget.confidence_widget is False
        assert widget.decision_object_widget is False
        assert widget.readiness_to_trade_widget is False
        assert widget.suitability_profile_widget is False
        assert widget.execution_widget is False

    for badge in default_retail_trader_experience_display_badges():
        assert badge.active_ui is False
        assert badge.unavailable is True
        assert badge.recommendation is False
        assert badge.confidence_signal is False
        assert badge.decision_object_signal is False
        assert badge.readiness_to_trade is False
        assert badge.suitability_profile is False
        assert badge.execution_ready is False


def test_retail_trader_experience_display_endpoints_are_read_only_placeholders() -> None:
    for path in DISPLAY_ENDPOINTS:
        response = client.get(path)
        assert response.status_code == 200, path
        assert client.post(path).status_code in {404, 405}, path
        serialized = json.dumps(response.json()).lower()
        for snippet in [
            '"recommendation_generated": true',
            '"confidence_generated": true',
            '"decision_object_generated": true',
            '"readiness_to_trade_generated": true',
            '"suitability_profile_generated": true',
            '"execution_ready": true',
        ]:
            assert snippet not in serialized, (path, snippet)


def test_no_frontend_or_desktop_retail_trader_experience_display_files_exist() -> None:
    ui_roots = [
        ROOT / "frontend",
        ROOT / "web",
        ROOT / "ui",
        ROOT / "apps/web",
        ROOT / "apps/frontend",
        ROOT / "apps/desktop",
    ]
    matches: list[str] = []
    for root in ui_roots:
        if root.exists():
            matches.extend(
                str(path.relative_to(ROOT))
                for path in root.rglob("*retail_trader_experience*")
                if path.is_file()
            )
    assert matches == []
