from pathlib import Path

from stark_terminal_core.research_artifact_index_boundary.invariants import (
    evaluate_research_artifact_index_boundary_invariants,
)


ROOT = Path(__file__).resolve().parents[2]

PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_index",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_boundary",
]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_boundary.py",
]


def test_index_packages_remain_skeleton_contract_boundary_only() -> None:
    readme_expectations = {
        "research_artifact_index": "planning",
        "research_artifact_index_api": "API contract skeleton",
        "research_artifact_index_display": "Display",
        "research_artifact_index_boundary": "boundary",
    }
    for package, phrase in readme_expectations.items():
        text = (ROOT / f"packages/core/stark_terminal_core/{package}/README.md").read_text(
            encoding="utf-8"
        )
        assert phrase in text
        assert "execution" in text.lower()


def test_index_api_display_integration_does_not_add_active_capabilities() -> None:
    forbidden = [
        "def render_index_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
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
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
        "def place_order",
        "def approve_trade",
        "def override_trade",
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
    ]
    bad: list[str] = []

    for root in PACKAGE_ROOTS:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    for path in ROUTE_FILES:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []


def test_boundary_invariants_pass_and_graph_readiness_is_planning_only() -> None:
    result = evaluate_research_artifact_index_boundary_invariants()
    assert result.passed
    assert result.execution_allowed is False
    assert result.recommendations_allowed is False

    plan = (ROOT / "docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md").read_text(encoding="utf-8")
    plan_lower = plan.lower()
    assert "planning and guardrails only" in plan_lower
    assert "graph implementation is not yet allowed" in plan_lower
    assert "no active graph database" in plan_lower
    assert "no persistent graph writes" in plan_lower
    assert "no graph traversal engine" in plan_lower
    assert "no graph search" in plan_lower
    assert "no graph ranking" in plan_lower
    assert "no graph retrieval" in plan_lower
    assert "no embeddings" in plan_lower
    assert "no vector store" in plan_lower
    assert "no execution apis" in plan_lower
