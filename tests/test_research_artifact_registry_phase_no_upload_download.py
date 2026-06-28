from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
]
SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
]


def test_phase_has_no_upload_download_preview_or_file_byte_behavior() -> None:
    route_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in ROUTE_FILES)
    for term in ["/upload", "/download", "/preview", "@router.post"]:
        assert term not in route_text

    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in SOURCE_ROOTS
        for path in root.glob("*.py")
    )
    for phrase in [
        "def upload_file",
        "def download_file",
        "def preview_file",
        "file_bytes:",
        "UploadFile",
        "File(",
        ".read_bytes(",
        ".open(",
    ]:
        assert phrase not in source


def test_phase_no_upload_download_doc_states_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_UPLOAD_DOWNLOAD_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no file upload endpoints",
        "no file download endpoints",
        "no file preview endpoints",
        "no file byte handling",
        "no local file reads",
        "no external downloads",
    ]:
        assert phrase in text
