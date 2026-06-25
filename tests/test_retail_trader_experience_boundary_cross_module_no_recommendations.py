from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary",
]


def test_retail_trader_experience_modules_do_not_generate_recommendations() -> None:
    forbidden = [
        "def generate_trader_recommendation",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "DecisionObject(",
    ]
    for root in MODULE_ROOTS:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in forbidden:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                assert needle not in haystack, f"{path}: {phrase}"


def test_retail_trader_experience_boundary_docs_forbid_recommendations() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_SYSTEM_BOUNDARY_HARDENING.md",
            "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIOR_REGISTRY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_CROSS_MODULE_INVARIANTS.md",
        ]
    )
    assert "no recommendations" in text
    assert "no action generation" in text
    assert "no confidence scoring" in text
    assert "no decisionobject generation" in text
