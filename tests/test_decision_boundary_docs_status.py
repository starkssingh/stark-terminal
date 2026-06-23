from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    ROOT / "docs/DECISION_DESK_SYSTEM_BOUNDARY_HARDENING.md",
    ROOT / "docs/DECISION_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    ROOT / "docs/DECISION_ENDPOINT_BOUNDARY_POLICY.md",
    ROOT / "docs/DECISION_MODULE_BOUNDARY_POLICY.md",
    ROOT / "docs/DECISION_CROSS_MODULE_INVARIANTS.md",
    ROOT / "docs/DECISION_BOUNDARY_HARDENING_NO_EXECUTION_POLICY.md",
]


def test_decision_boundary_docs_exist_and_state_boundaries() -> None:
    for path in DOCS:
        assert path.exists(), path

    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)
    for phrase in [
        "Decision Desk System Boundary Hardening",
        "forbidden behavior registry",
        "endpoint boundary policy",
        "module boundary policy",
        "cross-module invariants",
        "no active UI",
        "no active workflow",
        "no readiness-to-trade",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no approval",
        "no override",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_prompt_47_status_docs_are_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 47 - Decision Desk System Boundary Hardening" in prompt_log
    assert "Current Prompt: 47" in north_star
    assert "Completed Prompts: 48 after completion" in north_star
    assert "Decision Desk System Boundary Hardening" in project_map
