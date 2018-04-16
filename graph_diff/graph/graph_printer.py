from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphMap


class GraphPrinter:
    def __init__(self,
                 graph1: GraphWithRepetitiveNodesWithRoot,
                 graph2: GraphWithRepetitiveNodesWithRoot):
        self.graph1 = graph1
        self.nodes1 = list(graph1)
        self.node1_to_index = {node: i for i, node in enumerate(self.nodes1)}

        self.graph2 = graph2
        self.nodes2 = list(graph2)
        self.node2_to_index = {node: i for i, node in enumerate(self.nodes2)}

        self.labels = {node.Label for node in graph1} | {node.Label for node in graph2}
        self.label_to_index = {label: i for i, label in enumerate(self.labels)}

    def __graph_transformer(self,
                            graph: GraphWithRepetitiveNodesWithRoot,
                            nodes: [GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode],
                            nodes_to_index: {GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode: int}) \
            -> ([(int, int)], [[int]]):
        out_nodes = [(self.label_to_index[node.Label], node.Number)
                     for node in nodes]
        out_edges = [[nodes_to_index[to_node]
                      for to_node
                      in graph.get_list_of_adjacent_nodes(node)]
                     for node in nodes]

        return out_nodes, out_edges

    def graph_transformer_first(self):
        return self.__graph_transformer(self.graph1,
                                        self.nodes1,
                                        self.node1_to_index)

    def graph_transformer_second(self):
        return self.__graph_transformer(self.graph2,
                                        self.nodes2,
                                        self.node2_to_index)

    def print_graph1(self) -> [str]:
        return self.__print_graph(self.graph1, self.node1_to_index)

    def print_graph2(self) -> [str]:
        return self.__print_graph(self.graph2, self.node2_to_index)

    def __print_graph(self,
                      graph: GraphWithRepetitiveNodesWithRoot,
                      node_to_index: dict) -> [str]:
        out = [str(len(graph))]
        for node in graph:
            out.append('{} {}'.format(self.label_to_index[node.Label], node.Number))
        for node in graph:
            out.append(str(len(graph.get_list_of_adjacent_nodes(node))))
            for to_node in graph.get_list_of_adjacent_nodes(node):
                out.append(str(node_to_index[to_node]))
        return out

    def back_printer(self, output: str) -> GraphMap:
        output = [tuple(x.split()) for x in output.split('\n')]
        output = filter(lambda x: len(x) == 2, output)
        output = {int(a): int(b) for a, b in output}

        if len(self.graph1) > len(self.graph2):
            output = {self.nodes1[b]: self.nodes2[a]
                      for a, b in enumerate(output) if b != -1}
        else:
            output = {self.nodes1[a]: self.nodes2[b]
                      for a, b in enumerate(output) if b != -1}

        return GraphMap.construct_graph_map(output, self.graph1, self.graph2)

    def back_transformer(self, output: [tuple]) -> GraphMap:
        if len(self.graph1) > len(self.graph2):
            output = {self.nodes1[b]: self.nodes2[a]
                      for a, b in enumerate(output) if b != -1}
        else:
            output = {self.nodes1[a]: self.nodes2[b]
                      for a, b in enumerate(output) if b != -1}

        return GraphMap.construct_graph_map(output, self.graph1, self.graph2)
