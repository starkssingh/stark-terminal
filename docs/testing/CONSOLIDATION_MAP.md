# Documentation and Test Consolidation Map

Status: documentation/test consolidation interlude.

## Old Pattern

The previous safety-hardening pattern created one prompt-level document and one prompt-level test file for many individual forbidden capabilities. That was useful while the architecture was being fenced, but it made the repo harder to navigate.

Examples of the old pattern:

- one audit doc per forbidden behavior
- one test file per capability boundary
- prompt-number docs used as the primary navigation layer
- verifier checks tied to every granular artifact

## New Pattern

The new default is phase-first and boundary-first:

- phase summaries in `docs/phases/`
- grouped safety audits in `docs/audits/`
- test policy and baseline in `docs/testing/`
- grouped phase tests in `tests/phases/`
- grouped boundary tests in `tests/boundaries/`
- prompt logs remain for historical traceability

## Prompt 107 Compliance

Prompt 107 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc and status/audit docs, adds grouped closure
tests only, and creates no new runtime product capability:

- `tests/phases/test_retail_decision_console_internal_preview_milestone_closure.py`
- `tests/boundaries/test_retail_decision_console_internal_preview_milestone_boundaries.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 107.

## Prompt 106 Compliance

Prompt 106 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, updates the internal preview package
runbook, adds one smoke verification helper, one smoke verification script,
and grouped tests only:

- `packages/core/stark_terminal_core/retail_decision_console/internal_preview_smoke.py`
- `scripts/smoke_verify_retail_decision_console_internal_preview.py`
- `tests/phases/test_retail_decision_console_internal_preview_smoke_phase.py`
- `tests/boundaries/test_retail_decision_console_internal_preview_smoke_boundaries.py`
- `tests/boundaries/test_smoke_verify_retail_decision_console_internal_preview_script.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 106.

## Prompt 105 Compliance

Prompt 105 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one internal preview package module,
one internal preview package builder script, one internal preview package
runbook, one internal review notes template, and grouped tests only:

- `packages/core/stark_terminal_core/retail_decision_console/internal_preview_package.py`
- `scripts/build_retail_decision_console_internal_preview.py`
- `docs/runbooks/retail_decision_console_internal_preview_package.md`
- `docs/templates/retail_decision_console_internal_review_notes.md`
- `tests/phases/test_retail_decision_console_internal_preview_package_phase.py`
- `tests/boundaries/test_retail_decision_console_internal_preview_package_boundaries.py`
- `tests/boundaries/test_build_retail_decision_console_internal_preview_script.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 105.

## Prompt 104 Compliance

Prompt 104 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one manual acceptance checklist
runbook, and grouped tests only:

- `docs/runbooks/retail_decision_console_manual_acceptance_checklist.md`
- `tests/phases/test_retail_decision_console_manual_acceptance_phase.py`
- `tests/boundaries/test_retail_decision_console_manual_acceptance_boundaries.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 104.

## Prompt 103 Compliance

Prompt 103 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one QA bundle module, one local QA
bundle script, one local QA bundle runbook, and grouped tests only:

- `packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py`
- `scripts/build_retail_decision_console_qa_bundle.py`
- `docs/runbooks/retail_decision_console_local_qa_bundle.md`
- `tests/phases/test_retail_decision_console_local_qa_bundle_phase.py`
- `tests/boundaries/test_retail_decision_console_local_qa_bundle_boundaries.py`
- `tests/boundaries/test_build_retail_decision_console_qa_bundle_script.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 103.

## Prompt 102 Compliance

Prompt 102 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one snapshot export module, extends
the safe preview helper with local snapshot print/export flags, and adds
grouped tests only:

- `packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py`
- `tests/phases/test_retail_decision_console_preview_snapshot_phase.py`
- `tests/boundaries/test_retail_decision_console_preview_snapshot_boundaries.py`
- `tests/boundaries/test_preview_retail_decision_console_snapshot_script.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 102.

## Prompt 101 Compliance

Prompt 101 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one static interaction descriptor
module, exposes static interactions through the safe view-model/desktop
preview path, and adds grouped tests only:

