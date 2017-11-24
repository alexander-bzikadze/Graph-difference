from graph_diff.graph import rnr_graph, lr_node, GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_map import GraphMap
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.graph_map_dot_colorer import GraphMapDotColorer, GraphDotColorer
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
                sorted([key + self.KEY_VALUE_DIVIDER + value for key, value in block.options])
            )
        ]
        return self.NEST_DIVIDER.join(return_list)

    def input_nest_id(self, block: Block, nest_id: str):
        return_list = [
            block.operation.operation_id,
            self.KEY_VALUE_BLOCK_DIVIDER.join(
                sorted([key + self.KEY_VALUE_DIVIDER + value for key, value in block.options])
            ),
            nest_id + self.INPUT_DIVIDER
        ]
        return self.NEST_DIVIDER.join(return_list)

    def output_nest_id(self, block: Block, nest_id: str):
        return_list = [
            block.operation.operation_id,
            self.KEY_VALUE_BLOCK_DIVIDER.join(
                sorted([key + self.KEY_VALUE_DIVIDER + value for key, value in block.options])
            ),
            nest_id + self.OUTPUT_DIVIDER
        ]
        return self.NEST_DIVIDER.join(return_list)

    def is_input_nest(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        return self.INPUT_DIVIDER in str(node.Label)

    def is_output_nest(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        return self.OUTPUT_DIVIDER in str(node.Label)

    def is_block(self, node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode):
        return not self.is_input_nest(node) and not self.is_output_nest(
            node) and not node == GraphWithRepetitiveNodesWithRoot.ROOT

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
                block_blank.add((operation_id, tuple(key_values.items()), node.Number))

            elif self.is_output_nest(node):
                operation_id, key_values, nest = self.get_output_nest(node)
                outputs[operation_id, tuple(key_values.items()), node.Number].add(nest)
                block_blank.add((operation_id, tuple(key_values.items()), node.Number))

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

    def convert_graph_map(self, graph_map: GraphMap) -> (Workflow, GraphDotColorer):
        graph_map.eval_difference_complete()

        workflow = Workflow()

        from collections import defaultdict
        inputs = defaultdict(set)
        outputs = defaultdict(set)
        nest_to_center = {}

        for from_node, to_node in graph_map.get_edge_overlap_from_second() + graph_map.get_edges_in_2_not_in_1():
            if self.is_input_nest(from_node) and self.is_block(to_node):
                from_operation_id, from_key_values, from_nest = self.get_input_nest(from_node)
                to_operation_id, to_key_values = self.get_block_id(to_node)

                assert to_operation_id == from_operation_id
                assert to_key_values == from_key_values

                inputs[to_node, 2].add(from_nest)
                nest_to_center[from_node, 2] = to_node, 2

            elif self.is_block(from_node) and self.is_output_nest(to_node):
                from_operation_id, from_key_values = self.get_block_id(from_node)
                to_operation_id, to_key_values, to_nest = self.get_output_nest(to_node)

                assert to_operation_id == from_operation_id
                assert to_key_values == from_key_values

                outputs[from_node, 2].add(to_nest)
                nest_to_center[to_node, 2] = from_node, 2

        for from_node, to_node in graph_map.get_edges_in_1_not_in_2() + graph_map.get_edge_overlap_from_first():
            if self.is_input_nest(from_node) and self.is_block(to_node):
                from_operation_id, from_key_values, from_nest = self.get_input_nest(from_node)
                to_operation_id, to_key_values = self.get_block_id(to_node)

                assert to_operation_id == from_operation_id
                assert to_key_values == from_key_values

                inputs[to_node, 1].add(from_nest)
                nest_to_center[from_node, 1] = to_node, 1

            elif self.is_block(from_node) and self.is_output_nest(to_node):
                from_operation_id, from_key_values = self.get_block_id(from_node)
                to_operation_id, to_key_values, to_nest = self.get_output_nest(to_node)

                assert to_operation_id == from_operation_id
                assert to_key_values == from_key_values

                outputs[from_node, 1].add(to_nest)
                nest_to_center[to_node, 1] = from_node, 1

        block_colors = {}
        blocks = {}

        for node in graph_map.get_node_overlap_from_second():
            if not self.is_block(node):
                continue
            operation_id, key_values = self.get_block_id(node)
            key_values_tuple = tuple(key_values.items())
            block = Block(Operation(operation_id=operation_id,
                                    inputs=sorted(inputs[node, 2]),
                                    outputs=sorted(outputs[node, 2])),
                          options=key_values_tuple)
            blocks[node, 2] = block, workflow.add_block(block)
            block_colors[blocks[node, 2]] = 'black'

        for node in graph_map.get_nodes_in_2_not_in_1():
            if not self.is_block(node):
                continue
            operation_id, key_values = self.get_block_id(node)
            key_values_tuple = tuple(key_values.items())
            block = Block(Operation(operation_id=operation_id,
                                    inputs=sorted(inputs[node, 2]),
                                    outputs=sorted(outputs[node, 2])),
                          options=key_values_tuple)
            blocks[node, 2] = block, workflow.add_block(block)
            block_colors[blocks[node, 2]] = 'green'

        for node in graph_map.get_nodes_in_1_not_in_2():
            if not self.is_block(node):
                continue
            operation_id, key_values = self.get_block_id(node)
            key_values_tuple = tuple(key_values.items())
            block = Block(Operation(operation_id=operation_id,
                                    inputs=sorted(inputs[node, 1]),
                                    outputs=sorted(outputs[node, 1])),
                          options=key_values_tuple)
            blocks[node, 1] = block, workflow.add_block(block)
            block_colors[blocks[node, 1]] = 'red'

        for node in graph_map.get_node_overlap_from_first():
            if not self.is_block(node):
                continue
            map_node = graph_map.map_from_1(node)
            blocks[node, 1] = blocks[map_node, 2]
            block_colors[blocks[node, 1]] = 'black'

        data_connection_colors = {}
        exc_connection_colors = {}

        for from_node, to_node in graph_map.get_edge_overlap_from_second() + graph_map.get_edges_in_2_not_in_1():
            if self.is_output_nest(from_node) and self.is_input_nest(to_node):
                _, _, from_nest = self.get_output_nest(from_node)
                _, _, to_nest = self.get_input_nest(to_node)
                from_nest_block, from_nest_block_number = blocks[nest_to_center[from_node, 2]]
                to_nest_block, to_nest_block_number = blocks[nest_to_center[to_node, 2]]
                workflow.add_connection_by_data(
                    from_block=from_nest_block,
                    from_number=from_nest_block_number,
                    output_nest=from_nest,
                    to_block=to_nest_block,
                    to_number=to_nest_block_number,
                    input_nest=to_nest
                )
                data_connection_colors[
                    from_nest_block,
                    from_nest_block_number,
                    from_nest,
                    to_nest_block,
                    to_nest_block_number,
                    to_nest
                ] = 'black' if from_node in graph_map.get_node_overlap_from_second() and \
                               to_node in graph_map.get_node_overlap_from_second() else 'green'
            elif self.is_block(from_node) and self.is_block(to_node):
                from_block, from_number = blocks[from_node, 2]
                to_block, to_number = blocks[to_node, 2]
                workflow.add_connection_by_execution(
                    from_block=from_block,
                    from_number=from_number,
                    to_block=to_block,
                    to_number=to_number
                )
                exc_connection_colors[
                    from_block,
                    from_number,
                    to_block,
                    to_number
                ] = 'black' if from_node in graph_map.get_node_overlap_from_second() and \
                               to_node in graph_map.get_node_overlap_from_second() else 'green'

        for from_node, to_node in graph_map.get_edges_in_1_not_in_2():
            if self.is_output_nest(from_node) and self.is_input_nest(to_node):
                _, _, from_nest = self.get_output_nest(from_node)
                _, _, to_nest = self.get_input_nest(to_node)
                from_nest_block, from_nest_block_number = blocks[nest_to_center[from_node, 1]]
                to_nest_block, to_nest_block_number = blocks[nest_to_center[to_node, 1]]
                workflow.add_connection_by_data(
                    from_block=from_nest_block,
                    from_number=from_nest_block_number,
                    output_nest=from_nest,
                    to_block=to_nest_block,
                    to_number=to_nest_block_number,
                    input_nest=to_nest
                )
                data_connection_colors[
                    from_nest_block,
                    from_nest_block_number,
                    from_nest,
                    to_nest_block,
                    to_nest_block_number,
                    to_nest
                ] = 'red'
            elif self.is_block(from_node) and self.is_block(to_node):
                from_block, from_number = blocks[from_node, 1]
                to_block, to_number = blocks[to_node, 1]
                workflow.add_connection_by_execution(
                    from_block=from_block,
                    from_number=from_number,
                    to_block=to_block,
                    to_number=to_number
                )
                exc_connection_colors[
                    from_block,
                    from_number,
                    to_block,
                    to_number
                ] = 'red'

        return workflow, GraphMapDotColorer(block_colors, data_connection_colors, exc_connection_colors)
