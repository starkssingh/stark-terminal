import pytest

from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.master import LocalInstrumentMaster


def test_local_instrument_master_list_get_search_snapshot() -> None:
    master = LocalInstrumentMaster(create_sample_instruments())

    assert len(master.list_instruments()) == 6
    assert master.get_instrument("reliance", "NSE", "NSE_EQUITY") is not None
    assert master.get_instrument("missing", "NSE", "NSE_EQUITY") is None
    assert master.search("hdfc")[0].instrument_id.symbol == "HDFCBANK"
    assert len(master.search("synthetic", limit=2)) == 2
    assert len(master.snapshot().instruments) == 6


def test_local_instrument_master_search_limit_validation() -> None:
    master = LocalInstrumentMaster(create_sample_instruments())

    with pytest.raises(ValueError):
        master.search("reliance", limit=0)
