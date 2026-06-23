from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_core.decision_evidence.bundle import default_decision_object_evidence_bundle_contract
from stark_terminal_core.decision_evidence_validation.validators import validate_evidence_bundle_contract


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_decision_evidence_validation_remains_validation_only_and_read_only() -> None:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_evidence_validation"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_evidence_validation.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py"))
    text += "\n" + route.read_text(encoding="utf-8")

    for phrase in [
        "@router.post",
        "def generate_recommendation",
        "def approve_decision",
        "def generate_readiness_status",
        "def generate_decision_object",
        "DecisionObject(",
        "write_text(",
        "publish(",
        "emit(",
    ]:
        assert phrase not in text


def test_validation_pass_is_not_recommendation_approval_or_trade_readiness() -> None:
    sample = client.get("/decision-evidence-validation/sample").json()
    result = sample["validation_result"]

    assert sample["validation_only"] is True
    assert result["validation_only"] is True
    assert result["recommendations_allowed"] is False
    assert result["decision_object_generation_allowed"] is False
    assert result["approval_granted"] is False
    assert result["override_granted"] is False
    assert result["readiness_to_trade"] is False
    assert result["execution_allowed"] is False


def test_validators_do_not_mutate_inputs() -> None:
    bundle = default_decision_object_evidence_bundle_contract()
    before = deepcopy(bundle.model_dump(mode="json"))

    validate_evidence_bundle_contract(bundle)

    assert bundle.model_dump(mode="json") == before
