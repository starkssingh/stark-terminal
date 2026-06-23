from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_time_series_diagnostics_docs_exist_and_state_boundaries() -> None:
    docs = {
        "docs/TIME_SERIES_DIAGNOSTICS_FOUNDATION.md": [
            "Time-Series Diagnostics",
            "monotonicity",
            "duplicate timestamp",
            "gap diagnostics",
            "spacing summary",
            "source reference",
            "timezone-aware",
            "no stationarity tests",
            "no regime detection",
            "no signals",
            "no recommendations",
            "no execution APIs",
            "Mac mini M2",
            "Windows-native",
        ],
        "docs/TIMESTAMP_DIAGNOSTICS_POLICY.md": [
            "Timestamp Diagnostics Policy",
            "timezone-aware",
            "STRICTLY_INCREASING",
            "NON_DECREASING",
            "NON_MONOTONIC",
            "input-order",
            "no trading interpretation",
        ],
        "docs/TIME_SERIES_GAP_DIAGNOSTICS.md": [
            "expected_interval_seconds",
            "Gap Definition",
            "missing count estimate",
            "descriptive-only",
        ],
        "docs/TIME_SERIES_DIAGNOSTICS_SAFETY_BOUNDARY.md": [
            "Gaps are not signals",
            "Irregular intervals are not recommendations",
            "no DecisionObject generation",
            "no execution APIs",
        ],
        "docs/STATIONARITY_REGIME_DIAGNOSTICS_DEFERRED.md": [
            "stationarity",
            "ADF",
            "KPSS",
            "Hurst",
            "autocorrelation",
            "regime detection is not implemented",
        ],
    }

    for path, phrases in docs.items():
        text = _read(path)
        for phrase in phrases:
            assert phrase in text


def test_prompt_32_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    analytics_next = _read("docs/ANALYTICS_NEXT_PHASE_PLAN.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "Time-Series Diagnostics Foundation" in north_star
    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 34 - Regime Feature Preparation Contracts" in analytics_next
    assert "## Prompt 32 - Time-Series Diagnostics Foundation" in prompt_log
    assert "Prompt 32 Time-Series Diagnostics Foundation Artifacts" in project_map


def test_verify_and_audit_scripts_track_prompt_32_artifacts() -> None:
    verify = _read("scripts/verify_foundation.py")
    audit = _read("scripts/audit_foundation.py")

    for phrase in [
        "docs/TIME_SERIES_DIAGNOSTICS_FOUNDATION.md",
        "docs/TIMESTAMP_DIAGNOSTICS_POLICY.md",
        "docs/TIME_SERIES_GAP_DIAGNOSTICS.md",
        "docs/TIME_SERIES_DIAGNOSTICS_SAFETY_BOUNDARY.md",
        "docs/STATIONARITY_REGIME_DIAGNOSTICS_DEFERRED.md",
        "packages/analytics/stark_terminal_analytics/diagnostics/contracts.py",
        "packages/analytics/stark_terminal_analytics/diagnostics/validation.py",
        "packages/analytics/stark_terminal_analytics/diagnostics/calculations.py",
        "apps/api/stark_terminal_api/routes/time_series_diagnostics.py",
    ]:
        assert phrase in verify
        assert phrase in audit

