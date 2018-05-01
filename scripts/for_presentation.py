import pydot

from graph_diff.baseline_algorithm import BaselineAlgorithm
from graph_diff.graph import rnr_graph, lr_node, GraphWithRepetitiveNodesWithRoot
from graph_diff.graph.to_dot_converter import convert_graph, convert_diff
from graph_diff.graph_diff_algorithm.graph_map import GraphMap
from graph_diff.nirvana_object_model.pipeline import Pipeline
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow.block import Block
from graph_diff.nirvana_object_model.workflow.operation import Operation
from graph_diff.nirvana_object_model.workflow_to_dot_converter import print_together, WorkflowToDotConverter
from graph_diff.nirvana_object_model.workflow_to_graph_converter.complete_workflow_to_graph_converter import \
    CompleteWorkflowToGraphConverter


def print_images(name: str, graph1: GraphWithRepetitiveNodesWithRoot, graph2: GraphWithRepetitiveNodesWithRoot):
    dot1 = convert_graph(graph1, '1')
    dot2 = convert_graph(graph2, '2')

    graph_diff = BaselineAlgorithm().construct_diff(graph1, graph2)

    dot_diff = convert_diff(graph_diff)

    dot_for_print = print_together(dot1, dot_diff, dot2, names=['Before_changes', 'Changes', 'After_changes'])

    dot_for_print.write(path=f'for_presentation/{name}.png', format='png')


def abstract_problem():
    name = 'abstract_problem'
    graph1 = rnr_graph() \
        .add_node(lr_node(1, 2)) \
        .add_edge(lr_node(1, 1), lr_node(2, 1)) \
        .add_edge(lr_node(1, 1), lr_node(2, 2))
    graph2 = rnr_graph() \
        .add_edge(lr_node(1, 1), lr_node(2, 1)) \
        .add_edge(lr_node(1, 2), lr_node(2, 2))

    return name, graph1, graph2


def np_complete():
    name = 'np_complete'

    subgraph = lambda g: g \
        .add_edge(lr_node(0, 1), lr_node(0, 2)) \
        .add_edge(lr_node(0, 1), lr_node(0, 3)) \
        .add_edge(lr_node(0, 2), lr_node(0, 3)) \
        .add_edge(lr_node(0, 1), lr_node(0, 4))

    graph1 = subgraph(rnr_graph())
    graph2 = subgraph(rnr_graph()) \
        .add_edge(lr_node(0, 4), lr_node(0, 5)) \
        .add_edge(lr_node(0, 2), lr_node(0, 5)) \
        .add_edge(lr_node(0, 3), lr_node(0, 5)) \
        .add_edge(lr_node(0, 2), lr_node(0, 6)) \
        .add_edge(lr_node(0, 3), lr_node(0, 6))

    return name, graph1, graph2


def score_problem():
    name = 'score_problem'
    graph1 = rnr_graph() \
        .add_edge(lr_node('1', 1), lr_node(2, 1)) \
        .add_edge(lr_node('1', 1), lr_node('1', 2))
    graph2 = rnr_graph() \
        .add_edge(lr_node('1', 1), lr_node(2, 1)) \
        .add_node(lr_node('1', 2))

    diff1 = GraphMap().construct_graph_map(
        {lr_node(0, 1): lr_node(0, 1),
         lr_node('1', 1): lr_node('1', 1),
         lr_node('1', 2): lr_node('1', 2),
         lr_node(2, 1): lr_node(2, 1),
         },
        graph1,
        graph2
    )

    diff2 = GraphMap().construct_graph_map(
        {lr_node(0, 1): lr_node(0, 1),
         lr_node('1', 1): lr_node('1', 2),
         lr_node('1', 2): lr_node('1', 1),
         lr_node(2, 1): lr_node(2, 1),
         },
        graph1,
        graph2
    )

    dot_diff = convert_diff(diff1)
    dot_diff2 = convert_diff(diff2, '3')
    dot1 = convert_graph(graph1, '1')
    dot2 = convert_graph(graph2, '2')

    dot_for_print = print_together(dot1, dot_diff2, dot_diff, dot2,
                                   names=['Before_changes', 'Best_by_nodes', 'Best_by_edges', 'After_changes'])

    dot_for_print.write(path=name + '.png', format='png')


