from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_upload_download_docs_state_integration_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_UPLOAD_DOWNLOAD_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no file upload endpoints",
        "no file download endpoints",
        "no file preview endpoints",
        "no file byte handling",
        "no local file read",
        "no external download",
    ]:
        assert phrase in text


def test_no_upload_download_preview_routes_or_functions_exist() -> None:
    forbidden_defs = [
        "upload_file",
        "download_file",
        "preview_file",
        "read_local_file",
        "fetch_remote_file",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)
    for root in [
        ROOT / "apps/api/stark_terminal_api/routes",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
    ]:
        candidates = root.glob("research_artifact_registry*.py") if root.name == "routes" else root.rglob("*.py")
        for path in candidates:
            text = path.read_text(encoding="utf-8")
            assert pattern.search(text) is None, str(path.relative_to(ROOT))
            lowered = text.lower()
            assert "@router.post" not in lowered
            assert "upload" not in getattr(path, "stem", "").lower()
            assert "download" not in getattr(path, "stem", "").lower()
