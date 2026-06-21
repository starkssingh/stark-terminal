from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_stream_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/REDIS_STREAMS_FOUNDATION.md").exists()
    assert (ROOT / "docs/EVENT_PIPELINE_POLICY.md").exists()
    assert (ROOT / "docs/EVENT_ENVELOPE_SPEC.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 06 - Redis Streams Event Pipeline Foundation" in prompt_log
    assert "Current Prompt: 16" in north_star
    assert "Completed Prompts: 16 before this prompt, 17 after completion" in north_star
    assert "streams/names.py" in project_map
    assert "Redis Streams foundation" in project_map
