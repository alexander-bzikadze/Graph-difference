# Checks graphs on being isomorphic.
# g1, g2 - dict of lists (graph)
def naive_eq(g1, g2):
	from src_depricated.diff_construct import diff_construct
	# Max number of nodes in g1, g2.
	N = max([len(gr.keys()) for gr in [g1, g2] ])
	# Max number of edges in g1, g2.
	M = max([len([edge for _,edge_list in gr.items() for edge in edge_list]) for gr in [g1, g2] ])
	return (M, N) == diff_construct(g1, g2)[1]