"""
Module dedicated to graph difference problem.

graph_diff_algorithm contains interfaces
and common for any algorithm parts such as class for result - GraphMap.

Other *_algorithm modules describe different algorithms.
All of them are realization of one interface.
Some of the algorithms are exact, some heuristic.
If you don't know what to use, use baseline for very small graphs
and new ant for larger (this will not get you exact answer).

Graph module describes graph representation needed to perform algorithms.
This representation mostly intuitive
but one must know that graphs are represented as rooted.
If you do not intend to have rooted graph just ignore that fact
otherwise you may use it as an advantage.
Root is marked with label 0 and this label
is supposed not to be had any other node.

Nirvana object model contains code connected to nirvana workflow comparison.
Nirvana is non specialized cloud platform for computing processes management.
It allows to describe these processes as graphs where nodes are some operations
and edges describe connections of the results of one operations
with another one's input data.
It is solved through transformation workflow to graph,
solving graph difference problem and reverse transformation.
The usage of the module is highly recommended through the Pipeline class.
When constructing it you may specify way of transformation of the workflow,
algorithm to be used, etc.
"""

# import graph_diff.ant_algorithm
# import graph_diff.baseline_algorithm
# import graph_diff.baseline_with_chop_algorithm
# import graph_diff.graph
# import graph_diff.graph_diff_algorithm
# import graph_diff.new_ant_algorithm
# import graph_diff.nirvana_object_model
# import graph_diff.simulated_annealing_algorithm
