import pytest
from unittest.mock import MagicMock, patch
import sys
import os
from application.tournamentOperations import TournamentOperations
from domain.player import Player
from domain.gameOutcome import GameOutcome
from domain.gamePoints import GamePoints


class TestTournamentOperations:
    @pytest.fixture
    def mock_db(self):
        """Fixture to mock a database connection or file handler."""
        return MagicMock()

    @pytest.fixture
    def players(self):
        all_players = []
        for i in range(0, 6):
            all_players.append(Player("Kate"+str(i), "Holdener"+str(i), str(i), i*100))
        return all_players
    
    def test_first_round(self, players):
        """Test generating the first round of the swiss tournament"""
        # Arrange
        tournament_ops = TournamentOperations(players)

        # Act
        round1 = tournament_ops.generate_next_round()

        # Assert
        assert(len(round1.get_games()) == 3)

        # assert result["name"] == tournament_name
        # assert len(result["participants"]) == 3
        pass

    def test_generate_score_cards(self, players):
        # Arrange
        tournament_ops = TournamentOperations(players)
        round1 = tournament_ops.generate_next_round()
        games = round1.get_games()
        for game in games:
            game.set_outcome(GameOutcome.WHITE_WIN)
        # Act
        score_cards = tournament_ops.build_cards()

        # Assert
        assert(len(score_cards) == len(players))
        white_players = []
        black_players = []
        for game in games:
            white_players.append(game.white.id)
            black_players.append(game.black.id)
        for card in score_cards.values():
            if card.id in white_players:
                assert(card.get_total_score() == GamePoints.WIN.value)
            if card.id in black_players:
                assert(card.get_total_score() == GamePoints.LOSE.value)        

    def test_generate_2nd_round_white_black_draw(self, players):
        tournament_op = TournamentOperations(players)
        round1 = tournament_op.generate_next_round()
        games = round1.get_games()
        games[0].set_outcome(GameOutcome.WHITE_WIN)
        games[1].set_outcome(GameOutcome.BLACK_WIN)
        games[2].set_outcome(GameOutcome.DRAW)
        round2 = tournament_op.generate_next_round()
        assert(len(round2.get_games()) == 3)

    def test_generate_2nd_round_white_white_draw(self, players):
        tournament_op = TournamentOperations(players)
        round1 = tournament_op.generate_next_round()
        games = round1.get_games()
        games[0].set_outcome(GameOutcome.WHITE_WIN)
        games[1].set_outcome(GameOutcome.WHITE_WIN)
        games[2].set_outcome(GameOutcome.DRAW)
        round2 = tournament_op.generate_next_round()
        assert(len(round2.get_games()) == 3)

    def test_generate_2nd_round_black_black_draw(self, players):
        tournament_op = TournamentOperations(players)
        round1 = tournament_op.generate_next_round()
        games = round1.get_games()
        games[0].set_outcome(GameOutcome.BLACK_WIN)
        games[1].set_outcome(GameOutcome.BLACK_WIN)
        games[2].set_outcome(GameOutcome.DRAW)
        round2 = tournament_op.generate_next_round()
        assert(len(round2.get_games()) == 3)