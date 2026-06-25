import pytest

from stark_terminal_core.strategy_research_workspace.papers import (
    StrategyResearchPaperReferencePlaceholder,
    default_strategy_research_paper_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchPaperReferenceKind


def test_strategy_research_paper_reference_placeholders_validate():
    papers = default_strategy_research_paper_reference_placeholders()

    assert papers
    for paper in papers:
        assert paper.planning_only is True
        assert paper.paper_ingested is False
        assert paper.paper_parsed is False
        assert paper.method_extracted is False
        assert paper.strategy_extracted is False
        assert paper.code_generated is False
        assert paper.backtest_generated is False
        assert paper.recommendation_generated is False


@pytest.mark.parametrize(
    "field",
    [
        "paper_ingested",
        "paper_parsed",
        "method_extracted",
        "strategy_extracted",
        "code_generated",
        "backtest_generated",
        "recommendation_generated",
    ],
)
def test_strategy_research_paper_reference_rejects_generated_or_parsed_flags(field):
    payload = default_strategy_research_paper_reference_placeholders()[0].model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchPaperReferencePlaceholder(**payload)


def test_strategy_research_paper_reference_rejects_unknown_kind():
    payload = default_strategy_research_paper_reference_placeholders()[0].model_dump()
    payload["paper_kind"] = StrategyResearchPaperReferenceKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchPaperReferencePlaceholder(**payload)
