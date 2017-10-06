import unittest
from graph_diff.graph.GraphWithRepetitiveNodes import GraphWithRepetitiveNodes


class GraphWithRepetitiveNodesTest(unittest.TestCase):
    def setUp(self):
        self.test_graph = GraphWithRepetitiveNodes()

    def test_initialize_contains_root(self):
        self.assertTrue(self.test_graph._ROOT in self.test_graph.get_list_of_nodes())

    def test_initialize_does_not_contain_anything_but_root(self):
        test_graph = GraphWithRepetitiveNodes()
        for i in range(0, 10):
            for j in range(0, 10):
                if (i, j) != test_graph._ROOT:
                    self.assertFalse((i, j) in self.test_graph.get_list_of_nodes())

    def test_add_edge_explicit_throws_if_node_is_not_in_graph(self):
        from graph_diff.graph.GraphWithRepetitiveNodesExceptions \
            import GraphWithRepetitiveNodesKeyError
        with self.assertRaises(GraphWithRepetitiveNodesKeyError):
            self.test_graph.add_edge_explicit((1, 0),(1, 0))

    def test_successfully_adds_nodes(self):
        test_graph = GraphWithRepetitiveNodes()
        for i in range(0, 10):
            for j in range(0, 10):
                if (i, j) != test_graph._ROOT:
                    self.assertTrue((i, j) in self
                                    .test_graph.add_node((i, j))
                                    .get_list_of_nodes())

    def test_successfully_adds_edges(self):
        test_graph = GraphWithRepetitiveNodes()
        for i in range(0, 10):
            for j in range(0, 10):
                if (i, j) != test_graph._ROOT:
                    self.assertTrue((test_graph._ROOT, (i, j)) in self
                                    .test_graph.add_edge(test_graph._ROOT, (i, j))
                                    .get_list_of_edges())
        for i in range(0, 10):
            for j in range(0, 10):
                if (i, j) != test_graph._ROOT:
                    self.assertTrue(((i, j)) in self
                                    .test_graph.add_edge(test_graph._ROOT, (i, j))
                                    .get_list_of_adjacent_nodes(test_graph._ROOT))


if __name__ == '__main__':
    unittest.main()
