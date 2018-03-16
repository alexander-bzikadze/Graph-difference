import os
import subprocess

import stringcase

from graph_diff.cpp_algorithms import parameters
from graph_diff.cpp_algorithms.algorithm_compiler import AlgorithmCompiler
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph.graph_printer import GraphPrinter
from graph_diff.graph_diff_algorithm import GraphMap


class AlgorithmRunner:
    """Class for running cpp executables and constructing graph differences"""

    RECOMPILE = parameters.RECOMPILE
    SUPPORTED_ALGORITHMS = parameters.SUPPORTED_ALGORITHMS
    EXE_FILENAME = parameters.EXE_FILENAME

    def __init__(self):
        for algo in self.SUPPORTED_ALGORITHMS:
            def new_method(graph1: GraphWithRepetitiveNodesWithRoot,
                           graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
                """Refer to docstring of method `construct_diff`."""
                return self.construct_diff(algo, graph1, graph2)

            name = '{}_construct_diff'.format(stringcase.snakecase(algo))
            self.__setattr__(name, new_method)

    def construct_diff(self,
                       algorithm: str,
                       graph1: GraphWithRepetitiveNodesWithRoot,
                       graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
        """
        Constructs difference between graph1 and graph2. Uses defined algorithm for that.
        Uses cpp executable inside itself.
        Can (and to preferred) to be ran as
        {snake_case_version_of_algorithm_name}_construct_diff.

        For example:
            runner.baseline_algorithm_construct_diff()

        :param algorithm:   class name of the corresponding algorithm to use
        :param graph1:      original graph
        :param graph2:      changed graph
        :return:            difference 'twixt graphs
        """
        if len(graph1) > len(graph2):
            graph1, graph2 = graph2, graph1

        graph1_printer = GraphPrinter(graph1)
        graph2_printer = GraphPrinter(graph2)

        graph1_str_representation = graph1_printer.print_graph()
        graph2_str_representation = graph2_printer.print_graph()

        program_input = graph1_str_representation + graph2_str_representation
        program_input = '\n'.join(program_input)

        location = os.path.realpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__)))
        if self.SUPPORTED_ALGORITHMS:
            exe_filename = AlgorithmCompiler().compile(algorithm)
        else:
            exe_filename = self.EXE_FILENAME

        cpp_algorithm = os.path.join(location, exe_filename)

        process = subprocess.Popen(cpp_algorithm, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = process.communicate(program_input.encode())[0].decode()
        output = [tuple(x.split()) for x in output.split('\n')]
        output = filter(lambda x: len(x) == 2, output)
        output = {int(a): int(b) for a, b in output}
        output = {graph1_printer.nodes[a]: graph2_printer.nodes[b] for a, b in output.items()}

        return GraphMap.construct_graph_map(output, graph1, graph2)
