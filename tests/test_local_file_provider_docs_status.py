from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_24_docs_exist_and_state_safety_boundaries() -> None:
    docs = [
        "docs/LOCAL_FILE_PROVIDER_ADAPTER.md",
        "docs/LOCAL_FILE_PROVIDER_POLICY.md",
        "docs/LOCAL_FILE_PATH_SAFETY.md",
    ]
    for path in docs:
        assert (ROOT / path).exists()

    text = "\n".join(_read(path) for path in docs)
    for phrase in [
        "Local File Provider",
        "local-file-only",
        "path safety",
        "no external calls",
        "no real market data",
        "no scraping",
        "no credentials",
        "no arbitrary file read API",
        "no execution APIs",
        "no trading signals",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_24_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 25" in north_star
    assert "Completed Prompts: 25 before this prompt, 26 after completion" in north_star
    assert "Provider Adapter Milestone Audit completed" in north_star
    assert "## Prompt 24 - Local File Provider Adapter v0" in prompt_log
    assert "Prompt 24 Local File Provider Adapter Artifacts" in project_map
    assert "Prompt 26 - Quant/Time-Series Analytics Foundation Plan" in next_phase


def test_verify_and_audit_scripts_track_prompt_24_artifacts() -> None:
    verify = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")
    for phrase in [
        "docs/LOCAL_FILE_PROVIDER_ADAPTER.md",
        "docs/LOCAL_FILE_PROVIDER_POLICY.md",
        "docs/LOCAL_FILE_PATH_SAFETY.md",
        "packages/data_platform/stark_terminal_data_platform/providers/local_file.py",
        "apps/api/stark_terminal_api/routes/local_file_provider.py",
        "Prompt 24",
    ]:
        assert phrase in verify
        assert phrase in audit
