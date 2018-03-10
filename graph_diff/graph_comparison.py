import logging
import time

from graph_diff.graph.graph_generator import GraphGenerator
from graph_diff.graph_diff_algorithm import GraphDiffAlgorithm
from .baseline_algorithm import BaselineAlgorithm
from .graph import GraphWithRepetitiveNodesWithRoot, StandardGraphGenerator
from .graph_map import GraphMap
from .graph_map import GraphMapComparator
from .to_dot_converter import convert_graph, convert_diff


# TODO: move to scripts


def graph_comparison_with_baseline(graph1: GraphWithRepetitiveNodesWithRoot,
                                   graph2: GraphWithRepetitiveNodesWithRoot,
                                   comparator: GraphMapComparator) -> GraphMap:
    algorithm = BaselineAlgorithm(comparator)
    return algorithm.construct_diff(graph1, graph2)


def baseline_on_different_comparators(graph1: GraphWithRepetitiveNodesWithRoot,
                                      graph2: GraphWithRepetitiveNodesWithRoot,
                                      comparators: [GraphMapComparator]):
    return [graph_comparison_with_baseline(graph1, graph2, comparator) for comparator in comparators]


def generate_n_comparator_tests(n: int,
                                comparators: [GraphMapComparator],
                                directory: str,
                                graph_generator: GraphGenerator = StandardGraphGenerator(2, 5)):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(0, n):
        logging.info('Start test {0}'.format(i))

        logging.debug('Generating two graphs')
        graph1 = graph_generator.generate_graph()
        graph2 = graph_generator.generate_graph()

        import pydot

        def dot_to_subgraph(graph: pydot.Dot, label: str) -> pydot.Cluster:
            graph_s = pydot.Cluster(label, label=label)
            for node in graph.get_nodes():
                graph_s.add_node(node)
            for edge in graph.get_edges():
                graph_s.add_edge(edge)
            return graph_s

        res = pydot.Dot()
        res.add_subgraph(dot_to_subgraph(convert_graph(graph1, "graph1"), "graph1"))

        logging.debug('Running different comparators on baseline algorithm')
        for j, graph_map in enumerate(baseline_on_different_comparators(graph1, graph2, comparators)):
            res.add_subgraph(dot_to_subgraph(convert_diff(
                graph_map=graph_map,
                separator=comparators[j].__class__.__name__),
                comparators[j].__class__.__name__
            ))
        res.add_subgraph(dot_to_subgraph(convert_graph(graph2, "graph2"), "graph2"))

        res.write(directory + "comparison" + str(i) + ".png", format="png")

        logging.info("Test i={0} of n={1} done.".format(i, n))


def generate_n_algo_tests(n: int,
                          algoes: [GraphDiffAlgorithm],
                          directory: str,
                          graph_generator: GraphGenerator = StandardGraphGenerator(0, 50)):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(0, n):
        timer.time = time.time()
        logging.debug('Start test {0}'.format(i))

        timer('Generate')
        logging.debug('Generating two graphs')
        graph1 = graph_generator.generate_graph()
        graph2 = graph_generator.generate_graph()
        timer('Generated')

        import pydot

        def dot_to_subgraph(graph: pydot.Dot, label: str) -> pydot.Cluster:
            graph_s = pydot.Cluster(label, label=label)
            for node in graph.get_nodes():
                graph_s.add_node(node)
            for edge in graph.get_edges():
                graph_s.add_edge(edge)
            return graph_s

        res = pydot.Dot()
        res.add_subgraph(dot_to_subgraph(convert_graph(graph1, "graph1"), "graph1"))

        timer('Start algoes')
        logging.debug('Running different algorithms')
        for j, graph_map in enumerate([algo.construct_diff(graph1, graph2) for algo in algoes]):
            timer('algo')
            print(len(list(graph1)), len(list(graph2)))
            res.add_subgraph(dot_to_subgraph(convert_diff(
                graph_map=graph_map,
                separator=algoes[j].__class__.__name__),
                algoes[j].__class__.__name__
            ))
        res.add_subgraph(dot_to_subgraph(convert_graph(graph2, "graph2"), "graph2"))

        res.write(directory + "comparison" + str(i) + ".png", format="png")

        logging.info("Test i={0} of n={1} done.".format(i, n))


def timer(mes=''):
    print(time.time() - timer.time, mes)
    timer.time = time.time()
