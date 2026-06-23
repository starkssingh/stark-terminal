from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_analytics_milestone_audit_docs_exist() -> None:
    docs = [
        "docs/ANALYTICS_MILESTONE_AUDIT.md",
        "docs/ANALYTICS_BOUNDARY_AUDIT.md",
        "docs/ANALYTICS_NO_SIGNAL_AUDIT.md",
        "docs/ANALYTICS_DEPENDENCY_AUDIT.md",
        "docs/ANALYTICS_NEXT_PHASE_PLAN.md",
    ]

    for path in docs:
        assert (ROOT / path).exists()


def test_analytics_milestone_docs_state_required_boundaries() -> None:
    text = "\n".join(
        _read(path)
        for path in [
            "docs/ANALYTICS_MILESTONE_AUDIT.md",
            "docs/ANALYTICS_BOUNDARY_AUDIT.md",
            "docs/ANALYTICS_NO_SIGNAL_AUDIT.md",
            "docs/ANALYTICS_DEPENDENCY_AUDIT.md",
            "docs/ANALYTICS_NEXT_PHASE_PLAN.md",
        ]
    )

    for phrase in [
        "Prompts 26-29",
        "analytics foundation",
        "numerical analytics",
        "returns analytics",
        "rolling window analytics",
        "volatility analytics",
        "drawdown analytics",
        "no real ingestion",
        "no external calls",
        "no heavy analytics dependencies",
        "no signals",
        "no recommendations",
        "no DecisionObject",
        "no execution APIs",
        "no backtests",
        "no regimes",
        "no indicators",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_analytics_next_phase_plan_recommends_prompt_32() -> None:
    text = _read("docs/ANALYTICS_NEXT_PHASE_PLAN.md")

    assert "Prompt 34 - Regime Feature Preparation Contracts" in text
    assert "Prompt 34 - Regime Feature Preparation Contracts" in text
    assert "Prompt 35 - Analytics/Regime Milestone Audit" in text
    assert "no signals" in text
    assert "no recommendations" in text
