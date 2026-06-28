from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_decision_console_phase_doc_records_prompt_100_visual_layout() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")

    assert "Prompt 100 Visual Polish and Section Layout Pass" in phase_doc
    assert "visual_layout_pass" in phase_doc
    assert "layout zones" in phase_doc
    assert "Prompt 101 - Retail Decision Console Static Interaction Placeholders" in phase_doc
    assert "Prompt 100 follows the grouped docs/tests policy" in consolidation


def test_prompt_100_status_docs_recommend_prompt_101() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 100" in north_star
    assert "Retail Decision Console Productization - Visual Layout Pass" in north_star
    assert "Prompt 100 - Retail Decision Console Visual Polish and Section Layout Pass" in prompt_log
    assert "Prompt 101 - Retail Decision Console Static Interaction Placeholders" in next_phase


def test_prompt_100_adds_no_micro_audit_doc_or_test_sprawl() -> None:
    docs = list((ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md"))
    tests = [
        path.name
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
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
    ]

    assert docs == []
    assert tests == []
