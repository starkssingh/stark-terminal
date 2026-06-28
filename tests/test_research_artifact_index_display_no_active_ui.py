from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_index_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py"


def test_research_artifact_index_display_adds_no_active_ui_functions() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))

    for forbidden in [
        "def render_index_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def preview_file",
        "QWidget",
        "QMainWindow",
        "React",
    ]:
        assert forbidden not in source


def test_research_artifact_index_display_adds_no_frontend_or_desktop_files() -> None:
    for path in ROOT.rglob("*artifact_index*"):
        path_text = str(path).replace("\\", "/")
        assert "/apps/frontend/" not in path_text
        assert "/apps/desktop/" not in path_text


def test_research_artifact_index_display_adds_no_active_ui_routes() -> None:
    route_source = DISPLAY_ROUTE.read_text(encoding="utf-8")

    assert "@router.post" not in route_source
    for forbidden in ["render", "widget", "frontend", "desktop", "preview"]:
        assert f'@router.get("/research-artifact-index-display/{forbidden}' not in route_source
