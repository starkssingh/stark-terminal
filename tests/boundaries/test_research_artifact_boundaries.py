from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
    ROOT / "apps/api/stark_terminal_api/routes",
]

ARTIFACT_ROUTE_FILES = {
    "research_artifact_registry.py",
    "research_artifact_registry_api.py",
    "research_artifact_registry_display.py",
    "research_artifact_registry_boundary.py",
    "research_artifact_index.py",
    "research_artifact_index_api.py",
    "research_artifact_index_display.py",
}


def test_consolidated_research_artifact_boundary_doc_covers_registry_and_index() -> None:
    text = (ROOT / "docs/audits/research_artifact_boundaries.md").read_text(encoding="utf-8").lower()

    required = [
        "research artifact registry",
        "research artifact index",
        "no active registry implementation",
        "no active index implementation",
        "no indexing engine",
        "no search engine",
        "no ranking engine",
        "no retrieval engine",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no file upload",
        "no file upload, download, or preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution apis",
    ]

    for phrase in required:
        assert phrase in text


def test_research_artifact_sources_do_not_add_active_capability_functions() -> None:
    forbidden = [
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def semantic_search",
        "def keyword_search",
        "def rank_artifacts",
        "def score_artifacts",
        "def retrieve_artifacts",
        "def lookup_artifact",
        "def lookup_index",
        "def lookup_registry",
        "def fetch_index_reference",
        "def embed_artifacts",
        "def create_embeddings",
        "def create_vector_store",
        "def vector_search",
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def generate_strategy",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def execute_trade",
    ]
    forbidden_routes = [
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
    ]

    bad: list[str] = []
    for root in ARTIFACT_SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in ARTIFACT_ROUTE_FILES:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
            for phrase in forbidden_routes:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []
