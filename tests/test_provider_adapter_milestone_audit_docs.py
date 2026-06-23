from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_provider_adapter_milestone_audit_docs_exist() -> None:
    docs = [
        "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
        "docs/PROVIDER_BOUNDARY_AUDIT.md",
        "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
        "docs/PROVIDER_NEXT_PHASE_PLAN.md",
    ]

    for path in docs:
        assert (ROOT / path).exists()


def test_provider_adapter_milestone_docs_state_required_boundaries() -> None:
    text = "\n".join(
        _read(path)
        for path in [
            "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
            "docs/PROVIDER_BOUNDARY_AUDIT.md",
            "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
            "docs/PROVIDER_NEXT_PHASE_PLAN.md",
        ]
    )

    for phrase in [
        "Prompts 20-24",
        "provider guardrails",
        "Real Provider Readiness",
        "Local Sample Provider",
        "Local File Provider",
        "no real ingestion",
        "no external calls",
        "no scraping",
        "no credentials",
        "no provider SDKs",
        "no execution APIs",
        "no analytics/signals/decisions",
        "no arbitrary file read API",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_provider_next_phase_plan_recommends_prompt_26() -> None:
    text = _read("docs/PROVIDER_NEXT_PHASE_PLAN.md")

    assert "Prompt 28 - Returns and Rolling Window Analytics v0" in text
    assert "Prompt 28 - Returns and Rolling Window Analytics v0" in text
    assert "Prompt 34 - Regime Feature Preparation Contracts" in text
    assert "Real provider integration remains forbidden" in text
