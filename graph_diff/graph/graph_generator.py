from abc import ABC, abstractmethod

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot


class GraphGenerator(ABC):
    """
    Interface for generator of graphs.
    """

    @abstractmethod
    def generate_graph(self) -> GraphWithRepetitiveNodesWithRoot: pass
