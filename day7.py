"""Paul's solution for AOC day 7."""

from collections import Counter
from typing import Counter as CounterType, Dict, Tuple

from lib import data_lines


def parse_position_data() -> CounterType[Dict[int, int]]:
    """Parse the initial lantern position data.

    :return:
        A Counter mapping from position to the number of crabs submarines in
        that position.
    """
    positions: CounterType = Counter()
    for line in data_lines(__file__):
        positions.update(int(sv) for sv in line.split(','))
    return positions


def get_best_position():
    """Find the most scary position positions."""
    positions = parse_position_data()

    def position_cost(p: int) -> Tuple[int, int]:
        return sum(n * abs(q - p) for q, n in positions.items()), p

    a, b = 1, max(positions.keys()) + 1
    fuel, _ = min(position_cost(p) for p in range(a, b))
    print(fuel)


def get_best_position2():
    """Find the most scary position positions."""
    positions = parse_position_data()

    def position_cost(p: int) -> Tuple[int, int]:
        def tri(v):
            return v * (v + 1) // 2

        return sum(n * tri(abs(q - p)) for q, n in positions.items()), p

    a, b = 1, max(positions.keys()) + 1
    fuel, _ = min(position_cost(p) for p in range(a, b))
    print(fuel)


get_best_position()
get_best_position2()
