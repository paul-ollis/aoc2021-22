"""Paul's solution for AOC day 17."""

from typing import List, Tuple, Iterator

from lib import data_lines


def parse_input() -> List[int]:
    """Parse the target area input.

    The input has the formL

        target area: x=20..30, y=-10..-5
    """
    line = next(data_lines(__file__))
    _, _, s = line.partition(': ')
    xs, _, ys = s.partition(', ')
    _, _, xs = xs.partition('=')
    _, _, ys = ys.partition('=')
    xss, _, xes = xs.partition('..')
    yss, _, yes = ys.partition('..')

    return [int(s) for s in (xss, xes, yss, yes)]


class Trajectory:
    """Information about a probe trajectory."""
    def __init__(
            self, xvel: int, yvel: int, target: Tuple[int, int , int, int]):
        self.xvel = xvel
        self.yvel = yvel
        self.target = target

        self.max_y = 0
        for (self.x, _), self.y in zip(x_pos_vel(xvel), y_pos(yvel)):
            self.max_y = max(self.max_y, self.y)
            if self.hit or self.overshot_x or self.overshot_y:
                break

    @property
    def hit(self) -> bool:
        """True if this trajectory has hit the target"""
        xa, xb, ya, yb = self.target
        return ya <= self.y <= yb and xa <= self.x <= xb

    @property
    def overshot_x(self) -> bool:
        """True if this trajectory has overshot right edge of the target"""
        _, xb, *_= self.target
        return self.x > xb

    @property
    def overshot_y(self) -> bool:
        """True if this trajectory has overshot bottom edge of the target"""
        *_, ya, _= self.target
        return self.y < ya


def x_pos_vel(initial: int) -> Iterator[int]:
    """Iterate X position and velocity given an inital velocity."""
    x = 0
    xvel = initial
    while True:
        yield x, xvel
        x += xvel
        if xvel > 0:
            xvel -= 1


def y_pos(initial: int) -> Iterator[int]:
    """Iterate Y position given an inital velocity."""
    y = 0
    yvel = initial
    while True:
        yield y
        y += yvel
        yvel -= 1


def solve():
    """Solve the puzzle..."""
    target = parse_input()
    xa, xb, ya, _ = target

    # Work out viable range of initial X velocities.
    possible_xvels = []
    for xvel in range(0, xb + 1):
        for x, xv in x_pos_vel(xvel):
            if xa <= x <= xb:
                possible_xvels.append(xvel)
                break
            if (x < xa and xv == 0) or x > xb:
                break

    hits = []
    for xvel in possible_xvels:
        for yvel in range(ya, -ya):
            t = Trajectory(xvel, yvel, target)
            if t.hit:
                hits.append(t)
            elif t.overshot_x or t.overshot_y and yvel >= -ya:
                break

    print(max(t.max_y for t in hits))
    print(len(hits))


solve()
