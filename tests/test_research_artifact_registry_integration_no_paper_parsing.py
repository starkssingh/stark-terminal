from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_paper_parsing_docs_state_integration_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_PAPER_PARSING_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no paper ingestion",
        "no pdf parsing",
        "no arxiv ingestion",
        "no llm paper analysis",
        "no method extraction",
        "no strategy extraction",
        "no paper-to-code",
        "no paper-to-backtest",
    ]:
        assert phrase in text


def test_no_paper_parsing_functions_exist() -> None:
    forbidden_defs = [
        "parse_paper",
        "parse_pdf",
        "ingest_arxiv",
        "analyze_paper_with_llm",
        "extract_method",
        "extract_strategy",
        "paper_to_code",
        "paper_to_backtest",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)
    for root in [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
    ]:
        for path in root.rglob("*.py"):
            assert pattern.search(path.read_text(encoding="utf-8")) is None, str(path.relative_to(ROOT))

