from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]


def test_strategy_research_workspace_phase_has_no_strategy_generation_functions() -> None:
    code = "\n".join(
        path.read_text(encoding="utf-8")
        for package in PACKAGES
        for path in package.glob("*.py")
    ).lower()

    for forbidden in [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "paper_to_strategy",
        "hidden_threshold",
    ]:
        assert forbidden not in code


def test_strategy_research_workspace_phase_no_strategy_generation_doc_is_explicit() -> None:
    text = (
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_STRATEGY_GENERATION_AUDIT.md"
    ).read_text(encoding="utf-8")

    for phrase in [
        "No strategy generation exists",
        "No strategy code generation exists",
        "No signal generation exists",
        "No factor generation exists",
        "No alpha generation exists",
        "Hypotheses remain placeholders only",
    ]:
        assert phrase in text
