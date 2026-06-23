from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


AUDIT_DOCS = [
    "docs/ANALYTICS_REGIME_MILESTONE_AUDIT.md",
    "docs/REGIME_BOUNDARY_AUDIT.md",
    "docs/REGIME_NO_CLASSIFICATION_AUDIT.md",
    "docs/REGIME_FEATURE_PREPARATION_AUDIT.md",
    "docs/ANALYTICS_REGIME_NO_SIGNAL_AUDIT.md",
    "docs/ANALYTICS_REGIME_DEPENDENCY_AUDIT.md",
    "docs/DECISION_DESK_READINESS_PLAN.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_35_audit_docs_exist() -> None:
    for path in AUDIT_DOCS:
        assert (ROOT / path).exists(), path


def test_prompt_35_audit_docs_cover_required_scope_and_boundaries() -> None:
    text = "\n".join(_read(path) for path in AUDIT_DOCS)

    for phrase in [
        "Prompts 26-34",
        "no real ingestion",
        "no external calls",
        "heavy dependencies",
        "no feature computation",
        "no regime classification",
        "no signals",
        "no recommendations",
        "no DecisionObject",
        "no execution APIs",
        "Decision Desk planning",
        "no stationarity tests",
        "no indicators",
        "backtesting",
    ]:
        assert phrase in text


def test_prompt_35_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Analytics/Regime Milestone Audit completed" in north_star
    assert "## Prompt 35 - Analytics/Regime Milestone Audit" in prompt_log
    assert "Prompt 35 Analytics/Regime Milestone Audit" in project_map
