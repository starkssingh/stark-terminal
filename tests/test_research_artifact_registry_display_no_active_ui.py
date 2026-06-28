from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py"


def _source_text() -> str:
    paths = list(PACKAGE_ROOT.glob("*.py")) + [ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_no_frontend_or_desktop_research_artifact_registry_display_files() -> None:
    candidates = [
        *ROOT.glob("apps/web/**/*research_artifact_registry_display*"),
        *ROOT.glob("apps/frontend/**/*research_artifact_registry_display*"),
        *ROOT.glob("apps/desktop/**/*research_artifact_registry_display*"),
        *ROOT.glob("apps/desktop/**/*research-artifact-registry-display*"),
    ]

    assert candidates == []


def test_display_package_has_no_active_render_functions() -> None:
    text = _source_text()
    forbidden = [
        "def render_artifact_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def render_layout",
        "def preview_file",
    ]

    for phrase in forbidden:
        assert phrase not in text


def test_display_docs_state_no_active_ui() -> None:
    docs = [
        ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_CONTRACT_SKELETON.md",
        ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_ACTIVE_UI_POLICY.md",
    ]
    combined = " ".join(path.read_text(encoding="utf-8").lower() for path in docs)

    assert "no active ui" in combined
    assert "no frontend" in combined or "frontend components" in combined
    assert "desktop" in combined
