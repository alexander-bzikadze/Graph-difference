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


        # node_number = random.randint(self.min_node_num, self.max_node_num)
        #
        # generated_nodes = 1
        # len_in_labels = []
        # while generated_nodes < node_number:
        #     generate_label = random.randint(1, node_number - generated_nodes + 1)
        #     len_in_labels.append(generate_label)
        #     for i in range(1, generate_label + 1):
        #         graph.add_node(lr_node(len(len_in_labels), i))
        #     generated_nodes += generate_label
        # graph_density = random.random()
        # added_edges = 0
        # import math
        # print(len_in_labels)
        # print(generated_nodes, node_number)
        # for _ in range(0, int(math.floor(graph_density * node_number ** 2))):
        #     label1 = random.randint(1, len(len_in_labels) - 1)
        #     label2 = random.randint(label1 + 1, len(len_in_labels))
        #     number1 = random.randint(1, len_in_labels[label1 - 1] + 1)
        #     number2 = random.randint(1, len_in_labels[label2 - 1] + 1)
        #     graph.add_edge(lr_node(label1, number1), lr_node(label2, number2))
        # return graph

        return graph
