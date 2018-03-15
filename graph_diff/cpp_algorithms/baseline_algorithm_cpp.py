import os
import subprocess
import sys

from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph.graph_printer import print_graph
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm, GraphMap


class BaselineAlgorithmCpp(GraphDiffAlgorithm):
    def construct_diff(self,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        graph1_str_representation = print_graph(graph1)
        graph2_str_representation = print_graph(graph2)
        program_input = graph1_str_representation + graph2_str_representation
        program_input = '\n'.join(program_input)
        # program_input = StringIO(program_input)
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __cpp_algorithm__ = os.path.join(__location__, 'main')

        process = subprocess.Popen(__cpp_algorithm__, stdin=subprocess.PIPE, stdout=sys.stdout)
        # process.stdin.write(program_input)
        # print(program_input)
        # print(program_input.encode())
        process.communicate(program_input.encode())
