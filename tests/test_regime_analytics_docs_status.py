from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_regime_analytics_docs_exist_and_state_boundaries() -> None:
    docs = {
        "docs/REGIME_ANALYTICS_PLANNING.md": [
            "Regime Analytics",
            "planning-only",
            "no regime classification",
            "human review",
            "no signals",
            "no recommendations",
            "no DecisionObject",
            "no execution APIs",
            "Mac mini M2",
            "Windows-native",
        ],
        "docs/REGIME_LABEL_CONTRACTS.md": [
            "Regime Label Contracts",
            "label placeholders",
            "No labels are assigned",
            "no trading interpretation",
        ],
        "docs/REGIME_EVIDENCE_REQUIREMENTS.md": [
            "evidence requirements",
            "source reference",
            "validated input",
            "Missing required evidence blocks readiness",
        ],
        "docs/REGIME_ANALYTICS_SAFETY_POLICY.md": [
            "no classification",
            "no trade signals",
            "no recommendations",
            "no DecisionObject generation",
            "no execution APIs",
            "human review required",
        ],
        "docs/REGIME_DEPENDENCY_STAGING.md": [
            "dependency staging",
            "planning_only",
            "statsmodels",
            "hmmlearn",
            "ruptures",
            "no classifier implementation",
        ],
        "docs/REGIME_ANALYTICS_ROADMAP.md": [
            "Prompt 34 - Regime Feature Preparation Contracts",
            "Prompt 35 - Analytics/Regime Milestone Audit",
            "what remains forbidden",
        ],
    }

    for path, phrases in docs.items():
        text = _read(path)
        for phrase in phrases:
            assert phrase in text


def test_prompt_33_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    analytics_next = _read("docs/ANALYTICS_NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Regime Analytics Planning Phase - Planning and Guardrails" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 34 - Regime Feature Preparation Contracts" in analytics_next
    assert "## Prompt 33 - Regime Analytics Planning and Guardrails" in prompt_log
    assert "Regime Analytics Planning and Guardrails" in project_map


def test_verify_and_audit_scripts_track_prompt_33_artifacts() -> None:
    verify = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    for phrase in [
        "docs/REGIME_ANALYTICS_PLANNING.md",
        "docs/REGIME_LABEL_CONTRACTS.md",
        "docs/REGIME_EVIDENCE_REQUIREMENTS.md",
        "docs/REGIME_ANALYTICS_SAFETY_POLICY.md",
        "docs/REGIME_DEPENDENCY_STAGING.md",
        "docs/REGIME_ANALYTICS_ROADMAP.md",
        "packages/analytics/stark_terminal_analytics/regime/contracts.py",
        "packages/analytics/stark_terminal_analytics/regime/evidence.py",
        "packages/analytics/stark_terminal_analytics/regime/safety.py",
        "packages/analytics/stark_terminal_analytics/regime/readiness.py",
        "apps/api/stark_terminal_api/routes/regime_analytics.py",
    ]:
        assert phrase in verify
        assert phrase in audit
