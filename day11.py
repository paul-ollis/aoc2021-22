"""Paul's solution for AOC day 11."""

from itertools import chain, count
from typing import List, Set

from lib import data_lines, windowize


class Octopus:
    """An model of an Octopus."""
    def __init__(self, energy: int = 0):
        self.energy = energy
        self.neighbours: List[Octopus] = []

    def inc(self):
        """Increment this Octopus's energy level."""
        self.energy += 1

    def flash_if_ready(self, flashed: Set['Octopus']):
        """Flash if ready and then pass flash effect onto neighbours.

        :flashed: A set of any Octopus instances that have already flashed.
        """
        if self.energy > 9:
            flashed.add(self)
            for octopus in self.neighbours:
                if octopus not in flashed:
                    octopus.inc()
                    octopus.flash_if_ready(flashed)
            self.energy = 0


class Nonopus(Octopus):
    """Something like an Octopus, but with an unchanging energy level."""
    def inc(self):
        """Do *not* increment energy by 1."""


def parse_octopus_energies() -> List[List[Octopus]]:
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

    Then each Octopus is linked to its eight neighbours. Nonopus instance do
    not have any links set up.
    """
    np = Nonopus(0)
    octopi: List[List[Octopus]] = [[]]
    for line in data_lines(__file__):
        octopi.append([np, *[Octopus(int(c)) for c in line.strip()], np])

    w = len(octopi[1])
    octopi[0] = [np] * w
    octopi.append([np] * w)

    for behind, row, infront in windowize(octopi, 3):
        for i, (a, octopus, b) in enumerate(windowize(row, 3)):
            octopus.neighbours.extend([a, b])
            octopus.neighbours.extend(list(behind[i:i+3]))
            octopus.neighbours.extend(list(infront[i:i+3]))

    return octopi


def run_step(octopi: List[List[Octopus]]):
    """Run the octopi through a single step."""
    flashed: Set[Octopus] = set()
    for octopus in chain(*octopi):
        octopus.inc()
    for octopus in chain(*octopi):
        octopus.flash_if_ready(flashed)
    return flashed


def count_flashes(octopi: List[List[Octopus]], n: int):
    """Count all the flashes after ``n`` steps."""
    total_flashes = 0
    for _ in range(n):
        flashes = run_step(octopi)
        total_flashes += len(flashes)

    print(total_flashes)


def find_first_simulflash(octopi: List[List[Octopus]]):
    """Find the first time that all the octopi flash simultaneously."""
    for n in count(1):
        flashes = run_step(octopi)
        if len(flashes) == 100:
            print(n)
            return


count_flashes(parse_octopus_energies(), 100)
find_first_simulflash(parse_octopus_energies())
