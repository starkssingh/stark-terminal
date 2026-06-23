from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/core/stark_terminal_core/retail_dashboard_boundary"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/retail_dashboard_boundary.py"


def test_retail_dashboard_boundary_adds_no_frontend_or_desktop_ui_files() -> None:
    ui_candidates = [
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard_boundary.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard_boundary",
        ROOT / "apps/web/retail_dashboard",
        ROOT / "apps/web/retail-dashboard",
        ROOT / "frontend/retail-dashboard",
        ROOT / "frontend/retail_dashboard",
    ]
    for path in ui_candidates:
        assert not path.exists()


def test_retail_dashboard_boundary_does_not_create_active_ui_or_broker_controls() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in [*PACKAGE.glob("*.py"), ROUTE])
    forbidden_names = [
        "def build_active_dashboard",
        "def render_active_widget",
        "def create_order_button",
        "class Broker",
        "broker_control_enabled=True",
        "active_ui_generated=True",
        "frontend_component_generated=True",
        "desktop_component_generated=True",
        "executes_trade=True",
    ]
    for name in forbidden_names:
        assert name not in text


def test_retail_dashboard_boundary_docs_state_no_active_ui_or_broker_controls() -> None:
    docs = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETAIL_DASHBOARD_SYSTEM_BOUNDARY_HARDENING.md",
            "docs/RETAIL_DASHBOARD_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
            "docs/RETAIL_DASHBOARD_BOUNDARY_NO_EXECUTION_POLICY.md",
        ]
    )
    for phrase in [
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no broker controls",
        "no execution APIs",
    ]:
        assert phrase in docs
