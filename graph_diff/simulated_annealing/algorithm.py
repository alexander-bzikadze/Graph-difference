from collections import defaultdict

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_map import GraphMap


class Algorithm(GraphDiffAlgorithm):
    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        labels = defaultdict(set)
        for node in graph1:
            labels[node.Label].add(node)

        node_indices = {node: i for i, node in enumerate(graph1)}
