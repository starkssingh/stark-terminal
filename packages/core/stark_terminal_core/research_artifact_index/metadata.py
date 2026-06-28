from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKind,
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class ResearchArtifactIndexMetadataPlaceholder(BaseModel):
    index_id: str
    index_kind: ResearchArtifactIndexKind
    title: str
    description: str | None = None
    schema_version: str = "v1"
    planning_only: bool = True
    indexing_engine_enabled: bool = False
    search_engine_enabled: bool = False
    ranking_engine_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    persistent_storage_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("index_id", "title", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index metadata placeholder text fields")

    @field_validator("description")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def metadata_must_remain_planning_only(self) -> ResearchArtifactIndexMetadataPlaceholder:
        if self.index_kind == ResearchArtifactIndexKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact index kind is not allowed")
        if not self.planning_only:
            raise ValueError("research artifact index metadata must remain planning-only")
        dangerous_flags = {
            "indexing engine": self.indexing_engine_enabled,
            "search engine": self.search_engine_enabled,
            "ranking engine": self.ranking_engine_enabled,
            "embeddings": self.embeddings_enabled,
            "vector store": self.vector_store_enabled,
            "persistent storage": self.persistent_storage_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact index metadata cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_index_metadata_placeholders() -> list[ResearchArtifactIndexMetadataPlaceholder]:
    return [
        ResearchArtifactIndexMetadataPlaceholder(
            index_id="research-artifact-index-metadata-placeholder-v1",
            index_kind=ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER,
            title="Research Artifact Index Metadata Placeholder",
            description="Planning-only index metadata placeholder; no indexing engine or storage.",
        ),
        ResearchArtifactIndexMetadataPlaceholder(
            index_id="research-artifact-index-key-placeholder-v1",
            index_kind=ResearchArtifactIndexKind.KEY_INDEX_PLACEHOLDER,
            title="Research Artifact Index Key Placeholder",
            description="Planning-only key placeholder; no lookup, search, retrieval, or ranking.",
        ),
        ResearchArtifactIndexMetadataPlaceholder(
            index_id="research-artifact-index-registry-reference-placeholder-v1",
            index_kind=ResearchArtifactIndexKind.REGISTRY_REFERENCE_PLACEHOLDER,
            title="Registry Reference Placeholder",
            description="Descriptive registry reference placeholder; no registry fetch or persistence.",
        ),
    ]
