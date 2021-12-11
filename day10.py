"""Paul's solution for AOC day 10."""

from typing import List, Tuple

from lib import data_lines


def load_navigation_subsystem() -> List[str]:
    """Load in the navigation subsystem.

    This is simply a sequence of lines.
    """
    return [line.strip() for line in data_lines(__file__)]


def parse_navigation_line(code) -> Tuple[str, str]:
    """Parse a line of navigation code.

    :return:
        A tuple of (bad_char, completion). The bad_char is the one that
        causes a syntax error. The the bad_char == '' then the completion
        string provides an characters missing from the end of the code line.
    """
    openers = '([{<'
    closers = ')]}>'
    matches = dict(zip(closers, openers))
    completers = dict(zip(openers, closers))
    expr_stack = []
    for c in code:
        if c in openers:
            expr_stack.append(c)
        elif c in closers:
            try:
                top = expr_stack.pop()
            except IndexError:
                return c, ''
            else:
                if matches[c] != top:
                    return c, ''

    return '', ''.join(completers[c] for c in reversed(expr_stack))


def find_syntax_errors():
    """Find the characters that are syntax errors."""

    score_lookup = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    score = 0
    for line in load_navigation_subsystem():
        c, _ = parse_navigation_line(line)
        if c:
            score += score_lookup[c]
    print(score)


def complete_lines():
    """Auto-complete short lines.."""

    score_lookup = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    scores = []
    for line in load_navigation_subsystem():
        _, completion = parse_navigation_line(line)
        if completion:
            score = 0
            for c in completion:
                score *= 5
                score += score_lookup[c]
            scores.append(score)
    m = len(scores) // 2
    print(sorted(scores)[m])


find_syntax_errors()
complete_lines()
