from graph_diff.graph.graph_generator import GraphGenerator
from .graph import GraphWithRepetitiveNodesWithRoot, StandardGraphGenerator
from .baseline_algorithm import BaselineAlgorithm
from .graph_map import GraphMap
from .graph_map import GraphMapComparator
from .to_dot_converter import convert_graph, convert_diff


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
                                graph_generator: GraphGenerator = StandardGraphGenerator(0, 5)):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(0, n):
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
        for j, graph_map in enumerate(baseline_on_different_comparators(graph1, graph2, comparators)):
            res.add_subgraph(dot_to_subgraph(convert_diff(
                graph_map=graph_map,
                separator=comparators[j].__class__.__name__),
                comparators[j].__class__.__name__
            ))
        res.add_subgraph(dot_to_subgraph(convert_graph(graph2, "graph2"), "graph2"))

        res.write(directory + "comparison" + str(i) + ".png", format="png")

        print("Test i=" + str(i) + " of n=" + str(n) + " done.")
