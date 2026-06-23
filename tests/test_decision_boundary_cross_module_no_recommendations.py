from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_MODULE_ROOT = ROOT / "packages/core/stark_terminal_core"
DECISION_MODULE_DIRS = [
    "decision_desk",
    "decision_evidence",
    "decision_safety",
    "decision_api",
    "decision_readiness_api",
    "decision_display",
    "decision_evidence_validation",
    "decision_human_review",
    "decision_boundary",
]

FORBIDDEN_ACTIVE_FUNCTIONS = [
    "def generate_decision_object",
    "def generate_recommendation",
    "def score_confidence",
    "def generate_action_state",
    "def generate_readiness_status",
    "def approve_decision",
    "def override_decision",
]


def _decision_python_files() -> list[Path]:
    files: list[Path] = []
    for directory in DECISION_MODULE_DIRS:
        files.extend((DECISION_MODULE_ROOT / directory).glob("*.py"))
    return files


def test_decision_modules_do_not_generate_recommendations_or_decision_objects() -> None:
    bad: list[str] = []
    for path in _decision_python_files():
        text = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_ACTIVE_FUNCTIONS:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
        if "decisionobject(" in text:
            bad.append(f"{path.relative_to(ROOT)}:DecisionObject(")

    assert bad == []


def test_decision_modules_do_not_set_generated_dangerous_flags_true() -> None:
    bad: list[str] = []
    for path in _decision_python_files():
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "recommendation_generated: bool = true",
            "action_generated: bool = true",
            "confidence_generated: bool = true",
            "decision_object_generated: bool = true",
            "readiness_to_trade_generated: bool = true",
            "approval_granted: bool = true",
            "override_granted: bool = true",
            "execution_ready: bool = true",
        ]:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []
