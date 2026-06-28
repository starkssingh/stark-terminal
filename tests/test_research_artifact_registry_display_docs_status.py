from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_72_DOCS = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_CARD_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_LIFECYCLE_BADGES.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_ACTIVE_UI_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_INGESTION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_EXECUTION_POLICY.md",
]


def test_prompt_72_docs_exist_and_state_display_boundaries() -> None:
    combined = []
    for doc in PROMPT_72_DOCS:
        path = ROOT / doc
        assert path.exists(), f"{doc} missing"
        text = path.read_text(encoding="utf-8")
        combined.append(text)
        lowered = text.lower()
        assert "research artifact registry display" in lowered
        assert "prompt 72" in lowered or "display contract" in lowered

    normalized = " ".join("\n".join(combined).lower().split())
    assert "display contract skeleton" in normalized
    assert "backend-only" in normalized
    assert "read-only" in normalized
    assert "unavailable" in normalized
    assert "no active ui" in normalized
    assert "frontend" in normalized
    assert "desktop" in normalized
    assert "no file preview" in normalized or "file previews" in normalized
    assert "no active artifact ingestion" in normalized or "no active ingestion" in normalized
    assert "no file upload" in normalized or "file upload/download" in normalized
    assert "no paper parsing" in normalized
    assert "no strategy generation" in normalized
    assert "no backtesting" in normalized
    assert "no recommendations" in normalized or "no recommendation" in normalized
    assert "no execution" in normalized
    assert "mac mini m2" in normalized
    assert "windows-native" in normalized


def test_status_docs_reflect_prompt_72() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Research Artifact Registry Status" in north_star
    assert "research_artifact_registry_display" in project_map
    assert "Prompt 73 - Research Artifact Registry Safety Boundary Audit" in next_phase
    assert "Prompt 72 - Research Artifact Registry Display Contract Skeleton" in prompt_log
