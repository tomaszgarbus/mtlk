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
    nodes, edges = g
    if not edges:
        return k ** len(nodes)
    edge = min(edges)
    return (
        count_colorings(remove_edge(g, edge), k)
        -
        count_colorings(contract_edge(g, edge), k)
    )

