import numpy as np

from graph_diff.nirvana_object_model.block import Block


class Workflow:
    def __init__(self):
        self._blocks = np.array([], Block)
        self._connections = {}

    def set_blocks_size(self, size: int):
        self._blocks.resize(size)

    def set_blocks(self, iterable):
        if len(iterable) > self._blocks.size:
            raise Exception("Size of incoming iterable bigger then inner block size.")
        for i, a in enumerate(iterable):
            self._blocks[i] = a

    BY_COMPLETING_CONNECTION = "by_completion_connection"

    def add_connection(self, first: int, output_nest: str, second: int, input_nest: str):
        if output_nest == Workflow.BY_COMPLETING_CONNECTION or input_nest == Workflow.BY_COMPLETING_CONNECTION:
            assert output_nest == input_nest
        assert output_nest in self._blocks[first].operation.exits
        assert input_nest in self._blocks[second].operation.entrances
        self._connections[(first, output_nest)] = second, input_nest
