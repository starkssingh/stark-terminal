from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_artifact_registry_packages_keep_declared_boundary_roles() -> None:
    package_readmes = {
        "planning": ROOT / "packages/core/stark_terminal_core/research_artifact_registry/README.md",
        "api": ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api/README.md",
        "display": ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display/README.md",
        "boundary": ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary/README.md",
    }
    for label, path in package_readmes.items():
        assert path.exists(), label
        text = path.read_text(encoding="utf-8").lower()
        assert "no execution" in text
        assert "no strategy" in text

    assert "planning" in package_readmes["planning"].read_text(encoding="utf-8").lower()
    assert "api contract skeleton" in package_readmes["api"].read_text(encoding="utf-8").lower()
    assert "display contract skeleton" in package_readmes["display"].read_text(encoding="utf-8").lower()
    assert "boundary" in package_readmes["boundary"].read_text(encoding="utf-8").lower()


def test_api_display_boundary_docs_forbid_active_paths() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No active display rendering",
        "No active artifact cards",
        "No file-preview display path",
        "No parsed-paper display path",
        "No generated-strategy display path",
        "No backtest-result display path",
        "No recommendation-to-display path",
        "No readiness-to-trade display path",
        "No artifact-to-strategy path",
        "No execution controls",
    ]:
        assert phrase in text


def test_no_artifact_to_recommendation_display_endpoint_exists() -> None:
    routes_root = ROOT / "apps/api/stark_terminal_api/routes"
    for path in routes_root.glob("research_artifact_registry*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "artifact-to-recommendation",
            "artifact_to_recommendation",
            "market-data-to-recommendation",
            "market_data_to_recommendation",
            "@router.get(\"/file-preview",
            "@router.get('/file-preview",
            "def preview_file",
            "@router.post",
        ]:
            assert phrase not in text, f"{path.name}:{phrase}"
