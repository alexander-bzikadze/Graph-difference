def py_to_dot_converter(gr):
	import pydot
	dot = pydot.Dot(graph_type='digraph')

	for node in gr.keys():
		a = pydot.Node(node, label=str(node).split("_")[0])
		dot.add_node(a)
		a.set_shape('circle')

	for node, edges in gr.items():
		for edge in edges:
			dot.add_edge(pydot.Edge(node, edge))

	return dot
