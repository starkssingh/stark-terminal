from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.candidates import (
    ProviderDataAccessMethod,
    create_provider_candidate_profile,
)
from stark_terminal_data_platform.providers.selection import (
    analyze_capability_gaps,
    default_provider_selection_criteria,
)


def test_analyze_capability_gaps_detects_missing_required_capabilities() -> None:
    profile = create_provider_candidate_profile(
        candidate_id="candidate",
        provider_name="generic_candidate",
        display_name="Generic Candidate",
        data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
        requested_capabilities=[ProviderCapability.HEALTH_CHECK],
    )

    gaps = analyze_capability_gaps(profile, default_provider_selection_criteria())
    missing = [gap.capability for gap in gaps if gap.gap]

    assert ProviderCapability.INSTRUMENT_MASTER in missing
    assert ProviderCapability.HISTORICAL_BARS in missing
    assert all(gap.required for gap in gaps)


def test_capability_gaps_pass_when_required_capabilities_present() -> None:
    profile = create_provider_candidate_profile(
        candidate_id="candidate",
        provider_name="generic_candidate",
        display_name="Generic Candidate",
        data_access_method=ProviderDataAccessMethod.LOCAL_FILE,
        requested_capabilities=[
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HISTORICAL_BARS,
            ProviderCapability.HEALTH_CHECK,
        ],
    )

    gaps = analyze_capability_gaps(profile, default_provider_selection_criteria())

    assert not [gap for gap in gaps if gap.gap]
