from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_68_DOCS = [
    "STRATEGY_RESEARCH_WORKSPACE_SYSTEM_BOUNDARY_HARDENING.md",
    "STRATEGY_RESEARCH_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "STRATEGY_RESEARCH_ENDPOINT_BOUNDARY_POLICY.md",
    "STRATEGY_RESEARCH_MODULE_BOUNDARY_POLICY.md",
    "STRATEGY_RESEARCH_CROSS_MODULE_INVARIANTS.md",
    "STRATEGY_RESEARCH_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "STRATEGY_RESEARCH_BOUNDARY_NO_PAPER_PARSING_POLICY.md",
    "STRATEGY_RESEARCH_BOUNDARY_NO_STRATEGY_GENERATION_POLICY.md",
    "STRATEGY_RESEARCH_BOUNDARY_NO_BACKTESTING_POLICY.md",
    "STRATEGY_RESEARCH_BOUNDARY_NO_EXECUTION_POLICY.md",
]


def test_strategy_research_workspace_boundary_docs_exist_and_state_scope() -> None:
    required_phrases = [
        "boundary-hardening-only",
        "no active UI",
        "no frontend",
        "no desktop",
        "no paper ingestion",
        "no paper parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no signal",
        "no backtesting",
        "no optimization",
        "no recommendation generation",
        "no action generation",
        "no confidence",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker",
        "no execution APIs",
        "future prompt",
        "audit-before-unlock",
        "Mac mini M2",
        "Windows-native",
    ]
    combined = ""
    for doc_name in PROMPT_68_DOCS:
        path = ROOT / "docs" / doc_name
        assert path.exists(), doc_name
        combined += "\n" + path.read_text(encoding="utf-8")

    lowered = combined.lower()
    for phrase in required_phrases:
        assert phrase.lower() in lowered, phrase


def test_strategy_research_workspace_boundary_status_docs_reflect_prompt_68() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 72 after completion" in north_star
    assert "Research Artifact Registry Planning Phase - API Contract Skeleton" in north_star
    assert "strategy_research_workspace_boundary" in project_map
    assert "Strategy Research Workspace System Boundary Hardening" in project_map
    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in prompt_log


def test_strategy_research_workspace_boundary_verifier_and_audit_include_prompt_68() -> None:
    verify = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")
    audit = (ROOT / "scripts/audit_foundation.py").read_text(encoding="utf-8")

    for artifact in [
        "STRATEGY_RESEARCH_WORKSPACE_SYSTEM_BOUNDARY_HARDENING.md",
        "STRATEGY_RESEARCH_FORBIDDEN_BEHAVIOR_REGISTRY.md",
        "strategy_research_workspace_boundary/forbidden.py",
        "strategy_research_workspace_boundary.py",
    ]:
        assert artifact in verify
        assert artifact in audit
