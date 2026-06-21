import pytest
from pydantic import ValidationError

from stark_terminal_core.domain.decision_object import DecisionObject
from stark_terminal_core.domain.enums import (
    ActionState,
    ConfidenceMethod,
    DecisionSource,
    MarketSegment,
    RiskLevel,
)
from stark_terminal_core.serialization.json import to_jsonable


def test_decision_object_can_be_created_with_defaults() -> None:
    decision = DecisionObject(
        instrument="RELIANCE",
        exchange="NSE",
        segment=MarketSegment.NSE_EQUITY,
        timeframe="1D",
        action_state=ActionState.WATCH,
        confidence=55.5,
        risk=RiskLevel.MEDIUM,
    )

    assert decision.instrument == "RELIANCE"
    assert decision.evidence == []
    assert decision.generated_at.tzinfo is not None


def test_watch_decision_can_have_empty_evidence() -> None:
    decision = DecisionObject(
        instrument="NIFTY",
        exchange="NSE",
        segment=MarketSegment.INDEX,
        timeframe="1D",
        action_state=ActionState.WATCH,
        confidence=50,
        risk=RiskLevel.MEDIUM,
    )

    assert decision.evidence == []


def test_buy_bias_without_evidence_is_rejected() -> None:
    with pytest.raises(ValidationError):
        DecisionObject(
            instrument="RELIANCE",
            exchange="NSE",
            segment=MarketSegment.NSE_EQUITY,
            timeframe="1D",
            action_state=ActionState.BUY_BIAS,
            confidence=70,
            risk=RiskLevel.HIGH,
        )


def test_buy_bias_with_evidence_is_accepted() -> None:
    decision = DecisionObject(
        instrument="RELIANCE",
        exchange="NSE",
        segment=MarketSegment.NSE_EQUITY,
        timeframe="1D",
        action_state=ActionState.BUY_BIAS,
        confidence=70,
        confidence_method=ConfidenceMethod.RULE_SCORE,
        risk=RiskLevel.HIGH,
        evidence=["Price closed above prior range with volume confirmation."],
        decision_source=DecisionSource.RULE_BASED,
        audit_id="audit_test",
        model_or_rule_version="rule-v0",
    )

    serialized = to_jsonable(decision)
    assert serialized["confidence_method"] == "RULE_SCORE"
    assert serialized["decision_source"] == "RULE_BASED"
    assert serialized["audit_id"] == "audit_test"
    assert serialized["model_or_rule_version"] == "rule-v0"


@pytest.mark.parametrize("confidence", [-0.1, 100.1])
def test_decision_object_validates_confidence_range(confidence: float) -> None:
    with pytest.raises(ValidationError):
        DecisionObject(
            instrument="NIFTY",
            exchange="NSE",
            segment=MarketSegment.INDEX,
            timeframe="1D",
            action_state=ActionState.HOLD,
            confidence=confidence,
            risk=RiskLevel.LOW,
        )
