from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_diagnostics_modules_do_not_expose_action_terms() -> None:
    diagnostics_root = ROOT / "packages/analytics/stark_terminal_analytics/diagnostics"
    forbidden_terms = {"buy", "sell", "hold", "watch", "avoid"}

    for path in diagnostics_root.glob("*.py"):
        text = _read(path).lower()
        for term in forbidden_terms:
            assert term not in text, f"{term} found in {path}"


def test_diagnostics_modules_do_not_generate_decision_objects_or_regimes() -> None:
    diagnostics_root = ROOT / "packages/analytics/stark_terminal_analytics/diagnostics"

    for path in diagnostics_root.glob("*.py"):
        text = _read(path)
        lowered = text.lower()
        assert "DecisionObject(" not in text
        assert "def regime" not in lowered
        assert "def generate_signal" not in lowered
        assert "def recommend" not in lowered
        assert "adfuller" not in lowered
        assert "kpss" not in lowered


def test_time_series_diagnostics_route_does_not_imply_signal_or_recommendation_paths() -> None:
    text = _read(ROOT / "apps/api/stark_terminal_api/routes/time_series_diagnostics.py").lower()

    assert "/signals" not in text
    assert "/recommendations" not in text
    assert "/decisions" not in text
    assert "@router.post" not in text


def test_time_series_diagnostics_docs_explicitly_forbid_signals_and_regimes() -> None:
    docs = [
        ROOT / "docs/TIME_SERIES_DIAGNOSTICS_FOUNDATION.md",
        ROOT / "docs/TIME_SERIES_DIAGNOSTICS_SAFETY_BOUNDARY.md",
        ROOT / "docs/STATIONARITY_REGIME_DIAGNOSTICS_DEFERRED.md",
    ]
    combined = "\n".join(_read(path) for path in docs)

    assert "no signals" in combined
    assert "no recommendations" in combined
    assert "no DecisionObject generation" in combined
    assert "no execution APIs" in combined
    assert "regime detection is not implemented" in combined

