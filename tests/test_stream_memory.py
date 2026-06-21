from stark_terminal_data_platform.streams.memory import InMemoryStreamStore


def test_in_memory_stream_xadd_and_xrange() -> None:
    store = InMemoryStreamStore()

    first_id = store.xadd("stream", {"event_id": "event-1"})
    second_id = store.xadd("stream", {"event_id": "event-2"})

    assert first_id == "1-0"
    assert second_id == "2-0"
    assert store.xrange("stream") == [
        ("1-0", {"event_id": "event-1"}),
        ("2-0", {"event_id": "event-2"}),
    ]


def test_in_memory_stream_xread() -> None:
    store = InMemoryStreamStore()
    store.xadd("stream", {"event_id": "event-1"})

    assert store.xread({"stream": "0-0"}) == [("stream", [("1-0", {"event_id": "event-1"})])]


def test_in_memory_stream_group_read_and_ack() -> None:
    store = InMemoryStreamStore()
    store.xadd("stream", {"event_id": "event-1"})

    assert store.xgroup_create("stream", "group", id="0-0") is True
    entries = store.xreadgroup("group", "consumer", {"stream": ">"})

    assert entries == [("stream", [("1-0", {"event_id": "event-1"})])]
    assert store.xack("stream", "group", "1-0") == 1
    assert store.xack("stream", "group", "1-0") == 0


def test_in_memory_stream_maxlen_trimming_and_isolation() -> None:
    first = InMemoryStreamStore()
    second = InMemoryStreamStore()

    first.xadd("stream", {"event_id": "event-1"}, maxlen=2)
    first.xadd("stream", {"event_id": "event-2"}, maxlen=2)
    first.xadd("stream", {"event_id": "event-3"}, maxlen=2)

    assert [entry_id for entry_id, _ in first.xrange("stream")] == ["2-0", "3-0"]
    assert second.xrange("stream") == []

