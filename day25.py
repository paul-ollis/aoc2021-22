"""Paul's solution for AOC day 25."""

import numpy as np                               # pylint: disable=import-error

from lib import data_lines, windowize


def half_step(grid, sc):
    """Perform half of a single step."""
    n = 0
    for row in grid:
        to_move = [
            i for i, (a, b) in enumerate(windowize(row, 2))
            if a == sc and b == '.']
        if row[0] == '.' and row[-1] == sc:
            row[0] = row[-1]
            row[-1] = '.'
            n += 1
        for i in to_move:
            row[i + 1] = row[i]
            row[i] = '.'
            n += 1

    return n


def dump(grid):
    """Print the sea cucumber grid."""
    for row in grid:
        print(''.join(row))
    print("----------")


def solve():
    """Solve the puzzle."""
    lines = list(data_lines(__file__))
    nx = len(lines[0])
    ny = len(lines)
    print(nx, ny)
    grid = np.array([list(line) for line in lines])

    t_grid = grid.T
    dump(grid)

    n = 1
    i = 0
    while n > 0:
        n = half_step(grid, '>')
        n += half_step(t_grid, 'v')
        i += 1
        # print(i, n)
        # dump(grid)

    dump(grid)
    print(i)


solve()
