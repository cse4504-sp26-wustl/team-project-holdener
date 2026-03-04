from enum import Enum
class GameOutcome(Enum):
    NONE = 0
    WHITE_WIN = 1
    BLACK_WIN = 2
    DRAW = 3
    FORCED_BYE = 4
    REQUESTED_BYE = 5
