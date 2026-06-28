from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactForbiddenInteractionKind,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_INTERACTIONS = {
    ResearchArtifactForbiddenInteractionKind.ACTIVE_INGESTION,
    ResearchArtifactForbiddenInteractionKind.PERSISTENT_STORAGE,
    ResearchArtifactForbiddenInteractionKind.FILE_UPLOAD,
    ResearchArtifactForbiddenInteractionKind.FILE_DOWNLOAD,
    ResearchArtifactForbiddenInteractionKind.PAPER_INGESTION,
    ResearchArtifactForbiddenInteractionKind.PAPER_PARSING,
    ResearchArtifactForbiddenInteractionKind.PDF_PARSING,
    ResearchArtifactForbiddenInteractionKind.ARXIV_INGESTION,
    ResearchArtifactForbiddenInteractionKind.LLM_ANALYSIS,
    ResearchArtifactForbiddenInteractionKind.METHOD_EXTRACTION,
    ResearchArtifactForbiddenInteractionKind.STRATEGY_EXTRACTION,
    ResearchArtifactForbiddenInteractionKind.STRATEGY_GENERATION,
    ResearchArtifactForbiddenInteractionKind.STRATEGY_CODE_GENERATION,
    ResearchArtifactForbiddenInteractionKind.SIGNAL_GENERATION,
    ResearchArtifactForbiddenInteractionKind.FACTOR_GENERATION,
    ResearchArtifactForbiddenInteractionKind.ALPHA_GENERATION,
    ResearchArtifactForbiddenInteractionKind.BACKTESTING,
    ResearchArtifactForbiddenInteractionKind.OPTIMIZATION,
    ResearchArtifactForbiddenInteractionKind.RECOMMENDATION_GENERATION,
    ResearchArtifactForbiddenInteractionKind.ACTION_GENERATION,
    ResearchArtifactForbiddenInteractionKind.CONFIDENCE_SCORING,
    ResearchArtifactForbiddenInteractionKind.DECISION_OBJECT_GENERATION,
    ResearchArtifactForbiddenInteractionKind.READINESS_TO_TRADE,
    ResearchArtifactForbiddenInteractionKind.BROKER_CONTROL,
    ResearchArtifactForbiddenInteractionKind.APPROVAL_CONTROL,
    ResearchArtifactForbiddenInteractionKind.OVERRIDE_CONTROL,
    ResearchArtifactForbiddenInteractionKind.EXECUTION,
    ResearchArtifactForbiddenInteractionKind.EXTERNAL_CALL,
    ResearchArtifactForbiddenInteractionKind.DATABASE_WRITE,
    ResearchArtifactForbiddenInteractionKind.OBJECT_STORAGE_WRITE,
}


class ResearchArtifactForbiddenInteraction(BaseModel):
    interaction_id: str
    kind: ResearchArtifactForbiddenInteractionKind
    name: str
    description: str
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("interaction_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact forbidden interaction text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def interaction_must_remain_forbidden(self) -> ResearchArtifactForbiddenInteraction:
        if self.kind == ResearchArtifactForbiddenInteractionKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact forbidden interaction kind is not allowed")
        if not self.forbidden_now:
            raise ValueError("research artifact forbidden interaction cannot be unlocked in Prompt 70")
        if not self.requires_future_prompt:
            raise ValueError("research artifact forbidden interaction requires a future prompt")
        if not self.requires_audit_before_unlock:
            raise ValueError("research artifact forbidden interaction requires audit before unlock")
        return self


class ResearchArtifactForbiddenInteractionRegistry(BaseModel):
    registry_id: str
    interactions: list[ResearchArtifactForbiddenInteraction]
    complete: bool = True
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    paper_parsing_enabled: bool = False
    pdf_parsing_enabled: bool = False
    arxiv_ingestion_enabled: bool = False
    llm_analysis_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("registry_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact forbidden interaction registry text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def registry_must_be_complete_and_fail_closed(self) -> ResearchArtifactForbiddenInteractionRegistry:
        if not self.interactions:
            raise ValueError("research artifact forbidden interaction registry requires interactions")
        if not self.complete:
            raise ValueError("research artifact forbidden interaction registry must be complete")
        dangerous_flags = {
            "active ingestion": self.active_ingestion_enabled,
            "persistent storage": self.persistent_storage_enabled,
            "file uploads": self.file_uploads_enabled,
            "file downloads": self.file_downloads_enabled,
            "paper parsing": self.paper_parsing_enabled,
            "PDF parsing": self.pdf_parsing_enabled,
            "arXiv ingestion": self.arxiv_ingestion_enabled,
            "LLM analysis": self.llm_analysis_enabled,
            "strategy generation": self.strategy_generation_enabled,
            "backtesting": self.backtesting_enabled,
            "recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact registry cannot allow: {', '.join(enabled)}")
        present = {interaction.kind for interaction in self.interactions}
        missing = sorted(kind.value for kind in REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_INTERACTIONS - present)
        if missing:
            raise ValueError(
                "research artifact forbidden registry missing required interactions: "
                + ", ".join(missing)
            )
        return self


def default_research_artifact_forbidden_interactions() -> list[ResearchArtifactForbiddenInteraction]:
    return [
        ResearchArtifactForbiddenInteraction(
            interaction_id=f"research-artifact-forbidden-{kind.value.lower().replace('_', '-')}-v1",
            kind=kind,
            name=kind.value.replace("_", " ").title(),
            description=f"{kind.value} is forbidden while the Research Artifact Registry is planning-only.",
            notes=["Requires a future prompt and safety audit before any unlock."],
        )
        for kind in sorted(
            REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_INTERACTIONS,
            key=lambda item: item.value,
        )
    ]


def default_research_artifact_forbidden_interaction_registry() -> ResearchArtifactForbiddenInteractionRegistry:
    return ResearchArtifactForbiddenInteractionRegistry(
        registry_id="research-artifact-forbidden-interaction-registry-v1",
        interactions=default_research_artifact_forbidden_interactions(),
    )

