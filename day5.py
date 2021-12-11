"""Paul's solution for AOC day 5."""

from dataclasses import dataclass
from itertools import cycle
from typing import Iterator, Sequence, Iterable

from lib import data_lines


@dataclass
class Point:
    """"A simple point."""
    x: int
    y: int

    @classmethod
    def from_string(cls, s: str) -> 'Point':
        """Create a Point from a sting of the form 'x,y'."""
        return cls(*[int(c) for c in s.split(',')])


@dataclass
class Vector:
    """A simple vector."""
    a: Point
    b: Point

    @classmethod
    def from_string(cls, s: str) -> 'Vector':
        """Create a Vector from a sting of the form 'x1,y1 -> x2,y2'."""
        return cls(*[Point.from_string(c) for c in s.split(' -> ')])

    def coords(self) -> Iterator[Point]:
        """Generate all coordinates for a vector.

        This will only produce correct results for a vector with an angle that
        is a multiple of 45°.
        """
        xr: Iterable[int]
        yr: Iterable[int]

        a, b = self.a, self.b
        if a.x == b.x:
            xr, yr = cycle([a.x]), fs_range(a.y, b.y)
        elif a.y == b.y:
            xr, yr = fs_range(a.x, b.x), cycle([a.y])
        else:
            xr, yr = fs_range(a.x, b.x), fs_range(a.y, b.y)
        return (Point(x, y) for x, y in zip(xr, yr))

    def is_vertical_or_horizontal(self) -> bool:
        """Test whether this vector is vertical or horizonal."""
        a, b = self.a, self.b
        return a.x == b.x or a.y == b.y

    @property
    def max_x(self) -> int:
        """Maximum X coordinate."""
        return max(self.a.x, self.b.x)

    @property
    def max_y(self) -> int:
        """Maximum Y coordinate."""
        return max(self.a.y, self.b.y)


def fs_range(a: int, b:int) -> range:
    """A range, handling when b < a and including both a and b."""
    if b < a:
        return range(a, b - 1, -1)
    else:
        return range(a, b + 1)


def parse_vent_data() -> Iterator[Vector]:
    """Parse the vent data.

    This reads in each vector value, yielding Vector instances.
    """
    yield from (Vector.from_string(line) for line in data_lines(__file__))


def get_vector_hits(vectors: Sequence[Vector], inc_diagonal=False) -> int:
    """Work out the number of lines crossing each point.

    :return: The number of points crossed by 2 or more vectors.
    """
    x_dim = max(v.max_x for v in vectors) + 1
    y_dim = max(v.max_y for v in vectors) + 1
    grid = [[0] * x_dim for _ in range(y_dim)]

    for v in vectors:
        if inc_diagonal or v.is_vertical_or_horizontal():
            for p in v.coords():
                grid[p.y][p.x] += 1

    zeros = sum(row.count(0) for row in grid)
    ones = sum(row.count(1) for row in grid)
    return x_dim * y_dim - zeros - ones


def find_scary_vent_points():
    """Find the most scary vent positions."""
    print(get_vector_hits(list(parse_vent_data())))


def find_scary_vent_points2():
    """Find the most scary vent positions."""
    print(get_vector_hits( list(parse_vent_data()), inc_diagonal=True))


find_scary_vent_points()
find_scary_vent_points2()
