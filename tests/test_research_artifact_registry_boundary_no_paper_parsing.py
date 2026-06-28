from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py"


def test_boundary_has_no_paper_pdf_arxiv_or_llm_parsing_functions() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
    for phrase in [
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
    ]:
        assert phrase not in text


def test_boundary_has_no_parse_routes() -> None:
    route_text = ROUTE_PATH.read_text(encoding="utf-8").lower()
    for phrase in ["/parse", "/paper", "/pdf", "/arxiv", "@router.post"]:
        assert phrase not in route_text


def test_boundary_docs_state_no_paper_parsing_policy() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_PAPER_PARSING_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no paper parsing",
        "no pdf/arxiv ingestion",
        "no llm paper analysis",
        "no method extraction",
        "no strategy extraction",
        "future prompt and audit required",
    ]:
        assert phrase in text

