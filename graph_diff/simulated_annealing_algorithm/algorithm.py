from collections import defaultdict
from copy import copy

import math
import scipy
from scipy.stats import randint

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph.graph_printer import GraphPrinter
from graph_diff.graph_diff_algorithm.graph_diff_algorithm import GraphDiffAlgorithmWithInit
from graph_diff.graph_diff_algorithm.graph_map import GraphMap


# TODO: the algorithm
class Algorithm(GraphDiffAlgorithmWithInit):
    def __init__(self):
        self.graph1 = None
        self.graph2 = None
        self.init_solution = None
        self.current_solution = None
        self.nodes1, self.edges1 = None, None
        self.nodes2, self.edges2 = None, None
        self.printer = None

    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        self.graph1 = graph1
        self.graph2 = graph2

        self.printer = GraphPrinter(graph1, graph2)
        self.nodes1, self.edges1 = self.printer.graph_transformer_first()
        self.nodes2, self.edges2 = self.printer.graph_transformer_second()
        self.edges1, self.edges2 = list(map(set, self.edges1)), list(map(set, self.edges2))

        if self.init_solution is None:
            self.init_solution = self._initial_solution()
        else:
            self.init_solution = self.printer.graph_map_to_list(self.init_solution)
        self.current_solution = copy(self.init_solution)

        energy = self._score(self.current_solution)
        global_energy = energy
        global_solution = copy(self.current_solution)

        for _ in range(1, 10000):
            if global_energy < energy:
                global_solution = copy(self.current_solution)
                global_energy = energy
            x = self._take_step()
            x_energy = self._score(x)
            alpha = scipy.random.uniform(0, 1)
            if alpha < math.exp(-(energy - x_energy) / self.time_law(_)):
                self.current_solution = x
                energy = x_energy

        self.init_solution = None
        return self.printer.back_transformer(global_solution)

    def time_law(self, k: int):
        t0 = 100
        return t0 / k

    def set_init(self, new_init: GraphMap):
        self.init_solution = copy(new_init)

    def _initial_solution(self):
        initial = [-1] * len(self.graph1)
        labels = defaultdict(list)
        for v in self.graph2:
            labels[v.Label].append(self.printer.node2_to_index[v])
        for i, v in enumerate(self.graph1):
            if labels[v.Label]:
                initial[i] = labels[v.Label][-1]
                labels[v.Label].pop()
        return initial

    def _score(self, x):
        score = 0
        for i, j in enumerate(x):
            if j == -1:
                continue
            for v in self.edges1[i]:
                if x[v] in self.edges2[j]:
                    score += 1
        return score

    def _take_step(self,
                   num_try=0):
        if num_try == 10:
            return self.current_solution

        solution = copy(self.current_solution)

        change = randint.rvs(0, len(solution))

        label, _ = self.nodes1[change]
        choice = [i for i, (l, _) in enumerate(self.nodes2) if l == label]

        if len(choice) < 2:
            return self._take_step(num_try + 1)

        change_with = randint.rvs(0, len(choice))
        change_with = choice[change_with]

        i = [i for i, x in enumerate(solution) if x == change_with]

        if not i:
            solution[change] = change_with
        elif len(i) == 1:
            solution[change], solution[i[0]] = solution[i[0]], solution[change]
        else:
            assert False

        return solution
