from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.candidates import ProviderDataAccessMethod
from stark_terminal_data_platform.providers.selection import (
    ProviderSelectionCriteria,
    default_provider_selection_criteria,
    readiness_thresholds_from_settings,
)


def test_default_selection_criteria_are_conservative() -> None:
    criteria = default_provider_selection_criteria()

    assert ProviderCapability.INSTRUMENT_MASTER in criteria.required_capabilities
    assert ProviderCapability.HISTORICAL_BARS in criteria.required_capabilities
    assert ProviderCapability.HEALTH_CHECK in criteria.required_capabilities
    assert ProviderDataAccessMethod.LOCAL_FILE in criteria.preferred_data_access_methods
    assert criteria.allow_network_required_candidates is False
    assert criteria.allow_scraping_candidates is False
    assert criteria.allow_credential_required_candidates is False
    assert criteria.require_terms_review is True


def test_selection_criteria_validate_required_fields() -> None:
    with pytest.raises(ValidationError):
        ProviderSelectionCriteria(
            criteria_id=" ",
            name="Default",
            required_capabilities=[ProviderCapability.HEALTH_CHECK],
            preferred_data_access_methods=[ProviderDataAccessMethod.LOCAL_FILE],
        )

    with pytest.raises(ValidationError):
        ProviderSelectionCriteria(
            criteria_id="criteria",
            name="Default",
            required_capabilities=[],
            preferred_data_access_methods=[ProviderDataAccessMethod.LOCAL_FILE],
        )

    with pytest.raises(ValidationError):
        ProviderSelectionCriteria(
            criteria_id="criteria",
            name="Default",
            required_capabilities=[ProviderCapability.HEALTH_CHECK],
            preferred_data_access_methods=[],
        )


def test_readiness_thresholds_from_settings_are_ordered() -> None:
    thresholds = readiness_thresholds_from_settings()

    assert thresholds["design"] == 70
    assert thresholds["network_tests"] >= thresholds["design"]
    assert thresholds["production"] >= thresholds["network_tests"]
