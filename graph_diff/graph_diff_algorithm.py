from abc import ABC, abstractmethod
from .graph import GraphWithRepetitiveNodesWithRoot


class GraphDiffAlgorithm(ABC):
    @abstractmethod
    def construct_diff(self, graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot): pass