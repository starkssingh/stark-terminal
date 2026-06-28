from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.internal_preview_package import (
    RetailDecisionConsoleInternalPreviewManifest,
)
from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
)


INTERNAL_PREVIEW_SMOKE_STAGE = "internal_preview_smoke_verification"
INTERNAL_PREVIEW_SMOKE_SAFETY_BANNER = (
    "Retail Decision Console internal preview smoke verification - "
    "demo/static only, no live data, no recommendations, no execution"
)

REQUIRED_INTERNAL_PREVIEW_ARTIFACTS = (
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
)

DANGEROUS_FLAG_FIELDS = (
    "live_data_enabled",
    "recommendations_enabled",
    "action_generation_enabled",
    "confidence_scoring_enabled",
    "decision_object_generation_enabled",
    "broker_controls_enabled",
    "order_buttons_enabled",
    "execution_enabled",
)

READINESS_BLOCK_FIELDS = (
    "not_production_ready",
    "not_trading_ready",
    "not_recommendation_ready",
    "not_execution_ready",
)

REQUIRED_SAFETY_PHRASES = (
    "demo/static only",
    "unavailable",
    "local-only",
    "read-only",
    "not production ready",
    "not trading ready",
    "not recommendation ready",
    "not execution ready",
    "no live data",
    "no recommendations",
    "no confidence scoring",
    "no active decisionobjects",
    "no broker controls",
    "no order buttons",
    "no execution",
)

FORBIDDEN_ACTIVE_CONTENT_MARKERS = (
    "api_key=",
    "password=",
    "secret=",
    "token=",
    "place" "_order",
    "connect" "_broker",
    "execute" "_trade",
    "order_button" "_handler",
    "live_signal:",
    "confidence 70%",
    "recommended:",
    "decisionobject generated",
)


class RetailDecisionConsoleInternalPreviewSmokeCheck(BaseModel):
    check_id: str
    passed: bool
    detail: str

    @field_validator("check_id", "detail")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console smoke check text")


class RetailDecisionConsoleInternalPreviewSmokeResult(BaseModel):
    package_dir: str
    service: str = SERVICE_NAME
    stage: str = INTERNAL_PREVIEW_SMOKE_STAGE
    safety_banner: str = INTERNAL_PREVIEW_SMOKE_SAFETY_BANNER
    passed: bool
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    not_production_ready: bool = True
    not_trading_ready: bool = True
    not_recommendation_ready: bool = True
    not_execution_ready: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    checks: list[RetailDecisionConsoleInternalPreviewSmokeCheck] = Field(default_factory=list)

    @field_validator("package_dir", "service", "stage", "safety_banner")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console smoke result text")

    @model_validator(mode="after")
    def result_must_remain_smoke_verification_safe(self) -> RetailDecisionConsoleInternalPreviewSmokeResult:
        if self.stage != INTERNAL_PREVIEW_SMOKE_STAGE:
            raise ValueError("retail decision console internal preview smoke stage must be internal_preview_smoke_verification")
        if not (self.demo_only and self.unavailable and self.local_only and self.read_only):
            raise ValueError("retail decision console internal preview smoke result must remain demo, unavailable, local, and read-only")
        if not (
            self.not_production_ready
            and self.not_trading_ready
            and self.not_recommendation_ready
            and self.not_execution_ready
        ):
            raise ValueError("retail decision console smoke verification must not imply production, trading, recommendation, or execution readiness")
        enabled = [field for field in DANGEROUS_FLAG_FIELDS if getattr(self, field)]
        if enabled:
            raise ValueError("retail decision console smoke verification cannot enable: " + ", ".join(enabled))
        if not self.checks:
            raise ValueError("retail decision console smoke verification requires checks")
        return self


def _check(check_id: str, passed: bool, detail: str) -> RetailDecisionConsoleInternalPreviewSmokeCheck:
    return RetailDecisionConsoleInternalPreviewSmokeCheck(check_id=check_id, passed=passed, detail=detail)


def _load_manifest(package_dir: Path) -> tuple[dict[str, object], str | None]:
    manifest_path = package_dir / "internal_preview_manifest.json"
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - smoke verification should report all failures.
        return {}, str(exc)
    return payload, None


