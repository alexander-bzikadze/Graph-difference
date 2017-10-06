# Constructs diff between graphs.
# Return best match between them and its score.
# Algorithm is naive.
# g1_or, g2_or - dict of lists (graph)
def diff_construct(g1_or, g2_or):
	g1, g2 = split_graph_by_labels(g1_or), split_graph_by_labels(g2_or)
	extend_graphs(g1, g2)
	g1, g2 = add_zero_nodes(g1, g2)

	# min score.
	# edge_metric - number of matched edges.
	# node_metric - numer of matched nodes.
	best = {}
	score = (0, 0)
	for g1_to_g2 in graph_maps(g1, g2):
		node_metric = 0
		edge_metric = 0
		for node, li in g1_or.items():
			# If 0 in num of one of the nodes, it means that there is no match for another.
			if node.split("_")[1] == "0" or g1_to_g2[node].split("_")[1] == "0":
				continue
			node_metric += 1
			edge_metric += sum([int(g1_to_g2[to_node] in g2_or[g1_to_g2[node]]) for to_node in li])
		if (edge_metric, node_metric) > score:
			best = g1_to_g2
			score = (edge_metric, node_metric)

	return best, score

# Creates a copy of gr that is splitted by value of the node's labels.
# gr - dict of lists (graph)
def split_graph_by_labels(gr):
	from collections import defaultdict
	res = defaultdict(list)
	for num,_ in gr.items():
		num = str(num)
		# transform num to label_number format
		num = num if "_" in num else num + "_1"
		label, number = num.split("_")
		# dict from label to list of number of node in graph.
		res[int(label)].append((int(number)))
	return res;

# Extend graph with new nodes to have nodes woth all labels in interval (0, m + 1)
# m = max(labels(g1), labels(g2))
# g1, g2 - dict of lists of pairs (graph)
def extend_graphs(g1, g2):
	if len(g1.keys()) == 0 and len(g2.keys()) == 0:
		return
	m = max(max(g1.keys()), max(g2.keys()))
	for i in range(1, m + 1):
		if i not in g1.keys():
			g1[i] = [1]
		if i not in g2.keys():
			g2[i] = [1]

# Adds zero-numed nodes to labels in order to have the ability 
# to match nodes from g2 with "not" nodes from g1.
# g1, g2 - dict of lists of pairs (graph)
def add_zero_nodes(g1, g2):
	# Returns new list that for each label has n nodes from g1 and m 0-nodes, 
	# where m is number of nonzero nodes under label questioned.
	def add_zero_nodes_helper(g1, g2):
		return { label1: (l1 + [0] * len([ num for num in g2[label1] if num != 0 ])) for label1, l1 in g1.items() }
	return add_zero_nodes_helper(g1, g2), add_zero_nodes_helper(g2, g1)

# Returns all possible matches between nodes of the graphs. 
# Including not matching node with any node from another graph.
# g1, g2 - dict of lists of pairs (graph)
def graph_maps(g1, g2):
	from itertools import product

	# Returns all possible maps from g1 to g2 for each label without duplicated and mapping zero node to zero node.
	# It is important, that mapping are for labels.
	def graph_maps_for_each_label(g1, g2):
		# Map permutations to l1
		def permuts(l1):
			from itertools import permutations
			return [list(l) for l in permutations(l1)]

		# Removing any duplicates from l1
		# list(set()) conversion does not work for hashiable types.
		def remove_dupli(l1):
			res = []
			for elem in l1:
				if elem not in res:
					res.append(elem)
			return res

		# zip(sorted(g1.items()), sorted(g2.items())) guarantees, that 
		# if extend_graph func was applied to g1, g2, label1 == label2.
		# That is why only label1 is taken as label.
		return { label: remove_dupli({ k: v for k, v in zip(lr1, lr2) if k != 0 or v != 0}
									for lr1,lr2 in product(permuts(l1), permuts(l2))) 
				for (label, l1), (_, l2) in zip(sorted(g1.items()), sorted(g2.items())) }

	# Products maps for all labels into one map.
	# The result is tuple(dict, tuple(dict, t... (dict,dict))) structure of maps from g1 to g2.
	def produce_all_possible_maps(g1_to_g2_for_each_label):
		from functools import reduce
		if len(g1_to_g2_for_each_label) == 0:
			return {}
		return reduce(product, 
			[ [{str(label) + "_" + str(num1): str(label) + "_" + str(num2) for num1, num2 in gmap.items()} 
					for gmap in gmap_list ] 
				for label, gmap_list in g1_to_g2_for_each_label.items() ])
		
	print (list(produce_all_possible_maps(graph_maps_for_each_label(g1, g2))))

	l = list(produce_all_possible_maps(graph_maps_for_each_label(g1, g2)))
	if len(l) == 1:
		return l

	for l in produce_all_possible_maps(graph_maps_for_each_label(g1, g2)):
		for x in l:
			print(x)


	# Sums tuple(dict, tuple(dict, t...)) to one dict.
	return [ dict(sum( [ list(x.items()) for x in l], [] ) ) for l in produce_all_possible_maps(graph_maps_for_each_label(g1, g2))]








