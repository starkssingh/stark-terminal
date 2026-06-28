import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

from stark_terminal_core.retail_decision_console.internal_preview_package import (
    build_retail_decision_console_internal_preview_package,
)


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/smoke_verify_retail_decision_console_internal_preview.py"


def _load_smoke_module():
    spec = spec_from_file_location("smoke_verify_retail_decision_console_internal_preview", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_smoke_script_imports_safely_and_help_works(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_smoke_module()

    with pytest.raises(SystemExit) as exc_info:
        module.main(["--help"])
    output = capsys.readouterr().out

    assert exc_info.value.code == 0
    assert "--package-dir" in output
    assert "--json" in output
    assert "--print-summary" in output
    assert "Retail Decision Console internal preview smoke verification" in output


def test_smoke_script_verifies_generated_package_and_prints_summary(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = _load_smoke_module()
    output_dir = tmp_path / "retail_decision_console_internal_preview"
    build_retail_decision_console_internal_preview_package(output_dir, clean=True)

    result = module.main(["--package-dir", str(output_dir), "--print-summary"])
    output = capsys.readouterr().out.casefold()

    assert result == 0
    assert "retail decision console internal preview smoke verification" in output
    assert "passed: true" in output
    assert "no live data" in output
    assert "no recommendations" in output
    assert "no execution" in output
    assert "internal_preview_manifest.json" in output


def test_smoke_script_json_output_reports_safe_result(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = _load_smoke_module()
    output_dir = tmp_path / "retail_decision_console_internal_preview"
    build_retail_decision_console_internal_preview_package(output_dir, clean=True)

    result = module.main(["--package-dir", str(output_dir), "--json"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert result == 0
    assert payload["passed"] is True
    assert payload["stage"] == "internal_preview_smoke_verification"
    assert payload["demo_only"] is True
    assert payload["unavailable"] is True
    assert payload["local_only"] is True
    assert payload["read_only"] is True
    assert payload["not_production_ready"] is True
    assert payload["not_trading_ready"] is True
    assert payload["not_recommendation_ready"] is True
    assert payload["not_execution_ready"] is True
    assert payload["live_data_enabled"] is False
    assert payload["recommendations_enabled"] is False
    assert payload["confidence_scoring_enabled"] is False
    assert payload["decision_object_generation_enabled"] is False
    assert payload["broker_controls_enabled"] is False
    assert payload["order_buttons_enabled"] is False
    assert payload["execution_enabled"] is False


def test_smoke_script_fails_missing_package_without_enabling_runtime_behavior(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = _load_smoke_module()
    missing_dir = tmp_path / "missing_internal_preview"

    result = module.main(["--package-dir", str(missing_dir), "--print-summary"])
    output = capsys.readouterr().out.casefold()

    assert result == 1
    assert "passed: false" in output
    assert "package-directory-exists" in output
    assert "no execution" in output


def test_smoke_script_source_has_no_runtime_integration_terms() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    forbidden_terms = [
        "requests.",
        "httpx.",
        "urllib",
        "QThread",
        "QTimer",
        "threading",
        "asyncio",
        "subprocess",
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

    assert 'if __name__ == "__main__"' in source
    for term in forbidden_terms:
        assert term not in source
