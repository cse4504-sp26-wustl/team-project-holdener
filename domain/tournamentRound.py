from domain.game import Game

class TournamentRound:
    def __init__(self):
        self.games = []

    def add_game(self, game: Game):
        self.games.append(game)

    def to_dict(self):
        dict_obj = {}
        dict_obj["games"] = []
        for game in self.games:
            dict_obj["games"].append(game.to_dict())
        return dict_obj