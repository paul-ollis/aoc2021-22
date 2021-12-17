"""Paul's solution for AOC day 15."""

from typing import List

from lib import data_lines


def parse_risk_grid(expand=False) -> List[List[int]]:
    """Parse the risk grid.

    The grid input is simply a sequence of lines containing digits 1 to 9.
    Each digit is a risk level. We can simply load it as a nested list of
    integers.
    """
    grid = [[int(c) for c in line] for line in data_lines(__file__)]
    if expand:
        new_grid = []
        for row in grid:
            new_row = []
            for n in range(5):
                part = [(v + n - 1) % 9 + 1 for v in row]
                new_row.extend(part)
            new_grid.append(new_row)

        grid, new_grid = new_grid, []
        for n in range(5):
            for row in grid:
                new_grid.append([(v + n - 1) % 9 + 1 for v in row])

        grid = new_grid

    assert len(grid) == len(grid[0])  # Must be square.
    return grid


def add_initial_best_risk(grid, corner):
    """Add initial figures for the best minimum risk for a grib border.

    The figures we not be the actual minima, but provide a good starting point
    for refinement.
    """
    dmax = len(grid) - 1

    def calc_risk(x, y, offsets):
        risk, _ = grid[y][x]
        choices = []
        for dx, dy in offsets:
            xc, yc = x + dx, y + dy
            if xc <= dmax and yc <= dmax:
                choices.append(grid[yc][xc][1])
        grid[y][x] = risk, min(risk + total for total in choices)

    for x, y in border_coords(corner, dmax):
        calc_risk(x, y, [(0, 1), (1, 0)])


def top_border_coords(corner, dmax):
    """Yield coordinate for the top border for a given corner."""
    for x in range(dmax, corner, -1):
        yield x, corner


def left_border_coords(corner, dmax):
    """Yield coordinate for the left border for a given corner."""
    for y in range(dmax, corner, -1):
        yield corner, y


def border_coords(corner, dmax):
    """Yield coordinate for the border defined by a given corner."""
    yield from top_border_coords(corner, dmax)
    yield from left_border_coords(corner, dmax)
    yield corner, corner


def refine_risk(grid, corner):
    """Visit each potentially unstable coord, refining its min risk."""

    dmax = len(grid) - 1
    changed = 0

    def expanding_border_coords(corner):
        for i, c in enumerate(range(corner, -1, -1)):
            yield from border_coords(c, dmax)
            # TODO: This escape uses an un-verified heuristic. One day it would
            #       be good to verify it, but it seems to work and I could add
            #       a full grid pass to prove the grid is stable.
            if i > 3 and changed:
                break

    def calc_risk(x, y, offsets):
        nonlocal changed, corner

        risk, min_risk = grid[y][x]
        choices = []
        for dx, dy in offsets:
            xc, yc = x + dx, y + dy
            if 0 <= xc <= dmax and 0 <= yc <= dmax:
                choices.append(grid[yc][xc][1])
        alt_risk = min(risk + total for total in choices)
        if alt_risk < min_risk:
            grid[y][x] = risk, alt_risk
            changed += 1
            if changed == 1:
                corner = min(x, y)

    neighbours = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for x, y in expanding_border_coords(corner):
        calc_risk(x, y, neighbours)

    return changed, corner


def find_smallest_risk(expand=False):
    """Find the value for the route with the lowest risk."""
    input_grid = parse_risk_grid(expand)
    grid = [[[risk, None] for risk in row] for row in input_grid]

    # Mark the destination cell with its minimum risk and make it our
    # initial wall.
    dmax = len(grid) - 1
    x = y = dmax
    risk, _ = grid[y][x]
    grid[y][x] = risk, risk
    corner = dmax

    for corner in range(dmax - 1, -1, -1):
        add_initial_best_risk(grid, corner)

    if debug:
        for row in grid:
            print([f'{str(v):9}' for v in row])

    n = 0
    cc = 1
    corner = dmax - 1
    while cc:
        cc, corner = refine_risk(grid, corner)
        n += 1

    if debug:
        print()
        for row in grid:
            print([f'{str(v):9}' for v in row])

    risk, min_risk = grid[0][0]
    print(min_risk - risk)


debug = False
find_smallest_risk()
find_smallest_risk(expand=True)
