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


def test_research_metadata_graph_phase_is_closed_in_canonical_doc() -> None:
    phase_doc = _read("docs/phases/research_metadata_graph.md").lower()

    assert "research metadata graph phase closure" in phase_doc
    assert "phase closure verdict" in phase_doc
    assert "phase closed" in phase_doc
    assert "no graph implementation exists" in phase_doc
    assert "research knowledge map planning and guardrails" in phase_doc


def test_phase_based_policy_is_enforced_for_future_prompts() -> None:
    policy = _read("docs/testing/TEST_POLICY.md").lower()

    assert "future prompts must prefer phase-level tests" in policy
    assert "do not add one test file per forbidden capability" in policy
    assert "use grouped boundary tests for repeated safety rules" in policy
    assert "add feature tests only when actual product behavior changes" in policy
    assert "avoid audit-only prompts unless closing a real phase" in policy


def test_next_phase_and_prompt_log_use_lean_prompt_89_direction() -> None:
    next_phase = _read("docs/NEXT_PHASE_PLAN.md").lower()
    prompt_log = _read("docs/PROMPT_LOG.md").lower()

    assert "prompt 89" in next_phase
    assert "research knowledge map planning and guardrails" in next_phase
    assert "one phase doc" in next_phase
    assert "no micro-audit sprawl" in next_phase
    assert "prompt 88 - b" in prompt_log
    assert "phase closure only" in prompt_log


def test_prompt_88_b_added_no_micro_audit_files() -> None:
    forbidden_paths = [
        ROOT / "docs/RESEARCH_METADATA_GRAPH_MILESTONE_AUDIT.md",
        ROOT / "docs/RESEARCH_METADATA_GRAPH_NEXT_PHASE_PLAN.md",
        ROOT / "tests/phases/test_research_metadata_graph_milestone_phase.py",
        ROOT / "tests/boundaries/test_research_metadata_graph_milestone_boundaries.py",
        ROOT / "tests/boundaries/test_research_metadata_graph_next_phase_readiness.py",
    ]

    assert [path.relative_to(ROOT).as_posix() for path in forbidden_paths if path.exists()] == []


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
