from graph_diff.graph import rnr_graph, lr_node
import time
from tqdm import tqdm

from graph_diff.simulated_annealing_algorithm import SimAnnealAlgorithm


def full_graph(num: int):
    graph = rnr_graph()
    for i in range(1, num + 1):
        for j in range(i + 1, num + 1):
            graph.add_edge(lr_node(1, i), lr_node(1, j))
    return graph


NUMBER_OF_TESTS = 100
with open(file='sim_anneal.dat', mode='w') as file:
    # file.write('GRAPH_SIZE GLOBAL_ITERATIONS REAL_ITERATIONS TIME ERROR RELATED_ERROR\n')
    algorithm = SimAnnealAlgorithm()
    for num in tqdm(range(100, 1000, 100)):
        graph1 = full_graph(num)
        graph2 = full_graph(num)
        for _ in tqdm(range(NUMBER_OF_TESTS)):
            start = time.time()
            _, iterations, energy = algorithm.construct_diff(graph1, graph2)
            end = time.time()
            expected = num * (num + 1) // 2
            file.write(f'{num} {SimAnnealAlgorithm.NUMBER_OF_ITERATIONS} {iterations} {end-start} {abs(energy - expected)} {abs(energy - expected) / expected}\n')

