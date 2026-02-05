import uuid
from domain.gameOutcome import GameOutcome
from domain.player import Player

class Game:
    def __init__(self, white: Player, black: Player):
        self.id = uuid.uuid4() 
        self.white = white
        self.black = black
        self.outcome = GameOutcome.NONE
        pass

    def setGameOutcome(self, outcome: GameOutcome):
        pass

    def to_dict(self):
        dict_obj = self.__dict__.copy()
        dict_obj["white"] = self.white.to_dict()
        dict_obj["black"] = self.black.to_dict()
        return dict_obj
