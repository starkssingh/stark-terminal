from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]


def _combined_code() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for package in PACKAGES
        for path in package.glob("*.py")
    ).lower()


def test_strategy_research_workspace_phase_has_no_paper_parsing_functions() -> None:
    code = _combined_code()

    for forbidden in [
        "def ingest_paper",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def extract_method",
        "def extract_strategy",
        "paper_to_code",
        "paper_to_backtest",
    ]:
        assert forbidden not in code


def test_strategy_research_workspace_phase_no_paper_parsing_doc_is_explicit() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_PAPER_PARSING_AUDIT.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "No paper ingestion exists",
        "No PDF parsing exists",
        "No arXiv ingestion exists",
        "No method extraction exists",
        "Paper artifacts remain references and placeholders only",
    ]:
        assert phrase in text
