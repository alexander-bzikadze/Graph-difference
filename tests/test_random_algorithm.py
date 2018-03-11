import unittest

from parameterized import parameterized

from graph_diff.ant_algorithm import AntAlgorithm
from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import StandardGraphGenerator, GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_diff_algorithm.graph_map_comparator import GraphMapComparatorByEdgeNum, GraphMapComparator
from graph_diff.new_ant_algorithm import NewAntAlgorithm


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
                                          StandardGraphGenerator(0, 10))
                      for algo in [BaselineAlgorithm(), AntAlgorithm(), NewAntAlgorithm()]], [])

    @parameterized.expand(parameters)
    def test_random(self,
                    _,
                    algo: GraphDiffAlgorithm,
                    graph: GraphWithRepetitiveNodesWithRoot,
                    comparator: GraphMapComparator):
        algo2_result = algo.construct_diff(graph, graph)
        l = sum([len(graph.get_list_of_adjacent_nodes(v)) for v in graph])
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
