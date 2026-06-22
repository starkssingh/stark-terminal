from pytest import raises

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.candidates import (
    ProviderCandidateChecklist,
    ProviderDataAccessMethod,
    create_provider_candidate_profile,
)
from stark_terminal_data_platform.providers.selection import (
    ProviderCandidateRegistry,
    ProviderSelectionDecision,
    default_provider_selection_criteria,
)


def _profile(candidate_id: str = "candidate"):
    return create_provider_candidate_profile(
        candidate_id=candidate_id,
        provider_name=f"{candidate_id}_local_file",
        display_name=f"{candidate_id} Local File",
        data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
        requested_capabilities=[
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HISTORICAL_BARS,
            ProviderCapability.HEALTH_CHECK,
        ],
    )


def _checklist(candidate_id: str) -> ProviderCandidateChecklist:
    return ProviderCandidateChecklist(
        candidate_id=candidate_id,
        terms_review_available=True,
        storage_rights_known=True,
        redistribution_rights_known=True,
        rate_limits_known=True,
        attribution_requirements_known=True,
        delayed_data_requirements_known=True,
        data_quality_plan_ready=True,
        audit_logging_plan_ready=True,
        fallback_plan_ready=True,
        no_scraping_or_approved_scraping=True,
    )


def test_candidate_registry_register_get_list_and_replace() -> None:
    registry = ProviderCandidateRegistry()
    profile = _profile()
    checklist = _checklist(profile.candidate_id)

    registry.register(profile, checklist)
    assert registry.get(profile.candidate_id) == profile
    assert registry.get_checklist(profile.candidate_id) == checklist
    assert registry.list_candidates() == [profile]

    with raises(ValueError):
        registry.register(profile)

    replacement = _profile("candidate")
    registry.register(replacement, checklist, replace=True)
    assert registry.get("candidate") == replacement


def test_candidate_registry_scores_and_shortlists_without_global_state() -> None:
    first = ProviderCandidateRegistry()
    second = ProviderCandidateRegistry()
    profile = _profile("strong_candidate")
    checklist = _checklist(profile.candidate_id)
    criteria = default_provider_selection_criteria()

    first.register(profile, checklist)
    score = first.score_candidate(profile, checklist, criteria)
    shortlist = first.list_shortlist(criteria)

    assert score.decision == ProviderSelectionDecision.SHORTLIST
    assert [entry.candidate_id for entry in shortlist] == ["strong_candidate"]
    assert second.list_candidates() == []


def test_candidate_registry_rejects_mismatched_checklist() -> None:
    registry = ProviderCandidateRegistry()
    with raises(ValueError):
        registry.register(_profile("candidate"), _checklist("other"))
