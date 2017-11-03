from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_map import GraphMap
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.complete_workflow_to_graph_converter import CompleteWorkflowToGraphConverter
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow


class CompleteWorkflowMap:
    def convert_graph_map(self, graph_map: GraphMap):
        workflow = Workflow()

        input_label = CompleteWorkflowToGraphConverter.INPUT_LABEL
        output_label = CompleteWorkflowToGraphConverter.OUTPUT_LABEL

        from collections import defaultdict
        blocks_nums = defaultdict(int)

        def construct_set(graph_map_sub_set, graph_number):
            from collections import defaultdict
            inputs = defaultdict(set)
            outputs = defaultdict(set)
            block_blank = set()

            for node in graph_map_sub_set:
                if input_label in str(node.Label):
                    splitted = str(node.Label).split(input_label)
                    assert len(splitted) == 2
                    operation_id, nest = splitted[0], splitted[1]
                    inputs[operation_id, node.Number].add(nest)
                    block_blank.add((operation_id, node.Number))

                elif output_label in str(node.Label):
                    splitted = str(node.Label).split(output_label)
                    assert len(splitted) == 2
                    operation_id, nest = splitted[0], splitted[1]
                    outputs[operation_id, node.Number].add(nest)
                    block_blank.add((operation_id, node.Number))

            return [
                Block(Operation(operation_id=operation_id,
                                inputs=inputs[operation_id, number],
                                outputs=outputs[operation_id, number]))
                for operation_id, number in block_blank
            ], {(operation_id, number): i for i, (operation_id, number) in enumerate(block_blank)}

        self.block_overlap_from_first, self.map_for_matched = construct_set(graph_map.get_node_overlap_from_first(), 1)
        self.blocks_in_1_not_in_2, self.map_for_deleted = construct_set(graph_map.get_nodes_in_1_not_in_2(), 1)
        self.blocks_in_2_not_in_1, self.map_for_added = construct_set(graph_map.get_nodes_in_2_not_in_1(), 2)

        matcher = {}
        for (operation_id, number), i in self.map_for_matched.items():
            matcher[operation_id, number, 1] = self.block_overlap_from_first[i]
        for (operation_id, number), i in self.map_for_deleted.items():
            matcher[operation_id, number, 1] = self.blocks_in_1_not_in_2[i]
        for (operation_id, number), i in self.map_for_added.items():
            matcher[operation_id, number, 2] = self.blocks_in_2_not_in_1[i]

        from collections import defaultdict
        blocks_nums = defaultdict(int)
        num_of_the_block = {}
        block_colors = {}
        for block in self.block_overlap_from_first:
            blocks_nums[block] += 1
            num_of_the_block[id(block)] = blocks_nums[block]
            block_colors[block, blocks_nums[block]] = 'black'
            workflow.add_block(block)
        for block in self.blocks_in_1_not_in_2:
            blocks_nums[block] += 1
            num_of_the_block[id(block)] = blocks_nums[block]
            block_colors[block, blocks_nums[block]] = 'red'
            workflow.add_block(block)
        for block in self.blocks_in_2_not_in_1:
            blocks_nums[block] += 1
            num_of_the_block[id(block)] = blocks_nums[block]
            block_colors[block, blocks_nums[block]] = 'green'
            workflow.add_block(block)

        data_connection_colors = {}
        exc_connection_colors = {}

        def add_set_of_edges(graph_map_edge_set, graph_number, color, trans_graph_number, transform_node=lambda x: x):
            for from_node, to_node in graph_map_edge_set:
                if transform_node(from_node).Number != 0:
                    from_node = transform_node(from_node)
                    from_graph_number = trans_graph_number
                else:
                    from_graph_number = graph_number
                if transform_node(to_node).Number != 0:
                    to_node = transform_node(to_node)
                    to_graph_number = trans_graph_number
                else:
                    to_graph_number = graph_number
                if output_label in str(from_node.Label) and input_label in str(to_node.Label):
                    splitted = str(from_node.Label).split(output_label)
                    assert len(splitted) == 2
                    from_operation_id, output_nest = splitted[0], splitted[1]
                    splitted = str(to_node.Label).split(input_label)
                    assert len(splitted) == 2
                    to_operation_id, input_nest = splitted[0], splitted[1]
                    workflow.add_connection_by_data(
                            from_block=matcher[from_operation_id, from_node.Number, from_graph_number],
                            from_number=num_of_the_block[id(matcher[from_operation_id, from_node.Number, from_graph_number])],
                            output_nest=output_nest,
                            to_block=matcher[to_operation_id, to_node.Number, to_graph_number],
                            to_number=num_of_the_block[id(matcher[to_operation_id, to_node.Number, to_graph_number])],
                            input_nest=input_nest
                        )
                    data_connection_colors[
                            matcher[from_operation_id, from_node.Number, from_graph_number],
                            num_of_the_block[id(matcher[from_operation_id, from_node.Number, from_graph_number])],
                            output_nest,
                            matcher[to_operation_id, to_node.Number, to_graph_number],
                            num_of_the_block[id(matcher[to_operation_id, to_node.Number, to_graph_number])],
                            input_nest
                    ] = color
                elif input_label in str(from_node.Label):
                    pass
                elif from_node != GraphWithRepetitiveNodesWithRoot.ROOT:
                    if input_label not in to_node.Label and output_label not in to_node.Label:
                        workflow.add_connection_by_execution(
                            from_block=matcher[from_node.Label, from_node.Number, from_graph_number],
                            from_number=num_of_the_block[id(matcher[from_node.Label, from_node.Number, from_graph_number])],
                            to_block=matcher[to_node.Label, to_node.Number, to_graph_number],
                            to_number=num_of_the_block[id(matcher[to_node.Label, to_node.Number, to_graph_number])]
                        )
                        exc_connection_colors[
                            matcher[from_node.Label, from_node.Number, from_graph_number],
                            num_of_the_block[id(matcher[from_node.Label, from_node.Number, from_graph_number])],
                            matcher[to_node.Label, to_node.Number, to_graph_number],
                            num_of_the_block[id(matcher[to_node.Label, to_node.Number, to_graph_number])]
                        ] = color

        add_set_of_edges(graph_map.get_edge_overlap_from_first(), 1, 'black', 1)
        add_set_of_edges(graph_map.get_edges_in_1_not_in_2(), 1, 'red', 1)
        add_set_of_edges(graph_map.get_edges_in_2_not_in_1(), 2, 'green', 1, graph_map.map_from_2)

        return workflow, (lambda block, number: block_colors[block, number],
                          lambda from_block, from_number, output_nest, to_block, to_number, input_nest:
                          data_connection_colors[from_block, from_number, output_nest, to_block, to_number, input_nest],
                          lambda from_block, from_number, to_block, to_number:
                          exc_connection_colors[from_block, from_number, to_block, to_number])



