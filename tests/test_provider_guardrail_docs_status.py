from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_provider_guardrail_docs_exist_and_state_boundaries() -> None:
    docs = [
        "docs/PROVIDER_ADAPTER_IMPLEMENTATION_PLAN.md",
        "docs/PROVIDER_GUARDRAIL_POLICY.md",
        "docs/PROVIDER_APPROVAL_WORKFLOW.md",
        "docs/PROVIDER_COMPLIANCE_CHECKLIST.md",
    ]
    required_phrases = [
        "Provider Adapter",
        "Guardrail",
        "approval workflow",
        "compliance checklist",
        "no scraping",
        "no external calls",
        "no real market ingestion",
        "no credentials",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]

    combined = ""
    for doc in docs:
        path = ROOT / doc
        assert path.exists()
        combined += "\n" + path.read_text(encoding="utf-8")
    for phrase in required_phrases:
        assert phrase in combined


def test_provider_guardrail_status_docs_are_current() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 20 - Data Provider Adapter Implementation Plan and Guardrails" in prompt_log
    assert "Current Prompt: 36" in north_star
    assert "Provider Status: Guardrails, readiness/candidate selection, local sample provider, and local file provider implemented and audited; no real provider implementation; no external calls" in north_star
    assert "Provider Adapter Guardrails" in project_map
    assert "provider_guardrails.py" in project_map
