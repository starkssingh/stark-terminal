from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_retail_trader_experience_frontend_or_desktop_implementation_added() -> None:
    suspicious_roots = [
        ROOT / "apps/frontend",
        ROOT / "apps/desktop",
    ]
    bad: list[str] = []
    for root in suspicious_roots:
        if not root.exists():
            continue
        for path in root.rglob("*retail*trader*experience*"):
            if path.is_file():
                bad.append(str(path.relative_to(ROOT)))
    assert bad == []


def test_retail_trader_experience_boundary_code_has_no_ui_or_broker_imports() -> None:
    forbidden = [
        "import PySide6",
        "from PySide6",
        "import tkinter",
        "from tkinter",
        "import React",
        "broker_client",
        "create_order",
    ]
    for path in (ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in forbidden:
            assert phrase.lower() not in lowered, f"{path}: {phrase}"


def test_docs_state_no_active_ui_and_no_broker_controls() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_SYSTEM_BOUNDARY_HARDENING.md",
            "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_EXECUTION_POLICY.md",
        ]
    )
    assert "no active ui" in text
    assert "no frontend components" in text
    assert "no desktop components" in text
    assert "no broker controls" in text
