import os
import tempfile
import unittest
from collections.abc import Sequence
from typing import Self

from tsvhold import TSVHolder

__all__ = ["TestTSVHolder"]


class TestTSVHolder(unittest.TestCase):
    sample_data: list[Sequence[int | float | str | bool | None]]
    expected: tuple[tuple[str, ...], ...]

    def setUp(self: Self) -> None:
        self.sample_data = [
            [1, 2, 3],
            ["a", "b", "c"],
            [True, None, 4.5],
        ]
        self.expected = (
            ("1", "2", "3"),
            ("a", "b", "c"),
            ("True", "None", "4.5"),
        )

    def test_data_conversion(self: Self) -> None:
        holder: TSVHolder
        holder = TSVHolder(self.sample_data)
        self.assertEqual(holder.data, self.expected)

    def test_dumps(self: Self) -> None:
        expected: str
        holder: TSVHolder
        result: str
        holder = TSVHolder(self.sample_data)
        result = holder.dumps()
        expected = "1\t2\t3\r\na\tb\tc\r\nTrue\tNone\t4.5\r\n"
        self.assertEqual(result, expected)

    def test_dumpintofile_and_loadfromfile(self: Self) -> None:
        filepath: str
        holder: TSVHolder
        loaded: TSVHolder
        tmpdir: str
        holder = TSVHolder(self.sample_data)
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.tsv")
            holder.dumpintofile(filepath)
            loaded = TSVHolder.loadfromfile(filepath)
            self.assertEqual(loaded.data, self.expected)

    def test_loads(self: Self) -> None:
        content: str
        holder: TSVHolder
        content = "x\ty\tz\n1\t2\t3\n"
        holder = TSVHolder.loads(content)
        self.assertEqual(
            holder.data,
            (("x", "y", "z"), ("1", "2", "3")),
        )

    def test_empty_data(self: Self) -> None:
        holder: TSVHolder
        holder = TSVHolder([])
        self.assertEqual(holder.data, ())
        self.assertEqual(holder.dumps(), "")


if __name__ == "__main__":
    unittest.main()
