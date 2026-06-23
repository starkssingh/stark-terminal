from __future__ import annotations

from pathlib import Path
import re

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_no_classify_or_detect_regime_implementation_exists() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "packages/analytics/stark_terminal_analytics/regime").glob("*.py")
    )

    assert re.search(r"\bdef classify_regime\b", text) is None
    assert re.search(r"\bdef detect_regime\b", text) is None
    assert "computed_regime_label" not in text
    assert re.search(r"\bmarket_state_decision\s*:", text) is None
    assert "confidence_score" not in text
    assert "action_state" not in text


def test_regime_endpoints_do_not_classify_market_states() -> None:
    client = TestClient(app)

    for endpoint in [
        "/regime-analytics/health",
        "/regime-analytics/contracts",
        "/regime-analytics/readiness-template",
        "/regime-analytics/dependency-gate",
    ]:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body.get("classification_allowed", False) is False
        assert body.get("classification_allowed_now", False) is False
        assert body.get("no_classification", True) is True


def test_docs_and_api_forbid_regime_classification() -> None:
    combined_docs = "\n".join(
        _read(path)
        for path in [
            "docs/REGIME_NO_CLASSIFICATION_AUDIT.md",
            "docs/REGIME_BOUNDARY_AUDIT.md",
            "docs/REGIME_ANALYTICS_PLANNING.md",
            "docs/REGIME_ANALYTICS_SAFETY_POLICY.md",
        ]
    )

    for phrase in [
        "no regime classification",
        "no regime detection",
        "no stationarity tests",
        "no model fitting",
        "no computed labels",
        "no market-state decision",
    ]:
        assert phrase in combined_docs
