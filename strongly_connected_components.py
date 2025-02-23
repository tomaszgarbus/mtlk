"""
Finds SCCs in a directed graph.
"""
from collections import deque, defaultdict
from collections.abc import Callable


type DirectedEdge = tuple[int, int]
type DirectedGraph = tuple[set[int], set[Edge]] 


def _transpose(g: DirectedGraph) -> DirectedGraph:
    nodes, edges = g
    transposed_edges = set([
        (edge[1], edge[0])
        for edge in edges
    ])
    return (nodes, transposed_edges)


def _build_edges_dict(edges: set[DirectedEdge]) -> dict[int, list[int]]:
    """Builds a dictionary of edges.

    Keys are nodes, values are lists of connected nodes."""
    result = defaultdict(list)
    for u, v in edges:
        result[u].append(v)
    return result


def strongly_connected_components(g: DirectedGraph) -> list[set[int]]:
    """
    Finds SCCs in `g`. Returns a list of sets of nodes, where each set is one
    SCC.
    """
    # Algorithm:
    # First, list all nodes in post-order.
    # Second, the nodes in decreasing post-order numbers in the transposed
    # graph and build the SCCs.
    # Why this works: consider the graph as a DAG of SCCs. Consider SCCs S1
    # and S2, where S1 is topologically earlier. Then there must be a node
    # u in S1 which has a higher postorder number than any node in S2. Thus
    # when iterating nodes in decreasing postorder, we will process S1 first.
    postorder: list[int] = [] 
    visited = set()

    nodes, edges = g
    neighbours = _build_edges_dict(edges)

    def dfs(u: int, neighbours: dict[int, list[int]], visited: set[int],
        postprocess_callback: Callable[[int], None]):
        if u in visited:
            return
        visited.add(u)
        for v in neighbours[u]:
            dfs(v, neighbours, visited, postprocess_callback)
        postprocess_callback(u)

    for u in nodes:
        dfs(u, neighbours, visited,
            lambda node: postorder.append(node))

    visited = set()
    nodes, edges = _transpose(g)
    neighbours = _build_edges_dict(edges)
    result = []
    for u in postorder[::-1]:
        scc = set()
        dfs(u, neighbours, visited, lambda node: scc.add(node))
        if scc:
            result.append(scc)
    return result
