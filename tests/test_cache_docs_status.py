from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cache_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/REDIS_CACHE_FOUNDATION.md").exists()
    assert (ROOT / "docs/CACHE_KEY_POLICY.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 05 - Redis Cache Foundation" in prompt_log
    assert "Current Prompt: 16" in north_star
    assert "Completed Prompts: 16 before this prompt, 17 after completion" in north_star
    assert "cache/keys.py" in project_map
    assert "Redis cache foundation" in project_map
