from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_strategy_research_workspace_frontend_or_desktop_ui_files_added() -> None:
    frontend_roots = [ROOT / "apps/web", ROOT / "frontend", ROOT / "packages/ui"]
    for root in frontend_roots:
        if root.exists():
            matches = list(root.rglob("*strategy*research*workspace*"))
            assert not matches

    desktop_root = ROOT / "apps/desktop"
    matches = [
        path
        for path in desktop_root.rglob("*")
        if path.is_file() and "strategy_research_workspace" in path.name.lower()
    ]
    assert matches == []


def test_display_package_remains_backend_contract_skeleton() -> None:
    display_root = ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display"
    forbidden_functions = [
        "def render_active_workspace",
        "def build_active_workspace",
        "def create_workspace_page",
        "def create_order_button",
    ]
    for path in display_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden_functions:
            assert phrase not in text


def test_no_active_ui_integration_doc_is_explicit() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No active Strategy Research Workspace UI exists",
        "No frontend implementation exists",
        "No desktop implementation exists",
        "No Research Artifact Registry UI exists",
        "No active widgets exist",
        "No active layout rendering exists",
    ]:
        assert phrase in text
