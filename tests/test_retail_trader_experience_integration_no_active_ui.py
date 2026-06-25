from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_frontend_or_desktop_retail_trader_experience_files_exist() -> None:
    frontend_roots = [ROOT / "apps/web", ROOT / "apps/frontend", ROOT / "frontend"]
    for root in frontend_roots:
        if root.exists():
            assert not [
                path for path in root.rglob("*retail_trader_experience*") if path.is_file()
            ]

    desktop_root = ROOT / "apps/desktop"
    assert not [
        path
        for path in desktop_root.rglob("*retail_trader_experience*")
        if path.is_file() and "__pycache__" not in path.parts
    ]


def test_no_active_experience_render_functions_exist() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary",
        ]
        for path in root.glob("*.py")
    )
    for forbidden in [
        "def render_experience",
        "def render_active_experience",
        "def render_active_widget",
        "def build_active_experience",
        "def mount_experience",
        "def create_order_button",
    ]:
        assert forbidden not in source


def test_integration_docs_explicitly_state_no_active_ui() -> None:
    text = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No active Retail Trader Experience UI exists",
        "No frontend trader experience implementation exists",
        "No desktop trader experience implementation exists",
        "No active layout rendering exists",
        "No active widgets exist",
        "contracts, placeholders, unavailable responses",
    ]:
        assert phrase in text

