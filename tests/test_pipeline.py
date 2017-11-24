import unittest

from parameterized import parameterized

from graph_diff.ant_algorithm.algorithm import Algorithm as AntAlgorithm
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_map import GraphMapComparatorByEdgeNum
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.simple_workflow_to_graph_converter import SimpleWorkflowToGraphConverter
from graph_diff.nirvana_object_model.standard_workflow_generator import StandardWorkflowGenerator
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter
from graph_diff.pipeline import Pipeline


def generate_parameters(algo1, number_of_tests, *args):
    return sum([
        [(str(i) + "_" + str(type(generator).__name__),
          algo1,
          generator.generate_workflow(),
          generator.generate_workflow(),
          converter) for _ in range(0, number_of_tests)]
        for i, (generator, converter) in enumerate(args)
    ], [])


class GraphWithRepetitiveNodesWithRootTest(unittest.TestCase):
    NUMBER_OF_TESTS = 100
    comparator = GraphMapComparatorByEdgeNum()
    parameters = generate_parameters(AntAlgorithm(),
                                     NUMBER_OF_TESTS,
                                     (
                                         StandardWorkflowGenerator().generate_blocks(500, 1000),
                                         CompleteWorkflowToGraphConverter()),
                                     (StandardWorkflowGenerator().generate_blocks(500, 1000),
                                      SimpleWorkflowToGraphConverter()))

    @parameterized.expand(parameters)
    def test_random(self,
                    _,
                    algo1: GraphDiffAlgorithm,
                    graph1: Workflow,
                    graph2: Workflow,
                    converter: WorkflowToGraphConverter):
        Pipeline(
            algorithm=algo1,
            workflow_converter=converter
        ).get_diff(graph1, graph2)


if __name__ == '__main__':
    unittest.main()
