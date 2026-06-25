from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
]


def test_no_frontend_or_desktop_retail_trader_experience_ui_files_added() -> None:
    ui_roots = [
        ROOT / "frontend",
        ROOT / "web",
        ROOT / "ui",
        ROOT / "apps/web",
        ROOT / "apps/frontend",
        ROOT / "apps/desktop",
    ]
    matches: list[str] = []
    for root in ui_roots:
        if root.exists():
            matches.extend(
                str(path.relative_to(ROOT))
                for path in root.rglob("*retail*trader*experience*")
                if path.is_file()
            )
            matches.extend(
                str(path.relative_to(ROOT))
                for path in root.rglob("*retail_trader_experience*")
                if path.is_file()
            )
    assert matches == []


def test_no_active_experience_render_functions_exist() -> None:
    forbidden_names = [
        "build_active_experience",
        "render_active_experience",
        "create_order_button",
        "generate_readiness_status",
    ]
    for root in PACKAGE_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for name in forbidden_names:
                assert f"def {name}" not in text


def test_no_active_ui_docs_remain_explicit() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_ACTIVE_UI_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT.md",
        ]
    )
    assert "no active retail trader experience ui exists" in text
    assert "no frontend trader experience files" in text
    assert "no desktop trader experience files" in text
    assert "contracts/placeholders" in text or "contracts/placeholders/docs/tests" in text
