from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_decision_desk_docs_exist() -> None:
    for path in [
        "docs/RETAIL_DECISION_DESK_PLANNING.md",
        "docs/DECISION_DESK_ACTION_PLACEHOLDERS.md",
        "docs/DECISION_DESK_EVIDENCE_REQUIREMENTS.md",
        "docs/DECISION_DESK_HUMAN_REVIEW_GUARDRAILS.md",
        "docs/DECISION_DESK_SAFETY_POLICY.md",
        "docs/DECISION_DESK_DISPLAY_BOUNDARY.md",
    ]:
        assert (ROOT / path).exists()


def test_decision_desk_docs_cover_required_safety_boundary() -> None:
    combined = "\n".join(
        _read(path)
        for path in [
            "docs/RETAIL_DECISION_DESK_PLANNING.md",
            "docs/DECISION_DESK_ACTION_PLACEHOLDERS.md",
            "docs/DECISION_DESK_EVIDENCE_REQUIREMENTS.md",
            "docs/DECISION_DESK_HUMAN_REVIEW_GUARDRAILS.md",
            "docs/DECISION_DESK_SAFETY_POLICY.md",
            "docs/DECISION_DESK_DISPLAY_BOUNDARY.md",
        ]
    )

    for phrase in [
        "Retail Decision Desk",
        "planning-only",
        "action placeholders",
        "evidence requirements",
        "human review",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in combined


def test_decision_desk_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    project_map = _read("PROJECT_MAP.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 36" in north_star
    assert "Retail Decision Desk Planning Phase - Planning and Guardrails" in north_star
    assert "Prompt 36 Retail Decision Desk Planning and Guardrails" in project_map
    assert "## Prompt 36 - Retail Decision Desk Planning and Guardrails" in prompt_log
    assert "Prompt 37 - DecisionObject Evidence Bundle Contracts" in next_phase