- `packages/core/stark_terminal_core/retail_decision_console/interactions.py`
- `tests/phases/test_retail_decision_console_static_interactions_phase.py`
- `tests/boundaries/test_retail_decision_console_static_interactions_boundaries.py`
- `tests/boundaries/test_desktop_retail_decision_console_static_interactions.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 101.

## Prompt 100 Compliance

Prompt 100 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one layout descriptor module, improves
the static/demo desktop shell layout and preview summary, and adds grouped
tests only:

- `packages/core/stark_terminal_core/retail_decision_console/layout.py`
- `tests/phases/test_retail_decision_console_visual_layout_phase.py`
- `tests/boundaries/test_retail_decision_console_visual_layout_boundaries.py`
- `tests/boundaries/test_desktop_retail_decision_console_visual_layout.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 100.

## Prompt 99 Compliance

Prompt 99 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds two runbooks, one safe preview helper
script, and grouped tests only:

- `docs/runbooks/retail_decision_console_local_preview.md`
- `docs/runbooks/retail_decision_console_manual_smoke_test.md`
- `scripts/preview_retail_decision_console.py`
- `tests/phases/test_retail_decision_console_local_preview_phase.py`
- `tests/boundaries/test_retail_decision_console_local_preview_boundaries.py`
- `tests/boundaries/test_preview_retail_decision_console_script.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 99.

## Prompt 98 Compliance

Prompt 98 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds one state view-model/wiring module,
one GET-only metadata endpoint, and grouped tests only:

- `tests/phases/test_retail_decision_console_static_state_wiring_phase.py`
- `tests/boundaries/test_retail_decision_console_static_state_wiring_boundaries.py`
- `tests/boundaries/test_desktop_retail_decision_console_static_state_wiring.py`
- `tests/boundaries/test_api_retail_decision_console_static_state_wiring.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 98.

## Prompt 97 Compliance

Prompt 97 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds static/demo state modules, one
GET-only metadata endpoint, and grouped tests only:

- `tests/phases/test_retail_decision_console_demo_state_phase.py`
- `tests/boundaries/test_retail_decision_console_demo_state_boundaries.py`
- `tests/boundaries/test_api_retail_decision_console_demo_state.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 97.

## Prompt 96 Compliance

Prompt 96 follows the grouped docs/tests policy. It updates the canonical
Retail Decision Console phase doc, adds UI descriptor modules, one desktop
shell module, and grouped tests only:

- `tests/phases/test_retail_decision_console_ui_shell_phase.py`
- `tests/boundaries/test_retail_decision_console_ui_shell_boundaries.py`
- `tests/boundaries/test_desktop_retail_decision_console_shell.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 96.

## Prompt 95 Compliance

Prompt 95 follows the grouped docs/tests policy. It adds one canonical phase
doc, one product surface package, one GET-only read-only route family, and
grouped tests only:

