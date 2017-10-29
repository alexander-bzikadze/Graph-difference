import pydot
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.workflow import Workflow


class WorkflowToDotConverter:
    def __init__(self, separator=""):
        self._separator = separator
        self.by_exc = "by_exc"

    def __block_id_generator(self, block: Block, addition="") -> str:
        return block.operation.operation_id + addition + self._separator

    @staticmethod
    def __block_body_printer(block: Block) -> str:
        outputs = block.operation.outputs
        outputs = zip(outputs, outputs)
        outputs = "<by_exc>by execution|" + "|".join(["<o" + a + "> " + b for a, b in outputs])
        inputs = block.operation.inputs
        inputs = zip(inputs, inputs)
        inputs = "|".join(["<i" + a + "> " + b for a, b in inputs])

        return '{ {' + inputs + '} | ' + block.operation.operation_id + ' | {' + outputs + '}}'

    def __edge_node_conversion(self, block: Block, num: int, nest: str, where: str = ""):
        return block.operation.operation_id + str(num) + self._separator + ":" + where + nest

    def convert_workflow(self, workflow: Workflow) -> pydot.Dot:
        dot = pydot.Dot(graph_type='digraph')

        from collections import defaultdict
        number_of_blocks = defaultdict(int)
        for block in workflow:
            number_of_blocks[block] += 1
            node = pydot.Node(self.__block_id_generator(block, addition=str(number_of_blocks[block])),
                              label=self.__block_body_printer(block),
                              shape='record')
            dot.add_node(node)

        for (from_block, from_num, output_nest), a2 in workflow.items():
            for to_block, to_num, input_nest in a2:
                edge = pydot.Edge(src=self.__edge_node_conversion(from_block, from_num, output_nest, 'o'),
                                  dst=self.__edge_node_conversion(to_block, to_num, input_nest, 'i'))
                dot.add_edge(edge)

        for (from_block, from_num), a2 in workflow.items_by_exc():
            for to_block, to_num in a2:
                edge = pydot.Edge(src=self.__edge_node_conversion(from_block, from_num, self.by_exc),
                                  dst=self.__edge_node_conversion(to_block, to_num, self.by_exc))
                dot.add_edge(edge)

        return dot
