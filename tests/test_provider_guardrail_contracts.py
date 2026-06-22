from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.approval import (
    ProviderApprovalRecord,
    approve_for_design,
    create_provider_approval_record,
)
from stark_terminal_data_platform.providers.guardrails import (
    ProviderGuardrailDecision,
    ProviderGuardrailPolicy,
    ProviderIntegrationMode,
    default_provider_guardrail_policy,
    evaluate_provider_guardrails,
    reject_execution_capabilities,
)
from stark_terminal_data_platform.providers.readiness import ProviderComplianceChecklist


def _approved_synthetic_record() -> ProviderApprovalRecord:
    record = create_provider_approval_record(
        provider_name="local_sample_design",
        requested_capabilities=[ProviderCapability.INSTRUMENT_MASTER, ProviderCapability.HEALTH_CHECK],
        requester="test",
        requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
    )
    return approve_for_design(record, reviewer="reviewer")


def test_default_policy_forbids_dangerous_provider_behavior() -> None:
    policy = default_provider_guardrail_policy(Settings())

    assert policy.network_calls_allowed is False
    assert policy.scraping_allowed is False
    assert policy.credentials_allowed is False
    assert policy.execution_allowed is False
    assert policy.real_ingestion_allowed is False
    assert policy.synthetic_only is True


def test_policy_rejects_execution_allowed_and_invalid_real_ingestion() -> None:
    with pytest.raises(ValidationError):
        ProviderGuardrailPolicy(policy_id="p1", name="bad", execution_allowed=True)

    with pytest.raises(ValidationError):
        ProviderGuardrailPolicy(
            policy_id="p2",
            name="bad",
            real_ingestion_allowed=True,
            synthetic_only=True,
        )


def test_synthetic_only_safe_mode_allows_design_contracts() -> None:
    result = evaluate_provider_guardrails(
        provider_name="local_sample_design",
        requested_capabilities=[ProviderCapability.INSTRUMENT_MASTER, ProviderCapability.HEALTH_CHECK],
        policy=default_provider_guardrail_policy(Settings()),
        approval=_approved_synthetic_record(),
        compliance=ProviderComplianceChecklist(
            provider_name="local_sample_design",
            terms_review_completed=True,
        ),
    )

    assert result.decision == ProviderGuardrailDecision.ALLOW
    assert result.risk_level.value == "LOW"


def test_execution_order_broker_capabilities_are_blocked() -> None:
    rejected = reject_execution_capabilities(["ORDER_PLACEMENT", "broker execution"])
    assert rejected

    result = evaluate_provider_guardrails(
        provider_name="broker_execution_provider",
        requested_capabilities=["ORDER_PLACEMENT"],
        policy=default_provider_guardrail_policy(Settings()),
        approval=_approved_synthetic_record(),
        compliance=ProviderComplianceChecklist(
            provider_name="broker_execution_provider",
            terms_review_completed=True,
        ),
    )

    assert result.decision == ProviderGuardrailDecision.BLOCK
    assert any("execution" in reason.lower() for reason in result.reasons)


def test_missing_approval_and_terms_review_block_provider() -> None:
    policy = default_provider_guardrail_policy(Settings())
    missing_approval = evaluate_provider_guardrails(
        provider_name="local_sample_design",
        requested_capabilities=[ProviderCapability.HEALTH_CHECK],
        policy=policy,
    )
    assert missing_approval.decision == ProviderGuardrailDecision.BLOCK
    assert any("approval" in reason.lower() for reason in missing_approval.reasons)

    missing_terms = evaluate_provider_guardrails(
        provider_name="local_sample_design",
        requested_capabilities=[ProviderCapability.HEALTH_CHECK],
        policy=policy,
        approval=_approved_synthetic_record(),
        compliance=ProviderComplianceChecklist(provider_name="local_sample_design"),
    )
    assert missing_terms.decision == ProviderGuardrailDecision.BLOCK
    assert any("terms" in reason.lower() for reason in missing_terms.reasons)


def test_network_scraping_credentials_and_real_ingestion_modes_block_by_default() -> None:
    approval = ProviderApprovalRecord(
        provider_name="future_vendor",
        requested_mode=ProviderIntegrationMode.READ_ONLY_PRODUCTION,
        approval_status="APPROVED_FOR_DESIGN",
        requested_capabilities=[ProviderCapability.HISTORICAL_BARS],
        approved_capabilities=[ProviderCapability.HISTORICAL_BARS],
        requester="test",
        reviewer="reviewer",
        terms_review_completed=True,
        credentials_required=True,
        network_calls_required=True,
        scraping_required=True,
    )
    result = evaluate_provider_guardrails(
        provider_name="future_vendor",
        requested_capabilities=[ProviderCapability.HISTORICAL_BARS],
        policy=default_provider_guardrail_policy(Settings()),
        approval=approval,
        compliance=ProviderComplianceChecklist(
            provider_name="future_vendor",
            terms_review_completed=True,
        ),
    )

    assert result.decision == ProviderGuardrailDecision.BLOCK
    reasons = " ".join(result.reasons).lower()
    assert "network" in reasons
    assert "scraping" in reasons
    assert "credentials" in reasons
    assert "synthetic" in reasons
