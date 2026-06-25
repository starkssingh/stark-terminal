from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    "docs/RETAIL_TRADER_EXPERIENCE_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MODULE_BOUNDARY_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CROSS_MODULE_INVARIANTS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_SUITABILITY_PROFILING_POLICY.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_trader_experience_boundary_docs_exist() -> None:
    for path in DOCS:
        assert (ROOT / path).exists(), path


def test_retail_trader_experience_boundary_docs_state_forbidden_behavior() -> None:
    combined = "\n".join(_read(path) for path in DOCS).lower()
    for phrase in [
        "retail trader experience system boundary hardening",
        "forbidden behavior registry",
        "endpoint boundary policy",
        "module boundary policy",
        "cross-module invariants",
        "no active ui",
        "no frontend components",
        "no desktop components",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no decisionobject generation",
        "no readiness-to-trade",
        "no suitability profiling",
        "no broker controls",
        "no execution apis",
        "mac mini m2",
        "windows-native",
    ]:
        assert phrase in combined


def test_retail_trader_experience_boundary_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    project_map = _read("PROJECT_MAP.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Current Prompt: 61" in north_star
    assert "Completed Prompts: 62 after completion" in north_star
    assert "Retail Trader Experience System Boundary Hardening" in project_map
    assert "Prompt 61 - Retail Trader Experience System Boundary Hardening" in prompt_log
    assert "Prompt 62 - Retail Trader Experience API/Display Integration Readiness Audit" in prompt_log
