from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_prompt_16_docs_exist() -> None:
    assert (ROOT / "docs/MARKET_DATA_BATCH_PERSISTENCE.md").exists()
    assert (ROOT / "docs/BATCH_METADATA_POLICY.md").exists()


def test_prompt_16_docs_contain_required_boundaries() -> None:
    combined = "\n".join(
        [
            (ROOT / "docs/MARKET_DATA_BATCH_PERSISTENCE.md").read_text(encoding="utf-8"),
            (ROOT / "docs/BATCH_METADATA_POLICY.md").read_text(encoding="utf-8"),
        ]
    )

    for phrase in [
        "Market Data Batch Persistence",
        "batch metadata",
        "validation-before-persistence",
        "synthetic",
        "no full OHLCV bars",
        "no real market ingestion",
        "no external calls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in combined


def test_prompt_16_status_docs_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Market Data Batch Persistence" in north_star
    assert "Prompt 16 - Market Data Batch Persistence Contracts" in prompt_log
    assert "MarketDataBatchRecordORM" in project_map
    assert "MarketDataBatchMetadataService" in project_map
