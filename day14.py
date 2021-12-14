"""Paul's solution for AOC day 14."""

from typing import List, Tuple, Dict
from collections import Counter

from lib import data_lines, windowize


def parse_polymer_rules() -> Tuple[List[str], Dict[str, str]]:
    """Parse the polymer generation rule set.

    The first line is read as the initial polymer formula converted to a list
    of element symbols. Subsequent lines are converted to a dictionary where
    each key is the pair to match and each value the element to insert.
    """
    lines = data_lines(__file__)
    polymer = next(lines)
    next(lines)
    rules = dict(line.split(' -> ') for line in lines)

    return list(polymer), rules


def grow_polymer(n: int):
    """Grow the polymenr using ``n`` steps."""
    polymer, rules = parse_polymer_rules()

    for _ in range(n):
        new_polymer = []
        b = ''
        for a, b in windowize(polymer, 2):
            new_element = rules.get(f'{a}{b}')
            new_polymer.append(a)
            if new_element:
                new_polymer.append(new_element)
        new_polymer.append(b)
        polymer = new_polymer

    counts = Counter(polymer)
    ordered_counts = counts.most_common()
    print(ordered_counts[0][1] - ordered_counts[-1][1])
    print(Counter(polymer))


grow_polymer(10)
# grow_polymer(40)
