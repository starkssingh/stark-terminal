from __future__ import annotations

from pathlib import Path

from stark_terminal_core.retail_dashboard_display.layouts import (
    default_retail_dashboard_layout_placeholders,
)
from stark_terminal_core.retail_dashboard_display.sections import (
    default_retail_dashboard_visual_section_placeholders,
)
from stark_terminal_core.retail_dashboard_display.widgets import (
    default_retail_dashboard_widget_placeholders,
)


ROOT = Path(__file__).resolve().parents[1]


def test_no_frontend_or_desktop_retail_dashboard_files_added() -> None:
    forbidden_paths = [
        ROOT / "apps/web/retail_dashboard",
        ROOT / "apps/web/retail-dashboard",
        ROOT / "frontend/retail_dashboard",
        ROOT / "frontend/retail-dashboard",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard_display.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard_display",
    ]
    for path in forbidden_paths:
        assert not path.exists(), path


def test_no_active_dashboard_render_functions_exist() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_dashboard",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
        ]
        for path in root.glob("*.py")
    )
    for phrase in [
        "def render_dashboard",
        "def render_active_widget",
        "def build_active_dashboard",
        "class RetailDashboardWindow",
        "class RetailDashboardWidget(",
    ]:
        assert phrase not in text


def test_display_placeholders_remain_placeholders() -> None:
    for layout in default_retail_dashboard_layout_placeholders():
        assert layout.active_ui is False
        assert layout.rendered_now is False
        assert layout.display_contract_only is True

    for section in default_retail_dashboard_visual_section_placeholders():
        assert section.active_ui is False
        assert section.rendered_now is False
        assert section.display_contract_only is True

    for widget in default_retail_dashboard_widget_placeholders():
        assert widget.active_ui is False
        assert widget.rendered_now is False
        assert widget.display_contract_only is True


def test_phase_no_active_ui_doc_states_contracts_only() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_PHASE_NO_ACTIVE_UI_AUDIT.md").read_text(encoding="utf-8")
    assert "no active Retail Dashboard UI exists" in text
    assert "No frontend dashboard files exist" in text
    assert "No desktop dashboard files exist" in text
    assert "backend contracts, placeholders, documentation, tests" in text
