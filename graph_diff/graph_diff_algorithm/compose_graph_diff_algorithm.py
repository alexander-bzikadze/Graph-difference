from functools import reduce

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from .graph_diff_algorithm import GraphDiffAlgorithm, GraphDiffAlgorithmWithInit
from .graph_map import GraphMap


class ComposedGraphDiffAlgorithm(GraphDiffAlgorithm):
    """Class that allows composition of algorithms"""

    def __init__(self,
                 first_algorithm: GraphDiffAlgorithm,
                 *other_algorithms: GraphDiffAlgorithmWithInit):
        self.first = first_algorithm
        self.others = list(other_algorithms)

    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        return reduce(lambda diff, algo: algo.set_init(diff).construct_diff(graph1, graph2),
                      self.others,
                      self.first.construct_diff(graph1, graph2))
