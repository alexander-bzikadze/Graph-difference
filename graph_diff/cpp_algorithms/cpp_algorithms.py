from graph_diff.cpp_algorithms.decorators import add_algorithms


@add_algorithms
class Cpp:
    """
    Class for running cpp realizations of algorithms.
    Logical part of the class initialization is contained in the decorator.
    This class should be considered a module
    containing algorithms and treated as such.
    List of the available algorithms contained in parameters.SUPPORTED_ALGORITHMS.

    Example of usage:
    graph1, graph2
    diff = Cpp.BaselineAlgorithm().construct_diff(graph1, graph2)
    """
    pass
