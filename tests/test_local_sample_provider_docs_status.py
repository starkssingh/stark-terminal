from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_local_sample_provider_docs_exist_and_state_boundaries() -> None:
    adapter_doc = (ROOT / "docs/LOCAL_SAMPLE_PROVIDER_ADAPTER.md").read_text(encoding="utf-8")
    policy_doc = (ROOT / "docs/LOCAL_SAMPLE_PROVIDER_POLICY.md").read_text(encoding="utf-8")
    docs_text = f"{adapter_doc}\n{policy_doc}"

    assert "Local Sample Provider" in docs_text
    assert "synthetic" in docs_text
    assert "local-only" in docs_text
    assert "no external calls" in docs_text
    assert "no real market data" in docs_text
    assert "no scraping" in docs_text
    assert "no credentials" in docs_text
    assert "no execution APIs" in docs_text
    assert "no trading signals" in docs_text
    assert "Mac mini M2" in docs_text
    assert "Windows-native" in docs_text


def test_local_sample_provider_status_docs_are_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 21 - Local Sample Provider Adapter v0" in prompt_log
    assert "Current Prompt: 25" in north_star
    assert "Local Sample Provider and Local File Provider implemented and audited" in north_star
    assert "local_sample.py" in project_map
    assert "local_sample_provider.py" in project_map
