from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_artifact_index_milestone_readiness_recommends_prompt_82() -> None:
    readiness = (ROOT / "docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_READINESS.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Prompt 82 - Research Artifact Index System Boundary Hardening" in readiness
    assert "Prompt 82 - Research Artifact Index System Boundary Hardening" in next_phase
    assert "Current Prompt: 81" in north_star
    assert "Prompt 81 - Research Artifact Index Milestone Audit" in prompt_log


def test_active_decision_architecture_docs_and_tests_remain_present() -> None:
    for relative in [
        "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
        "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
        "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
        "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
        "docs/AUDIT_LOG_JOURNAL_TARGET.md",
        "tests/test_active_decision_architecture_target_docs.py",
        "tests/test_decision_candidate_pipeline_target_docs.py",
        "tests/test_verifier_layer_target_architecture_docs.py",
        "tests/test_no_trade_commit_language_in_active_decision_target.py",
    ]:
        assert (ROOT / relative).exists()
