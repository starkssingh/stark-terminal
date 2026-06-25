from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DOCS = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_CONTRACT_SKELETON.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_REFERENCE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_UNAVAILABLE_RESPONSES.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_SAFETY_BOUNDARY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_PAPER_PARSING_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_BACKTESTING_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_RECOMMENDATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_EXECUTION_POLICY.md",
]


def test_strategy_research_workspace_api_docs_exist_and_state_boundaries():
    combined = ""
    for doc in DOCS:
        path = ROOT / doc
        assert path.exists(), doc
        combined += path.read_text(encoding="utf-8") + "\n"

    required = [
        "Strategy Research Workspace API",
        "API contract skeleton",
        "unavailable by default",
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no paper ingestion",
        "no paper parsing",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    for phrase in required:
        assert phrase in combined


def test_strategy_research_workspace_api_status_docs_are_updated():
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    readiness = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )

    assert "Prompt 64" in prompt_log
    assert "Current Prompt: 64" in north_star
    assert (
        "Strategy Research Workspace Status: Planning/guardrails and API contract skeleton implemented"
        in north_star
    )
    assert "Strategy Research Workspace API Contract Skeleton" in project_map
    assert "Prompt 65 - Strategy Research Workspace Display Contract Skeleton" in next_phase
    assert "Prompt 65 - Strategy Research Workspace Display Contract Skeleton" in readiness
