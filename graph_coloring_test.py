import unittest
from graph_coloring import count_colorings 

class GraphColoringTest(unittest.TestCase):
    
    def test_no_edges(self):
        graph = (
            set([5, 9, 20, 24]),
            set()
        )
        self.assertEqual(count_colorings(graph, 1), 1)
        self.assertEqual(count_colorings(graph, 2), 16)
        self.assertEqual(count_colorings(graph, 3), 81)
        self.assertEqual(count_colorings(graph, 4), 256)

    def test_two_nodes_one_edge(self):
        graph = (
            set([1, 2]),
            set([(1, 2)])
        )
        self.assertEqual(count_colorings(graph, 1), 0)
        self.assertEqual(count_colorings(graph, 2), 2)

    def test_four_nodes_fully_connected(self):
        graph = (
            set([1, 2, 3, 4]),
            set([
                (1, 2), (2, 3), (3, 4), (4, 1), (1, 3),
                (2, 4)
            ])
        )
        self.assertEqual(count_colorings(graph, 3), 0)
        self.assertEqual(count_colorings(graph, 4), 24)
        self.assertEqual(count_colorings(graph, 5), 120)

    def test_petersen_graph(self):
        graph = (
            set(range(1, 11)),
            set([
                (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
                (1, 6), (2, 7), (3, 8), (4, 9), (5, 10),
                (6, 8), (8, 10), (10, 7), (7, 9), (9, 6)
            ])
        )
        # Petersen graph's chromatic polynomial:
        cp = lambda t: (
            t * (t - 1) * (t - 2) * (
                t ** 7 - 12 * t ** 6 + 67 * t ** 5 - 230 * t ** 4
                + 529 * t ** 3 - 814 * t ** 2 + 775 * t - 352
            )
        )
        for t in range(15):
            self.assertEqual(count_colorings(graph, t), cp(t))
        

if __name__ == '__main__':
    unittest.main()
