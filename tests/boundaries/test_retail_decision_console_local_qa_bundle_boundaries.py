import json
from pathlib import Path

import pytest

from stark_terminal_core.retail_decision_console.qa_bundle import (
    LOCAL_QA_BUNDLE_STAGE,
    RetailDecisionConsoleQaBundleManifest,
    build_retail_decision_console_qa_bundle,
    retail_decision_console_qa_bundle_manifest,
)


FORBIDDEN_CONTENT = [
    "api_key=",
    "password=",
    "secret=",
    "token=",
    "live signal",
    "strong buy",
    "strong sell",
    "ready to trade",
    "place_order",
    "connect_broker",
    "execute_trade",
]


def _all_generated_text(output_dir: Path) -> str:
    generated = [
        "manifest.json",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
    ]
    return "\n".join((output_dir / name).read_text(encoding="utf-8") for name in generated)


def test_qa_bundle_manifest_validates_as_demo_unavailable_local_read_only() -> None:
    manifest = retail_decision_console_qa_bundle_manifest()

    assert manifest.stage == LOCAL_QA_BUNDLE_STAGE
    assert manifest.demo_only is True
    assert manifest.unavailable is True
    assert manifest.local_only is True
    assert manifest.read_only is True
    assert manifest.artifacts
    assert manifest.no_secrets_marker == "no secrets included"
    assert manifest.no_credentials_marker == "no credentials included"


def test_qa_bundle_manifest_dangerous_flags_remain_false() -> None:
    manifest = retail_decision_console_qa_bundle_manifest()

    assert manifest.live_data_enabled is False
    assert manifest.recommendations_enabled is False
    assert manifest.action_generation_enabled is False
    assert manifest.confidence_scoring_enabled is False
    assert manifest.decision_object_generation_enabled is False
    assert manifest.broker_controls_enabled is False
    assert manifest.order_buttons_enabled is False
    assert manifest.execution_enabled is False
    assert all(value is False for value in manifest.safety_flags.values())
    assert all(value is False for artifact in manifest.artifacts for value in artifact.safety_flags.values())


def test_qa_bundle_manifest_rejects_enabled_runtime_behavior() -> None:
    manifest_dict = retail_decision_console_qa_bundle_manifest().model_dump(mode="json")
    manifest_dict["live_data_enabled"] = True

    with pytest.raises(ValueError, match="cannot enable"):
        RetailDecisionConsoleQaBundleManifest(**manifest_dict)


def test_build_qa_bundle_writes_expected_local_artifacts(tmp_path) -> None:
    output_dir = tmp_path / "qa_bundle"
    manifest = build_retail_decision_console_qa_bundle(output_dir, clean=True)

    expected_files = {
        "manifest.json",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
        "retail_decision_console_local_preview.md",
        "retail_decision_console_manual_smoke_test.md",
    }
    written_files = {path.name for path in output_dir.iterdir() if path.is_file()}

    assert expected_files <= written_files
    assert {artifact.path for artifact in manifest.artifacts} == expected_files
    for artifact in manifest.artifacts:
        artifact_path = (output_dir / artifact.path).resolve()
        assert artifact_path.is_relative_to(output_dir.resolve())


def test_qa_bundle_artifacts_preserve_demo_safety_and_no_sensitive_content(tmp_path) -> None:
    output_dir = tmp_path / "qa_bundle"
    build_retail_decision_console_qa_bundle(output_dir, clean=True)
    manifest_payload = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    snapshot_payload = json.loads((output_dir / "preview_snapshot.json").read_text(encoding="utf-8"))
    all_text = _all_generated_text(output_dir).casefold()

    assert manifest_payload["stage"] == LOCAL_QA_BUNDLE_STAGE
    assert manifest_payload["demo_only"] is True
    assert manifest_payload["unavailable"] is True
    assert manifest_payload["local_only"] is True
    assert manifest_payload["read_only"] is True
    assert snapshot_payload["demo_only"] is True
    assert snapshot_payload["unavailable"] is True
    assert snapshot_payload["local_only"] is True
    assert snapshot_payload["read_only"] is True
    assert "no live data" in all_text
    assert "no recommendations" in all_text
    assert "no confidence scoring" in all_text
    assert "no active decisionobjects" in all_text
    assert "no broker controls" in all_text
    assert "no order buttons" in all_text
    assert "no execution" in all_text
    for forbidden in FORBIDDEN_CONTENT:
        assert forbidden not in all_text
