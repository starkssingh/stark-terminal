from __future__ import annotations

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexForbiddenInteractionKind,
    ResearchArtifactIndexKeyKind,
    ResearchArtifactIndexKind,
    ResearchArtifactIndexSafetyLabel,
    ResearchArtifactIndexStage,
    ResearchArtifactIndexTagKind,
)


def test_research_artifact_index_expected_types_exist() -> None:
    assert ResearchArtifactIndexStage.PLANNING_AND_GUARDRAILS.value == "planning_and_guardrails"
    assert ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER.value == "METADATA_INDEX_PLACEHOLDER"
    assert ResearchArtifactIndexKeyKind.ARTIFACT_ID.value == "ARTIFACT_ID"
    assert ResearchArtifactIndexTagKind.PAPER_REFERENCE.value == "PAPER_REFERENCE"
    assert ResearchArtifactIndexSafetyLabel.NOT_A_VECTOR_STORE.value == "NOT_A_VECTOR_STORE"


def test_research_artifact_index_forbidden_kinds_cover_dangerous_behavior() -> None:
    expected = {
        "INDEXING_ENGINE",
        "SEARCH_ENGINE",
        "RANKING_ENGINE",
        "RETRIEVAL_ENGINE",
        "EMBEDDING_PIPELINE",
        "VECTOR_STORE",
        "SEMANTIC_SEARCH",
        "KEYWORD_SEARCH",
        "ACTIVE_INGESTION",
        "PERSISTENT_STORAGE",
        "FILE_UPLOAD",
        "FILE_DOWNLOAD",
        "FILE_PREVIEW",
        "PAPER_PARSING",
        "PDF_PARSING",
        "ARXIV_INGESTION",
        "LLM_PAPER_ANALYSIS",
        "STRATEGY_GENERATION",
        "STRATEGY_CODE_GENERATION",
        "BACKTESTING",
        "OPTIMIZATION",
        "RECOMMENDATION_GENERATION",
        "CONFIDENCE_SCORING",
        "DECISION_OBJECT_GENERATION",
        "READINESS_TO_TRADE",
        "BROKER_CONTROL",
        "EXECUTION",
    }
    actual = {kind.value for kind in ResearchArtifactIndexForbiddenInteractionKind}

    assert expected <= actual
    assert ResearchArtifactIndexForbiddenInteractionKind.UNKNOWN.value == "UNKNOWN"

