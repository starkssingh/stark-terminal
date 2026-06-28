from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexForbiddenInteractionKind,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


REQUIRED_RESEARCH_ARTIFACT_INDEX_FORBIDDEN_INTERACTIONS = {
    ResearchArtifactIndexForbiddenInteractionKind.INDEXING_ENGINE,
    ResearchArtifactIndexForbiddenInteractionKind.SEARCH_ENGINE,
    ResearchArtifactIndexForbiddenInteractionKind.RANKING_ENGINE,
    ResearchArtifactIndexForbiddenInteractionKind.RETRIEVAL_ENGINE,
    ResearchArtifactIndexForbiddenInteractionKind.EMBEDDING_PIPELINE,
    ResearchArtifactIndexForbiddenInteractionKind.VECTOR_STORE,
    ResearchArtifactIndexForbiddenInteractionKind.SEMANTIC_SEARCH,
    ResearchArtifactIndexForbiddenInteractionKind.KEYWORD_SEARCH,
    ResearchArtifactIndexForbiddenInteractionKind.ACTIVE_INGESTION,
    ResearchArtifactIndexForbiddenInteractionKind.PERSISTENT_STORAGE,
    ResearchArtifactIndexForbiddenInteractionKind.FILE_UPLOAD,
    ResearchArtifactIndexForbiddenInteractionKind.FILE_DOWNLOAD,
    ResearchArtifactIndexForbiddenInteractionKind.FILE_PREVIEW,
    ResearchArtifactIndexForbiddenInteractionKind.PAPER_PARSING,
    ResearchArtifactIndexForbiddenInteractionKind.PDF_PARSING,
    ResearchArtifactIndexForbiddenInteractionKind.ARXIV_INGESTION,
    ResearchArtifactIndexForbiddenInteractionKind.LLM_PAPER_ANALYSIS,
    ResearchArtifactIndexForbiddenInteractionKind.METHOD_EXTRACTION,
    ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_EXTRACTION,
    ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_GENERATION,
    ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_CODE_GENERATION,
    ResearchArtifactIndexForbiddenInteractionKind.BACKTESTING,
    ResearchArtifactIndexForbiddenInteractionKind.OPTIMIZATION,
    ResearchArtifactIndexForbiddenInteractionKind.RECOMMENDATION_GENERATION,
    ResearchArtifactIndexForbiddenInteractionKind.ACTION_GENERATION,
    ResearchArtifactIndexForbiddenInteractionKind.CONFIDENCE_SCORING,
    ResearchArtifactIndexForbiddenInteractionKind.DECISION_OBJECT_GENERATION,
    ResearchArtifactIndexForbiddenInteractionKind.READINESS_TO_TRADE,
    ResearchArtifactIndexForbiddenInteractionKind.BROKER_CONTROL,
    ResearchArtifactIndexForbiddenInteractionKind.EXECUTION,
}


class ResearchArtifactIndexForbiddenInteraction(BaseModel):
    interaction_id: str
    kind: ResearchArtifactIndexForbiddenInteractionKind
    name: str
    description: str
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("interaction_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index forbidden interaction text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def interaction_must_remain_forbidden(self) -> ResearchArtifactIndexForbiddenInteraction:
        if self.kind == ResearchArtifactIndexForbiddenInteractionKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact index forbidden interaction kind is not allowed")
        if not self.forbidden_now:
            raise ValueError("research artifact index forbidden interaction cannot be unlocked in Prompt 77")
        if not self.requires_future_prompt:
            raise ValueError("research artifact index forbidden interaction requires a future prompt")
        if not self.requires_audit_before_unlock:
            raise ValueError("research artifact index forbidden interaction requires audit before unlock")
        return self


def default_research_artifact_index_forbidden_interactions() -> list[ResearchArtifactIndexForbiddenInteraction]:
    return [
        ResearchArtifactIndexForbiddenInteraction(
            interaction_id=f"research-artifact-index-forbidden-{kind.value.lower().replace('_', '-')}-v1",
            kind=kind,
            name=kind.value.replace("_", " ").title(),
            description=f"{kind.value} is forbidden while the Research Artifact Index is planning-only.",
            notes=["Requires a future prompt and safety audit before any unlock."],
        )
        for kind in sorted(
            REQUIRED_RESEARCH_ARTIFACT_INDEX_FORBIDDEN_INTERACTIONS,
            key=lambda item: item.value,
        )
    ]
