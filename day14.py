"""Paul's solution for AOC day 14."""

from collections import Counter
from typing import Counter as CounterType, Dict, List, Tuple

from lib import data_lines, windowize

# My approach:
#
# The length of the polymner increases exponentially so that 40 steps requires
# way to much memory to hold the polymer's structure. I found working out a
# scalable solution to this quite tricky. The key (for me) was to consider an
# arbitrary element pair within the polymer.
#
#     x A B y
#
# The 'x' and 'y' represent the preceding and following sequences of the
# polymer, either of which can be empty. The set of element pairs for the
# entire polymer is:
#
#     a. All the overlapping pairs in 'x'.
#     b. All the overlapping pairs in 'y'.
#     c. (x[-1], A) (which may not exist).
#     d. (B, y[0]) (which may not exist).
#     e. The pair (A, B).
#
# If there is a rule for (A B) then applying it will insert a new element C
# giving:
#
#     x A C B y
#
# Now the set of element pairs is:
#
#     a. All the overlapping pairs in 'x'.
#     b. All the overlapping pairs in 'y'.
#     c. (x[-1], A) (which may not exist).
#     d. (B, y[0]) (which may not exist).
#     e. The pair (A, C).
#     f. The pair (C, B)
#
# So the application of the rule has removed one instance of (A, B) from the
# set of all element pairs and added two more element pairs (B, C) and (C, B).
# This means we can easily count how many of each unique element pair exists
# after each step without tracking the actual sequence of the entire polymer.
#
# The count of each element is the number of times it appears as first element
# in a pair. Plus an extra count for the very last element in the polymer.

ElementPair = Tuple[str, str]     # For example ('C', 'N').
RuleTable = Dict[
    ElementPair,                  # Original element pair
    Tuple[
        ElementPair,              # First newly created pair.
        ElementPair,              # Second newly create pair.
    ]
]


def parse_polymer_rules() -> Tuple[List[str], RuleTable]:
    """Parse the polymer generation rule set.

    The first line is read as the initial polymer formula converted to a list
    of element symbols. Subsequent lines are converted to a dictionary where
    each key is the pair to match and each value the element to insert.
    """
    lines = data_lines(__file__)
    polymer = next(lines)
    next(lines)
    basic_rules = dict(line.split(' -> ') for line in lines)

    rules = {}
    for pair, element in basic_rules.items():
        a, b = pair[0], pair[1]
        rules[(a ,b)] = ((a, element), (element, b))

    return list(polymer), rules


def grow_polymer(n_steps: int):
    """Grow the polymenr for a given number of steps."""
    polymer, rules = parse_polymer_rules()
    counts = Counter(windowize(polymer, 2))
    for _ in range(n_steps):
        for pair, n in list(counts.items()):
            if pair not in rules:
                continue
            # TODO: This unpacking is to keep mypy quiet. Find a better way.
            a, b, *_ = pair
            new_pair1, new_pair2 = rules[(a, b)]
            counts[new_pair1] += n
            counts[new_pair2] += n
            counts[pair] -= n

    el_counts: CounterType[str] = Counter()
    for (a, _), n in counts.items():
        el_counts[a] += n

    el_counts[polymer[-1]] += 1
    ordered_counts = el_counts.most_common()
    print(ordered_counts[0][1] - ordered_counts[-1][1])


grow_polymer(10)
grow_polymer(40)
