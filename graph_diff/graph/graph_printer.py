from graph_diff.graph import GraphWithRepetitiveNodesWithRoot


class GraphPrinter:
    def __init__(self, graph: GraphWithRepetitiveNodesWithRoot):
        self.graph = graph
        self.nodes = list(graph)
        self.node_to_index = {node: str(i) for i, node in enumerate(graph)}

    def print_graph(self) -> [str]:
        out = [str(len(self.graph))]
        for node in self.graph:
            out.append('{} {}'.format(node.Label, node.Number))
        for node in self.graph:
            out.append(str(len(self.graph.get_list_of_adjacent_nodes(node))))
            for to_node in self.graph.get_list_of_adjacent_nodes(node):
                out.append(self.node_to_index[to_node])
        return out
