import time
from tqdm import tqdm

from graph_diff.cpp_algorithms.algorithms import CppImport
from graph_diff.graph import rnr_graph, lr_node
from graph_diff.graph_diff_algorithm import ComposedGraphDiffAlgorithm, GraphMapComparatorByEdgeNum
from graph_diff.simulated_annealing_algorithm import SimAnnealAlgorithm


def full_graph(num: int):
    graph = rnr_graph()
    for i in range(1, num + 1):
        for j in range(i + 1, num + 1):
            graph.add_edge(lr_node(1, i), lr_node(1, j))
    return graph

NUMBER_OF_TESTS = 100

ALGORITHMS = {
              # CppImport.OrderedAntAlgorithm:      [10, 110, 10],
              # ComposedGraphDiffAlgorithm
              #   (CppImport.OrderedAntAlgorithm(),
              #    SimAnnealAlgorithm()):             [10, 110, 10],
              #  CppImport.UnorderedAntAlgorithm:    [50, 110, 10],
              SimAnnealAlgorithm: [10, 110, 10]}

for algo, params in ALGORITHMS.items():
    with open(file=f'{algo.__name__}.dat', mode='a') as file:
        file.write('GRAPH_SIZE TIME ERROR RELATED_ERROR\n')
        algorithm = algo() if isinstance(algo, type) else algo
        for num in tqdm(range(*params)):
            graph1 = full_graph(num)
            graph2 = full_graph(num)
            expected = sum([len(graph1.get_list_of_adjacent_nodes(v)) for v in graph1])
            for _ in tqdm(range(NUMBER_OF_TESTS)):
                start = time.time()
                diff = algorithm.construct_diff(graph1, graph2)
                energy = GraphMapComparatorByEdgeNum().comparable_representation(diff)
                end = time.time()
                file.write(f'{num} {end-start} {abs(energy - expected)} {abs(energy - expected) / expected}\n')
    print(f'{algo.__name__} DONE!')
    pass
