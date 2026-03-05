from domain.scoreCard import ScoreCard
def no_repeat_opponents(card1: ScoreCard, card2: ScoreCard) -> bool:
    if card1.id in card2.opponents or card2.id in card1.opponents:
        return False
    return True