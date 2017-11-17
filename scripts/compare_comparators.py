import logging

from graph_diff.graph import rnr_graph
from graph_diff.graph.graph_generator import GraphGenerator
from graph_diff.graph_comparison import generate_n_comparator_tests
from graph_diff.graph_map import *

NUMBER_OF_TESTS = 100
DIRECTORY = "../comparator_png/"

comparators = [
    GraphMapComparatorByEdgeNumAndThenNodeNum(),
    # GraphMapComparatorByEdgeNumAndNodeNumSum(),
    # GraphMapComparatorByNodeNumAndThenEdgeNum(),
    GraphMapComparatorByNodeNum(),
    GraphMapComparatorByEdgeNum(),
    GraphMapComparatorByEdgeDiffAndThenNodeDiff()
]

logging.info("Start comparator test with {0} tests".format(NUMBER_OF_TESTS))
generate_n_comparator_tests(n=NUMBER_OF_TESTS, comparators=comparators, directory=DIRECTORY)


class GeneratorMock(GraphGenerator):
    i = 0
    def generate_graph(self):
        if self.i == 0:
            graph = rnr_graph()
            graph.add_node(lr_node(1, 1))
            graph.add_node(lr_node(1, 2))
            graph.add_node(lr_node(1, 3))
            graph.add_node(lr_node(2, 1))
            graph.add_node(lr_node(2, 2))
        elif self.i == 1:
            graph = rnr_graph()
            graph.add_node(lr_node(1, 1))
            graph.add_node(lr_node(1, 2))
            graph.add_node(lr_node(2, 3))
            graph.add_node(lr_node(2, 1))
            graph.add_node(lr_node(2, 2))
        else:
            raise Exception("")
        self.i += 1
        return graph


# generate_n_comparator_tests(n=1, comparators=comparators, directory=DIRECTORY, graph_generator=GeneratorMock())
