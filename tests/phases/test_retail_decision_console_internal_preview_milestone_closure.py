from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_decision_console_phase_doc_records_prompt_107_milestone_closure() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")

    assert "Prompt 107 Internal Preview Milestone Closure" in phase_doc
    assert "internal_preview_milestone_closed" in phase_doc
    assert "The Retail Decision Console internal preview milestone is closed" in phase_doc
    assert "safe for internal local preview only" in phase_doc
    assert "not production ready" in phase_doc
    assert "not trading ready" in phase_doc
    assert "not recommendation ready" in phase_doc
    assert "not execution ready" in phase_doc


def test_prompt_107_status_docs_recommend_commit_push_and_prompt_108() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 107" in north_star
    assert "Current Milestone: Retail Decision Console Internal Preview - Closed" in north_star
    assert "Next Action: commit/push before starting next phase" in north_star
    assert "Prompt 107 - Retail Decision Console Internal Preview Milestone Closure" in prompt_log
    assert "git commit -m \"Close retail decision console internal preview milestone\"" in next_phase
    assert "Prompt 108 - Retail Decision Console Post-Preview UX Backlog and Next Product Phase Selection" in next_phase


def test_prompt_107_consolidation_policy_and_no_micro_audit_sprawl() -> None:
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    docs = [path.name for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")]
    allowed_tests = {
        "test_retail_decision_console_phase.py",
        "test_retail_decision_console_boundaries.py",
        "test_api_retail_decision_console.py",
        "test_retail_decision_console_ui_shell_phase.py",
        "test_retail_decision_console_ui_shell_boundaries.py",
        "test_desktop_retail_decision_console_shell.py",
        "test_retail_decision_console_demo_state_phase.py",
        "test_retail_decision_console_demo_state_boundaries.py",
        "test_api_retail_decision_console_demo_state.py",
        "test_retail_decision_console_static_state_wiring_phase.py",
        "test_retail_decision_console_static_state_wiring_boundaries.py",
        "test_desktop_retail_decision_console_static_state_wiring.py",
        "test_api_retail_decision_console_static_state_wiring.py",
        "test_retail_decision_console_local_preview_phase.py",
        "test_retail_decision_console_local_preview_boundaries.py",
        "test_preview_retail_decision_console_script.py",
        "test_retail_decision_console_visual_layout_phase.py",
        "test_retail_decision_console_visual_layout_boundaries.py",
        "test_desktop_retail_decision_console_visual_layout.py",
        "test_retail_decision_console_static_interactions_phase.py",
        "test_retail_decision_console_static_interactions_boundaries.py",
        "test_desktop_retail_decision_console_static_interactions.py",
        "test_retail_decision_console_preview_snapshot_phase.py",
        "test_retail_decision_console_preview_snapshot_boundaries.py",
        "test_preview_retail_decision_console_snapshot_script.py",
        "test_retail_decision_console_local_qa_bundle_phase.py",
        "test_retail_decision_console_local_qa_bundle_boundaries.py",
        "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
        "test_retail_decision_console_internal_preview_smoke_phase.py",
        "test_retail_decision_console_internal_preview_smoke_boundaries.py",
        "test_smoke_verify_retail_decision_console_internal_preview_script.py",
        "test_retail_decision_console_internal_preview_milestone_closure.py",
        "test_retail_decision_console_internal_preview_milestone_boundaries.py",
    }
    retail_console_tests = {
        path.name for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
    }

    assert "Prompt 107 follows the grouped docs/tests policy" in consolidation
    assert "No micro-audit sprawl was added for\nPrompt 107" in consolidation
    assert docs == []
    assert retail_console_tests <= allowed_tests


def test_prompt_107_artifact_inventory_is_recorded() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")

    for phrase in [
        "desktop shell module",
        "demo/static state modules",
        "layout module",
        "interaction module",
        "snapshot export module",
        "QA bundle module",
        "internal preview package module",
        "internal preview smoke module",
        "preview script",
        "QA bundle script",
        "internal preview package script",
        "smoke verification script",
        "local preview runbook",
        "manual smoke test runbook",
        "local QA bundle runbook",
        "manual acceptance checklist",
        "internal preview package runbook",
        "internal review notes template",
        "grouped phase, boundary, API, desktop, script, package, smoke, and milestone tests",
    ]:
        assert phrase in phase_doc
