from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_numerical_analytics_docs_exist() -> None:
    docs = [
        "docs/NUMERICAL_ANALYTICS_CORE_CONTRACTS.md",
        "docs/NUMERICAL_ANALYTICS_VALIDATION_POLICY.md",
        "docs/NUMERICAL_ANALYTICS_DEPENDENCY_GATE.md",
        "docs/NUMERICAL_ANALYTICS_SAFETY_BOUNDARY.md",
    ]

    for path in docs:
        assert (ROOT / path).exists()


def test_numerical_analytics_docs_state_required_boundaries() -> None:
    text = "\n".join(
        _read(path)
        for path in [
            "docs/NUMERICAL_ANALYTICS_CORE_CONTRACTS.md",
            "docs/NUMERICAL_ANALYTICS_VALIDATION_POLICY.md",
            "docs/NUMERICAL_ANALYTICS_DEPENDENCY_GATE.md",
            "docs/NUMERICAL_ANALYTICS_SAFETY_BOUNDARY.md",
        ]
    )

    for phrase in [
        "Numerical Analytics",
        "source reference",
        "finite",
        "dependency gate",
        "descriptive-only",
        "No returns",
        "No volatility",
        "No drawdown",
        "No recommendations",
        "No DecisionObject",
        "No execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_28_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    analytics_roadmap = _read("docs/ANALYTICS_ROADMAP.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Numerical Core Contracts" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 27 - Numerical Analytics Core Contracts" in analytics_roadmap
    assert "## Prompt 27 - Numerical Analytics Core Contracts" in prompt_log
    assert "Prompt 27 Numerical Analytics Core Contracts Artifacts" in project_map


def test_verify_foundation_mentions_prompt_28_artifacts() -> None:
    verifier = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    assert "docs/NUMERICAL_ANALYTICS_CORE_CONTRACTS.md" in verifier
    assert "packages/analytics/stark_terminal_analytics/numerical/contracts.py" in verifier
    assert "apps/api/stark_terminal_api/routes/numerical_analytics.py" in verifier
    assert "Numerical Analytics" in verifier
    assert "Prompt 28" in audit
    assert "numerical analytics" in audit.lower()
