"""A puzzle script runner.

This will run puzzle scripts and verify that the solution is correct.
"""

import argparse
import os
import subprocess
from pathlib import Path

solutions = {
    'day1': (1709, 1761),
    'day2': (1813801, 1960569556),
    'day3': (3969000, 4267809),
    'day4': (67716, 1830),
    'day5': (8060, 21577),
    'day6': (353_079, 1_605_400_130_036),
    'day7': (352331, 99266250),
    'day8': (321, 1028926),
    'day9': (528, 920448),
    'day10': (392139, 4001832844),
    'day11': (1647, 348),
    'day12': (5756, 144603),
}


def run_solvers(args):
    """Run the solvers."""

    def lines(output):
        yield from (f'{line}' for line in output.decode().splitlines())

    if args.devel:
        os.environ['AOC_DEVEL'] = 'dev_data'

    if args.solver:
        solvers = [args.solver]
    else:
        solvers = Path('.').glob('day*.py')
    for py_file in sorted(solvers):
        expected = solutions.get(py_file.stem, (None, None))
        print(f'Running: {py_file}, expecting {expected}')
        res= subprocess.run(
            ['python', str(py_file)], check=False, capture_output=True)
        print('\n'.join(f'    {line}' for line in lines(res.stdout)))
        print('\n'.join(f'    !! {line}' for line in lines(res.stderr)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run one or all scripts')
    parser.add_argument(
        'solver', type=Path, nargs='?', help='The name os a solver script')
    parser.add_argument(
        '-d', '--devel', action='store_true', help='Use development data')
    cmd_args = parser.parse_args()
    run_solvers(cmd_args)
