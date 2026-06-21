from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, CheckConstraint, DateTime, Float, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from stark_terminal_core.domain.decision_object import DecisionObject
from stark_terminal_core.domain.enums import (
    ActionState,
    ConfidenceMethod,
    DecisionSource,
    MarketSegment,
    RiskLevel,
)
from stark_terminal_data_platform.db.base import Base, IdMixin, utc_now


class DecisionObjectRecordORM(IdMixin, Base):
    __tablename__ = "decision_object_records"
    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 100",
            name="ck_decision_object_records_confidence_range",
        ),
        Index(
            "ix_decision_records_lookup",
            "instrument",
            "exchange",
            "segment",
            "timeframe",
            "generated_at",
        ),
    )

    instrument: Mapped[str] = mapped_column(String(64), nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), nullable=False)
    segment: Mapped[str] = mapped_column(String(32), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), nullable=False)
    regime: Mapped[str | None] = mapped_column(String(64), nullable=True)
    state: Mapped[str | None] = mapped_column(String(64), nullable=True)
    action_state: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_method: Mapped[str] = mapped_column(String(64), nullable=False)
    risk: Mapped[str] = mapped_column(String(32), nullable=False)
    evidence_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    invalidation: Mapped[str | None] = mapped_column(String(512), nullable=True)
    horizon: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    decision_source: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_id: Mapped[str | None] = mapped_column(String(96), index=True, nullable=True)
    model_or_rule_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    @classmethod
    def from_domain(cls, decision: DecisionObject) -> DecisionObjectRecordORM:
        return cls(
            instrument=decision.instrument,
            exchange=decision.exchange,
            segment=decision.segment.value,
            timeframe=decision.timeframe,
            regime=decision.regime,
            state=decision.state,
            action_state=decision.action_state.value,
            confidence=decision.confidence,
            confidence_method=decision.confidence_method.value,
            risk=decision.risk.value,
            evidence_json=list(decision.evidence),
            invalidation=decision.invalidation,
            horizon=decision.horizon,
            source_data_reference=decision.source_data_reference,
            decision_source=decision.decision_source.value,
            audit_id=decision.audit_id,
            model_or_rule_version=decision.model_or_rule_version,
            generated_at=decision.generated_at,
        )

    def to_domain(self) -> DecisionObject:
        return DecisionObject(
            instrument=self.instrument,
            exchange=self.exchange,
            segment=MarketSegment(self.segment),
            timeframe=self.timeframe,
            regime=self.regime,
            state=self.state,
            action_state=ActionState(self.action_state),
            confidence=self.confidence,
            confidence_method=ConfidenceMethod(self.confidence_method),
            risk=RiskLevel(self.risk),
            evidence=list(self.evidence_json or []),
            invalidation=self.invalidation,
            horizon=self.horizon,
            source_data_reference=self.source_data_reference,
            decision_source=DecisionSource(self.decision_source),
            audit_id=self.audit_id,
            model_or_rule_version=self.model_or_rule_version,
            generated_at=self.generated_at,
        )
