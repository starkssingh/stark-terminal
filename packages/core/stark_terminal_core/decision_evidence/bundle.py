from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    DecisionEvidenceStage,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    default_decision_evidence_item_contracts,
    sanitize_decision_evidence_notes,
)
from stark_terminal_core.decision_evidence.provenance import (
    DecisionEvidenceProvenanceMap,
    build_decision_evidence_provenance_map,
)


class DecisionObjectEvidenceBundleContract(BaseModel):
    bundle_id: str
    name: str
    planning_stage: DecisionEvidenceStage = DecisionEvidenceStage.CONTRACTS_ONLY
    evidence_items: list[DecisionEvidenceItemContract]
    provenance_map: DecisionEvidenceProvenanceMap | None = None
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    contracts_only: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("bundle_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence bundle text fields")

    @field_validator("evidence_items")
    @classmethod
    def evidence_items_must_be_present(cls, value: list[DecisionEvidenceItemContract]) -> list[DecisionEvidenceItemContract]:
        if not value:
            raise ValueError("decision evidence bundle evidence_items cannot be empty")
        return value

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def bundle_must_remain_contract_only(self) -> DecisionObjectEvidenceBundleContract:
        if self.planning_stage == DecisionEvidenceStage.UNKNOWN:
            raise ValueError("decision evidence planning stage cannot be UNKNOWN")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden for decision evidence bundles in Prompt 38")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden for decision evidence bundles in Prompt 38")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden for decision evidence bundles in Prompt 38")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden for decision evidence bundles in Prompt 38")
        if self.execution_allowed:
            raise ValueError("execution is forbidden for decision evidence bundles in Prompt 38")
        if not self.contracts_only:
            raise ValueError("decision evidence bundles must remain contracts-only in Prompt 38")
        return self


def create_decision_object_evidence_bundle_contract(
    bundle_id: str,
    name: str,
    evidence_items: list[DecisionEvidenceItemContract],
    provenance_map: DecisionEvidenceProvenanceMap | None = None,
    notes: list[str] | None = None,
) -> DecisionObjectEvidenceBundleContract:
    return DecisionObjectEvidenceBundleContract(
        bundle_id=bundle_id,
        name=name,
        evidence_items=evidence_items,
        provenance_map=provenance_map,
        notes=notes or [],
    )


def default_decision_object_evidence_bundle_contract() -> DecisionObjectEvidenceBundleContract:
    items = default_decision_evidence_item_contracts()
    provenance_map = build_decision_evidence_provenance_map()
    return DecisionObjectEvidenceBundleContract(
        bundle_id="decisionobject-evidence-bundle-contract-v1",
        name="DecisionObject Evidence Bundle Contract",
        planning_stage=DecisionEvidenceStage.CONTRACTS_ONLY,
        evidence_items=items,
        provenance_map=provenance_map,
        notes=[
            "Prompt 38 defines contracts only.",
            "No active DecisionObject generation, recommendations, action generation, confidence scoring, or execution is allowed.",
        ],
    )