def isomorphism():
    name = 'isomorphism'
    graph1 = rnr_graph() \
        .add_edge(lr_node('1', 1), lr_node(2, 1)) \
        .add_edge(lr_node('1', 1), lr_node('1', 2))
    graph2 = rnr_graph() \
        .add_edge(lr_node('1', 1), lr_node(2, 1)) \
        .add_node(lr_node('1', 2))
    dot1 = convert_graph(graph1, '1')
    dot2 = convert_graph(graph2, '2')

    dot_for_print = print_together(dot1, dot2, names=['Before_changes', 'After_changes'])

    dot_for_print.add_edge(pydot.Edge('0_1__1', '0_1__2', style='dashed'))
    dot_for_print.add_edge(pydot.Edge('1_1__1', '1_1__2', style='dashed'))
    dot_for_print.add_edge(pydot.Edge('1_2__1', '1_2__2', style='dashed'))
    dot_for_print.add_edge(pydot.Edge('2_1__1', '2_1__2', style='dashed'))

    dot_for_print.write(path=name + '.png', format='png')


def block_to_graph():
    name = 'block_to_graph'

    workflow = Workflow()
    b1 = Block(operation=Operation("Block Name", ['json'], ["json", "html"]))
    workflow.add_block(b1)

    graph = CompleteWorkflowToGraphConverter().convert(workflow)

    dot_workflow = WorkflowToDotConverter(separator='1').convert_workflow(workflow)
    dot_graph = convert_graph(graph, '2')

    # dot_for_print = print_together(dot_workflow, dot_graph, names=["workflow", "graph"])

    dot_workflow.write(path=name + '1' + '.png', format='png')
    dot_graph.write(path=name + '2' + '.png', format='png')


def to_acyclic():
    name = 'to_acyclic'
    graph1 = rnr_graph() \
        .add_edge(lr_node(1, 1), lr_node(2, 1)) \
        .add_edge(lr_node(2, 1), lr_node(3, 1)) \
        .add_edge(lr_node(3, 1), lr_node(1, 1))
    graph2 = rnr_graph() \
        .add_edge(lr_node(1, 1), lr_node('1_2', 1)) \
        .add_edge(lr_node(2, 1), lr_node('1_2', 1)) \
        .add_edge(lr_node(2, 1), lr_node('2_3', 1)) \
        .add_edge(lr_node(3, 1), lr_node('2_3', 1)) \
        .add_edge(lr_node(3, 1), lr_node('3_1', 1)) \
        .add_edge(lr_node(1, 1), lr_node('3_1', 1))
    dot1 = convert_graph(graph1, '1')
    dot2 = convert_graph(graph2, '2')

    dot_for_print = print_together(dot1, dot2, names=['first_graph', 'second_graph'])
    dot_for_print.write(path=name + '.png', format='png')


def classic_workflow():
    name = 'classic_workflow'

    workflow = Workflow()
    blocks = []
    blocks.append(Block(Operation('Получаем пул для обучения из FML', [], ['2'])))
    blocks.append(Block(Operation('Загружаем данные для обучения', ['2'], ['1'])))
    blocks.append(Block(Operation('Делаем выборку для обучения', ['1'], ['1'])))
    blocks.append(Block(Operation('Делаем выборку для теста', ['1'], ['3'])))
    blocks.append(Block(Operation('Получаем пул для валидации из FML', [], ['2'])))
    blocks.append(Block(Operation('Загружаем данные для валидации', ['2'], ['1'])))
    blocks.append(Block(Operation('Создаем утилиту для оценки качества', [], ['3'])))
    blocks.append(Block(Operation('Обучаем Матрикснет', ['1', '3'], ['4'])))
    blocks.append(Block(Operation('Запускаем оценку качества формулы', ['3', '1', '4'], ['5'])))

    for block in blocks:
        workflow.add_block(block)

    workflow.add_connection_by_data(blocks[0], 1, '2', blocks[1], 1, '2')
    workflow.add_connection_by_data(blocks[1], 1, '1', blocks[2], 1, '1')
    workflow.add_connection_by_data(blocks[1], 1, '1', blocks[3], 1, '1')
    workflow.add_connection_by_data(blocks[2], 1, '1', blocks[7], 1, '1')
    workflow.add_connection_by_data(blocks[3], 1, '3', blocks[7], 1, '3')
    workflow.add_connection_by_data(blocks[4], 1, '2', blocks[5], 1, '2')
    workflow.add_connection_by_data(blocks[5], 1, '1', blocks[8], 1, '1')
    workflow.add_connection_by_data(blocks[6], 1, '3', blocks[8], 1, '3')
    workflow.add_connection_by_data(blocks[7], 1, '4', blocks[8], 1, '4')

    dot = WorkflowToDotConverter().convert_workflow(workflow)
    dot.set_splines(False)

    dot.write(path=name + '.png', format='png')


