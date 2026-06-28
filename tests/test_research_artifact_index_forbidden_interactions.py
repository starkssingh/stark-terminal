from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.interactions import (
    ResearchArtifactIndexForbiddenInteraction,
    default_research_artifact_index_forbidden_interactions,
)
from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexForbiddenInteractionKind


def test_default_research_artifact_index_forbidden_interactions_are_complete() -> None:
    interactions = default_research_artifact_index_forbidden_interactions()
    kinds = {item.kind.value for item in interactions}

    for required in [
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
        "ARXIV_INGESTION",
        "LLM_PAPER_ANALYSIS",
        "STRATEGY_GENERATION",
        "BACKTESTING",
        "RECOMMENDATION_GENERATION",
        "EXECUTION",
    ]:
        assert required in kinds
    assert all(item.forbidden_now for item in interactions)
    assert all(item.requires_future_prompt for item in interactions)
    assert all(item.requires_audit_before_unlock for item in interactions)


@pytest.mark.parametrize("field", ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"])
def test_research_artifact_index_forbidden_interactions_enforce_lock_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexForbiddenInteraction(
            interaction_id="x",
            kind=ResearchArtifactIndexForbiddenInteractionKind.INDEXING_ENGINE,
            name="x",
            description="x",
            **{field: False},
        )


def test_research_artifact_index_forbidden_interactions_reject_unknown() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexForbiddenInteraction(
            interaction_id="x",
            kind=ResearchArtifactIndexForbiddenInteractionKind.UNKNOWN,
            name="x",
            description="x",
        )

