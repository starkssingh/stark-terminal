from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    ResearchArtifactLifecycleStatus,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class ResearchArtifactMetadataPlaceholder(BaseModel):
    artifact_id: str
    artifact_kind: ResearchArtifactKind
    title: str
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    source_reference: str | None = None
    provenance_reference: str | None = None
    lifecycle_status: ResearchArtifactLifecycleStatus
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("artifact_id", "title", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact metadata placeholder text fields")

    @field_validator("description", "source_reference", "provenance_reference")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("tags")
    @classmethod
    def tags_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def placeholder_must_not_claim_active_artifact(self) -> ResearchArtifactMetadataPlaceholder:
        if self.artifact_kind == ResearchArtifactKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact kind is not allowed for metadata placeholders")
        if self.lifecycle_status == ResearchArtifactLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed for metadata placeholders")
        dangerous_status_terms = {
            "approved",
            "validated_strategy",
            "recommendation",
            "readiness_to_trade",
            "execution",
        }
        normalized_status = self.lifecycle_status.value.lower()
        if any(term in normalized_status for term in dangerous_status_terms):
            raise ValueError("research artifact lifecycle status cannot imply trading readiness")
        return self


def default_research_artifact_metadata_placeholders() -> list[ResearchArtifactMetadataPlaceholder]:
    return [
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-paper-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.PAPER_REFERENCE,
            title="Paper Reference Placeholder",
            description="Descriptive paper reference only; no ingestion or parsed paper content.",
            tags=["planning-only", "paper-reference", "not-parsed"],
            source_reference="paper-source-placeholder",
            provenance_reference="paper-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-dataset-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.DATASET_REFERENCE,
            title="Dataset Reference Placeholder",
            description="Dataset reference only; no real/live market data trust claim.",
            tags=["planning-only", "dataset-reference", "not-validated"],
            source_reference="dataset-source-placeholder",
            provenance_reference="dataset-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-hypothesis-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.HYPOTHESIS_REFERENCE,
            title="Hypothesis Reference Placeholder",
            description="Hypothesis reference only; no generated strategy or signal.",
            tags=["planning-only", "hypothesis-reference", "not-strategy"],
            source_reference="hypothesis-source-placeholder",
            provenance_reference="hypothesis-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.DRAFT,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-experiment-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.EXPERIMENT_REFERENCE,
            title="Experiment Reference Placeholder",
            description="Experiment plan reference only; no executable backtest.",
            tags=["planning-only", "experiment-reference", "not-executable"],
            source_reference="experiment-source-placeholder",
            provenance_reference="experiment-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.REVIEW_REQUIRED,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-notebook-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.NOTEBOOK_REFERENCE,
            title="Notebook Reference Placeholder",
            description="Notebook reference only; no file read or code execution.",
            tags=["planning-only", "notebook-reference", "not-executed"],
            source_reference="notebook-source-placeholder",
            provenance_reference="notebook-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-code-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.CODE_REFERENCE,
            title="Code Reference Placeholder",
            description="Code reference only; no generated executable strategy code.",
            tags=["planning-only", "code-reference", "not-executable"],
            source_reference="code-source-placeholder",
            provenance_reference="code-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-report-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.REPORT_REFERENCE,
            title="Report Reference Placeholder",
            description="Report reference only; no performance claim or recommendation.",
            tags=["planning-only", "report-reference", "not-recommendation"],
            source_reference="report-source-placeholder",
            provenance_reference="report-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-backtest-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.BACKTEST_REFERENCE_PLACEHOLDER,
            title="Backtest Reference Placeholder",
            description="Backtest reference placeholder only; no metrics or validation result.",
            tags=["planning-only", "backtest-placeholder", "no-results"],
            source_reference="backtest-source-placeholder",
            provenance_reference="backtest-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.BLOCKED,
        ),
        ResearchArtifactMetadataPlaceholder(
            artifact_id="research-artifact-strategy-reference-placeholder-v1",
            artifact_kind=ResearchArtifactKind.STRATEGY_REFERENCE_PLACEHOLDER,
            title="Strategy Reference Placeholder",
            description="Strategy reference placeholder only; no generated strategy logic.",
            tags=["planning-only", "strategy-placeholder", "no-logic"],
            source_reference="strategy-source-placeholder",
            provenance_reference="strategy-provenance-placeholder",
            lifecycle_status=ResearchArtifactLifecycleStatus.BLOCKED,
        ),
    ]

