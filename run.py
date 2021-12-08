"""A puzzle script runner.

This will run puzzle scripts and verify that the solution is correct.
"""

import argparse
import subprocess
from pathlib import Path

solutions = {
    'day1': (1709, 1761),
    'day2': (1813801, 1960569556),
}


def run_solvers(args):
    """Run the solvers."""

    def lines(output):
        yield from (f'{line}' for line in output.decode().splitlines())

    solvers = args.solver
    if not solvers:
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
        'solver', type=str, nargs='?', help='The name os a solver script')
    cmd_args = parser.parse_args()
    run_solvers(cmd_args)
