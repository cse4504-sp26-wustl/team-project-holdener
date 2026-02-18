
from typing import Optional
class Player:
    def __init__(self, firstName: str, lastName: str, uscfId: str, rating=None):
        self.firstName = firstName
        self.lastName  = lastName
        self.id = uscfId
        self.rating = int(rating) if rating else 0

    def to_dict(self):
        dict_obj = self.__dict__.copy()
        return dict_obj
