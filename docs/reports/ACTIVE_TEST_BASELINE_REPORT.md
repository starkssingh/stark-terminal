# Active Test Baseline Report

Status: cleanup/deletion baseline report.

Report set: Aggressive Deletion Pass, DOCS_CONSOLIDATED_REPORT,
TESTS_CONSOLIDATED_REPORT, DELETED_FILES_REPORT, SAFETY_COVERAGE_REPORT, and
ACTIVE_TEST_BASELINE_REPORT.

## Baseline Before Cleanup

- Active pytest baseline before this cleanup/deletion pass: 4782 tests.
- `audit_foundation.py`: passed before this pass.
- `verify_foundation.py`: passed with 4782 tests before this pass.
- Full `.venv/bin/pytest`: passed with 4782 tests before this pass.
- Archived tests were not collected by pytest before this pass.

## Deleted Test Files

This pass deletes 27 previously archived `.py.archived` files under
`tests/archive/prompt_audits/`. They represented 58 historical test functions
but were not active pytest members.

Deleted archived test families:

- Research Artifact Index Prompt 80 micro-audits: 12 files, 18 historical test functions.
- Strategy Research Workspace `NO_*` micro-audits: 6 files, 19 historical test functions.
- Research Artifact Registry `NO_*` micro-audits: 9 files, 21 historical test functions.

## Active Grouped Tests

The active grouped tests remain:

- `tests/phases/test_research_artifact_index_phase.py`
- `tests/phases/test_research_artifact_registry_phase.py`
- `tests/phases/test_strategy_research_workspace_phase.py`
- `tests/phases/test_active_decision_architecture_phase.py`
- `tests/boundaries/test_no_execution_boundary.py`
- `tests/boundaries/test_research_artifact_boundaries.py`
- `tests/boundaries/test_documentation_consolidation_policy.py`
- other grouped phase/boundary tests already present in the repo

## Active Behavior Tests Preserved

No active behavior test was deleted. The pass does not delete settings tests,
schema/model tests, API endpoint tests, contract validation tests,
calculation tests, storage tests, worker tests, provider contract tests,
analytics tests, serialization tests, health endpoint tests, or package
invariant tests.

## Baseline After Cleanup

- Active pytest baseline after cleanup: 4782 tests.
- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4782 tests.
- Full `.venv/bin/pytest` result: passed with 4782 tests.
- `git diff --check` result: passed after final cleanup verification.
- Archived/deleted tests collected by pytest: 0 `.py` files under `tests/archive`.

## Intentional Count Change Explanation

The expected active pytest count is unchanged at 4782 because deleted tests
were already `.py.archived` historical references and were not collected by
pytest before deletion. If verification reports a different count, the delta
must be investigated and documented before completion.

## Prompt 82 Expected Baseline

Pre-Prompt 82 active pytest baseline: 4782 tests.

Prompt 82 adds grouped phase/API/boundary tests for Research Artifact Index
system boundary hardening. It does not intentionally delete, archive, skip,
xfail, or consolidate active tests. The active pytest count should remain at
least 4782 plus the new grouped tests after verification.

## Prompt 82 Verified Baseline

- Focused Prompt 82 pytest: 10 passed.
- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4792 tests.
- Full `.venv/bin/pytest` result: passed with 4792 tests.
- `git diff --check` result: passed.

Prompt 82 increases the active pytest baseline from 4782 to 4792 tests. The
increase comes from grouped system-boundary phase, boundary, and API tests.

## Prompt 83 Expected Baseline

Pre-Prompt 83 active pytest baseline: 4792 tests.

Prompt 83 adds grouped phase/API-display-integration/boundary tests for
Research Artifact Index API/display integration readiness. It does not
intentionally delete, archive, skip, xfail, or consolidate active tests. The
active pytest count should remain at least 4792 plus the new grouped tests
after verification.

## Prompt 83 Verified Baseline

- Focused Prompt 83 pytest: 8 passed.
- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4800 tests.
- Full `.venv/bin/pytest` result: passed with 4800 tests.
- `git diff --check` result: passed.

