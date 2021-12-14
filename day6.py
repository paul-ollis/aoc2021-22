"""Paul's solution for AOC day 6."""

from collections import deque

from lib import data_lines


def parse_fish_data() -> deque[int]:
    """Parse the initial lantern fish data.

    :return:
        A deque representing the fish population. The right side of the deque
        represents those fish with count = 0 and the left side as those fish
        with count == 0. Each entry is simply the number of fish with the given
        count.
    """
    data_line = list(data_lines(__file__))[0]
    population = [0] * 9
    for v in (int(sv) for sv in data_line.split(',')):
        population[v] += 1
    return deque(reversed(population))


def get_population(num_days):
    """Find the most scary fish positions."""
    fishes = parse_fish_data()
    for _ in range(num_days):
        births = fishes[-1]
        fishes.rotate()
        fishes[2] += births
    print(f'{sum(fishes):_d}')


get_population(80)
get_population(256)
