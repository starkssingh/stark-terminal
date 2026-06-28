from __future__ import annotations

import json
import shutil
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
)
from stark_terminal_core.retail_decision_console.snapshot_export import (
    RetailDecisionConsolePreviewSnapshot,
    RetailDecisionConsoleSnapshotFormat,
    retail_decision_console_preview_snapshot,
    retail_decision_console_snapshot_to_dict,
    retail_decision_console_snapshot_to_markdown,
)
from stark_terminal_core.retail_decision_console.state_view_model import (
    retail_decision_console_state_view_model,
)


LOCAL_QA_BUNDLE_STAGE = "local_qa_bundle"
QA_BUNDLE_SAFETY_BANNER = (
    "Retail Decision Console QA bundle — demo/static only, "
    "no live data, no recommendations, no execution"
)


class RetailDecisionConsoleQaBundleStatus(StrEnum):
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


class RetailDecisionConsoleQaBundleArtifact(BaseModel):
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
        return non_empty_text(value, "retail decision console QA bundle artifact text")

    @model_validator(mode="after")
    def artifact_must_remain_local_static_safe(self) -> RetailDecisionConsoleQaBundleArtifact:
        if not (self.demo_only and self.unavailable and self.local_only and self.read_only):
            raise ValueError("retail decision console QA bundle artifact must remain demo, unavailable, local, and read-only")
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
            raise ValueError("retail decision console QA bundle artifact cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleQaBundleManifest(BaseModel):
    bundle_id: str = "retail-decision-console-local-qa-bundle-v1"
    created_at_utc: datetime
    service: str = SERVICE_NAME
    stage: str = LOCAL_QA_BUNDLE_STAGE
    schema_version: str = "v1"
    status: RetailDecisionConsoleQaBundleStatus = RetailDecisionConsoleQaBundleStatus.BUILT
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    artifacts: list[RetailDecisionConsoleQaBundleArtifact]
    safety_banner: str = QA_BUNDLE_SAFETY_BANNER
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
        "bundle_id",
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
        return non_empty_text(value, "retail decision console QA bundle manifest text")

    @field_validator("created_at_utc")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def manifest_must_remain_local_static_safe(self) -> RetailDecisionConsoleQaBundleManifest:
        if self.stage != LOCAL_QA_BUNDLE_STAGE:
            raise ValueError("retail decision console QA bundle stage must be local_qa_bundle")
        if not (self.demo_only and self.unavailable and self.local_only and self.read_only):
            raise ValueError("retail decision console QA bundle manifest must remain demo, unavailable, local, and read-only")
        if not self.artifacts:
            raise ValueError("retail decision console QA bundle manifest requires artifacts")
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
            raise ValueError("retail decision console QA bundle manifest cannot enable: " + ", ".join(enabled))
        return self


def _artifact(artifact_id: str, artifact_type: str, path: str) -> RetailDecisionConsoleQaBundleArtifact:
    return RetailDecisionConsoleQaBundleArtifact(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        path=path,
    )


def _default_artifacts() -> list[RetailDecisionConsoleQaBundleArtifact]:
    return [
        _artifact("manifest", "manifest_json", "manifest.json"),
        _artifact("preview-snapshot-json", "preview_snapshot_json", "preview_snapshot.json"),
        _artifact("preview-snapshot-markdown", "preview_snapshot_markdown", "preview_snapshot.md"),
        _artifact("no-gui-preview", "no_gui_preview_text", "no_gui_preview.txt"),
        _artifact("safety-summary", "safety_summary_text", "safety_summary.txt"),
        _artifact("local-preview-runbook", "runbook_copy", "retail_decision_console_local_preview.md"),
        _artifact("manual-smoke-test", "runbook_copy", "retail_decision_console_manual_smoke_test.md"),
    ]


def retail_decision_console_qa_bundle_manifest(
    artifacts: list[RetailDecisionConsoleQaBundleArtifact] | None = None,
    created_at_utc: datetime | None = None,
    status: RetailDecisionConsoleQaBundleStatus = RetailDecisionConsoleQaBundleStatus.BUILT,
) -> RetailDecisionConsoleQaBundleManifest:
    snapshot = retail_decision_console_preview_snapshot()
    return RetailDecisionConsoleQaBundleManifest(
        created_at_utc=created_at_utc or snapshot.generated_at_utc,
        status=status,
        artifacts=artifacts or _default_artifacts(),
    )


def retail_decision_console_no_gui_preview_text() -> str:
    view_model = retail_decision_console_state_view_model()
    lines = [
        QA_BUNDLE_SAFETY_BANNER,
        "Demo/static preview only — no live data, no recommendations, no execution",
        f"Title: {view_model.title}",
        f"Stage: {view_model.stage}",
        f"Layout stage: {view_model.layout.stage}",
        "State: demo-only, unavailable, local-only, read-only",
        f"Static interactions: {len(view_model.interactions)}",
    ]
    lines.extend(
        f"- [{interaction.interaction_type.value}] {interaction.label}: "
        f"{interaction.target_section_id}; demo-only unavailable local-only"
        for interaction in view_model.interactions
    )
    lines.append("Layout zones:")
    for zone in view_model.layout.zones:
        zone_sections = [section for section in view_model.sections if section.layout_zone == zone]
        if zone_sections:
            lines.append(f"- {zone.value}: {len(zone_sections)} sections")
    lines.append(f"Sections: {len(view_model.sections)}")
    zone_order = {zone: index for index, zone in enumerate(view_model.layout.zones)}
    lines.extend(
        f"- [{section.layout_zone.value}] {section.title}: {section.unavailable_demo_label}"
        for section in sorted(view_model.sections, key=lambda item: (zone_order[item.layout_zone], item.layout_priority))
    )
    return "\n".join(lines) + "\n"


def retail_decision_console_qa_safety_summary() -> str:
    lines = [
        QA_BUNDLE_SAFETY_BANNER,
        "Stage: local_qa_bundle",
        "State: demo-only, unavailable, local-only, read-only",
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
        "The QA bundle is a local review artifact, not packaging, deployment, ingestion, decision, or execution infrastructure.",
    ]
    return "\n".join(lines) + "\n"


def _manifest_payload(manifest: RetailDecisionConsoleQaBundleManifest) -> str:
    return json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"


def _resolve_output_dir(output_dir: str | Path) -> Path:
    resolved = Path(output_dir).expanduser().resolve()
    unsafe = {Path("/").resolve(), Path.cwd().resolve(), Path.home().resolve()}
    if resolved in unsafe:
        raise ValueError("retail decision console QA bundle output directory is too broad")
    return resolved


def _ensure_path_under_output(output_dir: Path, path: Path) -> None:
    resolved_output = output_dir.resolve()
    resolved_path = path.resolve()
    if not resolved_path.is_relative_to(resolved_output):
        raise ValueError("retail decision console QA bundle artifact path must stay under output directory")


def _write_text_under_output(output_dir: Path, relative_path: str, payload: str) -> Path:
    output_path = output_dir / relative_path
    _ensure_path_under_output(output_dir, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    return output_path


def _copy_runbook(output_dir: Path, source: Path, relative_path: str) -> Path:
    output_path = output_dir / relative_path
    _ensure_path_under_output(output_dir, output_path)
    output_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return output_path


def build_retail_decision_console_qa_bundle(
    output_dir: str | Path,
    *,
    clean: bool = False,
    created_at_utc: datetime | None = None,
) -> RetailDecisionConsoleQaBundleManifest:
    output_path = _resolve_output_dir(output_dir)
    if clean and output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    snapshot = retail_decision_console_preview_snapshot(generated_at_utc=created_at_utc)
    artifacts = _default_artifacts()
    manifest = retail_decision_console_qa_bundle_manifest(
        artifacts=artifacts,
        created_at_utc=snapshot.generated_at_utc,
        status=RetailDecisionConsoleQaBundleStatus.BUILT,
    )

    _write_text_under_output(
        output_path,
        "preview_snapshot.json",
        json.dumps(retail_decision_console_snapshot_to_dict(snapshot), indent=2, sort_keys=True) + "\n",
    )
    _write_text_under_output(
        output_path,
        "preview_snapshot.md",
        retail_decision_console_snapshot_to_markdown(snapshot),
    )
    _write_text_under_output(output_path, "no_gui_preview.txt", retail_decision_console_no_gui_preview_text())
    _write_text_under_output(output_path, "safety_summary.txt", retail_decision_console_qa_safety_summary())

    root = Path(__file__).resolve().parents[4]
    _copy_runbook(
        output_path,
        root / "docs/runbooks/retail_decision_console_local_preview.md",
        "retail_decision_console_local_preview.md",
    )
    _copy_runbook(
        output_path,
        root / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        "retail_decision_console_manual_smoke_test.md",
    )
    _write_text_under_output(output_path, "manifest.json", _manifest_payload(manifest))

    for artifact in manifest.artifacts:
        _ensure_path_under_output(output_path, output_path / artifact.path)

    return manifest
