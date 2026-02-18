from domain.game import Game

class TournamentRound:
    def __init__(self):
        self.games = {}

    def add_game(self, game: Game, game_id: int):
        self.games[game_id] = game

    def get_game(self, game_id: int):
        if game_id in self.games:
            return self.games[game_id]
        return None

    def get_games(self) -> list[Game]:
        return list(self.games.values())

    def to_dict(self):
        dict_obj = {}
        dict_obj["games"] = []
        games = self.get_games()
        for game in games:
            dict_obj["games"].append(game.to_dict())
        return dict_obj
