from graph_diff.graph.graph_generator import GraphGenerator
from graph_diff.graph_map import GraphMapComparatorByEdgeNumAndThenNodeNum, GraphMapComparatorByEdgeNumAndNodeNumSum
from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import lr_node, RNR_graph
from graph_diff.to_dot_converter import write_diff, write_graph
from graph_diff.graph_comparison import generate_n_comparator_tests

# graph1 = RNR_graph().add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 1), lr_node(1, 3))
# graph2 = RNR_graph().add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 2), lr_node(1, 3)).add_node(lr_node(1, 4))
# graph_map = BaselineAlgorithm(GraphMapComparatorByEdgeNumAndThenNodeNum()).construct_diff(graph1, graph2)
# write_graph(graph1, "./graph1.png")
# write_graph(graph2, "./graph2.png")
# write_diff(graph_map, "./graph_map.png")

generate_n_comparator_tests(10, [
    GraphMapComparatorByEdgeNumAndThenNodeNum(),
    GraphMapComparatorByEdgeNumAndNodeNumSum()
])

# graph_test1 = RNR_graph()\
#     .add_edge(lr_node(1, 1), lr_node(2, 1))\
#     .add_edge(lr_node(2, 2), lr_node(2, 3))\
#     .add_edge(lr_node(1, 1), lr_node(2, 2))
# graph_test2 = RNR_graph()\
#     .add_edge(lr_node(1, 1), lr_node(4, 1))\
#     .add_edge(lr_node(1, 1), lr_node(2, 1))\
#     .add_edge(lr_node(2, 1), lr_node(3, 1))\
#     .add_edge(lr_node(2, 1), lr_node(5, 1))\
#     .add_edge(lr_node(3, 1), lr_node(5, 1))
#
# graph_map = BaselineAlgorithm(GraphMapComparatorByEdgeNumAndNodeNumSum()).construct_diff(graph_test1, graph_test2)

# write_graph(graph_test1, "./graph1_test.png")
# write_graph(graph_test2, "./graph2_test.png")
# write_diff(graph_map, "./graph_map_test.png")
