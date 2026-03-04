from application.tournament_styles.py4swiss.scorecards_to_parsed_trf import scorecards_to_parsed_trf
#from py4swiss.engines.dutch.engine import Engine
from py4swiss.engines.dutch.engine import Engine
from domain.scoreCard import ScoreCard

class Py4SwissAdapter:
    def get_next_round(self, cards: list[ScoreCard] ) -> list[(int, int)]:
        parsedTrf = scorecards_to_parsed_trf(cards, "my tournament", 3)
        my_engine = Engine()
        pairs = my_engine.generate_pairings(parsedTrf)
        print(pairs)
        return [(str(pairing.white), str(pairing.black)) for pairing in pairs]