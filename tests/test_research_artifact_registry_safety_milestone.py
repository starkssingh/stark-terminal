from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def _walk(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            items.append((key, child))
            items.extend(_walk(child))
    elif isinstance(value, list):
        for child in value:
            items.extend(_walk(child))
    return items


def test_prompt_73_safety_docs_exist_and_are_referenced() -> None:
    milestone = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_MILESTONE_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for doc in [
        "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_BOUNDARY_AUDIT.md",
        "docs/RESEARCH_ARTIFACT_REGISTRY_API_BOUNDARY_AUDIT.md",
        "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_BOUNDARY_AUDIT.md",
    ]:
        assert (ROOT / doc).exists()
    assert "Prompt 73 safety boundary audit is complete" in milestone


def test_dangerous_flags_false_across_research_artifact_health_endpoints() -> None:
    for endpoint in [
        "/research-artifact-registry/health",
        "/research-artifact-registry-api/health",
        "/research-artifact-registry-display/health",
    ]:
        body = client.get(endpoint).json()
        for key, value in _walk(body):
            if key.endswith("_enabled") and key not in {"enabled"}:
                assert value is False, (endpoint, key, value)


def test_safety_milestone_doc_states_path_prohibitions() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_MILESTONE_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "unavailable-by-default behavior remains intact",
        "no artifact-to-strategy path",
        "no artifact-to-backtest path",
        "no artifact-as-recommendation path",
        "no artifact-as-execution-control path",
        "no active registry implementation",
        "no ingestion/storage/upload/download",
        "no broker controls",
        "no readiness-to-trade",
    ]:
        assert phrase in text
