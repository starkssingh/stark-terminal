from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_boundary_adds_no_frontend_or_desktop_ui_files() -> None:
    forbidden_roots = [
        ROOT / "apps/frontend",
        ROOT / "frontend",
        ROOT / "packages/frontend",
    ]
    for root in forbidden_roots:
        if root.exists():
            matches = [path for path in root.rglob("*strategy*research*workspace*") if path.is_file()]
            assert matches == []

    desktop_root = ROOT / "apps/desktop"
    desktop_matches = [
        path
        for path in desktop_root.rglob("*strategy*research*workspace*")
        if path.is_file() and "strategy_research_workspace_boundary" not in path.as_posix()
    ]
    assert desktop_matches == []


def test_strategy_research_workspace_boundary_code_has_no_active_render_functions() -> None:
    code = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "packages/core/stark_terminal_core").rglob("*.py")
        if "strategy_research_workspace" in path.as_posix()
    )

    assert "def render_active_workspace" not in code
    assert "def create_order_button" not in code
    assert "active Strategy Research Workspace UI" not in code


def test_strategy_research_workspace_boundary_docs_state_no_active_ui() -> None:
    docs = (ROOT / "docs/STRATEGY_RESEARCH_BOUNDARY_NO_ACTIVE_UI_POLICY.md").read_text(
        encoding="utf-8"
    )

    assert "No active Strategy Research Workspace UI exists" in docs
    assert "No frontend implementation" in docs
    assert "desktop implementation" in docs
