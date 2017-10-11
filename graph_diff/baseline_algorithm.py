from .graph import GraphWithRepetitiveNodesWithRoot
from .graph import lr_node
from .graph_diff_algorithm import GraphDiffAlgorithm


class BaselineAlgorithm(GraphDiffAlgorithm):
    class RNRGraphForBLAlg():
        def __init__(self, graph: GraphWithRepetitiveNodesWithRoot):
            from collections import defaultdict
            self._label_to_node_map = defaultdict(list)
            for node in graph:
                self._label_to_node_map[node.Label].append(node)

        def get(self, label: int):
            return self._label_to_node_map[label]

        def __iter__(self):
            return iter([label for label, node_list in self._label_to_node_map.items() if bool(node_list)])

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

        def graph_maps_for_each_label(self, graph):

            def list_map_permutations(l1):
                from itertools import permutations
                return [list(l) for l in permutations(l1)]

            def remove_duplicates_from_iterable(l1):
                res = []
                for elem in l1:
                    if elem not in res:
                        res.append(elem)
                return res
            from itertools import product
            res = {
                label: remove_duplicates_from_iterable(
                {node_from_self: node_from_graph for node_from_self, node_from_graph in zip(lr1, lr2)
                        if node_from_self.Number != 0 or node_from_graph.Number != 0}
                    for lr1, lr2 in product(list_map_permutations(l1), list_map_permutations(l2))
                ) for (label, l1), (_, l2) in zip(sorted(self.items()), sorted(graph.items()))
            }
            return res

    class BLAGraphMap():
        def __init__(self, graph_map, graph1, graph2):
            self._graph_map = graph_map
            self._graph1 = graph1
            self._graph2 = graph2
            def eval_score(graph_map):
                node_metric = 0
                edge_metric = 0
                for node in graph_map._graph1:
                    # If 0 in num of one of the nodes, it means that there is no match for another.
                    if node.Number == 0 or graph_map.match(node).Number == 0:
                        continue
                    node_metric += 1
                    edge_metric += sum(
                        [int(graph_map.match(to_node) in graph_map._graph2.get_list_of_adjacent_nodes(graph_map.match(node)))
                         for to_node in graph_map._graph1.get_list_of_adjacent_nodes(node)]
                    )
                return (edge_metric, node_metric)
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
        graph1_internal.add_zero_nodes(graph2_internal)
        graph2_internal.add_zero_nodes(graph1_internal)

        def produce_all_possible_maps(graph_maps_for_each_label):
            from functools import reduce
            from itertools import product
            graph_maps_for_each_label = [ graph_map for _, graph_map in graph_maps_for_each_label.items() ]
            return reduce(product, graph_maps_for_each_label)

        def sum_tuples(pair):
            if type(pair) == tuple:
                pair, dictionary = pair
                return list(dictionary.items()) + list(sum_tuples(pair))
            elif type(pair) == dict:
                return pair.items()
            raise Exception("")

        graph_maps = graph1_internal.graph_maps_for_each_label(graph2_internal)
        graph_maps = produce_all_possible_maps(graph_maps)
        graph_maps = [dict(sum_tuples(pair)) for pair in graph_maps]
        graph_maps = [ BaselineAlgorithm.BLAGraphMap(graph_map, graph1, graph2) for graph_map in graph_maps ]

        return max(graph_maps)
