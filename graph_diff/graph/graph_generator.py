from .graph_with_repetitive_nodes_with_root import GraphWithRepetitiveNodesWithRoot
from .graph_with_repetitive_nodes_with_root import RNR_graph
from .graph_with_repetitive_nodes_with_root import lr_node


class GraphGenerator:
    def __init__(self, min_node_num = 2,
                 max_node_num = 30,
                 node_number_expectation = None):
        self.min_node_num = min_node_num
        self.max_node_num = max_node_num
        if node_number_expectation is None:
            self.node_number_expectation = max_node_num * 0.3
        else:
            self.node_number_expectation = node_number_expectation

    def generate_graph(self):
        graph = RNR_graph()

        import numpy.random as nrandom
        import math

        node_number = nrandom.geometric(1 / self.node_number_expectation) + 1
        node_number = max(self.min_node_num, node_number)
        node_number = min(self.max_node_num, node_number)

        a_label_number = 1
        mode_label_number = math.ceil((node_number - 1) / 5)
        b_label_number = node_number

        label_number = int(math.ceil(nrandom.triangular(a_label_number, mode_label_number, b_label_number)))

        node_labels = nrandom.multinomial(node_number - label_number, [1/label_number] * label_number)
        node_labels = [ls + 1 for ls in node_labels]

        for label, label_size in enumerate(node_labels):
            label += 1 # labels start from 1
            for i in range(1, label_size + 1): # numbers start from 1
                new_node = lr_node(label, i)
                graph.add_node(new_node)
                for node in graph:
                    if 1 == nrandom.randint(2) and node not in [new_node, GraphWithRepetitiveNodesWithRoot._ROOT]:
                        graph.add_edge_exp(node, new_node)

        return graph
