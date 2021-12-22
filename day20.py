"""Paul's solution for AOC day 20."""

from collections import Counter
from itertools import chain
from typing import List, Literal, Tuple

from lib import data_lines, windowize


Bit = Literal[0, 1]
Program = List[Bit]
Image = List[List[Bit]]


def parse_input() -> Tuple[Program, Image]:
    """Parse the program and image data.

    The first line is the program. The 3rd and subsequent lines are rows of the
    image. Within the image and program '#' is 'on' (1) and '.' is 'off' (0).
    """
    lkup = {'#': 1, '.': 0}
    lines = data_lines(__file__)

    program = [lkup[c] for c in next(lines)]
    next(lines)
    return program, [[lkup[c] for c in line] for line in lines]


def add_infinity_border(image: Image, pixel: Bit) -> Image:
    """Add a border to act as the inifinite part of an immage.

    Add a border of 3 pixels around the image to act as a suitable amount of
    the infinite extent.
    """
    ncols = len(image[0]) + 6
    new_image = [[pixel] * ncols for _ in range(3)]
    new_image.extend([[pixel] * 3 + row + [pixel] * 3 for row in image])
    new_image.extend([[pixel] * ncols for _ in range(3)])
    return new_image


def trim_unprocessed_infinity(image: Image) -> Image:
    """Trim the part of the infinity border that was not processed.

    This is a single pixel border around the image.
    """
    return [row[1:-1] for row in image[1:-1]]


def trim_unlit_border(image: Image) -> Image:
    """Trim any unlit border from the image."""
    new_image = image
    for i, row in enumerate(new_image):
        if any(row):
            new_image = new_image[i:]
            break
    while not any(new_image[-1]):
        new_image.pop()

    start = min(row.index(1) for row in new_image)
    for row in new_image:
        row.reverse()
    end = min(row.index(1) for row in new_image)
    for row in new_image:
        row.reverse()

    n = len(image[0]) - end
    new_image = [row[start:n] for row in new_image]
    return new_image


def new_blank_image(image: Image):
    """Create a new blank image or equal dimensions."""
    n = len(image[0])
    return [[0] * n for _ in image]


def process(image: Image, program: Program) -> Image:
    """Process the image using the program."""
    # pylint: disable=too-many-locals

    result = new_blank_image(image)
    for ri, (ra, rb, rc) in enumerate(windowize(image, 3), 1):
        ra_win = windowize(ra, 3)
        rb_win = windowize(rb, 3)
        rc_win = windowize(rc, 3)
        for ci, (ba, bb, bc) in enumerate(zip(ra_win, rb_win, rc_win), 1):
            n = 0
            for d in chain(ba, bb, bc):
                n = (n << 1) | d

            result[ri][ci] = program[n]

    return result


def dump_image(image: Image, lkup: str = ' #'):
    """Dump aeasily readable version of the image."""
    for row in image:
        print(''.join(lkup[c] for c in row))


def solve(count: int):
    """Solve the puzzle."""
    program, image = parse_input()

    border_value = 0
    for i in range(count):
        image = add_infinity_border(image, border_value)
        image = process(image, program)
        image = trim_unprocessed_infinity(image)
        border_value = image[0][0]
        if i % 2 == 1:
            image = trim_unlit_border(image)

    # dump_image(image)

    counts = Counter(chain(*image))
    print(counts[1])


solve(2)
solve(50)
