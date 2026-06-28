from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_index_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py"


def test_research_artifact_index_display_adds_no_indexing_search_ranking_embedding_functions() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))
    source += "\n" + DISPLAY_ROUTE.read_text(encoding="utf-8")

    for forbidden in [
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def rank_artifacts",
        "def retrieve_artifacts",
        "def embed_artifacts",
        "def create_vector_store",
        "def semantic_search",
        "def keyword_search",
    ]:
        assert forbidden not in source


def test_research_artifact_index_display_adds_no_indexing_search_vector_routes() -> None:
    route_source = DISPLAY_ROUTE.read_text(encoding="utf-8")

    assert "@router.post" not in route_source
    for forbidden in ["indexing", "search", "rank", "retrieve", "embed", "vector"]:
        assert f'@router.get("/research-artifact-index-display/{forbidden}' not in route_source


def test_research_artifact_index_display_adds_no_vector_search_or_ui_dependencies() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()

    for forbidden in [
        "faiss",
        "chromadb",
        "qdrant",
        "weaviate",
        "pinecone",
        "elasticsearch",
        "opensearch",
        "sentence-transformers",
        "transformers",
        "llama-index",
        "langchain",
        "react",
        "plotly",
        "bokeh",
        "dash",
    ]:
        assert forbidden not in pyproject
