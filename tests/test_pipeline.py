import unittest

from parameterized import parameterized

from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_map import GraphMapComparatorByEdgeNum
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.simple_workflow_to_graph_converter import SimpleWorkflowToGraphConverter
from graph_diff.nirvana_object_model.standard_workflow_generator import StandardWorkflowGenerator
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter
from graph_diff.pipeline import Pipeline


def generate_parameters(algo1, algo2, number_of_tests, *args):
    return sum([
        [(str(i) + "_" + str(type(generator).__name__),
          algo1,
          algo2,
          generator.generate_workflow(),
          generator.generate_workflow(),
          converter) for _ in range(0, number_of_tests)]
        for i, (generator, converter) in enumerate(args)
    ], [])


class GraphWithRepetitiveNodesWithRootTest(unittest.TestCase):
    NUMBER_OF_TESTS = 1000
    comparator = GraphMapComparatorByEdgeNum()
    parameters = generate_parameters(BaselineAlgorithm(),
                                     BaselineAlgorithm(),
                                     NUMBER_OF_TESTS,
                                     (
                                     StandardWorkflowGenerator().generate_blocks(), CompleteWorkflowToGraphConverter()),
                                     (StandardWorkflowGenerator().generate_blocks(), SimpleWorkflowToGraphConverter()))

    @parameterized.expand(parameters)
    def test_random(self,
                    _,
                    algo1: GraphDiffAlgorithm,
                    algo2: GraphDiffAlgorithm,
                    graph1: GraphWithRepetitiveNodesWithRoot,
                    graph2: GraphWithRepetitiveNodesWithRoot,
                    converter: WorkflowToGraphConverter):
        Pipeline(
            algorithm=BaselineAlgorithm(),
            workflow_converter=converter
        )


if __name__ == '__main__':
    unittest.main()
