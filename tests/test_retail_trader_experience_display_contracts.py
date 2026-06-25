from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RETAIL_TRADER_EXPERIENCE_DISPLAY_FORBIDDEN_OUTPUTS,
    RetailTraderExperienceDisplayBadgeKind,
    RetailTraderExperienceDisplayContractMetadata,
    RetailTraderExperienceDisplayJourneyKind,
    RetailTraderExperienceDisplayPersonaKind,
    RetailTraderExperienceDisplaySectionKind,
    RetailTraderExperienceDisplayStage,
    RetailTraderExperienceDisplayWidgetKind,
    default_retail_trader_experience_display_contract_metadata,
)


def _contract_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "contract_id": "display-contract-test",
        "persona_kinds": [RetailTraderExperienceDisplayPersonaKind.RETAIL_TRADER_VISUAL_PLACEHOLDER],
        "journey_kinds": [RetailTraderExperienceDisplayJourneyKind.ONBOARDING_VISUAL_PLACEHOLDER],
        "section_kinds": [RetailTraderExperienceDisplaySectionKind.OVERVIEW],
        "widget_kinds": [RetailTraderExperienceDisplayWidgetKind.PLACEHOLDER],
        "badge_kinds": [RetailTraderExperienceDisplayBadgeKind.PLANNING_ONLY],
        "forbidden_outputs": list(RETAIL_TRADER_EXPERIENCE_DISPLAY_FORBIDDEN_OUTPUTS),
    }
    values.update(overrides)
    return values


def test_default_retail_trader_experience_display_contract_metadata_validates() -> None:
    metadata = default_retail_trader_experience_display_contract_metadata()

    assert metadata.stage == RetailTraderExperienceDisplayStage.DISPLAY_CONTRACT_SKELETON
    assert metadata.returns_unavailable_by_default is True
    assert metadata.active_ui_allowed is False
    assert metadata.suitability_profiling_allowed is False
    assert metadata.persona_kinds
    assert metadata.journey_kinds
    assert metadata.section_kinds
    assert metadata.widget_kinds
    assert metadata.badge_kinds


@pytest.mark.parametrize(
    "field",
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
def test_retail_trader_experience_display_contract_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayContractMetadata(**_contract_kwargs(**{field: True}))


def test_retail_trader_experience_display_contract_enforces_unavailable_default() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayContractMetadata(
            **_contract_kwargs(returns_unavailable_by_default=False)
        )


def test_retail_trader_experience_display_contract_rejects_unknown_kinds() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayContractMetadata(
            **_contract_kwargs(persona_kinds=[RetailTraderExperienceDisplayPersonaKind.UNKNOWN])
        )


def test_retail_trader_experience_display_contract_requires_forbidden_outputs() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayContractMetadata(**_contract_kwargs(forbidden_outputs=["active UI"]))
