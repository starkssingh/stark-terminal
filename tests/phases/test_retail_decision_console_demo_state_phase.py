from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_decision_console_demo_state_phase_is_recorded() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Prompt 97" in phase_doc
    assert "Demo Data Contract and Static State Model" in phase_doc
    assert "demo_static_state" in phase_doc
    assert "Prompt 97 follows the grouped docs/tests policy" in consolidation
    assert "Current Prompt: 97" in north_star
    assert "Retail Decision Console Status: UI shell skeleton plus demo/static state only" in north_star
    assert "Prompt 97 - Retail Decision Console Demo Data Contract and Static State Model" in prompt_log
    assert "Prompt 98 - Retail Decision Console Static State Wiring into Desktop Shell" in next_phase


def test_prompt_97_added_no_micro_audit_doc_sprawl() -> None:
    top_level_docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
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
    unexpected_tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name not in allowed_tests
    ]

    assert top_level_docs == []
    assert unexpected_tests == []
