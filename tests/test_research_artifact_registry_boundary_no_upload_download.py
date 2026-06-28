from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py"


def test_boundary_has_no_upload_download_preview_or_fetch_functions() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
    for phrase in [
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
    ]:
        assert phrase not in text


def test_boundary_has_no_upload_download_preview_routes() -> None:
    route_text = ROUTE_PATH.read_text(encoding="utf-8").lower()
    for phrase in ["/upload", "/download", "/preview", "@router.post", "@router.put", "@router.delete"]:
        assert phrase not in route_text
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/research-artifact-registry-boundary"):
            assert "POST" not in methods


def test_boundary_docs_state_no_upload_download_policy() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_UPLOAD_DOWNLOAD_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no file upload/download",
        "no file preview",
        "no local file reads",
        "no external downloads",
        "future prompt and audit required",
    ]:
        assert phrase in text