- `docs/phases/retail_decision_console.md`
- `tests/phases/test_retail_decision_console_phase.py`
- `tests/boundaries/test_retail_decision_console_boundaries.py`
- `tests/boundaries/test_api_retail_decision_console.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 95.

## Prompt 94 Compliance

Prompt 94 follows the phase-based docs/tests policy. It adds:

- `docs/phases/product_surface_reorientation.md`
- `tests/phases/test_product_surface_reorientation_phase.py`
- `tests/boundaries/test_product_surface_reorientation_boundaries.py`

It does not create prompt-level audit docs, one doc per forbidden capability,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 94.

## Major Families Consolidated

| Historical family | Grouped replacement |
| --- | --- |
| Research Artifact Index Prompt 77-80 docs | `docs/phases/research_artifact_index.md`, `docs/audits/research_artifact_boundaries.md` |
| Research Artifact Index Prompt 77-80 tests | `tests/phases/test_research_artifact_index_phase.py`, `tests/boundaries/test_research_artifact_boundaries.py` |
| Research Artifact Registry Prompt 70-76 docs | `docs/phases/research_artifact_registry.md`, `docs/audits/research_artifact_boundaries.md` |
| Research Artifact Registry Prompt 70-76 tests | `tests/phases/test_research_artifact_registry_phase.py`, `tests/boundaries/test_research_artifact_boundaries.py` |
| Strategy Research Workspace phase docs | `docs/phases/strategy_research_workspace.md`, `docs/audits/safety_boundaries.md` |
| Strategy Research Workspace phase tests | `tests/phases/test_strategy_research_workspace_phase.py` |
| Active Decision Architecture target docs | `docs/phases/active_decision_architecture.md` plus the original target docs |
| Execution boundary docs/tests | `docs/audits/no_execution.md`, `tests/boundaries/test_no_execution_boundary.py` |

## Prompt 81 Compliance

Prompt 81 follows the phase-based consolidation policy. It adds:

- `docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT.md`
- `docs/RESEARCH_ARTIFACT_INDEX_NEXT_PHASE_PLAN.md`
- `tests/phases/test_research_artifact_index_milestone_phase.py`
- `tests/boundaries/test_research_artifact_index_milestone_boundaries.py`
- `tests/boundaries/test_research_artifact_index_next_phase_readiness.py`

It does not create prompt-sprawl or one audit file per forbidden capability.

## Prompt 82 Compliance

Prompt 82 follows the grouped docs/tests policy. It adds:

- `docs/RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_HARDENING.md`
- `tests/phases/test_research_artifact_index_system_boundary_phase.py`
- `tests/boundaries/test_research_artifact_index_system_boundaries.py`
- `tests/boundaries/test_api_research_artifact_index_boundary.py`

It updates grouped phase/audit/status docs and does not create one audit file
per forbidden capability. No micro-audit sprawl was added; the exact active
policy is no micro-audit sprawl.

## Prompt 83 Compliance

Prompt 83 follows the grouped docs/tests policy. It adds:

- `docs/RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md`
- `docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md`
- `tests/phases/test_research_artifact_index_api_display_integration_phase.py`
- `tests/boundaries/test_research_artifact_index_api_display_integration_boundaries.py`
- `tests/boundaries/test_api_research_artifact_index_integration_consistency.py`

It updates grouped phase/audit/status docs and does not create one audit file
per forbidden capability. No micro-audit sprawl was added for Prompt 83.

## Prompt 84 Compliance

Prompt 84 follows the grouped docs/tests policy. It adds:

- `docs/RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md`
- `docs/phases/research_metadata_graph.md`
- `tests/phases/test_research_metadata_graph_phase.py`
- `tests/boundaries/test_research_metadata_graph_boundaries.py`
- `tests/boundaries/test_api_research_metadata_graph.py`

It updates grouped phase/audit/status docs and does not create one audit file
per forbidden capability. No micro-audit sprawl was added for Prompt 84.

## Prompt 85 Compliance

Prompt 85 follows the grouped docs/tests policy. It adds:

- `docs/RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md`
- `tests/phases/test_research_metadata_graph_api_phase.py`
- `tests/boundaries/test_research_metadata_graph_api_boundaries.py`
- `tests/boundaries/test_api_research_metadata_graph_contract.py`

It updates grouped phase/audit/status docs and does not create one audit file
per forbidden capability. No micro-audit sprawl was added for Prompt 85.

## Prompt 86 Compliance

Prompt 86 follows the grouped docs/tests policy. It adds:

- `docs/RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md`
- `tests/phases/test_research_metadata_graph_display_phase.py`
- `tests/boundaries/test_research_metadata_graph_display_boundaries.py`
- `tests/boundaries/test_api_research_metadata_graph_display.py`

It updates grouped phase/audit/status docs and does not create one audit file
per forbidden capability. No micro-audit sprawl was added for Prompt 86.

## Prompt 87 Compliance

Prompt 87 follows the grouped docs/tests policy. It adds:

- `docs/RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md`
- `tests/phases/test_research_metadata_graph_safety_audit_phase.py`
- `tests/boundaries/test_research_metadata_graph_safety_boundaries.py`
- `tests/boundaries/test_api_research_metadata_graph_safety_surface.py`

It updates grouped phase/audit/status docs and does not create one audit file
per forbidden capability. No micro-audit sprawl was added for Prompt 87.

## Prompt 88-B Compliance

Prompt 88-B follows the phase-based docs/tests policy. It closes the Research
Metadata Graph phase in the canonical phase doc and adds only:

- `tests/phases/test_research_metadata_graph_phase_closure.py`

It does not add standalone milestone-audit docs, standalone next-phase docs,
or one test file per forbidden capability. No micro-audit sprawl was added for
Prompt 88-B.

## Prompt 89 Compliance

Prompt 89 follows the phase-based docs/tests policy. It adds one canonical
phase doc, one planning package, one GET-only read-only route family, and
grouped tests only:

- `docs/phases/research_knowledge_map.md`
- `tests/phases/test_research_knowledge_map_phase.py`
- `tests/boundaries/test_research_knowledge_map_boundaries.py`
- `tests/boundaries/test_api_research_knowledge_map.py`

No prompt-level micro-audit docs or one-test-file-per-forbidden-capability
files were added for Prompt 89.

## Prompt 90 Compliance

Prompt 90 follows the phase-based docs/tests policy. It updates the canonical
Research Knowledge Map phase doc, adds one API contract package, one GET-only
read-only route family, and grouped tests only:

- `docs/phases/research_knowledge_map.md`
- `tests/phases/test_research_knowledge_map_api_phase.py`
- `tests/boundaries/test_research_knowledge_map_api_boundaries.py`
- `tests/boundaries/test_api_research_knowledge_map_contract.py`

No prompt-level micro-audit docs or one-test-file-per-forbidden-capability
files were added for Prompt 90.

## Prompt 91 Compliance

Prompt 91 follows the phase-based docs/tests policy. It updates the canonical
Research Knowledge Map phase doc, adds one display contract package, one
GET-only read-only route family, and grouped tests only:

- `docs/phases/research_knowledge_map.md`
- `tests/phases/test_research_knowledge_map_display_phase.py`
- `tests/boundaries/test_research_knowledge_map_display_boundaries.py`
- `tests/boundaries/test_api_research_knowledge_map_display.py`

No prompt-level micro-audit docs or one-test-file-per-forbidden-capability
files were added for Prompt 91.

## Prompt 92 Compliance

Prompt 92 follows the phase-based docs/tests policy. It updates the canonical
Research Knowledge Map phase doc, adds no standalone safety-boundary audit
doc, adds no runtime endpoint, and uses grouped tests only:

- `docs/phases/research_knowledge_map.md`
- `tests/phases/test_research_knowledge_map_safety_phase.py`
- `tests/boundaries/test_research_knowledge_map_safety_boundaries.py`
- `tests/boundaries/test_api_research_knowledge_map_safety_surface.py`

No prompt-level micro-audit docs or one-test-file-per-forbidden-capability
files were added for Prompt 92.

## Prompt 93 Compliance

Prompt 93 follows the phase-based docs/tests policy. It updates the canonical
Research Knowledge Map phase doc, adds no standalone milestone audit doc, adds
no standalone next-phase plan doc, adds no runtime endpoint, and uses one
grouped test only:

- `docs/phases/research_knowledge_map.md`
- `tests/phases/test_research_knowledge_map_phase_closure.py`

No prompt-level micro-audit docs or one-test-file-per-forbidden-capability
files were added for Prompt 93.

## Intentionally Unmerged

These remain intentionally separate:

- `docs/PROMPT_LOG.md` for chronological continuity
- `docs/API_SURFACE_INVENTORY.md` for endpoint inventory
- `docs/SAFETY_AUDIT.md` for top-level safety status
- active decision architecture target docs and tests
- granular prompt-level docs and tests already used by historical verifier checks

## Superseded

Granular prompt audit docs are superseded for navigation by grouped phase docs, but they are not deleted in this interlude. They remain historical audit artifacts.

Verifier keyword lock: granular prompt audit docs are superseded.

## Archive Pass 1

Archive Pass 1 moves obvious Research Artifact Index Prompt 80 micro-audit
artifacts into historical archive directories after grouped phase and boundary
coverage passed in Prompt 81.

Grouped replacement coverage:

- `docs/phases/research_artifact_index.md`
- `docs/audits/research_artifact_boundaries.md`
- `docs/audits/safety_boundaries.md`
- `tests/phases/test_research_artifact_index_phase.py`
- `tests/phases/test_research_artifact_index_milestone_phase.py`
- `tests/boundaries/test_research_artifact_boundaries.py`
- `tests/boundaries/test_research_artifact_index_milestone_boundaries.py`
- `tests/boundaries/test_research_artifact_index_next_phase_readiness.py`

Archived docs:

| Original path | Archive path |
| --- | --- |
| `docs/RESEARCH_ARTIFACT_INDEX_API_BOUNDARY_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_API_BOUNDARY_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_BOUNDARY_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_DISPLAY_BOUNDARY_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_UI_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_UI_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_INDEXING_SEARCH_RANKING_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_INDEXING_SEARCH_RANKING_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_RETRIEVAL_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_RETRIEVAL_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_EMBEDDINGS_VECTOR_STORE_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_EMBEDDINGS_VECTOR_STORE_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_UPLOAD_DOWNLOAD_PREVIEW_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_UPLOAD_DOWNLOAD_PREVIEW_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_PAPER_PARSING_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_PAPER_PARSING_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_STRATEGY_GENERATION_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_STRATEGY_GENERATION_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_BACKTESTING_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_BACKTESTING_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_INDEX_NO_RECOMMENDATION_EXECUTION_AUDIT.md` | `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_RECOMMENDATION_EXECUTION_AUDIT.md` |

Archived tests:

| Original path | Archive path |
| --- | --- |
| `tests/test_research_artifact_index_api_boundary_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_api_boundary_audit.py.archived` |
| `tests/test_research_artifact_index_display_boundary_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_display_boundary_audit.py.archived` |
| `tests/test_research_artifact_index_no_active_ui_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_active_ui_audit.py.archived` |
| `tests/test_research_artifact_index_no_indexing_search_ranking_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_indexing_search_ranking_audit.py.archived` |
| `tests/test_research_artifact_index_no_retrieval_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_retrieval_audit.py.archived` |
| `tests/test_research_artifact_index_no_embeddings_vector_store_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_embeddings_vector_store_audit.py.archived` |
| `tests/test_research_artifact_index_no_active_ingestion_storage_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_active_ingestion_storage_audit.py.archived` |
| `tests/test_research_artifact_index_no_upload_download_preview_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_upload_download_preview_audit.py.archived` |
| `tests/test_research_artifact_index_no_paper_parsing_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_paper_parsing_audit.py.archived` |
| `tests/test_research_artifact_index_no_strategy_generation_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_strategy_generation_audit.py.archived` |
| `tests/test_research_artifact_index_no_backtesting_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_backtesting_audit.py.archived` |
| `tests/test_research_artifact_index_no_recommendation_execution_audit.py` | `tests/archive/prompt_audits/test_research_artifact_index_no_recommendation_execution_audit.py.archived` |

Archived tests are historical references, not active suite members. They use
the `.py.archived` suffix and are not collected by pytest.

Verifier keyword lock: archived tests are historical references.

## Intentionally Not Archived In Pass 1

These remain active because they are main phase, milestone, API-surface, active
decision, or grouped consolidation artifacts:

- `docs/RESEARCH_ARTIFACT_INDEX_SAFETY_BOUNDARY_AUDIT.md`
- `docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_READINESS.md`
- `docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT.md`
- `docs/RESEARCH_ARTIFACT_INDEX_NEXT_PHASE_PLAN.md`
- `tests/test_research_artifact_index_safety_boundary_audit_docs.py`
- `tests/test_research_artifact_index_api_surface_safety.py`
- `tests/test_research_artifact_index_milestone_readiness.py`
- active decision architecture docs/tests
- grouped docs under `docs/phases/`, `docs/audits/`, and `docs/testing/`
- grouped tests under `tests/phases/` and `tests/boundaries/`

Uncertain or pending future review:

- older Decision Desk, Retail Dashboard, Retail Trader Experience, Strategy
  Research Workspace, and Research Artifact Registry granular audit files
- product-contract and settings tests that may still enforce unique behavior

## Archive Pass 2

Archive Pass 2 moves obvious older `NO_*` micro-audit artifacts for Strategy
Research Workspace and Research Artifact Registry into phase-specific archive
folders. The pass is conservative: it does not archive active source code,
active API routes, active package modules, settings/schema tests, contract
behavior tests, API endpoint tests, grouped phase/boundary docs/tests, active
decision architecture docs/tests, or top-level control documents.

Grouped replacement coverage:

- `docs/phases/strategy_research_workspace.md`
- `tests/phases/test_strategy_research_workspace_phase.py`
- `docs/phases/research_artifact_registry.md`
- `tests/phases/test_research_artifact_registry_phase.py`
- `docs/audits/safety_boundaries.md`
- `docs/audits/research_artifact_boundaries.md`
- `tests/boundaries/test_no_execution_boundary.py`
- `tests/boundaries/test_research_artifact_boundaries.py`
- `tests/boundaries/test_documentation_consolidation_policy.py`
- remaining active API-surface, safety boundary, milestone, and integration
  tests for these phases

### Strategy Research Workspace Archived Docs

| Original path | Archive path |
| --- | --- |
| `docs/STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md` | `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md` |
| `docs/STRATEGY_RESEARCH_WORKSPACE_NO_PAPER_PARSING_AUDIT.md` | `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_PAPER_PARSING_AUDIT.md` |
| `docs/STRATEGY_RESEARCH_WORKSPACE_NO_STRATEGY_GENERATION_AUDIT.md` | `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_STRATEGY_GENERATION_AUDIT.md` |
| `docs/STRATEGY_RESEARCH_WORKSPACE_NO_BACKTESTING_AUDIT.md` | `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_BACKTESTING_AUDIT.md` |
| `docs/STRATEGY_RESEARCH_WORKSPACE_NO_RECOMMENDATION_AUDIT.md` | `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_RECOMMENDATION_AUDIT.md` |
| `docs/STRATEGY_RESEARCH_WORKSPACE_NO_EXECUTION_AUDIT.md` | `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_EXECUTION_AUDIT.md` |

### Strategy Research Workspace Archived Tests

| Original path | Archive path |
| --- | --- |
| `tests/test_strategy_research_workspace_no_active_ui_audit.py` | `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_active_ui_audit.py.archived` |
| `tests/test_strategy_research_workspace_no_paper_parsing_audit.py` | `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_paper_parsing_audit.py.archived` |
| `tests/test_strategy_research_workspace_no_strategy_generation_audit.py` | `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_strategy_generation_audit.py.archived` |
| `tests/test_strategy_research_workspace_no_backtesting_audit.py` | `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_backtesting_audit.py.archived` |
| `tests/test_strategy_research_workspace_no_recommendation_audit.py` | `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_recommendation_audit.py.archived` |
| `tests/test_strategy_research_workspace_no_execution_audit.py` | `tests/archive/prompt_audits/strategy_research_workspace/test_strategy_research_workspace_no_execution_audit.py.archived` |

### Research Artifact Registry Archived Docs

| Original path | Archive path |
| --- | --- |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_INGESTION_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_INGESTION_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_PERSISTENT_STORAGE_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_PERSISTENT_STORAGE_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_UPLOAD_DOWNLOAD_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_UPLOAD_DOWNLOAD_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_UI_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_UI_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_PAPER_PARSING_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_PAPER_PARSING_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_STRATEGY_GENERATION_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_STRATEGY_GENERATION_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_BACKTESTING_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_BACKTESTING_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_RECOMMENDATION_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_RECOMMENDATION_AUDIT.md` |
| `docs/RESEARCH_ARTIFACT_REGISTRY_NO_EXECUTION_AUDIT.md` | `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_EXECUTION_AUDIT.md` |

