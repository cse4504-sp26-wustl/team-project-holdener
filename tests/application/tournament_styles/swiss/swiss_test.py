import pytest
from domain.scoreCard import ScoreCard
from domain.player import Player
from domain.gameColor import GameColor
from application.tournament_styles.swiss.swiss import Swiss
class TestSwiss:
    @pytest.fixture(autouse=True)
    def init_players(self):
        self.players = []
        for i in range(0,10):
            self.players.append(Player(str(i), str(i), i, i))

    def test_make_pair(self):
        card1 = ScoreCard(self.players[0])
        card2 = ScoreCard(self.players[1])
        card1.add_opponent(self.players[2], GameColor.BLACK)
        card2.add_opponent(self.players[3], GameColor.WHITE)
        swiss = Swiss()
        white, black = swiss.make_pair(card1, card2)
        assert(white == self.players[1].id)
        assert(black == self.players[0].id)