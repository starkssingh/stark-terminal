from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.approval import ProviderApprovalRecord
from stark_terminal_data_platform.providers.guardrails import (
    APPROVED_PROVIDER_STATUSES,
    ProviderApprovalStatus,
    ProviderGuardrailDecision,
    ProviderGuardrailResult,
    ProviderIntegrationMode,
    sanitize_provider_notes,
)


class ProviderComplianceChecklist(BaseModel):
    provider_name: str
    terms_review_completed: bool = False
    redistribution_allowed: bool | None = None
    storage_allowed: bool | None = None
    delayed_data_required: bool | None = None
    attribution_required: bool | None = None
    scraping_prohibited: bool = True
    credential_handling_reviewed: bool = False
    rate_limits_documented: bool = False
    data_quality_plan_ready: bool = False
    audit_logging_plan_ready: bool = False
    notes: list[str] = Field(default_factory=list)
    schema_version: str = "v1"

    @field_validator("provider_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider compliance text fields cannot be empty")
        return normalized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)


class ProviderReadinessReport(BaseModel):
    provider_name: str
    approval_status: ProviderApprovalStatus
    guardrail_decision: ProviderGuardrailDecision
    compliance_ready: bool
    implementation_ready: bool
    allowed_mode: ProviderIntegrationMode
    allowed_capabilities: list[ProviderCapability]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "v1"

    @field_validator("provider_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider readiness text fields cannot be empty")
        return normalized

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @model_validator(mode="after")
    def readiness_must_not_bypass_guardrails(self) -> ProviderReadinessReport:
        if self.implementation_ready and self.guardrail_decision == ProviderGuardrailDecision.BLOCK:
            raise ValueError("implementation cannot be ready when guardrails block the provider")
        if self.implementation_ready and self.approval_status.value not in APPROVED_PROVIDER_STATUSES:
            raise ValueError("implementation cannot be ready without approved provider status")
        return self


def build_provider_readiness_report(
    provider_name: str,
    approval: ProviderApprovalRecord,
    compliance: ProviderComplianceChecklist,
    guardrail_result: ProviderGuardrailResult,
) -> ProviderReadinessReport:
    blockers: list[str] = []
    warnings: list[str] = []

    if guardrail_result.decision == ProviderGuardrailDecision.BLOCK:
        blockers.extend(guardrail_result.reasons)
    if approval.approval_status.value not in APPROVED_PROVIDER_STATUSES:
        blockers.append("provider is not approved for implementation")
    if not compliance.terms_review_completed:
        blockers.append("terms review is incomplete")
    if not compliance.data_quality_plan_ready:
        blockers.append("data quality plan is not ready")
    if not compliance.audit_logging_plan_ready:
        blockers.append("audit logging plan is not ready")
    if not compliance.scraping_prohibited:
        blockers.append("scraping must remain prohibited unless separately reviewed")
    if approval.credentials_required and not compliance.credential_handling_reviewed:
        blockers.append("credential handling review is incomplete")
    if approval.network_calls_required and not compliance.rate_limits_documented:
        blockers.append("rate limits are not documented for network testing")

    if approval.approval_status == ProviderApprovalStatus.APPROVED_FOR_PRODUCTION:
        warnings.append("production approval is documented only; no production provider implementation exists in Prompt 20")
    if approval.network_calls_required:
        warnings.append("network tests require a future explicit prompt and guardrail update")

    compliance_ready = (
        compliance.terms_review_completed
        and compliance.data_quality_plan_ready
        and compliance.audit_logging_plan_ready
        and compliance.scraping_prohibited
        and (not approval.credentials_required or compliance.credential_handling_reviewed)
        and (not approval.network_calls_required or compliance.rate_limits_documented)
    )
    approved = approval.approval_status.value in APPROVED_PROVIDER_STATUSES
    implementation_ready = (
        guardrail_result.decision != ProviderGuardrailDecision.BLOCK
        and approved
        and compliance_ready
        and not blockers
    )

    allowed_mode = approval.requested_mode if guardrail_result.decision != ProviderGuardrailDecision.BLOCK else ProviderIntegrationMode.DISABLED
    allowed_capabilities = approval.approved_capabilities if guardrail_result.decision != ProviderGuardrailDecision.BLOCK else []

    return ProviderReadinessReport(
        provider_name=provider_name,
        approval_status=approval.approval_status,
        guardrail_decision=guardrail_result.decision,
        compliance_ready=compliance_ready,
        implementation_ready=implementation_ready,
        allowed_mode=allowed_mode,
        allowed_capabilities=allowed_capabilities,
        blockers=blockers,
        warnings=warnings,
        schema_version=approval.schema_version,
    )


def provider_is_ready_for_design(report: ProviderReadinessReport) -> bool:
    return (
        report.implementation_ready
        and report.approval_status
        in {
            ProviderApprovalStatus.APPROVED_FOR_DESIGN,
            ProviderApprovalStatus.APPROVED_FOR_LOCAL_TESTS,
            ProviderApprovalStatus.APPROVED_FOR_NETWORK_TESTS,
            ProviderApprovalStatus.APPROVED_FOR_PRODUCTION,
        }
    )


def provider_is_ready_for_network_tests(report: ProviderReadinessReport) -> bool:
    return (
        report.implementation_ready
        and report.approval_status
        in {
            ProviderApprovalStatus.APPROVED_FOR_NETWORK_TESTS,
            ProviderApprovalStatus.APPROVED_FOR_PRODUCTION,
        }
        and report.allowed_mode
        in {
            ProviderIntegrationMode.SANDBOX_NETWORK,
            ProviderIntegrationMode.READ_ONLY_PRODUCTION,
        }
    )


def provider_is_ready_for_production(report: ProviderReadinessReport) -> bool:
    return (
        report.implementation_ready
        and report.approval_status == ProviderApprovalStatus.APPROVED_FOR_PRODUCTION
        and report.allowed_mode == ProviderIntegrationMode.READ_ONLY_PRODUCTION
        and report.guardrail_decision == ProviderGuardrailDecision.ALLOW
    )