### Research Artifact Registry Archived Tests

| Original path | Archive path |
| --- | --- |
| `tests/test_research_artifact_registry_no_active_ingestion_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_active_ingestion_audit.py.archived` |
| `tests/test_research_artifact_registry_no_persistent_storage_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_persistent_storage_audit.py.archived` |
| `tests/test_research_artifact_registry_no_upload_download_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_upload_download_audit.py.archived` |
| `tests/test_research_artifact_registry_no_active_ui_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_active_ui_audit.py.archived` |
| `tests/test_research_artifact_registry_no_paper_parsing_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_paper_parsing_audit.py.archived` |
| `tests/test_research_artifact_registry_no_strategy_generation_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_strategy_generation_audit.py.archived` |
| `tests/test_research_artifact_registry_no_backtesting_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_backtesting_audit.py.archived` |
| `tests/test_research_artifact_registry_no_recommendation_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_recommendation_audit.py.archived` |
| `tests/test_research_artifact_registry_no_execution_audit.py` | `tests/archive/prompt_audits/research_artifact_registry/test_research_artifact_registry_no_execution_audit.py.archived` |

Archived tests are historical references, not active suite members. They use
the `.py.archived` suffix and are not collected by pytest.

Verifier keyword lock: Archive Pass 2 archived older phase micro-audit docs
and tests.

