from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_api.contracts import (
    DecisionDeskAPIContractMetadata,
    default_decision_desk_api_contract_metadata,
)
from stark_terminal_core.decision_api.requests import (
    DecisionAPIRequestKind,
    DecisionAPIStage,
    DecisionAPIUnavailableReason,
)


def _valid_metadata_kwargs() -> dict[str, object]:
    return {
        "contract_id": "contract-1",
        "stage": DecisionAPIStage.CONTRACT_SKELETON,
        "request_kinds": [DecisionAPIRequestKind.SNAPSHOT_REQUEST],
        "unavailable_reasons": [DecisionAPIUnavailableReason.CONTRACT_SKELETON_ONLY],
        "forbidden_outputs": [
            "recommendations",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval",
            "override",
            "execution",
        ],
    }


def test_default_contract_metadata_validates() -> None:
    metadata = default_decision_desk_api_contract_metadata()

    assert metadata.stage == DecisionAPIStage.CONTRACT_SKELETON
    assert metadata.returns_unavailable_by_default is True
    assert metadata.request_kinds
    assert metadata.unavailable_reasons
    assert "recommendation_generation" in metadata.forbidden_outputs
    assert "DecisionObject_generation" in metadata.forbidden_outputs


@pytest.mark.parametrize(
    "field",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_contract_metadata_rejects_dangerous_allowed_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionDeskAPIContractMetadata(**_valid_metadata_kwargs(), **{field: True})


def test_contract_metadata_requires_unavailable_by_default() -> None:
    with pytest.raises(ValidationError):
        DecisionDeskAPIContractMetadata(**_valid_metadata_kwargs(), returns_unavailable_by_default=False)


def test_contract_metadata_requires_forbidden_output_concepts() -> None:
    with pytest.raises(ValidationError):
        DecisionDeskAPIContractMetadata(
            **{
                **_valid_metadata_kwargs(),
                "forbidden_outputs": ["recommendations"],
            },
        )

