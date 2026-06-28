from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.lifecycle import (
    ResearchArtifactLifecyclePlaceholder,
    default_research_artifact_lifecycle_placeholders,
)
from stark_terminal_core.research_artifact_registry.metadata import (
    ResearchArtifactMetadataPlaceholder,
    default_research_artifact_metadata_placeholders,
)
from stark_terminal_core.research_artifact_registry.provenance import (
    ResearchArtifactProvenancePlaceholder,
    default_research_artifact_provenance_placeholders,
)
from stark_terminal_core.research_artifact_registry.references import (
    ResearchArtifactReferencePlaceholder,
    default_research_artifact_reference_placeholders,
)
from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactRegistryPlanningContract(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-research-artifact-registry"
    planning_only: bool = True
    unavailable_by_default: bool = True
    artifact_kinds: list[ResearchArtifactKind]
    metadata_placeholders: list[ResearchArtifactMetadataPlaceholder]
    reference_placeholders: list[ResearchArtifactReferencePlaceholder]
    provenance_placeholders: list[ResearchArtifactProvenancePlaceholder]
    lifecycle_placeholders: list[ResearchArtifactLifecyclePlaceholder]
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    paper_parsing_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    next_allowed_phase: str = "api_contract_skeleton"
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("contract_id", "service_name", "next_allowed_phase", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact registry planning contract text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def contract_must_remain_planning_only(self) -> ResearchArtifactRegistryPlanningContract:
        if not self.planning_only:
            raise ValueError("research artifact registry planning contract must remain planning-only")
        if not self.unavailable_by_default:
            raise ValueError("research artifact registry planning contract must remain unavailable by default")
        if not self.artifact_kinds:
            raise ValueError("research artifact registry planning contract requires artifact kinds")
        if ResearchArtifactKind.UNKNOWN in self.artifact_kinds:
            raise ValueError("UNKNOWN artifact kind is not allowed in the planning contract")
        if not self.metadata_placeholders:
            raise ValueError("research artifact registry planning contract requires metadata placeholders")
        if not self.reference_placeholders:
            raise ValueError("research artifact registry planning contract requires reference placeholders")
        if not self.provenance_placeholders:
            raise ValueError("research artifact registry planning contract requires provenance placeholders")
        if not self.lifecycle_placeholders:
            raise ValueError("research artifact registry planning contract requires lifecycle placeholders")
        dangerous_flags = {
            "active ingestion": self.active_ingestion_enabled,
            "persistent storage": self.persistent_storage_enabled,
            "file uploads": self.file_uploads_enabled,
            "file downloads": self.file_downloads_enabled,
            "paper parsing": self.paper_parsing_enabled,
            "strategy generation": self.strategy_generation_enabled,
            "backtesting": self.backtesting_enabled,
            "recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact registry planning contract cannot enable: {', '.join(enabled)}")
        if self.next_allowed_phase != "api_contract_skeleton":
            raise ValueError("next_allowed_phase must be api_contract_skeleton in Prompt 70")
        return self


def default_research_artifact_registry_planning_contract() -> ResearchArtifactRegistryPlanningContract:
    artifact_kinds = [
        ResearchArtifactKind.PAPER_REFERENCE,
        ResearchArtifactKind.DATASET_REFERENCE,
        ResearchArtifactKind.HYPOTHESIS_REFERENCE,
        ResearchArtifactKind.EXPERIMENT_REFERENCE,
        ResearchArtifactKind.NOTEBOOK_REFERENCE,
        ResearchArtifactKind.CODE_REFERENCE,
        ResearchArtifactKind.REPORT_REFERENCE,
        ResearchArtifactKind.BACKTEST_REFERENCE_PLACEHOLDER,
        ResearchArtifactKind.STRATEGY_REFERENCE_PLACEHOLDER,
    ]
    return ResearchArtifactRegistryPlanningContract(
        contract_id="research-artifact-registry-planning-contract-v1",
        artifact_kinds=artifact_kinds,
        metadata_placeholders=default_research_artifact_metadata_placeholders(),
        reference_placeholders=default_research_artifact_reference_placeholders(),
        provenance_placeholders=default_research_artifact_provenance_placeholders(),
        lifecycle_placeholders=default_research_artifact_lifecycle_placeholders(),
    )

