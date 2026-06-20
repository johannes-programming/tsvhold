import csv
import io
from collections.abc import Iterable
from typing import Any, Self, cast

import datahold
import setdoc

__all__ = ["TSVHolder"]


def strtuple(iterable: Iterable[object], /) -> tuple[str, ...]:
    return tuple(map(str, iterable))


class BaseTSVHolder(datahold.BaseHoldList[tuple[str, ...]]): ...


class TSVHolder(BaseTSVHolder, datahold.HoldList[Iterable[object]]):
    __slots__ = ()

    @property
    @setdoc.basic
    def data(self: Self) -> tuple[tuple[str, ...], ...]:
        return self._data

    @data.setter
    def data(self: Self, value: Iterable[Iterable[object]]) -> None:
        self._data: tuple[tuple[str, ...], ...] = tuple(map(strtuple, value))

    def dumpintofile(self: Self, file: str, /) -> None:
        stream: Any
        with open(file, "w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, delimiter="\t")
            writer.writerows(self)

    def dumps(self: Self) -> str:
        buffer: io.StringIO
        writer: Any
        buffer = io.StringIO()
        writer = csv.writer(buffer, delimiter="\t")
        writer.writerows(self)
        return buffer.getvalue()

    @classmethod
    def loadfromfile(cls: type[Self], file: str, /) -> Self:
        with open(file, "r", newline="", encoding="utf-8") as f:
            return cls(csv.reader(f, delimiter="\t"))

    @classmethod
    def loads(cls: type[Self], string: str, /) -> Self:
        return cls(csv.reader(io.StringIO(string), delimiter="\t"))
