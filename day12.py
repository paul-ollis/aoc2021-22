"""Paul's solution for AOC day 12."""

from collections import defaultdict
from typing import Dict, Iterator, List, Set

from lib import data_lines


def parse_cave_connections() -> Dict[str, Set[str]]:
    """Parse the set of cave connections.

    The input is a set of node pairs, so this reads the input and creates a
    network. A dictionary of node sets should be sufficient. The entry for
    'end' is made an empty set. No node contains 'start' in its set of linked
    caves.
    """
    network: Dict[str, Set[str]] = defaultdict(set)
    for line in data_lines(__file__):
        a, _, b = line.partition('-')
        network[a].add(b)
        network[b].add(a)
    network['end'] = set()
    for node in network:
        network[node].discard('start')
    return network


def iter_routes(
        network:Dict[str, Set[str]],
        from_node: str,
        route: List[str],
        visited: Set[str],
        can_revisit: bool = False
    ) -> Iterator[List[str]]:
    """Walk the network finding all possible routes.

    :network:     The node network.
    :from_node:   The node from which to start walking.
    :route:       The route used to get to from_node.
    :visited:     A set of nodes that have been visited and must not be visited
                  again.
    :can_revisit: When set, a small cave may be revisited.
    """
    if from_node in visited:
        can_revisit = False

    visited = set(visited)
    route = list(route)
    if from_node[0].islower():
        visited.add(from_node)
    route.append(from_node)
    if can_revisit:
        choices = network[from_node]
    else:
        choices = set(n for n in network[from_node] if n not in visited)

    if not choices:
        if from_node == 'end':
            yield route
    else:
        for node in choices:
            yield from iter_routes(network, node, route, visited, can_revisit)


def find_all_routes():
    """Find all the routes through the caves."""
    network = parse_cave_connections()
    total = 0
    for _ in iter_routes(network, 'start', [], set()):
        total += 1
    print(total)


def find_all_relaxed_routes():
    """Find all the routes through the caves given relaxed time constraints."""
    network = parse_cave_connections()
    total = 0
    for _ in iter_routes(network, 'start', [], set(), can_revisit=True):
        total += 1
    print(total)


find_all_routes()
find_all_relaxed_routes()
