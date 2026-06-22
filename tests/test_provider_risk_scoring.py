from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.candidates import (
    ProviderCandidateChecklist,
    ProviderDataAccessMethod,
    create_provider_candidate_profile,
)
from stark_terminal_data_platform.providers.selection import (
    ProviderSelectionDecision,
    default_provider_selection_criteria,
    score_provider_candidate,
)


def _complete_checklist(candidate_id: str) -> ProviderCandidateChecklist:
    return ProviderCandidateChecklist(
        candidate_id=candidate_id,
        terms_review_available=True,
        storage_rights_known=True,
        redistribution_rights_known=True,
        rate_limits_known=True,
        attribution_requirements_known=True,
        delayed_data_requirements_known=True,
        credential_handling_plan_ready=False,
        data_quality_plan_ready=True,
        audit_logging_plan_ready=True,
        fallback_plan_ready=True,
        no_execution_scope_confirmed=True,
        no_scraping_or_approved_scraping=True,
    )


def _base_profile(**kwargs):
    data = {
        "candidate_id": "candidate",
        "provider_name": "generic_local_file_candidate",
        "display_name": "Generic Local File Candidate",
        "data_access_method": ProviderDataAccessMethod.LOCAL_FILE,
        "requested_capabilities": [
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HISTORICAL_BARS,
            ProviderCapability.HEALTH_CHECK,
        ],
    }
    data.update(kwargs)
    return create_provider_candidate_profile(**data)


def test_strong_local_file_candidate_can_be_shortlisted_for_design_only() -> None:
    profile = _base_profile()
    score = score_provider_candidate(profile, _complete_checklist(profile.candidate_id), default_provider_selection_criteria())

    assert score.decision == ProviderSelectionDecision.SHORTLIST
    assert score.score >= 70
    assert score.blockers == []
    assert any("production approval remains unavailable" in warning.lower() for warning in score.warnings)


def test_missing_terms_and_rights_block_candidate() -> None:
    profile = _base_profile()
    score = score_provider_candidate(
        profile,
        ProviderCandidateChecklist(candidate_id=profile.candidate_id),
        default_provider_selection_criteria(),
    )

    assert score.decision == ProviderSelectionDecision.BLOCK
    reasons = " ".join(score.blockers).lower()
    assert "terms" in reasons
    assert "storage rights" in reasons
    assert "redistribution" in reasons


def test_network_credentials_and_scraping_block_by_default() -> None:
    network_profile = _base_profile(
        data_access_method=ProviderDataAccessMethod.OFFICIAL_API,
        requires_network_calls=True,
        requires_credentials=True,
    )
    network_score = score_provider_candidate(
        network_profile,
        _complete_checklist(network_profile.candidate_id),
        default_provider_selection_criteria(),
    )
    assert network_score.decision == ProviderSelectionDecision.BLOCK
    assert "network" in " ".join(network_score.blockers).lower()
    assert "credential" in " ".join(network_score.blockers).lower()

    scraping_profile = _base_profile(
        candidate_id="scraping_candidate",
        provider_name="generic_scraping_candidate",
        display_name="Generic Scraping Candidate",
        data_access_method=ProviderDataAccessMethod.SCRAPING,
        requires_scraping=True,
    )
    scraping_score = score_provider_candidate(
        scraping_profile,
        _complete_checklist(scraping_profile.candidate_id),
        default_provider_selection_criteria(),
    )
    assert scraping_score.decision == ProviderSelectionDecision.BLOCK
    assert "scraping" in " ".join(scraping_score.blockers).lower()


def test_scoring_is_deterministic() -> None:
    profile = _base_profile()
    checklist = _complete_checklist(profile.candidate_id)
    criteria = default_provider_selection_criteria()

    first = score_provider_candidate(profile, checklist, criteria)
    second = score_provider_candidate(profile, checklist, criteria)

    assert first.model_dump(exclude={"generated_at"}) == second.model_dump(exclude={"generated_at"})
