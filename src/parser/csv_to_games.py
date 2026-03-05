from domain.player import Player
from domain.game import Game
from domain.gameOutcome import GameOutcome

WHITE_USCF_ID = 0
BLACK_USCF_ID = 1
RESULT = 2

def csv_to_games(file_name: str, players: list[Player])->list[Game]:
    game_list = []
    next_game_id = 1
    with open(file_name) as input_file:
       next(input_file)  # Skip header row
       for line in input_file:
           game = create_game_from_csv(line, players, next_game_id)
           if not game:
               raise ValueError('Could not find a players for game: ' + line)
           game_list.append(game)
           next_game_id += 1
    return game_list

def create_game_from_csv(csv_line: str, players: list[Player], next_game_id: int) -> Game:
    cleaned_line = csv_line.strip()
    if not cleaned_line:
        return
        
    parts = cleaned_line.split(',')
    white_uscf_id = parts[WHITE_USCF_ID].strip()
    black_uscf_id = parts[BLACK_USCF_ID].strip()
    result_str = parts[RESULT].strip().lower()
    
    # Find the game by matching both player USCF IDs
    white_player = next((p for p in players if p.id == white_uscf_id), None)
    black_player = next((p for p in players if p.id == black_uscf_id), None)
    if not white_player or not black_player:
        return None
    
    game = Game(next_game_id, white_player, black_player)
    
    if result_str == 'white':
        game.set_outcome(GameOutcome.WHITE_WIN)
    elif result_str == 'black':
        game.set_outcome(GameOutcome.BLACK_WIN)
    elif result_str == 'draw':
        game.set_outcome(GameOutcome.DRAW)
    return game