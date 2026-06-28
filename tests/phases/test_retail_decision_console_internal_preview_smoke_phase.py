from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_decision_console_phase_doc_records_prompt_106_internal_preview_smoke() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")
    runbook = _read("docs/runbooks/retail_decision_console_internal_preview_package.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")

    assert "Prompt 106 Internal Preview Package Smoke Verification" in phase_doc
    assert "internal_preview_smoke_verification" in phase_doc
    assert "smoke_verify_retail_decision_console_internal_preview.py" in phase_doc
    assert "smoke verification" in runbook
    assert "Prompt 106 follows the grouped docs/tests policy" in consolidation


def test_prompt_106_status_docs_recommend_prompt_107() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 106" in north_star
    assert "Current Milestone: Retail Decision Console Productization - Internal Preview Smoke Verification" in north_star
    assert "Prompt 106 - Retail Decision Console Internal Preview Package Smoke Verification" in prompt_log
    assert "Prompt 107 - Retail Decision Console Internal Preview Milestone Closure" in next_phase
    assert "Prompt 107 - Retail Decision Console Internal Preview Milestone Closure" in prompt_log


def test_prompt_106_adds_no_micro_audit_doc_or_test_sprawl() -> None:
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
        "test_retail_decision_console_internal_preview_smoke_phase.py",
        "test_retail_decision_console_internal_preview_smoke_boundaries.py",
        "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
    }
    retail_console_tests = {
        path.name for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
    }

    assert docs == []
    assert retail_console_tests <= allowed_tests
