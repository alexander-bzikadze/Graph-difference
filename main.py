# from graph_diff.cpp_algorithms.algorithm_compiler import AlgorithmCompiler
# from graph_diff.cpp_algorithms.algorithm_runner import AlgorithmRunner
from graph_diff.cpp_algorithms.algorithms import CppImport
from graph_diff.graph import rnr_graph, lr_node

# from graph_diff.nirvana_object_model.workflow.block import Block
# from graph_diff.nirvana_object_model.workflow.operation import Operation
# from graph_diff.nirvana_object_model.worflow_generator.standard_workflow_generator import StandardWorkflowGenerator
# from graph_diff.nirvana_object_model.workflow import Workflow
# from graph_diff.nirvana_object_model.workflow_to_dot_converter import WorkflowToDotConverter

# logging.info("Creating first workflow")
#
# workflow = Workflow()
# b1 = Block(operation=Operation("1", (), ["json", "html"]))
# b2 = Block(operation=Operation("2", ["json"], ["json"]))
# b3 = Block(operation=Operation("3", ["json"]))
# workflow.add_block(b1)
# workflow.add_block(b2)
# workflow.add_block(b2)
# workflow.add_block(b3)
# workflow.add_connection_by_data(b1, 1, "json", b2, 1, "json")
# workflow.add_connection_by_data(b2, 1, "json", b3, 1, "json")
# workflow.add_connection_by_data(b1, 1, "json", b2, 2, "json")
# workflow.add_connection_by_data(b1, 1, "json", b3, 1, "json")
# workflow.add_connection_by_data(b2, 2, "json", b3, 1, "json")
# workflow.add_connection_by_execution(b1, 1, b3, 1)
#
# logging_config.logging.info("Creating second workflow")
#
# workflow1 = workflow
# workflow2 = Workflow()
# workflow2.add_block(b1)
# workflow2.add_block(b1)
# workflow2.add_block(b2)
# workflow2.add_block(b3)
# workflow2.add_connection_by_data(b1, 1, "json", b2, 1, "json")
# workflow2.add_connection_by_data(b1, 2, "json", b2, 1, "json")
# workflow2.add_connection_by_data(b2, 1, "json", b3, 1, "json")
#
# logging.info("Run pipeline with Complete converter on workflows 1 and 2. Result printed to nirvana+")
# Pipeline(BaselineAlgorithm(GraphMapComparatorByEdgeNum()), CompleteWorkflowToGraphConverter()).print_diff(
#     workflow1=workflow1, workflow2=workflow2, path="./nirvana+.png")

# generator = StandardWorkflowGenerator().generate_blocks()
#
# logging.info("Generation two workflows")
# w = generator.generate_workflow()
# w1 = generator.generate_workflow()
#
# logging.info("Converting workflows to dot")
# w_dot = WorkflowToDotConverter('1').convert_workflow(w)
# w1_dot = WorkflowToDotConverter('2').convert_workflow(w1)
#
# w_dot.write("./w.png", format='png')
# w1_dot.write("./w1.png", format='png')
#
# logging.info("Run pipeline on generated workflows")
# w2_dot = Pipeline(BaselineAlgorithm(GraphMapComparatorByEdgeNum()), CompleteWorkflowToGraphConverter()).get_diff(w, w1)

# print_together(w_dot, w2_dot, w1_dot, names=['w_dot', 'w2_dot', 'w1_dot']).write("./w2.png", format='png')
from graph_diff.graph_diff_algorithm.compose_graph_diff_algorithm import ComposedGraphDiffAlgorithm
from graph_diff.simulated_annealing_algorithm.sim_anneal_algorithm import SimAnnealAlgorithm as SimAnnealAlgorithm

NUM = 5

def full_graph(num: int):
    graph = rnr_graph()
    for i in range(1, num + 1):
        for j in range(i + 1, num + 1):
            graph.add_edge(lr_node(1, i), lr_node(1, j))
    return graph

graph1 = full_graph(NUM)
graph2 = full_graph(NUM)

algo = SimAnnealAlgorithm()
algo.construct_diff(graph1, graph2)

# with open('big_graph.txt', mode='w') as file:
#     print('\n'.join(GraphPrinter(graph1, graph2).print_graph1()), file=file)



# for i in range(1, NUM + 1):
#     graph2.add_node(lr_node(1, i))

# graph1 = rnr_graph()
# graph2 = rnr_graph()
# x = 3
# y = 3
# for i in range(1, x + 1):
#     graph1.add_node(lr_node(i, i))
# for i in range(1, y + 1):
#     graph2.add_node(lr_node(i, i))


# print('\n'.join(GraphPrinter(graph1).print_graph()))
# AlgorithmCompiler().compile_baseline_algorithm()

# sc = 0
# for _ in tqdm.tqdm(range(0, 10000)):
#     diff = CppImport.AntAlgorithm().construct_diff(graph1, graph1)
#     if GraphMapComparatorByEdgeNum().comparable_representation(diff) != 1:
#         print(diff._graph_map_1_to_2)
#         sc += 1
# print(sc)

# for _ in range(0, 1):
#     diff = CppImport.AntAlgorithm().construct_diff(graph1, graph1)
#     if GraphMapComparatorByEdgeNum().comparable_representation(diff) != 3:
#         print(GraphMapComparatorByEdgeNum().comparable_representation(diff))
#         print(diff._graph_map_1_to_2)

# print(AlgorithmCompiler().compile_baseline_algorithm)
# AlgorithmRunner().baseline_algorithm_construct_diff(graph1, graph2)
