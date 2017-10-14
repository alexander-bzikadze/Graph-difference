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
        self._nodes_in_1_not_in_2 = None
        self._nodes_in_2_not_in_1 = None
        self._edges_in_1_not_in_2 = None
        self._edges_in_2_not_in_1 = None
        self._complete_analysis_done = False

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
        return graph_map.__eval_difference()

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

        def complement_of_nodes(graph: GraphWithRepetitiveNodesWithRoot, nodes):
            return [node for node in graph if node not in nodes]

        self._node_overlap_from_first = nodes_overlap(self._graph1, self._graph2)
        self._num_node_overlap = len(self._node_overlap_from_first)
        self._edge_overlap_from_first = edges_overlap(self._graph1, self._graph2)
        self._num_edge_overlap = len(self._edge_overlap_from_first)

        return self

    def eval_difference_complete(self):
        def complement_of_nodes(graph: GraphWithRepetitiveNodesWithRoot, nodes):
            return [node for node in graph if node not in nodes]

        def complement_of_edges(graph: GraphWithRepetitiveNodesWithRoot, edges):
            return [(from_node, to_node)
                    for from_node in graph
                    for to_node in graph.get_list_of_adjacent_nodes(from_node)
                    if (from_node, to_node) not in edges]
        if self._complete_analysis_done:
            return self

        self._node_overlap_from_second = [self.map_from_1(node) for node in self._node_overlap_from_first]
        self._edge_overlap_from_second = [(self.map_from_1(from_node), self.map_from_1(to_node)) for from_node, to_node in self._edge_overlap_from_first]

        self._nodes_in_1_not_in_2 = complement_of_nodes(self._graph1, self._node_overlap_from_first)
        self._nodes_in_2_not_in_1 = complement_of_nodes(self._graph2, self._node_overlap_from_second)

        self._edges_in_1_not_in_2 = complement_of_edges(self._graph1, self._edge_overlap_from_first)
        self._edges_in_2_not_in_1 = complement_of_edges(self._graph2, self._edge_overlap_from_second)

        self._complete_analysis_done = True
        return self

    def get_node_overlap_from_first(self):
        return self._node_overlap_from_first

    def get_edge_overlap_from_first(self):
        return self._edge_overlap_from_first

    def get_node_overlap_from_second(self):
        return self._node_overlap_from_second

    def get_edge_overlap_from_second(self):
        return self._edge_overlap_from_second

    def get_num_node_overlap(self):
        return self._num_node_overlap

    def get_num_edge_overlap(self):
        return self._num_edge_overlap

    def get_nodes_in_1_not_in_2(self):
        return self._nodes_in_1_not_in_2

    def get_nodes_in_2_not_in_1(self):
        return self._nodes_in_2_not_in_1

    def get_edges_in_1_not_in_2(self):
        return self._edges_in_1_not_in_2

    def get_edges_in_2_not_in_1(self):
        return self._edges_in_2_not_in_1

    def get_first_graph(self):
        return self._graph1

    def get_second_graph(self):
        return self._graph2


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
