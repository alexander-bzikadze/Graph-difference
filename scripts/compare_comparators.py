from graph_diff.graph_map import GraphMapComparatorByEdgeNumAndThenNodeNum, GraphMapComparatorByEdgeNumAndNodeNumSum
from graph_diff.graph_comparison import generate_n_comparator_tests

NUMBER_OF_TESTS = 100

generate_n_comparator_tests(NUMBER_OF_TESTS, [
    GraphMapComparatorByEdgeNumAndThenNodeNum(),
    GraphMapComparatorByEdgeNumAndNodeNumSum()
])
