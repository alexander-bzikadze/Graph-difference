class Operation:
    def __init__(self,
                 operation_id: str,
                 inputs=(),
                 outputs=()):
        self.operation_id = operation_id
        self.inputs = tuple(inputs)
        self.outputs = tuple(outputs)

    def __hash__(self) -> int:
        return hash(self.operation_id) ^ hash(self.inputs) ^ hash(self.outputs)

    def __eq__(self, other):
        return other.operation_id == self.operation_id\
            and self.inputs == other.inputs\
            and self.outputs == other.outputs
