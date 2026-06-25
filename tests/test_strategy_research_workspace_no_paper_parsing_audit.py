from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]
ROUTES = list((ROOT / "apps/api/stark_terminal_api/routes").glob("strategy_research_workspace*.py"))


def _combined_code() -> str:
    return "\n".join(
        [path.read_text(encoding="utf-8") for package in PACKAGES for path in package.glob("*.py")]
        + [route.read_text(encoding="utf-8") for route in ROUTES]
    )


def test_strategy_research_workspace_has_no_paper_ingestion_or_parsing_functions() -> None:
    combined = _combined_code()

    for forbidden in [
        "def ingest_paper",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def extract_method",
        "def extract_strategy",
        "def generate_code_from_paper",
        "def generate_backtest_from_paper",
    ]:
        assert forbidden not in combined


def test_strategy_research_workspace_api_has_no_paper_processing_routes() -> None:
    combined = "\n".join(route.read_text(encoding="utf-8") for route in ROUTES)

    for forbidden_path in [
        "paper-upload",
        "paper-ingestion",
        "paper-parsing",
        "parse-paper",
        "parse-pdf",
        "arxiv",
        "method-extraction",
        "strategy-extraction",
    ]:
        assert forbidden_path not in combined


def test_strategy_research_workspace_no_paper_parsing_docs_and_api_forbid_processing() -> None:
    docs = [
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NO_PAPER_PARSING_AUDIT.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_PAPER_PARSING_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_PAPER_PARSING_POLICY.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs).lower()

    for phrase in [
        "no paper ingestion",
        "no paper parsing",
        "no pdf parsing",
        "no arxiv ingestion",
        "no method extraction",
        "no strategy extraction",
        "no code generation from paper",
        "no backtest generation from paper",
    ]:
        assert phrase in combined
