import unittest

from parameterized import parameterized

from graph_diff.ant_algorithm.algorithm import Algorithm as AntAlgorithm
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_diff_algorithm.graph_map_comparator import GraphMapComparatorByEdgeNum
from graph_diff.new_ant_algorithm import NewAntAlgorithm
from graph_diff.nirvana_object_model.pipeline import Pipeline
from graph_diff.nirvana_object_model.worflow_generator.standard_workflow_generator import StandardWorkflowGenerator
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter
from graph_diff.nirvana_object_model.workflow_to_graph_converter.complete_workflow_to_graph_converter import \
    CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.workflow_to_graph_converter.simple_workflow_to_graph_converter import \
    SimpleWorkflowToGraphConverter


def generate_parameters(algo, number_of_tests, *args):
    return sum([[(str(i) + "_" + str(type(generator).__name__),
                  algo,
                  generator.generate_workflow(),
                  generator.generate_workflow(),
                  converter) for _ in range(0, number_of_tests)]
                for i, (generator, converter) in enumerate(args)], [])


class GraphWithRepetitiveNodesWithRootTest(unittest.TestCase):
    NUMBER_OF_TESTS = 10
    comparator = GraphMapComparatorByEdgeNum()
    parameters = sum([generate_parameters(algo,
                                          NUMBER_OF_TESTS,
                                          (StandardWorkflowGenerator().generate_blocks(20, 200),
                                           CompleteWorkflowToGraphConverter()),
                                          (StandardWorkflowGenerator().generate_blocks(20, 200),
                                           SimpleWorkflowToGraphConverter()))
                      for algo in (AntAlgorithm(), NewAntAlgorithm())], [])

    @parameterized.expand(parameters)
    def test_random(self,
                    _,
                    algo: GraphDiffAlgorithm,
                    graph1: Workflow,
                    graph2: Workflow,
                    converter: WorkflowToGraphConverter):
        Pipeline(algorithm=algo,
                 workflow_converter=converter).get_diff(graph1, graph2)


if __name__ == '__main__':
    unittest.main()
