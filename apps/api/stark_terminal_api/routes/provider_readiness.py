from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.providers.candidates import (
    ProviderDataAccessMethod,
    create_default_candidate_checklist,
    create_provider_candidate_profile,
)
from stark_terminal_data_platform.providers.selection import (
    check_provider_readiness_health,
    default_provider_selection_criteria,
    score_provider_candidate,
)

router = APIRouter()


def _template_profile():
    return create_provider_candidate_profile(
        candidate_id="generic_local_file_candidate_template",
        provider_name="generic_local_file_candidate",
        display_name="Generic Local File Candidate Template",
        data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
        requested_capabilities=[
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HISTORICAL_BARS,
            ProviderCapability.HEALTH_CHECK,
        ],
        requires_credentials=False,
        requires_network_calls=False,
        requires_scraping=False,
        provides_execution=False,
        terms_url_reference="terms-reference-placeholder",
        documentation_reference="documentation-reference-placeholder",
        notes=[
            "Template only; not a real provider approval.",
            "No external calls, no scraping, no credentials, no real ingestion, no execution APIs.",
        ],
    )


@router.get("/provider-readiness/health")
def provider_readiness_health() -> dict[str, Any]:
    status = check_provider_readiness_health()
    return {
        "service": "stark-terminal-provider-readiness",
        **status.model_dump(),
    }


@router.get("/provider-readiness/contracts")
def provider_readiness_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-provider-readiness",
        "schema_version": settings.provider_candidate_selection_schema_version,
        "real_implementation_allowed_now": False,
        "external_calls_allowed_now": False,
        "scraping_allowed_now": False,
        "credentials_allowed_now": False,
        "production_approval_available_now": False,
        "required_artifacts": [
            "provider candidate profile",
            "provider readiness checklist",
            "terms and compliance metadata",
            "data quality plan",
            "audit logging plan",
            "provider guardrail approval workflow",
            "explicit future implementation prompt",
        ],
        "current_allowed_provider_type": "local_sample_and_local_file_only",
    }


@router.get("/provider-readiness/template")
def provider_readiness_template() -> dict[str, Any]:
    profile = _template_profile()
    checklist = create_default_candidate_checklist(profile.candidate_id)
    return {
        "service": "stark-terminal-provider-readiness",
        "template_only": True,
        "real_provider_approved": False,
        "external_calls": False,
        "credentials_included": False,
        "execution_allowed": False,
        "profile": to_jsonable(profile),
        "checklist": to_jsonable(checklist),
    }


@router.get("/provider-readiness/example-score")
def provider_readiness_example_score() -> dict[str, Any]:
    profile = _template_profile()
    checklist = create_default_candidate_checklist(profile.candidate_id).model_copy(
        update={
            "terms_review_available": True,
            "storage_rights_known": True,
            "redistribution_rights_known": True,
            "rate_limits_known": True,
            "attribution_requirements_known": True,
            "delayed_data_requirements_known": True,
            "data_quality_plan_ready": True,
            "audit_logging_plan_ready": True,
            "fallback_plan_ready": True,
            "no_scraping_or_approved_scraping": True,
        }
    )
    score = score_provider_candidate(profile, checklist, default_provider_selection_criteria())
    return {
        "service": "stark-terminal-provider-readiness",
        "example_only": True,
        "real_implementation_allowed_now": False,
        "production_approval_available_now": False,
        "external_calls": False,
        "candidate_score": to_jsonable(score),
    }
