import logging

from graph_diff.graph_comparison import generate_n_algo_tests
from graph_diff.ordered_ant_algorithm.ordered_ant_algorithm import OrderedAntAlgorithm as AntAlgorithm

NUMBER_OF_TESTS = 100
DIRECTORY = "../algo_png/"

algoes = [
    # BaselineAlgorithm(),
    AntAlgorithm()
]

logging.info("Start comparator test with {0} tests".format(NUMBER_OF_TESTS))
generate_n_algo_tests(n=NUMBER_OF_TESTS, algoes=algoes, directory=DIRECTORY)
