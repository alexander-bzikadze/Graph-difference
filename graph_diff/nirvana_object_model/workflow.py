from graph_diff.nirvana_object_model.block import Block
from collections import defaultdict


class Workflow:
    def __init__(self):
        self._blocks = []
        self._connections_by_execution = defaultdict(set)
        self._connections_by_data = defaultdict(set)

    def add_block(self, new_block: Block):
        self._blocks.append(new_block)
        return self

    def add_connection_by_execution(self, from_block: Block, to_block: Block):
        assert from_block in self._blocks
        assert to_block in self._blocks
        self._connections_by_execution[from_block].add(to_block)
        return self

    def add_connection_by_data(self, from_block: Block, output_nest: str, to_block: Block, input_nest: str):
        assert from_block in self._blocks
        assert to_block in self._blocks
        assert output_nest in from_block.operation.outputs
        assert input_nest in to_block.operation.inputs
        self._connections_by_data[from_block, output_nest].add(to_block, input_nest)
