class Operation:
    def __init__(self,
                 operationId: str,
                 inputs: tuple=(),
                 outputs: tuple=()):
        self.operationId = operationId
        self.inputs = inputs
        self.outputs = outputs

    def __hash__(self) -> int:
        return hash(self.operationId) ^ hash(self.inputs) ^ hash(self.outputs)
