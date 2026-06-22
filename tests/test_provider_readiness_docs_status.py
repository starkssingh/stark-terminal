from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_23_docs_exist_and_state_safety_boundaries() -> None:
    docs = [
        "docs/REAL_PROVIDER_READINESS_CHECKLIST.md",
        "docs/PROVIDER_CANDIDATE_SELECTION_POLICY.md",
        "docs/PROVIDER_RISK_SCORING_POLICY.md",
        "docs/PROVIDER_CAPABILITY_GAP_ANALYSIS.md",
    ]
    for path in docs:
        assert (ROOT / path).exists()

    text = "\n".join(_read(path) for path in docs)
    for phrase in [
        "Real Provider Readiness",
        "Candidate Selection",
        "risk scoring",
        "capability gap",
        "no external calls",
        "no SDKs",
        "no scraping",
        "no credentials",
        "no real market ingestion",
        "no production approval",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_23_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 25" in north_star
    assert "Completed Prompts: 25 before this prompt, 26 after completion" in north_star
    assert "Provider Adapter Milestone Audit completed" in north_star
    assert "## Prompt 23 - Real Provider Readiness Checklist and Candidate Selection" in prompt_log
    assert "Prompt 23 Real Provider Readiness Checklist And Candidate Selection Artifacts" in project_map
    assert "Prompt 26 - Quant/Time-Series Analytics Foundation Plan" in next_phase


def test_verify_and_audit_scripts_track_prompt_23_artifacts() -> None:
    verify = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")
    for phrase in [
        "docs/REAL_PROVIDER_READINESS_CHECKLIST.md",
        "docs/PROVIDER_CANDIDATE_SELECTION_POLICY.md",
        "docs/PROVIDER_RISK_SCORING_POLICY.md",
        "docs/PROVIDER_CAPABILITY_GAP_ANALYSIS.md",
        "packages/data_platform/stark_terminal_data_platform/providers/candidates.py",
        "packages/data_platform/stark_terminal_data_platform/providers/selection.py",
        "apps/api/stark_terminal_api/routes/provider_readiness.py",
        "Prompt 23",
    ]:
        assert phrase in verify
        assert phrase in audit
