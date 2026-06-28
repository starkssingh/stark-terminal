from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py"
client = TestClient(app)


def _display_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in [*DISPLAY_PACKAGE.glob("*.py"), DISPLAY_ROUTE]
    )


def test_research_artifact_registry_display_remains_contract_skeleton_only() -> None:
    response = client.get("/research-artifact-registry-display/contracts")
    body = response.json()

    assert response.status_code == 200
    assert body["display_contract_skeleton_only"] is True
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["active_ui_enabled"] is False
    assert body["frontend_components_enabled"] is False
    assert body["desktop_components_enabled"] is False
    assert body["active_ingestion_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["execution_enabled"] is False


def test_research_artifact_registry_display_has_no_active_rendering_or_controls() -> None:
    text = _display_source()
    for phrase in [
        "def render_artifact_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def preview_file",
        "def display_backtest_result",
        "def display_recommendation",
        "def create_order_button",
        "def execute_trade",
    ]:
        assert phrase not in text


def test_research_artifact_registry_display_boundary_doc_lists_required_scope() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()

    for phrase in [
        "display contract skeleton exists",
        "display metadata placeholders exist",
        "artifact card placeholders exist",
        "provenance display placeholders exist",
        "lifecycle badge placeholders exist",
        "unavailable display responses exist",
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no file preview",
        "no parsed-paper display path",
        "no generated-strategy display path",
        "no backtest-result display path",
        "no recommendation display path",
        "no execution display path",
    ]:
        assert phrase in text
