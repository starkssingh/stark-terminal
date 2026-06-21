from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from stark_terminal_core.domain.audit import AuditMetadata
from stark_terminal_core.domain.identifiers import AuditId
from stark_terminal_data_platform.db.base import Base, IdMixin


class AuditRecordORM(IdMixin, Base):
    __tablename__ = "audit_records"

    audit_id: Mapped[str] = mapped_column(String(96), unique=True, index=True, nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    model_or_rule_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    @classmethod
    def from_domain(cls, metadata: AuditMetadata) -> AuditRecordORM:
        return cls(
            audit_id=str(metadata.audit_id),
            source=metadata.source,
            source_data_reference=metadata.source_data_reference,
            model_or_rule_version=metadata.model_or_rule_version,
            notes_json=list(metadata.notes),
            created_at=metadata.created_at,
        )

    def to_domain(self) -> AuditMetadata:
        return AuditMetadata(
            audit_id=AuditId(value=self.audit_id),
            created_at=self.created_at,
            source=self.source,
            source_data_reference=self.source_data_reference,
            model_or_rule_version=self.model_or_rule_version,
            notes=list(self.notes_json or []),
        )
