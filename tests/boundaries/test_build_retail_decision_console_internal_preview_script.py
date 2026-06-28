from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/build_retail_decision_console_internal_preview.py"


def _load_internal_preview_module():
    spec = spec_from_file_location("build_retail_decision_console_internal_preview", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_internal_preview_script_imports_safely_and_help_works(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_internal_preview_module()

    with pytest.raises(SystemExit) as exc_info:
        module.main(["--help"])
    output = capsys.readouterr().out

    assert exc_info.value.code == 0
    assert "--output-dir" in output
    assert "--clean" in output
    assert "--print-manifest" in output
    assert "Retail Decision Console internal preview" in output


def test_internal_preview_script_writes_local_package_and_prints_manifest(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = _load_internal_preview_module()
    output_dir = tmp_path / "retail_decision_console_internal_preview"

    result = module.main(["--output-dir", str(output_dir), "--clean", "--print-manifest"])
    output = capsys.readouterr().out

    assert result == 0
    assert "Retail Decision Console internal preview" in output
    assert '"stage": "internal_preview_package"' in output
    assert (output_dir / "internal_preview_manifest.json").exists()
    assert (output_dir / "README_INTERNAL_PREVIEW.md").exists()
    assert (output_dir / "preview_snapshot.json").exists()
    assert (output_dir / "preview_snapshot.md").exists()
    assert (output_dir / "no_gui_preview.txt").exists()
    assert (output_dir / "safety_summary.txt").exists()
    assert (output_dir / "manual_acceptance_checklist.md").exists()
    assert (output_dir / "manual_smoke_test.md").exists()
    assert (output_dir / "local_preview_runbook.md").exists()
    assert (output_dir / "local_qa_bundle_runbook.md").exists()
    assert (output_dir / "internal_review_notes.md").exists()


def test_internal_preview_script_clean_replaces_existing_local_output(tmp_path) -> None:
    module = _load_internal_preview_module()
    output_dir = tmp_path / "retail_decision_console_internal_preview"
    output_dir.mkdir()
    sentinel = output_dir / "old.txt"
    sentinel.write_text("old", encoding="utf-8")

    result = module.main(["--output-dir", str(output_dir), "--clean"])

    assert result == 0
    assert not sentinel.exists()
    assert (output_dir / "internal_preview_manifest.json").exists()


def test_internal_preview_script_generated_files_remain_safe(tmp_path) -> None:
    module = _load_internal_preview_module()
    output_dir = tmp_path / "retail_decision_console_internal_preview"

    module.main(["--output-dir", str(output_dir), "--clean"])
    manifest = json.loads((output_dir / "internal_preview_manifest.json").read_text(encoding="utf-8"))
    snapshot = json.loads((output_dir / "preview_snapshot.json").read_text(encoding="utf-8"))
    all_text = "\n".join(path.read_text(encoding="utf-8") for path in output_dir.glob("*") if path.is_file()).casefold()

    assert manifest["demo_only"] is True
    assert manifest["unavailable"] is True
    assert manifest["local_only"] is True
    assert manifest["read_only"] is True
    assert manifest["not_production_ready"] is True
    assert manifest["not_trading_ready"] is True
    assert manifest["not_recommendation_ready"] is True
    assert manifest["not_execution_ready"] is True
    assert snapshot["demo_only"] is True
    assert snapshot["unavailable"] is True
    assert snapshot["live_data_enabled"] is False
    assert snapshot["recommendations_enabled"] is False
    assert snapshot["confidence_scoring_enabled"] is False
    assert snapshot["decision_object_generation_enabled"] is False
    assert snapshot["broker_controls_enabled"] is False
    assert snapshot["order_buttons_enabled"] is False
    assert snapshot["execution_enabled"] is False
    assert "no secrets included" in all_text
    assert "no credentials included" in all_text
    assert "not production ready" in all_text
    assert "not trading ready" in all_text
    assert "not recommendation ready" in all_text
    assert "not execution ready" in all_text


def test_internal_preview_script_source_has_no_runtime_integration_terms() -> None:
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
