from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_prompt_14_docs_exist() -> None:
    for path in [
        "docs/SYNTHETIC_MARKET_DATA_FIXTURES.md",
        "docs/OHLCV_FIXTURE_CONTRACTS.md",
        "docs/SAMPLE_DATA_POLICY.md",
    ]:
        assert (ROOT / path).exists()


def test_prompt_14_docs_contain_required_status() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))

    for phrase in [
        "synthetic",
        "OHLCV",
        "local-only",
        "test/dev only",
        "no real market data",
        "no execution APIs",
        "no market data ingestion",
        "no external calls",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_prompt_14_status_docs_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 25" in north_star
    assert "Completed Prompts: 25 before this prompt, 26 after completion" in north_star
    assert "Fixture Status: Synthetic local-only test/dev fixtures implemented and audited" in north_star
    assert "fixtures/" in project_map
    assert "Prompt 14 - Sample Market Data Fixtures + Synthetic OHLCV Contracts" in prompt_log
