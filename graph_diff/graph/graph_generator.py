from .graph_with_repetitive_nodes_with_root import GraphWithRepetitiveNodesWithRoot
from .graph_with_repetitive_nodes_with_root import RNR_graph
from .graph_with_repetitive_nodes_with_root import lr_node


class GraphGenerator:
    def __init__(self, min_node_num, max_node_num):
        self.min_node_num = min_node_num
        self.max_node_num = max_node_num

    def generate_graph(self):
        graph = RNR_graph()
        import random
        node_number = random.randint(self.min_node_num, self.max_node_num)
        generated_nodes = 1
        len_in_labels = []
        while generated_nodes < node_number:
            generate_label = random.randint(generated_nodes, node_number) - generated_nodes
            len_in_labels.append(generate_label)
            for i in range(1, generate_label + 1):
                graph.add_node(lr_node(len(len_in_labels), i))
            generated_nodes += generate_label
        graph_density = random.random()
        added_edges = 0
        import math
        print(len_in_labels)
        print(generated_nodes, node_number)
        for _ in range(0, int(math.floor(graph_density * node_number ** 2))):
            label1 = random.randint(1, len(len_in_labels) - 1)
            label2 = random.randint(label1 + 1, len(len_in_labels))
            number1 = random.randint(1, len_in_labels[label1 - 1] + 1)
            number2 = random.randint(1, len_in_labels[label2 - 1] + 1)
            graph.add_edge(lr_node(label1, number1), lr_node(label2, number2))
        return graph
