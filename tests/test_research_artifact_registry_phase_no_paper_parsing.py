from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
]


def test_phase_has_no_paper_parsing_or_extraction_functions() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in SOURCE_ROOTS
        for path in root.glob("*.py")
    )
    for phrase in [
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def paper_to_code",
        "def paper_to_backtest",
    ]:
        assert phrase not in source


def test_phase_no_paper_parsing_doc_states_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_PAPER_PARSING_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no paper ingestion",
        "no paper parsing",
        "no pdf parsing",
        "no arxiv ingestion",
        "no llm paper analysis",
        "no method extraction",
        "no strategy extraction",
        "no paper-to-code path",
        "no paper-to-backtest path",
    ]:
        assert phrase in text
