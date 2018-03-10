class GraphDoesNotContainMappedNodeException(Exception):
    """
    Exception to be thrown GraphMap.
    Indicates that node is mapped to nonexistent node.
    """

    def __init__(self, message):
        self.message = message
