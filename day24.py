"""Paul's solution for AOC day 24."""

# Analysys
#
# The code for each digit is the same except for some literal values, (shown
# below as <A>, <B> and <C>) which vary between input digits. Manually running
# this block of code, with the input digit denoted by 'D'.
#
#  1:   inp w
#  2:   mul x 0
#  3:   add x z
#  4:   mod x 26    x = z_p % 26
#  5:   div z <C>   z = z_p // C
#  6:   add x <A>
#  7:   eql x w
#  8:   eql x 0     x = z_p % 26 + A != D = Q
#  9:   mul y 0
#  10:  add y 25
#  11:  mul y x     y = 25 * Q
#  12:  add y 1     y = Q * 25 + 1
#  13:  mul z y     z = (z_p // C) * (Q * 25 + 1)
#  14:  mul y 0
#  15:  add y w
#  16:  add y <B>   y = D + B
#  17:  mul y x     y = (D + B) * Q
#  18:  add z y     z = (z_p // C) * (Q * 25 + 1) + (D + B) * Q
#
#  z = (z_p // C) * (z_p % 26 + A != D) * 25 + 1)
#    + (D + B)    * (z_p % 26 + A != D)
#
#  or
#     Q = (z_p % 26 + A) != D                                       (a)
#     z = (z_p // C) * (Q * 25 + 1) + (D + B) * Q
#
#  We know:
#     Q is always 1 or 0
#     C is always 1 or 26 (from the input analysis.)
#
#  When:
#
#     C/Q == 1/0 :   z = z_p                                        (1)
#     C/Q == 1/1 :   z = z_p * 26 + B + D                           (2)
#     C/Q == 26/0 :  z = z_p // 26                                  (3)
#     C/Q == 26/1 :  z = (z_p // 26) * 26 + (B + D)                 (4)
#
#  C   Q  Notes
#  -- --  -------------------
#  1   0  z = zp
#  1   1  z ~= zp * 26
#  26  0  z = zp // 26
#  26  1  z ~= zp + B + D
#
# My sequence of A    B    C
#                15   13   1      Q=1  z = D + B
#                10   16   1      Q=1  z ~= zp * 26
#                12   2    1      Q=1  z ~= zp * 26^2
#                10   8    1      Q=1  z ~= zp * 26^3
#                14   11   1      Q=1  z ~= zp * 26^4
#                -11  6    26          z ~= zp * 26^3
#                10   12   1      Q=1  z ~= zp * 26^4
#                -16  2    26          z ~= zp * 26^3
#                -9   2    26          z ~= zp * 26^2
#                11   15   1      Q=1  z ~= zp * 26^3
#                -8   1    26          z ~= zp * 26^2
#                -8   10   26          z ~= zp * 26^1
#                -10  14   26          z ~= zp * 26^0
#                -9   10   26          z ~= zp * 26^-1
#
# The program analysis suggest that Z will grow by a failrly lareg amount for
# of the input digits, so we almost cetainly need to chhose digits that reduce
# Z for the other 7 digits. In =other words:
#
# If C == 26 then only consider digits for which Q == 0.

literals = (
    (15, 13, 1),
    (10, 16, 1),
    (12, 2, 1),
    (10, 8, 1),
    (14, 11, 1),
    (-11, 6, 26),
    (10, 12, 1),
    (-16, 2, 26),
    (-9, 2, 26),
    (11, 15, 1),
    (-8, 1, 26),
    (-8, 10, 26),
    (-10, 14, 26),
    (-9, 10, 26),
)
mem = {}


def calc_q(zp, d, a):
    """Calculate the  Q value."""
    return int((zp % 26 + a) != d)


def calc_z(zp, d, q, b, c):
    """Calculate the new Z value."""
    return (zp // c) * (q * 25 + 1) + (d + b) * q


def find_rem_sequences(zp: int, step: int, n: int, rng):
    """Try the next potential set of digits."""
    k = zp, step
    if k in mem:
        return mem[k]

    a, b, c = literals[step]
    choices = [(d, calc_q(zp, d, a)) for d in rng]
    if c == 26:
        # When c == 26, then we want the Q value to be zero, so that Z can
        # decrease.
        choices = [(d, q) for d, q in choices if q == 0]
    if not choices:
        return []

    if step == n - 1:
        choices = [[d] for d, q in choices if calc_z(zp, d, q, b, c) == 0]
        mem[k] = choices
        return choices

    ret = []
    for d, q in choices:
        z = calc_z(zp, d, q, b, c)
        for seq in find_rem_sequences(z, step + 1, n, rng):
            ret.append([d] + seq)
            if ret:
                return ret
    mem[k] = ret
    return ret


def solve():
    """Solve the puzzle."""
    solutions = find_rem_sequences(0, 0, 14, range(9, 0, -1))
    print(''.join(str(d) for d in solutions[0]))
    solutions = find_rem_sequences(0, 0, 14, range(1, 10))
    print(''.join(str(d) for d in solutions[-1]))


solve()
