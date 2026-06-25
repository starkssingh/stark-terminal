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


def test_strategy_research_workspace_has_no_strategy_generation_functions() -> None:
    combined = _combined_code()

    for forbidden in [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def paper_to_strategy",
        "strategy_threshold",
        "hidden_threshold",
    ]:
        assert forbidden not in combined


def test_strategy_research_workspace_has_no_strategy_generation_routes() -> None:
    combined = "\n".join(route.read_text(encoding="utf-8") for route in ROUTES)

    for forbidden_path in [
        "generate-strategy",
        "strategy-generation",
        "strategy-code",
        "generate-signal",
        "generate-factor",
        "generate-alpha",
        "paper-to-strategy",
    ]:
        assert forbidden_path not in combined


def test_strategy_research_workspace_no_strategy_generation_docs_forbid_generation() -> None:
    docs = [
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NO_STRATEGY_GENERATION_AUDIT.md",
        ROOT / "docs/STRATEGY_RESEARCH_NO_STRATEGY_GENERATION_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_STRATEGY_GENERATION_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_STRATEGY_GENERATION_POLICY.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs).lower()

    for phrase in [
        "no strategy generation",
        "no strategy code generation",
        "no signal generation",
        "no factor generation",
        "no alpha generation",
        "no hidden strategy thresholds",
        "no paper-to-strategy path",
    ]:
        assert phrase in combined
