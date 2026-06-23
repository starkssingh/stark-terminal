from __future__ import annotations

from pathlib import Path

from stark_terminal_core.retail_dashboard_display.badges import default_retail_dashboard_display_badges
from stark_terminal_core.retail_dashboard_display.contracts import (
    default_retail_dashboard_display_contract_metadata,
)
from stark_terminal_core.retail_dashboard_display.layouts import (
    default_retail_dashboard_layout_placeholders,
)
from stark_terminal_core.retail_dashboard_display.widgets import (
    default_retail_dashboard_widget_placeholders,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/core/stark_terminal_core/retail_dashboard_display"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/retail_dashboard_display.py"


def test_retail_dashboard_display_package_remains_display_contract_skeleton_only() -> None:
    metadata = default_retail_dashboard_display_contract_metadata()

    assert metadata.stage.value.lower() == "display_contract_skeleton"
    assert metadata.returns_unavailable_by_default is True
    assert metadata.active_ui_allowed is False
    assert metadata.recommendations_allowed is False
    assert metadata.action_generation_allowed is False
    assert metadata.confidence_scoring_allowed is False
    assert metadata.decision_object_generation_allowed is False
    assert metadata.readiness_to_trade_allowed is False
    assert metadata.broker_controls_allowed is False
    assert metadata.execution_allowed is False


def test_retail_dashboard_display_placeholders_are_not_rendered_ui() -> None:
    for layout in default_retail_dashboard_layout_placeholders():
        assert layout.active_ui is False
        assert layout.rendered_now is False
        assert layout.unavailable is True
        assert layout.execution_allowed is False

    for widget in default_retail_dashboard_widget_placeholders():
        assert widget.active_ui is False
        assert widget.rendered_now is False
        assert widget.unavailable is True
        assert widget.recommendation_widget is False
        assert widget.action_widget is False
        assert widget.confidence_widget is False
        assert widget.decision_object_widget is False
        assert widget.readiness_to_trade_widget is False
        assert widget.broker_control_widget is False
        assert widget.execution_widget is False


def test_retail_dashboard_display_badges_do_not_signal_trading_readiness() -> None:
    for badge in default_retail_dashboard_display_badges():
        assert badge.active_ui is False
        assert badge.unavailable is True
        assert badge.recommendation is False
        assert badge.action_signal is False
        assert badge.confidence_signal is False
        assert badge.decision_object_signal is False
        assert badge.readiness_to_trade is False
        assert badge.broker_control is False
        assert badge.execution_ready is False


def test_retail_dashboard_display_code_has_no_active_widgets_or_controls() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in [*PACKAGE.glob("*.py"), ROUTE])
    for phrase in [
        "def render_active_widget",
        "def build_active_dashboard",
        "def create_order_button",
        "def generate_dashboard_recommendation",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "@router.post",
    ]:
        assert phrase not in text
