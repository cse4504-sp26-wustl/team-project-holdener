from typing import List
from domain.player import Player

def parse_file(file_name: str) -> List[Player]:
    players_list = []
    with open(file_name) as input_file:
       for line in input_file:
           player = csv_to_player(line)
           if not player:
               raise ValueError('invalid csv line: ' + line)
           players_list.append(player)
    return players_list

# convert a csv line to a Player object
# csv line format is:
# USCF ID, LAST NAME, FIRST NAME, RATING
# the RATING field is optional
USCF_ID = 0
LAST_NAME = 1
FIRST_NAME = 2
RATING = 3

def csv_to_player(csv_line: str) -> Player:
    tokens = csv_line.strip().split(',')
    player = None
    if len(tokens) == 3:
        player = Player(tokens[FIRST_NAME], tokens[LAST_NAME], tokens[USCF_ID])
    elif len(tokens) == 4:
        player = Player(tokens[FIRST_NAME], tokens[LAST_NAME], tokens[USCF_ID], tokens[RATING])
    return player

