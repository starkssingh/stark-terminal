from __future__ import annotations

import json
import shutil
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
)
from stark_terminal_core.retail_decision_console.qa_bundle import (
    retail_decision_console_no_gui_preview_text,
)
from stark_terminal_core.retail_decision_console.snapshot_export import (
    retail_decision_console_preview_snapshot,
    retail_decision_console_snapshot_to_dict,
    retail_decision_console_snapshot_to_markdown,
)


INTERNAL_PREVIEW_PACKAGE_STAGE = "internal_preview_package"
INTERNAL_PREVIEW_SAFETY_BANNER = (
    "Retail Decision Console internal preview — demo/static only, "
    "no live data, no recommendations, no execution"
)


class RetailDecisionConsoleInternalPreviewStatus(StrEnum):
    READY = "ready"
    BUILT = "built"


def _safe_flag_snapshot() -> dict[str, bool]:
    return {
        "live_data_enabled": False,
        "recommendations_enabled": False,
        "action_generation_enabled": False,
        "confidence_scoring_enabled": False,
        "decision_object_generation_enabled": False,
        "broker_controls_enabled": False,
        "order_buttons_enabled": False,
        "execution_enabled": False,
    }


def _enabled_flags(flags: dict[str, bool]) -> list[str]:
    return [name for name, value in flags.items() if value]


class RetailDecisionConsoleInternalPreviewArtifact(BaseModel):
    artifact_id: str
    artifact_type: str
    path: str
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)

    @field_validator("artifact_id", "artifact_type", "path")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console internal preview artifact text")

    @model_validator(mode="after")
    def artifact_must_remain_internal_preview_safe(self) -> RetailDecisionConsoleInternalPreviewArtifact:
        if not (self.demo_only and self.unavailable and self.local_only and self.read_only):
            raise ValueError("retail decision console internal preview artifact must remain demo, unavailable, local, and read-only")
        enabled = _enabled_flags(
            {
                **self.safety_flags,
                "live data": self.live_data_enabled,
                "recommendations": self.recommendations_enabled,
                "action generation": self.action_generation_enabled,
                "confidence scoring": self.confidence_scoring_enabled,
                "DecisionObject generation": self.decision_object_generation_enabled,
                "broker controls": self.broker_controls_enabled,
                "order buttons": self.order_buttons_enabled,
                "execution": self.execution_enabled,
            }
        )
        if enabled:
            raise ValueError("retail decision console internal preview artifact cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleInternalPreviewManifest(BaseModel):
    package_id: str = "retail-decision-console-internal-preview-v1"
    created_at_utc: datetime
    service: str = SERVICE_NAME
    stage: str = INTERNAL_PREVIEW_PACKAGE_STAGE
    schema_version: str = "v1"
    status: RetailDecisionConsoleInternalPreviewStatus = RetailDecisionConsoleInternalPreviewStatus.BUILT
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    not_production_ready: bool = True
    not_trading_ready: bool = True
    not_recommendation_ready: bool = True
    not_execution_ready: bool = True
    artifacts: list[RetailDecisionConsoleInternalPreviewArtifact]
    safety_banner: str = INTERNAL_PREVIEW_SAFETY_BANNER
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    no_secrets_marker: str = "no secrets included"
    no_credentials_marker: str = "no credentials included"
    no_live_data_marker: str = "no live data included"
    no_recommendation_marker: str = "no recommendations included"
    no_execution_marker: str = "no execution controls included"
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)

    @field_validator(
        "package_id",
        "service",
        "stage",
        "schema_version",
        "safety_banner",
        "no_secrets_marker",
        "no_credentials_marker",
        "no_live_data_marker",
        "no_recommendation_marker",
        "no_execution_marker",
    )
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console internal preview manifest text")

    @field_validator("created_at_utc")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def manifest_must_remain_internal_preview_safe(self) -> RetailDecisionConsoleInternalPreviewManifest:
        if self.stage != INTERNAL_PREVIEW_PACKAGE_STAGE:
            raise ValueError("retail decision console internal preview stage must be internal_preview_package")
        if not (self.demo_only and self.unavailable and self.local_only and self.read_only):
            raise ValueError("retail decision console internal preview manifest must remain demo, unavailable, local, and read-only")
        if not (
            self.not_production_ready
            and self.not_trading_ready
            and self.not_recommendation_ready
            and self.not_execution_ready
        ):
            raise ValueError("retail decision console internal preview must not imply production, trading, recommendation, or execution readiness")
        if not self.artifacts:
            raise ValueError("retail decision console internal preview manifest requires artifacts")
        enabled = _enabled_flags(
            {
                **self.safety_flags,
                "live data": self.live_data_enabled,
                "recommendations": self.recommendations_enabled,
                "action generation": self.action_generation_enabled,
                "confidence scoring": self.confidence_scoring_enabled,
                "DecisionObject generation": self.decision_object_generation_enabled,
                "broker controls": self.broker_controls_enabled,
                "order buttons": self.order_buttons_enabled,
                "execution": self.execution_enabled,
            }
        )
        if enabled:
            raise ValueError("retail decision console internal preview manifest cannot enable: " + ", ".join(enabled))
        return self


