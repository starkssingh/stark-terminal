from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.providers.approval import create_provider_approval_record
from stark_terminal_data_platform.providers.guardrails import (
    ProviderIntegrationMode,
    check_provider_guardrail_health,
)
from stark_terminal_data_platform.providers.readiness import ProviderComplianceChecklist

router = APIRouter()


@router.get("/provider-guardrails/health")
def provider_guardrails_health() -> dict[str, Any]:
    status = check_provider_guardrail_health()
    return {
        "service": "stark-terminal-provider-guardrails",
        **status.model_dump(),
    }


@router.get("/provider-guardrails/contracts")
def provider_guardrails_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-provider-guardrails",
        "schema_version": settings.provider_guardrail_schema_version,
        "execution_allowed": False,
        "default_network_calls_allowed": settings.provider_network_calls_default_allowed,
        "default_scraping_allowed": settings.provider_scraping_default_allowed,
        "credentials_allowed": settings.provider_credentials_allowed,
        "approval_required": settings.provider_implementation_approval_required,
        "terms_review_required": settings.provider_terms_review_required,
        "allowed_current_mode": ProviderIntegrationMode.SYNTHETIC_ONLY.value,
        "real_ingestion_allowed_now": False,
    }


@router.get("/provider-guardrails/readiness-template")
def provider_guardrails_readiness_template() -> dict[str, Any]:
    approval = create_provider_approval_record(
        provider_name="future_local_sample_adapter_template",
        requested_capabilities=[
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HEALTH_CHECK,
        ],
        requester="architecture_review",
        requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
        notes=["Template only; not an approval for any real provider."],
    )
    compliance = ProviderComplianceChecklist(
        provider_name=approval.provider_name,
        terms_review_completed=False,
        data_quality_plan_ready=False,
        audit_logging_plan_ready=False,
        notes=["Template only; no credentials, network calls, scraping, or real ingestion."],
    )
    return {
        "service": "stark-terminal-provider-guardrails",
        "template_only": True,
        "real_provider_approved": False,
        "external_calls": False,
        "credentials_included": False,
        "execution_allowed": False,
        "approval_record": to_jsonable(approval),
        "compliance_checklist": to_jsonable(compliance),
    }
