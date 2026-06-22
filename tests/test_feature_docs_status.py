from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_feature_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/FEATURE_REGISTRY_FOUNDATION.md").exists()
    assert (ROOT / "docs/FEATURE_DEFINITION_SPEC.md").exists()
    assert (ROOT / "docs/FEATURE_QUALITY_POLICY.md").exists()
    assert (ROOT / "docs/TRAINING_SERVING_CONSISTENCY_POLICY.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 10 - Feature Store / Stark Feature Registry Foundation" in prompt_log
    assert "Current Prompt: 25" in north_star
    assert "Completed Prompts: 25 before this prompt, 26 after completion" in north_star
    assert "features/definitions.py" in project_map
    assert "Feature Registry foundation" in project_map
