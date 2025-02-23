import unittest
import sys

from strongly_connected_components import (
    DirectedEdge, DirectedGraph, strongly_connected_components 
)


def _verify(result: list[set[int]], expected: list[set[int]]) -> bool:
    if len(result) != len(expected):
        return False
    for scc in expected:
        if scc not in result:
            return False
    return True


def _expand_dag(dag: DirectedGraph, factor: int) -> (
    DirectedGraph, list[set[int]]):
    """Expands a DAG by replacing each node with a cycle.

    Returns a pair (expanded graph, list of SCCs)."""
    nodes, edges = dag
    new_nodes = []
    new_edges = []
    sccs = []
    for u in nodes:
        scc = set()
        for i in range(factor):
            new_nodes.append(u * factor + i)
            scc.add(u * factor + i)
            new_edges.append((u * factor + i, u * factor + (i + 1) % factor))
        sccs.append(scc)
    for edge in edges:
        u, v = edge
        new_edges.append((u * factor, v * factor))
    return (set(new_nodes), set(new_edges)), sccs


class StronglyConnectedComponentsTest(unittest.TestCase):
    
    def test_chain(self):
        graph = (
            set([1, 2, 3, 4, 5]),
            set([(1, 2), (2, 3), (3, 4), (4, 5)])
        )
        output = strongly_connected_components(graph)
        assert _verify(
            output,
            [set([i]) for i in [1, 2, 3, 4, 5]]
        ), str(output)

    def test_reverse_chain(self):
        graph = (
            set([1, 2, 3, 4, 5]),
            set([(5, 4), (4, 3), (3, 2), (2, 1)])
        )
        output = strongly_connected_components(graph)
        assert _verify(
            output,
            [set([i]) for i in [1, 2, 3, 4, 5]]
        ), str(output)

    def test_cycle(self):
        n = 100000
        sys.setrecursionlimit(max(n * 2, sys.getrecursionlimit()))
        nodes = set([i for i in range(n)])
        graph = (
            nodes,
            set([(i, (i+1)%n) for i in range(n)])
        )
        output = strongly_connected_components(graph)
        assert _verify(
            output,
            [nodes]
        ), output

    def test_dag(self):
        dag = (
            set([0, 1, 2, 3, 4]),
            set([(0, 2), (0, 3), (1, 2), (1, 3), (2, 4), (3, 4)])
        )
        graph, expected = _expand_dag(dag, 20)
        output = strongly_connected_components(graph)
        assert _verify(output, expected), output


if __name__ == '__main__':
    unittest.main()
