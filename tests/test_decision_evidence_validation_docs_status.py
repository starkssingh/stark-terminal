from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_evidence_validation_docs_exist_and_state_boundaries() -> None:
    required_docs = [
        "docs/DECISION_EVIDENCE_VALIDATION_V0.md",
        "docs/DECISION_EVIDENCE_VALIDATION_RESULT_SCHEMA.md",
        "docs/DECISION_EVIDENCE_VALIDATION_FAILURE_REASONS.md",
        "docs/DECISION_EVIDENCE_VALIDATION_SAFETY_BOUNDARY.md",
        "docs/DECISION_EVIDENCE_VALIDATION_API_SKELETON.md",
        "docs/DECISION_EVIDENCE_VALIDATION_NO_RECOMMENDATION_POLICY.md",
    ]
    for path in required_docs:
        assert (ROOT / path).exists()

    docs_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in required_docs)
    for phrase in [
        "Decision Evidence Validation",
        "validation-only",
        "validation result",
        "failure reasons",
        "source reference",
        "provenance",
        "human review attachment",
        "no readiness-to-trade",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no approval",
        "no override",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_decision_evidence_validation_status_docs_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 44 - Decision Desk Evidence Bundle Validation v0" in prompt_log
    assert "Current Prompt: 44" in north_star
    assert "Decision Desk Evidence Bundle Validation v0" in project_map
    assert "packages/core/stark_terminal_core/decision_evidence_validation/" in project_map

