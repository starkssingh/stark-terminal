from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = ROOT / "packages/core/stark_terminal_core"
MODULES = [
    "decision_api",
    "decision_readiness_api",
    "decision_display",
    "decision_boundary",
    "decision_evidence_validation",
    "decision_human_review",
]


def _decision_integration_files() -> list[Path]:
    files: list[Path] = []
    for module in MODULES:
        files.extend((CORE_ROOT / module).glob("*.py"))
    return files


def test_decision_integration_modules_do_not_generate_recommendations_or_decisions() -> None:
    forbidden = [
        "def generate_recommendation",
        "def generate_action_state",
        "def generate_action",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "decisionobject(",
    ]
    bad: list[str] = []
    for path in _decision_integration_files():
        text = path.read_text(encoding="utf-8").lower()
        for snippet in forbidden:
            if snippet in text:
                bad.append(f"{path.relative_to(ROOT)}:{snippet}")

    assert bad == []


def test_decision_integration_modules_do_not_set_generated_flags_true() -> None:
    forbidden = [
        "recommendation_generated: bool = true",
        "action_generated: bool = true",
        "confidence_generated: bool = true",
        "decision_object_generated: bool = true",
        "readiness_to_trade_generated: bool = true",
        "approval_granted: bool = true",
        "override_granted: bool = true",
        "execution_ready: bool = true",
    ]
    bad: list[str] = []
    for path in _decision_integration_files():
        text = path.read_text(encoding="utf-8").lower()
        for snippet in forbidden:
            if snippet in text:
                bad.append(f"{path.relative_to(ROOT)}:{snippet}")

    assert bad == []


def test_decision_integration_docs_explicitly_forbid_recommendations() -> None:
    text = (ROOT / "docs/DECISION_INTEGRATION_NO_RECOMMENDATION_AUDIT.md").read_text(encoding="utf-8")

    for phrase in [
        "no buy/sell/hold/watch/avoid active output",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no readiness-to-trade",
        "no execution APIs",
        "No hidden thresholds",
    ]:
        assert phrase in text

