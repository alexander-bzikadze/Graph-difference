from collections import defaultdict

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot, lr_node


class AntGraph:
    def __init__(self, graph: GraphWithRepetitiveNodesWithRoot):
        self.graph = graph
        self.nodes = [lr_node(0, 0)] + sorted([node for node in self.graph])
        self.node_indices = {node: i for i, node in enumerate(self.nodes)}
        self.edges = {(self.node_indices[v], self.node_indices[u])
                      for v in self.graph
                      for u in self.graph.get_list_of_adjacent_nodes(v)}
        self.len = len(self.nodes)
        self._label = defaultdict(list)
        for i in self.node_indices.values():
            self._label[self.nodes[i].Label].append(i)
        self.label_indices = {label: i for i, label in enumerate(self._label)}
        self._incoming = [None] * self.len
        for i in self.node_indices.values():
            self._incoming[i] = [v for (v, u) in self.edges if u == i]
        self._outcoming = [None] * self.len
        for i in self.node_indices.values():
            self._outcoming[i] = [u for (v, u) in self.edges if v == i]
        self.iterator = None

    def get_label(self, v: int):
        return self.nodes[v].Label

    def set_iterator(self, matched: dict):
        self.iterator = [
                            i for i, node in enumerate(self.nodes) if node not in matched.keys()
                        ][1:]  # we exclude zero index

    def __iter__(self):
        return iter(self.iterator)

    def labels(self):
        return self._label.keys()

    def label_size(self, label: int):
        return len(self._label[label])

    def label(self, label: int):
        return self._label[label]

    def incoming(self, v: int):
        return self._incoming[v]

    def outcoming(self, v: int):
        return self._outcoming[v]
