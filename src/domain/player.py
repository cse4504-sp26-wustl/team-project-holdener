from domain.gamePoints import GamePoints
class Player:
    def __init__(self, firstName: str, lastName: str, uscfId: str, rating=None):
        self.firstName = firstName
        self.lastName  = lastName
        self.id = uscfId
        self.rating = int(rating) if rating else 0
    
    def give_bye_for_next_round(self):
        self.card.add_score(GamePoints.BYE)

    def has_bye_for_round(self, round: int) -> bool:
        return self.card.has_bye(round)
    
    def to_dict(self):
        dict_obj = self.__dict__.copy()
        return dict_obj
