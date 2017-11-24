from abc import ABC, abstractmethod

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_map import GraphMap
from graph_diff.nirvana_object_model.graph_map_dot_colorer import GraphDotColorer
from graph_diff.nirvana_object_model.workflow import Workflow


class WorkflowToGraphConverter(ABC):
    @abstractmethod
    def convert(self, workflow: Workflow) -> GraphWithRepetitiveNodesWithRoot: pass

    @abstractmethod
    def reverse_graph(self, graph: GraphWithRepetitiveNodesWithRoot) -> Workflow: pass

    @abstractmethod
    def convert_graph_map(self, graph_map: GraphMap) -> (Workflow, GraphDotColorer): pass
