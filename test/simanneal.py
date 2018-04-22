from graph_diff.cpp_algorithms.algorithms import CppImport
from graph_diff.graph import rnr_graph, lr_node
from graph_diff.graph_diff_algorithm import GraphMap
from graph_diff.simulated_annealing_algorithm.algorithm import Algorithm as SimAnnealAlgorithm

alg = SimAnnealAlgorithm()

NUM = 30
graph1 = rnr_graph()
graph2 = rnr_graph()
for i in range(1, NUM + 1):
    for j in range(i + 1, NUM + 1):
        graph1.add_edge(lr_node(1, i), lr_node(1, j))
        graph2.add_edge(lr_node(1, i), lr_node(1, j))

new_alg = SimAnnealAlgorithm()
for _ in range(0, 100):
    diff = new_alg.construct_diff(graph1, graph2)
print(diff._graph_map_1_to_2)

# for _ in range(0, 10000):
#     new_alg._take_step(new_alg.init_solution)

# print(new_alg._take_step(new_alg.init_solution))

pass