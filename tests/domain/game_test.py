import pytest
from domain.game import Game
from domain.gameOutcome import GameOutcome
from domain.player import Player

class TestGame():
    @pytest.fixture(autouse=True)
    def setup(self):
        self.white = Player("a", "b", "ab123", 100)
        self.black = Player("x", "y", "xy123", 200)
        self.game = Game(1, self.white, self.black)

    def test_switch_sides(self):
        self.game.switch_sides()
        assert(self.game.white == self.black)
        assert(self.game.black == self.white)

    def test_set_outcome(self):
        self.game.set_outcome(GameOutcome.WHITE_WIN)
        assert (self.game.outcome == GameOutcome.WHITE_WIN)