from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactReferenceKind,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactReferencePlaceholder(BaseModel):
    reference_id: str
    artifact_id: str
    reference_kind: ResearchArtifactReferenceKind
    reference_uri_placeholder: str | None = None
    source_label: str | None = None
    checksum_placeholder: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("reference_id", "artifact_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact reference placeholder text fields")

    @field_validator("reference_uri_placeholder", "source_label", "checksum_placeholder")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def reference_must_remain_placeholder(self) -> ResearchArtifactReferencePlaceholder:
        if self.reference_kind == ResearchArtifactReferenceKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact reference kind is not allowed")
        for field_name, value in {
            "reference_uri_placeholder": self.reference_uri_placeholder,
            "checksum_placeholder": self.checksum_placeholder,
        }.items():
            if value is not None and "placeholder" not in value.lower():
                raise ValueError(f"{field_name} must remain a placeholder value")
        return self


def default_research_artifact_reference_placeholders() -> list[ResearchArtifactReferencePlaceholder]:
    return [
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-paper-reference-uri-placeholder-v1",
            artifact_id="research-artifact-paper-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.PAPER_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="paper-uri-placeholder",
            source_label="Paper reference placeholder",
            checksum_placeholder="paper-checksum-placeholder",
        ),
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-dataset-reference-uri-placeholder-v1",
            artifact_id="research-artifact-dataset-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.DATASET_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="dataset-uri-placeholder",
            source_label="Dataset reference placeholder",
            checksum_placeholder="dataset-checksum-placeholder",
        ),
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-hypothesis-reference-uri-placeholder-v1",
            artifact_id="research-artifact-hypothesis-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.HYPOTHESIS_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="hypothesis-uri-placeholder",
            source_label="Hypothesis reference placeholder",
            checksum_placeholder="hypothesis-checksum-placeholder",
        ),
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-experiment-reference-uri-placeholder-v1",
            artifact_id="research-artifact-experiment-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.EXPERIMENT_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="experiment-uri-placeholder",
            source_label="Experiment reference placeholder",
            checksum_placeholder="experiment-checksum-placeholder",
        ),
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-notebook-reference-uri-placeholder-v1",
            artifact_id="research-artifact-notebook-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.NOTEBOOK_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="notebook-uri-placeholder",
            source_label="Notebook reference placeholder",
            checksum_placeholder="notebook-checksum-placeholder",
        ),
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-code-reference-uri-placeholder-v1",
            artifact_id="research-artifact-code-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.CODE_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="code-uri-placeholder",
            source_label="Code reference placeholder",
            checksum_placeholder="code-checksum-placeholder",
        ),
        ResearchArtifactReferencePlaceholder(
            reference_id="research-artifact-report-reference-uri-placeholder-v1",
            artifact_id="research-artifact-report-reference-placeholder-v1",
            reference_kind=ResearchArtifactReferenceKind.REPORT_REFERENCE_PLACEHOLDER,
            reference_uri_placeholder="report-uri-placeholder",
            source_label="Report reference placeholder",
            checksum_placeholder="report-checksum-placeholder",
        ),
    ]

