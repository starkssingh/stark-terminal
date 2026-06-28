from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_local_preview_runbooks_keep_preview_non_executive() -> None:
    combined = "\n".join(
        [
            _read("docs/runbooks/retail_decision_console_local_preview.md"),
            _read("docs/runbooks/retail_decision_console_manual_smoke_test.md"),
        ]
    )
    required = [
        "no live data",
        "no recommendations",
        "no confidence scoring",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution",
        "demo/static",
        "unavailable",
    ]

    for phrase in required:
        assert phrase in combined


def test_local_preview_runbooks_include_preflight_and_manual_safety_checklist() -> None:
    combined = "\n".join(
        [
            _read("docs/runbooks/retail_decision_console_local_preview.md"),
            _read("docs/runbooks/retail_decision_console_manual_smoke_test.md"),
        ]
    )
    required = [
        ".venv/bin/python -m pip install -e .",
        ".venv/bin/python scripts/audit_foundation.py",
        ".venv/bin/python scripts/verify_foundation.py",
        ".venv/bin/pytest",
        "git diff --check",
        ".venv/bin/python scripts/preview_retail_decision_console.py",
        "No buy button exists",
        "No sell button exists",
        "No execute button exists",
        "No place order button exists",
        "No broker connect button exists",
        "No active recommendation is shown",
        "No confidence score is shown",
        "No active DecisionObject is shown",
        "No execution controls exist",
    ]

    for phrase in required:
        assert phrase in combined


def test_prompt_99_does_not_add_runtime_decision_capability() -> None:
    script = _read("scripts/preview_retail_decision_console.py")
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QThread",
        "QTimer",
        "threading",
        "asyncio",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "generate_recommendation",
        "generate_action",
        "score_confidence",
        "generate_decision_object",
    ]

    for term in forbidden:
        assert term not in script
