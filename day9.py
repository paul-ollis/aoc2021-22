"""Paul's solution for AOC day 9."""

from typing import List

from lib import data_lines, windowize


def parse_heightmap_data() -> List[List[int]]:
    """Parse the cave floor heightmap data.

    Each line is turned into a simple sequence of integer values in the range 0
    to 9 and then a value of 9 is added at either end to represent the cave
    side walls. Start and end sequences of [9, 9, 9, ...] are also added
    to represent the front and back cave walls.
    """
    data = [[]]
    for line in data_lines(__file__):
        data.append([9] + [int(c) for c in line.strip()] + [9])
    w = len(data[1])
    data[0] = [9] * w
    data.append([9] * w)
    return data


def find_low_points(floor_heights):
    """Find all the low point on the floor."""
    row_triplets = windowize(floor_heights, 3)
    for ri, (behind, row, infront) in enumerate(row_triplets):
        for ci, (a, v, b) in enumerate(windowize(row, 3)):
            if v < a and v < b:
                c, d = behind[ci+1], infront[ci+1]
                if v < c and v < d:
                    yield v, ri + 1, ci + 1


def calc_risk_total():
    """Calculate the risk total for the cave floor."""
    floor_heights = parse_heightmap_data()
    print(sum(v + 1 for v, r, c in find_low_points(floor_heights)))


def find_basin_heighbours(floor_heights, r, c, known):
    """Find the neighbours that are higher than a given point.

    The caller must not call this for edge points. This will not yield edge
    points.
    """
    # pylint: disable=dangerous-default-value
    v = floor_heights[r][c]

    for rn, cn in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
        vn = floor_heights[rn][cn]
        if 9 > vn > v:
            p = rn, cn
            if p not in known:
                known.add(p)
                known = find_basin_heighbours(floor_heights, rn, cn, known)
    return known


def find_basins():
    """Find the basins around each low point."""
    floor_heights = parse_heightmap_data()
    basins = []
    for _, r, c in find_low_points(floor_heights):
        found = find_basin_heighbours(floor_heights, r, c, set([(r, c)]))
        basins.append(found)

    *_, a, b, c = sorted([len(b) for b in basins])
    print(a * b * c)


calc_risk_total()
find_basins()
