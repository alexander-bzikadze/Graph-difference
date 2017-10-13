from .graph import GraphWithRepetitiveNodesWithRoot
from .graph import lr_node
from .graph_diff_algorithm import GraphDiffAlgorithm


class BaselineAlgorithm(GraphDiffAlgorithm):
    class BLPermutationsForLabel:
        def __init__(self, label: int, graph):
            self._label = label
            self._length_of_another_graph = len(graph.get(label))

        def list_map_permutations(self, list_to_perm, current):
            if self._length_of_another_graph <= current:
                return [[]]
            res = []
            list_copy = list_to_perm.copy()
            for i in range(0, len(list_to_perm)):
                list_copy[0], list_copy[i] = list_copy[i], list_copy[0]
                res += [[list_copy[0]] + perm for perm in self.list_map_permutations(list_copy[1:], current + 1)]
            res += [[lr_node(self._label, 0)] + perm for perm in self.list_map_permutations(list_copy[1:], current + 1)]
            return res

    class RNRGraphForBLAlg:
        def __init__(self, graph: GraphWithRepetitiveNodesWithRoot):
            from collections import defaultdict
            self._label_to_node_map = defaultdict(list)
            self._nodes_in_graph = list(graph)
            for node in graph:
                self._label_to_node_map[node.Label].append(node)

        def get(self, label: int):
            return self._label_to_node_map[label]

        def __iter__(self):
            return iter([label for label, node_list in self._label_to_node_map.items() if bool(node_list)])

        def __len__(self):
            return len(self._label_to_node_map.keys())

        def keys(self):
            return self._nodes_in_graph

        def items(self):
            return self._label_to_node_map.items()

        def extend_graph(self, graph):
            for label in graph:
                if label not in self:
                    self._label_to_node_map[label] = []
            return self

        def add_zero_nodes(self, graph):
            for label, list_of_nodes in self._label_to_node_map.items():
                list_of_nodes += [lr_node(label, 0)] * len([node for node in graph.get(label) if bool(node.Number)])
            return self

    class BLAGraphMap:
        def __init__(self, graph_map, graph1, graph2):
            self._graph_map = graph_map
            self._graph1 = graph1
            self._graph2 = graph2

            def eval_score(graph_map_to_get_score):
                node_metric = 0
                edge_metric = 0
                for node in graph_map_to_get_score._graph1:
                    # If 0 in num of one of the nodes, it means that there is no match for another.
                    if node.Number == 0 \
                            or node not in graph_map_to_get_score._graph_map \
                            or graph_map_to_get_score.match(node).Number == 0:
                        continue
                    node_metric += 1
                    edge_metric += sum(
                        [int(to_node.Number != 0
                             and node.Number != 0
                             and node in graph_map_to_get_score._graph1
                             and node in graph_map_to_get_score._graph_map
                             and to_node in graph_map_to_get_score._graph_map and
                             graph_map_to_get_score.match(to_node) in graph_map_to_get_score._graph2.get_list_of_adjacent_nodes(
                                 graph_map_to_get_score.match(node)))
                         for to_node in graph_map_to_get_score._graph1.get_list_of_adjacent_nodes(node)]
                    )
                return edge_metric, node_metric

            self._score = eval_score(self)

        def __repr__(self):
            return str(self._graph_map) + str(self._score)

        def match(self, node):
            return self._graph_map[node]

        def get_score(self):
            return self._score

        def __lt__(self, other):
            return self._score < other._score

    def construct_diff(self, graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot):
        graph1_internal = BaselineAlgorithm.RNRGraphForBLAlg(graph1)
        graph2_internal = BaselineAlgorithm.RNRGraphForBLAlg(graph2)
        graph1_internal.extend_graph(graph2_internal)
        graph1_internal.extend_graph(graph1_internal)

        # graph1_internal.add_zero_nodes(graph2_internal)
        # graph2_internal.add_zero_nodes(graph1_internal)

        def produce_all_possible_maps(graph_maps_for_each_label):
            from functools import reduce
            from itertools import product
            graph_maps_for_each_label = [graph_map for _, graph_map in graph_maps_for_each_label.items()]
            return reduce(product, graph_maps_for_each_label)

        def sum_tuples(pair):
            if type(pair) == tuple:
                pair, dictionary = pair
                return list(dictionary.items()) + list(sum_tuples(pair))
            elif type(pair) == dict:
                return pair.items()
            raise Exception("")

        graph_maps = self.graph_maps_for_each_label(graph1_internal, graph2_internal)
        graph_maps = produce_all_possible_maps(graph_maps)
        graph_maps = [dict(sum_tuples(pair)) for pair in graph_maps]
        graph_maps = [BaselineAlgorithm.BLAGraphMap(graph_map, graph1, graph2) for graph_map in graph_maps]

        return max(graph_maps)

    def graph_maps_for_each_label(self, graph1, graph2):
        res = {
            label: (
                {node_from_self: node_from_graph for node_from_self, node_from_graph in zip(lr1, lr2)
                if node_from_self.Number != 0 or node_from_graph.Number != 0}
                for lr1, lr2 in
                self.zip_all(l1, BaselineAlgorithm.BLPermutationsForLabel(label, graph2).list_map_permutations(l2, 0))
            ) for (label, l1), (_, l2) in zip(sorted(graph1.items()), sorted(graph2.items()))
        }
        return res

    def zip_all(self, l1, l2_perms):
        return [(l1, l2) for l2 in l2_perms]