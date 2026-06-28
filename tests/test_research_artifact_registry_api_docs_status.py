from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_71_DOCS = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_INGESTION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_EXECUTION_POLICY.md",
]


def test_prompt_71_docs_exist_and_state_api_boundaries() -> None:
    combined = []
    for doc in PROMPT_71_DOCS:
        path = ROOT / doc
        assert path.exists(), f"{doc} missing"
        text = path.read_text(encoding="utf-8")
        combined.append(text)
        lowered = text.lower()
        assert "research artifact registry api" in lowered
        assert "prompt 71" in lowered or "api contract" in lowered

    normalized = " ".join("\n".join(combined).lower().split())
    assert "api contract skeleton" in normalized
    assert "read-only" in normalized
    assert "unavailable" in normalized
    assert "no active" in normalized
    assert "no file upload" in normalized or "no upload" in normalized
    assert "no file download" in normalized or "no download" in normalized or "upload/download" in normalized
    assert "no paper parsing" in normalized
    assert "no strategy generation" in normalized
    assert "no backtesting" in normalized
    assert "no recommendations" in normalized or "no recommendation" in normalized
    assert "no execution" in normalized


def test_status_docs_reflect_prompt_71() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Research Artifact Registry Status" in north_star
    assert "research_artifact_registry_api" in project_map
    assert "Prompt 73 - Research Artifact Registry Safety Boundary Audit" in next_phase
    assert "Prompt 71 - Research Artifact Registry API Contract Skeleton" in prompt_log
