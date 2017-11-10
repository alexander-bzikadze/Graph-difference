from graph_diff.graph import rnr_graph, lr_node, GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_map import GraphMap
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow

# noinspection PyAssignmentToLoopOrWithParameter
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter


class CompleteWorkflowToGraphConverter(WorkflowToGraphConverter):
    NEST_DIVIDER = "<n>"
    KEY_VALUE_DIVIDER = "<:>"
    KEY_VALUE_BLOCK_DIVIDER = "<;>"
    INPUT_DIVIDER = "<i>"
    OUTPUT_DIVIDER = "<o>"

    def block_id(self, block: Block):
        return_list = [
            block.operation.operation_id,
            self.KEY_VALUE_BLOCK_DIVIDER.join(
                [key + self.KEY_VALUE_DIVIDER + value for key, value in block.options]
            )
        ]
        return self.NEST_DIVIDER.join(return_list)

    def input_nest_id(self, block: Block, nest_id: str):
        return_list = [
            block.operation.operation_id,
            self.KEY_VALUE_BLOCK_DIVIDER.join(
                [key + self.KEY_VALUE_DIVIDER + value for key, value in block.options]
            ),
            nest_id + self.INPUT_DIVIDER
        ]
        return self.NEST_DIVIDER.join(return_list)

    def output_nest_id(self, block: Block, nest_id: str):
        return_list = [
            block.operation.operation_id,
            self.KEY_VALUE_BLOCK_DIVIDER.join(
                [key + self.KEY_VALUE_DIVIDER + value for key, value in block.options]
            ),
            nest_id + self.OUTPUT_DIVIDER
        ]
        return self.NEST_DIVIDER.join(return_list)

    def is_input_nest(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        return self.INPUT_DIVIDER in str(node.Label)

    def is_output_nest(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        return self.OUTPUT_DIVIDER in str(node.Label)

    def get_input_nest(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        splitted = str(node.Label).split(self.NEST_DIVIDER)
        assert len(splitted) == 3
        operation_id, key_values, input_nest = splitted[0], splitted[1], splitted[2]
        key_values = dict([
                              tuple(key_value.split(self.KEY_VALUE_DIVIDER)) for key_value in
                              key_values.split(self.KEY_VALUE_BLOCK_DIVIDER)
                          ] if len(key_values) > 0 else [])
        return operation_id, key_values, input_nest.split(self.INPUT_DIVIDER)[0]

    def get_output_nest(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        splitted = str(node.Label).split(self.NEST_DIVIDER)
        assert len(splitted) == 3
        operation_id, key_values, output_nest = splitted[0], splitted[1], splitted[2]
        key_values = dict([
                              tuple(key_value.split(self.KEY_VALUE_DIVIDER)) for key_value in
                              key_values.split(self.KEY_VALUE_BLOCK_DIVIDER)
                          ] if len(key_values) > 0 else [])
        return operation_id, key_values, output_nest.split(self.OUTPUT_DIVIDER)[0]

    def get_block_id(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        splitted = str(node.Label).split(self.NEST_DIVIDER)
        assert len(splitted) == 2
        operation_id, key_values = splitted[0], splitted[1]
        key_values = dict([
                              tuple(key_value.split(self.KEY_VALUE_DIVIDER)) for key_value in
                              key_values.split(self.KEY_VALUE_BLOCK_DIVIDER)
                          ] if len(key_values) > 0 else [])
        return operation_id, key_values

    def convert(self, workflow: Workflow) -> GraphWithRepetitiveNodesWithRoot:
        graph = rnr_graph()

        from collections import defaultdict
        number_of_blocks = defaultdict(int)

        for block in workflow:
            number_of_blocks[block] += 1
            block_node = lr_node(self.block_id(block), number_of_blocks[block])
            graph.add_node(block_node)

            for nest in block.operation.inputs:
                nest_node = lr_node(self.input_nest_id(block, nest), number_of_blocks[block])
                graph.add_node(nest_node)
                graph.add_edge_exp(nest_node,
                                   block_node)

            for nest in block.operation.outputs:
                nest_node = lr_node(self.output_nest_id(block, nest), number_of_blocks[block])
                graph.add_node(nest_node)
                graph.add_edge_exp(block_node,
                                   nest_node)

        for (from_block, from_num, output_nest), a2 in workflow.items():
            for to_block, to_num, input_nest in a2:
                graph.add_edge_exp(lr_node(self.output_nest_id(from_block, output_nest), from_num),
                                   lr_node(self.input_nest_id(to_block, input_nest), to_num))

        for (from_block, from_num), a2 in workflow.items_by_exc():
            for to_block, to_num in a2:
                graph.add_edge_exp(lr_node(self.block_id(from_block), from_num),
                                   lr_node(self.block_id(to_block), to_num))

        return graph

    def reverse_graph(self, graph: GraphWithRepetitiveNodesWithRoot) -> Workflow:
        workflow = Workflow()

        from collections import defaultdict
        inputs = defaultdict(set)
        outputs = defaultdict(set)
        block_blank = set()

        for node in graph:
            if self.is_input_nest(node):
                operation_id, key_values, nest = self.get_input_nest(node)
                inputs[operation_id, tuple(key_values.items()), node.Number].add(nest)
                block_blank.add((operation_id, key_values, node.Number))

            elif self.is_output_nest(node):
                operation_id, key_values, nest = self.get_output_nest(node)
                outputs[operation_id, tuple(key_values.items()), node.Number].add(nest)
                block_blank.add((operation_id, key_values, node.Number))

            elif node != GraphWithRepetitiveNodesWithRoot.ROOT:
                operation_id, key_values = self.get_block_id(node)
                block_blank.add((operation_id, tuple(key_values.items()), node.Number))

        for operation_id, key_values, number in block_blank:
            block_input = inputs[operation_id, tuple(key_values.items()), number]
            block_output = outputs[operation_id, tuple(key_values.items()), number]
            workflow.add_block(new_block=Block(operation=Operation(operation_id=operation_id,
                                                                   inputs=block_input,
                                                                   outputs=block_output),
                                               options=key_values))

        for from_node in graph:
            if self.is_output_nest(from_node):
                from_operation_id, from_key_values, from_nest = self.get_output_nest(from_node)
                for to_node in graph.get_list_of_adjacent_nodes(from_node):
                    if not self.is_input_nest(to_node):
                        continue
                    to_operation_id, to_key_values, to_nest = self.get_input_nest(to_node)
                    from_input = inputs[from_operation_id, tuple(from_key_values.items()), from_node.Number],
                    from_output = outputs[from_operation_id, tuple(from_key_values.items()), from_node.Number]
                    to_input = inputs[to_operation_id, tuple(to_key_values.items()), to_node.Number]
                    to_output = outputs[to_operation_id, tuple(to_key_values.items()), to_node.Number]
                    workflow.add_connection_by_data(
                        from_block=Block(operation=Operation(operation_id=from_operation_id,
                                                             inputs=from_input,
                                                             outputs=from_output),
                                         options=from_key_values),
                        from_number=from_node.Number,
                        output_nest=from_nest,
                        to_block=Block(operation=Operation(operation_id=to_operation_id,
                                                           inputs=to_input,
                                                           outputs=to_output),
                                       options=to_key_values),
                        to_number=to_node.Number,
                        input_nest=to_nest
                    )
            elif self.is_input_nest(from_node):
                pass
            elif from_node != GraphWithRepetitiveNodesWithRoot.ROOT:
                from_operation_id, from_key_values = self.get_block_id(from_node)
                for to_node in graph.get_list_of_adjacent_nodes(from_node):
                    if self.is_input_nest(to_node) and self.is_output_nest(to_node):
                        to_operation_id, to_key_values = self.get_block_id(to_node)
                        from_input = inputs[from_operation_id, tuple(from_key_values.items()), from_node.Number],
                        from_output = outputs[from_operation_id, tuple(from_key_values.items()), from_node.Number]
                        to_input = inputs[to_operation_id, tuple(to_key_values.items()), to_node.Number]
                        to_output = outputs[to_operation_id, tuple(to_key_values.items()), to_node.Number]
                        workflow.add_connection_by_execution(
                            from_block=Block(operation=Operation(operation_id=from_operation_id,
                                                                 inputs=from_input,
                                                                 outputs=from_output),
                                             options=from_key_values),
                            from_number=from_node.Number,
                            to_block=Block(Operation(operation_id=to_node.Label,
                                                     inputs=to_input,
                                                     outputs=to_output),
                                           options=to_key_values),
                            to_number=to_node.Number)
        return workflow

    def convert_graph_map(self, graph_map: GraphMap):
        workflow = Workflow()

        def construct_set(graph_map_sub_set):
            from collections import defaultdict
            inputs = defaultdict(set)
            outputs = defaultdict(set)
            block_blank = set()

            for node in graph_map_sub_set:
                if self.is_input_nest(node):
                    operation_id, key_values, nest = self.get_input_nest(node)
                    inputs[operation_id, tuple(key_values.items()), node.Number].add(nest)
                    block_blank.add((operation_id, tuple(key_values.items()), node.Number))

                elif self.is_output_nest(node):
                    operation_id, key_values, nest = self.get_output_nest(node)
                    outputs[operation_id, tuple(key_values.items()), node.Number].add(nest)
                    block_blank.add((operation_id, tuple(key_values.items()), node.Number))

                elif node != GraphWithRepetitiveNodesWithRoot.ROOT:
                    operation_id, key_values = self.get_block_id(node)
                    block_blank.add((operation_id, tuple(key_values.items()), node.Number))

            return [
                       Block(Operation(operation_id=operation_id,
                                       inputs=inputs[operation_id, key_values_tuple, number],
                                       outputs=outputs[operation_id, key_values_tuple, number]),
                             options=key_values_tuple)
                       for operation_id, key_values_tuple, number in block_blank
                   ], {(operation_id, key_values_tuple, number): i for i, (operation_id, key_values_tuple, number) in
                       enumerate(block_blank)}

        # Construction of different lists of blocks and their parameters and number in list.
        block_overlap_from_first, map_for_matched = construct_set(graph_map.get_node_overlap_from_first())
        blocks_in_1_not_in_2, map_for_deleted = construct_set(graph_map.get_nodes_in_1_not_in_2())
        blocks_in_2_not_in_1, map_for_added = construct_set(graph_map.get_nodes_in_2_not_in_1())

        matcher = {}
        for (operation_id, key_values_tuple, number), i in map_for_matched.items():
            matcher[operation_id, key_values_tuple, number, 1] = block_overlap_from_first[i]
        for (operation_id, key_values_tuple, number), i in map_for_deleted.items():
            matcher[operation_id, key_values_tuple, number, 1] = blocks_in_1_not_in_2[i]
        for (operation_id, key_values_tuple, number), i in map_for_added.items():
            matcher[operation_id, key_values_tuple, number, 2] = blocks_in_2_not_in_1[i]

        from collections import defaultdict
        blocks_nums = defaultdict(int)
        num_of_the_block = {}
        block_colors = {}
        for block in block_overlap_from_first:
            blocks_nums[block] += 1
            num_of_the_block[id(block)] = blocks_nums[block]
            block_colors[block, blocks_nums[block]] = 'black'
            workflow.add_block(block)
        for block in blocks_in_1_not_in_2:
            blocks_nums[block] += 1
            num_of_the_block[id(block)] = blocks_nums[block]
            block_colors[block, blocks_nums[block]] = 'red'
            workflow.add_block(block)
        for block in blocks_in_2_not_in_1:
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
                if self.is_output_nest(from_node) and self.is_input_nest(to_node):
                    from_operation_id, from_key_values, from_nest = self.get_output_nest(from_node)
                    to_operation_id, to_key_values, to_nest = self.get_input_nest(to_node)
                    from_block = matcher[
                        from_operation_id, tuple(from_key_values.items()), from_node.Number, from_graph_number]
                    to_block = matcher[to_operation_id, tuple(to_key_values.items()), to_node.Number, to_graph_number]
                    workflow.add_connection_by_data(
                        from_block=from_block,
                        from_number=num_of_the_block[id(from_block)],
                        output_nest=from_nest,
                        to_block=to_block,
                        to_number=num_of_the_block[id(to_block)],
                        input_nest=to_nest
                    )
                    data_connection_colors[
                        from_block,
                        num_of_the_block[id(from_block)],
                        from_nest,
                        to_block,
                        num_of_the_block[id(to_block)],
                        to_nest
                    ] = color
                elif self.is_input_nest(from_node):
                    pass
                elif from_node != GraphWithRepetitiveNodesWithRoot.ROOT:
                    if not self.is_input_nest(to_node) and not self.is_output_nest(to_node):
                        from_operation_id, from_key_values = self.get_block_id(from_node)
                        to_operation_id, to_key_values = self.get_block_id(to_node)
                        from_block = matcher[
                            from_operation_id, tuple(from_key_values.items()), from_node.Number, from_graph_number]
                        to_block = matcher[
                            to_operation_id, tuple(to_key_values.items()), to_node.Number, to_graph_number]
                        workflow.add_connection_by_execution(
                            from_block=from_block,
                            from_number=num_of_the_block[id(from_block)],
                            to_block=to_block,
                            to_number=num_of_the_block[id(to_block)]
                        )
                        exc_connection_colors[
                            from_block,
                            num_of_the_block[id(from_block)],
                            to_block,
                            num_of_the_block[id(to_block)]
                        ] = color

        # Constructing sets and setting colors
        add_set_of_edges(graph_map.get_edge_overlap_from_first(), 1, 'black', 1)
        add_set_of_edges(graph_map.get_edges_in_1_not_in_2(), 1, 'red', 1)
        add_set_of_edges(graph_map.get_edges_in_2_not_in_1(), 2, 'green', 1, graph_map.map_from_2)

        return workflow, (lambda lam_block, lam_number: block_colors[lam_block, lam_number],
                          lambda from_block, from_number, output_nest, to_block, to_number, input_nest:
                          data_connection_colors[from_block, from_number, output_nest, to_block, to_number, input_nest],
                          lambda from_block, from_number, to_block, to_number:
                          exc_connection_colors[from_block, from_number, to_block, to_number])
