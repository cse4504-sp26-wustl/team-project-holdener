from enum import Enum
class GameOutcome(str, Enum):
    NONE = " "
    WHITE_WIN = "white win"
    BLACK_WIN = "black win"
    DRAW = "draw"
    FORCED_BYE = "forced bye"
    REQUESTED_BYE = "requested bye"
