from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_prompt_11_audit_docs_exist() -> None:
    expected = [
        "docs/MILESTONE_A_B_AUDIT.md",
        "docs/REPO_INVENTORY.md",
        "docs/API_SURFACE_INVENTORY.md",
        "docs/SAFETY_AUDIT.md",
        "docs/NEXT_PHASE_PLAN.md",
    ]

    for relative_path in expected:
        assert (ROOT / relative_path).exists()


def test_audit_docs_capture_required_boundaries() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/MILESTONE_A_B_AUDIT.md",
            "docs/API_SURFACE_INVENTORY.md",
            "docs/SAFETY_AUDIT.md",
            "docs/NEXT_PHASE_PLAN.md",
        ]
    )

    assert "Prompts 00-10 audited" in text
    assert "no execution APIs" in text
    assert "no real market ingestion" in text
    assert "Kafka/Redpanda" in text
    assert "Mac mini M2" in text
    assert "Windows-native" in text


def test_prompt_12_status_docs_are_current() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Current Prompt: 16" in north_star
    assert "Completed Prompts: 16 before this prompt, 17 after completion" in north_star
    assert "Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines" in north_star
    assert "Data Quality Status: Validation framework/contracts only, no production ingestion pipeline" in north_star
    assert "Prompt 11 - Milestone A/B Infrastructure Audit and Consolidation" in prompt_log
    assert "scripts/audit_foundation.py" in project_map
