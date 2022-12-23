"""Paul's solution for AOC day 23."""

import sys
from typing import List, Tuple
from collections import defaultdict

from lib import data_lines, watch_counter

MAX_COST = 999_999_999_999_999

move_costs = dict(A=1, B=10, C=100, D=1000)

wc = watch_counter(1000000)

sys.setrecursionlimit(sys.getrecursionlimit() * 10)

PositionEntry = Tuple[Tuple[int, int], str]

# This is the final position we are aiming for.
target_position = {}
corridor = set(list(target_position.keys())[:11])
homes = {'A': (2, 2), 'B': (2, 4), 'C': (2, 6), 'D': (2, 8)}

positions = defaultdict(lambda: MAX_COST)


class saved_state:
    """Context manager to save and restore thingy."""
    def __init__(self, position):
        self.position = position
        self.saved_position = {}

    def __enter__(self):
        self.saved_position = dict(self.position)

    def __exit__(self, *args, **kwargs):
        self.position.update(self.saved_position)


def create_target_position(room_size):
    """Create the end (target) position."""
    t = dict((
        *(((0, i), ' ') for i in range(11)),
        *(((1, 2), 'A'), ((1, 4), 'B'), ((1, 6), 'C'), ((1, 8), 'D')),
        *(((2, 2), 'A'), ((2, 4), 'B'), ((2, 6), 'C'), ((2, 8), 'D'))))
    if room_size == 4:
        t.update(dict((
        *(((3, 2), 'A'), ((3, 4), 'B'), ((3, 6), 'C'), ((3, 8), 'D')),
        *(((4, 2), 'A'), ((4, 4), 'B'), ((4, 6), 'C'), ((4, 8), 'D')))))
    target_position.clear()
    target_position.update(t)


def create_move_sets(room_size):
    """Create exit_move_sets and home_move_sets.

    These contain all the single-step move sequences that are both permitted
    and useful; ignoring the which cells are currently occupied."""
    # pylint: disable=too-many-locals,disable=redefined-outer-name
    coords = list(target_position)
    exit_move_sets.clear()
    x_openings = (2, 4, 6, 8)
    a, b = 11, 15
    for _ in range(room_size):
        for coord in coords[a:b]:
            ys, xs = coord
            ascent = [(y, xs) for y in range(ys - 1, -1, -1)]
            moves = []

            for xstop in range(xs - 1, -1, -1):
                if xstop in x_openings:
                    continue
                move = list(ascent)
                for x in range(xs - 1, xstop - 1, -1):
                    move.append((0, x))
                moves.append(move)

            for xstop in range(xs + 1, 11):
                if xstop in x_openings:
                    continue
                move = list(ascent)
                for x in range(xs + 1, xstop + 1):
                    move.append((0, x))
                moves.append(move)

            exit_move_sets[coord] = moves

        a, b = a + 4, b + 4

    for coord in coords[15:]:
        ys, xs = coord
        above = ys - 1, xs
        exit_move_sets[coord] = [
            [above] + moves for moves in exit_move_sets[above]]

    # hh = dict((b, a) for a, b in homes.items())
    home_move_sets.clear()
    home_move_sets.update({'A': {}, 'B': {}, 'C': {}, 'D': {}})
    ys = 2 if room_size == 2 else 4
    for y in range(ys, 0, -1):
        homes = ((y, 2), (y, 4), (y, 6), (y, 8))
        for move_sets, coord in zip(home_move_sets.values(), homes):
            for exit_move in exit_move_sets[coord]:
                start = exit_move[-1]
                move = list(reversed(exit_move[:-1]))
                move_sets.setdefault(start, []).append(move + [coord])


def dump_pos(position):
    """Dump a user friendly version of a burrow position."""
    def sym(c):
        return c if c in 'ABCD' else '.'

    pos_chars = list(position.values())
    n = len(position)
    print(''.join(sym(e) for e in pos_chars[:11]))
    for a in range(11, n, 4):
        print(' ', ' '.join(sym(e) for e in pos_chars[a:a + 4]))


