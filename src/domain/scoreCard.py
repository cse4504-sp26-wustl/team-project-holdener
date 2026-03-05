from domain.gamePoints import GamePoints
from domain.gameColor import GameColor, oppositeColor
from domain.player import Player
from domain.gameOutcome import GameOutcome
class ScoreCard:
    def __init__(self, player: Player):
        self.scores = []
        self.outcomes = []
        self.id = player.id
        self.rating = player.rating
        self.opponents = []
        self.sides = []

    def add_outcome(self, outcome: GameOutcome):
        self.outcomes.append(outcome)

    def add_score(self, score: GamePoints):
        self.scores.append(score)

    def has_bye(self, round: int) -> bool:
        if len(self.scores) < round:
            return False
        else:
            return self.scores[round] == GamePoints.BYE
        
    def get_total_score(self) -> float:
        total = 0
        for score in self.scores:
            total = total+score.value
        return total
    
    def add_opponent(self, player: Player, side: GameColor):
        """
        player - the opponent in a specific game
        side - the color of the opponent
        """
        self.opponents.append(player.id)
        self.sides.append(oppositeColor(side))

    def get_last_color(self):
        if len(self.sides) == 0:
            return GameColor.NONE
        else:
            return self.sides[-1]

