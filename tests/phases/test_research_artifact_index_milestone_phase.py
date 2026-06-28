from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_DOCS = [
    "docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NEXT_PHASE_PLAN.md",
    "docs/phases/research_artifact_index.md",
    "docs/audits/research_artifact_boundaries.md",
    "docs/testing/TEST_POLICY.md",
    "docs/testing/CONSOLIDATION_MAP.md",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_81_milestone_docs_exist() -> None:
    for path in REQUIRED_DOCS:
        assert (ROOT / path).exists(), path


def test_prompt_81_milestone_docs_cover_phase_and_safety_scope() -> None:
    combined = "\n".join(read(path) for path in REQUIRED_DOCS)

    required = [
        "Prompts 77-80",
        "consolidation interlude",
        "Research Artifact Index Planning and Guardrails",
        "Research Artifact Index API Contract Skeleton",
        "Research Artifact Index Display Contract Skeleton",
        "Research Artifact Index Safety Boundary Audit",
        "no active UI",
        "no frontend",
        "no desktop",
        "no indexing",
        "no search",
        "no ranking",
        "no retrieval",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no persistent storage",
        "no file upload",
        "download",
        "preview",
        "no paper parsing",
        "PDF parsing",
        "arXiv ingestion",
        "LLM paper analysis",
        "no strategy generation",
        "strategy code generation",
        "no backtesting",
        "optimization",
        "no recommendations",
        "action generation",
        "confidence scoring",
        "active DecisionObjects",
        "no broker controls",
        "readiness-to-trade",
        "execution APIs",
        "phase-level",
        "grouped",
    ]

    for phrase in required:
        assert phrase in combined
