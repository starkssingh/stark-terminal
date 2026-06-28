from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_CONSOLIDATION_DOCS = [
    "docs/testing/TEST_POLICY.md",
    "docs/testing/TEST_BASELINE.md",
    "docs/testing/CONSOLIDATION_MAP.md",
    "docs/phases/PHASE_DOCUMENTATION_POLICY.md",
    "docs/phases/research_artifact_index.md",
    "docs/phases/research_artifact_registry.md",
    "docs/phases/strategy_research_workspace.md",
    "docs/phases/active_decision_architecture.md",
    "docs/audits/safety_boundaries.md",
    "docs/audits/no_execution.md",
    "docs/audits/research_artifact_boundaries.md",
    "docs/reports/DOCS_CONSOLIDATED_REPORT.md",
    "docs/reports/TESTS_CONSOLIDATED_REPORT.md",
    "docs/reports/DELETED_FILES_REPORT.md",
    "docs/reports/SAFETY_COVERAGE_REPORT.md",
    "docs/reports/ACTIVE_TEST_BASELINE_REPORT.md",
]

REQUIRED_GROUPED_TESTS = [
    "tests/phases/test_research_artifact_index_phase.py",
    "tests/phases/test_research_artifact_registry_phase.py",
    "tests/phases/test_strategy_research_workspace_phase.py",
    "tests/phases/test_active_decision_architecture_phase.py",
    "tests/boundaries/test_no_execution_boundary.py",
    "tests/boundaries/test_research_artifact_boundaries.py",
    "tests/boundaries/test_documentation_consolidation_policy.py",
]


def test_consolidation_docs_and_grouped_tests_exist() -> None:
    for path in [*REQUIRED_CONSOLIDATION_DOCS, *REQUIRED_GROUPED_TESTS]:
        assert (ROOT / path).exists(), path


def test_test_policy_and_phase_policy_define_new_default() -> None:
    policy = (ROOT / "docs/testing/TEST_POLICY.md").read_text(encoding="utf-8").lower()
    phase_policy = (ROOT / "docs/phases/PHASE_DOCUMENTATION_POLICY.md").read_text(encoding="utf-8").lower()
    map_text = (ROOT / "docs/testing/CONSOLIDATION_MAP.md").read_text(encoding="utf-8").lower()

    required = [
        "tests remain required",
        "grouped by phase and boundary",
        "avoid creating excessive one-off",
        "safety-critical behavior must remain tested",
        "phase-first",
        "prompt logs remain",
        "documentation should support development",
        "granular prompt audit docs are superseded for navigation",
        "archive pass 1",
        "archive pass 2",
        "older phase micro-audit docs and tests",
        "aggressive deletion pass",
        "docs_consolidated_report",
        "tests_consolidated_report",
        "deleted_files_report",
        "safety_coverage_report",
        "active_test_baseline_report",
        "archived tests are historical references",
    ]
    combined = "\n".join([policy, phase_policy, map_text])

    for phrase in required:
        assert phrase in combined


def test_archived_prompt_audit_tests_are_not_pytest_collected() -> None:
    archive_dir = ROOT / "tests/archive/prompt_audits"

    assert archive_dir.exists()
    assert list(archive_dir.rglob("*.py")) == []
    assert (ROOT / "docs/reports/DELETED_FILES_REPORT.md").exists()
