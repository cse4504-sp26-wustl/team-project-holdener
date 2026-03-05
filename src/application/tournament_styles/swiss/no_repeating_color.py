from domain.scoreCard import ScoreCard
from domain.gameColor import GameColor
def no_repeating_color(card1: ScoreCard, card2: ScoreCard) -> bool:
    # look at the last color played in each card
    # if they are the same (card1's last color is same as card2's last color)
    # then one of the cards will have to repeat
    color1 = card1.get_last_color()
    color2 = card2.get_last_color()
    if color1 == color2 and color1 != GameColor.NONE:
        return False
    return True