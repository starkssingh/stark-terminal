from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ACTIVE_DECISION_DOCS = [
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
]
ACTIVE_DECISION_TESTS = [
    "tests/test_active_decision_architecture_target_docs.py",
    "tests/test_decision_candidate_pipeline_target_docs.py",
    "tests/test_verifier_layer_target_architecture_docs.py",
    "tests/test_no_trade_commit_language_in_active_decision_target.py",
    "tests/phases/test_active_decision_architecture_phase.py",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_research_artifact_index_next_phase_points_to_prompt_82() -> None:
    combined = "\n".join(
        [
            read("docs/RESEARCH_ARTIFACT_INDEX_NEXT_PHASE_PLAN.md"),
            read("docs/NEXT_PHASE_PLAN.md"),
            read("docs/NORTH_STAR.md"),
            read("docs/PROMPT_LOG.md"),
        ]
    )

    required = [
        "Prompt 82 - Research Artifact Index System Boundary Hardening",
        "Current Prompt: 81",
        "Prompt 81 - Research Artifact Index Milestone Audit",
        "implementation remains forbidden",
        "no indexing",
        "no search",
        "no ranking",
        "no retrieval",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no persistent storage",
        "no file upload",
        "download",
        "preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no broker controls",
        "execution",
    ]

    for phrase in required:
        assert phrase in combined


def test_active_decision_architecture_docs_and_tests_remain_preserved() -> None:
    for path in [*ACTIVE_DECISION_DOCS, *ACTIVE_DECISION_TESTS]:
        assert (ROOT / path).exists(), path

    combined_docs = "\n".join(read(path) for path in ACTIVE_DECISION_DOCS)

    assert "Decision candidate is not a trade" in combined_docs
    assert "No direct signal-to-trade path" in combined_docs
    assert "Execution APIs remain forbidden" in combined_docs
