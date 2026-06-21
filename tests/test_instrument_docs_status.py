from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_instrument_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/INSTRUMENT_MASTER_FOUNDATION.md").exists()
    assert (ROOT / "docs/MARKET_DATA_PROVIDER_CONTRACTS.md").exists()
    assert (ROOT / "docs/SYMBOL_NORMALIZATION_POLICY.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 08 - Instrument Master + Market Data Contracts" in prompt_log
    assert "Current Prompt: 16" in north_star
    assert "Completed Prompts: 16 before this prompt, 17 after completion" in north_star
    assert "instruments/normalization.py" in project_map
    assert "Market Data Provider" in project_map
