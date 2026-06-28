from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/preview_retail_decision_console.py"


def _load_preview_module():
    spec = spec_from_file_location("preview_retail_decision_console", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_preview_script_imports_safely_and_has_main_guard() -> None:
    module = _load_preview_module()
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    assert hasattr(module, "main")
    assert hasattr(module, "_build_parser")
    assert 'if __name__ == "__main__":' in source
    assert module.SAFETY_BANNER == "Demo/static preview only — no live data, no recommendations, no execution"


def test_preview_script_prints_safe_descriptor_summary_without_gui(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_preview_module()

    result = module.main(["--no-gui"])
    output = capsys.readouterr().out

    assert result == 0
    assert "Demo/static preview only — no live data, no recommendations, no execution" in output
    assert "Stark Terminal — Retail Decision Console" in output
    assert "Stage: static_state_wired_shell" in output
    assert "State: demo-only, unavailable, read-only" in output
    assert "Sections:" in output


def test_preview_script_help_is_safe(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load_preview_module()

    with pytest.raises(SystemExit) as exc_info:
        module.main(["--help"])
    output = capsys.readouterr().out

    assert exc_info.value.code == 0
    assert "Demo/static preview only — no live data, no recommendations, no execution" in output
    assert "--no-gui" in output


def test_preview_script_source_has_no_provider_or_broker_integrations() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    forbidden_terms = [
        "requests.",
        "httpx.",
        "urllib",
        "QThread",
        "QTimer",
        "threading",
        "asyncio",
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

    for term in forbidden_terms:
        assert term not in source
