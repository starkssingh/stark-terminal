from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_worker_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/WORKER_SYSTEM_FOUNDATION.md").exists()
    assert (ROOT / "docs/WORKER_ROLE_POLICY.md").exists()
    assert (ROOT / "docs/JOB_ENVELOPE_SPEC.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 07 - Worker System Foundation" in prompt_log
    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "workers/jobs.py" in project_map
    assert "Worker System foundation" in project_map