Prompt 83 increases the active pytest baseline from 4792 to 4800 tests. The
increase comes from grouped API/display integration readiness phase, boundary,
and API consistency tests.

## Prompt 84 Expected Baseline

Pre-Prompt 84 active pytest baseline: 4800 tests.

Prompt 84 adds grouped phase/boundary/API tests for Research Metadata Graph
Planning and Guardrails. It does not intentionally delete, archive, skip,
xfail, or consolidate active tests. The active pytest count should remain at
least 4800 plus the new grouped tests after verification.

## Prompt 84 Verified Baseline

- Focused Prompt 84 pytest: 10 passed.
- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4810 tests.
- Full `.venv/bin/pytest` result: passed with 4810 tests.
- `git diff --check` result: passed.

Prompt 84 increases the active pytest baseline from 4800 to 4810 tests. The
increase comes from grouped Research Metadata Graph phase, boundary, and API
tests.

## Prompt 85 Expected Baseline

Pre-Prompt 85 active pytest baseline: 4810 tests.

Prompt 85 adds grouped phase/boundary/API tests for Research Metadata Graph
API Contract Skeleton. It does not intentionally delete, archive, skip, xfail,
or consolidate active tests. The active pytest count should remain at least
4810 plus the new grouped tests after verification.

## Prompt 85 Verified Baseline

- Focused Prompt 85 pytest: 15 passed.
- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4820 tests.
- Full `.venv/bin/pytest` result: passed with 4820 tests.
- `git diff --check` result: passed.

Prompt 85 increases the active pytest baseline from 4810 to 4820 tests. The
increase comes from grouped Research Metadata Graph API phase, boundary, and
API contract tests.

## Prompt 86 Expected Baseline

Pre-Prompt 86 active pytest baseline: 4820 tests.

Prompt 86 adds grouped phase/boundary/API tests for Research Metadata Graph
Display Contract Skeleton. It does not intentionally delete, archive, skip,
xfail, or consolidate active tests. The active pytest count should remain at
least 4820 plus the new grouped tests after verification.

## Prompt 86 Verified Baseline

- `verify_foundation.py` result: passed with 4829 tests.
- Full `.venv/bin/pytest` result: passed with 4829 tests.
- `audit_foundation.py` result: passed.
- Editable install result: passed.
- `git diff --check` result: passed.

Prompt 86 increases the active pytest baseline from 4820 to 4829 tests. The
increase comes from grouped Research Metadata Graph display phase, boundary,
and API display tests. No active tests were deleted, archived, skipped, xfailed,
or weakened.

## Prompt 87 Expected Baseline

Pre-Prompt 87 active pytest baseline: 4829 tests.

Prompt 87 adds grouped phase/boundary/API surface tests for Research Metadata
Graph Safety Boundary Audit. It does not intentionally delete, archive, skip,
xfail, or consolidate active tests. The active pytest count should remain at
least 4829 plus the new grouped tests after verification.

## Prompt 87 Verified Baseline

- Focused Prompt 87 pytest: 32 passed.
- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4838 tests.
- Full `.venv/bin/pytest` result: passed with 4838 tests.

Prompt 87 increases the active pytest baseline from 4829 to 4838 tests. The
increase comes from grouped Research Metadata Graph safety audit phase,
boundary, and API safety surface tests. No active tests were deleted,
archived, skipped, xfailed, or weakened.

## Prompt 88-B Expected Baseline

Pre-Prompt 88 active pytest baseline: 4838 tests.

Prompt 88-B adds one grouped Research Metadata Graph phase-closure test file.
It removes the untracked Prompt 88 milestone-audit artifacts from this working
turn and keeps the active suite phase-based. The active pytest count should
remain at least 4838 plus the new grouped closure coverage after verification.

## Prompt 88-B Verified Baseline

- `audit_foundation.py` result: passed.
- `verify_foundation.py` result: passed with 4843 tests.
- Full `.venv/bin/pytest` result: passed with 4843 tests.
- `git diff --check` result: passed.

Coverage is preserved by existing Research Metadata Graph grouped phase/API/
display/safety tests and the new phase-closure test. No active tests are
skipped, xfailed, or weakened.
