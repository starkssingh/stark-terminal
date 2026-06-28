from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.interactions import (
    ResearchArtifactForbiddenInteraction,
    ResearchArtifactForbiddenInteractionRegistry,
    default_research_artifact_forbidden_interaction_registry,
    default_research_artifact_forbidden_interactions,
)
from stark_terminal_core.research_artifact_registry.types import ResearchArtifactForbiddenInteractionKind


def test_forbidden_interactions_include_required_dangerous_behavior() -> None:
    interactions = default_research_artifact_forbidden_interactions()
    kinds = {interaction.kind for interaction in interactions}

    assert ResearchArtifactForbiddenInteractionKind.ACTIVE_INGESTION in kinds
    assert ResearchArtifactForbiddenInteractionKind.PERSISTENT_STORAGE in kinds
    assert ResearchArtifactForbiddenInteractionKind.FILE_UPLOAD in kinds
    assert ResearchArtifactForbiddenInteractionKind.FILE_DOWNLOAD in kinds
    assert ResearchArtifactForbiddenInteractionKind.PAPER_PARSING in kinds
    assert ResearchArtifactForbiddenInteractionKind.ARXIV_INGESTION in kinds
    assert ResearchArtifactForbiddenInteractionKind.LLM_ANALYSIS in kinds
    assert ResearchArtifactForbiddenInteractionKind.STRATEGY_GENERATION in kinds
    assert ResearchArtifactForbiddenInteractionKind.BACKTESTING in kinds
    assert ResearchArtifactForbiddenInteractionKind.RECOMMENDATION_GENERATION in kinds
    assert ResearchArtifactForbiddenInteractionKind.EXECUTION in kinds


def test_forbidden_interaction_enforces_lock_flags() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenInteraction(
            interaction_id="unsafe-interaction",
            kind=ResearchArtifactForbiddenInteractionKind.ACTIVE_INGESTION,
            name="Unsafe interaction",
            description="Unsafe",
            forbidden_now=False,
        )


def test_forbidden_registry_rejects_dangerous_enabled_flags() -> None:
    registry = default_research_artifact_forbidden_interaction_registry()
    data = registry.model_dump()
    data["active_ingestion_enabled"] = True

    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenInteractionRegistry(**data)


def test_default_forbidden_registry_validates() -> None:
    registry = default_research_artifact_forbidden_interaction_registry()

    assert registry.complete is True
    assert registry.active_ingestion_enabled is False
    assert registry.execution_enabled is False