def _all_artifact_text(package_dir: Path) -> str:
    chunks: list[str] = []
    for artifact_name in REQUIRED_INTERNAL_PREVIEW_ARTIFACTS:
        path = package_dir / artifact_name
        if path.exists() and path.is_file():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks).casefold()


def _artifact_paths_are_under_package(package_dir: Path, manifest_payload: dict[str, object]) -> bool:
    artifacts = manifest_payload.get("artifacts", [])
    if not isinstance(artifacts, list):
        return False
    resolved_package = package_dir.resolve()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            return False
        relative_path = artifact.get("path")
        if not isinstance(relative_path, str):
            return False
        try:
            artifact_path = (package_dir / relative_path).resolve()
        except RuntimeError:
            return False
        if not artifact_path.is_relative_to(resolved_package):
            return False
    return True


def smoke_verify_retail_decision_console_internal_preview(
    package_dir: str | Path,
) -> RetailDecisionConsoleInternalPreviewSmokeResult:
    package_path = Path(package_dir).expanduser().resolve()
    checks: list[RetailDecisionConsoleInternalPreviewSmokeCheck] = []

    checks.append(_check("package-directory-exists", package_path.exists() and package_path.is_dir(), str(package_path)))

    for artifact_name in REQUIRED_INTERNAL_PREVIEW_ARTIFACTS:
        artifact_path = package_path / artifact_name
        checks.append(_check(f"artifact-{artifact_name}", artifact_path.exists() and artifact_path.is_file(), artifact_name))

    manifest_payload, manifest_error = _load_manifest(package_path)
    checks.append(_check("manifest-json-loads", manifest_error is None, manifest_error or "internal_preview_manifest.json loads"))

    manifest_valid = False
    if manifest_payload:
        try:
            RetailDecisionConsoleInternalPreviewManifest(**manifest_payload)
            manifest_valid = True
        except ValueError as exc:
            checks.append(_check("manifest-model-validates", False, str(exc)))
        else:
            checks.append(_check("manifest-model-validates", True, "manifest validates against internal preview contract"))
    else:
        checks.append(_check("manifest-model-validates", False, "manifest payload unavailable"))

    if manifest_valid:
        checks.append(_check("manifest-demo-only", manifest_payload.get("demo_only") is True, "demo_only true"))
        checks.append(_check("manifest-unavailable", manifest_payload.get("unavailable") is True, "unavailable true"))
        checks.append(_check("manifest-local-only", manifest_payload.get("local_only") is True, "local_only true"))
        checks.append(_check("manifest-read-only", manifest_payload.get("read_only") is True, "read_only true"))
        for field in READINESS_BLOCK_FIELDS:
            checks.append(_check(f"manifest-{field}", manifest_payload.get(field) is True, f"{field} true"))
        for field in DANGEROUS_FLAG_FIELDS:
            checks.append(_check(f"manifest-{field}-false", manifest_payload.get(field) is False, f"{field} false"))
        safety_flags = manifest_payload.get("safety_flags", {})
        checks.append(
            _check(
                "manifest-safety-flags-false",
                isinstance(safety_flags, dict) and all(value is False for value in safety_flags.values()),
                "all manifest safety flags false",
            )
        )
        checks.append(
            _check(
                "manifest-artifact-paths-local",
                _artifact_paths_are_under_package(package_path, manifest_payload),
                "manifest artifact paths stay under package directory",
            )
        )

    all_text = _all_artifact_text(package_path)
    for phrase in REQUIRED_SAFETY_PHRASES:
        checks.append(_check(f"safety-phrase-{phrase.replace(' ', '-')}", phrase in all_text, phrase))
    for marker in FORBIDDEN_ACTIVE_CONTENT_MARKERS:
        checks.append(_check(f"forbidden-marker-{marker}", marker not in all_text, marker))

    readme_text = (package_path / "README_INTERNAL_PREVIEW.md").read_text(encoding="utf-8").casefold() if (package_path / "README_INTERNAL_PREVIEW.md").exists() else ""
    checks.append(_check("readme-demo-static-only", "demo/static only" in readme_text, "README states demo/static only"))
    checks.append(_check("readme-not-ready", "not production ready" in readme_text and "not execution ready" in readme_text, "README states not ready"))

    passed = all(check.passed for check in checks)
    return RetailDecisionConsoleInternalPreviewSmokeResult(
        package_dir=str(package_path),
        passed=passed,
        checks=checks,
    )
