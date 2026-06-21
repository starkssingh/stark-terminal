from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_lake_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/RESEARCH_LAKE_FOUNDATION.md").exists()
    assert (ROOT / "docs/PARQUET_DATA_ZONES.md").exists()
    assert (ROOT / "docs/DUCKDB_FOUNDATION.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 04 - DuckDB + Parquet Research Lake Foundation" in prompt_log
    assert "Current Prompt: 13" in north_star
    assert "Completed Prompts: 13 before this prompt, 14 after completion" in north_star
    assert "research_lake.py" in project_map
