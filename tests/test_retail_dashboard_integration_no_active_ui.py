from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_frontend_or_desktop_retail_dashboard_files_exist() -> None:
    frontend_roots = [ROOT / "apps/web", ROOT / "apps/frontend", ROOT / "frontend"]
    for root in frontend_roots:
        if root.exists():
            assert not [path for path in root.rglob("*retail_dashboard*") if path.is_file()]

    desktop_root = ROOT / "apps/desktop"
    assert not [
        path
        for path in desktop_root.rglob("*retail_dashboard*")
        if path.is_file() and "__pycache__" not in path.parts
    ]


def test_no_active_dashboard_render_functions_exist() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_dashboard",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_boundary",
        ]
        for path in root.glob("*.py")
    )
    for forbidden in [
        "def render_dashboard",
        "def render_active_widget",
        "def build_active_dashboard",
        "def mount_dashboard",
        "def create_order_button",
    ]:
        assert forbidden not in source


def test_integration_docs_explicitly_state_no_active_ui() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_INTEGRATION_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "no active Retail Dashboard UI",
        "no frontend implementation",
        "no desktop implementation",
        "no active layout rendering",
        "no active widgets",
        "contracts, placeholders, unavailable responses",
    ]:
        assert phrase in text
