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

    return grid


def add_best_risks(grid, corner):
    """A properly viable approach, expanding outward from the finish."""

    # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    xc, yc = corner
    ylen = len(grid)
    xlen = len(grid[0])

    def calc_risk(x, y, offsets):
        risk, _ = grid[y][x]
        choices = []
        for dx, dy in offsets:
            xc, yc = x + dx, y + dy
            if xc < xlen and yc < ylen:
                choices.append(grid[yc][xc][1])
        grid[y][x] = risk, min(risk + total for total in choices)

    for x, y in [(xx, yc - 1) for xx in range(xc, xlen)]:
        calc_risk(x, y, [(0, 1)])
    for x, y in [(xc - 1, yy) for yy in range(yc, ylen)]:
        calc_risk(x, y, [(1, 0)])
    calc_risk(xc - 1, yc - 1, [(1, 0), (0, 1)])

    xc = max(xc - 1, 0)
    yc = max(yc - 1, 0)
    return xc, yc


def refine_risk(grid, recalc_start):
    """Yada."""

    ymax = len(grid) - 1
    xmax = len(grid[0]) - 1
    changed = 0

    def border_coords(xb, yb):
        x, y = xmax, ymax
        for x in range(xmax, xb, -1):
            yield x, yb
        for y in range(ymax, yb, -1):
            yield xb, y
        yield xb, yb

    def expanding_border_coords(cb):
        for i, c in enumerate(range(cb, -1, -1)):
            yield from border_coords(c, c)
            if i > 3 and changed:
                break

    def calc_risk(x, y, offsets):
        nonlocal changed, recalc_start

        risk, min_risk = grid[y][x]
        choices = []
        for dx, dy in offsets:
            xc, yc = x + dx, y + dy
            if 0 <= xc <= xmax and 0 <= yc <= ymax:
                choices.append(grid[yc][xc][1])
        alt_risk = min(risk + total for total in choices)
        if alt_risk < min_risk:
            grid[y][x] = risk, alt_risk
            changed += 1
            if changed == 1:
                recalc_start = min(x, y)

    recalc_start = recalc_start or (xmax, ymax)
    neighbours = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for x, y in expanding_border_coords(recalc_start):
        calc_risk(x, y, neighbours)

    return changed, recalc_start


def find_smallest_risk(expand=False):
    """Yada."""
    input_grid = parse_risk_grid(expand)
    grid = [[[risk, None] for risk in row] for row in input_grid]

    # Mark the destination cell with its minimum risk and make it our
    # initial wall.
    y = len(grid) - 1
    x = len(grid[0]) - 1
    risk, _ = grid[y][x]
    grid[y][x] = risk, risk
    corner = x, y

    while corner != (0, 0):
        corner = add_best_risks(grid, corner)

    if debug:
        for row in grid:
            print([f'{str(v):9}' for v in row])

    n = 0
    cc = 1
    recalc_start = len(grid) - 2
    while cc:
        cc, recalc_start = refine_risk(grid, recalc_start)
        n += 1
        # print(n, cc, recalc_start)

    if debug:
        print()
        for row in grid:
            print([f'{str(v):9}' for v in row])

    risk, min_risk = grid[0][0]
    print(min_risk - risk)


debug = False
find_smallest_risk()
find_smallest_risk(expand=True)
