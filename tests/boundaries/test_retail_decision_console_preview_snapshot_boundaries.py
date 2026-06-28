import json

import pytest

from stark_terminal_core.retail_decision_console.snapshot_export import (
    PREVIEW_SNAPSHOT_STAGE,
    RetailDecisionConsolePreviewSnapshot,
    RetailDecisionConsoleSnapshotFormat,
    retail_decision_console_preview_snapshot,
    retail_decision_console_snapshot_to_dict,
    retail_decision_console_snapshot_to_markdown,
    retail_decision_console_snapshot_to_text,
    write_retail_decision_console_snapshot,
)


def test_preview_snapshot_descriptor_validates_as_demo_unavailable_local_read_only() -> None:
    snapshot = retail_decision_console_preview_snapshot()

    assert snapshot.stage == PREVIEW_SNAPSHOT_STAGE
    assert snapshot.demo_only is True
    assert snapshot.unavailable is True
    assert snapshot.local_only is True
    assert snapshot.read_only is True
    assert snapshot.safety_banner
    assert snapshot.layout_summary
    assert snapshot.section_summary
    assert snapshot.card_summary
    assert snapshot.static_interaction_summary
    assert snapshot.no_secrets_marker == "no secrets included"
    assert snapshot.no_credentials_marker == "no credentials included"


def test_preview_snapshot_dangerous_flags_remain_false() -> None:
    snapshot = retail_decision_console_preview_snapshot()

    assert snapshot.live_data_enabled is False
    assert snapshot.recommendations_enabled is False
    assert snapshot.action_generation_enabled is False
    assert snapshot.confidence_scoring_enabled is False
    assert snapshot.decision_object_generation_enabled is False
    assert snapshot.broker_controls_enabled is False
    assert snapshot.order_buttons_enabled is False
    assert snapshot.execution_enabled is False
    assert all(value is False for value in snapshot.safety_flags.values())


def test_preview_snapshot_rejects_enabled_runtime_behavior() -> None:
    snapshot_dict = retail_decision_console_snapshot_to_dict()
    snapshot_dict["live_data_enabled"] = True

    with pytest.raises(ValueError, match="cannot enable"):
        RetailDecisionConsolePreviewSnapshot(**snapshot_dict)


def test_preview_snapshot_serializes_to_json_markdown_and_text() -> None:
    snapshot = retail_decision_console_preview_snapshot()
    payload = retail_decision_console_snapshot_to_dict(snapshot)
    markdown = retail_decision_console_snapshot_to_markdown(snapshot)
    text = retail_decision_console_snapshot_to_text(snapshot)
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["demo_only"] is True
    assert payload["unavailable"] is True
    assert payload["local_only"] is True
    assert payload["read_only"] is True
    assert payload["no_live_data_marker"] == "no live data included"
    assert payload["no_recommendation_marker"] == "no recommendations included"
    assert payload["no_execution_marker"] == "no execution controls included"
    assert "Retail Decision Console Preview Snapshot" in markdown
    assert "Demo/static shell only" in markdown
    assert "Retail Decision Console Preview Snapshot" in text
    assert "demo-only, unavailable, local-only, read-only" in text
    assert "execution_enabled" in encoded


def test_preview_snapshot_writes_local_files(tmp_path) -> None:
    json_path = tmp_path / "snapshot.json"
    markdown_path = tmp_path / "snapshot.md"
    text_path = tmp_path / "snapshot.txt"

    write_retail_decision_console_snapshot(json_path, snapshot_format=RetailDecisionConsoleSnapshotFormat.JSON)
    write_retail_decision_console_snapshot(markdown_path, snapshot_format=RetailDecisionConsoleSnapshotFormat.MARKDOWN)
    write_retail_decision_console_snapshot(text_path, snapshot_format=RetailDecisionConsoleSnapshotFormat.TEXT)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["demo_only"] is True
    assert payload["unavailable"] is True
    assert payload["live_data_enabled"] is False
    assert payload["recommendations_enabled"] is False
    assert payload["confidence_scoring_enabled"] is False
    assert payload["decision_object_generation_enabled"] is False
    assert payload["broker_controls_enabled"] is False
    assert payload["order_buttons_enabled"] is False
    assert payload["execution_enabled"] is False
    assert "Retail Decision Console Preview Snapshot" in markdown_path.read_text(encoding="utf-8")
    assert "Retail Decision Console Preview Snapshot" in text_path.read_text(encoding="utf-8")
