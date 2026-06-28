from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_index"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py"


def _source_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in [*PACKAGE_ROOT.glob("*.py"), ROUTE_PATH])


def test_no_indexing_search_ranking_retrieval_embedding_functions_exist() -> None:
    text = _source_text()
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
        assert forbidden not in text


def test_no_indexing_search_ranking_vector_embedding_routes_exist() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")
    for forbidden in ["indexing", "search", "ranking", "retrieval", "embedding", "vector"]:
        assert f"/research-artifact-index/{forbidden}" not in route_source
    assert "@router.post" not in route_source


def test_no_vector_store_or_embedding_dependencies_added() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    for dependency in ["faiss", "pinecone", "weaviate", "qdrant", "chromadb", "milvus", "sentence-transformers"]:
        assert dependency not in pyproject

