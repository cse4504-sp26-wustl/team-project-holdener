from pprint import pprint
from domain.player import Player
import sys
from domain.gameOutcome import GameOutcome
from application.tournamentOperations import TournamentOperations
from parser.csv_to_player import parse_file

def main():
    if len(sys.argv) == 1:
        print('Usage: ' + sys.argv[0] + ' <CSV_FILE>')
        return

    playerList = parse_file(sys.argv[1])

    tournamentOp = TournamentOperations(playerList);
    # generating tournament round
    round1 = tournamentOp.generate_next_round()

    # setting game outcome
    tournamentOp.set_outcome(round1.games[0].id, GameOutcome.WHITE_WIN)

    for game in round1.games:
        print(game.to_dict())



    # updating game details after the round is over
    #tournamentOp.update_game(round1.games[0].id, playerList[1], playerList[0], GameOutcome.WHITE_WIN)
    
    round_dict = round1.to_dict()
    print(round_dict)

    for game in round1.games:
        print(game.to_dict())

if __name__ == '__main__':
    main()
