from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_index",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
]


def test_research_artifact_index_packages_remain_contract_skeleton_layers() -> None:
    package_readmes = {
        "research_artifact_index": "planning",
        "research_artifact_index_api": "API contract skeleton",
        "research_artifact_index_display": "Display",
    }

    for package, phrase in package_readmes.items():
        text = (ROOT / f"packages/core/stark_terminal_core/{package}/README.md").read_text(
            encoding="utf-8"
        )
        assert phrase in text
        assert "execution APIs" in text


def test_research_artifact_index_routes_remain_get_only() -> None:
    forbidden = ["@router.post", "@router.put", "@router.patch", "@router.delete"]
    bad: list[str] = []

    for path in ROUTE_FILES:
        text = path.read_text(encoding="utf-8")
        assert "@router.get" in text
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []


def test_research_artifact_index_sources_have_no_active_capability_functions() -> None:
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


def test_no_active_artifact_index_frontend_or_desktop_files_exist() -> None:
    suspicious_roots = [
        ROOT / "apps/frontend",
        ROOT / "apps/desktop/stark_terminal_desktop/research_artifact_index",
        ROOT / "apps/desktop/stark_terminal_desktop/research_artifact_index_display",
    ]

    assert [path for path in suspicious_roots if path.exists()] == []
