from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_readiness_api.contracts import (
    DecisionReadinessAPIContractMetadata,
    default_decision_readiness_api_contract_metadata,
)
from stark_terminal_core.decision_readiness_api.requests import (
    DecisionReadinessAPIStage,
    DecisionReadinessRequestKind,
    DecisionReadinessUnavailableReason,
)


def _valid_metadata_kwargs() -> dict[str, object]:
    return {
        "contract_id": "readiness-contract-1",
        "stage": DecisionReadinessAPIStage.READINESS_CONTRACT_SKELETON,
        "request_kinds": [DecisionReadinessRequestKind.READINESS_STATUS_REQUEST],
        "unavailable_reasons": [DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY],
        "forbidden_outputs": [
            "readiness-as-recommendation",
            "recommendations",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval",
            "override",
            "execution",
        ],
    }


def test_default_readiness_contract_metadata_validates() -> None:
    metadata = default_decision_readiness_api_contract_metadata()

    assert metadata.stage == DecisionReadinessAPIStage.READINESS_CONTRACT_SKELETON
    assert metadata.returns_unavailable_by_default is True
    assert metadata.readiness_status_generation_allowed is False
    assert metadata.request_kinds
    assert metadata.unavailable_reasons
    assert "readiness-as-recommendation" in metadata.forbidden_outputs
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
        "readiness_status_generation_allowed",
    ],
)
def test_readiness_contract_metadata_rejects_dangerous_allowed_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessAPIContractMetadata(**_valid_metadata_kwargs(), **{field: True})


def test_readiness_contract_metadata_requires_unavailable_by_default() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessAPIContractMetadata(
            **_valid_metadata_kwargs(),
            returns_unavailable_by_default=False,
        )


def test_readiness_contract_metadata_requires_forbidden_output_concepts() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessAPIContractMetadata(
            **{
                **_valid_metadata_kwargs(),
                "forbidden_outputs": ["recommendations"],
            },
        )
