from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_retail_trader_experience_modules_do_not_generate_suitability_profiles() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary",
        ]
        for path in root.glob("*.py")
    )
    for forbidden in [
        "def build_suitability_profile",
        "def generate_suitability_profile",
        "def build_trading_permission_profile",
        "def generate_trading_permission_profile",
        "def persona_to_suitability_profile",
        "def journey_to_trading_advice",
        "def generate_suitability_based_recommendation",
    ]:
        assert forbidden not in source


def test_integration_docs_explicitly_forbid_suitability() -> None:
    text = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_SUITABILITY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No suitability profiling",
        "No trading permission profiling",
        "No persona-to-suitability-profile path",
        "No journey-to-trading-advice path",
        "No suitability-based recommendation behavior",
        "No API/display/boundary bypass path",
    ]:
        assert phrase in text

