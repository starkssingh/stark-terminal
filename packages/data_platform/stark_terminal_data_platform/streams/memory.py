from __future__ import annotations

from typing import Any


def _entry_number(entry_id: str) -> int:
    if entry_id in {"-", "0", "0-0"}:
        return 0
    if entry_id in {"+", "$"}:
        return 10**30
    return int(str(entry_id).split("-", 1)[0])


class InMemoryStreamStore:
    """Local/test Redis Streams subset. This is not durable storage."""

    def __init__(self) -> None:
        self._streams: dict[str, list[tuple[str, dict[str, str]]]] = {}
        self._sequence = 0
        self._groups: dict[tuple[str, str], str] = {}
        self._pending: dict[tuple[str, str], set[str]] = {}

    def _next_id(self) -> str:
        self._sequence += 1
        return f"{self._sequence}-0"

    def _latest_id(self, stream: str) -> str:
        entries = self._streams.get(stream, [])
        return entries[-1][0] if entries else "0-0"

    def xadd(
        self,
        stream: str,
        fields: dict[str, str],
        maxlen: int | None = None,
        approximate: bool = True,
    ) -> str:
        entry_id = self._next_id()
        entries = self._streams.setdefault(stream, [])
        entries.append((entry_id, dict(fields)))
        if maxlen is not None and maxlen > 0 and len(entries) > maxlen:
            del entries[: len(entries) - maxlen]
        return entry_id

    def xrange(
        self,
        stream: str,
        start: str = "-",
        end: str = "+",
        count: int | None = None,
    ) -> list[tuple[str, dict[str, str]]]:
        start_number = _entry_number(start)
        end_number = _entry_number(end)
        entries = [
            (entry_id, dict(fields))
            for entry_id, fields in self._streams.get(stream, [])
            if start_number <= _entry_number(entry_id) <= end_number
        ]
        return entries[:count] if count is not None else entries

    def xread(
        self,
        streams: dict[str, str],
        count: int | None = None,
        block: int | None = None,
    ) -> list[tuple[str, list[tuple[str, dict[str, str]]]]]:
        result: list[tuple[str, list[tuple[str, dict[str, str]]]]] = []
        for stream, last_id in streams.items():
            if last_id == "$":
                entries: list[tuple[str, dict[str, str]]] = []
            else:
                last_number = _entry_number(last_id)
                entries = [
                    (entry_id, dict(fields))
                    for entry_id, fields in self._streams.get(stream, [])
                    if _entry_number(entry_id) > last_number
                ]
            if count is not None:
                entries = entries[:count]
            if entries:
                result.append((stream, entries))
        return result

    def xgroup_create(
        self,
        stream: str,
        group: str,
        id: str = "$",
        mkstream: bool = True,
    ) -> bool:
        if mkstream:
            self._streams.setdefault(stream, [])
        group_id = self._latest_id(stream) if id == "$" else id
        self._groups[(stream, group)] = group_id
        self._pending.setdefault((stream, group), set())
        return True

    def xreadgroup(
        self,
        group: str,
        consumer: str,
        streams: dict[str, str],
        count: int | None = None,
        block: int | None = None,
    ) -> list[tuple[str, list[tuple[str, dict[str, str]]]]]:
        result: list[tuple[str, list[tuple[str, dict[str, str]]]]] = []
        for stream, requested_id in streams.items():
            group_key = (stream, group)
            if group_key not in self._groups:
                self.xgroup_create(stream, group, id="0-0", mkstream=True)
            last_id = self._groups[group_key] if requested_id == ">" else requested_id
            entries = self.xread({stream: last_id}, count=count, block=block)
            if entries:
                _, stream_entries = entries[0]
                if stream_entries:
                    self._groups[group_key] = stream_entries[-1][0]
                    self._pending.setdefault(group_key, set()).update(
                        entry_id for entry_id, _ in stream_entries
                    )
                    result.append((stream, stream_entries))
        return result

    def xack(self, stream: str, group: str, *ids: str) -> int:
        pending = self._pending.setdefault((stream, group), set())
        acknowledged = 0
        for entry_id in ids:
            if entry_id in pending:
                pending.remove(entry_id)
                acknowledged += 1
        return acknowledged

    def clear(self) -> None:
        self._streams.clear()
        self._groups.clear()
        self._pending.clear()
        self._sequence = 0

