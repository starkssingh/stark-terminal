from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    ResearchArtifactForbiddenBehaviorKind,
)
from stark_terminal_core.research_artifact_registry_boundary.modules import (
    ResearchArtifactModuleBoundaryPolicy,
    default_research_artifact_module_boundary_policies,
    evaluate_research_artifact_module_boundary_policies,
)


def test_research_artifact_module_boundary_default_policies_validate() -> None:
    policies = default_research_artifact_module_boundary_policies()
    families = {policy.module_family for policy in policies}

    assert families == {
        "research_artifact_registry",
        "research_artifact_registry_api",
        "research_artifact_registry_display",
        "research_artifact_registry_boundary",
    }
    assert evaluate_research_artifact_module_boundary_policies(policies) == []
    for policy in policies:
        assert policy.forbidden_behaviors
        assert ResearchArtifactForbiddenBehaviorKind.EXECUTION in policy.forbidden_behaviors
        assert policy.may_ingest_artifacts is False
        assert policy.may_persist_artifacts is False
        assert policy.may_upload_files is False
        assert policy.may_download_files is False
        assert policy.may_preview_files is False
        assert policy.may_create_active_ui is False
        assert policy.may_create_frontend_components is False
        assert policy.may_create_desktop_components is False
        assert policy.may_parse_papers is False
        assert policy.may_parse_pdfs is False
        assert policy.may_ingest_arxiv is False
        assert policy.may_call_llm_analysis is False
        assert policy.may_generate_strategies is False
        assert policy.may_generate_strategy_code is False
        assert policy.may_run_backtests is False
        assert policy.may_optimize is False
        assert policy.may_generate_recommendations is False
        assert policy.may_score_confidence is False
        assert policy.may_generate_decision_objects is False
        assert policy.may_generate_readiness_to_trade is False
        assert policy.may_expose_broker_controls is False
        assert policy.may_execute is False


@pytest.mark.parametrize(
    "flag",
    [
        "may_ingest_artifacts",
        "may_persist_artifacts",
        "may_upload_files",
        "may_download_files",
        "may_preview_files",
        "may_create_active_ui",
        "may_create_frontend_components",
        "may_create_desktop_components",
        "may_parse_papers",
        "may_parse_pdfs",
        "may_ingest_arxiv",
        "may_call_llm_analysis",
        "may_generate_strategies",
        "may_generate_strategy_code",
        "may_run_backtests",
        "may_optimize",
        "may_generate_recommendations",
        "may_generate_actions",
        "may_score_confidence",
        "may_generate_decision_objects",
        "may_generate_readiness_to_trade",
        "may_expose_broker_controls",
        "may_execute",
        "may_grant_approval",
        "may_grant_override",
    ],
)
def test_research_artifact_module_boundary_rejects_dangerous_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactModuleBoundaryPolicy(
            policy_id="research-artifact-module-policy-test-v1",
            module_family="research_artifact_registry",
            allowed_purpose="boundary test",
            forbidden_behaviors=[ResearchArtifactForbiddenBehaviorKind.EXECUTION],
            **{flag: True},
        )


def test_research_artifact_module_boundary_rejects_unknown_forbidden_behavior() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactModuleBoundaryPolicy(
            policy_id="research-artifact-module-policy-test-v1",
            module_family="research_artifact_registry",
            allowed_purpose="boundary test",
            forbidden_behaviors=[ResearchArtifactForbiddenBehaviorKind.UNKNOWN],
        )

