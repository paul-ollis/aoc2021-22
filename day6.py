"""Paul's solution for AOC day 6."""

from collections import deque


def parse_fish_data(data: str) -> deque[int]:
    """Parse the initial lantern fish data.

    :return:
        A deque representing the fish population. The right side of the deque
        represents those fish with count = 0 and the left side as those fish
        with count == 0. Each entry is simply the number of fish with the given
        count.
    """
    data_line = [line.strip() for line in data.splitlines() if line.strip()][0]
    population = [0] * 9
    for v in (int(sv) for sv in data_line.split(',')):
        population[v] += 1
    return deque(reversed(population))


def get_population(num_days):
    """Find the most scary fish positions."""
    fishes = parse_fish_data(fish_data)
    for _ in range(num_days):
        births = fishes[-1]
        fishes.rotate()
        fishes[2] += births
    print(sum(fishes), 353079, 1605400130036)


fish_data = """
4,5,3,2,3,3,2,4,2,1,2,4,5,2,2,2,4,1,1,1,5,1,1,2,5,2,1,1,4,4,5,5,1,2,1,1,5,3,5,2,4,3,2,4,5,3,2,1,4,1,3,1,2,4,1,1,4,1,4,2,5,1,4,3,5,2,4,5,4,2,2,5,1,1,2,4,1,4,4,1,1,3,1,2,3,2,5,5,1,1,5,2,4,2,2,4,1,1,1,4,2,2,3,1,2,4,5,4,5,4,2,3,1,4,1,3,1,2,3,3,2,4,3,3,3,1,4,2,3,4,2,1,5,4,2,4,4,3,2,1,5,3,1,4,1,1,5,4,2,4,2,2,4,4,4,1,4,2,4,1,1,3,5,1,5,5,1,3,2,2,3,5,3,1,1,4,4,1,3,3,3,5,1,1,2,5,5,5,2,4,1,5,1,2,1,1,1,4,3,1,5,2,3,1,3,1,4,1,3,5,4,5,1,3,4,2,1,5,1,3,4,5,5,2,1,2,1,1,1,4,3,1,4,2,3,1,3,5,1,4,5,3,1,3,3,2,2,1,5,5,4,3,2,1,5,1,3,1,3,5,1,1,2,1,1,1,5,2,1,1,3,2,1,5,5,5,1,1,5,1,4,1,5,4,2,4,5,2,4,3,2,5,4,1,1,2,4,3,2,1
"""

get_population(80)
get_population(256)
