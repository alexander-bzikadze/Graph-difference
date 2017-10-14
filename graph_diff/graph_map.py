from abc import ABC, abstractmethod
from graph_diff.graph import lr_node
from .graph import GraphWithRepetitiveNodesWithRoot
from .graph_map_exceptions import *


class GraphMap:
    def __init__(self):
        self._graph1 = None
        self._graph2 = None
        self._graph_map_1_to_2 = None
        self._graph_map_2_to_1 = None

    @staticmethod
    def construct_graph_map(graph_map_1_to_2, graph1: GraphWithRepetitiveNodesWithRoot,
                            graph2: GraphWithRepetitiveNodesWithRoot):
        error_list = []
        for node1, node2 in graph_map_1_to_2.items():
            if node1 not in graph1 and node1.Number != 0:
                error_list.append(str(node1) + " not in first graph!")
            if node2 not in graph2 and node2.Number != 0:
                error_list.append(str(node2) + " not in second graph!")

        if len(error_list) > 0:
            raise GraphDoesNotContainMappedNodeException(" ".join(error_list))

        graph_map = GraphMap()

        # graph_map_1_to_2 needs to have iter
        graph_map._graph_map_1_to_2 = dict(graph_map_1_to_2)
        graph_map._graph_map_2_to_1 = {}
        for node_from_1, node_from_2 in graph_map._graph_map_1_to_2.items():
            graph_map._graph_map_2_to_1[node_from_2] = node_from_1

        graph_map._graph1 = graph1
        graph_map._graph2 = graph2
        graph_map.__eval_difference()

        return graph_map

    def map_from_1(self, node):
        return self._graph_map_1_to_2[node] if node in self._graph_map_1_to_2.keys() else lr_node(node.Label, 0)

    def map_from_2(self, node):
        return self._graph_map_2_to_1[node] if node in self._graph_map_2_to_1.keys() else lr_node(node.Label, 0)

    def __eval_difference(self):
        def nodes_overlap(graph1, graph2):
            return [node_1 for node_1 in graph1 if self.map_from_1(node_1) in graph2]

        def edges_overlap(graph1, graph2):
            return [
                (from_node_1, to_node_1)
                for from_node_1 in graph1
                for to_node_1 in graph1.get_list_of_adjacent_nodes(from_node_1)
                if self.map_from_1(to_node_1) in graph2.get_list_of_adjacent_nodes(self.map_from_1(from_node_1))
            ]
        self._node_overlap = nodes_overlap(self._graph1, self._graph2)
        self._num_node_overlap = len(self._node_overlap)
        self._edge_overlap = edges_overlap(self._graph1, self._graph2)
        self._num_edge_overlap = len(self._edge_overlap)

    def get_num_node_overlap(self):
        return self._num_node_overlap

    def get_num_edge_overlap(self):
        return self._num_edge_overlap


class GraphMapComparator(ABC):
    def compare(self, graph_map: GraphMap, other_graph_map: GraphMap):
        return self.comparable_representation(graph_map) < self.comparable_representation(other_graph_map)

    @abstractmethod
    def comparable_representation(self, graph_map: GraphMap): pass


class GraphMapComparatorByEdgeNumAndThenNodeNum(GraphMapComparator):
    def comparable_representation(self, graph_map: GraphMap):
        return graph_map.get_num_edge_overlap(), graph_map.get_num_node_overlap()


class GraphMapComparatorByEdgeNumAndNodeNumSum(GraphMapComparator):
    def comparable_representation(self, graph_map: GraphMap):
        return graph_map.get_num_node_overlap() + graph_map.get_num_edge_overlap()
