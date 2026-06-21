from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import DataProviderType, Exchange, MarketSegment
from stark_terminal_core.domain.identifiers import AuditId, DataProviderId, InstrumentId


def test_instrument_id_normalizes_symbol_uppercase() -> None:
    instrument_id = InstrumentId(
        symbol=" reliance ",
        exchange=Exchange.NSE,
        segment=MarketSegment.NSE_EQUITY,
    )

    assert instrument_id.symbol == "RELIANCE"


def test_instrument_id_string_representation_is_stable() -> None:
    instrument_id = InstrumentId(
        symbol="RELIANCE",
        exchange=Exchange.NSE,
        segment=MarketSegment.NSE_EQUITY,
    )

    assert str(instrument_id) == "NSE:RELIANCE:NSE_EQUITY"


def test_instrument_id_rejects_empty_symbol() -> None:
    with pytest.raises(ValidationError):
        InstrumentId(symbol=" ", exchange=Exchange.NSE, segment=MarketSegment.NSE_EQUITY)


def test_data_provider_id_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        DataProviderId(name="", provider_type=DataProviderType.LOCAL_SAMPLE)


def test_audit_id_new_creates_non_empty_id() -> None:
    audit_id = AuditId.new()

    assert str(audit_id).startswith("audit_")
    assert len(str(audit_id)) > len("audit_")
