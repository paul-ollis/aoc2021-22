"""Paul's solution for AOC day 3."""

from collections import Counter
from itertools import count
from typing import Counter as CounterType, Iterable, List

from lib import data_lines


def parse_diagnotic_data() -> Iterable[List[str]]:
    """Parse the diagnostic data.

    This takes a sequence of binary values (one per line) and converts it
    to a sequence of tuples of the form:

        (b1, b2, b3, ...)

    Where b1 is the leftmost bit, b2 is the second bit, etc. Each value
    is left as a string value.
    """
    for line in data_lines(__file__):
        yield list(line.strip())


def count_bits(bit_strings: Iterable[List[str]]) -> List[CounterType[str]]:
    """Count the number of ones and zeros in each bit position."""
    for i, bits in enumerate(bit_strings):
        if not i:
            counters = [Counter({'0': 0, '1': 0}) for _ in bits]
        for b, counter in zip(bits, counters):
            counter[b] += 1

    return counters


def selector(bit_values, bit, cidx, fallback):
    """Obtains the selector for given bit position."""
    counts = count_bits(bit_values)[bit].most_common()
    if counts[0][1] == counts[1][1]:
        return fallback
    else:
        return counts[cidx][0]


def select_life_support_value(bit_values, cidx, fallback):
    """Select a life support value from the data."""
    bit_values = list(bit_values)
    for i in count():
        sel = selector(bit_values, i, cidx, fallback)
        bit_values = [bits for bits in bit_values if bits[i] == sel]
        if len(bit_values) == 1:
            return int(''.join(bit_values[0]), 2)

    raise RuntimeError('Unreachable code!!!')


def calc_power():
    """Calculate diagnostic power."""
    counters = count_bits(parse_diagnotic_data())
    gamma_bin = [counter.most_common(1)[0][0] for counter in counters]
    epsilon_bin = [counter.most_common()[-1][0] for counter in counters]

    gamma = int(''.join(gamma_bin), 2)
    epsilon = int(''.join(epsilon_bin), 2)

    print(gamma * epsilon)


def calc_life_support_rating():
    """Calculate diagnostic life support rating."""
    bit_values = list(parse_diagnotic_data())
    oxygen_genrator_rating = select_life_support_value(
        bit_values, cidx=0, fallback='1')
    co2_scrubber_rating = select_life_support_value(
        bit_values, cidx=1, fallback='0')

    print(oxygen_genrator_rating * co2_scrubber_rating)


calc_power()
calc_life_support_rating()
