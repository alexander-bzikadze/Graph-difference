from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import rnr_graph, lr_node
from graph_diff.graph_map import GraphMapComparatorByEdgeNum
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.standard_workflow_generator import StandardWorkflowGenerator
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter, print_together
from graph_diff.nirvana_object_model.simple_workflow_to_graph_converter import WorkflowToGraphConverter, \
    SimpleWorkflowToGraphConverter
from graph_diff.pipeline import Pipeline
from graph_diff.to_dot_converter import write_graph, write_diff

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

workflow1 = workflow
workflow2 = Workflow()
workflow2.add_block(b1)
workflow2.add_block(b1)
workflow2.add_block(b2)
workflow2.add_block(b3)
workflow2.add_connection_by_data(b1, 1, "json", b2, 1, "json")
workflow2.add_connection_by_data(b1, 2, "json", b2, 1, "json")
workflow2.add_connection_by_data(b2, 1, "json", b3, 1, "json")


w = StandardWorkflowGenerator().generate_workflow()
w1 = StandardWorkflowGenerator().generate_workflow()

Pipeline(BaselineAlgorithm(GraphMapComparatorByEdgeNum()), CompleteWorkflowToGraphConverter()).print_diff(
    workflow1=workflow1, workflow2=workflow2, path="./nirvana+.png")

w2 = Pipeline(BaselineAlgorithm(GraphMapComparatorByEdgeNum()), CompleteWorkflowToGraphConverter()).get_diff(
    workflow1=w1, workflow2=w)

w = WorkflowToDotConverter().convert_workflow(w)
w1 = WorkflowToDotConverter().convert_workflow(w1)

print_together(w, w1).write("./w.png", format='png')
