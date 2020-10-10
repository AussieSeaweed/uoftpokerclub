class RoomException(Exception):
    """Base exception for room models"""


class GameCreationException(RoomException):
    """Raised when game cannot be created"""


class GameActionException(RoomException):
    """Raised when game action cannot be acted"""
