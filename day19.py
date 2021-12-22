"""Paul's solution for AOC day 19."""

from collections import Counter
from functools import partial
from itertools import product, combinations
from typing import Callable, List, Optional, Tuple

from lib import data_lines

# We use three basic reorientation operations.
#
#  RR Rotate right          x = -z                 -3,  2,  1
#     (Screw in action)     y   unchanged
#                           z = x
#
#  TR Turn right            x = -y                 -2,  1,  3
#                           y = x                  -1, -2,  3
#                           z   unchanged
#
#  PD Point Down            x   unchanged           1, -3,  2
#                           y = -z
#                           z = y
#
# The above can be combined in the following ways to acheive all
# possible orientations.
#
# 1.  RR x 1
# 2,  RR x 2
# 3.  RR x 3
# 4.  TR x 1
# 5.  TR x 2
# 6.  TR x 3
# 7.  PD x 1
# 8.  PD x 2
# 9.  PD x 3
# 10. TR x 1, RR x 1
# 11. TR x 1, RR x 2
# 12. TR x 1, RR x 3
# 13. TR x 2, RR x 1
# 14. TR x 2, RR x 3   note: TR x 2, RR x 2 is the same as PD x 2.
# 15. TR x 3, RR x 1
# 16. TR x 3, RR x 2
# 17. TR x 3, RR x 3
# 18. PD x 1, RR x 1
# 19. PD x 1, RR x 2
# 20. PD x 1, RR x 3
# 21. PD x 3, RR x 1   note: PD x 2, etc. already covered.
# 22. PD x 3, RR x 2
# 23. PD x 3, RR x 3

Coord = Tuple[int, int, int]


def rotate_right(n: int, coord: Coord) -> Coord:
    """Perform rotate right reorientation one or more times."""
    x, y, z = coord
    for _ in range(n):
        x, y, z = -z, y, x            # pylint: disable=self-assigning-variable
    return x, y, z


def turn_right(n: int, coord: Coord) -> Coord:
    """Perform turn right reorientation one or more times."""
    x, y, z = coord
    for _ in range(n):
        x, y, z = -y, x, z            # pylint: disable=self-assigning-variable
    return x, y, z


def point_down(n: int, coord: Coord) -> Coord:
    """Perform point down reorientation one or more times."""
    x, y, z = coord
    for _ in range(n):
        x, y, z = x, -z, y            # pylint: disable=self-assigning-variable
    return x, y, z


# Combinations of basic operationsto reach all possible orientations.
reorientations = [
   (),
   (partial(rotate_right, 1),),
   (partial(rotate_right, 2),),
   (partial(rotate_right, 3),),
   (partial(turn_right, 1),),
   (partial(turn_right, 2),),
   (partial(turn_right, 3),),
   (partial(point_down, 1),),
   (partial(point_down, 2),),
   (partial(point_down, 3),),
   (partial(turn_right, 1), partial(rotate_right, 1)),
   (partial(turn_right, 1), partial(rotate_right, 2)),
   (partial(turn_right, 1), partial(rotate_right, 3)),
   (partial(turn_right, 2), partial(rotate_right, 1)),
   (partial(turn_right, 2), partial(rotate_right, 3)),
   (partial(turn_right, 3), partial(rotate_right, 1)),
   (partial(turn_right, 3), partial(rotate_right, 2)),
   (partial(turn_right, 3), partial(rotate_right, 3)),
   (partial(point_down, 1), partial(rotate_right, 1)),
   (partial(point_down, 1), partial(rotate_right, 2)),
   (partial(point_down, 1), partial(rotate_right, 3)),
   (partial(point_down, 3), partial(rotate_right, 1)),
   (partial(point_down, 3), partial(rotate_right, 2)),
   (partial(point_down, 3), partial(rotate_right, 3)),
]