def classic_workflow_diff():
    name = 'classic_workflow_diff'

    workflow = Workflow()
    blocks = []
    blocks.append(Block(Operation('Получаем пул для обучения из FML', [], ['2'])))
    blocks.append(Block(Operation('Загружаем данные для обучения', ['2'], ['1'])))
    blocks.append(Block(Operation('Делаем выборку для обучения', ['1'], ['1'])))
    blocks.append(Block(Operation('Делаем выборку для теста', ['1'], ['3'])))
    blocks.append(Block(Operation('Получаем пул для валидации из FML', ['6'], ['2'])))
    blocks.append(Block(Operation('Загружаем данные для валидации', ['2'], ['1'])))
    blocks.append(Block(Operation('Создаем утилиту для оценки качества', [], ['3'])))
    blocks.append(Block(Operation('Обучаем Матрикснет', ['1', '3'], ['4'])))
    blocks.append(Block(Operation('Запускаем оценку качества формулы', ['3', '1', '4'], ['5'])))

    for block in blocks:
        workflow.add_block(block)

    workflow.add_block(Block(Operation('Установление соединения с пулом', [], ['6'])))

    workflow.add_connection_by_data(blocks[0], 1, '2', blocks[1], 1, '2')
    workflow.add_connection_by_data(blocks[1], 1, '1', blocks[2], 1, '1')
    workflow.add_connection_by_data(blocks[1], 1, '1', blocks[3], 1, '1')
    workflow.add_connection_by_data(blocks[2], 1, '1', blocks[7], 1, '1')
    workflow.add_connection_by_data(blocks[3], 1, '3', blocks[7], 1, '3')
    workflow.add_connection_by_data(blocks[4], 1, '2', blocks[5], 1, '2')
    workflow.add_connection_by_data(blocks[5], 1, '1', blocks[8], 1, '1')
    workflow.add_connection_by_data(blocks[6], 1, '3', blocks[8], 1, '3')
    workflow.add_connection_by_data(blocks[7], 1, '4', blocks[8], 1, '4')

    workflow.add_connection_by_data(Block(Operation('Установление соединения с пулом', [], ['6'])), 1, '6', blocks[4],
                                    1, '6')

    workflow_update = Workflow()

    for block in blocks:
        workflow_update.add_block(block)
    workflow_update.add_block(Block(Operation('Неиспользуемые данные', [], ['2'])))
    workflow_update.add_block(Block(Operation('Неиспользуемые данные', [], ['2'])))

    workflow_update.add_connection_by_data(blocks[0], 1, '2', blocks[1], 1, '2')
    workflow_update.add_connection_by_data(blocks[1], 1, '1', blocks[2], 1, '1')
    workflow_update.add_connection_by_data(blocks[1], 1, '1', blocks[3], 1, '1')
    workflow_update.add_connection_by_data(blocks[2], 1, '1', blocks[7], 1, '1')
    workflow_update.add_connection_by_data(blocks[3], 1, '3', blocks[7], 1, '3')
    workflow_update.add_connection_by_data(blocks[4], 1, '2', blocks[5], 1, '2')
    workflow_update.add_connection_by_data(blocks[5], 1, '1', blocks[8], 1, '1')
    workflow_update.add_connection_by_data(blocks[6], 1, '3', blocks[8], 1, '3')
    workflow_update.add_connection_by_data(blocks[7], 1, '4', blocks[8], 1, '4')
    workflow_update.add_connection_by_data(blocks[7], 1, '4', blocks[8], 1, '4')

    workflow_update.add_connection_by_data(Block(Operation('Неиспользуемые данные', [], ['2'])), 1, '2', blocks[1], 1,
                                           '2')
    workflow_update.add_connection_by_data(Block(Operation('Неиспользуемые данные', [], ['2'])), 2, '2', blocks[1], 1,
                                           '2')

    Pipeline(algorithm=BaselineAlgorithm(), workflow_converter=CompleteWorkflowToGraphConverter()).print_diff(
        workflow_update, workflow, path=name + '.png')


print_images(*abstract_problem())
print_images(*np_complete())
block_to_graph()
to_acyclic()
classic_workflow()
classic_workflow_diff()
score_problem()
isomorphism()
