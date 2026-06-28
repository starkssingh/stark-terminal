from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"


def test_boundary_has_no_strategy_signal_factor_or_alpha_generation_functions() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
    for phrase in [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
    ]:
        assert phrase not in text


def test_boundary_docs_state_no_strategy_generation_policy() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_STRATEGY_GENERATION_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no strategy generation",
        "no strategy code generation",
        "no signal/factor/alpha generation",
        "no artifact-to-strategy path",
        "no paper-to-strategy path",
        "future prompt and audit required",
    ]:
        assert phrase in text

