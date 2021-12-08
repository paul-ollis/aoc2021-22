"""Paul's solution for AOC day 2."""

from itertools import accumulate
from typing import Iterator, Tuple

from lib import data_lines


def parse_route() -> Iterator[Tuple[int, int]]:
    """Parse the route.

    This takes the sequence of route instructions (one per line) and converts
    it to a sequence of tuples of the form:

        (depth_change, distance_change)

    For part two of the puzzle, the tuple meaning is:

        (aim_change, impulse_value)
    """
    for line in data_lines(__file__):
        command, value_str = line.split()
        if command == 'forward':
            yield 0, int(value_str)
        elif command == 'down':
            yield int(value_str), 0
        elif command == 'up':
            yield -int(value_str), 0
        else:
            raise RuntimeError(f'Unhandled command {command}')


def calc_position():
    """Calculate position, part 1."""
    depth = sum(d for d, _ in parse_route())
    position = sum(p for _, p in parse_route())

    print(depth * position)


def calc_position2():
    """Calculate position, part 2."""
    aims = accumulate(d for d, _ in parse_route())
    impulses = list(imp for _, imp in parse_route())
    depth = sum(aim * imp for aim, imp in zip(aims, impulses))
    position = sum(impulses)

    print(depth * position)


calc_position()
calc_position2()
