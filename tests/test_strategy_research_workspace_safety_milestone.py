from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_strategy_research_workspace_safety_milestone_references_prompt_66_audit() -> None:
    text = open("docs/STRATEGY_RESEARCH_WORKSPACE_SAFETY_MILESTONE_AUDIT.md", encoding="utf-8").read()

    assert "Prompt 66 safety boundary audit is complete" in text
    assert "unavailable-by-default behavior" in text
    assert "no paper-to-strategy path" in text
    assert "no strategy-to-backtest path" in text
    assert "no research-as-recommendation path" in text
    assert "no research-as-execution-control path" in text
    assert "no live-data-display path" in text


def test_strategy_research_workspace_health_surfaces_keep_dangerous_flags_false() -> None:
    for path in [
        "/strategy-research-workspace/health",
        "/strategy-research-workspace-api/health",
        "/strategy-research-workspace-display/health",
    ]:
        payload = client.get(path).json()
        for key, value in payload.items():
            if key.endswith("_allowed") and key not in {"enabled"}:
                assert value is False, (path, key)
        assert payload["returns_unavailable_by_default"] is True