class Scanner:
    """A single scanner and its beacon information.

    A scanner considers the Y axis to extend formward, the X axis to extend to
    the right and the Z axis to extend upward.
    """
    b_hits = 0
    b_misses = 0
    c_hits = 0
    c_misses = 0

    def __init__(self, index, beacons):
        self.index = index
        self.recorded_beacons = list(beacons)
        self.rel_beacons = list(beacons)
        self.orientation = 0
        self.origin: Optional[Coord] = 0, 0, 0
        self._beacon_cache = {}
        self._offset_cache = {}

    def set_orientation(self, orientation: int):
        """Switch to the next possible orientation for this scanner."""
        if self.orientation != orientation:
            self.orientation = orientation % 24
            self.rel_beacons = []

            operations = reorientations[self.orientation]
            for coord in self.recorded_beacons:
                for op in operations:
                    coord = op(coord)
                self.rel_beacons.append(coord)

    @property
    def beacons(self):
        """The beacon positions adjusted by the origin."""
        key = self.orientation, self.origin
        if key in self._beacon_cache:
            Scanner.b_hits += 1
            return self._beacon_cache[key]

        Scanner.b_misses += 1
        xo, yo, zo = self.origin
        ret = [(x + xo, y + yo, z + zo) for x, y, z in self.rel_beacons]
        self._beacon_cache[key] = ret
        return ret

    def coord_offsets(self, other: 'Scanner', i: int) -> List[int]:
        """Calculate a coordinate's offset for all beacon pairs."""
        key = (
            other, i,
            self.orientation, self.origin,
            other.orientation, other.origin)
        if key in self._offset_cache:
            Scanner.c_hits += 1
            return self._offset_cache[key]

        Scanner.c_misses += 1
        ret = [a[i] - b[i] for a, b in product(self.beacons, other.beacons)]
        self._offset_cache[key] = ret
        return ret

    def x_offsets(self, other: 'Scanner'):
        """Calculate the X coordinate offset for all beacon pairs."""
        return self.coord_offsets(other, 0)

    def y_offsets(self, other: 'Scanner'):
        """Calculate the Y coordinate offset for all beacon pairs."""
        return self.coord_offsets(other, 1)

    def z_offsets(self, other: 'Scanner'):
        """Calculate the Z coordinate offset for all beacon pairs."""
        return self.coord_offsets(other, 2)

    def manhattan_distance(self, other: 'Scanner'):
        """The Manhattan distance to another scanner."""
        x, y, z = self.origin
        xb, yb, zb = other.origin
        return abs(x - xb) + abs(y - yb) + abs(z - zb)

    def dump(self):
        """Dump details to stdout."""
        for coord in self.beacons:
            print(coord)


def parse_input() -> List[Scanner]:
    """Parse the scanner data.

    :return:
        A list of `Scanner` instances.
    """
    def emit():
        nonlocal index
        if coords:
            scanners.append(Scanner(index, coords))
            coords[:] = []
            index += 1

    index = 0
    scanners = []
    coords = []
    for line in data_lines(__file__):
        if line.startswith('--- '):
            emit()
        elif line:
            coords.append(tuple(int(v) for v in line.split(',')))
    emit()
    return scanners


def get_offsets(
        scanner: Scanner, orientation: int, offsets: Callable[[int], None]):
    """Get the possible offset for a given coordinate and orientation."""
    scanner.set_orientation(orientation)
    counts = Counter(offsets(scanner))
    return [off for off, n in counts.most_common() if n >= 12]


def compare_scanners(a: Scanner, b: Scanner) -> Optional[Coord]:
    """Compare wo scanners to find common beacons."""

    # There are 24 possible orientations for scanner B. Try each to find any
    # offsets where 12 or more pairs of A and B scanner beacons coincide for
    # each of the X, Y and Z coordinates. The set of possible orientations is
    # reduced as each coordinate is considered.
    orientations = list(range(24))
    for offset_func in (a.x_offsets, a.y_offsets, a.z_offsets):
        orientations = [
            orit for orit in orientations if get_offsets(b, orit, offset_func)]

    # There could be no overlap.
    if not orientations:
        return None

    for orientation in orientations:
        # Get the possible offsets for each of X, Y and Z coords.
        x_offsets = get_offsets(b, orientation, a.x_offsets)
        y_offsets = get_offsets(b, orientation, a.y_offsets)
        z_offsets = get_offsets(b, orientation, a.z_offsets)

        if not (x_offsets and y_offsets and z_offsets):
            continue

        # For now we are assuming beacons are sparse enough to find one unique
        # combination of X, Y and Z offsets.
        assert (len(x_offsets), len(y_offsets), len(z_offsets)) == (1, 1, 1)

        # We have a possible position of scanner B relative to scanner A and
        # its orientation. Set them and then find the set of common beacons.
        b.origin = x_offsets[0], y_offsets[0], z_offsets[0]
        b.set_orientation(orientation)
        common_beacons = set(a.beacons) & set(b.beacons)

        # It is possible that we have found fewer than 12 common beacons.
        if len(common_beacons) >= 12:
            return b.origin

        b.origin = 0, 0, 0

    return None


def solve():
    """Solve the puzzle - part 1."""
    scanners = parse_input()
    fixed = set(scanners[:1])
    unfixed = set(scanners[1:])
    while unfixed:
        for second, first in product(unfixed, fixed):
            origin = compare_scanners(first, second)
            if origin:
                fixed.add(second)
                unfixed.remove(second)
                #print(first.index, second.index, origin)
                break

    beacons = set(scanners[0].beacons)
    for scanner in scanners[1:]:
        beacons |= set(scanner.beacons)

    print(len(beacons))
    print(max(a.manhattan_distance(b) for a, b in combinations(scanners, 2)))


def solve_part2():
    """Solve the puzzle, part 2."""
    scanners = parse_input()
    print(len(list(scanners)))


solve()
# solve_part2()
