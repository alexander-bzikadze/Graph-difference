from collections import defaultdict
from .BaseGraph import BaseGraph


class GraphWithRepetitiveNodes(BaseGraph):
    _adjacency_list = defaultdict(set)
    _ROOT = (0, 0)

    def __init__(self):
        self._adjacency_list[(0, 0)] = set()

    def add_edge_explicit(self, from_node: (int, int),
                          to_node: (int, int)):
        self.check_node_for_existence(from_node)
        self._adjacency_list[from_node].add(to_node)
        return self

    def add_edge(self, from_node: (int, int),
                 to_node: (int, int)):
        self._adjacency_list[from_node].add(to_node)
        return self

    def add_node(self, new_node: (int, int)):
        if new_node not in self._adjacency_list:
            self._adjacency_list[new_node] = set()
        return self

    def get_list_of_adjacent_nodes(self, node: (int, int)) -> [(int, int)]:
        self.check_node_for_existence(node)
        return self._adjacency_list[node]

    def get_list_of_nodes(self) -> [(int, int)]:
        return self._adjacency_list.keys()

    def get_list_of_edges(self) -> [((int, int), (int, int))]:
        return [(from_node, to_node)
                    for from_node, to_node_list in self._adjacency_list.items()
                    for to_node in to_node_list]

    def check_node_for_existence(self, node: (int, int)):
        if node not in self._adjacency_list:
            from graph_diff.graph.GraphWithRepetitiveNodesExceptions \
                import GraphWithRepetitiveNodesKeyError
            raise GraphWithRepetitiveNodesKeyError(
                "{0} not contained as a node.".format(str(node)))

    @staticmethod
    def get_from_dict(adjacency_list: {(int, int): [(int, int)]}):
        res = GraphWithRepetitiveNodes()
        res._adjacency_list += adjacency_list
        return res
