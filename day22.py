"""Paul's solution for AOC day 22."""

from itertools import product
from typing import List, Tuple

from lib import data_lines, range_intersection


Instruction = Tuple[int, 'Cuboid']


class Cuboid:
    """Simple representation of a cube."""
    def __init__(self, xr: range, yr: range, zr: range):
        self.xr = xr
        self.yr = yr
        self.zr = zr

    def intersection(self, other: 'Cuboid'):
        """Get the intersection with another cuboid."""
        ri = range_intersection
        o = other
        return Cuboid(ri(self.xr, o.xr), ri(self.yr, o.yr), ri(self.zr, o.zr))

    def explode(self, embedded: 'Cuboid') -> List['Cuboid']:
        """Explode this cuboid around another embedded cuboid.

        This creates up to 6 new cuboids that fit around the embedded cuboid to
        form a cuboid that matches this one. Empty cuboids are not included in
        the returned set.
        """
        ret = []
        c, e = self, embedded

        # Split into 3 along the X axis.
        ret.append(Cuboid(range(c.xr.start, e.xr.start), c.yr, c.zr))
        ret.append(Cuboid(range(e.xr.stop, c.xr.stop), c.yr, c.zr))
        c = Cuboid(range(e.xr.start, e.xr.stop), c.yr, c.zr)
        ret = [c for c in ret if c]

        # Split the middle cuboid along the Y axiz in the same way.
        ret.append(Cuboid(c.xr, range(c.yr.start, e.yr.start), c.zr))
        ret.append(Cuboid(c.xr, range(e.yr.stop, c.yr.stop), c.zr))
        c = Cuboid(c.xr, range(e.yr.start, e.yr.stop), c.zr)
        ret = [c for c in ret if c]

        # Finally split the second middle cuboid along the Z axiz to get the
        # finally two new cuboids.
        ret.append(Cuboid(c.xr, c.yr, range(c.zr.start, e.zr.start)))
        ret.append(Cuboid(c.xr, c.yr, range(e.zr.stop, c.zr.stop)))
        ret = [c for c in ret if c]

        return [c for c in ret if c]

    @property
    def count(self):
        """The number of cells in this cuboid."""
        return len(self.xr) * len(self.yr) * len(self.zr)

    def cells(self):
        """Iterate over all this cuboid's cell coordiantes."""
        yield from product(self.xr, self.yr, self.zr)

    def __str__(self):
        rngs = [f'{r.start}..{r.stop}' for r in (self.xr, self.yr, self.zr)]
        return f'Cuboid({" : ".join(rngs)})'

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return bool(self.xr and self.yr and self.zr)


def parse_input() -> List[Instruction]:
    """Parse the reactor sequence."""
    lkup = dict(off=0, on=1)
    instrs = []
    for line in data_lines(__file__):
        a, b = line.split(' ')
        ranges = [
            tuple(int(s) for s in p)
                for p in (r.split('..')
                    for r in (c[2:] for c in b.split(',')))
        ]
        ranges = [range(a, b + 1) for a, b in ranges]
        instrs.append((lkup[a], Cuboid(*ranges)))

    return instrs


def split_around_intersection(cuboid: Cuboid, other: Cuboid):
    """Split a cuboid if it interescts with the other.

    The new cuboids replace the non-intersected volume. If there is no
    intersection the the returned list contains just the original cuboid.
    """
    intersection = cuboid.intersection(other)
    if not intersection:
        return [cuboid]

    return cuboid.explode(intersection)


def initialise():
    """Solve the puzzle."""
    operations = parse_input()
    on_cuboids: List[Cuboid] = []
    for state, cuboid in operations:
        temp = []
        for on_cuboid in on_cuboids:
            replaced = split_around_intersection(on_cuboid, cuboid)
            temp.extend(replaced)
        if state:
            temp.append(cuboid)
        on_cuboids[:] = temp
    return on_cuboids



def solve():
    """Solve the puzzle."""
    on_cuboids = initialise()
    init_cuboid = Cuboid(range(-50, 51), range(-50, 51), range(-50, 51))
    print(sum(c.intersection(init_cuboid).count for c in on_cuboids))


def solve2():
    """Solve the puzzle, part 2."""
    on_cuboids = initialise()
    print(f'{sum(c.count for c in on_cuboids):_}')


solve()
solve2()
