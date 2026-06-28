from __future__ import annotations

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.research_artifact_registry.readiness import research_artifact_registry_readiness


def test_research_artifact_registry_readiness_is_planning_only() -> None:
    readiness = research_artifact_registry_readiness(Settings())

    assert readiness.registry_planning_ready is True
    assert readiness.active_ingestion_enabled is False
    assert readiness.persistent_storage_enabled is False
    assert readiness.file_uploads_enabled is False
    assert readiness.file_downloads_enabled is False
    assert readiness.paper_parsing_enabled is False
    assert readiness.strategy_generation_enabled is False
    assert readiness.backtesting_enabled is False
    assert readiness.recommendations_enabled is False
    assert readiness.execution_enabled is False
    assert readiness.next_allowed_phase == "api_contract_skeleton"

