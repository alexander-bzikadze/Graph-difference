import json
import unittest

from graph_diff.ant_algorithm import AntAlgorithm
from graph_diff.cpp_algorithms.algorithms import CppImport
from graph_diff.graph_diff_algorithm.compose_graph_diff_algorithm import ComposedGraphDiffAlgorithm
from graph_diff.nirvana_object_model import Pipeline
from graph_diff.nirvana_object_model import workflow_deserializer
from graph_diff.nirvana_object_model.workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.simulated_annealing_algorithm.algorithm import Algorithm as SimAnnealAlgorithm


class NirvanaWorkflowDeserializerTest(unittest.TestCase):
    def test_deserialization_should_work_correctly_with_repeating_blocks(self):
        actual = ''
        with open('process_instance_simple.json') as f:
            workflow = workflow_deserializer.deserialize(json.loads(f.read()))
            for connection in workflow.items():
                (source_block, source_block_count, source_name) = connection[0]
                for target in connection[1]:
                    (target_block, target_block_count, target_name) = target
                    actual += '%s (№%s) %s -> %s (№%s) %s\n' % (
                        source_block.operation.operation_id, source_block_count, source_name,
                        target_block.operation.operation_id, target_block_count, target_name)
        print(actual)
        with open('process_instance_pretty.txt', 'r') as f:
            expected = f.read()
        self.assertEqual(actual, expected)

    def test_algorithm_on_deserialization(self):
        with open('process_instance.json') as f:
            workflow1 = workflow_deserializer.deserialize(json.loads(f.read()))

        with open('process_instance_upgraded.json') as f:
            workflow2 = workflow_deserializer.deserialize(json.loads(f.read()))

        # Pipeline(AntAlgorithm(), CompleteWorkflowToGraphConverter()).get_diff(workflow1, workflow1)
        # Pipeline(CppImport.LinAntAlgorithm(), CompleteWorkflowToGraphConverter()).get_diff(workflow1, workflow1)
        # Pipeline(SimAnnealAlgorithm(), CompleteWorkflowToGraphConverter()).get_diff(workflow1, workflow1)
        Pipeline(ComposedGraphDiffAlgorithm(CppImport.LinAntAlgorithm(), SimAnnealAlgorithm()),
                 CompleteWorkflowToGraphConverter()).get_diff(workflow1, workflow1)
        # Pipeline(NewAntAlgorithm(), CompleteWorkflowToGraphConverter()).get_diff(workflow1, workflow2)
        # Pipeline(CppRun.AntAlgorithm(), CompleteWorkflowToGraphConverter()).get_diff(workflow1, workflow2)


if __name__ == '__main__':
    unittest.main()
