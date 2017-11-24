from graph_diff.nirvana_object_model.operation import Operation


class Block:
    def __init__(self, operation: Operation, options=None):
        if options is None:
            options = {}
        self.operation = operation
        self.options = tuple(sorted(options.items())) if type(options) is dict else tuple(sorted(options))

    def __hash__(self):
        return hash(self.operation) ^ hash(self.options)

    def __eq__(self, other):
        return self.options == other.options and self.operation == other.operation
