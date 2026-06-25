from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_no_suitability_profile_generators_exist() -> None:
    forbidden = [
        "def build_suitability_profile",
        "def generate_suitability_profile",
        "def create_trading_permission_profile",
        "persona_to_suitability_profile(",
        "journey_to_trading_advice(",
        "suitability_based_recommendation(",
    ]
    for root in [
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary",
    ]:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                assert phrase not in text, f"{path}: {phrase}"


def test_boundary_endpoints_explicitly_keep_suitability_false() -> None:
    for path in [
        "/retail-trader-experience-boundary/health",
        "/retail-trader-experience-boundary/contracts",
        "/retail-trader-experience-boundary/invariants",
    ]:
        payload = client.get(path).json()
        serialized = str(payload).lower()
        assert "'suitability_profiling_allowed': true" not in serialized
        assert "'suitability_profile_generated': true" not in serialized
        assert "'generates_suitability_profile': true" not in serialized


def test_docs_explicitly_forbid_suitability_profiling() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_SYSTEM_BOUNDARY_HARDENING.md",
            "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_SUITABILITY_PROFILING_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
        ]
    )
    assert "no suitability profiling" in text
    assert "no persona-to-suitability-profile path" in text
    assert "no journey-to-trading-advice path" in text
