from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_70_DOCS = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_PLANNING.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_GUARDRAILS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_LIFECYCLE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_FORBIDDEN_INTERACTIONS.md",
    "docs/RESEARCH_ARTIFACT_NO_INGESTION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_RECOMMENDATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_EXECUTION_POLICY.md",
]


def test_prompt_70_docs_exist_and_state_boundaries() -> None:
    for doc in PROMPT_70_DOCS:
        path = ROOT / doc
        assert path.exists(), f"{doc} missing"
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        normalized = " ".join(lowered.split())
        assert "research artifact registry" in lowered
        assert "planning" in lowered
        assert "guardrails" in lowered or "policy" in lowered or "placeholder" in lowered
        assert "no active artifact ingestion" in normalized
        assert "no active artifact storage" in normalized or "no persistent artifact storage" in normalized
        assert "no paper parsing" in normalized
        assert "no strategy generation" in normalized
        assert "no backtesting" in normalized
        assert "no recommendations" in normalized or "no recommendation" in normalized
        assert "no execution" in normalized


def test_status_docs_reflect_prompt_70() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Research Artifact Registry Status" in north_star
    assert "research_artifact_registry" in project_map
    assert "Prompt 71 - Research Artifact Registry API Contract Skeleton" in next_phase
    assert "Prompt 70 - Research Artifact Registry Planning and Guardrails" in prompt_log
