"""Paul's solution for AOC day 24."""

from typing import List

from lib import data_lines


class ALU:
    """Emulation of the ALU."""
    w: int
    x: int
    y: int
    z: int

    def __init__(self, program):
        self.source = program
        self.code = self.compile(program)
        self.regs = {}
        self.reset()
        self.input = list('')

    def set_input(self, digits):
        """Set the input number."""
        self.input = list(reversed(digits))

    def reset(self):
        """Reset the ALU ready to run a new program."""
        for name in 'wxyz':
            self.regs[name] = 0

    def compile(self, program):                   # pylint: disable=no-self-use
        """Compile the program easy and fast to execute instructions."""
        code = []
        for instr in (line.split() for line in program):
            match instr:
                case [op, reg, ('w' | 'x' | 'y' | 'z') as arg]:
                    print(f'A: {op} {reg!r} {arg!r}')
                    code.append((getattr(self, op), (reg, arg)))

                case [op, reg, arg]:
                    arg = int(arg)
                    print(f'B: {op} {reg!r} {arg!r}')
                    code.append((getattr(self, f'{op}_int'), (reg, arg)))

                case (op, reg):
                    print(f'B: {op} {reg!r}')
                    code.append((getattr(self, op), (reg,)))

                case ():
                    pass

                case _:
                    assert False

        return code

    def inp(self, reg):
        """Input to a register."""
        self.regs[reg] = int(self.input.pop())

    def add(self, reg, breg):
        """Add another register to a register."""
        r = self.regs
        r[reg] += r[breg]

    def add_int(self, reg, value):
        """Add a literal integer to a register."""
        self.regs[reg] += value

    def mul(self, reg, breg):
        """Add another register to a register."""
        r = self.regs
        r[reg] *= r[breg]

    def mul_int(self, reg, value):
        """Add a literal integer to a register."""
        self.regs[reg] *= value

    def div(self, reg, breg):
        """Add another register to a register."""
        r = self.regs
        a, b = r[reg], r[breg]
        assert b != 0
        r[reg] = a // b if a * b > 0 else (a + (-a % b)) // b

    def div_int(self, reg, value):
        """Add a literal integer to a register."""
        r = self.regs
        a, b = r[reg], value
        assert b != 0
        r[reg] = a // b if a * b > 0 else (a + (-a % b)) // b

    def mod(self, reg, breg):
        """Add another register to a register."""
        r = self.regs
        a, b = r[reg], r[breg]
        assert a >= 0 and b >= 0
        r[reg] = a % b

    def mod_int(self, reg, value):
        """Add a literal integer to a register."""
        r = self.regs
        a, b = r[reg], value
        assert a >= 0 and b >= 0
        r[reg] = a % b

    def eql(self, reg, breg):
        """Add another register to a register."""
        r = self.regs
        r[reg] = int((r[reg] == r[breg]))

    def eql_int(self, reg, value):
        """Add a literal integer to a register."""
        r = self.regs
        r[reg] = int((r[reg] == value))

    def run(self, digits):
        """Run program on a sequence of input digits."""
        self.set_input(digits)
        self.reset()
        for i, (op, args) in enumerate(self.code):
            try:
                op(*args)
            except IndexError:
                break
            if i > 1000:
                break
        self.dump()

    def dump(self):
        """Dump the stat of the ALU."""
        print(f'{"".join(reversed(self.input))} {self.regs=}')


def parse_input() -> List:
    """Parse the XX starting positions.

    :return:
    """
    lines = data_lines(__file__)
    return list(lines)


def solve():
    """Solve the puzzle."""
    alu = ALU(parse_input())
    for n in '123456789':
        alu.run(n)
    # alu.run('13579246899999')


solve()
