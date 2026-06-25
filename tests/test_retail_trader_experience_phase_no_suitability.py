from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
]


def test_no_suitability_profile_generator_functions_exist() -> None:
    forbidden_function_names = [
        "build_suitability_profile",
        "generate_suitability_profile",
        "create_suitability_profile",
        "generate_trading_permission_profile",
    ]
    for root in PACKAGE_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for name in forbidden_function_names:
                assert f"def {name}" not in text


def test_no_persona_or_journey_path_creates_suitability_or_advice() -> None:
    persona_text = (
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience/personas.py"
    ).read_text(encoding="utf-8")
    journey_text = (
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience/journeys.py"
    ).read_text(encoding="utf-8")

    assert "suitability_profile: bool = False" in persona_text
    assert "trading_permission_profile: bool = False" in persona_text
    assert "trading_advice_journey: bool = False" in journey_text
    assert "recommendation_journey: bool = False" in journey_text


def test_no_suitability_docs_remain_explicit() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_SUITABILITY_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_API_NO_SUITABILITY_PROFILING_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_SUITABILITY_PROFILING_POLICY.md",
        ]
    )
    for phrase in [
        "no suitability profiling",
        "no trading permission profile",
        "no persona-as-suitability-profile",
        "no journey-as-trading-advice",
        "no suitability-based recommendation",
        "no retail trader categorization for actions",
    ]:
        assert phrase in text
