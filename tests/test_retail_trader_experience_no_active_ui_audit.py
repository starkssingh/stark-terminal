from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
]


def _code_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for root in PACKAGE_ROOTS
        for path in root.glob("*.py")
    ).lower()


def test_no_frontend_or_desktop_retail_trader_experience_files_exist() -> None:
    frontend_roots = [
        ROOT / "frontend",
        ROOT / "web",
        ROOT / "ui",
        ROOT / "apps/web",
        ROOT / "apps/frontend",
    ]
    desktop_roots = [ROOT / "apps/desktop"]

    frontend_matches = [
        path
        for root in frontend_roots
        if root.exists()
        for path in root.rglob("*retail_trader_experience*")
    ]
    desktop_matches = [
        path
        for root in desktop_roots
        if root.exists()
        for path in root.rglob("*retail_trader_experience*")
    ]

    assert frontend_matches == []
    assert desktop_matches == []


def test_no_active_experience_render_functions_exist() -> None:
    text = _code_text()

    for forbidden in [
        "def render_active_experience",
        "def build_active_experience",
        "def render_trader_experience",
        "def create_order_button",
        "react",
        "jsx",
        "from pyside6",
        "import pyside6",
        "from tkinter",
        "import tkinter",
    ]:
        assert forbidden not in text


def test_retail_trader_experience_routes_do_not_create_active_ui_surfaces() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience"):
            assert "active-ui" not in path
            assert "render" not in path
            assert "component" not in path
            assert "screen" not in path
            assert "widget-action" not in path


def test_no_active_ui_audit_docs_are_explicit() -> None:
    text = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()

    for phrase in [
        "no active retail trader experience ui exists",
        "no frontend trader experience components were added",
        "no desktop trader experience components were added",
        "no rendered experience layout exists",
        "no active widgets exist",
        "contracts/placeholders only",
    ]:
        assert phrase in text

