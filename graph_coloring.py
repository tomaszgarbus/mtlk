"""
Tools for counting and finding graph colorings.

WARNING: Graphs are undirected here.
"""
from collections import defaultdict


# A graph is a set of nodes and a set of edges.
type Edge = tuple[int, int]
type Graph = tuple[set[int], set[Edge]]


def contract_edge(g: Graph, edge: Edge):
    u, v = edge
    nodes, edges = g
    node_mapper = lambda w: u if w == v else w
    new_nodes = set()
    new_edges = set()
    for node in nodes:
        new_nodes.add(node_mapper(node))
    for uu, vv in edges:
        ee = node_mapper(uu), node_mapper(vv)
        # Normalizing to avoid duplicate edges.
        if ee[0] > ee[1]:
            ee = ee[1], ee[0]
        if ee[0] != ee[1]:
            new_edges.add(ee)
    return new_nodes, new_edges


def remove_edge(g: Graph, edge: Edge):
    nodes, edges = g
    return nodes, set([e for e in edges if e != edge])


def count_colorings(g: Graph, k: int) -> int:
    """
    Count number of good colorings in a graph using the deletion–contraction
    recurrence.
    """
    nodes, edges = g
    if not edges:
        return k ** len(nodes)
    edge = min(edges)
    return (
        count_colorings(remove_edge(g, edge), k)
        -
        count_colorings(contract_edge(g, edge), k)
    )


def _build_edges_dict(edges: set[Edge]) -> dict[int, list[int]]:
    """Builds a dictionary of edges.

    Keys are nodes, values are lists of connected nodes."""
    result = defaultdict(list)
    for u, v in edges:
        result[u].append(v)
        result[v].append(u)
    return result


def find_2_coloring_if_any(g: Graph) -> dict[int, int] | None:
    """Returns a 2-coloring if such exists."""
    nodes, edges = g 
    color: dict[int, int] = {}
    neighbors = _build_edges_dict(edges)
    for u in nodes:
        if u in color:
            continue
        q = [u]
        color[u] = 0
        while q:
            v = q.pop()
            for w in neighbors[v]:
                if w in color:
                    if color[w] == color[v]:
                        # We found a cycle of odd length.
                        return None
                    else:
                        continue
                color[w] = 1 - color[v]
                q.append(w)
    return color

