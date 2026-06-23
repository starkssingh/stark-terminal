from pathlib import Path
import importlib.util
import sys


ROOT = Path(__file__).resolve().parents[1]


def _run_audit():
    spec = importlib.util.spec_from_file_location("audit_foundation", ROOT / "scripts/audit_foundation.py")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.run_audit()


def test_audit_foundation_script_passes_current_repo() -> None:
    results = _run_audit()
    failures = [result for result in results if not result.passed]

    assert failures == []


def test_verify_foundation_script_includes_data_foundation_artifacts() -> None:
    text = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")

    for phrase in [
        "docs/DATA_FOUNDATION_AUDIT.md",
        "docs/DATA_PERSISTENCE_BOUNDARY.md",
        "docs/SYNTHETIC_DATA_SAFETY_AUDIT.md",
        "docs/DATA_FOUNDATION_NEXT_PHASE.md",
        "tests/test_data_foundation_audit_docs.py",
        "tests/test_data_foundation_no_real_ingestion.py",
        "tests/test_data_foundation_persistence_boundaries.py",
        "tests/test_data_foundation_api_safety.py",
        "tests/test_data_foundation_readiness.py",
        "docs/SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md",
        "docs/TIMESCALE_SYNTHETIC_STORAGE_POLICY.md",
        "docs/SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md",
        "docs/OHLCV_EXPORT_MANIFEST_POLICY.md",
        "docs/PROVIDER_ADAPTER_IMPLEMENTATION_PLAN.md",
        "docs/PROVIDER_GUARDRAIL_POLICY.md",
        "docs/PROVIDER_APPROVAL_WORKFLOW.md",
        "docs/PROVIDER_COMPLIANCE_CHECKLIST.md",
        "docs/LOCAL_SAMPLE_PROVIDER_ADAPTER.md",
        "docs/LOCAL_SAMPLE_PROVIDER_POLICY.md",
        "packages/data_platform/stark_terminal_data_platform/repositories/ohlcv_bars.py",
        "packages/data_platform/stark_terminal_data_platform/services/synthetic_ohlcv_storage.py",
        "packages/data_platform/stark_terminal_data_platform/exports/synthetic_ohlcv.py",
        "apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py",
        "apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py",
        "apps/api/stark_terminal_api/routes/provider_guardrails.py",
        "apps/api/stark_terminal_api/routes/local_sample_provider.py",
    ]:
        assert phrase in text


def test_next_phase_and_status_docs_reflect_prompt_19_readiness() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Local Sample Provider and Local File Provider implemented and audited" in north_star
    assert "Prompt 17 - Data Foundation Audit and Readiness Check" in prompt_log
    assert "Prompt 18 - TimescaleDB Synthetic OHLCV Storage Foundation" in prompt_log
    assert "Prompt 19 - Synthetic OHLCV to Research Lake Export Contract" in prompt_log
    assert "Prompt 20 - Data Provider Adapter Implementation Plan and Guardrails" in prompt_log
    assert "Prompt 21 - Local Sample Provider Adapter v0" in prompt_log
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Real ingestion remains forbidden" in next_phase
