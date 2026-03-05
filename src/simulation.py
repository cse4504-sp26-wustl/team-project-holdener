from application.tournamentOperationsFromBackup import TournamentOperationsFromBackup
from domain.tournamentRound import TournamentRound
from parser.csv_to_player import parse_file
from parser.csv_to_games import csv_to_games
import sys

def process_command_line_args():
    """
    Process command line arguments for tournament simulation.
    
    Returns:
        tuple: (player_file, round_files) where player_file is a string
               and round_files is a list of round result file names.
    """
    if len(sys.argv) < 2:
        raise ValueError("At least one argument (player data file) is required")
    
    player_file = sys.argv[1]
    round_files = sys.argv[2:] if len(sys.argv) > 2 else []
    
    return player_file, round_files

if __name__ == "__main__":
    roster, round_files = process_command_line_args()
    players = parse_file(roster)
    tournament_rounds = []

    for round_file in round_files:
        game_list = csv_to_games(round_file, players)
        next_round = TournamentRound()
        for g in game_list:
            next_round.add_game(g, g._id)
        tournament_rounds.append(next_round)
    for r in tournament_rounds:
        print(r.to_dict())
    tournament_ops = TournamentOperationsFromBackup(players, tournament_rounds)
    next_round = tournament_ops.generate_next_round()
    for game in next_round.get_games():
        print(f"{game.white.id},{game.black.id}")