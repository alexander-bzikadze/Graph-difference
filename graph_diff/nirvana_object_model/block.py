from graph_diff.nirvana_object_model.operation import Operation


class Block:
    def __init__(self, operation: Operation, options: dict):
        self.operation = operation
        self.options = options
