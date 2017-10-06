from src.py_to_dot_converter import py_to_dot_converter
g1 = getattr(__import__("graph_examples_py.g5", fromlist=["gr"]), "gr")
g2 = getattr(__import__("graph_examples_py.g4", fromlist=["gr"]), "gr")

from src.diff_construct import diff_construct
print(diff_construct(g1, g2))

from src.naive_eq import naive_eq
print(naive_eq(g1, g2))



# diff_construct({"1_1":[]}, {"1_1":[]})