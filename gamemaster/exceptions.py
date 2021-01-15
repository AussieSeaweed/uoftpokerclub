class GameMasterException(Exception):
    pass


class GameCreationException(GameMasterException):
    pass


class SeatNotFoundException(GameMasterException):
    pass


class NoEmptySeatException(GameMasterException):
    pass
