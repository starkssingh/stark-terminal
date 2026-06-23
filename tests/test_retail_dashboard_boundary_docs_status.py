from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DOCS = [
    "docs/RETAIL_DASHBOARD_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RETAIL_DASHBOARD_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RETAIL_DASHBOARD_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RETAIL_DASHBOARD_MODULE_BOUNDARY_POLICY.md",
    "docs/RETAIL_DASHBOARD_CROSS_MODULE_INVARIANTS.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_NO_EXECUTION_POLICY.md",
]


def test_retail_dashboard_boundary_docs_exist() -> None:
    for doc in DOCS:
        assert (ROOT / doc).exists()


def test_retail_dashboard_boundary_docs_contain_required_safety_language() -> None:
    text = "\n".join((ROOT / doc).read_text(encoding="utf-8") for doc in DOCS)
    for phrase in [
        "Retail Dashboard System Boundary Hardening",
        "forbidden behavior registry",
        "endpoint boundary policy",
        "module boundary policy",
        "cross-module invariants",
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_retail_dashboard_boundary_status_docs_are_updated() -> None:
    assert "Prompt 54" in (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    assert "Current Prompt: 54" in (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    assert "Retail Dashboard System Boundary Hardening" in (ROOT / "PROJECT_MAP.md").read_text(
        encoding="utf-8"
    )
