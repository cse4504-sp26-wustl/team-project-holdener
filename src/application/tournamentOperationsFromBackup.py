from application.tournamentOperations import TournamentOperations
from domain.player import Player
from domain.tournamentRound import TournamentRound

class TournamentOperationsFromBackup(TournamentOperations):
    def __init__(self, players: list[Player], rounds: list[TournamentRound]):
        super().__init__(players)
        self.all_rounds = rounds
        game_count = 0
        for r in rounds:
            game_count += len(r.get_games())
        self.next_game_id = game_count + 1
