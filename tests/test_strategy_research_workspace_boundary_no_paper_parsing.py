from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _strategy_research_code() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "packages/core/stark_terminal_core").rglob("*.py")
        if "strategy_research_workspace" in path.as_posix()
    )


def test_strategy_research_workspace_boundary_has_no_paper_ingestion_or_parsing_functions() -> None:
    code = _strategy_research_code()

    forbidden_function_names = [
        "def ingest_paper",
        "def parse_paper",
        "def ingest_arxiv",
        "def extract_method",
        "def extract_strategy",
        "def generate_code_from_paper",
        "def generate_backtest_from_paper",
    ]
    for name in forbidden_function_names:
        assert name not in code


def test_strategy_research_workspace_boundary_docs_and_api_forbid_paper_parsing() -> None:
    docs = (ROOT / "docs/STRATEGY_RESEARCH_BOUNDARY_NO_PAPER_PARSING_POLICY.md").read_text(
        encoding="utf-8"
    )
    route = (ROOT / "apps/api/stark_terminal_api/routes/strategy_research_workspace_boundary.py").read_text(
        encoding="utf-8"
    )

    assert "does not add paper ingestion" in docs
    assert "does not add paper parsing" in docs
    assert '"no_paper_parsing": True' in route
    assert '"paper_parsed": False' in route
