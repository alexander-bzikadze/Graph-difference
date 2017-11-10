from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph_map import GraphMapComparatorByEdgeNum
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.standard_workflow_generator import StandardWorkflowGenerator
from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter, print_together
from graph_diff.pipeline import Pipeline

NUMBER_OF_TESTS = 10
DIRECTORY = "../nirvana_diffs/"

import os

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

for i in range(0, NUMBER_OF_TESTS):
    generator = StandardWorkflowGenerator().generate_blocks()
    workflow1 = generator.generate_workflow()
    workflow2 = generator.generate_workflow()

    workflow1_dot = WorkflowToDotConverter('1').convert_workflow(workflow1)
    workflow2_dot = WorkflowToDotConverter('2').convert_workflow(workflow2)

    workflow_diff_dot = Pipeline(
        algorithm=BaselineAlgorithm(GraphMapComparatorByEdgeNum()),
        workflow_converter=CompleteWorkflowToGraphConverter()
    ).get_diff(workflow1=workflow1, workflow2=workflow2)

    try:
        print_together(workflow1_dot,
                       workflow_diff_dot,
                       workflow2_dot,
                       names=['workflow_1', 'workflow_diff', 'workflow_2']
        ).write(DIRECTORY + str(i) + '.png', format='png')
    except AssertionError:
        workflow1_dot.write("./workflow1_error.png", format='png')
        workflow2_dot.write("./workflow2_error.png", format='png')

    print("Test i=" + str(i) + " of n=" + str(NUMBER_OF_TESTS) + " done.")
