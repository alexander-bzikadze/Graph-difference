from .graph import GraphWithRepetitiveNodesWithRoot
from .graph_map import GraphMap
import pydot


class RNRGraphToDotConverter:
    @staticmethod
    def __node_to_str_converter(node: GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode, addition="") -> str:
        return '_'.join([str(node.Label), str(node.Number), addition])

    def convert_graph(self, graph: GraphWithRepetitiveNodesWithRoot) -> pydot.Dot:
        dot = pydot.Dot(graph_type='digraph')

        node_to_dot = {node: pydot.Node(self.__node_to_str_converter(node), label=str(node.Label), shape='circle') for node in graph}

        for _, dot_node in node_to_dot.items():
            dot.add_node(dot_node)

        # As graphs have root, every node has at least one incoming edge.
        for from_node in graph:
            for to_node in graph.get_list_of_adjacent_nodes(from_node):
                dot.add_edge(pydot.Edge(
                    node_to_dot[from_node],
                    node_to_dot[to_node]
                ))
        return dot

    def convert_graph_map(self, graph_map: GraphMap) -> pydot.Dot:
        graph_map.eval_difference_complete()

        dot = pydot.Dot(graph_type='digraph')

        node_to_dot = {}
        for node in graph_map.get_node_overlap_from_first():
            node_to_dot[node] = pydot.Node(self.__node_to_str_converter(node, '1'), label=str(node.Label), shape='circle')
        for node in graph_map.get_nodes_in_1_not_in_2():
            node_to_dot[node] = pydot.Node(self.__node_to_str_converter(node, '1'), color='red', label=str(node.Label), shape='circle')
        for node in graph_map.get_nodes_in_2_not_in_1():
            node_to_dot[node] = pydot.Node(self.__node_to_str_converter(node, '2'), color='green', label=str(node.Label), shape='circle')

        for _, dot_node in node_to_dot.items():
            dot.add_node(dot_node)

        for (from_node, to_node) in graph_map.get_edge_overlap_from_first():
            dot.add_edge(pydot.Edge(node_to_dot[from_node], node_to_dot[to_node]))
        for (from_node, to_node) in graph_map.get_edges_in_1_not_in_2():
            dot.add_edge(pydot.Edge(node_to_dot[from_node], node_to_dot[to_node], color='red'))
        for (from_node, to_node) in graph_map.get_edges_in_2_not_in_1():
            dot.add_edge(pydot.Edge(node_to_dot[from_node], node_to_dot[to_node], color='green'))

        return dot

def write_graph(graph: GraphWithRepetitiveNodesWithRoot, path):
    write_graph.converter = RNRGraphToDotConverter()
    write_graph.converter.convert_graph(graph).write(path, format="png")

def write_diff(graph_map: GraphMap, path):
    write_graph.converter = RNRGraphToDotConverter()
    write_graph.converter.convert_graph_map(graph_map).write(path, format="png")
    write_graph.converter.convert_graph_map(graph_map).write(path.split(".png")[0] + ".dot")

