import json
from pathlib import Path

import pytest

from stark_terminal_core.retail_decision_console.internal_preview_package import (
    INTERNAL_PREVIEW_PACKAGE_STAGE,
    RetailDecisionConsoleInternalPreviewManifest,
    build_retail_decision_console_internal_preview_package,
    retail_decision_console_internal_preview_manifest,
)


FORBIDDEN_CONTENT = [
    "api_key=",
    "password=",
    "secret=",
    "token=",
    "place_order",
    "connect_broker",
    "execute_trade",
]


def _all_generated_text(output_dir: Path) -> str:
    generated = [
        "internal_preview_manifest.json",
        "README_INTERNAL_PREVIEW.md",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
        "manual_acceptance_checklist.md",
        "manual_smoke_test.md",
        "local_preview_runbook.md",
        "local_qa_bundle_runbook.md",
        "internal_review_notes.md",
    ]
    return "\n".join((output_dir / name).read_text(encoding="utf-8") for name in generated)


def test_internal_preview_manifest_validates_as_demo_unavailable_local_read_only_not_ready() -> None:
    manifest = retail_decision_console_internal_preview_manifest()

    assert manifest.stage == INTERNAL_PREVIEW_PACKAGE_STAGE
    assert manifest.demo_only is True
    assert manifest.unavailable is True
    assert manifest.local_only is True
    assert manifest.read_only is True
    assert manifest.not_production_ready is True
    assert manifest.not_trading_ready is True
    assert manifest.not_recommendation_ready is True
    assert manifest.not_execution_ready is True
    assert manifest.artifacts


def test_internal_preview_manifest_dangerous_flags_remain_false() -> None:
    manifest = retail_decision_console_internal_preview_manifest()

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


def test_internal_preview_manifest_rejects_runtime_or_readiness_enablement() -> None:
    manifest_dict = retail_decision_console_internal_preview_manifest().model_dump(mode="json")
    manifest_dict["live_data_enabled"] = True

    with pytest.raises(ValueError, match="cannot enable"):
        RetailDecisionConsoleInternalPreviewManifest(**manifest_dict)

    manifest_dict = retail_decision_console_internal_preview_manifest().model_dump(mode="json")
    manifest_dict["not_execution_ready"] = False

    with pytest.raises(ValueError, match="must not imply"):
        RetailDecisionConsoleInternalPreviewManifest(**manifest_dict)


def test_build_internal_preview_package_writes_expected_local_artifacts(tmp_path) -> None:
    output_dir = tmp_path / "internal_preview"
    manifest = build_retail_decision_console_internal_preview_package(output_dir, clean=True)

    expected_files = {
        "internal_preview_manifest.json",
        "README_INTERNAL_PREVIEW.md",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
        "manual_acceptance_checklist.md",
        "manual_smoke_test.md",
        "local_preview_runbook.md",
        "local_qa_bundle_runbook.md",
        "internal_review_notes.md",
    }
    written_files = {path.name for path in output_dir.iterdir() if path.is_file()}

    assert expected_files <= written_files
    assert {artifact.path for artifact in manifest.artifacts} == expected_files
    for artifact in manifest.artifacts:
        artifact_path = (output_dir / artifact.path).resolve()
        assert artifact_path.is_relative_to(output_dir.resolve())


def test_internal_preview_artifacts_preserve_safety_and_no_sensitive_content(tmp_path) -> None:
    output_dir = tmp_path / "internal_preview"
    build_retail_decision_console_internal_preview_package(output_dir, clean=True)
    manifest_payload = json.loads((output_dir / "internal_preview_manifest.json").read_text(encoding="utf-8"))
    snapshot_payload = json.loads((output_dir / "preview_snapshot.json").read_text(encoding="utf-8"))
    all_text = _all_generated_text(output_dir).casefold()

    assert manifest_payload["stage"] == INTERNAL_PREVIEW_PACKAGE_STAGE
    assert manifest_payload["demo_only"] is True
    assert manifest_payload["unavailable"] is True
    assert manifest_payload["local_only"] is True
    assert manifest_payload["read_only"] is True
    assert manifest_payload["not_production_ready"] is True
    assert manifest_payload["not_trading_ready"] is True
    assert manifest_payload["not_recommendation_ready"] is True
    assert manifest_payload["not_execution_ready"] is True
    assert snapshot_payload["demo_only"] is True
    assert snapshot_payload["unavailable"] is True
    assert "no live data" in all_text
    assert "no recommendations" in all_text
    assert "no confidence scoring" in all_text
    assert "no active decisionobjects" in all_text
    assert "no broker controls" in all_text
    assert "no order buttons" in all_text
    assert "no execution" in all_text
    assert "not production ready" in all_text
    assert "not trading ready" in all_text
    assert "not recommendation ready" in all_text
    assert "not execution ready" in all_text
    for forbidden in FORBIDDEN_CONTENT:
        assert forbidden not in all_text
