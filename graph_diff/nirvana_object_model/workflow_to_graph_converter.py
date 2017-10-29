from abc import ABC, abstractstaticmethod

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.nirvana_object_model.workflow import Workflow


class WorkflowToGraphConverter(ABC):
    @abstractstaticmethod
    def convert(workflow: Workflow) -> GraphWithRepetitiveNodesWithRoot: pass

    @abstractstaticmethod
    def reverse_graph(graph: GraphWithRepetitiveNodesWithRoot) -> Workflow: pass
