from domain.gameOutcome import GameOutcome
from domain.player import Player

class Game:
    def __init__(self, game_id: int, white: Player, black: Player):
        self._id = game_id 
        self.white = white
        self.black = black
        self.outcome = GameOutcome.NONE
        pass

    def switch_sides(self):
        black = self.black
        self.black = self.white
        self.white = black

    def set_outcome(self, outcome: GameOutcome):
        self.outcome = outcome

    def to_dict(self):
        dict_obj = {}
        dict_obj["id"] = self._id
        dict_obj["outcome"] = self.outcome
        dict_obj["white"] = self.white.to_dict()
        dict_obj["black"] = self.black.to_dict()
        return dict_obj
