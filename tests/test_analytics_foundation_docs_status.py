from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_analytics_foundation_docs_exist() -> None:
    docs = [
        "docs/QUANT_ANALYTICS_FOUNDATION_PLAN.md",
        "docs/TIME_SERIES_ANALYTICS_BOUNDARY.md",
        "docs/ANALYTICS_SAFETY_POLICY.md",
        "docs/ANALYTICS_DEPENDENCY_STAGING.md",
        "docs/ANALYTICS_ROADMAP.md",
    ]

    for path in docs:
        assert (ROOT / path).exists()


def test_analytics_foundation_docs_state_required_boundaries() -> None:
    text = "\n".join(
        _read(path)
        for path in [
            "docs/QUANT_ANALYTICS_FOUNDATION_PLAN.md",
            "docs/TIME_SERIES_ANALYTICS_BOUNDARY.md",
            "docs/ANALYTICS_SAFETY_POLICY.md",
            "docs/ANALYTICS_DEPENDENCY_STAGING.md",
            "docs/ANALYTICS_ROADMAP.md",
        ]
    )

    for phrase in [
        "Quant Analytics",
        "Time-Series Analytics",
        "analytics safety",
        "dependency staging",
        "no trading signals",
        "no recommendations",
        "no execution APIs",
        "no analytics calculations",
        "descriptive/research-only",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_26_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    provider_next_phase = _read("docs/PROVIDER_NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Quant/Time-Series Analytics Foundation Phase - Numerical Core Contracts" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 28 - Returns and Rolling Window Analytics v0" in provider_next_phase
    assert "## Prompt 26 - Quant/Time-Series Analytics Foundation Plan" in prompt_log
    assert "Prompt 26 Quant/Time-Series Analytics Foundation Plan Artifacts" in project_map

def test_verify_foundation_mentions_prompt_26_artifacts() -> None:
    verifier = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    assert "docs/QUANT_ANALYTICS_FOUNDATION_PLAN.md" in verifier
    assert "packages/analytics/stark_terminal_analytics/foundation/contracts.py" in verifier
    assert "apps/api/stark_terminal_api/routes/analytics_foundation.py" in verifier
    assert "Quant Analytics" in verifier
    assert "Prompt 26" in audit
    assert "analytics foundation" in audit.lower()

