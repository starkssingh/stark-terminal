from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _run_audit():
    spec = importlib.util.spec_from_file_location("audit_foundation", ROOT / "scripts/audit_foundation.py")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.run_audit()


def test_audit_foundation_passes_prompt_22_invariants() -> None:
    results = _run_audit()
    failures = [result for result in results if not result.passed]
    assert failures == []


def test_verify_foundation_tracks_prompt_18_to_22_artifacts() -> None:
    text = _read("scripts/verify_foundation.py")
    required = [
        "docs/DATA_FOUNDATION_MILESTONE_AUDIT.md",
        "docs/SYNTHETIC_STORAGE_EXPORT_AUDIT.md",
        "docs/PROVIDER_GUARDRAIL_AUDIT.md",
        "docs/LOCAL_SAMPLE_PROVIDER_AUDIT.md",
        "docs/DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md",
        "packages/data_platform/stark_terminal_data_platform/repositories/ohlcv_bars.py",
        "packages/data_platform/stark_terminal_data_platform/exports/synthetic_ohlcv.py",
        "packages/data_platform/stark_terminal_data_platform/providers/guardrails.py",
        "packages/data_platform/stark_terminal_data_platform/providers/local_sample.py",
    ]
    for phrase in required:
        assert phrase in text


def test_prompt_22_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    data_next_phase = _read("docs/DATA_FOUNDATION_NEXT_PHASE.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Quant/Time-Series Analytics Foundation Phase - Numerical Core Contracts" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 28 - Returns and Rolling Window Analytics v0" in data_next_phase
    assert "## Prompt 22 - Data Foundation Milestone Audit" in prompt_log
    assert "Prompt 22 Data Foundation Milestone Audit Artifacts" in project_map


def test_prompt_22_docs_reaffirm_no_real_provider_work() -> None:
    text = "\n".join(
        [
            _read("docs/DATA_FOUNDATION_MILESTONE_AUDIT.md"),
            _read("docs/DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md"),
            _read("docs/SAFETY_AUDIT.md"),
            _read("docs/DATA_POLICY.md"),
        ]
    )
    required = [
        "no real ingestion",
        "no external calls",
        "no scraping",
        "no credentials",
        "no provider SDKs",
        "no analytics/signals/decisions",
        "no execution APIs",
        "Prompt 23",
    ]
    for phrase in required:
        assert phrase in text
