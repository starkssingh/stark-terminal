from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
]


def test_phase_has_no_strategy_signal_factor_or_alpha_generation_functions() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in SOURCE_ROOTS
        for path in root.glob("*.py")
    )
    for phrase in [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def artifact_to_strategy",
        "def paper_to_strategy",
    ]:
        assert phrase not in source


def test_phase_no_strategy_generation_doc_states_boundary() -> None:
    text = (
        ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_STRATEGY_GENERATION_AUDIT.md"
    ).read_text(encoding="utf-8").lower()
    for phrase in [
        "no strategy generation",
        "no strategy code generation",
        "no signal generation",
        "no factor generation",
        "no alpha generation",
        "no generated thresholds",
        "no artifact-to-strategy path",
        "no paper-to-strategy path",
    ]:
        assert phrase in text
