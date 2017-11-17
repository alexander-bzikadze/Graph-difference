from abc import ABC, abstractmethod

from graph_diff.nirvana_object_model.block import Block


class GraphDotColorer(ABC):
    @abstractmethod
    def color_of_block(self,
                       block: Block,
                       number: int): pass

    @abstractmethod
    def color_data_connection(self,
                              from_block: Block,
                              from_number: int,
                              output_nest: str,
                              to_block: Block,
                              to_number: int,
                              input_nest: str): pass

    @abstractmethod
    def color_exc_connection(self,
                             from_block: Block,
                             from_number: int,
                             to_block: Block,
                             to_number: int): pass


class StandardGraphDotColorer(GraphDotColorer):
    def color_of_block(self,
                       block: Block,
                       number: int): return 'black'

    def color_data_connection(self,
                              from_block: Block,
                              from_number: int,
                              output_nest: str,
                              to_block: Block,
                              to_number: int,
                              input_nest: str): return 'black'

    def color_exc_connection(self,
                             from_block: Block,
                             from_number: int,
                             to_block: Block,
                             to_number: int): return 'black'


class GraphMapDotColorer:
    def __init__(self, block_colors, data_connection_colors, exc_connection_colors):
        self._block_colors = block_colors
        self._data_connection_colors = data_connection_colors
        self._exc_connection_colors = exc_connection_colors

    def color_of_block(self,
                       block: Block,
                       number: int):
        return self._block_colors[block, number]

    def color_data_connection(self,
                              from_block: Block,
                              from_number: int,
                              output_nest: str,
                              to_block: Block,
                              to_number: int,
                              input_nest: str):
        return self._data_connection_colors[from_block, from_number, output_nest, to_block, to_number, input_nest]

    def color_exc_connection(self,
                             from_block: Block,
                             from_number: int,
                             to_block: Block,
                             to_number: int):
        return self._exc_connection_colors[from_block, from_number, to_block, to_number]
