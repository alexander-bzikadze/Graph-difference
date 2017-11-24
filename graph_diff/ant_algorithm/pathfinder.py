import logging
import time
from collections import defaultdict

import numpy


def timer(mes=""):
    print(time.time() - timer.time, mes)
    timer.time = time.time()


from graph_diff.ant_algorithm import parameters
from graph_diff.ant_algorithm.ant_graph import AntGraph


class Pathfinder:
    ALPHA = parameters.ALPHA
    BETA = parameters.BETA

    def __init__(self,
                 graph1: AntGraph,
                 graph2: AntGraph,
                 pheromon: [dict]):
        self.graph1 = graph1
        self.graph2 = graph2
        self.route = None
        self.number_of_nodes_in_first_graph = None
        self.inverse_route = None
        self.score = None
        self.scores = {}
        self.pheromon = pheromon

    def find_route(self):

        logging.debug('Finding new route')

        self.route = [None] * self.graph1.len
        self.route_set = set()
        self.inverse_route = {}
        self.score = 0
        self.number_of_nodes_in_first_graph = self.graph2.len

        chosen_zeroes_label = defaultdict(int)
        for v in self.graph1:
            timer.time = time.time()

            u_score = self.find_pair(v)

            discussed_label = self.graph1.get_label(v)
            logging.debug('Node {} has label {}'.format(v, discussed_label))

            logging.debug(
                '{}, {}, {}'.format(self.graph1.label_size(discussed_label), self.graph2.label_size(discussed_label),
                                    chosen_zeroes_label[discussed_label]))
            number_of_zeroes = max(0,
                                   self.graph1.label_size(discussed_label) - self.graph2.label_size(discussed_label) -
                                   chosen_zeroes_label[discussed_label])
            logging.debug('Number of possible zeroes is {}'.format(number_of_zeroes))

            if number_of_zeroes > 0:
                zeroes = [0]
                zeroes_probs = [self.pheromon[v][0] ** self.ALPHA + number_of_zeroes ** self.BETA]
            else:
                zeroes = []
                zeroes_probs = []

            logging.debug('{}, {}'.format(zeroes, zeroes_probs))
            probability = [(self.pheromon[v][u] ** self.ALPHA) * (us ** self.BETA) if u not in self.route_set else 0 for
                           u, us in u_score.items()] + zeroes_probs
            logging.debug('Probability is {}'.format(probability))

            prob_sum = sum(probability)
            probability = [p / prob_sum for p in probability]
            values = self.graph2.label(self.graph1.get_label(v)) + zeroes
            chosen = numpy.random.choice(a=values, p=probability)

            self.route[v] = chosen
            self.route_set.add(chosen)
            self.inverse_route[chosen] = v
            self.update(v, chosen)
            if chosen == 0:
                chosen_zeroes_label[discussed_label] += 1
            else:
                self.score += u_score[chosen]

        logging.debug('route is {}'.format(self.route))
        self.route = self.route[1:]
        self.scores = {}

    def find_pair(self, v):
        u_score = {}
        logging.debug('Finding pair for node {}'.format(v))
        logging.debug('Score is number of adjacent nodes, that being mapped to first graph have edge with v.')
        for u in self.graph2.label(self.graph1.get_label(v)):
            if (v, u) not in self.scores.keys():
                self.scores[v, u] = 1
            u_score[u] = self.scores[v, u]
        logging.debug('Scores for node {} are dict {}'.format(v, dict(u_score)))
        return u_score

    def update(self, v, u):
        if v == 0 or u == 0:
            return
        for u1 in self.graph1.outcoming(v):
            for u2 in self.graph2.outcoming(u):
                if (u1, u2) not in self.scores.keys():
                    self.scores[u1, u2] = 1
                self.scores[u1, u2] += 1
        for u1 in self.graph1.incoming(v):
            for u2 in self.graph2.incoming(u):
                if (u1, u2) not in self.scores.keys():
                    self.scores[u1, u2] = 1
                self.scores[u1, u2] += 1
