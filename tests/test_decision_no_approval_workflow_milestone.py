from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_no_decision_endpoint_grants_approval_or_override() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith(("/decision-", "/decision_")):
            continue
        response = client.get(path)
        if response.status_code != 200:
            continue
        text = str(response.json()).lower()
        assert "approval_granted': true" not in text
        assert "override_granted': true" not in text
        assert "approval_allowed': true" not in text
        assert "override_allowed': true" not in text
        assert "execution_allowed': true" not in text


def test_no_decision_module_grants_approval_or_override() -> None:
    decision_root = ROOT / "packages/core/stark_terminal_core"
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for directory in [
            decision_root / "decision_readiness_api",
            decision_root / "decision_display",
            decision_root / "decision_evidence_validation",
            decision_root / "decision_human_review",
        ]
        for path in directory.glob("*.py")
    )

    for phrase in [
        "def approve_decision",
        "def override_decision",
        "approval_granted: bool = True",
        "override_granted: bool = True",
        "approval_allowed: bool = True",
        "override_allowed: bool = True",
        "execution_allowed: bool = True",
    ]:
        assert phrase not in text


def test_docs_confirm_no_approval_workflow() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/DECISION_NO_APPROVAL_WORKFLOW_AUDIT.md",
            "docs/DECISION_REVIEW_NO_APPROVAL_POLICY.md",
            "docs/DECISION_EVIDENCE_VALIDATION_BOUNDARY_AUDIT.md",
            "docs/DECISION_DISPLAY_BOUNDARY_AUDIT.md",
        ]
    )

    for phrase in [
        "no active approval workflow",
        "no active override workflow",
        "no endpoint grants approval",
        "no endpoint grants override",
        "validation pass grants approval",
        "display badge grants approval",
    ]:
        assert phrase in text
