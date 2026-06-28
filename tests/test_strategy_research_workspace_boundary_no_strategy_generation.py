from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_boundary_has_no_strategy_generation_functions() -> None:
    code = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "packages/core/stark_terminal_core").rglob("*.py")
        if "strategy_research_workspace" in path.as_posix()
    )

    for name in [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def paper_to_strategy",
    ]:
        assert name not in code


def test_strategy_research_workspace_boundary_docs_forbid_strategy_generation() -> None:
    docs = (ROOT / "docs/STRATEGY_RESEARCH_BOUNDARY_NO_STRATEGY_GENERATION_POLICY.md").read_text(
        encoding="utf-8"
    )

    assert "does not add strategy generation" in docs
    assert "does not add strategy code generation" in docs
    assert "hidden strategy logic" in docs
