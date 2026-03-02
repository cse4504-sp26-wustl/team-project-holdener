from enum import Enum
class GameColor(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

def oppositeColor(side: GameColor) -> GameColor:
    if side == GameColor.BLACK:
        return GameColor.WHITE
    elif side == GameColor.WHITE:
        return GameColor.BLACK
    return GameColor.NONE