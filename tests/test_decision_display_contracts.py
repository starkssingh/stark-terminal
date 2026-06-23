from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_display.contracts import (
    DecisionDisplayBadgeKind,
    DecisionDisplayCardKind,
    DecisionDisplayContractMetadata,
    DecisionDisplaySectionKind,
    default_decision_display_contract_metadata,
)


def _valid_contract_kwargs() -> dict[str, object]:
    return {
        "contract_id": "display-contract-test",
        "supported_section_kinds": [DecisionDisplaySectionKind.HEADER],
        "supported_card_kinds": [DecisionDisplayCardKind.PLACEHOLDER],
        "supported_badge_kinds": [DecisionDisplayBadgeKind.UNAVAILABLE],
        "forbidden_outputs": [
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval_workflow",
            "override_workflow",
            "readiness-to-trade",
            "execution_apis",
        ],
    }


def test_decision_display_contract_metadata_validates() -> None:
    metadata = DecisionDisplayContractMetadata(**_valid_contract_kwargs())

    assert metadata.returns_unavailable_by_default is True
    assert metadata.recommendations_allowed is False
    assert metadata.readiness_to_trade_allowed is False


@pytest.mark.parametrize(
    "override",
    [
        {"recommendations_allowed": True},
        {"action_generation_allowed": True},
        {"confidence_scoring_allowed": True},
        {"decision_object_generation_allowed": True},
        {"execution_allowed": True},
        {"approval_allowed": True},
        {"override_allowed": True},
        {"readiness_to_trade_allowed": True},
        {"returns_unavailable_by_default": False},
        {"supported_section_kinds": [DecisionDisplaySectionKind.UNKNOWN]},
        {"supported_card_kinds": [DecisionDisplayCardKind.UNKNOWN]},
        {"supported_badge_kinds": [DecisionDisplayBadgeKind.UNKNOWN]},
        {"forbidden_outputs": ["recommendation"]},
    ],
)
def test_decision_display_contract_metadata_rejects_unsafe_values(override: dict[str, object]) -> None:
    kwargs = _valid_contract_kwargs()
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionDisplayContractMetadata(**kwargs)


def test_default_decision_display_contract_metadata_covers_supported_kinds() -> None:
    metadata = default_decision_display_contract_metadata()

    assert DecisionDisplaySectionKind.HEADER in metadata.supported_section_kinds
    assert DecisionDisplayCardKind.UNAVAILABLE in metadata.supported_card_kinds
    assert DecisionDisplayBadgeKind.NOT_A_RECOMMENDATION in metadata.supported_badge_kinds
    forbidden = " ".join(metadata.forbidden_outputs).lower()
    for term in [
        "recommendation",
        "action",
        "confidence",
        "decisionobject",
        "approval",
        "override",
        "readiness-to-trade",
        "execution",
    ]:
        assert term in forbidden

