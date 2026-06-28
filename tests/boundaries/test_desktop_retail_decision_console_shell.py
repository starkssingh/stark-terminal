from pathlib import Path

from stark_terminal_desktop import retail_decision_console
from stark_terminal_desktop.retail_decision_console import (
    RetailDecisionConsoleDesktopFallback,
    create_retail_decision_console_shell,
    create_retail_decision_console_window,
    pyside6_available,
)


ROOT = Path(__file__).resolve().parents[2]


def test_desktop_retail_decision_console_module_imports_safely() -> None:
    descriptor = retail_decision_console.retail_decision_console_shell_descriptor()

    assert descriptor.title == "Stark Terminal — Retail Decision Console"
    assert descriptor.stage == "ui_shell_skeleton"
    assert descriptor.safety_banner == "Skeleton only — no live data, no recommendations, no execution"
    assert descriptor.live_data_enabled is False
    assert descriptor.recommendations_enabled is False
    assert descriptor.confidence_scoring_enabled is False
    assert descriptor.decision_object_generation_enabled is False
    assert descriptor.broker_controls_enabled is False
    assert descriptor.order_buttons_enabled is False
    assert descriptor.execution_enabled is False


def test_desktop_retail_decision_console_fallback_is_safe_without_running_qapplication() -> None:
    shell = create_retail_decision_console_shell()
    window_or_fallback = create_retail_decision_console_window()

    assert shell.descriptor.skeleton_only is True
    assert shell.descriptor.sections
    if isinstance(window_or_fallback, RetailDecisionConsoleDesktopFallback):
        assert window_or_fallback.descriptor.skeleton_only is True
        assert window_or_fallback.view_model.demo_only is True
        assert window_or_fallback.view_model.unavailable is True
        assert "descriptor" in window_or_fallback.reason.lower() or "view-model" in window_or_fallback.reason.lower()
        assert window_or_fallback.pyside6_available in {True, False}
    else:
        assert pyside6_available() is True
        assert window_or_fallback.windowTitle() == "Stark Terminal — Retail Decision Console"


def test_desktop_retail_decision_console_source_has_no_fetch_threads_or_execution_controls() -> None:
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
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
    ]
    for term in forbidden_source_terms:
        assert term not in source
