from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py"
client = TestClient(app)


def test_research_artifact_registry_display_remains_display_contract_skeleton_only() -> None:
    response = client.get("/research-artifact-registry-display/contracts")
    body = response.json()

    assert response.status_code == 200
    assert body["display_contract_skeleton_only"] is True
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["active_ui_enabled"] is False
    assert body["frontend_components_enabled"] is False
    assert body["desktop_components_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["execution_enabled"] is False


def test_research_artifact_registry_display_has_no_active_rendering_paths() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [*DISPLAY_PACKAGE.glob("*.py"), DISPLAY_ROUTE]
    )
    for phrase in [
        "def render_artifact_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def preview_file",
        "def display_parsed_paper",
        "def display_generated_strategy",
        "def display_backtest_result",
        "def display_recommendation",
        "def execute_trade",
    ]:
        assert phrase not in source


def test_display_milestone_doc_states_required_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_MILESTONE_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "display contract skeleton exists",
        "display metadata placeholders exist",
        "artifact card placeholders exist",
        "reference display placeholders exist",
        "provenance display placeholders exist",
        "lifecycle badge placeholders exist",
        "unavailable display responses exist",
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no file preview",
        "no parsed-paper display",
        "no generated-strategy display",
        "no backtest-result display",
        "no recommendation display",
        "no execution display",
    ]:
        assert phrase in text
