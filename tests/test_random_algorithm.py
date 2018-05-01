import unittest

from parameterized import parameterized

from graph_diff.cpp_algorithms.algorithms import CppImport
from graph_diff.graph import StandardGraphGenerator, GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_diff_algorithm.compose_graph_diff_algorithm import ComposedGraphDiffAlgorithm
from graph_diff.graph_diff_algorithm.graph_map_comparator import GraphMapComparatorByEdgeNum, GraphMapComparator
from graph_diff.simulated_annealing_algorithm.sim_anneal_algorithm import SimAnnealAlgorithm as SimAnnealAlgorithm


def generate_parameters(algo, comparator, number_of_tests, *args):
    return sum([[(str(i) + "_" + str(type(algo).__name__),
                  algo,
                  generator.generate_graph(),
                  comparator)
                 for _ in range(0, number_of_tests)]
                for i, generator in enumerate(args)], [])


class RandomGraphTest(unittest.TestCase):
    NUMBER_OF_TESTS = 100

    ERROR = 0
    FAILED_NUMBER = 0

    parameters = sum([generate_parameters(algo,
                                          GraphMapComparatorByEdgeNum(),
                                          100,
                                          StandardGraphGenerator(0, 60))
                      for algo in [
                          # BaselineAlgorithm(),
                          # OrderedAntAlgorithm(),
                          # UnorderedAntAlgorithm(),
                          # Cpp.BaselineAlgorithm(),
                          # Cpp.BaselineWithChopAlgorithm(),
                          # CppRun.OrderedAntAlgorithm(),
                          # CppImport.BaselineWithChopAlgorithm(),
                          CppImport.OrderedAntAlgorithm(),
                          # SimAnnealAlgorithm(),
                          # ComposedGraphDiffAlgorithm(CppImport.OrderedAntAlgorithm(), SimAnnealAlgorithm())
                      ]], [])

    @parameterized.expand(parameters)
    def test_random(self,
                    _,
                    algo: GraphDiffAlgorithm,
                    graph: GraphWithRepetitiveNodesWithRoot,
                    comparator: GraphMapComparator):
        algo2_result = algo.construct_diff(graph, graph)
        l = sum([len(graph.get_list_of_adjacent_nodes(v)) for v in graph])
        # print(l)
        if l != comparator.comparable_representation(algo2_result):
            RandomGraphTest.ERROR += l - comparator.comparable_representation(algo2_result)
            RandomGraphTest.FAILED_NUMBER += 1
        self.assertEqual(l,
                         second=comparator.comparable_representation(algo2_result))

    @classmethod
    def tearDownClass(cls):
        print(RandomGraphTest.ERROR / RandomGraphTest.NUMBER_OF_TESTS)
        print(RandomGraphTest.ERROR / RandomGraphTest.FAILED_NUMBER
              if RandomGraphTest.FAILED_NUMBER is not 0
              else 0)


if __name__ == '__main__':
    unittest.main()
