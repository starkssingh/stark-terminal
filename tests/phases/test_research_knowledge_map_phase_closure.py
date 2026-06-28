from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ACTIVE_DECISION_DOCS = [
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
    "docs/phases/active_decision_architecture.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_research_knowledge_map_phase_is_closed_in_canonical_doc() -> None:
    phase_doc = _read("docs/phases/research_knowledge_map.md").lower()

    assert "prompt 93 phase closure" in phase_doc
    assert "phase closure verdict" in phase_doc
    assert "phase closed" in phase_doc
    assert "no active knowledge map implementation exists" in phase_doc
    assert "no active implementation" in phase_doc
    assert "prompt 94 - product surface reorientation and development plan" in phase_doc


def test_phase_based_policy_and_prompt_93_status_are_recorded() -> None:
    policy = _read("docs/testing/TEST_POLICY.md").lower()
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md").lower()
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "phase-based docs/tests only" in policy
    assert "prompt-by-prompt audit/test/doc sprawl" in policy
    assert "one-test-file-per-forbidden-capability pattern" in policy
    assert "audit-only prompts should be rare" in policy
    assert "prompt 93 follows the phase-based docs/tests policy" in consolidation
    assert "test_research_knowledge_map_phase_closure.py" in consolidation
    assert "Current Prompt: 93" in north_star
    assert "Completed Prompts: 94 after completion" in north_star
    assert "Research Knowledge Map Status: phase closed" in north_star
    assert "Prompt 93 - Research Knowledge Map Phase Closure" in prompt_log
    assert "Prompt 94 - Product Surface Reorientation and Development Plan" in next_phase


def test_prompt_93_added_no_micro_audit_sprawl() -> None:
    forbidden_docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    allowed_tests = {
        "test_research_knowledge_map_phase.py",
        "test_research_knowledge_map_boundaries.py",
        "test_api_research_knowledge_map.py",
        "test_research_knowledge_map_api_phase.py",
        "test_research_knowledge_map_api_boundaries.py",
        "test_api_research_knowledge_map_contract.py",
        "test_research_knowledge_map_display_phase.py",
        "test_research_knowledge_map_display_boundaries.py",
        "test_api_research_knowledge_map_display.py",
        "test_research_knowledge_map_safety_phase.py",
        "test_research_knowledge_map_safety_boundaries.py",
        "test_api_research_knowledge_map_safety_surface.py",
        "test_research_knowledge_map_phase_closure.py",
    }
    unexpected_tests = [
        path.name
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name not in allowed_tests
    ]

    assert forbidden_docs == []
    assert unexpected_tests == []


def test_execution_apis_remain_forbidden_and_active_decision_docs_exist() -> None:
    combined = "\n".join(
        [
            _read("docs/NORTH_STAR.md"),
            _read("docs/audits/no_execution.md"),
            _read("docs/audits/safety_boundaries.md"),
            *[_read(path) for path in ACTIVE_DECISION_DOCS],
        ]
    ).lower()

    assert "execution apis remain forbidden" in combined
    assert "execution apis: forbidden" in combined
    assert "decision candidate is not a trade" in combined

    for path in ACTIVE_DECISION_DOCS:
        assert (ROOT / path).exists()
