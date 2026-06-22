from __future__ import annotations

from pathlib import Path

from stark_terminal_core.config.settings import Settings


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_synthetic_storage_and_export_docs_are_synthetic_only() -> None:
    text = "\n".join(
        [
            _text("docs/SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md"),
            _text("docs/SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md"),
            _text("docs/SYNTHETIC_STORAGE_EXPORT_AUDIT.md"),
        ]
    )
    required = [
        "synthetic-only",
        "validation-before-storage",
        "validation-before-export",
        "DatasetManifest",
        "no real market data",
        "no real market ingestion",
        "no external calls",
        "no production research lake writes by default",
        "no analytics/signals/decisions",
        "no execution APIs",
    ]
    for phrase in required:
        assert phrase in text


def test_synthetic_storage_settings_do_not_require_live_timescale_for_tests() -> None:
    settings = Settings()
    assert settings.synthetic_ohlcv_storage_allow_sqlite is True
    assert settings.timescale_enabled is False
    assert settings.timescale_create_hypertables is False
    assert settings.synthetic_ohlcv_export_allow_disk_writes is False


def test_synthetic_export_tests_use_temporary_paths_only() -> None:
    export_tests = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "tests").glob("test_synthetic_ohlcv_export*.py")
    )
    assert "tmp_path" in export_tests
    assert "data/lake" not in export_tests
    assert "data/research_artifacts" not in export_tests


def test_storage_export_api_routes_do_not_claim_decision_outputs() -> None:
    text = "\n".join(
        [
            _text("apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py"),
            _text("apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py"),
        ]
    ).lower()
    forbidden = [
        "buy bias",
        "sell bias",
        "recommendation",
        "decisionobject",
        "order placement",
        "broker execution",
    ]
    for term in forbidden:
        assert term not in text
