from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_decision_console_phase_doc_records_prompt_105_internal_preview_package() -> None:
    phase_doc = _read("docs/phases/retail_decision_console.md")
    runbook = ROOT / "docs/runbooks/retail_decision_console_internal_preview_package.md"
    template = ROOT / "docs/templates/retail_decision_console_internal_review_notes.md"
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")

    assert runbook.exists()
    assert template.exists()
    assert "Prompt 105 Shareable Internal Preview Package" in phase_doc
    assert "Retail Decision Console Shareable Internal Preview Package" in phase_doc
    assert "internal_preview_package" in phase_doc
    assert "internal_preview_manifest.json" in phase_doc
    assert "README_INTERNAL_PREVIEW.md" in phase_doc
    assert "Prompt 105 follows the grouped docs/tests policy" in consolidation


def test_prompt_105_status_docs_recommend_prompt_106() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Current Prompt: 105" in north_star
    assert "Current Milestone: Retail Decision Console Productization - Shareable Internal Preview Package" in north_star
    assert "Prompt 105 - Retail Decision Console Shareable Internal Preview Package" in prompt_log
    assert "Prompt 106 - Retail Decision Console Internal Preview Package Smoke Verification" in next_phase
    assert "Prompt 106 - Retail Decision Console Internal Preview Package Smoke Verification" in prompt_log


def test_prompt_105_adds_no_micro_audit_doc_or_test_sprawl() -> None:
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

    assert docs == []
    assert retail_console_tests <= allowed_tests
