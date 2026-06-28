from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY_ROOT = ROOT / "packages/core/stark_terminal_core"


def test_no_paper_ingestion_or_parsing_functions_exist() -> None:
    forbidden = [
        "def ingest_paper",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def paper_to_code",
        "def paper_to_backtest",
    ]
    for package in [
        "strategy_research_workspace",
        "strategy_research_workspace_api",
        "strategy_research_workspace_display",
        "strategy_research_workspace_boundary",
    ]:
        for path in (STRATEGY_ROOT / package).rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                assert phrase not in text, f"{path}:{phrase}"


def test_no_paper_parsing_dependencies_added_to_strategy_research_modules() -> None:
    forbidden_imports = [
        "import fitz",
        "import pypdf",
        "import pdfplumber",
        "import arxiv",
        "import openai",
        "import langchain",
    ]
    for package in [
        "strategy_research_workspace",
        "strategy_research_workspace_api",
        "strategy_research_workspace_display",
        "strategy_research_workspace_boundary",
    ]:
        for path in (STRATEGY_ROOT / package).rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden_imports:
                assert phrase not in text, f"{path}:{phrase}"


def test_no_paper_parsing_integration_doc_is_explicit() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_PAPER_PARSING_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No paper ingestion exists",
        "No PDF parsing exists",
        "No arXiv ingestion exists",
        "No LLM paper analysis exists",
        "No method extraction exists",
        "No strategy extraction exists",
        "No paper-to-code path exists",
        "No paper-to-backtest path exists",
    ]:
        assert phrase in text
