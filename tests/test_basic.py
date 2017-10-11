import unittest
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph import lr_node
from graph_diff.graph import RNR_graph

from graph_diff.graph.graph_with_repetitive_nodes_exceptions import GraphWithRepetitiveNodesKeyError


class GraphWithRepetitiveNodesWithRootTest(unittest.TestCase):
    _ROOT = (GraphWithRepetitiveNodesWithRoot._ROOT.Label,
             GraphWithRepetitiveNodesWithRoot._ROOT.Number)

    def setUp(self):
        self.test_graph = RNR_graph()

    def test_add_node(self):
        self.assertFalse(lr_node(1, 1) in self.test_graph)
        self.test_graph.add_node(lr_node(1, 1))
        self.assertTrue(lr_node(1, 1) in self.test_graph)

    def test_add_edge(self):
        self.assertFalse(lr_node(1, 1) in self.test_graph)
        self.assertFalse(lr_node(1, 2) in self.test_graph)
        self.test_graph.add_edge(lr_node(1, 1), lr_node(1, 2))
        self.assertTrue(lr_node(1, 1) in self.test_graph)
        self.assertTrue(lr_node(1, 2) in self.test_graph)

    def test_add_edge_exp(self):
        self.assertFalse(lr_node(1, 1) in self.test_graph)
        self.assertFalse(lr_node(1, 2) in self.test_graph)
        self.assertRaises(GraphWithRepetitiveNodesKeyError, self.test_graph.add_edge_exp, lr_node(1, 1), lr_node(1, 2))


class BaseLineAlgorithmTest(unittest.TestCase):
    def setUp(self):
        from graph_diff.baseline_algorithm import BaselineAlgorithm
        self.test_algorithm = BaselineAlgorithm()

    def template_test(self, graph1, graph2, score):
        self.assertEqual(self.test_algorithm.construct_diff(graph1, graph2).get_score(), score)

    def test_two_empty(self):
        graph1 = RNR_graph()
        graph2 = RNR_graph()
        self.template_test(graph1, graph2, (0, 1))

    def test_empty_and_one(self):
        graph1 = RNR_graph()
        graph2 = RNR_graph().add_node(lr_node(1, 1))
        self.template_test(graph1, graph2, (0, 1))
        self.template_test(graph2, graph1, (0, 1))

    def test_one_and_one(self):
        graph1 = RNR_graph().add_node(lr_node(1, 1))
        graph2 = RNR_graph().add_node(lr_node(1, 1))
        self.template_test(graph1, graph2, (1, 2))
        self.template_test(graph2, graph1, (1, 2))

    def test_one_and_two(self):
        graph1 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 2))
        graph2 = RNR_graph().add_node(lr_node(1, 1))
        self.template_test(graph1, graph2, (1, 2))
        self.template_test(graph2, graph1, (1, 2))

    def test_two_and_two(self):
        graph1 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 2))
        graph2 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 2))
        self.template_test(graph1, graph2, (2, 3))
        self.template_test(graph2, graph1, (2, 3))

    def test_one_and_two_with_edge(self):
        graph1 = RNR_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
        graph2 = RNR_graph().add_node(lr_node(1, 1))
        self.template_test(graph1, graph2, (1, 2))
        self.template_test(graph2, graph1, (1, 2))

    def test_two_with_edge_and_two_with_edge(self):
        graph1 = RNR_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
        graph2 = RNR_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
        self.template_test(graph1, graph2, (2, 3))
        self.template_test(graph2, graph1, (2, 3))

    def test_three_and_three(self):
        graph1 = RNR_graph().add_node(lr_node(1, 2)).add_node(lr_node(1, 1)).add_node(lr_node(1, 3))
        graph2 = RNR_graph().add_node(lr_node(1, 2)).add_node(lr_node(1, 1)).add_node(lr_node(1, 3))
        self.template_test(graph1, graph2, (3, 4))
        self.template_test(graph2, graph1, (3, 4))

    def test_three_and_three_with_dif_labels(self):
        graph1 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        graph2 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        self.template_test(graph1, graph2, (3, 4))
        self.template_test(graph2, graph1, (3, 4))

    def test_three_and_three_with_dif_labels_and_edges_to_center(self):
        graph1 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        graph2 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        graph1.add_edge(lr_node(1, 1), lr_node(2, 1)).add_edge(lr_node(3, 1), lr_node(2, 1))
        graph2.add_edge(lr_node(1, 1), lr_node(2, 1)).add_edge(lr_node(3, 1), lr_node(2, 1))
        self.template_test(graph1, graph2, (4, 4))
        self.template_test(graph2, graph1, (4, 4))

    def test_three_and_three_but_diff_numbers(self):
        graph1 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 2)).add_node(lr_node(1, 3))
        graph2 = RNR_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 3)).add_node(lr_node(1, 3))
        graph1.add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 3), lr_node(1, 2))
        graph2.add_edge(lr_node(1, 1), lr_node(1, 3)).add_edge(lr_node(1, 2), lr_node(1, 3))
        self.template_test(graph1, graph2, (4, 4))
        self.template_test(graph2, graph1, (4, 4))


if __name__ == '__main__':
    unittest.main()
