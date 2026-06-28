from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_research_artifact_registry_phase_doc_consolidates_prompts_70_to_76() -> None:
    text = (ROOT / "docs/phases/research_artifact_registry.md").read_text(encoding="utf-8")

    for prompt in range(70, 77):
        assert f"Prompt {prompt}" in text

    required = [
        "planning and guardrails",
        "API contract skeleton",
        "display contract skeleton",
        "safety boundary audit",
        "milestone audit",
        "system boundary hardening",
        "API/display integration readiness audit",
    ]

    for phrase in required:
        assert phrase in text


def test_research_artifact_registry_phase_preserves_forbidden_boundaries() -> None:
    text = (ROOT / "docs/phases/research_artifact_registry.md").read_text(encoding="utf-8").lower()

    required = [
        "no active artifact registry implementation",
        "no active ingestion",
        "no file upload",
        "no active ui",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution apis",
    ]

    for phrase in required:
        assert phrase in text
