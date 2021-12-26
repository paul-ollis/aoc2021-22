"""Some common code for the Advent of Code puzzle solvers."""

import os
from pathlib import Path
from typing import Iterator, Sequence, TypeVar, Tuple

T = TypeVar('T')


def data_lines(py_file_name: str) -> Iterator[str]:
    """Iterate through the lines for a puzzle solver's data file.

    This should be invoked as ``data_lines(__file__)``. The py_file_name is
    used to find the data file. So, for example, if py_file_name is
    'aoc/day1.py' then the file 'data/day1.txt' will be read.

    :py_file_name: The name of the solver;s python file.
    """
    data = os.environ.get('AOC_DEVEL', 'data')
    with open(f'{data}/{Path(py_file_name).stem}.txt', encoding='utf8') as f:
        for line in f:
            yield line.strip()


def windowize(seq: Sequence[T], n: int) -> Iterator[Tuple[T, ...]]:
    """Turn a sequence into overlapping windows of n items.

    For example, given n = 3 and a, b, c, d, e, f, ... The sequence (a, b, c),
    (b, c, d), (c, d, e), ... is produced.
    """
    iterators = [iter(seq) for _ in range(n)]
    for i, it in enumerate(iterators):
        for _ in range(i):
            next(it)
    return zip(*iterators)


def watch_counter(n:int):
    """A generator that asserts if executed too many times."""
    while True:
        assert n > 0
        n -= 1
        yield n


def range_intersection(ra: range, rb: range) -> range:
    """Calculate the intersection of two ranges.

    This only works for ranges with step == 1.

    :return:
        A new range that represents the overlap of the two ranges. The range
        (r) will be empty if there is no overlap, in which case

            range(r.end, r.start)

        is the range that fits between ra and rb.
    """
    return range(max(ra.start, rb.start), min(ra.stop, rb.stop))
