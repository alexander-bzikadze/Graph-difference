from abc import ABC, abstractmethod
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot


class GraphGenerator(ABC):
    @abstractmethod
    def generate_graph(self) -> GraphWithRepetitiveNodesWithRoot: pass