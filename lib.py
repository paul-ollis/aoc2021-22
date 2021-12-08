"""Some common code for the Advent of Code puxxle solvers."""

from pathlib import Path
from typing import Iterator


def data_lines(py_file_name: str) -> Iterator[str]:
    """Iterate through the lines for a puzzle solver's data file.

    This should be invoked as ``data_lines(__file__)``. The py_file_name is
    used to find the data file. So, for example, if py_file_name is
    'aoc/day1.py' then the file 'data/day1.txt' will be read.

    :py_file_name: The name of the solver;s python file.
    """
    with open(f'data/{Path(py_file_name).stem}.txt', encoding='utf8') as f:
        yield from f
