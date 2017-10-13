from graph_diff.graph import lr_node
from .graph import GraphWithRepetitiveNodesWithRoot
from abc import ABC, abstractmethod

class GraphMap:
    def __init__(self, graph_map_1_to_2, graph1: GraphWithRepetitiveNodesWithRoot, graph2: GraphWithRepetitiveNodesWithRoot):
        # graph_map_1_to_2 needs to have iter
        self._graph_map_1_to_2 = dict(graph_map_1_to_2)
        self._graph_map_2_to_1 = {}
        for node_from_1, node_from_2 in self._graph_map_1_to_2.items():
            self._graph_map_2_to_1[node_from_2] = node_from_1

        for node_from_1 in graph1:
            if node_from_1 not in self._graph_map_1_to_2.keys():
                self._graph_map_1_to_2[node_from_1] = lr_node(node_from_1.Label, 0)
        for node_from_2 in graph2:
            if node_from_2 not in self._graph_map_2_to_1.keys():
                self._graph_map_2_to_1[node_from_2] = lr_node(node_from_2.Label, 0)
        self._graph1 = graph1
        self._graph2 = graph2
        self.eval_difference()

    def map_from_1(self, node):
        return self._graph_map_1_to_2[node]

    def map_from_2(self, node):
        return self._graph_map_2_to_1[node]

    def eval_difference(self):
        def nodes_diff(graph1, graph2):
            return [node_1 for node_1 in self._graph1 if self.map_from_1(node_1).Number == 0 ]
        def edges_diff(graph1, graph2):
            return [
                (from_node_1, to_node_1)
                for from_node_1 in self._graph1
                for to_node_1 in self._graph1
                if self.map_from_1(to_node_1) not in self._graph1.get_list_of_adjacent_nodes(self.map_from_1(from_node_1))
            ]
        self._node_in_1_but_not_in_2 = nodes_diff(self._graph1, self._graph2)
        self._num_node_in_1_but_not_in_2 = len(self._node_in_1_but_not_in_2)
        self._edge_in_1_but_not_in_2 = edges_diff(self._graph1, self._graph2)
        self._num_edge_in_1_but_not_in_2 = len(self._edge_in_1_but_not_in_2)
        self._node_in_2_but_not_in_1 = nodes_diff(self._graph2, self._graph1)
        self._num_node_in_2_but_not_in_1 = len(self._node_in_2_but_not_in_1)
        self._edge_in_2_but_not_in_1 = edges_diff(self._graph2, self._graph1)
        self._num_edge_in_2_but_not_in_1 = len(self._edge_in_2_but_not_in_1)

    def get_num_node_in_1_but_not_in_2(self):
        return self._num_node_in_1_but_not_in_2

    def get_num_edge_in_1_but_not_in_2(self):
        return self._num_edge_in_1_but_not_in_2

    def get_num_node_in_2_but_not_in_1(self):
        return self._num_node_in_2_but_not_in_1

    def get_num_edge_in_2_but_not_in_1(self):
        return self._num_edge_in_2_but_not_in_1


def GraphMapComparator(ABC):
    @abstractmethod
    def compare(self, graph_map: GraphMap, other_graph_map: GraphMap): pass


class GraphMapComparatorByEdgeNumAndThenNodeNum:
    def compare(self, graph_map: GraphMap, other_graph_map: GraphMap):
        return (graph_map.get_num_node_in_1_but_not_in_2() + graph_map.get_num_node_in_2_but_not_in_1(),
                graph_map.get_num_edge_in_1_but_not_in_2() +  graph_map.get_num_edge_in_2_but_not_in_1()
                ) < (
            other_graph_map.get_num_node_in_1_but_not_in_2() + other_graph_map.get_num_node_in_2_but_not_in_1(),
            other_graph_map.get_num_edge_in_1_but_not_in_2() + other_graph_map.get_num_edge_in_2_but_not_in_1())

class GraphMapComparatorByEdgeNumAndNodeNumSum:
    def compare(self, graph_map: GraphMap, other_graph_map: GraphMap):
        return (graph_map.get_num_node_in_1_but_not_in_2() + graph_map.get_num_node_in_2_but_not_in_1() +
                graph_map.get_num_edge_in_1_but_not_in_2() +  graph_map.get_num_edge_in_2_but_not_in_1()
                ) < (
            other_graph_map.get_num_node_in_1_but_not_in_2() + other_graph_map.get_num_node_in_2_but_not_in_1() +
            other_graph_map.get_num_edge_in_1_but_not_in_() + other_graph_map.get_num_edge_in_2_but_not_in_1())

