# Prompt Audit Test Archive

This directory preserves superseded granular prompt-level audit tests.

Archived tests are historical references only and are not active pytest suite
members. Test files in this archive use the `.py.archived` suffix so pytest
does not collect them.

Active safety coverage is now provided by grouped tests under:

- `tests/phases/`
- `tests/boundaries/`

Archive Pass 1 moved obvious Research Artifact Index Prompt 80 micro-audit
tests after grouped phase and boundary tests were verified.

Archive Pass 2 adds phase subfolders for older Strategy Research Workspace and
Research Artifact Registry `NO_*` micro-audit tests after grouped phase and
boundary tests were verified. Archived tests preserve original content with the
`.py.archived` suffix and must not be collected by pytest.

The aggressive grouped report cleanup later deletes the superseded archived
test files after preserving their details in `docs/reports/`. This archive
directory may contain only this README after that cleanup, and it must contain
no `.py` files.
