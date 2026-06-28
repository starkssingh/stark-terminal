# Tests Consolidated Report

Status: grouped test-report consolidation and verified deletion.

This report preserves the details of superseded granular prompt-level audit
tests selected for deletion. The deleted tests were already archived with the
`.py.archived` suffix and were not active pytest suite members before this
pass.

## Grouped Replacement Tests

- `tests/phases/test_research_artifact_index_phase.py`
- `tests/phases/test_research_artifact_registry_phase.py`
- `tests/phases/test_strategy_research_workspace_phase.py`
- `tests/phases/test_active_decision_architecture_phase.py`
- `tests/boundaries/test_no_execution_boundary.py`
- `tests/boundaries/test_research_artifact_boundaries.py`
- `tests/boundaries/test_documentation_consolidation_policy.py`
- active API-surface, safety boundary, milestone, integration, settings, and
  contract behavior tests that remain in place

## Decision Desk

No Decision Desk tests are deleted in this pass. Decision Desk behavior,
contracts, API surfaces, evidence validation, human-review, and execution
boundary tests remain active.

## Retail Dashboard

No Retail Dashboard tests are deleted in this pass. Retail Dashboard planning,
API, display, safety, milestone, boundary, and integration tests remain active
pending a dedicated future consolidation review.

## Retail Trader Experience

No Retail Trader Experience tests are deleted in this pass. Retail Trader
Experience planning, API, display, safety, milestone, boundary, and integration
tests remain active pending a dedicated future consolidation review.

## Strategy Research Workspace

Deleted archived tests and original function counts:

- `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_active_ui_audit.py.archived`: 4 tests
- `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_paper_parsing_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_strategy_generation_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_backtesting_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_recommendation_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_execution_audit.py.archived`: 3 tests

Total deleted archived Strategy Research Workspace test functions: 19.

Coverage preserved by:

- `tests/phases/test_strategy_research_workspace_phase.py`
- `tests/boundaries/test_no_execution_boundary.py`
- `tests/boundaries/test_documentation_consolidation_policy.py`
- remaining active Strategy Research Workspace API/display/boundary/integration
  tests and package behavior tests

## Research Artifact Registry

Deleted archived tests and original function counts:

- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_active_ingestion_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_persistent_storage_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_upload_download_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_active_ui_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_paper_parsing_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_strategy_generation_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_backtesting_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_recommendation_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_execution_audit.py.archived`: 3 tests

Total deleted archived Research Artifact Registry test functions: 21.

Coverage preserved by:

- `tests/phases/test_research_artifact_registry_phase.py`
- `tests/boundaries/test_research_artifact_boundaries.py`
- `tests/boundaries/test_no_execution_boundary.py`
- `tests/boundaries/test_documentation_consolidation_policy.py`
- remaining active Research Artifact Registry API/display/boundary/integration
  tests and package behavior tests

## Research Artifact Index

Deleted archived tests and original function counts:

- `tests/archive/prompt_audits/test_research_artifact_index_api_boundary_audit.py.archived`: 3 tests
- `tests/archive/prompt_audits/test_research_artifact_index_display_boundary_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/test_research_artifact_index_no_active_ui_audit.py.archived`: 1 test
- `tests/archive/prompt_audits/test_research_artifact_index_no_indexing_search_ranking_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/test_research_artifact_index_no_retrieval_audit.py.archived`: 1 test
- `tests/archive/prompt_audits/test_research_artifact_index_no_embeddings_vector_store_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/test_research_artifact_index_no_active_ingestion_storage_audit.py.archived`: 2 tests
- `tests/archive/prompt_audits/test_research_artifact_index_no_upload_download_preview_audit.py.archived`: 1 test
- `tests/archive/prompt_audits/test_research_artifact_index_no_paper_parsing_audit.py.archived`: 1 test
- `tests/archive/prompt_audits/test_research_artifact_index_no_strategy_generation_audit.py.archived`: 1 test
- `tests/archive/prompt_audits/test_research_artifact_index_no_backtesting_audit.py.archived`: 1 test
- `tests/archive/prompt_audits/test_research_artifact_index_no_recommendation_execution_audit.py.archived`: 1 test

Total deleted archived Research Artifact Index test functions: 18.

Coverage preserved by:

- `tests/phases/test_research_artifact_index_phase.py`
- `tests/phases/test_research_artifact_index_milestone_phase.py`
- `tests/boundaries/test_research_artifact_boundaries.py`
- `tests/boundaries/test_research_artifact_index_milestone_boundaries.py`
- `tests/boundaries/test_research_artifact_index_next_phase_readiness.py`
- remaining active Research Artifact Index API/display/safety/milestone tests
  and package behavior tests

## Active Decision Architecture

No Active Decision Architecture tests are deleted. These remain active:

- `tests/test_active_decision_architecture_target_docs.py`
- `tests/test_decision_candidate_pipeline_target_docs.py`
- `tests/test_verifier_layer_target_architecture_docs.py`
- `tests/test_no_trade_commit_language_in_active_decision_target.py`
- `tests/phases/test_active_decision_architecture_phase.py`

## Deleted Archived Test Summary

- Deleted archived test files: 27
- Original archived test functions represented: 58
- Active pytest count before deletion: 4782
- Expected active pytest count after deletion: unchanged at 4782, because the
  deleted tests were already not collected by pytest

## Tests Intentionally Preserved

All active behavior tests remain preserved: settings, schema/model creation,
API endpoint behavior, contract validation, analytics calculations, storage,
workers, provider contracts, serialization, health endpoints, and package
invariants were not deleted.
