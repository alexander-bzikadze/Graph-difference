# noinspection PyUnresolvedReferences
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

        logging.debug('pheromon initialized as {} defaultdicts'.format(self.graph1.len + 1))
        self.pheromon = [defaultdict(itertools.repeat(1).__next__) for _ in range(self.graph1.len)]

        pathfinders = [Pathfinder(self.graph1, self.graph2, self.pheromon) for _ in range(0, self.NUMBER_OF_AGENTS)]

        assert self.NUMBER_OF_ITERATIONS > 0
        assert self.NUMBER_OF_AGENTS > 0

        for _ in range(0, self.NUMBER_OF_ITERATIONS):
            T_MIN = 1
            T_MAX = _ + 3

            for i in range(0, self.NUMBER_OF_AGENTS):
                pathfinders[i].find_route()

            # threads = [threading.Thread(target=pathfinders[i].find_route) for i in range(0, self.NUMBER_OF_AGENTS)]
            # for t in threads:
            #     t.start()
            # for t in threads:
            #     t.join()

            routes = [(p.route, p.score) for p in pathfinders]
            m = max(routes, key=lambda x: x[1])
            routes.append((m[0], m[1] * _ / 10))

            for i in range(self.graph1.len):
                for key in self.pheromon[i]:
                    self.pheromon[i][key] *= 1 - self.P
                    self.pheromon[i][key] = max(self.pheromon[i][key], T_MIN)

            for route, score in routes:
                for i, u in enumerate(route):
                    # Route is always assigned as there is at least one iteration of the algorithm
                    self.pheromon[i + 1][u] += 3 / self.NUMBER_OF_AGENTS
                    self.pheromon[i + 1][u] = min(T_MAX, self.pheromon[i + 1][u])

                    # for i in range(self.graph1.len):
                    #     print(dict(self.pheromon[i]))

        # noinspection PyUnboundLocalVariable
        route = {self.graph1.nodes[i + 1]: self.graph2.nodes[u] for i, u in enumerate(route)}

        return GraphMap().construct_graph_map(route, graph1, graph2)
