import stringcase

from graph_diff.cpp_algorithms.algorithm_importer import AlgorithmImporter
from graph_diff.cpp_algorithms.parameters import SUPPORTED_ALGORITHMS
from graph_diff.graph import GraphWithRepetitiveNodesWithRoot
from graph_diff.graph.graph_printer import GraphPrinter
from graph_diff.graph_diff_algorithm import GraphMap, GraphDiffAlgorithm


def add_run_algorithms(cls: type):
    """
    Adds supported algorithms-classes to class-container.

    :param cls: class-container to modify
    :return:    modified class
    """
    from graph_diff.cpp_algorithms.algorithm_runner import AlgorithmRunner
    runner = AlgorithmRunner()
    for algo in SUPPORTED_ALGORITHMS:
        class CppAlgorithm(GraphDiffAlgorithm):
            def construct_diff(self,
                               graph1: GraphWithRepetitiveNodesWithRoot,
                               graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
                __name__ = type(self).__name__
                return runner.construct_diff(__name__,
                                             graph1,
                                             graph2)

        CppAlgorithm.__name__ = algo
        CppAlgorithm.__doc__ = """Realization of algorithm {} on cpp""".format(algo)

        setattr(cls, algo, CppAlgorithm)
    return cls


def add_imported_algorithms(cls: type):
    algorithm_importer = AlgorithmImporter()
    for algo in SUPPORTED_ALGORITHMS:
        class CppAlgorithm(GraphDiffAlgorithm):
            def construct_diff(self,
                               graph1: GraphWithRepetitiveNodesWithRoot,
                               graph2: GraphWithRepetitiveNodesWithRoot) -> GraphMap:
                graph_printer = GraphPrinter(graph1, graph2)
                repr_first = graph_printer.graph_transformer_first()
                repr_second = graph_printer.graph_transformer_second()

                __name__ = type(self).__name__
                output = getattr(algorithm_importer.module, stringcase.snakecase(__name__)) \
                    (*repr_first, *repr_second)
                # print(*repr_first, *repr_second)
                # print(output)
                return graph_printer.back_transformer(output)

        CppAlgorithm.__name__ = algo
        CppAlgorithm.__doc__ = """Realization of algorithm {} on cpp""".format(algo)

        setattr(cls, algo, CppAlgorithm)
    return cls


def clone_method(method_name: str, *args):
    """
    Clones given method by given args and creates series of methods.
    Let x be one of the args. For every x in args
    this method adds method which has logic to run original method with x as argument
    and which name is f'{method_name}_{x}'.

    :param method_name:     name of the method with exactly one argument
    :param args:            arguments for the method
    :return:                decorator function that will modify a class given
    """

    def wrapped_decorator(cls: type):
        for clone_id in args:
            snake_case_clone_id = stringcase.snakecase(clone_id)
            new_method_name = '{}_{}'.format(method_name, snake_case_clone_id)

            def new_method(self):
                method = getattr(self, method_name)
                return method(clone_id)

            new_method.__doc__ = """
            Generated by clone_method decorator method {} of class {cls}. 
            Please refer to {cls}.{method_name} documentation.
            """.format(new_method_name, method_name=method_name, cls=cls.__name__)
            new_method.__name__ = new_method_name
            setattr(cls, new_method_name, new_method)
        return cls

    return wrapped_decorator
