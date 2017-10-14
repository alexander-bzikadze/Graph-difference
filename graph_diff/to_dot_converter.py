from .graph import GraphWithRepetitiveNodesWithRoot
import pydot


class RNRGraphToDotConverter:
    @staticmethod
    def __node_to_str_converter(node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode) -> str:
        return str(node.Label) + '_' + str(node.Number)

    def convert_graph(self, graph: GraphWithRepetitiveNodesWithRoot) -> pydot.Dot:
        dot = pydot.Dot(graph_type='digraph')

        node_to_dot = {node: pydot.Node(self.__node_to_str_converter(node), label=str(node.Label), shape='circle') for node in graph}

        for _, dot_node in node_to_dot.items():
            dot.add_node(dot_node)

        for from_node in graph:
            for to_node in graph.get_list_of_adjacent_nodes(from_node):
                dot.add_edge(pydot.Edge(
                    node_to_dot[from_node],
                    node_to_dot[to_node]
                ))
        return dot

def write_graph(graph: GraphWithRepetitiveNodesWithRoot, path):
    write_graph.converter = RNRGraphToDotConverter()
    write_graph.converter.convert_graph(graph).write(path, format="png")
