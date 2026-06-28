from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_research_artifact_index_phase_doc_consolidates_prompts_77_to_80() -> None:
    text = read_doc("docs/phases/research_artifact_index.md")

    required = [
        "Prompt 77",
        "Prompt 78",
        "Prompt 79",
        "Prompt 80",
        "Research Artifact Index Planning and Guardrails",
        "Research Artifact Index API Contract Skeleton",
        "Research Artifact Index Display Contract Skeleton",
        "Research Artifact Index Safety Boundary Audit",
        "Prompt 81",
    ]

    for phrase in required:
        assert phrase in text


def test_research_artifact_index_phase_preserves_core_boundaries() -> None:
    text = read_doc("docs/phases/research_artifact_index.md").lower()

    required = [
        "no indexing engine",
        "no search engine",
        "no ranking engine",
        "no retrieval engine",
        "no embeddings",
        "no active ingestion",
        "no file upload",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution apis",
    ]

    for phrase in required:
        assert phrase in text
