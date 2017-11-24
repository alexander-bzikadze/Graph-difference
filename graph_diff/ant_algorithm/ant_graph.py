from collections import defaultdict

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot, lr_node


class AntGraph:
    def __init__(self, graph: GraphWithRepetitiveNodesWithRoot):
        self.len = len(list(graph)) + 1
        self.nodes = [lr_node(1, 0)] + sorted(list(graph), key=lambda x: (x.Label, x.Number))
        self.edges = {(self.nodes.index(v), self.nodes.index(u)) for v in graph for u in
                      graph.get_list_of_adjacent_nodes(v)}
        self._label = defaultdict(list)
        for i in self:
            self._label[self.nodes[i].Label].append(i)
        self._incoming = [None] * self.len
        for i in self:
            self._incoming[i] = [v for (v, u) in self.edges if u == i]
        self._outcoming = [None] * self.len
        for i in self:
            self._outcoming[i] = [u for (v, u) in self.edges if v == i]

    def get_label(self, v: int):
        return self.nodes[v].Label

    def __iter__(self):
        # Return indices of nodes excluding 0
        return iter(range(1, len(self.nodes)))

    def label_size(self, label: int):
        return len(self._label[label])

    def label(self, label: int):
        return self._label[label]

    def incoming(self, v: int):
        return self._incoming[v]

    def outcoming(self, v: int):
        return self._outcoming[v]
