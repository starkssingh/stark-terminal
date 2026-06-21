from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_timeseries_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/TIMESCALEDB_FOUNDATION.md").exists()
    assert (ROOT / "docs/TIMESERIES_SCHEMA.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 03 - TimescaleDB Operational Time-Series Foundation" in prompt_log
    assert "timeseries.py" in project_map
