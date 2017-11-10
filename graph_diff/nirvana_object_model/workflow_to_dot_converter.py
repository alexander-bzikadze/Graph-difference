import pydot
from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.workflow import Workflow


class WorkflowToDotConverter:
    def __init__(self, separator=""):
        self._separator = separator
        self.BY_EXC = "by_exc"

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

    def convert_workflow(self, workflow: Workflow, colors=None) -> pydot.Dot:
        dot = pydot.Dot(graph_type='digraph')

        if colors is None:
            block_colors = lambda block, number: 'black'
            data_colors = lambda from_block, from_number, output_nest, to_block, to_number, input_nest: 'black'
            exc_colors = lambda from_block, from_number, to_block, to_number: 'black'
        else:
            block_colors, data_colors, exc_colors = colors

        from collections import defaultdict
        number_of_blocks = defaultdict(int)
        for block in workflow:
            number_of_blocks[block] += 1
            node = pydot.Node(self.__block_id_generator(block, addition=str(number_of_blocks[block])),
                              label=self.__block_body_printer(block),
                              shape='record',
                              color=block_colors(block, number_of_blocks[block]))
            dot.add_node(node)

        for (from_block, from_num, output_nest), a2 in workflow.items():
            for to_block, to_num, input_nest in a2:
                edge = pydot.Edge(src=self.__edge_node_conversion(from_block, from_num, output_nest, 'o'),
                                  dst=self.__edge_node_conversion(to_block, to_num, input_nest, 'i'),
                                  color=data_colors(from_block, from_num, output_nest, to_block, to_num, input_nest))
                dot.add_edge(edge)

        for (from_block, from_num), a2 in workflow.items_by_exc():
            for to_block, to_num in a2:
                edge = pydot.Edge(src=self.__edge_node_conversion(from_block, from_num, self.BY_EXC),
                                  dst=self.__edge_node_conversion(to_block, to_num, self.BY_EXC),
                                  color=exc_colors(from_block, from_num, to_block, to_num))
                dot.add_edge(edge)

        return dot


def print_together(*args) -> pydot.Dot:
    def dot_to_subgraph(graph: pydot.Dot, label: str) -> pydot.Cluster:
        graph_s = pydot.Cluster(label, label=label)
        for node in graph.get_nodes():
            graph_s.add_node(node)
        for edge in graph.get_edges():
            graph_s.add_edge(edge)
        return graph_s
    res = pydot.Dot()
    for i, workflow in enumerate(args):
        res.add_subgraph(dot_to_subgraph(workflow, "workflow" + str(i)))
    return res
