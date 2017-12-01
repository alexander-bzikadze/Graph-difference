import itertools
import logging
import time
from collections import defaultdict

from graph_diff.ant_algorithm import parameters
from graph_diff.ant_algorithm.ant_graph import AntGraph
from graph_diff.ant_algorithm.pathfinder import Pathfinder
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.graph_map import GraphMap


def timer():
    logging.INFO(time.time() - timer.time)
    timer.time = time.time()


class Algorithm(GraphDiffAlgorithm):
    P = parameters.P
    NUMBER_OF_ITERATIONS = parameters.NUMBER_OF_ITERATIONS
    NUMBER_OF_AGENTS = parameters.NUMBER_OF_AGENTS

    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        self.graph1 = AntGraph(graph1)
        self.graph2 = AntGraph(graph2)

        matched = construct_matched_for_first(graph1, graph2)
        self.graph1.set_iterator(matched)

        logging.debug('pheromon initialized as {} defaultdicts'.format(self.graph1.len + 1))
        self.pheromon = [defaultdict(itertools.repeat(1).__next__) for _ in range(self.graph1.len)]

        pathfinders = [Pathfinder(self.graph1, self.graph2, self.pheromon, matched) for _ in
                       range(0, self.NUMBER_OF_AGENTS)]

        assert self.NUMBER_OF_ITERATIONS > 0
        assert self.NUMBER_OF_AGENTS > 0

        route = []

        def T_MIN_f(iteration: int):
            return 1

        def T_MAX_f(iteration: int):
            return iteration + 3

        for _ in range(0, self.NUMBER_OF_ITERATIONS):
            T_MIN = T_MIN_f(_)
            T_MAX = T_MAX_f(_)

            for i in range(0, self.NUMBER_OF_AGENTS):
                pathfinders[i].find_route()

            routes = [(p.route, p.score) for p in pathfinders]
            m = max(routes, key=lambda x: x[1])
            routes.append((m[0], m[1] * _ / 10))

            for i in range(self.graph1.len):
                for key in self.pheromon[i]:
                    self.pheromon[i][key] *= 1 - self.P
                    self.pheromon[i][key] = max(self.pheromon[i][key], T_MIN)


            for route, score in routes:
                for i, u in enumerate(route):
                    self.pheromon[i + 1][u] += 3 / self.NUMBER_OF_AGENTS
                    self.pheromon[i + 1][u] = min(T_MAX, self.pheromon[i + 1][u])

        assert_set = set()
        for u in route:
            if not (u not in assert_set or u == 0):
                print("!")
            assert u not in assert_set or u == 0
            assert_set.add(u)

        route = {self.graph1.nodes[i + 1]: self.graph2.nodes[u] for i, u in enumerate(route) if u is not None}

        return GraphMap().construct_graph_map(route, graph1, graph2)


def construct_matched_for_first(graph1: GraphWithRepetitiveNodesWithRoot,
                                graph2: GraphWithRepetitiveNodesWithRoot):
    dict_matched = {}

    labels_first = defaultdict(set)
    labels_second = defaultdict(set)
    for node in graph1:
        labels_first[node.Label].add(node)
    for node in graph2:
        labels_second[node.Label].add(node)
    for label, label_set_first in labels_first.items():
        label_set_second = labels_second[label]
        if len(label_set_second) == 0:
            for node in label_set_first:
                dict_matched[node] = None
        elif len(label_set_second) == 1 and len(label_set_first) == 1:
            for node1 in label_set_first:
                for node2 in label_set_second:
                    dict_matched[node1] = node2
    return dict_matched
