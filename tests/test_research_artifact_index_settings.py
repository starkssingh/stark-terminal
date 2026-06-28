from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


ROOT = Path(__file__).resolve().parents[1]
DANGEROUS_FLAGS = [
    "research_artifact_index_allow_indexing_engine",
    "research_artifact_index_allow_search_engine",
    "research_artifact_index_allow_ranking_engine",
    "research_artifact_index_allow_retrieval_engine",
    "research_artifact_index_allow_embeddings",
    "research_artifact_index_allow_vector_store",
    "research_artifact_index_allow_active_ingestion",
    "research_artifact_index_allow_persistent_storage",
    "research_artifact_index_allow_file_uploads",
    "research_artifact_index_allow_file_downloads",
    "research_artifact_index_allow_file_previews",
    "research_artifact_index_allow_paper_parsing",
    "research_artifact_index_allow_pdf_parsing",
    "research_artifact_index_allow_arxiv_ingestion",
    "research_artifact_index_allow_llm_analysis",
    "research_artifact_index_allow_strategy_generation",
    "research_artifact_index_allow_backtesting",
    "research_artifact_index_allow_recommendations",
    "research_artifact_index_allow_execution",
]


def test_research_artifact_index_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.research_artifact_index_enabled is True
    assert settings.research_artifact_index_schema_version == "v1"
    assert settings.research_artifact_index_stage == "planning_and_guardrails"
    for flag in DANGEROUS_FLAGS:
        assert getattr(settings, flag) is False


def test_research_artifact_index_settings_snapshot_is_safe() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["prompt_number"] == "107"
    assert snapshot["research_artifact_index_enabled"] is True
    assert snapshot["research_artifact_index_schema_version"] == "v1"
    assert snapshot["research_artifact_index_stage"] == "planning_and_guardrails"
    for flag in DANGEROUS_FLAGS:
        assert snapshot[flag] is False


@pytest.mark.parametrize("field_name", DANGEROUS_FLAGS)
def test_research_artifact_index_rejects_dangerous_allow_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_research_artifact_index_stage_validation() -> None:
    assert Settings(research_artifact_index_stage="api_contract_skeleton").research_artifact_index_stage == "api_contract_skeleton"
    with pytest.raises(ValidationError):
        Settings(research_artifact_index_stage="active_index")


def test_active_decision_architecture_docs_and_tests_are_preserved() -> None:
    for path in [
        "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
        "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
        "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
        "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
        "docs/AUDIT_LOG_JOURNAL_TARGET.md",
        "tests/test_active_decision_architecture_target_docs.py",
        "tests/test_decision_candidate_pipeline_target_docs.py",
        "tests/test_verifier_layer_target_architecture_docs.py",
        "tests/test_no_trade_commit_language_in_active_decision_target.py",
    ]:
        assert (ROOT / path).exists(), path
