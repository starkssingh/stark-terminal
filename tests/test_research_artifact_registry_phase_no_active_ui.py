from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display"


def test_phase_has_no_frontend_desktop_or_active_render_functions() -> None:
    frontend_matches = [
        path for path in ROOT.rglob("*research_artifact_registry*") if "frontend" in path.parts
    ]
    desktop_matches = [
        path for path in ROOT.rglob("*research_artifact_registry*") if "desktop" in path.parts
    ]
    assert frontend_matches == []
    assert desktop_matches == []

    source = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))
    for phrase in [
        "def render_artifact_ui",
        "def render_card",
        "def create_frontend_component",
        "def create_desktop_widget",
        "class ArtifactBrowser",
        "class ActiveWidget",
    ]:
        assert phrase not in source


def test_phase_no_active_ui_doc_states_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no rendered cards",
        "no active widgets",
        "no artifact browser ui",
        "display contracts remain backend placeholders only",
    ]:
        assert phrase in text
