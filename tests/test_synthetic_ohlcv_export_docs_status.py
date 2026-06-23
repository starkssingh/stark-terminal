from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_ohlcv_export_docs_exist_and_state_boundaries() -> None:
    foundation = ROOT / "docs/SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md"
    policy = ROOT / "docs/OHLCV_EXPORT_MANIFEST_POLICY.md"

    assert foundation.exists()
    assert policy.exists()

    text = foundation.read_text(encoding="utf-8") + "\n" + policy.read_text(encoding="utf-8")
    for phrase in [
        "Synthetic OHLCV Research Lake Export",
        "DatasetManifest",
        "Parquet",
        "DuckDB",
        "validation-before-export",
        "no real market data",
        "no real market ingestion",
        "no external calls",
        "no execution APIs",
        "no trading signals",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_19_status_docs_and_project_map_are_current() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Current Prompt: 36" in north_star
    assert "Synthetic OHLCV Export Status" in north_star
    assert "Prompt 19 - Synthetic OHLCV to Research Lake Export Contract" in prompt_log
    assert "SyntheticOHLCVResearchLakeExportService" in project_map
    assert "exports/synthetic_ohlcv.py" in project_map
    assert "synthetic_ohlcv_exports.py" in project_map
