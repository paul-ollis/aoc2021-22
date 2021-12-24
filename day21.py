"""Paul's solution for AOC day 21."""

from functools import partial
from itertools import cycle
from typing import Callable, List, Optional, Tuple

from lib import data_lines

move: Optional[Callable] = None
ScoreHistory = List[List[int]]

# The different three die-roll totals along with the number of ways each total
# can be achieved.
roll_counts = (
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1)
)


class Die:
    """A single Die."""
    def __init__(self):
        self.values = cycle(range(1, 101))
        self.rolls = 0

    def __next__(self):
        self.rolls += 1
        return next(self.values)

    def __iter__(self):
        return self


def parse_input() -> Tuple[int, int]:
    """Parse the program and image data."""
    return [int(line.split()[-1]) for line in data_lines(__file__)]


def apply_roll_total(positions, scores, roll_total, i, winning_line=1000):
    """Perform a single move."""
    p = positions[i]
    p = (p - 1 + roll_total) % 10 + 1
    scores[i] += p
    positions[i] = p
    return scores[i] < winning_line


def do_move(positions, scores, die, i, winning_line=1000):
    """Perform a single move."""
    a = next(die)
    b = next(die)
    c = next(die)
    return apply_roll_total(positions, scores, a + b + c, i, winning_line)


def solve():
    """Solve the puzzle."""
    global move                              # pylint: disable=global-statement

    positions = parse_input()
    scores = [0, 0]
    die = Die()
    move = partial(do_move, positions, scores, die)
    while move(0) and move(1):
        pass

    print(min(scores) * die.rolls)


def explore_next_move(                     # pylint: disable=too-many-arguments
        positions: List[int],
        scores: List[int],
        player: int,
        wins: List[int],
        universes: int,
        trail: List,
        depth = 0,
    ) -> int:
    """Explore the result of the next 3 die rolls.

    :score_history: The history of scores so far.
    :player:        Which player is rollong.
    :wins:          The wins so far for each player.
    """
    for i, (roll_total, count) in enumerate(roll_counts):
        # if depth < 2:
        #     print(depth, trail, i)
        next_positions = list(positions)
        next_scores = list(scores)
        if move(next_positions, next_scores, roll_total, player):
            # This history need further exploration.
            trail.append(i)
            explore_next_move(
                next_positions, next_scores, (player + 1) % 2, wins,
                universes * count, trail, depth + 1)
            trail.pop()
        else:
            wins[player] += universes * count


def solve2():
    """Solve the puzzle, part 2."""
    global move                              # pylint: disable=global-statement

    positions = parse_input()
    scores = [0, 0]
    wins = [0, 0]
    move = partial(apply_roll_total, winning_line=21)

    explore_next_move(
        positions=positions, scores=scores, player=0, wins=wins, universes=1,
        trail=[])

    print(max(wins))

solve()
solve2()
