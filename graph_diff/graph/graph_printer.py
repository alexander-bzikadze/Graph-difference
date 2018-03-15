from graph_diff.graph import GraphWithRepetitiveNodesWithRoot


def print_graph(graph: GraphWithRepetitiveNodesWithRoot):
    out = []
    out.append(str(len(graph)))
    for node in graph:
        out.append('{} {}'.format(node.Label, node.Number))
    node_to_index = {node: str(i) for i, node in enumerate(graph)}
    for node in graph:
        out.append(str(len(graph.get_list_of_adjacent_nodes(node))))
        for to_node in graph.get_list_of_adjacent_nodes(node):
            out.append(node_to_index[to_node])
    return out
