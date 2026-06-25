import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayPaperKind,
)
from stark_terminal_core.strategy_research_workspace_display.papers import (
    StrategyResearchWorkspaceDisplayPaperPlaceholder,
    default_strategy_research_workspace_display_paper_placeholders,
)


def _paper_kwargs(**overrides):
    base = {
        "paper_reference_id": "paper-placeholder-test",
        "paper_kind": StrategyResearchWorkspaceDisplayPaperKind.ARXIV_REFERENCE_VISUAL_PLACEHOLDER,
        "title": "Paper Placeholder",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_paper_placeholder_validates():
    paper = StrategyResearchWorkspaceDisplayPaperPlaceholder(**_paper_kwargs())

    assert paper.display_contract_only is True
    assert paper.rendered_now is False
    assert paper.paper_ingested is False
    assert paper.paper_parsed is False
    assert paper.method_extracted is False
    assert paper.strategy_extracted is False
    assert paper.code_generated is False
    assert paper.backtest_generated is False
    assert paper.recommendation_generated is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("paper_kind", StrategyResearchWorkspaceDisplayPaperKind.UNKNOWN),
        ("display_contract_only", False),
        ("rendered_now", True),
        ("paper_ingested", True),
        ("paper_parsed", True),
        ("method_extracted", True),
        ("strategy_extracted", True),
        ("code_generated", True),
        ("backtest_generated", True),
        ("recommendation_generated", True),
    ],
)
def test_strategy_research_workspace_display_paper_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayPaperPlaceholder(**_paper_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_papers_validate():
    papers = default_strategy_research_workspace_display_paper_placeholders()

    assert papers
    assert all(paper.display_contract_only for paper in papers)
    assert all(not paper.paper_parsed and not paper.strategy_extracted for paper in papers)

