from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_active_ui_docs_state_integration_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_ACTIVE_UI_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no rendered artifact cards",
        "no active widgets",
        "no active layout rendering",
        "no artifact browser ui",
        "backend placeholders only",
    ]:
        assert phrase in text


def test_no_active_ui_frontend_desktop_files_or_render_functions_exist() -> None:
    forbidden_defs = [
        "render_artifact_ui",
        "create_frontend_component",
        "create_desktop_widget",
        "render_artifact_card",
        "create_artifact_browser",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)
    for root_name in ["apps", "packages"]:
        for path in (ROOT / root_name).rglob("*research_artifact_registry*"):
            lowered = str(path.relative_to(ROOT)).lower()
            assert "frontend" not in lowered
            assert "desktop" not in lowered
            if path.suffix == ".py":
                assert pattern.search(path.read_text(encoding="utf-8")) is None, str(path.relative_to(ROOT))

