from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_evidence_docs_exist_and_state_boundaries() -> None:
    required_docs = [
        "docs/DECISIONOBJECT_EVIDENCE_BUNDLE_CONTRACTS.md",
        "docs/DECISION_EVIDENCE_ITEM_SCHEMA.md",
        "docs/DECISION_EVIDENCE_PROVENANCE_POLICY.md",
        "docs/DECISION_EVIDENCE_VALIDATION_CHECKLIST.md",
        "docs/DECISION_EVIDENCE_HUMAN_REVIEW_ATTACHMENTS.md",
        "docs/DECISION_EVIDENCE_SAFETY_POLICY.md",
    ]
    for path in required_docs:
        assert (ROOT / path).exists()

    docs_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in required_docs)
    for phrase in [
        "DecisionObject Evidence Bundle",
        "contracts-only",
        "evidence item",
        "provenance",
        "validation checklist",
        "human review attachment",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_decision_evidence_status_docs_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 38 - DecisionObject Evidence Bundle Contracts" in prompt_log
    assert "Current Prompt: 38" in north_star
    assert "DecisionObject Evidence Bundle Contracts" in project_map
    assert "packages/core/stark_terminal_core/decision_evidence/" in project_map
