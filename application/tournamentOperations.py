from typing import List
from domain.player import Player
from domain.tournamentRound import TournamentRound
from domain.gameOutcome import GameOutcome
from domain.game import Game

class TournamentOperations:
    def __init__(self, players: List[Player]):
        self.all_rounds = []
        self.all_players = players

    def generate_next_round(self) -> TournamentRound:
        next_round = TournamentRound()
        self.all_rounds.append(next_round)
        for i in range(0, len(self.all_players),2):
            game = Game(self.all_players[i], self.all_players[i+1])
            next_round.add_game(game)
        return next_round
        
    def set_outcome(self, gameId: int, result: GameOutcome):
        pass

    def update_game(self, gameId, white: Player, black: Player, outcome: GameOutcome):
        pass
