"""Paul's solution for AOC day 13."""

from itertools import zip_longest
from typing import List, Tuple

from lib import data_lines

my_code = '''
###   ##  #  # #### ###  ####   ##  ##
#  # #  # #  #    # #  # #       # #  #
#  # #    ####   #  ###  ###     # #
###  # ## #  #  #   #  # #       # #
#    #  # #  # #    #  # #    #  # #  #
#     ### #  # #### ###  #     ##   ##
'''
my_code_str = 'PGHZBFJC'


def parse_code_page() -> Tuple[List[List[int]], List[Tuple[str, int]]]:
    """Parse the code page (page 1) of the thermal camera.

    The input starts with a sequence of coordinates of the form (col_idx,
    row_idx). Ihe second half is a sequence of instriction of the form:

        fold along x=4
        fold along y=8

    This parser produces an image of the paper organised as a list of rows,
    where each row is a list of integers. A zero indicate no dot and the value
    1 represents a dot.
    """
    coords: List[Tuple[int, int]] = []
    lines = data_lines(__file__)
    for line in lines:
        if not line:
            break

        a, b, *_ = tuple(int(v) for v in line.split(','))
        coords.append((a, b))

    folds: List[Tuple[str, int]] = []
    for line in lines:
        _, _, fold_line = line.rpartition(' ')
        direction, s_value = fold_line.split('=')
        folds.append((direction, int(s_value)))

    num_cols = max(c for c, _ in coords) + 1
    num_rows = max(r for _, r in coords) + 1
    paper: List[List[int]] = [[0] * num_cols for _ in range(num_rows)]
    for c, r in coords:
        paper[r][c] = 1
    return paper, folds


def fold_along_y(paper: List[List[int]], y: int) -> List[List[int]]:
    """Fold the paper along a y coordinate."""
    top, bottom = paper[:y], paper[y+1:]
    result: List[List[int]] = []
    lzip = zip_longest
    for topline, bottomline in lzip(reversed(top), bottom, fillvalue=[]):
        result.append(
            [a | b for a, b in lzip(topline, bottomline, fillvalue=0)])
    return list(reversed(result))


def fold_along_x(paper: List[List[int]], x: int) -> List[List[int]]:
    """Fold the paper along an x coordinate."""
    lzip = zip_longest
    result: List[List[int]] = []

    for row in paper:
        left, right = row[:x], row[x+1:]
        result.append(list(reversed(
            [a | b for a, b in lzip(reversed(left), right, fillvalue=0)])))
    return result


def perform_fold(
        paper: List[List[int]], fold: tuple[str, int]) -> List[List[int]]:
    """Performa given fold.

    :paper: The paper to fold.
    :fold:  The fold instruction as a tuple of coord-name, value. For example
            ('x', 7).
    """
    coord_name, coord = fold
    if coord_name == 'y':
        return fold_along_y(paper, coord)
    else:
        return fold_along_x(paper, coord)


def fold_once():
    """Just perform the first paper fold."""
    paper, folds = parse_code_page()
    for fold in folds:
        paper = perform_fold(paper, fold)
        break

    print(sum(row.count(1) for row in paper))


def fold_completely():
    """Perform all the paper folds."""
    paper, folds = parse_code_page()
    for fold in folds:
        paper = perform_fold(paper, fold)

    lkup = {0: ' ', 1: '#'}
    big_code = '\n' + '\n'.join(
        ''.join(lkup[v] for v in row).rstrip() for row in paper)
    big_code += '\n'
    if big_code == my_code:
        print(my_code_str)
    else:
        print(repr(big_code))
        print(big_code)
        print(repr(my_code))
        print(my_code)


fold_once()
fold_completely()
