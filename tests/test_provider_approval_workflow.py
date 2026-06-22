from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.approval import (
    ProviderApprovalRecord,
    approve_for_design,
    block_provider,
    create_provider_approval_record,
)
from stark_terminal_data_platform.providers.guardrails import ProviderApprovalStatus, ProviderIntegrationMode


def test_valid_provider_approval_record() -> None:
    record = create_provider_approval_record(
        provider_name="local_sample_design",
        requested_capabilities=[ProviderCapability.INSTRUMENT_MASTER],
        requester="architecture",
    )

    assert record.provider_name == "local_sample_design"
    assert record.approval_status == ProviderApprovalStatus.DRAFT
    assert record.requested_mode == ProviderIntegrationMode.SYNTHETIC_ONLY


def test_empty_provider_requester_and_capabilities_rejected() -> None:
    with pytest.raises(ValidationError):
        ProviderApprovalRecord(
            provider_name="",
            requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
            requested_capabilities=[ProviderCapability.HEALTH_CHECK],
            requester="architecture",
        )
    with pytest.raises(ValidationError):
        ProviderApprovalRecord(
            provider_name="local_sample",
            requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
            requested_capabilities=[ProviderCapability.HEALTH_CHECK],
            requester="",
        )
    with pytest.raises(ValidationError):
        ProviderApprovalRecord(
            provider_name="local_sample",
            requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
            requested_capabilities=[],
            requester="architecture",
        )


def test_execution_required_and_invalid_approved_capability_are_rejected() -> None:
    with pytest.raises(ValidationError):
        ProviderApprovalRecord(
            provider_name="local_sample",
            requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
            requested_capabilities=[ProviderCapability.HEALTH_CHECK],
            requester="architecture",
            execution_required=True,
        )

    with pytest.raises(ValidationError):
        ProviderApprovalRecord(
            provider_name="local_sample",
            requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
            requested_capabilities=[ProviderCapability.HEALTH_CHECK],
            approved_capabilities=[ProviderCapability.HISTORICAL_BARS],
            requester="architecture",
        )


def test_approve_for_design_and_block_provider() -> None:
    record = create_provider_approval_record(
        provider_name="local_sample",
        requested_capabilities=[ProviderCapability.HEALTH_CHECK],
        requester="architecture",
    )
    approved = approve_for_design(record, reviewer="reviewer")

    assert approved.approval_status == ProviderApprovalStatus.APPROVED_FOR_DESIGN
    assert approved.approved_capabilities == [ProviderCapability.HEALTH_CHECK]
    assert approved.reviewed_at is not None

    blocked = block_provider(approved, reviewer="reviewer", reason="terms review missing")
    assert blocked.approval_status == ProviderApprovalStatus.BLOCKED
    assert blocked.approved_capabilities == []
    assert any("terms review missing" in note for note in blocked.notes)


def test_production_approval_with_scraping_required_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ProviderApprovalRecord(
            provider_name="future_vendor",
            requested_mode=ProviderIntegrationMode.READ_ONLY_PRODUCTION,
            approval_status=ProviderApprovalStatus.APPROVED_FOR_PRODUCTION,
            requested_capabilities=[ProviderCapability.HISTORICAL_BARS],
            approved_capabilities=[ProviderCapability.HISTORICAL_BARS],
            requester="architecture",
            reviewer="reviewer",
            scraping_required=True,
        )
