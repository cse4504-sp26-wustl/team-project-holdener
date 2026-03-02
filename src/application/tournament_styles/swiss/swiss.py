from domain.tournamentRound import TournamentRound
from domain.game import Game
from domain.scoreCard import ScoreCard
from domain.gameColor import GameColor
from application.tournament_styles.swiss.no_repeat_opponent import no_repeat_opponents
from application.tournament_styles.swiss.no_repeating_color import no_repeating_color
def score_and_rating(card):
    return (card.get_total_score(), card.rating)

class Swiss:
    def __init__(self):
        self.rules = [no_repeat_opponents, no_repeating_color]

    def get_next_round(self, cards: list[ScoreCard] ) -> list[(int, int)]:
        games = []
        # group cards by score
        groups = []
        sorted_cards = sorted(cards, key=score_and_rating, reverse=True)
        while len(sorted_cards) > 0:
            groups.append(self.get_next_group(sorted_cards))
        
        for g in groups:
            game_pairs = self.pair_group(g)
            if game_pairs is not None:
                games.extend(game_pairs)
        return games
                
    def get_next_group(self, cards: list[ScoreCard]) -> list[ScoreCard]:
        group = []
        score = cards[0].get_total_score()
        index = 0
        for card in cards:
            if card.get_total_score() == score:
                group.append(card)
            index+=1
        if len(group) % 2 == 1:
            group.append(cards[index])
            index+=1

        del cards[0:index]
        return group

    def make_pair(self, card1: ScoreCard, card2: ScoreCard)->tuple[int, int]:
        if len(card1.sides) >= 2 and len(card2.sides) >= 2:
            # get the last 2 games of each player
            last_games_1 = card1.sides[-2:]
            last_games_2 = card2.sides[-2:]
            
            # calculate streaks
            
            c1_white_streak = last_games_1.count(GameColor.WHITE) == 2
            c1_black_streak = last_games_1.count(GameColor.BLACK) == 2
            c2_white_streak = last_games_2.count(GameColor.WHITE) == 2
            c2_black_streak = last_games_2.count(GameColor.BLACK) == 2

            # if a player has a streak of 2, force color switch
            if c1_white_streak: # played 2 whites, must play black
                return (card2.id, card1.id)
            if c2_black_streak: # played 2 blacks, must play white
                return (card2.id, card1.id)
            
            if c1_black_streak: # played 2 blacks, must play white
                return (card1.id, card2.id)
            if c2_white_streak: # played 2 whites, must play black
                return (card1.id, card2.id)

        # otherwise, try to alternate colors based on last game
        last_color1 = card1.get_last_color()
        last_color2 = card2.get_last_color()
        
        if last_color1 == GameColor.WHITE: # played white recently, switch to black
            return (card2.id, card1.id)
        elif last_color2 == GameColor.BLACK: # played black recently, switch to white
            return (card2.id, card1.id)
        
        return (card1.id, card2.id)


    def pair_group(self, group: list[ScoreCard]) -> list[(int, int)]:
        half = len(group)//2
        game_index = 0
        failed = False
        pairs = []
        for top in group[0:half]:
            for rule in self.rules:
                if not rule(group[game_index], group[half+game_index]):
                    failed = True
                    break
            the_pair = self.make_pair(group[game_index], group[half+game_index])
            pairs.append(the_pair)
            game_index += 1
        if failed:
            return None
        return pairs
        
                