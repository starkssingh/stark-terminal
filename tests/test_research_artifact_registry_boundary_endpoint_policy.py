from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_boundary.endpoints import (
    ResearchArtifactEndpointBoundaryPolicy,
    default_research_artifact_endpoint_boundary_policies,
    evaluate_research_artifact_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    ResearchArtifactForbiddenBehaviorKind,
)


def test_research_artifact_endpoint_boundary_default_policies_validate() -> None:
    policies = default_research_artifact_endpoint_boundary_policies()
    families = {policy.endpoint_family for policy in policies}

    assert families == {
        "research-artifact-registry",
        "research-artifact-registry-api",
        "research-artifact-registry-display",
        "research-artifact-registry-boundary",
    }
    assert evaluate_research_artifact_endpoint_boundary_policies(policies) == []
    for policy in policies:
        assert policy.allowed_methods == ["GET"]
        assert "POST" in policy.forbidden_methods
        assert policy.read_only is True
        assert policy.unavailable_by_default is True
        assert policy.accepts_file_input is False
        assert policy.accepts_artifact_input_for_storage is False
        assert policy.accepts_paper_input is False
        assert policy.generates_active_ui is False
        assert policy.ingests_artifact is False
        assert policy.stores_artifact is False
        assert policy.uploads_file is False
        assert policy.downloads_file is False
        assert policy.previews_file is False
        assert policy.parses_paper is False
        assert policy.generates_strategy is False
        assert policy.generates_backtest is False
        assert policy.generates_recommendation is False
        assert policy.generates_decision_object is False
        assert policy.exposes_broker_controls is False
        assert policy.executes_trade is False


@pytest.mark.parametrize("flag", ["read_only", "unavailable_by_default"])
def test_research_artifact_endpoint_boundary_requires_safe_booleans(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactEndpointBoundaryPolicy(
            policy_id="research-artifact-endpoint-policy-test-v1",
            endpoint_family="research-artifact-registry",
            allowed_methods=["GET"],
            forbidden_methods=["POST"],
            forbidden_outputs=[ResearchArtifactForbiddenBehaviorKind.EXECUTION],
            **{flag: False},
        )


@pytest.mark.parametrize(
    "flag",
    [
        "accepts_file_input",
        "accepts_artifact_input_for_storage",
        "accepts_paper_input",
        "accepts_market_data_for_research_decision",
        "generates_active_ui",
        "ingests_artifact",
        "stores_artifact",
        "uploads_file",
        "downloads_file",
        "previews_file",
        "parses_paper",
        "generates_strategy",
        "generates_backtest",
        "generates_recommendation",
        "generates_decision_object",
        "exposes_broker_controls",
        "executes_trade",
    ],
)
def test_research_artifact_endpoint_boundary_rejects_dangerous_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactEndpointBoundaryPolicy(
            policy_id="research-artifact-endpoint-policy-test-v1",
            endpoint_family="research-artifact-registry",
            allowed_methods=["GET"],
            forbidden_methods=["POST"],
            forbidden_outputs=[ResearchArtifactForbiddenBehaviorKind.EXECUTION],
            **{flag: True},
        )


def test_research_artifact_endpoint_boundary_rejects_unknown_forbidden_output() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactEndpointBoundaryPolicy(
            policy_id="research-artifact-endpoint-policy-test-v1",
            endpoint_family="research-artifact-registry",
            allowed_methods=["GET"],
            forbidden_methods=["POST"],
            forbidden_outputs=[ResearchArtifactForbiddenBehaviorKind.UNKNOWN],
        )

