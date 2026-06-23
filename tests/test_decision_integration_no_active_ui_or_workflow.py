from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = ROOT / "packages/core/stark_terminal_core"


def test_no_active_frontend_or_retail_dashboard_ui_added() -> None:
    forbidden_paths = [
        ROOT / "apps/desktop/stark_terminal_desktop/decision_dashboard",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard",
        ROOT / "apps/web",
    ]
    for path in forbidden_paths:
        assert not path.exists(), path


def test_decision_display_and_human_review_remain_backend_skeletons() -> None:
    bad: list[str] = []
    for root in [CORE_ROOT / "decision_display", CORE_ROOT / "decision_human_review"]:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for snippet in [
                "pyside6",
                "streamlit",
                "react",
                "def build_active_ui",
                "def render_live",
                "def assign_review_task",
                "def authenticate_reviewer",
                "def send_review_notification",
                "workflow_active: bool = true",
                "active_queue: bool = true",
            ]:
                if snippet in text:
                    bad.append(f"{path.relative_to(ROOT)}:{snippet}")

    assert bad == []


def test_docs_state_no_active_ui_or_workflow_for_integration_readiness() -> None:
    docs_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "docs/DECISION_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
            ROOT / "docs/RETAIL_DASHBOARD_READINESS_PLAN.md",
        ]
    )

    for phrase in [
        "no active UI",
        "no active workflow",
        "Retail Dashboard implementation is not allowed yet",
        "Ready for Retail Dashboard Planning and Guardrails only",
    ]:
        assert phrase in docs_text
