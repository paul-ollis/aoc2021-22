"""Paul's solution for AOC day 8."""

from typing import Iterator, Tuple

from lib import data_lines

# Crib from the puzzle page.
#
#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# My approach:
#
# Each code c0, c1, ... c9, is a subset of the letters 'a' to 'g'. The sets c1,
# c4, c7 and c8 have unique code lengths. For the standard codes and using
# Python set operations we can state the following facts.
#
#  1.  c4 - c1           == ('b', 'd'}     # Call this d1
#  2.  c8 - c7 - c4 - c1 == {'e', 'g'}     # Call this d2
#
# Codes c2, c3 and c5 all have length 5 and we can state:
#
#  3.  d1 - c2 == d1 - c3  == {'b'}
#  4.  d1 - c5             == set()
#  5.  d2 - c3             == {'e'}
#  6.  d2 - c2             == set()
#
# Codes c0, c6 and c9 all have lengths 6 and we can state:
#
#  7.   d2 - c0 == d2 - c6 == set()
#  8.   d2 - c9            == {'e'}
#  9.   d1 - c6            == set()
#  10.  d1 - c0            == {'d'}
#
# - Codes c1, c4, c7 and c8 are directly identifiable from the code lengths.
# - Facts (3) and (4) together allow c5 to be identified.
# - Facts (5) and (6) together allow c2 and c3 to be identified.
# - Facts (7) and (8) together allow c9 to be identified.
# - Facts (9) and (10) together allow c6 and c0 to be identified.


def parse_segment_data() -> Iterator[Tuple]:
    """Parse the segment driving data.

    Generates a sequence of (preamble, digit_data) tuples. Each part of the
    tuple is a list of segment codes. Each segment code is a subset of the
    characters 'a' to 'g'.
    """
    for line in data_lines(__file__):
        preamble, _, digit_data = line.partition(' | ')
        yield tuple([
            [frozenset(s) for s in preamble.split()],
            [frozenset(s) for s in digit_data.split()]])


def decypher_digits(preamble):
    """Get the signal mapping using the preamble sequence."""

    def find(choices, pred):
        return [code for code in choices if pred(code)]

    c1 = find(preamble, lambda c: len(c) == 2)[0]
    c4 = find(preamble, lambda c: len(c) == 4)[0]
    c7 = find(preamble, lambda c: len(c) == 3)[0]
    c8 = find(preamble, lambda c: len(c) == 7)[0]
    d1 = c4 - c1
    d2 = c8 - c7 - c4 - c1

    codes = find(preamble, lambda c: len(c) == 5)
    c5 = find(codes, lambda c: len(d1 - c) == 0)[0]
    codes.remove(c5)
    c2 = find(codes, lambda c: len(d2 - c) == 0)[0]
    codes.remove(c2)
    c3 = codes[0]

    codes = find(preamble, lambda c: len(c) == 6)
    c9 = find(codes, lambda c: len(d2 - c) == 1)[0]
    codes.remove(c9)
    c0 = find(codes, lambda c: len(d1 - c) == 1)[0]
    codes.remove(c0)
    c6 = codes[0]

    return {
        c0: '0', c1: '1', c2: '2', c3: '3', c4: '4',
        c5: '5', c6: '6', c7: '7', c8: '8', c9: '9'}


def count_easy_digits():
    """Count the number of easily identified digits."""
    segment_data = list(parse_segment_data())
    decypher_digits(segment_data[0][0])
    res = sum(
        (sum(1 for d in digit_data if len(d) in (2, 3, 4, 7))
            for _, digit_data in segment_data))
    print(res)


def sum_values():
    """Calculate the sum of all the displayed values."""
    segment_data = list(parse_segment_data())
    tot = 0
    for preamble, digit_data in segment_data:
        coding = decypher_digits(preamble)
        display = [coding[c] for c in digit_data]
        tot += int(''.join(display))
    print(tot)


count_easy_digits()
sum_values()
