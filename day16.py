"""Paul's solution for AOC day 16."""

from dataclasses import dataclass
from itertools import chain
from typing import Iterator, List, Optional

from lib import data_lines


@dataclass
class Packet:
    """A single packet."""
    ver: int
    typ: int
    sub_packets: List['Packet']
    value: Optional[int] = None

    def ver_total(self):
        """Calculate the total of this and all decendents' versions."""
        return self.ver + sum(p.ver_total() for p in self.sub_packets)

    def evaluate(self):            # pylint: disable=too-many-return-statements
        """Evaluate this packet's value."""
        match self.typ:
            case 0:
                return sum(p.evaluate() for p in self.sub_packets)
            case 1:
                v = 1
                for p in self.sub_packets:
                    v *= p.evaluate()
                return v
            case 2:
                return min(p.evaluate() for p in self.sub_packets)
            case 3:
                return max(p.evaluate() for p in self.sub_packets)
            case 4:
                return self.value
            case 5:
                a, b = self.sub_packets
                return int(a.evaluate() > b.evaluate())
            case 6:
                a, b = self.sub_packets
                return int(a.evaluate() < b.evaluate())
            case 7:
                a, b = self.sub_packets
                return int(a.evaluate() == b.evaluate())
            case _:
                raise RuntimeError(f'Bad type: {self.typ}')


def parse_input() -> Iterator[int]:
    """Parse the instruction input.

    The input is a stream of hexadecimal digits, which we want to convert to a
    stream of binary digits.
    """
    line = next(data_lines(__file__))
    hex_digits = (int(c, 16) for c in line)
    binary_strings = (f'{d:04b}' for d in hex_digits)
    return ((int(d) for d in chain(*binary_strings)))


def nbit_value(code: Iterator[int], count: int):
    """Read in a number of bits as a value."""
    v = 0
    for _ in range(count):
        v = (v << 1) | next(code)
    return v


def nbits(code: Iterator[int], count: int):
    """Iterate over a number of bits."""
    for _ in range(count):
        try:
            yield next(code)
        except StopIteration:
            pass


def parse_packet(code: Iterator[int]):
    """Parse a packet."""
    ver = nbit_value(code, 3)
    typ = nbit_value(code, 3)

    if typ == 4:
        bit_pattern = []
        c = 1
        while c:
            c = next(code)
            bit_pattern.extend([str(b) for b in nbits(code, 4)])
        return Packet(ver, typ, [], int(''.join(bit_pattern), 2))

    else:
        fmt = next(code)
        sub_packets = []
        if fmt == 0:
            sub_packet_code = nbits(code, nbit_value(code, 15))
            while True:
                try:
                    sub_packets.append(parse_packet(sub_packet_code))
                except StopIteration:
                    break
        else:
            sub_packet_count = nbit_value(code, 11)
            for _ in range(sub_packet_count):
                sub_packets.append(parse_packet(code))

    return Packet(ver, typ, sub_packets)


def solve():
    """Solve the puzzle..."""
    code = parse_input()
    outer_packet = parse_packet(code)
    print(outer_packet.ver_total())
    print(outer_packet.evaluate())


solve()
