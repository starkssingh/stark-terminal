from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.approval import ProviderApprovalRecord
from stark_terminal_data_platform.providers.guardrails import (
    ProviderApprovalStatus,
    ProviderGuardrailDecision,
    ProviderIntegrationMode,
)
from stark_terminal_data_platform.providers.local_sample import LocalSampleProviderAdapter


def test_local_sample_provider_guardrails_allow_synthetic_only_mode() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())

    result = provider.evaluate_guardrails()

    assert result.decision == ProviderGuardrailDecision.ALLOW
    assert "synthetic" in " ".join(result.reasons).lower()


def test_local_sample_provider_blocks_network_real_data_settings() -> None:
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_allow_network=True)

    with pytest.raises(ValidationError):
        Settings(local_sample_provider_allow_real_data=True)


def test_local_sample_provider_blocks_network_approval_request() -> None:
    approval = ProviderApprovalRecord(
        provider_name="local_sample",
        requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
        approval_status=ProviderApprovalStatus.APPROVED_FOR_DESIGN,
        requested_capabilities=[ProviderCapability.HISTORICAL_BARS],
        approved_capabilities=[ProviderCapability.HISTORICAL_BARS],
        requester="test",
        reviewer="reviewer",
        terms_review_completed=True,
        network_calls_required=True,
    )
    provider = LocalSampleProviderAdapter(settings=Settings(), approval=approval)

    result = provider.evaluate_guardrails()

    assert result.decision == ProviderGuardrailDecision.BLOCK
    assert any("network" in reason.lower() for reason in result.reasons)


def test_local_sample_provider_does_not_expose_execution_capabilities() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    capabilities = {capability.value.lower() for capability in provider.capabilities().capabilities}

    forbidden_terms = ("execution", "order", "broker", "credential", "real_money")

    assert all(not any(term in capability for term in forbidden_terms) for capability in capabilities)
