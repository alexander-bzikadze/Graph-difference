import abc


class BaseGraph(abc.ABC):
    @abc.abstractmethod
    def add_edge(self, from_node: (int, int), to_node: (int, int)): pass

    @abc.abstractmethod
    def add_node(self, new_node: (int, int)): pass

    @abc.abstractmethod
    def get_list_of_adjacent_nodes(self, node: (int, int)) -> [(int, int)]: pass

    @abc.abstractmethod
    def get_list_of_nodes(self) -> [(int, int)]: pass

    @abc.abstractmethod
    def get_list_of_edges(self) -> [((int, int), (int, int))]: pass
