from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import rnr_graph, lr_node
from graph_diff.graph_map import GraphMapComparatorByEdgeNum
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.complete_workflow_map import CompleteWorkflowMap
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter
from graph_diff.nirvana_object_model.simple_workflow_to_graph_converter import WorkflowToGraphConverter, \
    SimpleWorkflowToGraphConverter
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
workflow.add_connection_by_data(b2, 2, "json", b3, 1, "json")
workflow.add_connection_by_execution(b1, 1, b3, 1)

# WorkflowToDotConverter("1").convert_workflow(workflow).write("./nirvana.png", format="png")
# WorkflowToDotConverter("2").convert_workflow(workflow).write("./nirvana.png", format="png")

g = SimpleWorkflowToGraphConverter().convert(workflow)
write_graph(SimpleWorkflowToGraphConverter().convert(workflow), 'g.png')
nirv_converted = SimpleWorkflowToGraphConverter().reverse_graph(g)
# WorkflowToDotConverter("1").convert_workflow(nirv_converted).write("./nirvana.png", format="png")

g = CompleteWorkflowToGraphConverter().convert(workflow)
write_graph(g, 'g.png')
nirv_converted = CompleteWorkflowToGraphConverter().reverse_graph(g)
WorkflowToDotConverter("1").convert_workflow(nirv_converted).write("./nirvana.png", format="png")

workflow1 = workflow
workflow2 = Workflow()
workflow2.add_block(b1)
workflow2.add_block(b1)
workflow2.add_block(b2)
workflow2.add_block(b3)
workflow2.add_connection_by_data(b1, 1, "json", b2, 1, "json")
workflow2.add_connection_by_data(b1, 2, "json", b2, 1, "json")
workflow2.add_connection_by_data(b2, 1, "json", b3, 1, "json")
g1 = CompleteWorkflowToGraphConverter().convert(workflow1)
g2 = CompleteWorkflowToGraphConverter().convert(workflow2)
gm = BaselineAlgorithm(GraphMapComparatorByEdgeNum()).construct_diff(g1, g2)
write_graph(g1, "g1.png")
write_graph(g2, "g2.png")
write_diff(gm, "gm.png")

workflow, block_colors = CompleteWorkflowMap().convert_graph_map(gm)
WorkflowToDotConverter("1").convert_workflow(workflow, block_colors).write("./nirvana+.png", format="png")