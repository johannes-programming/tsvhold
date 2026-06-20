import os
import tempfile
import unittest
from collections.abc import Sequence
from typing import Self

from tsvhold import TSVHolder

__all__ = ["TestTSVHolder"]

Cell = int | float | str | bool | None
Row = Sequence[Cell]


class TestTSVHolder(unittest.TestCase):
    sample_data: list[Row]
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
        holder: TSVHolder = TSVHolder(self.sample_data)
        self.assertEqual(holder.data, self.expected)

    def test_dumps(self: Self) -> None:
        holder: TSVHolder = TSVHolder(self.sample_data)
        result: str = holder.dumps()
        expected: str = "1\t2\t3\r\na\tb\tc\r\nTrue\tNone\t4.5\r\n"
        self.assertEqual(result, expected)

    def test_dumpintofile_and_loadfromfile(self: Self) -> None:
        holder: TSVHolder = TSVHolder(self.sample_data)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath: str = os.path.join(tmpdir, "test.tsv")

            holder.dumpintofile(filepath)
            loaded: TSVHolder = TSVHolder.loadfromfile(filepath)

            self.assertEqual(loaded.data, self.expected)

    def test_loads(self: Self) -> None:
        content: str = "x\ty\tz\n1\t2\t3\n"
        holder: TSVHolder = TSVHolder.loads(content)

        self.assertEqual(
            holder.data,
            (("x", "y", "z"), ("1", "2", "3")),
        )

    def test_empty_data(self: Self) -> None:
        holder: TSVHolder = TSVHolder([])
        self.assertEqual(holder.data, ())
        self.assertEqual(holder.dumps(), "")


if __name__ == "__main__":
    unittest.main()
