from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_decision_console_phase_doc_records_prompt_101_static_interactions() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")

    assert "Prompt 101 Static Interaction Placeholders" in phase_doc
    assert "static_interaction_placeholders" in phase_doc
    assert "allowed static interactions" in phase_doc
    assert "forbidden interaction types" in phase_doc
    assert "Prompt 102 - Retail Decision Console Preview Snapshot Export" in phase_doc
    assert "Prompt 101 follows the grouped docs/tests policy" in consolidation


def test_prompt_101_status_docs_recommend_prompt_102() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 101" in north_star
    assert "Retail Decision Console Productization - Static Interaction Placeholders" in north_star
    assert "Prompt 101 - Retail Decision Console Static Interaction Placeholders" in prompt_log
    assert "Prompt 102 - Retail Decision Console Preview Snapshot Export" in next_phase


def test_prompt_101_adds_no_micro_audit_doc_or_test_sprawl() -> None:
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
