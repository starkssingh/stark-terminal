from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_correlation_beta_docs_exist_and_state_boundaries() -> None:
    docs = {
        "docs/CORRELATION_ANALYTICS_V0.md": [
            "Correlation Analytics",
            "Pearson correlation",
            "sample covariance",
            "sample variance",
            "equal length",
            "minimum observations",
            "zero variance",
            "descriptive-only",
            "no signals",
            "no recommendations",
            "no execution APIs",
            "Mac mini M2",
            "Windows-native",
        ],
        "docs/BETA_ANALYTICS_V0.md": [
            "Beta Analytics",
            "beta = covariance",
            "sample covariance",
            "sample variance",
            "benchmark variance",
            "equal length",
            "minimum observations",
            "descriptive-only",
            "no signals",
            "no recommendations",
            "no execution APIs",
        ],
        "docs/CORRELATION_BETA_VALIDATION_POLICY.md": [
            "Paired Vector Validation",
            "finite values",
            "source-reference",
            "no real market data",
            "failure behavior",
        ],
        "docs/CORRELATION_BETA_SAFETY_BOUNDARY.md": [
            "Correlation and Beta Safety Boundary",
            "Correlation is not a signal",
            "Beta is not a signal",
            "no DecisionObject generation",
            "no execution APIs",
        ],
    }

    for path, phrases in docs.items():
        text = _read(path)
        for phrase in phrases:
            assert phrase in text


def test_prompt_32_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    analytics_next = _read("docs/ANALYTICS_NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Time-Series Diagnostics Foundation" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 34 - Regime Feature Preparation Contracts" in analytics_next
    assert "## Prompt 31 - Correlation and Beta Analytics v0" in prompt_log
    assert "Prompt 31 Correlation and Beta Analytics v0 Artifacts" in project_map


def test_verify_and_audit_scripts_track_prompt_32_artifacts() -> None:
    verify = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    for phrase in [
        "docs/CORRELATION_ANALYTICS_V0.md",
        "docs/BETA_ANALYTICS_V0.md",
        "docs/CORRELATION_BETA_VALIDATION_POLICY.md",
        "docs/CORRELATION_BETA_SAFETY_BOUNDARY.md",
        "packages/analytics/stark_terminal_analytics/correlation/contracts.py",
        "packages/analytics/stark_terminal_analytics/beta/contracts.py",
        "apps/api/stark_terminal_api/routes/relationship_analytics.py",
    ]:
        assert phrase in verify
        assert phrase in audit
