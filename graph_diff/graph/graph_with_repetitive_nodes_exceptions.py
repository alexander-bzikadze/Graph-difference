class GraphWithRepetitiveNodesKeyError(Exception):
    def __init__(self, message):
        self.message = message


class LabeledRepetitiveNodePositiveArgumentException(Exception):
    def __init__(self, message):
        self.message = message
