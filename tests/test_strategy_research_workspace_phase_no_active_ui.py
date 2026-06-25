from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]


def test_strategy_research_workspace_phase_has_no_frontend_or_desktop_files() -> None:
    frontend_matches = [
        path
        for path in ROOT.rglob("*strategy*research*workspace*")
        if ".git" not in path.parts
        and "node_modules" not in path.parts
        and any(part in {"frontend", "web", "ui"} for part in path.parts)
    ]
    desktop_matches = [
        path
        for path in (ROOT / "apps/desktop").rglob("*strategy*research*workspace*")
        if path.is_file()
    ]

    assert frontend_matches == []
    assert desktop_matches == []


def test_strategy_research_workspace_phase_has_no_active_render_functions() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for package in PACKAGES
        for path in package.glob("*.py")
    )

    assert "def render_active_workspace" not in combined
    assert "def create_active_widget" not in combined
    assert "active_ui: bool = True" not in combined


def test_strategy_research_workspace_phase_no_active_ui_doc_is_explicit() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    )
    assert "No active Strategy Research Workspace UI exists" in text
    assert "all artifacts remain backend contracts" in text
