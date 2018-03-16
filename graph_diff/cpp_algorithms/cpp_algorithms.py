from graph_diff.cpp_algorithms.algorithm_runner import AlgorithmRunner
from graph_diff.cpp_algorithms.parameters import SUPPORTED_ALGORITHMS
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm, GraphMap


def add_algorithms(cls: type):
    for algo in SUPPORTED_ALGORITHMS:
        class CppAlgorithm(GraphDiffAlgorithm):
            def __init__(self):
                self.runner = AlgorithmRunner()

            def construct_diff(self,
                               graph1: GraphWithRepetitiveNodesWithRoot,
                               graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
                return self.runner.construct_diff(algo,
                                                  graph1,
                                                  graph2)

        setattr(cls, algo, CppAlgorithm)
    return cls


@add_algorithms
class Cpp:
    pass
