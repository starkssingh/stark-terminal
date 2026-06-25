from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_api.contracts import (
    RetailTraderExperienceAPIContractMetadata,
    default_retail_trader_experience_api_contract_metadata,
)
from stark_terminal_core.retail_trader_experience_api.requests import (
    RetailTraderExperienceAPIRequestKind,
    RetailTraderExperienceAPIStage,
    RetailTraderExperienceAPIUnavailableReason,
)


def test_retail_trader_experience_api_default_contract_metadata_validates() -> None:
    metadata = default_retail_trader_experience_api_contract_metadata()

    assert metadata.service_name == "stark-terminal-retail-trader-experience-api"
    assert metadata.stage == RetailTraderExperienceAPIStage.API_CONTRACT_SKELETON
    assert RetailTraderExperienceAPIRequestKind.EXPERIENCE_OVERVIEW_REQUEST in metadata.request_kinds
    assert RetailTraderExperienceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY in metadata.unavailable_reasons
    assert metadata.returns_unavailable_by_default is True
    assert metadata.suitability_profiling_allowed is False
    assert "execution_apis" in metadata.forbidden_outputs
    assert "suitability_profiling" in metadata.forbidden_outputs


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
        "suitability_profiling_allowed",
    ],
)
def test_retail_trader_experience_api_contract_metadata_rejects_unsafe_flags(field_name: str) -> None:
    metadata = default_retail_trader_experience_api_contract_metadata().model_dump()
    metadata[field_name] = True
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIContractMetadata(**metadata)


def test_retail_trader_experience_api_contract_metadata_rejects_missing_or_unknown_contract_terms() -> None:
    metadata = default_retail_trader_experience_api_contract_metadata().model_dump()
    metadata["returns_unavailable_by_default"] = False
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIContractMetadata(**metadata)

    metadata = default_retail_trader_experience_api_contract_metadata().model_dump()
    metadata["request_kinds"] = [RetailTraderExperienceAPIRequestKind.UNKNOWN]
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIContractMetadata(**metadata)

    metadata = default_retail_trader_experience_api_contract_metadata().model_dump()
    metadata["unavailable_reasons"] = [RetailTraderExperienceAPIUnavailableReason.UNKNOWN]
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIContractMetadata(**metadata)

    metadata = default_retail_trader_experience_api_contract_metadata().model_dump()
    metadata["forbidden_outputs"] = ["active UI"]
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIContractMetadata(**metadata)
