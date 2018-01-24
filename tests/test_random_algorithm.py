import unittest

from parameterized import parameterized

from graph_diff.ant_algorithm.algorithm import Algorithm as AntAlgorithm
from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import StandardGraphGenerator, GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_map import GraphMapComparatorByEdgeNum, GraphMapComparator


def generate_parameters(algo1, algo2, comparator, number_of_tests, *args):
    return sum([
        [(str(i) + "_" + str(type(generator).__name__),
          algo1,
          algo2,
          generator.generate_graph(),
          generator.generate_graph(),
          comparator) for _ in range(0, number_of_tests)]
        for i, generator in enumerate(args)
    ], [])


class GraphWithRepetitiveNodesWithRootTest(unittest.TestCase):
    NUMBER_OF_TESTS = 100

    ERROR = 0
    FAILED_NUMBER = 0

    # parameters = generate_parameters(BaselineAlgorithm(),
    #                                  Algorithm(),
    #                                  GraphMapComparatorByEdgeNum(),
    #                                  NUMBER_OF_TESTS,
    #                                  StandardGraphGenerator(0, 5))

    parameters = generate_parameters(AntAlgorithm(),
                                     BaselineAlgorithm(),
                                     GraphMapComparatorByEdgeNum(),
                                     NUMBER_OF_TESTS,
                                     StandardGraphGenerator(0, 10))

    # parameters = generate_parameters(NewAntAlgorithm(),
    #                                  BaselineAlgorithm(),
    #                                  GraphMapComparatorByEdgeNum(),
    #                                  NUMBER_OF_TESTS,
    #                                  StandardGraphGenerator(0, 10))

    # parameters = generate_parameters(AntAlgorithm(),
    #                                  AntAlgorithm(),
    #                                  GraphMapComparatorByEdgeNum(),
    #                                  NUMBER_OF_TESTS,
    #                                  StandardGraphGenerator(0, 60))

    @parameterized.expand(parameters)
    def test_random(self,
                    _,
                    algo1: GraphDiffAlgorithm,
                    algo2: GraphDiffAlgorithm,
                    graph1: GraphWithRepetitiveNodesWithRoot,
                    graph2: GraphWithRepetitiveNodesWithRoot,
                    comparator: GraphMapComparator):
        algo1_result = algo1.construct_diff(graph1, graph2)
        algo2_result = algo2.construct_diff(graph1, graph2)

        if comparator.comparable_representation(algo1_result) != comparator.comparable_representation(algo2_result):
            GraphWithRepetitiveNodesWithRootTest.FAILED_NUMBER += 1
            GraphWithRepetitiveNodesWithRootTest.ERROR += abs(
                comparator.comparable_representation(algo1_result) - comparator.comparable_representation(algo2_result))

        self.assertEqual(first=comparator.comparable_representation(algo1_result),
                         second=comparator.comparable_representation(algo2_result))

    @classmethod
    def tearDownClass(cls):
        print(GraphWithRepetitiveNodesWithRootTest.ERROR / GraphWithRepetitiveNodesWithRootTest.NUMBER_OF_TESTS)
        print(GraphWithRepetitiveNodesWithRootTest.ERROR / GraphWithRepetitiveNodesWithRootTest.FAILED_NUMBER
              if GraphWithRepetitiveNodesWithRootTest.FAILED_NUMBER is not 0 else 0)


if __name__ == '__main__':
    unittest.main()