def _artifact(
    artifact_id: str,
    artifact_type: str,
    path: str,
) -> RetailDecisionConsoleInternalPreviewArtifact:
    return RetailDecisionConsoleInternalPreviewArtifact(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        path=path,
    )


def _default_artifacts() -> list[RetailDecisionConsoleInternalPreviewArtifact]:
    return [
        _artifact("internal-preview-manifest", "manifest_json", "internal_preview_manifest.json"),
        _artifact("internal-preview-readme", "readme_markdown", "README_INTERNAL_PREVIEW.md"),
        _artifact("preview-snapshot-json", "preview_snapshot_json", "preview_snapshot.json"),
        _artifact("preview-snapshot-markdown", "preview_snapshot_markdown", "preview_snapshot.md"),
        _artifact("no-gui-preview", "no_gui_preview_text", "no_gui_preview.txt"),
        _artifact("safety-summary", "safety_summary_text", "safety_summary.txt"),
        _artifact("manual-acceptance-checklist", "checklist_copy", "manual_acceptance_checklist.md"),
        _artifact("manual-smoke-test", "runbook_copy", "manual_smoke_test.md"),
        _artifact("local-preview-runbook", "runbook_copy", "local_preview_runbook.md"),
        _artifact("local-qa-bundle-runbook", "runbook_copy", "local_qa_bundle_runbook.md"),
        _artifact("internal-review-notes", "review_template_copy", "internal_review_notes.md"),
    ]


def retail_decision_console_internal_preview_manifest(
    artifacts: list[RetailDecisionConsoleInternalPreviewArtifact] | None = None,
    created_at_utc: datetime | None = None,
    status: RetailDecisionConsoleInternalPreviewStatus = RetailDecisionConsoleInternalPreviewStatus.BUILT,
) -> RetailDecisionConsoleInternalPreviewManifest:
    snapshot = retail_decision_console_preview_snapshot()
    return RetailDecisionConsoleInternalPreviewManifest(
        created_at_utc=created_at_utc or snapshot.generated_at_utc,
        status=status,
        artifacts=artifacts or _default_artifacts(),
    )


def retail_decision_console_internal_preview_readme(
    manifest: RetailDecisionConsoleInternalPreviewManifest | None = None,
) -> str:
    current_manifest = manifest or retail_decision_console_internal_preview_manifest()
    artifact_lines = [f"- `{artifact.path}`" for artifact in current_manifest.artifacts]
    lines = [
        "# Retail Decision Console Internal Preview",
        "",
        current_manifest.safety_banner,
        "",
        "This package is for internal review of the current static/demo Retail Decision Console surface.",
        "",
        "It is not production ready, not trading ready, not recommendation ready, and not execution ready.",
        "",
        "## Safety",
        "",
        "- demo/static only",
        "- unavailable",
        "- local-only",
        "- read-only",
        "- no secrets",
        "- no credentials",
        "- no live data",
        "- no recommendations",
        "- no action generation",
        "- no confidence scoring",
        "- no active DecisionObjects",
        "- no broker controls",
        "- no order buttons",
        "- no execution",
        "",
        "## Artifacts",
        "",
        *artifact_lines,
    ]
    return "\n".join(lines) + "\n"


