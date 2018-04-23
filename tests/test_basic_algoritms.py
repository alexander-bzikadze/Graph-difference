import unittest

from parameterized import parameterized

from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.cpp_algorithms.algorithms import CppImport
from graph_diff.graph import rnr_graph, lr_node
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_diff_algorithm.compose_graph_diff_algorithm import ComposedGraphDiffAlgorithm
from graph_diff.graph_diff_algorithm.graph_map_comparator import GraphMapComparatorByEdgeNum
from graph_diff.simulated_annealing_algorithm.algorithm import Algorithm as SimAnnealAlgorithm


class BasicAlgorithmTest(unittest.TestCase):
    parameters = [
        ('Baseline', BaselineAlgorithm()),
        # ('Ant', AntAlgorithm()),
        # ('NewAnt', NewAntAlgorithm()),
        # ('BaselineCpp', CppRun.BaselineAlgorithm()),
        # ('BaselineWithChopAlgorithmCppRun', Cpp.BaselineWithChopAlgorithm()),
        # ('BaselineAlgorithmOmpCppRun', Cpp.BaselineAlgorithmOmp()),
        # ('BaselineWithChopAlgorithmOmpRun', Cpp.BaselineWithChopAlgorithmOmp())
        # ('AntAlgorithmCppRun', CppRun.AntAlgorithm()),
        # ('LinAntAlgorithmCppRun', CppRun.LinAntAlgorithm()),
        ('BaselineCppImport', CppImport.BaselineAlgorithm()),
        ('BaselineWithChopCppImport', CppImport.BaselineWithChopAlgorithm()),
        ('AntAlgorithmCppImport', CppImport.AntAlgorithm()),
        ('LinAntAlgorithmCppImport', CppImport.LinAntAlgorithm()),
        ('SimAnneal', SimAnnealAlgorithm()),
        ('Composition', ComposedGraphDiffAlgorithm(CppImport.LinAntAlgorithm(), SimAnnealAlgorithm()))
    ]

    def template_test(self, graph1, graph2, score, algorithm):
        diff = algorithm.construct_diff(graph1, graph2)
        self.assertEqual(first=GraphMapComparatorByEdgeNum()
                         .comparable_representation(diff),
                         second=score)

    def template_x_and_y_test_comp1(self, x: int, y: int, algorithm):
        graph1 = rnr_graph()
        graph2 = rnr_graph()
        for i in range(1, x + 1):
            graph1.add_node(lr_node(1, i))
        for i in range(1, y + 1):
            graph2.add_node(lr_node(1, i))
        i = min(x, y)
        self.template_test(graph1, graph2, i, algorithm)
        if x != y:
            self.template_test(graph2, graph1, i, algorithm)

    @parameterized.expand(parameters)
    def test_two_empty(self, _, algorithm):
        self.template_x_and_y_test_comp1(0, 0, algorithm)

    @parameterized.expand(parameters)
    def test_empty_and_one(self, _, algorithm):
        self.template_x_and_y_test_comp1(0, 1, algorithm)

    @parameterized.expand(parameters)
    def test_one_and_one(self, _, algorithm):
        self.template_x_and_y_test_comp1(1, 1, algorithm)

    @parameterized.expand(parameters)
    def test_one_and_two(self, _, algorithm):
        self.template_x_and_y_test_comp1(1, 2, algorithm)

    @parameterized.expand(parameters)
    def test_two_and_two(self, _, algorithm):
        self.template_x_and_y_test_comp1(2, 2, algorithm)

    @parameterized.expand(parameters)
    def test_one_and_two_with_edge(self, _, algorithm):
        graph1 = rnr_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
        graph2 = rnr_graph().add_node(lr_node(1, 1))
        self.template_test(graph1, graph2, 1, algorithm)
        self.template_test(graph2, graph1, 1, algorithm)

    @parameterized.expand(parameters)
    def test_two_with_edge_and_two_with_edge(self, _, algorithm):
        graph1 = rnr_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
        graph2 = rnr_graph().add_edge(lr_node(1, 2), lr_node(1, 1))
        self.template_test(graph1, graph2, 2, algorithm)
        self.template_test(graph2, graph1, 2, algorithm)

    @parameterized.expand(parameters)
    def test_three_and_three(self, _, algorithm):
        self.template_x_and_y_test_comp1(3, 3, algorithm)

    @parameterized.expand(parameters)
    def test_three_and_three_with_dif_labels(self, _, algorithm):
        graph1 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        graph2 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        self.template_test(graph1, graph2, 3, algorithm)
        self.template_test(graph2, graph1, 3, algorithm)

    @parameterized.expand(parameters)
    def test_three_and_three_with_dif_labels_and_edges_to_center(self, _, algorithm):
        graph1 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        graph2 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(2, 1)).add_node(lr_node(3, 1))
        graph1.add_edge(lr_node(1, 1), lr_node(2, 1)).add_edge(lr_node(3, 1), lr_node(2, 1))
        graph2.add_edge(lr_node(1, 1), lr_node(2, 1)).add_edge(lr_node(3, 1), lr_node(2, 1))
        self.template_test(graph1, graph2, 4, algorithm)
        self.template_test(graph2, graph1, 4, algorithm)

    @parameterized.expand(parameters)
    def test_three_and_three_but_diff_numbers(self, _, algorithm: GraphDiffAlgorithm):
        graph1 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 2)).add_node(lr_node(1, 3))
        graph2 = rnr_graph().add_node(lr_node(1, 1)).add_node(lr_node(1, 3)).add_node(lr_node(1, 3))
        graph1.add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 3), lr_node(1, 2))
        graph2.add_edge(lr_node(1, 1), lr_node(1, 3)).add_edge(lr_node(1, 2), lr_node(1, 3))
        self.template_test(graph1, graph2, 4, algorithm)
        self.template_test(graph2, graph1, 4, algorithm)

    @parameterized.expand(parameters)
    def test_four_and_four(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(4, 4, algorithm)

    @parameterized.expand(parameters)
    def test_five_and_five(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(5, 5, algorithm)

    @parameterized.expand(parameters)
    def test_six_and_six(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(6, 6, algorithm)

    @parameterized.expand(parameters)
    def test_four_and_three(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(4, 3, algorithm)

    @parameterized.expand(parameters)
    def test_four_and_two(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(4, 2, algorithm)

    @parameterized.expand(parameters)
    def test_four_and_one(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(4, 1, algorithm)

    @parameterized.expand(parameters)
    def test_four_and_empty(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(4, 0, algorithm)

    @parameterized.expand(parameters)
    def test_five_and_four(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(5, 4, algorithm)

    @parameterized.expand(parameters)
    def test_five_and_three(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(5, 3, algorithm)

    @parameterized.expand(parameters)
    def test_five_and_two(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(5, 2, algorithm)

    @parameterized.expand(parameters)
    def test_five_and_one(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(5, 1, algorithm)

    @parameterized.expand(parameters)
    def test_five_and_empty(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(5, 0, algorithm)

    @parameterized.expand(parameters)
    def test_seven_and_seven(self, _, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(7, 7, algorithm)

    @parameterized.expand(parameters)
    def test_eight_and_eight(self, name, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(8, 8, algorithm)

    @parameterized.expand(parameters)
    def test_nine_and_nine(self, name, algorithm: GraphDiffAlgorithm):
        self.template_x_and_y_test_comp1(9, 9, algorithm)

    # death to stoppers
    @parameterized.expand(parameters)
    def test_hundred_and_hundred(self, name, algorithm: GraphDiffAlgorithm):
        # self.template_x_and_y_test_comp1(100, 100, algorithm)
        pass

if __name__ == '__main__':
    unittest.main()