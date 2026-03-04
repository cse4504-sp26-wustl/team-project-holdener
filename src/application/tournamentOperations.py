from typing import List
from domain.player import Player
from domain.tournamentRound import TournamentRound
from domain.gameOutcome import GameOutcome
from domain.gamePoints import GamePoints
from domain.game import Game
from domain.scoreCard import ScoreCard
from application.tournament_styles.py4swiss.py_4swiss_adapter import Py4SwissAdapter

class TournamentOperations:
    def __init__(self, players: List[Player]):
        self.all_rounds = []
        self.players = {}
        self.all_players = sorted(players, key=lambda player: player.rating, reverse=True)
        self.next_game_id = 1
        self.format = Py4SwissAdapter()
        for p in players:
            self.players[p.id] = p

    def pair_players_in_group(self, group: List[Player]) -> List[Game]:
        pass

    def build_cards(self)->dict[ScoreCard]:
        cards = {}
        for player in self.all_players:
            cards[player.id] = ScoreCard(player)
        for round in self.all_rounds:
            # first, update score cards with byes
            for bye in round.byes:
                cards[bye.id].add_score(GameOutcome.BYE)

            for game in round.get_games():
                cards[game.white.id].add_opponent(game.black, 0)
                cards[game.black.id].add_opponent(game.white, 1)
                if game.outcome == GameOutcome.WHITE_WIN:
                    cards[game.white.id].add_score(GamePoints.WIN)
                    cards[game.black.id].add_score(GamePoints.LOSE)
                elif game.outcome == GameOutcome.BLACK_WIN:
                    cards[game.black.id].add_score(GamePoints.WIN)
                    cards[game.white.id].add_score(GamePoints.LOSE)
                elif game.outcome == GameOutcome.DRAW:
                    cards[game.white.id].add_score(GamePoints.DRAW)
                    cards[game.black.id].add_score(GamePoints.DRAW)
        return cards
    
    def generate_next_round(self) -> TournamentRound:
        cards = self.build_cards()
        pairs = self.format.get_next_round(list(cards.values()))
        next_round = TournamentRound()
        for pair in pairs:
            game = Game(self.next_game_id, self.players[pair[0]], self.players[pair[1]])
            next_round.add_game(game, self.next_game_id)
            self.next_game_id+= 1
        self.all_rounds.append(next_round)
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
