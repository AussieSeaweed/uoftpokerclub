class SOSException(Exception):
    def __init__(self):
        super().__init__(self.__doc__)


class UnregisteredModelException(SOSException):
    """The model is not registered as a live model."""
    pass
