"""Paul's solution for AOC day 4."""

from itertools import chain
from typing import List, Tuple, Iterator

from lib import data_lines


class Card:
    """An object representing a bingo card."""
    def __init__(self, card_lines: Iterator[str]):
        lines = [[int(s) for s in next(card_lines).split()] for _ in range(5)]
        self.columns = [set(line) for line in zip(*lines)]
        self.lines = [set(line) for line in lines]
        self.line_marks: List[List[int]] = [[] for _ in range(5)]
        self.column_marks: List[List[int]] = [[] for _ in range(5)]

    def mark(self, v):
        """Mark off a value for this card."""
        for marks, line in zip(self.line_marks, self.lines):
            if v in line:
                marks.append(v)
                if len(marks) == 5:
                    return marks
        for marks, column in zip(self.column_marks, self.columns):
            if v in column:
                marks.append(v)
                if len(marks) == 5:
                    return marks
        return []

    def unmarked(self):
        """All the unmarked numbers."""
        all_marked = set(chain(*self.line_marks))
        yield from (v for v in chain(*self.lines) if v not in all_marked)


def parse_bingo_data() -> Tuple[List[int], List[Card]]:
    """Parse the bingo data.

    This reads the sequences of drawn values and all the cards.
    """
    stripped = (line.strip() for line in data_lines(__file__))
    non_blanks = (line for line in stripped if line)
    drawn_values = [int(s) for s in next(non_blanks).split(',')]
    cards = []
    while True:
        try:
            cards.append(Card(non_blanks))
        except StopIteration:
            break

    return drawn_values, cards


def find_winning_card():
    """Find the winning card."""
    drawn_values, cards = parse_bingo_data()
    for v in drawn_values:
        for card in cards:
            if card.mark(v):
                print(sum(card.unmarked()) * v)
                return


def find_worst_card():
    """Find the last card to win."""
    drawn_values, cards = parse_bingo_data()
    rem_cards = set(cards)
    for v in drawn_values:
        for card in list(rem_cards):
            if card.mark(v):
                rem_cards.discard(card)
                if not rem_cards:
                    print(sum(card.unmarked()) * v)
                    return


find_winning_card()
find_worst_card()
