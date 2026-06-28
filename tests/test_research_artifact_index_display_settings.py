from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_DECISION_DOCS = [
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
]
ACTIVE_DECISION_TESTS = [
    "tests/test_active_decision_architecture_target_docs.py",
    "tests/test_decision_candidate_pipeline_target_docs.py",
    "tests/test_verifier_layer_target_architecture_docs.py",
    "tests/test_no_trade_commit_language_in_active_decision_target.py",
]


def test_research_artifact_index_display_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.research_artifact_index_display_enabled is True
    assert settings.research_artifact_index_display_schema_version == "v1"
    assert settings.research_artifact_index_display_stage == "display_contract_skeleton"
    for field_name in [
        "research_artifact_index_display_allow_active_ui",
        "research_artifact_index_display_allow_frontend_components",
        "research_artifact_index_display_allow_desktop_components",
        "research_artifact_index_display_allow_indexing_engine",
        "research_artifact_index_display_allow_search_engine",
        "research_artifact_index_display_allow_ranking_engine",
        "research_artifact_index_display_allow_retrieval_engine",
        "research_artifact_index_display_allow_embeddings",
        "research_artifact_index_display_allow_vector_store",
        "research_artifact_index_display_allow_active_ingestion",
        "research_artifact_index_display_allow_persistent_storage",
        "research_artifact_index_display_allow_file_uploads",
        "research_artifact_index_display_allow_file_downloads",
        "research_artifact_index_display_allow_file_previews",
        "research_artifact_index_display_allow_paper_parsing",
        "research_artifact_index_display_allow_strategy_generation",
        "research_artifact_index_display_allow_backtesting",
        "research_artifact_index_display_allow_recommendations",
        "research_artifact_index_display_allow_execution",
    ]:
        assert getattr(settings, field_name) is False


def test_research_artifact_index_display_safe_snapshot_exposes_safe_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["prompt_number"] == "107"
    assert snapshot["research_artifact_index_display_enabled"] is True
    assert snapshot["research_artifact_index_display_stage"] == "display_contract_skeleton"
    assert snapshot["research_artifact_index_display_schema_version"] == "v1"
    for key, value in snapshot.items():
        if key.startswith("research_artifact_index_display_allow_"):
            assert value is False


@pytest.mark.parametrize(
    "field_name",
    [
        "research_artifact_index_display_allow_active_ui",
        "research_artifact_index_display_allow_frontend_components",
        "research_artifact_index_display_allow_desktop_components",
        "research_artifact_index_display_allow_indexing_engine",
        "research_artifact_index_display_allow_search_engine",
        "research_artifact_index_display_allow_ranking_engine",
        "research_artifact_index_display_allow_retrieval_engine",
        "research_artifact_index_display_allow_embeddings",
        "research_artifact_index_display_allow_vector_store",
        "research_artifact_index_display_allow_active_ingestion",
        "research_artifact_index_display_allow_persistent_storage",
        "research_artifact_index_display_allow_file_uploads",
        "research_artifact_index_display_allow_file_downloads",
        "research_artifact_index_display_allow_file_previews",
        "research_artifact_index_display_allow_paper_parsing",
        "research_artifact_index_display_allow_strategy_generation",
        "research_artifact_index_display_allow_backtesting",
        "research_artifact_index_display_allow_recommendations",
        "research_artifact_index_display_allow_execution",
    ],
)
def test_research_artifact_index_display_settings_reject_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_active_decision_architecture_docs_and_tests_are_preserved_for_prompt_79() -> None:
    for relative in [*ACTIVE_DECISION_DOCS, *ACTIVE_DECISION_TESTS]:
        assert (ROOT / relative).exists()

    active_decision = (ROOT / "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md").read_text(encoding="utf-8")
    assert "Decision candidate is not a trade" in active_decision
    assert "execution APIs remain forbidden" in active_decision
