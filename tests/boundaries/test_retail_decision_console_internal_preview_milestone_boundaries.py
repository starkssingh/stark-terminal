from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_internal_preview_milestone_artifacts_exist() -> None:
    required_paths = [
        "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
        "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        "packages/core/stark_terminal_core/retail_decision_console/layout.py",
        "packages/core/stark_terminal_core/retail_decision_console/interactions.py",
        "packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py",
        "packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py",
        "packages/core/stark_terminal_core/retail_decision_console/internal_preview_package.py",
        "packages/core/stark_terminal_core/retail_decision_console/internal_preview_smoke.py",
        "scripts/preview_retail_decision_console.py",
        "scripts/build_retail_decision_console_qa_bundle.py",
        "scripts/build_retail_decision_console_internal_preview.py",
        "scripts/smoke_verify_retail_decision_console_internal_preview.py",
        "docs/runbooks/retail_decision_console_local_preview.md",
        "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        "docs/runbooks/retail_decision_console_local_qa_bundle.md",
        "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
        "docs/runbooks/retail_decision_console_internal_preview_package.md",
        "docs/templates/retail_decision_console_internal_review_notes.md",
    ]

    missing = [path for path in required_paths if not (ROOT / path).exists()]

    assert missing == []


def test_internal_preview_milestone_docs_preserve_not_ready_boundaries() -> None:
    combined = "\n".join(
        _read(path)
        for path in [
            "docs/phases/retail_decision_console.md",
            "docs/SAFETY_AUDIT.md",
            "docs/DATA_POLICY.md",
            "docs/NORTH_STAR.md",
        ]
    )

    for phrase in [
        "internal preview milestone is closed",
        "safe for internal local preview only",
        "not production ready",
        "not trading ready",
        "not recommendation ready",
        "not execution ready",
        "no live data",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
    ]:
        assert phrase in combined


def test_execution_apis_remain_forbidden_after_milestone_closure() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    phase_doc = _read("docs/phases/retail_decision_console.md")
    safety_audit = _read("docs/SAFETY_AUDIT.md")

    assert "Execution APIs: Forbidden" in north_star
    assert "no execution APIs" in phase_doc
    assert "execution APIs" in safety_audit
    assert "All forbidden\nbehavior remains forbidden" in safety_audit


def test_internal_preview_closure_does_not_create_runtime_capability() -> None:
    docs_text = "\n".join(
        _read(path)
        for path in [
            "docs/phases/retail_decision_console.md",
            "docs/SAFETY_AUDIT.md",
            "docs/INFRASTRUCTURE_STACK.md",
            "docs/DATA_POLICY.md",
        ]
    ).casefold()

    assert "no runtime decision capability was added" in docs_text
    assert "not deployment infrastructure" in docs_text
    assert "not production\npackaging infrastructure" in docs_text
    assert "must not be treated as live market intelligence" in docs_text
    assert "must not be used for trading decisions" in docs_text
