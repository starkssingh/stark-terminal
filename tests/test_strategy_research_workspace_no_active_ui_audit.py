from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]


def _strategy_research_code() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for package in PACKAGES
        for path in package.glob("*.py")
    )


def test_strategy_research_workspace_no_frontend_or_desktop_ui_files_added() -> None:
    frontend_matches = [
        path
        for path in ROOT.rglob("*strategy*research*workspace*")
        if "node_modules" not in path.parts
        and ".git" not in path.parts
        and any(part in {"frontend", "web", "ui"} for part in path.parts)
    ]
    desktop_matches = [
        path
        for path in (ROOT / "apps/desktop").rglob("*strategy*research*workspace*")
        if path.is_file()
    ]

    assert frontend_matches == []
    assert desktop_matches == []


def test_strategy_research_workspace_has_no_active_workspace_render_functions() -> None:
    combined = _strategy_research_code()

    for forbidden in [
        "def render_active_workspace",
        "def mount_workspace_ui",
        "def create_frontend_component",
        "def create_desktop_component",
        "ui_active=True",
        "active_ui=True",
    ]:
        assert forbidden not in combined


def test_strategy_research_workspace_placeholder_modules_remain_placeholders() -> None:
    combined = _strategy_research_code()

    for safe_label in [
        "planning_only",
        "api_contract_skeleton_only",
        "display_contract_only",
        "unavailable",
    ]:
        assert safe_label in combined


def test_strategy_research_workspace_no_active_ui_docs_state_boundary() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "No active Strategy Research Workspace UI exists",
        "No frontend Strategy Research Workspace components were added",
        "No desktop Strategy Research Workspace components were added",
        "No rendered workspace layout exists",
        "No active widgets exist",
        "contracts/placeholders only",
    ]:
        assert phrase in text
