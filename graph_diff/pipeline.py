from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter, print_together
from graph_diff.nirvana_object_model.workflow_to_graph_converter import WorkflowToGraphConverter


class Pipeline:
    def __init__(self,
                 algorithm: GraphDiffAlgorithm,
                 workflow_converter: WorkflowToGraphConverter):
        self._algo = algorithm
        self._to_abstract_converter = workflow_converter
        self._to_dot_converter = WorkflowToDotConverter

    def get_diff(self, workflow1: Workflow, workflow2: Workflow):
        # Transforming given workflow to abstract graphs
        graph1 = self._to_abstract_converter.convert(workflow=workflow1)
        graph2 = self._to_abstract_converter.convert(workflow=workflow2)

        # Constructing difference 'twixt abstract graphs.
        graph_map = self._algo.construct_diff(graph1=graph1, graph2=graph2)

        # Evaluation of complete difference between graphs.
        graph_map.eval_difference_complete()

        # Converting graph difference back to normal workflow with function of colors
        workflow_diff, block_colors = self._to_abstract_converter.convert_graph_map(graph_map=graph_map)

        # Conversion of workflow with colors to dot.
        dot_diff = self._to_dot_converter().convert_workflow(workflow=workflow_diff, colors=block_colors)

        return dot_diff

    def print_diff(self, workflow1: Workflow, workflow2: Workflow, path: str):
        dot_workflow1 = self._to_dot_converter("1").convert_workflow(workflow=workflow1)
        dot_workflow2 = self._to_dot_converter("2").convert_workflow(workflow=workflow2)

        dot_diff = self.get_diff(workflow1, workflow2)

        print_together(dot_workflow1, dot_diff, dot_workflow2,
                       names=['from_workflow', 'diff_workflow', 'to_workflow']).write(path, format='png')
