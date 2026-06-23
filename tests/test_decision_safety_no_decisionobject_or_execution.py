from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_safety_modules_do_not_generate_outputs_or_approvals() -> None:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_safety"
    route_path = ROOT / "apps/api/stark_terminal_api/routes/decision_safety.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py"))
    text += "\n" + route_path.read_text(encoding="utf-8")

    forbidden = [
        "def approve_decision",
        "def generate_decision_object",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def compute_confidence",
        "DecisionObject(",
        "@router.post",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_decision_safety_routes_and_docs_forbid_execution() -> None:
    route_text = (ROOT / "apps/api/stark_terminal_api/routes/decision_safety.py").read_text(encoding="utf-8")
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("DECISION_SAFETY*.md"))
    docs_text += "\n" + (ROOT / "docs/DECISION_HUMAN_REVIEW_GATES.md").read_text(encoding="utf-8")
    docs_text += "\n" + (ROOT / "docs/DECISION_APPROVAL_PLACEHOLDERS.md").read_text(encoding="utf-8")

    assert "/decision-safety" in route_text
    assert "recommendations_allowed_now" in route_text
    assert "decision_object_generation_allowed_now" in route_text
    assert "execution_allowed_now" in route_text
    assert "approval_granted" in route_text
    assert "no approvals" in docs_text
    assert "no DecisionObject generation" in docs_text
    assert "no recommendations" in docs_text
    assert "no execution APIs" in docs_text
    assert "buy/sell/hold/watch/avoid" not in route_text.lower()
