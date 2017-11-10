import unittest

from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph import lr_node
from graph_diff.graph import rnr_graph
from parameterized import parameterized, param

from graph_diff.graph.graph_with_repetitive_nodes_exceptions import GraphWithRepetitiveNodesKeyError
from graph_diff.graph_map import GraphMapComparatorByEdgeNum, GraphMapComparator


class GraphWithRepetitiveNodesWithRootTest(unittest.TestCase):
    _ROOT = (GraphWithRepetitiveNodesWithRoot.ROOT.Label,
             GraphWithRepetitiveNodesWithRoot.ROOT.Number)

    def setUp(self):
        self.test_graph = rnr_graph()

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


def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" % (
        testcase_func.__name__,
        parameterized.to_safe_name("_".join(str(x) for x in param.args)),
    )

class BaseLineAlgorithmTest(unittest.TestCase):
    parameters = [
        param("baseline", BaselineAlgorithm(GraphMapComparatorByEdgeNum()))
    ]

    # @parameterized(
    #     GraphMapComparatorByEdgeNum()
    # )

    def template_test(self, graph1, graph2, score, comparator: GraphMapComparator):
        from graph_diff.baseline_algorithm import BaselineAlgorithm
        from graph_diff.graph_map import GraphMapComparatorByEdgeNumAndThenNodeNum
        self.assertEqual(GraphMapComparatorByEdgeNumAndThenNodeNum()
                         .comparable_representation(BaselineAlgorithm(comparator)
                         .construct_diff(graph1, graph2)), score)

    def template_x_and_y_test_comp1(self, x: int, y: int, comparator: GraphMapComparator):
        graph1 = rnr_graph()
        graph2 = rnr_graph()
        for i in range(1, x + 1):
            graph1.add_node(lr_node(1, i))
        for i in range(1, y + 1):
            graph2.add_node(lr_node(1, i))
        i = min(x, y)
        self.template_test(graph1, graph2, (i, i + 1), comparator)
        if x != y:
            self.template_test(graph2, graph1, (i, i + 1), comparator)

    @parameterized.expand([
        ("2 and 3", 2, 3, 5),
        ("3 and 5", 2, 3, 5),
    ])
    def test_add(self, _, a, b, expected):
        pass

    # def test_two_empty(self, comparator: GraphMapComparator):
    #     self.template_x_and_y_test_comp1(0, 0, comparator)

    # def test_empty_and_one(self):
    #     self.template_x_and_y_test_comp1(0, 1)
    #
    # def test_one_and_one(self):
    #     self.template_x_and_y_test_comp1(1, 1)
    #
    # def test_one_and_two(self):
    #     self.template_x_and_y_test_comp1(1, 2)
    #
    # def test_two_and_two(self):
    #     self.template_x_and_y_test_comp1(2, 2)
    #
    # def test_one_and_two_with_edge(self):
    #     graph1 = rnr_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
    #     graph2 = rnr_graph().add_node(lr_node(1, 1))
    #     self.template_test(graph1, graph2, (1, 2), self.comparator)
    #     self.template_test(graph2, graph1, (1, 2), self.comparator)
    #
    # def test_two_with_edge_and_two_with_edge(self):
    #     graph1 = rnr_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
    #     graph2 = rnr_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
    #     self.template_test(graph1, graph2, (2, 3), self.comparator)
    #     self.template_test(graph2, graph1, (2, 3), self.comparator)
    #
    # def test_three_and_three(self):
    #     self.template_x_and_y_test_comp1(3, 3)
    #
    # def test_three_and_three_with_dif_labels(self):
    #     graph1 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
    #     graph2 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
    #     self.template_test(graph1, graph2, (3, 4), self.comparator)
    #     self.template_test(graph2, graph1, (3, 4), self.comparator)
    #
    # def test_three_and_three_with_dif_labels_and_edges_to_center(self):
    #     graph1 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
    #     graph2 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
    #     graph1.add_edge(lr_node(1, 1), lr_node(2, 1)).add_edge(lr_node(3, 1), lr_node(2, 1))
    #     graph2.add_edge(lr_node(1, 1), lr_node(2, 1)).add_edge(lr_node(3, 1), lr_node(2, 1))
    #     self.template_test(graph1, graph2, (4, 4), self.comparator)
    #     self.template_test(graph2, graph1, (4, 4), self.comparator)
    #
    # def test_three_and_three_but_diff_numbers(self):
    #     graph1 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 2)).add_node(lr_node(1, 3))
    #     graph2 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 3)).add_node(lr_node(1, 3))
    #     graph1.add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 3), lr_node(1, 2))
    #     graph2.add_edge(lr_node(1, 1), lr_node(1, 3)).add_edge(lr_node(1, 2), lr_node(1, 3))
    #     self.template_test(graph1, graph2, (4, 4), self.comparator)
    #     self.template_test(graph2, graph1, (4, 4), self.comparator)
    #
    # def test_four_and_four(self):
    #     self.template_x_and_y_test_comp1(4, 4)
    #
    # def test_five_and_five(self):
    #     self.template_x_and_y_test_comp1(5, 5)
    #
    # def test_six_and_six(self):
    #     self.template_x_and_y_test_comp1(6, 6)
    #
    # def test_four_and_three(self):
    #     self.template_x_and_y_test_comp1(4, 3)
    #
    # def test_four_and_two(self):
    #     self.template_x_and_y_test_comp1(4, 2)
    #
    # def test_four_and_one(self):
    #     self.template_x_and_y_test_comp1(4, 1)
    #
    # def test_four_and_empty(self):
    #     self.template_x_and_y_test_comp1(4, 0)
    #
    # def test_five_and_four(self):
    #     self.template_x_and_y_test_comp1(5, 4)
    #
    # def test_five_and_three(self):
    #     self.template_x_and_y_test_comp1(5, 3)
    #
    # def test_five_and_two(self):
    #     self.template_x_and_y_test_comp1(5, 2)
    #
    # def test_five_and_one(self):
    #     self.template_x_and_y_test_comp1(5, 1)
    #
    # def test_five_and_empty(self):
    #     self.template_x_and_y_test_comp1(5, 0)
    #
    # def test_seven_and_seven(self):
    #     self.template_x_and_y_test_comp1(7, 7)
    #
    # def test_eight_and_eight(self):
    #     self.template_x_and_y_test_comp1(8, 8)
    #
    # # one minute long
    # def test_nine_and_nine(self):
    #     self.template_x_and_y_test_comp1(9, 9)


if __name__ == '__main__':
    unittest.main()
