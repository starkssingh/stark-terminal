from datetime import date, datetime

from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.derivatives import FuturesContract
from stark_terminal_core.domain.enums import Exchange, MarketSegment, OptionType
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.options import OptionContract, OptionsChainSnapshot


def nifty() -> InstrumentId:
    return InstrumentId(symbol="NIFTY", exchange=Exchange.NSE, segment=MarketSegment.INDEX)


def banknifty() -> InstrumentId:
    return InstrumentId(
        symbol="BANKNIFTY",
        exchange=Exchange.NSE,
        segment=MarketSegment.INDEX,
    )


def option_contract(**overrides: object) -> OptionContract:
    payload = {
        "underlying": nifty(),
        "contract_symbol": "NIFTY26JUN23000CE",
        "expiry": date(2026, 6, 25),
        "strike": 23000.0,
        "option_type": OptionType.CALL,
        "lot_size": 50,
        "tick_size": 0.05,
    }
    payload.update(overrides)
    return OptionContract(**payload)


def test_valid_futures_contract() -> None:
    contract = FuturesContract(
        underlying=nifty(),
        contract_symbol="NIFTY26JUNFUT",
        expiry=date(2026, 6, 25),
        lot_size=50,
        tick_size=0.05,
    )

    assert contract.contract_symbol == "NIFTY26JUNFUT"


def test_valid_option_contract() -> None:
    contract = option_contract()

    assert contract.option_type == OptionType.CALL
    assert contract.strike == 23000.0


def test_options_chain_snapshot_rejects_mixed_underlying() -> None:
    with pytest.raises(ValidationError):
        OptionsChainSnapshot(
            underlying=nifty(),
            timestamp=datetime(2026, 6, 20, 9, 15),
            expiry=date(2026, 6, 25),
            contracts=[option_contract(), option_contract(underlying=banknifty())],
        )


def test_options_chain_snapshot_rejects_mixed_expiry() -> None:
    with pytest.raises(ValidationError):
        OptionsChainSnapshot(
            underlying=nifty(),
            timestamp=datetime(2026, 6, 20, 9, 15),
            expiry=date(2026, 6, 25),
            contracts=[option_contract(), option_contract(expiry=date(2026, 7, 30))],
        )


def test_options_chain_snapshot_rejects_empty_contracts() -> None:
    with pytest.raises(ValidationError):
        OptionsChainSnapshot(
            underlying=nifty(),
            timestamp=datetime(2026, 6, 20, 9, 15),
            expiry=date(2026, 6, 25),
            contracts=[],
        )
