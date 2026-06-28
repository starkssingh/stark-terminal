from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

from stark_terminal_desktop import retail_decision_console
from stark_terminal_desktop.retail_decision_console import (
    RetailDecisionConsoleDesktopFallback,
    create_retail_decision_console_shell,
    create_retail_decision_console_window,
)


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/preview_retail_decision_console.py"


def _load_preview_module():
    spec = spec_from_file_location("preview_retail_decision_console", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_desktop_shell_exposes_visual_layout_without_requiring_pyside6() -> None:
    shell = create_retail_decision_console_shell()
    view_model = retail_decision_console.retail_decision_console_shell_view_model()
    window_or_fallback = create_retail_decision_console_window()

    assert shell.descriptor.stage == "ui_shell_skeleton"
    assert view_model.layout.stage == "visual_layout_pass"
    assert view_model.layout.zones
    assert view_model.layout.sections
    assert "Demo/static shell only" in view_model.safety_banner
    assert {section.layout_zone.value for section in view_model.sections} >= {
        "HEADER",
        "CONTROLS",
        "PRIMARY",
        "SECONDARY",
        "CONTEXT",
        "FOOTER",
    }
    if isinstance(window_or_fallback, RetailDecisionConsoleDesktopFallback):
        assert window_or_fallback.view_model.layout.stage == "visual_layout_pass"
        assert window_or_fallback.view_model.demo_only is True
        assert window_or_fallback.view_model.unavailable is True
    else:
        assert window_or_fallback.windowTitle() == "Stark Terminal — Retail Decision Console"


def test_desktop_visual_layout_source_has_no_import_side_effects_or_execution_controls() -> None:
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


def test_preview_no_gui_prints_visual_layout_summary(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_preview_module()

    result = module.main(["--no-gui"])
    output = capsys.readouterr().out

    assert result == 0
    assert "Demo/static preview only — no live data, no recommendations, no execution" in output
    assert "Layout stage: visual_layout_pass" in output
    assert "Layout zones:" in output
    assert "[CONTROLS] Instrument selector placeholder" in output
    assert "[PRIMARY] Decision summary placeholder" in output
    assert "[SECONDARY] Evidence panel placeholder" in output
    assert "[CONTEXT] Research context placeholder" in output
    assert "[FOOTER] Settings placeholder" in output
