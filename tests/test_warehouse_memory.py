from stark_terminal_data_platform.warehouse.memory import InMemoryWarehouseQueryRecorder


def test_memory_warehouse_recorder_records_and_clears() -> None:
    recorder = InMemoryWarehouseQueryRecorder()

    recorder.record("SELECT 1", {"x": 1})

    assert recorder.count() == 1
    assert recorder.last_query() == {"query": "SELECT 1", "parameters": {"x": 1}}
    assert recorder.list_queries() == [{"query": "SELECT 1", "parameters": {"x": 1}}]

    recorder.clear()
    assert recorder.count() == 0
    assert recorder.last_query() is None


def test_memory_warehouse_recorder_has_no_global_state() -> None:
    one = InMemoryWarehouseQueryRecorder()
    two = InMemoryWarehouseQueryRecorder()

    one.record("SELECT 1")

    assert one.count() == 1
    assert two.count() == 0