## Intentionally Not Archived In Pass 2

These remain active because they either still enforce unique behavior or need a
separate future replacement review:

- Decision Desk granular audit docs/tests
- Retail Dashboard granular audit docs/tests
- Retail Trader Experience granular audit docs/tests
- Strategy Research Workspace boundary, integration, milestone, API surface,
  settings, planning, API contract, display contract, and package behavior tests
- Research Artifact Registry phase, boundary, integration, milestone, API
  surface, settings, planning, API contract, display contract, boundary package,
  and package behavior tests
- Research Artifact Index grouped and milestone docs/tests
- active decision architecture docs/tests
- all grouped docs under `docs/phases/`, `docs/audits/`, and `docs/testing/`
- all grouped tests under `tests/phases/` and `tests/boundaries/`

## Aggressive Deletion Pass

This cleanup pass creates grouped reports under `docs/reports/` and directly
deletes the archived micro-audit files from Archive Pass 1 and Archive Pass 2.
The deleted files were already historical archive members and were not active
product docs or active pytest files.

Grouped reports:

- `docs/reports/DOCS_CONSOLIDATED_REPORT.md`
- `docs/reports/TESTS_CONSOLIDATED_REPORT.md`
- `docs/reports/DELETED_FILES_REPORT.md`
- `docs/reports/SAFETY_COVERAGE_REPORT.md`
- `docs/reports/ACTIVE_TEST_BASELINE_REPORT.md`