def parse_input(room_size) -> List[PositionEntry]:
    """Parse the amphipod starting positions.

    :return:
        A dictionary of cell states. The key is a cell coordinate as (y, x)
        and the value is a amphipod name ('A' to 'D') or a space.
    """
    lines = data_lines(__file__)
    next(lines)
    next(lines)

    position = [((0, i), ' ') for i in range(11)]

    coords = ((1, 2 + i * 2) for i in range(4))
    amphipods = (c for c in next(lines) if c not in '# ')
    position.extend(zip(coords, amphipods))

    if room_size == 2:
        y = 2
    else:
        coords = ((2, 2 + i * 2) for i in range(4))
        position.extend(zip(coords, 'DCBA'))
        coords = ((3, 2 + i * 2) for i in range(4))
        position.extend(zip(coords, 'DBAC'))
        y = 4

    coords = ((y, 2 + i * 2) for i in range(4))
    amphipods = (c for c in next(lines) if c not in '# ')
    position.extend(zip(coords, amphipods))

    return dict(sorted(position))


def already_home(position, coord, ap):
    """Test is a amphipod is already home."""
    y, x = coord
    if y == 2:
        return target_position[coord] == ap
    elif y == 1:
        wanted_ap = target_position[coord]
        if wanted_ap == ap:
            return position[(2, x)] == wanted_ap
    return False


def permitted_exit_moves(position, coord):
    """Find all permitted moves from a coordinate, for a given position.

    The coordinate is assumed to contain an amphipod.
    """
    move_sets = []
    ap = position[coord]
    for move in exit_move_sets[coord]:
        for cell in move:
            if position[cell] != ' ':
                break
        else:
            move_sets.append((move_costs[ap] * len(move), coord, move[-1]))

    return move_sets


def permitted_home_move(position, start_coord):
    """Find a move that places an amphipod it its correct room.

    The coordinate is assumed to contain an amphipod.
    """
    # Walk the longest home move. If any cell is occupied then we can go no
    # further. If that cell is occupied by a different type of amphipod then no
    # home moves are possible.
    ap = position[start_coord]
    possible_moves = home_move_sets[ap][start_coord]
    longest_move = possible_moves[0]
    end_pos = len(longest_move)
    for i, coord in enumerate(longest_move):
        r_ap = position[coord]
        if r_ap != ' ':
            if r_ap != ap or coord[0] <= 1:
                return []
            end_pos = min(end_pos, i)

    move = longest_move[:end_pos]
    return [(move_costs[ap] * len(move), start_coord, move[-1])]


def find_home_fillers(position):
    """Find the coordinates of all rooms that are now being filled."""
    ymax, _ = list(position)[-1]
    fillers = set()
    for x, ap in ((2, 'A'), (4, 'B'), (6, 'C'), (8, 'D')):
        room = set()
        for y in range(ymax, 0, -1):
            if position[(y, x)] not in (' ', ap):
                break
            room.add((y, x))
        else:
            fillers.update(room)

    return fillers


def all_exit_moves(position):
    """Find all permitted room exiting moves.

    The returned set of moves is sorted with the lowest cost moves first.
    """
    all_move_sets = []
    coords = list(position)
    being_filled = find_home_fillers(position)
    for coord in coords[11:]:
        ap = position[coord]
        if ap == ' ':
            continue
        if coord in being_filled:
            continue
        all_move_sets.extend(permitted_exit_moves(position, coord))

    return sorted(all_move_sets)


def all_home_moves(position):
    """Find all permitted, home moves for a given position."""
    all_move_sets = []
    coords = list(position)
    for coord in coords[:11]:
        ap = position[coord]
        if ap != ' ':
            all_move_sets.extend(permitted_home_move(position, coord))
    return all_move_sets


