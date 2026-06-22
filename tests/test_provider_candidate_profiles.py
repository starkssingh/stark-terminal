from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.candidates import (
    ProviderCandidateChecklist,
    ProviderCandidateProfile,
    ProviderDataAccessMethod,
    candidate_requires_guardrail_block,
    create_default_candidate_checklist,
    create_provider_candidate_profile,
)


def test_valid_provider_candidate_profile() -> None:
    profile = create_provider_candidate_profile(
        candidate_id="candidate_local_file",
        provider_name="generic_local_file_candidate",
        display_name="Generic Local File Candidate",
        data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
        requested_capabilities=[
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HISTORICAL_BARS,
        ],
        claimed_exchanges=["nse"],
        notes=["metadata-only candidate"],
    )

    assert profile.candidate_id == "candidate_local_file"
    assert profile.claimed_exchanges == ["NSE"]
    assert profile.provides_execution is False


@pytest.mark.parametrize("field", ["candidate_id", "provider_name", "display_name"])
def test_empty_required_candidate_text_fields_rejected(field: str) -> None:
    data = {
        "candidate_id": "candidate",
        "provider_name": "generic_candidate",
        "display_name": "Generic Candidate",
        "data_access_method": ProviderDataAccessMethod.LOCAL_FILE,
        "requested_capabilities": [ProviderCapability.HEALTH_CHECK],
    }
    data[field] = " "

    with pytest.raises(ValidationError):
        ProviderCandidateProfile(**data)


def test_requested_capabilities_required_and_execution_rejected() -> None:
    with pytest.raises(ValidationError):
        ProviderCandidateProfile(
            candidate_id="candidate",
            provider_name="generic_candidate",
            display_name="Generic Candidate",
            data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
            requested_capabilities=[],
        )

    with pytest.raises(ValidationError):
        ProviderCandidateProfile(
            candidate_id="candidate",
            provider_name="generic_candidate",
            display_name="Generic Candidate",
            data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
            requested_capabilities=[ProviderCapability.HEALTH_CHECK],
            provides_execution=True,
        )


def test_scraping_method_requires_scraping_flag() -> None:
    with pytest.raises(ValidationError):
        ProviderCandidateProfile(
            candidate_id="scrape_candidate",
            provider_name="generic_scrape_candidate",
            display_name="Generic Scrape Candidate",
            data_access_method=ProviderDataAccessMethod.SCRAPING,
            requested_capabilities=[ProviderCapability.HISTORICAL_BARS],
        )


def test_notes_and_references_are_sanitized() -> None:
    profile = ProviderCandidateProfile(
        candidate_id="candidate",
        provider_name="generic_candidate",
        display_name="Generic Candidate",
        data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
        requested_capabilities=[ProviderCapability.HEALTH_CHECK],
        terms_url_reference="reference?token=secret",
        notes=["api_key=secret"],
    )

    assert profile.terms_url_reference == "[redacted]"
    assert profile.notes == ["[redacted]"]


def test_candidate_requires_guardrail_block_for_dangerous_defaults() -> None:
    profile = ProviderCandidateProfile(
        candidate_id="candidate",
        provider_name="generic_candidate",
        display_name="Generic Candidate",
        data_access_method=ProviderDataAccessMethod.OFFICIAL_API,
        requested_capabilities=[ProviderCapability.HISTORICAL_BARS],
        requires_credentials=True,
        requires_network_calls=True,
    )

    blockers = candidate_requires_guardrail_block(profile)
    assert any("network" in blocker.lower() for blocker in blockers)
    assert any("credential" in blocker.lower() for blocker in blockers)


def test_candidate_checklist_defaults_and_no_execution_scope() -> None:
    checklist = create_default_candidate_checklist("candidate")
    assert checklist.no_execution_scope_confirmed is True
    assert checklist.terms_review_available is False

    with pytest.raises(ValidationError):
        ProviderCandidateChecklist(candidate_id="candidate", no_execution_scope_confirmed=False)
