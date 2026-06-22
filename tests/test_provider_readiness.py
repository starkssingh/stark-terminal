from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.approval import approve_for_design, create_provider_approval_record
from stark_terminal_data_platform.providers.guardrails import (
    ProviderGuardrailDecision,
    ProviderGuardrailResult,
    ProviderIntegrationMode,
    ProviderRiskLevel,
    default_provider_guardrail_policy,
    evaluate_provider_guardrails,
)
from stark_terminal_data_platform.providers.readiness import (
    ProviderComplianceChecklist,
    ProviderReadinessReport,
    build_provider_readiness_report,
    provider_is_ready_for_design,
    provider_is_ready_for_network_tests,
    provider_is_ready_for_production,
)


def _approved_record():
    return approve_for_design(
        create_provider_approval_record(
            provider_name="local_sample_design",
            requested_capabilities=[ProviderCapability.INSTRUMENT_MASTER, ProviderCapability.HEALTH_CHECK],
            requester="architecture",
            requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
        ),
        reviewer="reviewer",
    )


def _ready_checklist() -> ProviderComplianceChecklist:
    return ProviderComplianceChecklist(
        provider_name="local_sample_design",
        terms_review_completed=True,
        scraping_prohibited=True,
        data_quality_plan_ready=True,
        audit_logging_plan_ready=True,
    )


def test_compliance_checklist_validates_and_sanitizes_notes() -> None:
    checklist = ProviderComplianceChecklist(
        provider_name="local_sample",
        notes=["api_token=secret"],
    )

    assert checklist.notes == ["[redacted]"]


def test_readiness_report_rejects_ready_when_guardrails_block() -> None:
    with pytest.raises(ValidationError):
        ProviderReadinessReport(
            provider_name="local_sample",
            approval_status="APPROVED_FOR_DESIGN",
            guardrail_decision=ProviderGuardrailDecision.BLOCK,
            compliance_ready=True,
            implementation_ready=True,
            allowed_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
            allowed_capabilities=[ProviderCapability.HEALTH_CHECK],
        )


def test_readiness_blocks_when_approval_not_approved() -> None:
    approval = create_provider_approval_record(
        provider_name="local_sample_design",
        requested_capabilities=[ProviderCapability.HEALTH_CHECK],
        requester="architecture",
    )
    guardrail_result = ProviderGuardrailResult(
        decision=ProviderGuardrailDecision.BLOCK,
        policy_id="provider_guardrails_default",
        provider_name="local_sample_design",
        reasons=["provider implementation approval is required"],
        risk_level=ProviderRiskLevel.HIGH,
    )
    report = build_provider_readiness_report(
        "local_sample_design",
        approval,
        _ready_checklist(),
        guardrail_result,
    )

    assert report.implementation_ready is False
    assert report.blockers
    assert provider_is_ready_for_design(report) is False


def test_ready_for_design_only_when_approved_compliant_and_allowed() -> None:
    approval = _approved_record()
    compliance = _ready_checklist()
    guardrail_result = evaluate_provider_guardrails(
        provider_name="local_sample_design",
        requested_capabilities=approval.requested_capabilities,
        policy=default_provider_guardrail_policy(),
        approval=approval,
        compliance=compliance,
    )
    report = build_provider_readiness_report(
        "local_sample_design",
        approval,
        compliance,
        guardrail_result,
    )

    assert report.implementation_ready is True
    assert provider_is_ready_for_design(report) is True
    assert provider_is_ready_for_network_tests(report) is False
    assert provider_is_ready_for_production(report) is False


def test_readiness_report_sanitizes_blockers_and_warnings() -> None:
    report = ProviderReadinessReport(
        provider_name="local_sample",
        approval_status="DRAFT",
        guardrail_decision=ProviderGuardrailDecision.BLOCK,
        compliance_ready=False,
        implementation_ready=False,
        allowed_mode=ProviderIntegrationMode.DISABLED,
        allowed_capabilities=[],
        blockers=["secret token"],
        warnings=["https://example.invalid/key"],
    )

    assert report.blockers == ["[redacted]"]
    assert report.warnings == ["[redacted]"]
