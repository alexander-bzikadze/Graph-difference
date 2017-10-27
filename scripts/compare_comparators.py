from graph_diff.graph_map import GraphMapComparatorByEdgeNumAndThenNodeNum, \
    GraphMapComparatorByEdgeNumAndNodeNumSum, \
    GraphMapComparatorByNodeNumAndThenEdgeNum, \
    GraphMapComparatorByEdgeNum, \
    GraphMapComparatorByNodeNum
from graph_diff.graph_comparison import generate_n_comparator_tests

NUMBER_OF_TESTS = 100
DIRECTORY = "../comparator_png/"

generate_n_comparator_tests(NUMBER_OF_TESTS, [
    GraphMapComparatorByEdgeNumAndThenNodeNum(),
    GraphMapComparatorByEdgeNumAndNodeNumSum(),
    GraphMapComparatorByNodeNumAndThenEdgeNum(),
    GraphMapComparatorByNodeNum(),
    GraphMapComparatorByEdgeNum()
], DIRECTORY)
