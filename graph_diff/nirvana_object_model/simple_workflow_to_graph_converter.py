from graph_diff.graph import rnr_graph, lr_node, GraphWithRepetitiveNodesWithRoot
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow


# noinspection PyAssignmentToLoopOrWithParameter
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter


class SimpleWorkflowToGraphConverter(WorkflowToGraphConverter):
    def __init__(self): pass

    @staticmethod
    def convert(workflow: Workflow):
        graph = rnr_graph()
        from collections import defaultdict
        number_of_blocks = defaultdict(int)
        for block in workflow:
            number_of_blocks[block] += 1
            graph.add_node(lr_node(block.operation.operation_id, number_of_blocks[block]))

        for (from_block, from_num, _), a2 in workflow.items():
            for to_block, to_num, _ in a2:
                graph.add_edge_exp(lr_node(from_block.operation.operation_id, from_num),
                                   lr_node(to_block.operation.operation_id, to_num))

        for (from_block, from_num), a2 in workflow.items_by_exc():
            for to_block, to_num in a2:
                graph.add_edge_exp(lr_node(from_block.operation.operation_id, from_num),
                                   lr_node(to_block.operation.operation_id, to_num))

        return graph

    @staticmethod
    def reverse_graph(graph: GraphWithRepetitiveNodesWithRoot):
        workflow = Workflow()
        for node in graph:
            if node.Label != 0:
                workflow.add_block(Block(Operation(str(node.Label))))
        for from_node in graph:
            if from_node.Label != 0:
                for to_node in graph.get_list_of_adjacent_nodes(from_node):
                    workflow.add_connection_by_execution(from_block=Block(Operation(str(from_node.Label))),
                                                         from_number=from_node.Number,
                                                         to_block=Block(Operation(str(to_node.Label))),
                                                         to_number=to_node.Number)
        return workflow
