from typing import List
from domain.player import Player
from domain.tournamentRound import TournamentRound
from domain.gameOutcome import GameOutcome
from domain.game import Game

class TournamentOperations:
    def __init__(self, players: List[Player]):
        self.all_rounds = []
        self.all_players = players
        self.next_game_id = 1
    def generate_next_round(self) -> TournamentRound:
        next_round = TournamentRound()
        self.all_rounds.append(next_round)
        for i in range(0, len(self.all_players),2):
            game = Game(self.next_game_id, self.all_players[i], self.all_players[i+1])
            next_round.add_game(game, self.next_game_id)
            self.next_game_id += 1
        return next_round
        
    def set_outcome(self, gameId: int, result: GameOutcome):
        game = self._find_game(gameId)
        if game:
            game.set_outcome(result)
        else:
             raise ValueError(f"Game {gameId} not found")

    def switch_sides(self, game_id):
        game = self._find_game(game_id)
        if game:
            game.switch_sides()
        else:
            raise ValueError(f"Game {game_id} not found")

    def get_games(self, round_number: int) -> List[Game]:
        return self.all_rounds[round_number].get_games()

    def _find_game(self, game_id: int):
        for t_round in self.all_rounds:
            game = t_round.get_game(game_id)
            if game:
                 return game
        return None
