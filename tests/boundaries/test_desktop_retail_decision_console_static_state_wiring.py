from pathlib import Path

from stark_terminal_desktop import retail_decision_console
from stark_terminal_desktop.retail_decision_console import (
    RetailDecisionConsoleDesktopFallback,
    create_retail_decision_console_shell,
    create_retail_decision_console_window,
    pyside6_available,
)


ROOT = Path(__file__).resolve().parents[2]


def test_desktop_retail_decision_console_static_state_view_model_imports_safely() -> None:
    view_model = retail_decision_console.retail_decision_console_shell_view_model()

    assert view_model.title == "Stark Terminal — Retail Decision Console"
    assert view_model.stage == "static_state_wired_shell"
    assert view_model.safety_banner == "Demo/static shell only — no live data, no recommendations, no execution"
    assert view_model.demo_only is True
    assert view_model.unavailable is True
    assert view_model.sections
    assert view_model.live_data_enabled is False
    assert view_model.recommendations_enabled is False
    assert view_model.confidence_scoring_enabled is False
    assert view_model.decision_object_generation_enabled is False
    assert view_model.broker_controls_enabled is False
    assert view_model.order_buttons_enabled is False
    assert view_model.execution_enabled is False


def test_desktop_shell_exposes_state_wiring_without_requiring_pyside6() -> None:
    shell = create_retail_decision_console_shell()
    window_or_fallback = create_retail_decision_console_window()

    assert shell.descriptor.stage == "ui_shell_skeleton"
    assert shell.view_model.stage == "static_state_wired_shell"
    assert shell.view_model.sections
    if isinstance(window_or_fallback, RetailDecisionConsoleDesktopFallback):
        assert window_or_fallback.descriptor.skeleton_only is True
        assert window_or_fallback.view_model.demo_only is True
        assert window_or_fallback.view_model.unavailable is True
        assert "view model" in window_or_fallback.reason.lower() or "view-model" in window_or_fallback.reason.lower()
        assert window_or_fallback.pyside6_available in {True, False}
    else:
        assert pyside6_available() is True
        assert window_or_fallback.windowTitle() == "Stark Terminal — Retail Decision Console"


def test_desktop_static_state_wiring_source_has_no_import_side_effects_or_execution_controls() -> None:
    source = (ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py").read_text(encoding="utf-8")
    forbidden_source_terms = [
        "requests.",
        "httpx.",
        "urllib",
        "QThread",
        "QTimer",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
    ]
    for term in forbidden_source_terms:
        assert term not in source
