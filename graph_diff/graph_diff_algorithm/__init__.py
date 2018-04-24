"""
Module containing interface for graph difference algorithms.
The result of this algorithms is also described here - GraphMap.
Different comparators used for comparison GraphMap objects are also defined.
"""

from .compose_graph_diff_algorithm import ComposedGraphDiffAlgorithm
from .graph_diff_algorithm import GraphDiffAlgorithm, GraphDiffAlgorithmWithInit
from .graph_map import GraphMap
from .graph_map_comparator import *
