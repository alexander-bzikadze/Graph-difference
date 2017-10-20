from graph_diff.graph.graph_generator import GraphGenerator
from graph_diff.graph_map import GraphMapComparatorByEdgeNumAndThenNodeNum
from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import lr_node, RNR_graph
from graph_diff.to_dot_converter import write_diff, write_graph

graph1 = RNR_graph().add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 1), lr_node(1, 3))
graph2 = RNR_graph().add_edge(lr_node(1, 1), lr_node(1, 2)).add_edge(lr_node(1, 2), lr_node(1, 3)).add_node(lr_node(1, 4))
graph_map = BaselineAlgorithm(GraphMapComparatorByEdgeNumAndThenNodeNum()).construct_diff(graph1, graph2)
write_graph(graph1, "./graph1.png")
write_graph(graph2, "./graph2.png")
write_diff(graph_map, "./graph_map.png")

generator = GraphGenerator(2, 10)
generated = generator.generate_graph()
write_graph(generated, "./generated.png")
