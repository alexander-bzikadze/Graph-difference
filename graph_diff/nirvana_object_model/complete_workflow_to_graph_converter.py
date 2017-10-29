from graph_diff.graph import rnr_graph, lr_node, GraphWithRepetitiveNodesWithRoot
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow

# noinspection PyAssignmentToLoopOrWithParameter
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter


class CompleteWorkflowToGraphConverter(WorkflowToGraphConverter):
    def __init__(self):
        pass

    OUTPUT_LABEL = "<o>"
    INPUT_LABEL = "<i>"

    # noinspection PyPep8Naming
    @staticmethod
    def convert(workflow: Workflow):
        graph = rnr_graph()

        INPUT_LABEL = CompleteWorkflowToGraphConverter.INPUT_LABEL
        OUTPUT_LABEL = CompleteWorkflowToGraphConverter.OUTPUT_LABEL

        from collections import defaultdict
        number_of_blocks = defaultdict(int)

        for block in workflow:
            number_of_blocks[block] += 1
            block_node = lr_node(block.operation.operation_id, number_of_blocks[block])
            graph.add_node(block_node)

            for nest in block.operation.inputs:
                nest_node = lr_node(block.operation.operation_id + INPUT_LABEL + nest, number_of_blocks[block])
                graph.add_node(nest_node)
                graph.add_edge_exp(nest_node,
                                   block_node)

            for nest in block.operation.outputs:
                nest_node = lr_node(block.operation.operation_id + OUTPUT_LABEL + nest, number_of_blocks[block])
                graph.add_node(nest_node)
                graph.add_edge_exp(block_node,
                                   nest_node)

        for (from_block, from_num, output_nest), a2 in workflow.items():
            for to_block, to_num, input_nest in a2:
                graph.add_edge_exp(lr_node(from_block.operation.operation_id + OUTPUT_LABEL + output_nest, from_num),
                                   lr_node(to_block.operation.operation_id + INPUT_LABEL + input_nest, to_num))

        for (from_block, from_num), a2 in workflow.items_by_exc():
            for to_block, to_num in a2:
                graph.add_edge_exp(lr_node(from_block.operation.operation_id, from_num),
                                   lr_node(to_block.operation.operation_id, to_num))

        return graph

    # noinspection PyPep8Naming
    @staticmethod
    def reverse_graph(graph: GraphWithRepetitiveNodesWithRoot):
        workflow = Workflow()

        INPUT_LABEL = CompleteWorkflowToGraphConverter.INPUT_LABEL
        OUTPUT_LABEL = CompleteWorkflowToGraphConverter.OUTPUT_LABEL

        from collections import defaultdict
        inputs = defaultdict(set)
        outputs = defaultdict(set)
        block_blank = set()

        for node in graph:
            if INPUT_LABEL in str(node.Label):
                splitted = str(node.Label).split(INPUT_LABEL)
                assert len(splitted) == 2
                operation_id, nest = splitted[0], splitted[1]
                inputs[operation_id, node.Number].add(nest)
                block_blank.add((operation_id, node.Number))

            elif OUTPUT_LABEL in str(node.Label):
                splitted = str(node.Label).split(OUTPUT_LABEL)
                assert len(splitted) == 2
                operation_id, nest = splitted[0], splitted[1]
                outputs[operation_id, node.Number].add(nest)
                block_blank.add((operation_id, node.Number))

            elif node.Label != 0:
                block_blank.add((node.Label, node.Number))

        for operation_id, number in block_blank:
            workflow.add_block(Block(Operation(operation_id=operation_id,
                                               inputs=inputs[operation_id, number],
                                               outputs=outputs[operation_id, number])))

        for from_node in graph:
            if OUTPUT_LABEL in str(from_node.Label):
                splitted = str(from_node.Label).split(OUTPUT_LABEL)
                assert len(splitted) == 2
                from_operation_id, output_nest = splitted[0], splitted[1]
                for to_node in graph.get_list_of_adjacent_nodes(from_node):
                    if INPUT_LABEL not in str(to_node.Label):
                        continue
                    splitted = str(to_node.Label).split(INPUT_LABEL)
                    assert len(splitted) == 2
                    to_operation_id, input_nest = splitted[0], splitted[1]
                    workflow.add_connection_by_data(
                        from_block=Block(Operation(operation_id=from_operation_id,
                                                   inputs=inputs[from_operation_id, from_node.Number],
                                                   outputs=outputs[from_operation_id, from_node.Number])),
                        from_number=from_node.Number,
                        output_nest=output_nest,
                        to_block=Block(Operation(operation_id=to_operation_id,
                                                 inputs=inputs[to_operation_id, to_node.Number],
                                                 outputs=outputs[to_operation_id, to_node.Number])),
                        to_number=to_node.Number,
                        input_nest=input_nest
                    )
            elif INPUT_LABEL in str(from_node.Label):
                pass
            elif from_node.Label != 0:
                for to_node in graph.get_list_of_adjacent_nodes(from_node):
                    if INPUT_LABEL not in to_node.Label and OUTPUT_LABEL not in to_node.Label:
                        workflow.add_connection_by_execution(from_block=Block(Operation(operation_id=from_node.Label,
                                                                                        inputs=inputs[from_node.Label, from_node.Number],
                                                                                        outputs=outputs[from_node.Label, from_node.Number])),
                                                             from_number=from_node.Number,
                                                             to_block=Block(Operation(operation_id=to_node.Label,
                                                                                      inputs=inputs[to_node.Label, to_node.Number],
                                                                                      outputs=outputs[to_node.Label, to_node.Number])),
                                                             to_number=to_node.Number)
        return workflow
