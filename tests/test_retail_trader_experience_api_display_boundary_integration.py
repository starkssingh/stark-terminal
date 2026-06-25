from __future__ import annotations

from pathlib import Path

from stark_terminal_core.retail_trader_experience_api.responses import (
    default_retail_trader_experience_api_response_placeholder,
)
from stark_terminal_core.retail_trader_experience_display.badges import (
    default_retail_trader_experience_display_badges,
)
from stark_terminal_core.retail_trader_experience_display.journeys import (
    default_retail_trader_experience_display_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.personas import (
    default_retail_trader_experience_display_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.sections import (
    default_retail_trader_experience_display_section_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    default_retail_trader_experience_display_widget_placeholders,
)


ROOT = Path(__file__).resolve().parents[1]


def test_api_and_display_outputs_remain_placeholders_only() -> None:
    response = default_retail_trader_experience_api_response_placeholder()
    assert response.api_contract_skeleton_only is True
    assert response.recommendation_generated is False
    assert response.action_generated is False
    assert response.confidence_generated is False
    assert response.decision_object_generated is False
    assert response.readiness_to_trade_generated is False
    assert response.suitability_profile_generated is False
    assert response.execution_ready is False

    for persona in default_retail_trader_experience_display_persona_placeholders():
        assert persona.display_contract_only is True
        assert persona.active_ui is False
        assert persona.rendered_now is False
        assert persona.suitability_profile is False
        assert persona.execution_allowed is False

    for journey in default_retail_trader_experience_display_journey_placeholders():
        assert journey.display_contract_only is True
        assert journey.active_ui is False
        assert journey.rendered_now is False
        assert journey.trading_advice_journey is False
        assert journey.execution_journey is False

    for section in default_retail_trader_experience_display_section_placeholders():
        assert section.display_contract_only is True
        assert section.active_ui is False
        assert section.rendered_now is False
        assert section.suitability_profiling_allowed is False
        assert section.execution_allowed is False

    for widget in default_retail_trader_experience_display_widget_placeholders():
        assert widget.display_contract_only is True
        assert widget.recommendation_widget is False
        assert widget.confidence_widget is False
        assert widget.suitability_profile_widget is False
        assert widget.execution_widget is False

    for badge in default_retail_trader_experience_display_badges():
        assert badge.active_ui is False
        assert badge.recommendation is False
        assert badge.suitability_profile is False
        assert badge.execution_ready is False


def test_no_api_to_display_recommendation_suitability_or_execution_path_is_documented() -> None:
    text = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_API_DISPLAY_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "API-to-display recommendation path",
        "API-to-active-UI path",
        "market-data-to-display-decision endpoint",
        "display-to-decision path",
        "persona-to-suitability-profile path",
        "journey-to-trading-advice path",
        "display-to-execution path",
        "execution controls",
    ]:
        assert phrase in text


def test_retail_trader_experience_api_display_packages_do_not_define_active_generation_functions() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
        ]
        for path in root.glob("*.py")
    )
    for forbidden in [
        "def generate_trader_recommendation",
        "def build_active_experience",
        "def create_order_button",
        "def generate_decision_object",
        "def generate_recommendation",
        "def score_confidence",
        "def render_active_experience",
        "def generate_readiness_status",
        "def build_suitability_profile",
    ]:
        assert forbidden not in source

