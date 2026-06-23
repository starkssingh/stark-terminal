from __future__ import annotations

from pathlib import Path

from stark_terminal_core.decision_boundary.endpoints import default_decision_endpoint_boundary_policies
from stark_terminal_core.decision_boundary.forbidden import (
    DecisionForbiddenBehaviorKind,
    default_decision_forbidden_behavior_registry,
)
from stark_terminal_core.decision_boundary.invariants import evaluate_decision_boundary_invariants
from stark_terminal_core.decision_boundary.modules import default_decision_module_boundary_policies


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ENDPOINT_FAMILIES = {
    "decision-desk",
    "decision-evidence",
    "decision-safety",
    "decision-desk-api",
    "decision-readiness-api",
    "decision-display",
    "decision-evidence-validation",
    "decision-human-review",
    "decision-boundary",
    "retail-dashboard",
    "retail-dashboard-api",
    "retail-dashboard-display",
}

EXPECTED_MODULE_FAMILIES = {
    "decision_desk",
    "decision_evidence",
    "decision_safety",
    "decision_api",
    "decision_readiness_api",
    "decision_display",
    "decision_evidence_validation",
    "decision_human_review",
    "decision_boundary",
    "retail_dashboard",
    "retail_dashboard_api",
    "retail_dashboard_display",
}


def test_boundary_integration_registry_covers_all_dangerous_behaviors() -> None:
    registry = default_decision_forbidden_behavior_registry()
    kinds = {behavior.kind for behavior in registry.behaviors}

    for kind in [
        DecisionForbiddenBehaviorKind.RECOMMENDATION,
        DecisionForbiddenBehaviorKind.ACTION_GENERATION,
        DecisionForbiddenBehaviorKind.CONFIDENCE_SCORING,
        DecisionForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
        DecisionForbiddenBehaviorKind.EXECUTION,
        DecisionForbiddenBehaviorKind.APPROVAL,
        DecisionForbiddenBehaviorKind.OVERRIDE,
        DecisionForbiddenBehaviorKind.ACTIVE_UI,
        DecisionForbiddenBehaviorKind.ACTIVE_WORKFLOW,
        DecisionForbiddenBehaviorKind.READINESS_TO_TRADE,
    ]:
        assert kind in kinds


def test_boundary_integration_endpoint_and_module_policies_cover_expected_families() -> None:
    endpoint_families = {policy.endpoint_family for policy in default_decision_endpoint_boundary_policies()}
    module_families = {policy.module_family for policy in default_decision_module_boundary_policies()}

    assert EXPECTED_ENDPOINT_FAMILIES.issubset(endpoint_families)
    assert EXPECTED_MODULE_FAMILIES.issubset(module_families)


def test_boundary_integration_invariants_pass_by_default() -> None:
    result = evaluate_decision_boundary_invariants()

    assert result.passed is True
    assert result.blockers == []
    assert result.recommendations_allowed is False
    assert result.action_generation_allowed is False
    assert result.confidence_scoring_allowed is False
    assert result.decision_object_generation_allowed is False
    assert result.execution_allowed is False
    assert result.approval_allowed is False
    assert result.override_allowed is False
    assert result.active_ui_allowed is False
    assert result.active_workflow_allowed is False
    assert result.readiness_to_trade_allowed is False


def test_boundary_integration_docs_and_scripts_reference_prompt_48() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs/DECISION_BOUNDARY_INTEGRATION_AUDIT.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DECISION_DESK_SYSTEM_BOUNDARY_HARDENING.md").read_text(encoding="utf-8"),
        ]
    )
    audit_script = (ROOT / "scripts/audit_foundation.py").read_text(encoding="utf-8")
    verify_script = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")

    assert "Prompt 48" in docs
    assert "DECISION_BOUNDARY_INTEGRATION_AUDIT.md" in audit_script
    assert "DECISION_BOUNDARY_INTEGRATION_AUDIT.md" in verify_script
