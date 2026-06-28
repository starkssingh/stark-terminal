from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/preview_retail_decision_console.py"


def _load_preview_module():
    spec = spec_from_file_location("preview_retail_decision_console_snapshot", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_preview_snapshot_script_imports_safely_and_help_works(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_preview_module()

    with pytest.raises(SystemExit) as exc_info:
        module.main(["--help"])
    output = capsys.readouterr().out

    assert exc_info.value.code == 0
    assert "--no-gui" in output
    assert "--print-snapshot" in output
    assert "--export-snapshot" in output
    assert "--snapshot-format" in output
    assert "Demo/static preview only" in output


def test_preview_snapshot_script_no_gui_still_prints_safe_summary(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_preview_module()

    result = module.main(["--no-gui"])
    output = capsys.readouterr().out

    assert result == 0
    assert "Demo/static preview only — no live data, no recommendations, no execution" in output
    assert "Static interactions:" in output
    assert "Sections:" in output


def test_preview_snapshot_script_print_snapshot_outputs_safe_json(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_preview_module()

    result = module.main(["--print-snapshot"])
    output = capsys.readouterr().out

    assert result == 0
    assert '"stage": "preview_snapshot_export"' in output
    assert '"demo_only": true' in output
    assert '"unavailable": true' in output
    assert '"live_data_enabled": false' in output
    assert '"recommendations_enabled": false' in output
    assert '"confidence_scoring_enabled": false' in output
    assert '"decision_object_generation_enabled": false' in output
    assert '"broker_controls_enabled": false' in output
    assert '"order_buttons_enabled": false' in output
    assert '"execution_enabled": false' in output
    assert "no secrets included" in output
    assert "no credentials included" in output


def test_preview_snapshot_script_writes_local_json_without_runtime_integrations(tmp_path) -> None:
    module = _load_preview_module()
    output_path = tmp_path / "retail_decision_console_snapshot.json"

    result = module.main(
        [
            "--export-snapshot",
            str(output_path),
            "--snapshot-format",
            "json",
        ]
    )
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    forbidden_terms = [
        "requests.",
        "httpx.",
        "urllib",
        "QThread",
        "QTimer",
        "threading",
        "asyncio",
        "client.get",
        "api.get",
        "provider",
        "broker",
        "credential",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
    ]

    assert result == 0
    assert payload["demo_only"] is True
    assert payload["unavailable"] is True
    assert payload["local_only"] is True
    assert payload["read_only"] is True
    assert payload["live_data_enabled"] is False
    assert payload["recommendations_enabled"] is False
    assert payload["action_generation_enabled"] is False
    assert payload["confidence_scoring_enabled"] is False
    assert payload["decision_object_generation_enabled"] is False
    assert payload["broker_controls_enabled"] is False
    assert payload["order_buttons_enabled"] is False
    assert payload["execution_enabled"] is False
    assert payload["no_secrets_marker"] == "no secrets included"
    assert payload["no_credentials_marker"] == "no credentials included"
    for term in forbidden_terms:
        assert term not in source
