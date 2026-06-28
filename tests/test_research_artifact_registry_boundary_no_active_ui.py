from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"


def test_boundary_has_no_active_ui_frontend_or_desktop_files() -> None:
    candidates = [
        path
        for path in ROOT.rglob("*research_artifact_registry_boundary*")
        if ".venv" not in path.parts
    ]
    bad = [
        path
        for path in candidates
        if "frontend" in path.parts
        or "desktop" in path.parts
        or "components" in path.parts
        or path.suffix in {".tsx", ".jsx", ".vue"}
    ]

    assert bad == []


def test_boundary_has_no_active_render_widget_or_page_functions() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
    for phrase in [
        "def render_artifact_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def render_card",
        "def create_page",
    ]:
        assert phrase not in text


def test_boundary_docs_state_no_active_ui_policy() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_ACTIVE_UI_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no active ui",
        "no frontend/desktop implementation",
        "no rendered cards",
        "no active widgets",
        "future prompt and audit required",
    ]:
        assert phrase in text

