"""Paul's solution for AOC day 23."""

import sys
from itertools import count
from typing import List, Optional

from lib import data_lines, windowize, watch_counter

MAX_COST = 999_999_999_999_999

move_energy = dict(A=1, B=10, C=100, D=1000)

wc = watch_counter(100)

sys.setrecursionlimit(sys.getrecursionlimit() * 10)

class Amphipod:                        # pylint: disable=too-few-public-methods
    """An amphipod of a given type."""
    ids = count()

    def __init__(self, name):
        self.name = name
        self.cell: Optional['Cell'] = None
        self.idx = next(self.ids)

    def permitted_moves(self) -> List:
        """The set of permitted next moves for this amphipod."""
        if self.area.complete:
            print(f'{self.name} - {self.area.name}: Complete - no moves')
            return []

        if self.in_corridor:
            # print('In corridor', self.cell, self.cell.in_corridor)
            for c in self.cell.empty_neighbours():
                route = self.find_route_home(self.cell, c)
                if route:
                    return [route]
            return []

        moves = []
        cells = self.cell.empty_neighbours()
        cpm = move_energy[self.name]
        for c in cells:
            if c.occupiable:
                moves.append((cpm, c))
            else:
                for cc in c.empty_neighbours():
                    if cc is not c:
                        moves.append((cpm * 2, cc))
        return moves

    def find_route_home(self, prev: 'Cell', cell: 'Cell'):
        """Find a route to the home room."""
        if cell.area.name == self.name:
            # Home has been reached. We may be able to move further in or
            # else the existing occupier must be compatible.
            below = cell.below
            if below.amphipod:
                if below.name == self.name:
                    return [cell, below]
            else:
                return [cell]

        for c in cell.empty_neighbours():
            if c is not prev:
                route = self.find_route_home(cell, c)
                if route:
                    return [cell] + route

        return []

    @property
    def area(self):
        """The area this amphipod is in."""
        return self.cell.area

    @property
    def in_corridor(self):
        """Test if currently in the corridor."""
        return self.cell.in_corridor

    def __str__(self):
        return f'{self.name}[{self.idx}]'

    def __repr__(self):
        return self.__str__()


class Cell:                      # pylint: disable=too-many-instance-attributes
    """A burrow cell that may be empty or contain an amphipod."""
    # pylint: disable=too-few-public-methods
    def __init__(self, name, area:'Area', amphipod: Optional[Amphipod] = None):
        self.cell_name = name
        self.area = area
        self.amphipod = amphipod
        self.left: Optional['Cell'] = None
        self.above: Optional['Cell'] = None
        self.right: Optional['Cell'] = None
        self.below: Optional['Cell'] = None
        self.target = None
        self.occupiable = True

    @property
    def in_corridor(self):
        """Test if this cell is in the corridor."""
        return True

    def empty_neighbours(self):
        """A list of all unoccupied neighbours."""
        neighbours = [self.left, self.right, self.above, self.below]
        neighbours = [n for n in neighbours if n]
        return [n for n in neighbours if not n.amphipod]

    def name(self):
        """The name of this cell's amphipod."""
        if self.amphipod:
            return self.amphipod.name
        else:
            return '.'

    def __str__(self):
        return f'CC-{self.cell_name}[{self.amphipod  or " "}]'

    def __repr__(self):
        return self.__str__()


class RoomCell(Cell):
    """A burrow cell withina room."""

    @property
    def in_corridor(self):
        """Test if this cell is in the corridor."""
        return False

    def __str__(self):
        return f'RC-{self.cell_name}[{self.amphipod  or " "}]'


class Area:                            # pylint: disable=too-few-public-methods
    """An area within the burrow."""
    def __init__(self):
        self.cells = []
        self.name = ''


class Room(Area):                  # pylint: disable=too-few-public-methods
    """A room within the burrow."""
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @property
    def complete(self):
        """Test if this room is completed."""
        return all(self.name == c.name() for c in self.cells)


