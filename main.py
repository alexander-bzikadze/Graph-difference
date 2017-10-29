from graph_diff.graph import rnr_graph, lr_node
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter
from graph_diff.nirvana_object_model.simple_workflow_to_graph_converter import WorkflowToGraphConverter, \
    SimpleWorkflowToGraphConverter
from graph_diff.to_dot_converter import write_graph

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
