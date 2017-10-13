from .graph_with_repetitive_nodes_exceptions import LabeledRepetitiveNodePositiveArgumentException
from .graph_with_repetitive_nodes_exceptions import GraphWithRepetitiveNodesKeyError


class GraphWithRepetitiveNodesWithRoot:
    class LabeledRepetitiveNode:
        def __hash__(self) -> int:
            return (self.Label, self.Number).__hash__()

        def __eq__(self, node) -> bool:
            return self.Label == node.Label and self.Number == node.Number

        def __init__(self, label: int, number: int):
            self.__Label = label
            self.__Number = number

        def __str__(self):
            return "Node: (" + str(self.Label) + ", " + str(self.Number) + ")"

        def __repr__(self):
            return "Node: (" + str(self.Label) + ", " + str(self.Number) + ")"

        def __lt__(self, other):
            return self.Label < other.Label if self.Label != other.Label else self.Number < other.Number

        @property
        def Label(self):
            return self.__Label

        @Label.setter
        def Label(self, label: int):
            if label < 0:
                raise LabeledRepetitiveNodePositiveArgumentException("Label should not be negative!")
            self.__Label = label

        @property
        def Number(self):
            return self.__Number

        @Number.setter
        def Number(self, number: int):
            if number < 0:
                raise LabeledRepetitiveNodePositiveArgumentException("Label should not be negative!")
            self.__Number = number

    _ROOT = LabeledRepetitiveNode(0, 1)

    def __init__(self):
        self._adjacency_list = {self._ROOT: set()}

    def __contains__(self, item):
        return item in self._adjacency_list.keys()

    def __iter__(self):
        return iter(self._adjacency_list.keys())

    def add_node(self, new_node):
        if new_node not in self._adjacency_list.keys():
            self._adjacency_list[self._ROOT].add(new_node)
            self._adjacency_list[new_node] = set()
        return self

    def add_edge(self, from_node, to_node):
        self.add_node(from_node)
        self.add_node(to_node)
        self._adjacency_list[from_node].add(to_node)
        if to_node in self._adjacency_list[self._ROOT]:
            self._adjacency_list[self._ROOT].remove(to_node)
        return self

    # Add edge explicitly.
    # Raise error if nodes are not in the graph.
    def add_edge_exp(self, from_node, to_node):
        if from_node not in self or to_node not in self:
            raise GraphWithRepetitiveNodesKeyError("Adding edge from or to not valid nodes")
        self._adjacency_list[from_node].add(to_node)
        if to_node in self._adjacency_list[self._ROOT]:
            self._adjacency_list[self._ROOT].remove(to_node)
        return self

    def get_list_of_adjacent_nodes(self, node):
        return self._adjacency_list[node] if node in self else []


def lr_node(label: int, number: int):
    return GraphWithRepetitiveNodesWithRoot.LabeledRepetitiveNode(label, number)


def RNR_graph():
    return GraphWithRepetitiveNodesWithRoot()