def retail_decision_console_internal_preview_safety_summary() -> str:
    lines = [
        INTERNAL_PREVIEW_SAFETY_BANNER,
        "Stage: internal_preview_package",
        "State: demo-only, unavailable, local-only, read-only",
        "Not production ready.",
        "Not trading ready.",
        "Not recommendation ready.",
        "Not execution ready.",
        "No secrets included.",
        "No credentials included.",
        "No live data included.",
        "No recommendations included.",
        "No action generation included.",
        "No confidence scoring included.",
        "No active DecisionObjects included.",
        "No broker controls included.",
        "No order buttons included.",
        "No execution controls included.",
        "The internal preview package is a local review artifact, not deployment, installer, ingestion, decision, or execution infrastructure.",
    ]
    return "\n".join(lines) + "\n"


def _manifest_payload(manifest: RetailDecisionConsoleInternalPreviewManifest) -> str:
    return json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"


def _resolve_output_dir(output_dir: str | Path) -> Path:
    resolved = Path(output_dir).expanduser().resolve()
    unsafe = {Path("/").resolve(), Path.cwd().resolve(), Path.home().resolve()}
    if resolved in unsafe:
        raise ValueError("retail decision console internal preview output directory is too broad")
    return resolved


def _ensure_path_under_output(output_dir: Path, path: Path) -> None:
    resolved_output = output_dir.resolve()
    resolved_path = path.resolve()
    if not resolved_path.is_relative_to(resolved_output):
        raise ValueError("retail decision console internal preview artifact path must stay under output directory")


def _write_text_under_output(output_dir: Path, relative_path: str, payload: str) -> Path:
    output_path = output_dir / relative_path
    _ensure_path_under_output(output_dir, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    return output_path


def _copy_markdown(output_dir: Path, source: Path, relative_path: str) -> Path:
    output_path = output_dir / relative_path
    _ensure_path_under_output(output_dir, output_path)
    output_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return output_path


def build_retail_decision_console_internal_preview_package(
    output_dir: str | Path,
    *,
    clean: bool = False,
    created_at_utc: datetime | None = None,
) -> RetailDecisionConsoleInternalPreviewManifest:
    output_path = _resolve_output_dir(output_dir)
    if clean and output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    snapshot = retail_decision_console_preview_snapshot(generated_at_utc=created_at_utc)
    artifacts = _default_artifacts()
    manifest = retail_decision_console_internal_preview_manifest(
        artifacts=artifacts,
        created_at_utc=snapshot.generated_at_utc,
        status=RetailDecisionConsoleInternalPreviewStatus.BUILT,
    )

    _write_text_under_output(
        output_path,
        "preview_snapshot.json",
        json.dumps(retail_decision_console_snapshot_to_dict(snapshot), indent=2, sort_keys=True) + "\n",
    )
    _write_text_under_output(output_path, "preview_snapshot.md", retail_decision_console_snapshot_to_markdown(snapshot))
    _write_text_under_output(output_path, "no_gui_preview.txt", retail_decision_console_no_gui_preview_text())
    _write_text_under_output(output_path, "safety_summary.txt", retail_decision_console_internal_preview_safety_summary())
    _write_text_under_output(output_path, "README_INTERNAL_PREVIEW.md", retail_decision_console_internal_preview_readme(manifest))

    root = Path(__file__).resolve().parents[4]
    _copy_markdown(
        output_path,
        root / "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
        "manual_acceptance_checklist.md",
    )
    _copy_markdown(
        output_path,
        root / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        "manual_smoke_test.md",
    )
    _copy_markdown(
        output_path,
        root / "docs/runbooks/retail_decision_console_local_preview.md",
        "local_preview_runbook.md",
    )
    _copy_markdown(
        output_path,
        root / "docs/runbooks/retail_decision_console_local_qa_bundle.md",
        "local_qa_bundle_runbook.md",
    )
    _copy_markdown(
        output_path,
        root / "docs/templates/retail_decision_console_internal_review_notes.md",
        "internal_review_notes.md",
    )
    _write_text_under_output(output_path, "internal_preview_manifest.json", _manifest_payload(manifest))

    for artifact in manifest.artifacts:
        artifact_path = output_path / artifact.path
        _ensure_path_under_output(output_path, artifact_path)
        if not artifact_path.exists():
            raise ValueError(f"retail decision console internal preview artifact was not written: {artifact.path}")

    return manifest
