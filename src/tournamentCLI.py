import cmd
import sys
from pprint import pprint
from domain.player import Player
from domain.gameOutcome import GameOutcome
from application.tournamentOperations import TournamentOperations
from parser.csv_to_player import parse_file

class TournamentCLI(cmd.Cmd):
    intro = 'Welcome to the Tournament Management CLI. Type help or ? to list commands.\n'
    prompt = '(chess) '

    def __init__(self):
        super().__init__()
        self.tournament_ops = None

    def do_load_players(self, arg):
        """Load players from a CSV file. Usage: load_players <filename>"""
        if not arg:
            print("Error: Please specify a CSV file.")
            return
        
        try:
            players_list = parse_file(arg)
            self.tournament_ops = TournamentOperations(players_list)
            print(f"Loaded {len(players_list)} players.")
        except Exception as e:
            print(f"Error loading players: {e}")

    def do_generate_round(self, arg):
        """Generate the next round of the tournament."""
        if not self.tournament_ops:
            print("Error: No players loaded. Use load_players first.")
            return

        try:
            round_obj = self.tournament_ops.generate_next_round()
            round_idx = len(self.tournament_ops.all_rounds)
            print(f"Round {round_idx} generated with {len(round_obj.get_games())} games.")
        except Exception as e:
            print(f"Error generating round: {e}")

    def do_record_result(self, arg):
        """Record a result for a game. Usage: record_result <game_id> <result>
           Result specific codes: 1=White Win, 2=Black Win, 3=Draw
        """
        if not self.tournament_ops:
            print("Error: No tournament in progress.")
            return

        args = arg.split()
        if len(args) != 2:
            print("Usage: record_result <game_id> <result_code>")
            print("Result codes: 1 (White Win), 2 (Black Win), 3 (Draw)")
            return

        try:
            game_id = int(args[0])
            result_code = int(args[1])
            
            outcome = None
            if result_code == 1:
                outcome = GameOutcome.WHITE_WIN
            elif result_code == 2:
                outcome = GameOutcome.BLACK_WIN
            elif result_code == 3:
                outcome = GameOutcome.DRAW
            else:
                 print("Invalid result code. Use 1, 2, or 3.")
                 return

            self.tournament_ops.set_outcome(game_id, outcome)
            print(f"Result recorded for game {game_id}: {outcome}")
        except ValueError:
             print("Invalid input. Game ID and result code must be integers.")
        except Exception as e:
            print(f"Error recording result: {e}")

    def do_list_games(self, arg):
        """List games in a specific round. Usage: list_games <round_number>"""
        if not self.tournament_ops:
             print("Error: No tournament in progress.")
             return
        
        if not arg:
            print("Usage: list_games <round_number>")
            return

        try:
            round_num = int(arg)
            # Assuming user interacts with 1-based round numbers
            internal_round_num = round_num - 1
            
            if internal_round_num < 0 or internal_round_num >= len(self.tournament_ops.all_rounds):
                print(f"Round {round_num} does not exist.")
                return

            games = self.tournament_ops.get_games(internal_round_num)
            print(f"--- Games in Round {round_num} ---")
            for game in games:
                d = game.to_dict()
                w_name = f"{d['white']['firstName']} {d['white']['lastName']}"
                b_name = f"{d['black']['firstName']} {d['black']['lastName']}"
                print(f"Game {d['id']}: {w_name} (White) vs {b_name} (Black) - Outcome: {d['outcome']}")
            print("-----------------------------")

        except ValueError:
            print("Round number must be an integer.")
        except Exception as e:
            print(f"Error listing games: {e}")

    def do_swap_players(self, arg):
        """Swap players (colors) in a specific game. Usage: swap_players <game_id>"""
        if not self.tournament_ops:
             print("Error: No tournament in progress.")
             return
        
        if not arg:
             print("Usage: swap_players <game_id>")
             return

        try:
            game_id = int(arg)
        except ValueError:
            print("Game ID must be an integer.")
            return

        try:
            self.tournament_ops.switch_sides(game_id)
            print(f"Swapped players for game {game_id}.")
        except Exception as e:
            print(f"Error swapping players: {e}")

    def do_exit(self, arg):
        """Exit the application."""
        print("Exiting...")
        return True

    def do_quit(self, arg): 
        """Exit the application."""
        return self.do_exit(arg)

if __name__ == '__main__':
    TournamentCLI().cmdloop()
