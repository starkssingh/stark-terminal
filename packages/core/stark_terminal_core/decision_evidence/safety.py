from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence.bundle import DecisionObjectEvidenceBundleContract
from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_notes,
)


class DecisionEvidenceSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_real_data: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_execution: bool = False
    require_source_reference: bool = True
    require_validation_checklist: bool = True
    require_human_review_attachment: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> DecisionEvidenceSafetyPolicy:
        if self.allow_real_data:
            raise ValueError("real data is forbidden for decision evidence in Prompt 38")
        if self.allow_recommendations:
            raise ValueError("recommendations are forbidden for decision evidence in Prompt 38")
        if self.allow_action_generation:
            raise ValueError("action generation is forbidden for decision evidence in Prompt 38")
        if self.allow_confidence_scoring:
            raise ValueError("confidence scoring is forbidden for decision evidence in Prompt 38")
        if self.allow_decision_object_generation:
            raise ValueError("DecisionObject generation is forbidden for decision evidence in Prompt 38")
        if self.allow_execution:
            raise ValueError("execution is forbidden for decision evidence in Prompt 38")
        if not self.require_source_reference:
            raise ValueError("source references are required for decision evidence in Prompt 38")
        if not self.require_validation_checklist:
            raise ValueError("validation checklist is required for decision evidence in Prompt 38")
        if not self.require_human_review_attachment:
            raise ValueError("human-review attachments are required for decision evidence in Prompt 38")
        return self


class DecisionEvidenceSafetyResult(BaseModel):
    decision: str
    reasons: list[str]
    policy_id: str
    evaluated_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"

    @field_validator("decision", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_evidence_notes(value)
        if not sanitized:
            raise ValueError("decision evidence safety result reasons cannot be empty")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)


def default_decision_evidence_safety_policy(settings: Any | None = None) -> DecisionEvidenceSafetyPolicy:
    notes = ["Prompt 38 permits DecisionObject evidence bundle contracts only."]
    if settings is not None:
        notes.append(f"planning_stage={settings.decision_evidence_planning_stage}")
    return DecisionEvidenceSafetyPolicy(
        policy_id="decision-evidence-safety-policy-v1",
        name="DecisionObject Evidence Bundle Safety Policy",
        notes=notes,
    )


def evaluate_decision_evidence_bundle_safety(
    bundle: DecisionObjectEvidenceBundleContract,
    policy: DecisionEvidenceSafetyPolicy,
) -> DecisionEvidenceSafetyResult:
    reasons: list[str] = []
    if policy.allow_real_data:
        reasons.append("real data is not allowed")
    if bundle.recommendations_allowed or policy.allow_recommendations:
        reasons.append("recommendations are not allowed")
    if bundle.action_generation_allowed or policy.allow_action_generation:
        reasons.append("action generation is not allowed")
    if bundle.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("confidence scoring is not allowed")
    if bundle.decision_object_generation_allowed or policy.allow_decision_object_generation:
        reasons.append("DecisionObject generation is not allowed")
    if bundle.execution_allowed or policy.allow_execution:
        reasons.append("execution is not allowed")
    if not bundle.contracts_only:
        reasons.append("bundle must remain contracts-only")
    if bundle.provenance_map is None and policy.require_source_reference:
        reasons.append("provenance map is required")
    if reasons:
        return DecisionEvidenceSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return DecisionEvidenceSafetyResult(
        decision="contracts_allowed",
        reasons=[
            "DecisionObject evidence bundle is contracts-only",
            "recommendations, action generation, confidence scoring, DecisionObject generation, and execution remain blocked",
        ],
        policy_id=policy.policy_id,
    )


def evaluate_decision_evidence_items_safety(
    items: list[DecisionEvidenceItemContract],
    policy: DecisionEvidenceSafetyPolicy,
) -> DecisionEvidenceSafetyResult:
    reasons: list[str] = []
    if not items:
        reasons.append("decision evidence items are missing")
    for item in items:
        if item.value_payload_allowed:
            reasons.append(f"{item.item_id}: value payloads are not allowed")
        if item.recommendation or policy.allow_recommendations:
            reasons.append(f"{item.item_id}: recommendations are not allowed")
        if item.action_generated or policy.allow_action_generation:
            reasons.append(f"{item.item_id}: action generation is not allowed")
        if item.confidence_generated or policy.allow_confidence_scoring:
            reasons.append(f"{item.item_id}: confidence scoring is not allowed")
        if item.decision_object_generated or policy.allow_decision_object_generation:
            reasons.append(f"{item.item_id}: DecisionObject generation is not allowed")
        if item.execution_ready or policy.allow_execution:
            reasons.append(f"{item.item_id}: execution readiness is not allowed")
        if not item.source_reference_required and policy.require_source_reference:
            reasons.append(f"{item.item_id}: source references are required")
        if not item.validation_required and policy.require_validation_checklist:
            reasons.append(f"{item.item_id}: validation is required")
        if not item.human_review_required and policy.require_human_review_attachment:
            reasons.append(f"{item.item_id}: human-review attachment is required")
    if policy.allow_real_data:
        reasons.append("real data is not allowed")
    if reasons:
        return DecisionEvidenceSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return DecisionEvidenceSafetyResult(
        decision="contracts_allowed",
        reasons=["decision evidence items are contract metadata only"],
        policy_id=policy.policy_id,
    )


def reject_decision_object_generation(
    reason: str = "DecisionObject generation is forbidden in Prompt 38",
) -> DecisionEvidenceSafetyResult:
    return DecisionEvidenceSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="decision-evidence-safety-policy-v1",
    )


def reject_recommendation_action_confidence_generation(
    reason: str = "recommendation, action, and confidence generation are forbidden in Prompt 38",
) -> DecisionEvidenceSafetyResult:
    return DecisionEvidenceSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="decision-evidence-safety-policy-v1",
    )

