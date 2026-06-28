from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKLIST = ROOT / "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md"


def _checklist() -> str:
    return CHECKLIST.read_text(encoding="utf-8")


def test_manual_acceptance_scope_is_local_demo_only_not_readiness_certification() -> None:
    text = _checklist()

    assert "not production acceptance" in text
    assert "not trading-readiness acceptance" in text
    assert "not recommendation-readiness acceptance" in text
    assert "not execution-readiness acceptance" in text
    assert "Acceptance scope: local demo preview only" in text
    assert "No live data" in text
    assert "No recommendations" in text
    assert "No confidence scoring" in text
    assert "No active DecisionObjects" in text
    assert "No broker controls" in text
    assert "No order buttons" in text
    assert "No execution" in text


def test_manual_acceptance_includes_preflight_preview_and_qa_bundle_commands() -> None:
    text = _checklist()

    for command in [
        ".venv/bin/python -m pip install -e .",
        ".venv/bin/python scripts/audit_foundation.py",
        ".venv/bin/python scripts/verify_foundation.py",
        ".venv/bin/pytest",
        "git diff --check",
        ".venv/bin/python scripts/preview_retail_decision_console.py --help",
        ".venv/bin/python scripts/preview_retail_decision_console.py --no-gui",
        ".venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot",
        ".venv/bin/python scripts/preview_retail_decision_console.py --export-snapshot tmp/preview_snapshots/retail_decision_console_snapshot.json --snapshot-format json",
        ".venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --help",
        ".venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --output-dir tmp/retail_decision_console_qa_bundle --clean --print-manifest",
    ]:
        assert command in text


def test_manual_acceptance_includes_required_visual_safety_snapshot_and_bundle_checks() -> None:
    text = _checklist()

    for section in [
        "Visual Acceptance Checks",
        "Safety Acceptance Checks",
        "Snapshot Acceptance Checks",
        "QA Bundle Acceptance Checks",
    ]:
        assert section in text

    for phrase in [
        "Title visible: `Stark Terminal — Retail Decision Console`",
        "Safety banner visible",
        "Demo/static/unavailable status visible",
        "Layout zones visible",
        "Static interactions visible",
        "No active decision widget appears",
        "No broker/order/execution control appears",
        "No credentials requested",
        "No provider setup requested",
        "No broker setup requested",
        "No background thread/fetch at import",
        "No API call at import",
        "Snapshot says `demo_only: true`",
        "Snapshot says `unavailable: true`",
        "Snapshot says `local_only: true`",
        "Snapshot says `read_only: true`",
        "Dangerous flags are false",
        "`manifest.json` exists",
        "`preview_snapshot.json` exists",
        "`no_gui_preview.txt` exists",
        "`safety_summary.txt` exists",
    ]:
        assert phrase in text


def test_manual_acceptance_includes_failure_criteria_and_verdict_template() -> None:
    text = _checklist()

    assert "Failure Criteria" in text
    assert "Buy, sell, execute, order, or broker active control appears" in text
    assert "Recommendation or confidence appears as output" in text
    assert "Live market data is claimed" in text
    assert "API, provider, or broker call is required" in text
    assert "Credentials are requested" in text
    assert "Execution path appears" in text
    assert "Snapshot contains secrets" in text
    assert "QA bundle contains decision or trading content" in text
    assert "Acceptance Verdict Template" in text
    for field in [
        "Accepted / Rejected:",
        "Date/time:",
        "Commit SHA if available:",
        "Tester:",
        "Commands run:",
        "Observed issues:",
        "Safety verdict:",
        "Next action:",
    ]:
        assert field in text
