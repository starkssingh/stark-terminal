from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_warehouse_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/CLICKHOUSE_WAREHOUSE_FOUNDATION.md").exists()
    assert (ROOT / "docs/ANALYTICAL_TABLE_CONTRACTS.md").exists()
    assert (ROOT / "docs/WAREHOUSE_QUERY_POLICY.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 09 - ClickHouse Analytical Warehouse Foundation" in prompt_log
    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "warehouse/tables.py" in project_map
    assert "ClickHouse Warehouse foundation" in project_map