class Corridor(Area):             # pylint: disable=too-few-public-methods
    """The corridor within the burrow."""

    @property
    def complete(self):
        """Test if this room is completed."""
        return False


def parse_input() -> List[Cell]:
    """Parse the reactor sequence."""
    lines = data_lines(__file__)
    next(lines)
    corridor = Corridor()
    cells = [
        Cell(f'CC{i}', corridor)
        for i, ch in enumerate(next(lines)) if ch == '.']
    corridor.cells[:] = cells

    for a, b in windowize(cells, 2):
        a.right = b
        b.left = a

    rooms = [Room(ch) for ch in 'ABCD']
    amphipods = []
    occupants = (
        (i, ch) for i, ch in enumerate(next(lines), -1) if ch not in '# ')
    for k, (room, (i, ch)) in enumerate(zip(rooms, occupants)):
        ap = Amphipod(ch)
        c_cell = cells[i]
        c_cell.occupiable = False
        cell = ap.cell = RoomCell(f'R{k}a', room, ap)
        cell.above = c_cell
        c_cell.below = cell
        room.cells.append(cell)
        amphipods.append(ap)

    occupants = (
        (i, ch) for i, ch in enumerate(next(lines), -1) if ch not in '# ')
    for k, (room, (i, ch)) in enumerate(zip(rooms, occupants)):
        ap = Amphipod(ch)
        c_cell = cells[i].below
        cell = ap.cell = RoomCell(f'R{k}b', room, ap)
        cell.above = c_cell
        c_cell.below = cell
        amphipods.append(ap)
        room.cells.append(cell)

    return amphipods, corridor, rooms


def position(amphipods):
    """Create position spec."""
    return tuple((ap, ap.cell) for ap in amphipods)


def next_moves(amphipods: List[Amphipod]):
    """All permitted next moves from the current position."""
    moves = []
    for ap in amphipods:
        for cost, next_cell in ap.permitted_moves():
            moves.append((ap, cost, next_cell))
    return moves


def dump_pos(corridor, rooms):
    """Yada."""
    print(''.join(c.name() for c in corridor.cells))
    s = ' '.join(room.cells[0].name() for room in rooms)
    print(f'  {s}')
    s = ' '.join(room.cells[1].name() for room in rooms)
    print(f'  {s}')


def thingy(
        amphipods: List[Amphipod],
        cost_so_far: int,
        min_cost: int,
        positions,
        corridor,
        rooms,
    ) -> int:
    """Todo."""
    next(wc)
    for ap, move_cost, cell in next_moves(amphipods):
        # print('M', ap, move_cost, cell)

        saved_cell = ap.cell
        ap.cell = cell
        cell.amphipod = ap
        saved_cell.amphipod = None

        pos = position(amphipods)
        if pos not in positions:
            dump_pos(corridor, rooms)
            if all(room.complete for room in rooms):
                print("Yes!", cost_so_far + move_cost)
            else:
                positions.add(pos)
                min_cost = thingy(
                    amphipods,
                    cost_so_far + move_cost,
                    min_cost,
                    positions,
                    corridor,
                    rooms,
                )

        ap.cell = saved_cell
        saved_cell.amphipod = ap
        cell.amphipod = None

    return min_cost


def solve():
    """Solve the puzzle."""
    # pylint: disable=unused-variable
    amphipods, corridor, rooms = parse_input()
    for c in corridor.cells:
        print(c, end='')
        if c.below:
            print(" ->", c.below, end='')
            if c.below.below:
                print(" ->", c.below.below, end='')
        print()

    dump_pos(corridor, rooms)
    cost = 0
    positions = set()
    positions.add(position(amphipods))
    min_cost = thingy(
        amphipods,
        0,
        MAX_COST,
        positions,
        corridor,
        rooms,
    )
    print(min_cost)


def solve2():
    """Solve the puzzle, part 2."""
    print(1)


solve()
# solve2()
