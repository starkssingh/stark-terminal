from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _decision_code_text() -> str:
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_desk",
        ROOT / "packages/core/stark_terminal_core/decision_evidence",
        ROOT / "packages/core/stark_terminal_core/decision_safety",
        ROOT / "packages/core/stark_terminal_core/decision_api",
    ]
    route_files = [
        ROOT / "apps/api/stark_terminal_api/routes/decision_desk.py",
        ROOT / "apps/api/stark_terminal_api/routes/decision_evidence.py",
        ROOT / "apps/api/stark_terminal_api/routes/decision_safety.py",
        ROOT / "apps/api/stark_terminal_api/routes/decision_desk_api.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for root in roots for path in root.glob("*.py"))
    return text + "\n" + "\n".join(path.read_text(encoding="utf-8") for path in route_files)


def test_decision_modules_do_not_generate_recommendations_or_decisionobjects() -> None:
    text = _decision_code_text()

    for phrase in [
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "def approve_decision",
        "def override_decision",
        "DecisionObject(",
        "@router.post",
    ]:
        assert phrase not in text


def test_decision_docs_and_api_explicitly_forbid_recommendations() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("DECISION*.md"))
    route_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "apps/api/stark_terminal_api/routes").glob("decision*.py")
    )

    assert "no recommendations" in docs_text
    assert "no confidence scoring" in docs_text
    assert "no active DecisionObject generation" in docs_text
    assert "no approvals" in docs_text
    assert "no overrides" in docs_text
    assert "no execution APIs" in docs_text
    assert "recommendation endpoint" not in route_text.lower()
    assert "confidence endpoint" not in route_text.lower()

