"""Paul's solution for AOC day 11."""

from typing import List, Set
from itertools import chain

from lib import data_lines, windowize


class Octopus:                         # pylint: disable=too-few-public-methods
    """An model of an Octopus."""
    def __init__(self, energy: int = 0):
        self.energy = energy
        self.neighbours = []

    def inc(self):
        """Increment energy by 1."""
        self.energy += 1

    def power_neighbours(self, flashed: Set['Octopus']):
        """Flash if ready and then pass flash effect onto neighbours.

        :flashed: A set of any Octopus instances that have already flashed.
        """
        if self.energy > 9:
            flashed.add(self)
            for octopus in self.neighbours:
                if octopus not in flashed:
                    octopus.inc()
                    octopus.power_neighbours(flashed)
            self.energy = 0


class Nonopus(Octopus):                # pylint: disable=too-few-public-methods
    """Something like an Octopus, but with an unchanging energy level."""
    def inc(self):
        """Increment energy by 1."""


def parse_octopus_energies() -> List[List[int]]:
    """Parse the octopus energy data.

    The data is read into a simple grid of Octopus instances, each with the
    initial energy level provided by the data. For example::

        [O, O, O]
        [O, O, O]

    Then a border of Nonopus instances is added. For our example this gives::

        [N, N, N, N]
        [N, O, O, N]
        [N, O, O, N]
        [N, N, N, N]

    Then each Octopus is linked to its eight neighbours.
    """
    np = Nonopus(0)
    octopi = [[]]
    for line in data_lines(__file__):
        octopi.append([np] + [Octopus(int(c)) for c in line.strip()] + [np])
    w = len(octopi[1])
    octopi[0] = [np] * w
    octopi.append([np] * w)

    for behind, row, infront in windowize(octopi, 3):
        for i, (a, octopus, b) in enumerate(windowize(row, 3)):
            octopus.neighbours.extend([a, b])
            octopus.neighbours.extend(list(behind[i:i+3]))
            octopus.neighbours.extend(list(infront[i:i+3]))

    return octopi


def count_flashes(octopi: List[Octopus], n: int):
    """Count all the flashes after ``n`` steps."""
    total_flashes = 0
    for _ in range(n):
        flashed = set()
        for octopus in chain(*octopi):
            octopus.inc()
        for octopus in chain(*octopi):
            octopus.power_neighbours(flashed)
        total_flashes += len(flashed)

    print(total_flashes)


count_flashes(parse_octopus_energies(), 100)
