class RoomException(Exception):
    """Base exception for room models"""


class GameCreationException(Exception):
    """Raised when game cannot be created"""


class GameActionException(Exception):
    """Raised when game action cannot be acted"""