Deleted doc families:

- Research Artifact Index Prompt 80 archived micro-audit docs.
- Strategy Research Workspace archived `NO_*` micro-audit docs.
- Research Artifact Registry archived `NO_*` micro-audit docs.

Deleted test families:

- Research Artifact Index Prompt 80 archived micro-audit tests.
- Strategy Research Workspace archived `NO_*` micro-audit tests.
- Research Artifact Registry archived `NO_*` micro-audit tests.

Preserved details location:

- Original path and replacement mapping: `docs/reports/DELETED_FILES_REPORT.md`
- Doc coverage details: `docs/reports/DOCS_CONSOLIDATED_REPORT.md`
- Test coverage and historical function counts: `docs/reports/TESTS_CONSOLIDATED_REPORT.md`
- Safety boundary mapping: `docs/reports/SAFETY_COVERAGE_REPORT.md`
- Active test baseline proof: `docs/reports/ACTIVE_TEST_BASELINE_REPORT.md`

Files intentionally kept active:

- all source code and active package modules
- all API routes
- active decision architecture docs/tests
- grouped phase docs/tests
- grouped audit docs/tests
- top-level control docs
- settings, schema, API, contract, calculation, storage, provider, worker,
  analytics, serialization, health, and package behavior tests

Uncertain files not touched:

- Decision Desk granular audit files
- Retail Dashboard granular audit files
- Retail Trader Experience granular audit files
- active Strategy Research Workspace integration/boundary/milestone files
- active Research Artifact Registry integration/boundary/milestone files

## Not Touched

No product capability, runtime execution path, broker path, market data ingestion path, indexing/search engine, strategy generator, backtest engine, recommendation engine, active UI, database migration, or dependency was added.
