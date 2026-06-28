import json
from pathlib import Path

from stark_terminal_core.retail_decision_console.internal_preview_package import (
    build_retail_decision_console_internal_preview_package,
)
from stark_terminal_core.retail_decision_console.internal_preview_smoke import (
    DANGEROUS_FLAG_FIELDS,
    REQUIRED_INTERNAL_PREVIEW_ARTIFACTS,
    RetailDecisionConsoleInternalPreviewSmokeResult,
    smoke_verify_retail_decision_console_internal_preview,
)


FORBIDDEN_ACTIVE_CONTENT = [
    "api_key=",
    "password=",
    "secret=",
    "token=",
    "place_order",
    "connect_broker",
    "execute_trade",
    "order_button_handler",
]


def _all_package_text(output_dir: Path) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in output_dir.iterdir()
        if path.is_file()
    ).casefold()


def test_internal_preview_package_smoke_verification_passes_on_generated_package(tmp_path) -> None:
    output_dir = tmp_path / "internal_preview"
    build_retail_decision_console_internal_preview_package(output_dir, clean=True)

    result = smoke_verify_retail_decision_console_internal_preview(output_dir)

    assert isinstance(result, RetailDecisionConsoleInternalPreviewSmokeResult)
    assert result.passed is True
    assert result.stage == "internal_preview_smoke_verification"
    assert result.demo_only is True
    assert result.unavailable is True
    assert result.local_only is True
    assert result.read_only is True
    assert result.not_production_ready is True
    assert result.not_trading_ready is True
    assert result.not_recommendation_ready is True
    assert result.not_execution_ready is True
    assert all(check.passed for check in result.checks)


def test_internal_preview_smoke_verifies_required_artifacts_and_manifest_safety(tmp_path) -> None:
    output_dir = tmp_path / "internal_preview"
    build_retail_decision_console_internal_preview_package(output_dir, clean=True)
    result = smoke_verify_retail_decision_console_internal_preview(output_dir)
    manifest = json.loads((output_dir / "internal_preview_manifest.json").read_text(encoding="utf-8"))

    for artifact_name in REQUIRED_INTERNAL_PREVIEW_ARTIFACTS:
        assert (output_dir / artifact_name).exists()
        assert any(check.check_id == f"artifact-{artifact_name}" and check.passed for check in result.checks)

    assert manifest["demo_only"] is True
    assert manifest["unavailable"] is True
    assert manifest["local_only"] is True
    assert manifest["read_only"] is True
    assert manifest["not_production_ready"] is True
    assert manifest["not_trading_ready"] is True
    assert manifest["not_recommendation_ready"] is True
    assert manifest["not_execution_ready"] is True
    for field in DANGEROUS_FLAG_FIELDS:
        assert manifest[field] is False
    assert all(value is False for value in manifest["safety_flags"].values())


def test_internal_preview_smoke_package_artifacts_remain_safe_text(tmp_path) -> None:
    output_dir = tmp_path / "internal_preview"
    build_retail_decision_console_internal_preview_package(output_dir, clean=True)
    all_text = _all_package_text(output_dir)

    assert "demo/static only" in all_text
    assert "unavailable" in all_text
    assert "local-only" in all_text
    assert "read-only" in all_text
    assert "not production ready" in all_text
    assert "not trading ready" in all_text
    assert "not recommendation ready" in all_text
    assert "not execution ready" in all_text
    assert "no live data" in all_text
    assert "no recommendations" in all_text
    assert "no confidence scoring" in all_text
    assert "no active decisionobjects" in all_text
    assert "no broker controls" in all_text
    assert "no order buttons" in all_text
    assert "no execution" in all_text
    for forbidden in FORBIDDEN_ACTIVE_CONTENT:
        assert forbidden not in all_text


def test_internal_preview_smoke_reports_missing_package_as_failed(tmp_path) -> None:
    missing_dir = tmp_path / "missing_internal_preview"

    result = smoke_verify_retail_decision_console_internal_preview(missing_dir)

    assert result.passed is False
    assert any(check.check_id == "package-directory-exists" and not check.passed for check in result.checks)
    assert result.execution_enabled is False
