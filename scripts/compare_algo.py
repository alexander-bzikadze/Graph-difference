import logging

from graph_diff.ant_algorithm.algorithm import Algorithm as AntAlgorithm
from graph_diff.graph_comparison import generate_n_algo_tests

NUMBER_OF_TESTS = 100
DIRECTORY = "../algo_png/"

algoes = [
    # BaselineAlgorithm(),
    AntAlgorithm()
]

logging.info("Start comparator test with {0} tests".format(NUMBER_OF_TESTS))
generate_n_algo_tests(n=NUMBER_OF_TESTS, algoes=algoes, directory=DIRECTORY)
