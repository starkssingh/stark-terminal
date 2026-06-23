from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_returns_rolling_docs_exist() -> None:
    for path in [
        "docs/RETURNS_ANALYTICS_V0.md",
        "docs/ROLLING_WINDOW_ANALYTICS_V0.md",
        "docs/RETURNS_ROLLING_VALIDATION_POLICY.md",
        "docs/RETURNS_ROLLING_SAFETY_BOUNDARY.md",
    ]:
        assert (ROOT / path).exists()


def test_returns_rolling_docs_state_required_boundaries() -> None:
    text = "\n".join(
        _read(path)
        for path in [
            "docs/RETURNS_ANALYTICS_V0.md",
            "docs/ROLLING_WINDOW_ANALYTICS_V0.md",
            "docs/RETURNS_ROLLING_VALIDATION_POLICY.md",
            "docs/RETURNS_ROLLING_SAFETY_BOUNDARY.md",
        ]
    )

    for phrase in [
        "Returns Analytics",
        "Rolling Window Analytics",
        "simple returns",
        "log returns",
        "rolling mean",
        "rolling min",
        "rolling max",
        "rolling count",
        "descriptive-only",
        "no volatility",
        "no drawdown",
        "no correlation",
        "no signals",
        "no recommendations",
        "no DecisionObject",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_28_status_docs_remain_recorded() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    roadmap = _read("docs/ANALYTICS_ROADMAP.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Returns and Rolling Window Analytics v0" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 28 - Returns and Rolling Window Analytics v0. Status: completed." in roadmap
    assert "## Prompt 28 - Returns and Rolling Window Analytics v0" in prompt_log
    assert "Prompt 28 Returns and Rolling Window Analytics v0 Artifacts" in project_map


def test_verify_foundation_mentions_prompt_28_artifacts() -> None:
    verifier = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    assert "docs/RETURNS_ANALYTICS_V0.md" in verifier
    assert "packages/analytics/stark_terminal_analytics/returns/contracts.py" in verifier
    assert "packages/analytics/stark_terminal_analytics/rolling/contracts.py" in verifier
    assert "apps/api/stark_terminal_api/routes/returns_analytics.py" in verifier
    assert "Returns Analytics" in verifier
    assert "Prompt 28" in audit
    assert "returns and rolling" in audit.lower()
