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
    MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE = parameters.MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE

    def __init__(self):
        self.best_choice = None
        self.best_score = -1

    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        self.graph1 = AntGraph(graph1)
        self.graph2 = AntGraph(graph2)

        self.best_choice = None
        self.best_score = -1

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
            return 1 / (iteration + 1)

        def T_MAX_f(iteration: int):
            return iteration / 2

        number_of_iterations_with_the_same_score = 0
        score_graphic = []

        for _ in range(0, self.NUMBER_OF_ITERATIONS):
            T_MIN = T_MIN_f(_)
            T_MAX = T_MAX_f(_)

            number_of_iterations_with_the_same_score += 1

            for i in range(0, self.NUMBER_OF_AGENTS):
                pathfinders[i].find_route()
                if pathfinders[i].score > self.best_score:
                    self.best_choice = pathfinders[i].route
                    self.best_score = pathfinders[i].score
                    number_of_iterations_with_the_same_score = 0

            if self.MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE <= number_of_iterations_with_the_same_score:
                break

            routes = [(p.route, p.score) for p in pathfinders]
            m = max(routes, key=lambda x: x[1])

            for i in range(self.graph1.len):
                for key in self.pheromon[i]:
                    self.pheromon[i][key] *= 1 - self.P

            for i, u in enumerate(m[0]):
                self.pheromon[i + 1][u] += 1 / (10 + self.best_score - m[1])

            score_graphic.append(self.best_score)

        assert_set = set()
        for u in route:
            if not (u not in assert_set or u == 0):
                print("!")
            assert u not in assert_set or u == 0
            assert_set.add(u)

        route = {self.graph1.nodes[i + 1]: self.graph2.nodes[u] for i, u in enumerate(self.best_choice) if
                 u is not None}

        with open('score_graph.txt', 'a') as f:
            f.write(str(score_graphic))
            f.write('\n')

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
