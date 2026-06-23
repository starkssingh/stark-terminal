from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_ohlcv_storage_docs_exist_and_state_boundaries() -> None:
    foundation = ROOT / "docs/SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md"
    policy = ROOT / "docs/TIMESCALE_SYNTHETIC_STORAGE_POLICY.md"

    assert foundation.exists()
    assert policy.exists()

    text = foundation.read_text(encoding="utf-8") + "\n" + policy.read_text(encoding="utf-8")
    for phrase in [
        "Synthetic OHLCV Storage",
        "TimescaleDB",
        "validation-before-storage",
        "LOCAL_SAMPLE",
        "no real market data",
        "no real market ingestion",
        "no external calls",
        "no execution APIs",
        "no trading signals",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_18_status_docs_and_project_map_are_current() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Current Prompt: 36" in north_star
    assert "Synthetic OHLCV Storage Status" in north_star
    assert "Prompt 18 - TimescaleDB Synthetic OHLCV Storage Foundation" in prompt_log
    assert "OHLCVBarRepository" in project_map
    assert "SyntheticOHLCVStorageService" in project_map
    assert "synthetic_ohlcv_storage.py" in project_map
