from abc import ABC, abstractmethod

from .graph import GraphWithRepetitiveNodesWithRoot
from .graph_map import GraphMap


class GraphDiffAlgorithm(ABC):
    @abstractmethod
    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap: pass