def seen(position, cost, check_only=True):
    """Check if a position has already been seen."""
    k = tuple(position.items())
    if positions[k] <= cost:
        return True
    if check_only:
        return False
    positions[k] = cost
    return False


def add_dead_positions(position, cost_so_far):
    """Add additional dead-end positions.

    This is called when no further moves are possible, which means the corridor
    is full. In such a case, there could be up to 3 other related positions
    that are also dead ends. For example::

        .C.A.B.B.C.    C..A.B.B.C.   .C.A.B.B..C    C..A.B.B..C
          . . . .        . . . .       . . . .        . . . .
          D D . A        D D . A       D D . A        D D . A
    """
    with saved_state(position):
        pos = position
        swap_left = ' ' in (pos[(0, 0)], pos[(0, 1)])
        if swap_left:
            pos[(0, 0)], pos[(0, 1)] = pos[(0, 1)], pos[(0, 0)]
            seen(pos, cost_so_far, check_only=False)
        if ' ' in (pos[(0, 9)], pos[(0, 10)]):
            pos[(0, 9)], pos[(0, 10)] = pos[(0, 10)], pos[(0, 9)]
            seen(pos, cost_so_far, check_only=False)
        if swap_left:
            pos[(0, 0)], pos[(0, 1)] = pos[(0, 1)], pos[(0, 0)]
            seen(pos, cost_so_far, check_only=False)


def thingy(position, cost_so_far, min_cost, found, level=0):
    """The recursive solving thingy."""
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    #next(wc)
    if seen(position, cost_so_far, check_only=False):
        return min_cost

    if debug:
        print("--------------------------")
    with saved_state(position):
        # Move as many amphipods home as possible.
        #print("Find home moves:")
        #dump_pos(position)
        homing_cost = 0
        home_moves = all_home_moves(position)
        #print(home_moves)
        while home_moves:
            cost, a, b = home_moves[0]
            homing_cost += cost
            position[b] = position[a]
            position[a] = ' '
            #dump_pos(position)
            if cost_so_far + homing_cost > min_cost:
                return min_cost
            home_moves = all_home_moves(position)
            #print(home_moves)

        # After moving amphipods home we mmay be finished.
        if position == target_position:
            new_cost = cost_so_far + homing_cost
            if debug:
                print(":New home:")
            if new_cost < min_cost:
                print(f'NEW BEST: L={level} C={new_cost} M={min_cost}')
                min_cost = new_cost
                found.append(min_cost)
            return min_cost

        # Now explore possibilities starting with all possible room exiting
        # moves.
        pm = all_exit_moves(position)
        cost_so_far += homing_cost
        if not pm:
            add_dead_positions(position, cost_so_far)
            # return min_cost

        if debug:
            print("Exploring from:")
            here_before = seen(position, cost_so_far)
            dump_pos(position)
            print(f'  {level=} {cost_so_far=} {min_cost=} {here_before=}')
            for m in pm:
                print('   ', m)

        for cost, a, b in pm:
            new_cost = cost_so_far + cost
            if new_cost > min_cost:
                continue

            with saved_state(position):
                position[b] = position[a]
                position[a] = ' '
                min_cost = thingy(
                    position, new_cost, min_cost, found, level+1)

        return min_cost


def solve(room_size):
    """Solve the puzzle."""
    # pylint: disable=unused-variable
    create_target_position(room_size)
    print("----------")
    dump_pos(target_position)
    create_move_sets(room_size)
    position = parse_input(room_size)
    found = []
    positions.clear()
    min_cost = thingy(position, 0, MAX_COST, found)
    print(min_cost)
    if debug:
        for coord, ent in exit_move_sets.items():
            print(coord)
            for move in ent:
                print("   ", move)
        for a, move_sets in home_move_sets.items():
            print(a)
            for coord, ent in move_sets.items():
                print("   ", coord)
                for move in ent:
                    print("       ", move)


exit_move_sets = {}
home_move_sets = {}
debug = True
# solve(2)
solve(4)
