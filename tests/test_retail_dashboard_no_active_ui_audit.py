from __future__ import annotations

from pathlib import Path

from stark_terminal_core.retail_dashboard.cards import default_retail_dashboard_card_placeholders
from stark_terminal_core.retail_dashboard.sections import (
    default_retail_dashboard_section_placeholders,
)
from stark_terminal_core.retail_dashboard_display.badges import default_retail_dashboard_display_badges
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


def test_no_frontend_or_desktop_retail_dashboard_files_exist() -> None:
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


def test_dashboard_placeholders_remain_placeholders_not_active_ui() -> None:
    for section in default_retail_dashboard_section_placeholders():
        assert section.active_ui is False
        assert section.unavailable is True
        assert section.planning_only is True

    for card in default_retail_dashboard_card_placeholders():
        assert card.active_ui is False
        assert card.unavailable is True
        assert card.planning_only is True

    for layout in default_retail_dashboard_layout_placeholders():
        assert layout.active_ui is False
        assert layout.rendered_now is False
        assert layout.display_contract_only is True

    for widget in default_retail_dashboard_widget_placeholders():
        assert widget.active_ui is False
        assert widget.rendered_now is False
        assert widget.display_contract_only is True

    for section in default_retail_dashboard_visual_section_placeholders():
        assert section.active_ui is False
        assert section.rendered_now is False
        assert section.display_contract_only is True

    for badge in default_retail_dashboard_display_badges():
        assert badge.active_ui is False
        assert badge.unavailable is True


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


def test_no_active_ui_audit_doc_states_contracts_only() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_NO_ACTIVE_UI_AUDIT.md").read_text(encoding="utf-8")
    assert "No active Retail Dashboard UI exists" in text
    assert "No frontend dashboard components were added" in text
    assert "No desktop dashboard components were added" in text
    assert "contracts and placeholders only" in text
