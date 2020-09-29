class RoomException(Exception):
    """Base exception for room models"""


class RoomCommandException(RoomException):
    """Raised when room command cannot be applied"""


class GameCreationException(RoomException):
    """Raised when game cannot be created"""


class GameActionException(RoomException):
    """Raised when game action cannot be acted"""
