from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_safety.approval import (
    DecisionApprovalPlaceholder,
    evaluate_decision_approval_placeholders,
)
from stark_terminal_core.decision_safety.blocked_outputs import DecisionBlockedOutputPolicy
from stark_terminal_core.decision_safety.guardrails import (
    DecisionSafetyGuardrailSet,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_safety_notes,
)
from stark_terminal_core.decision_safety.human_review import DecisionHumanReviewGateSet
from stark_terminal_core.decision_safety.overrides import (
    DecisionOverrideProhibition,
    evaluate_decision_override_prohibitions,
)


class DecisionSafetyReadinessReport(BaseModel):
    report_id: str
    guardrails_complete: bool
    human_review_gates_complete: bool
    approval_placeholders_complete: bool
    override_prohibitions_complete: bool
    blocked_output_policy_complete: bool
    ready_for_recommendations: bool = False
    ready_for_action_generation: bool = False
    ready_for_confidence_scoring: bool = False
    ready_for_decision_object_generation: bool = False
    ready_for_execution: bool = False
    ready_for_decision_desk_api_skeleton: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    generated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision safety readiness report text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def readiness_must_not_enable_outputs(self) -> DecisionSafetyReadinessReport:
        if self.ready_for_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 39")
        if self.ready_for_action_generation:
            raise ValueError("action generation is forbidden in Prompt 39")
        if self.ready_for_confidence_scoring:
            raise ValueError("confidence scoring is forbidden in Prompt 39")
        if self.ready_for_decision_object_generation:
            raise ValueError("DecisionObject generation is forbidden in Prompt 39")
        if self.ready_for_execution:
            raise ValueError("execution is forbidden in Prompt 39")
        if self.ready_for_decision_desk_api_skeleton and self.blockers:
            raise ValueError("API skeleton readiness requires no blockers")
        return self


def build_decision_safety_readiness_report(
    guardrail_set: DecisionSafetyGuardrailSet,
    human_review_gate_set: DecisionHumanReviewGateSet,
    approval_placeholders: list[DecisionApprovalPlaceholder],
    override_prohibitions: list[DecisionOverrideProhibition],
    blocked_output_policy: DecisionBlockedOutputPolicy,
) -> DecisionSafetyReadinessReport:
    blockers = [
        *guardrail_set.blockers,
        *human_review_gate_set.blockers,
        *evaluate_decision_approval_placeholders(approval_placeholders),
        *evaluate_decision_override_prohibitions(override_prohibitions),
    ]
    warnings = [
        *guardrail_set.warnings,
        *human_review_gate_set.warnings,
        "readiness is guardrail planning only and is not approval",
    ]
    blocked_output_policy_complete = bool(blocked_output_policy.blocked_outputs)
    if not blocked_output_policy_complete:
        blockers.append("blocked output policy is missing blocked outputs")
    approval_placeholders_complete = bool(approval_placeholders) and not evaluate_decision_approval_placeholders(
        approval_placeholders,
    )
    override_prohibitions_complete = bool(override_prohibitions) and not evaluate_decision_override_prohibitions(
        override_prohibitions,
    )
    ready_for_decision_desk_api_skeleton = (
        guardrail_set.complete
        and human_review_gate_set.complete
        and approval_placeholders_complete
        and override_prohibitions_complete
        and blocked_output_policy_complete
        and not blockers
    )
    return DecisionSafetyReadinessReport(
        report_id="decision-safety-readiness-report-v1",
        guardrails_complete=guardrail_set.complete,
        human_review_gates_complete=human_review_gate_set.complete,
        approval_placeholders_complete=approval_placeholders_complete,
        override_prohibitions_complete=override_prohibitions_complete,
        blocked_output_policy_complete=blocked_output_policy_complete,
        ready_for_recommendations=False,
        ready_for_action_generation=False,
        ready_for_confidence_scoring=False,
        ready_for_decision_object_generation=False,
        ready_for_execution=False,
        ready_for_decision_desk_api_skeleton=ready_for_decision_desk_api_skeleton,
        blockers=blockers,
        warnings=warnings,
    )


def decision_safety_ready_for_recommendations(report: DecisionSafetyReadinessReport) -> bool:
    return False


def decision_safety_ready_for_decision_object_generation(report: DecisionSafetyReadinessReport) -> bool:
    return False


def decision_safety_ready_for_execution(report: DecisionSafetyReadinessReport) -> bool:
    return False


def decision_safety_ready_for_api_skeleton(report: DecisionSafetyReadinessReport) -> bool:
    return (
        report.guardrails_complete
        and report.human_review_gates_complete
        and report.approval_placeholders_complete
        and report.override_prohibitions_complete
        and report.blocked_output_policy_complete
        and not report.blockers
    )
