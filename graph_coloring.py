"""
Count number of good colorings in a graph using the deletion–contraction
recurrence.

WARNING: Graphs are undirected here.
"""
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
        new_edges.add((node_mapper(uu), node_mapper(vv)))
    return new_nodes, new_edges


def remove_edge(g: Graph, edge: Edge):
    nodes, edges = g
    return nodes, set([e for e in edges if e != edge])
