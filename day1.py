"""Paul's solution for AOC day 1`."""

from lib import data_lines, windowize


def calc_incs(values):
    """Calculate number of increments for part A."""
    print(sum(1 for a, b in windowize(values, 2) if b > a))


def calc_windowed_incs(values):
    """Calculate number of increments for part B."""
    calc_incs(list(sum(t) for t in windowize(values, 3)))


input_data = [int(line) for line in data_lines(__file__)]
calc_incs(input_data)
calc_windowed_incs(input_data)
