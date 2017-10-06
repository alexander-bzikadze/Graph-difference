class GraphWithRepetitiveNodesInputFormatException(Exception):
    def __init__(self, message):
        self.message = message


class GraphWithRepetitiveNodesKeyError(Exception):
    def __init__(self, message):
        self.message = message
