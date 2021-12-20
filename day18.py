"""Paul's solution for AOC day 18."""

from itertools import permutations
from typing import List, Tuple, Union

from lib import data_lines

Number = List[Union['Number', int]]


def parse_input() -> Number:
    """Parse the homework assignment.

    The is pleasingly Python lists.
    """
    # pylint: disable=eval-used
    return [eval(line) for line in data_lines(__file__) if '#' not in line]


def expand(number: Number) -> List[Tuple[int, str]]:
    """Expand a number to a seuqnece of symbols and ints."""

    def int_or_str(s):
        try:
            return int(s)
        except ValueError:
            return s

    return list(int_or_str(c) for c in str(number).replace(' ', ''))


def collapse(seq: List[Tuple[int, str]]) -> Number:
    """Collapse a expanded number."""
    # pylint: disable=eval-used
    return eval(''.join(str(ent) for ent in seq))


def explode(seq: List[str], values: List[Tuple[int, int]]):
    """Explode part of an expression."""
    (ia, a), (ib, b) = values

    for k in range(ia -1, 0, -1):
        if isinstance(seq[k], int):
            seq[k] = seq[k] + a
            break

    for k in range(ib + 1, len(seq)):
        if isinstance(seq[k], int):
            seq[k] = seq[k] + b
            break

    seq[ia - 1: ib + 2] = [0]


def split(seq: List[str], value: int, i: int):
    """Split a vlue in an expression."""
    a, r = divmod(value, 2)
    b = a + r
    seq[i:i+1] = ['[', a, ',', b, ']']


def find_and_do_explosion(seq: List[str]) -> bool:
    """Search for and explode a suitably nested pair.

    :return: True if a pair was exploded.
    """
    level = 0
    values = []
    for i, ent in enumerate(seq):
        match ent:
            case '[':
                level += 1
                values = []
            case ']':
                if level > 4:
                    explode(seq, values)
                    return True
                level -= 1
            case int(_):
                values.append((i, ent))
    return False


def find_and_do_split(seq: List[str]) -> bool:
    """Search for and split a value greater then 9.

    :return: True if a value was split.
    """
    for i, ent in enumerate(seq):
        if isinstance(ent, int):
            if ent > 9:
                split(seq, ent, i)
                return True
    return False


def reduce_number(outer_number: Number):
    """Reduce a number to its simplified form."""
    seq = expand(outer_number)
    while find_and_do_explosion(seq) or find_and_do_split(seq):
        pass
    return collapse(seq)


def magnitude(number: Tuple[Number, int]):
    """Calculate the magnitiude of a number or number value."""
    try:
        a, b = number
    except TypeError:
        return number
    else:
        return 3 * magnitude(a) + 2 * magnitude(b)


def solve():
    """Solve the puzzle - part 1."""
    numbers = parse_input()
    total: Number = reduce_number(numbers[0])
    for n in numbers[1:]:
        n_red = reduce_number(n)
        total = [total, n_red]
        total = reduce_number(total)
    print(magnitude(total))


def solve_part2():
    """Solve the puzzle, part 2."""
    numbers = parse_input()
    max_mag = 0
    for a, b in permutations(numbers, 2):
        total: Number = reduce_number([a, b])
        max_mag = max(magnitude(total), max_mag)
    print(max_mag)


solve()
solve_part2()
