import logging

import logging_config
from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph_map import GraphMapComparatorByEdgeNum
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.standard_workflow_generator import StandardWorkflowGenerator
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter
from graph_diff.pipeline import Pipeline

logging.info("Creating first workflow")

workflow = Workflow()
b1 = Block(operation=Operation("1", (), ["json", "html"]))
b2 = Block(operation=Operation("2", ["json"], ["json"]))
b3 = Block(operation=Operation("3", ["json"]))
workflow.add_block(b1)
workflow.add_block(b2)
workflow.add_block(b2)
workflow.add_block(b3)
workflow.add_connection_by_data(b1, 1, "json", b2, 1, "json")
workflow.add_connection_by_data(b2, 1, "json", b3, 1, "json")
workflow.add_connection_by_data(b1, 1, "json", b2, 2, "json")
workflow.add_connection_by_data(b1, 1, "json", b3, 1, "json")
workflow.add_connection_by_data(b2, 2, "json", b3, 1, "json")
workflow.add_connection_by_execution(b1, 1, b3, 1)

logging_config.logging.info("Creating second workflow")

workflow1 = workflow
workflow2 = Workflow()
workflow2.add_block(b1)
workflow2.add_block(b1)
workflow2.add_block(b2)
workflow2.add_block(b3)
workflow2.add_connection_by_data(b1, 1, "json", b2, 1, "json")
workflow2.add_connection_by_data(b1, 2, "json", b2, 1, "json")
workflow2.add_connection_by_data(b2, 1, "json", b3, 1, "json")

logging.info("Run pipeline with Complete converter on workflows 1 and 2. Result printed to nirvana+")
Pipeline(BaselineAlgorithm(GraphMapComparatorByEdgeNum()), CompleteWorkflowToGraphConverter()).print_diff(
    workflow1=workflow1, workflow2=workflow2, path="./nirvana+.png")

generator = StandardWorkflowGenerator().generate_blocks()

logging.info("Generation two workflows")
w = generator.generate_workflow()
w1 = generator.generate_workflow()

logging.info("Converting workflows to dot")
w_dot = WorkflowToDotConverter('1').convert_workflow(w)
w1_dot = WorkflowToDotConverter('2').convert_workflow(w1)

w_dot.write("./w.png", format='png')
w1_dot.write("./w1.png", format='png')

logging.info("Run pipeline on generated workflows")
w2_dot = Pipeline(BaselineAlgorithm(GraphMapComparatorByEdgeNum()), CompleteWorkflowToGraphConverter()).get_diff(w, w1)

# print_together(w_dot, w2_dot, w1_dot, names=['w_dot', 'w2_dot', 'w1_dot']).write("./w2.png", format='png')
