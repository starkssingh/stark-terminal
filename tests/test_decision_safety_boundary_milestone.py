from __future__ import annotations

from pathlib import Path

from stark_terminal_core.decision_safety.approval import default_decision_approval_placeholders
from stark_terminal_core.decision_safety.blocked_outputs import default_decision_blocked_output_policy
from stark_terminal_core.decision_safety.guardrails import DecisionBlockedOutputKind, build_decision_safety_guardrail_set
from stark_terminal_core.decision_safety.human_review import build_decision_human_review_gate_set
from stark_terminal_core.decision_safety.overrides import default_decision_override_prohibitions


ROOT = Path(__file__).resolve().parents[1]


def test_decision_safety_package_remains_guardrails_only() -> None:
    guardrails = build_decision_safety_guardrail_set()
    gates = build_decision_human_review_gate_set()
    approvals = default_decision_approval_placeholders()
    overrides = default_decision_override_prohibitions()
    policy = default_decision_blocked_output_policy()

    assert guardrails.recommendations_allowed is False
    assert guardrails.action_generation_allowed is False
    assert guardrails.confidence_scoring_allowed is False
    assert guardrails.decision_object_generation_allowed is False
    assert guardrails.execution_allowed is False
    assert gates.approval_granted is False
    assert gates.recommendations_allowed is False
    assert gates.decision_object_generation_allowed is False
    assert all(not approval.approval_granted for approval in approvals)
    assert all(not approval.active_workflow for approval in approvals)
    assert all(not override.overrides_allowed for override in overrides)
    assert DecisionBlockedOutputKind.RECOMMENDATION in policy.blocked_outputs
    assert DecisionBlockedOutputKind.ACTION_GENERATION in policy.blocked_outputs
    assert DecisionBlockedOutputKind.CONFIDENCE_SCORE in policy.blocked_outputs
    assert DecisionBlockedOutputKind.DECISION_OBJECT in policy.blocked_outputs
    assert DecisionBlockedOutputKind.EXECUTION in policy.blocked_outputs
    assert DecisionBlockedOutputKind.BROKER_ORDER in policy.blocked_outputs
    assert DecisionBlockedOutputKind.MARKET_STATE_DECISION in policy.blocked_outputs


def test_decision_safety_code_has_no_active_approval_or_override_workflow() -> None:
    package_root = ROOT / "packages/core/stark_terminal_core/decision_safety"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_safety.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))
    text += route.read_text(encoding="utf-8")

    for phrase in [
        "def approve_decision",
        "def override_decision",
        "def generate_decision_object",
        "def generate_recommendation",
        "def score_confidence",
        "DecisionObject(",
        "@router.post",
    ]:
        assert phrase not in text

