from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Boolean, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from stark_terminal_core.domain.enums import DataProviderType
from stark_terminal_core.domain.identifiers import DataProviderId
from stark_terminal_data_platform.db.base import Base, IdMixin, TimestampMixin


class DataProviderORM(IdMixin, TimestampMixin, Base):
    __tablename__ = "data_providers"
    __table_args__ = (
        UniqueConstraint(
            "name",
            "provider_type",
            "version",
            name="uq_data_providers_identity",
        ),
        Index("ix_data_providers_identity", "name", "provider_type", "version"),
    )

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(32), nullable=False)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    @classmethod
    def from_domain(cls, provider: DataProviderId) -> DataProviderORM:
        return cls(
            name=provider.name,
            provider_type=provider.provider_type.value,
            version=provider.version,
        )

    def to_domain(self) -> DataProviderId:
        return DataProviderId(
            name=self.name,
            provider_type=DataProviderType(self.provider_type),
            version=self.version,
        )
