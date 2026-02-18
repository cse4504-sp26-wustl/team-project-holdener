from typing import List
from domain.player import Player
from domain.tournamentRound import TournamentRound
from domain.gameOutcome import GameOutcome
from domain.game import Game

class TournamentOperations:
    def __init__(self, players: List[Player]):
        self.all_rounds = []
        self.all_players = players
        self.next_game_id = 1
    def generate_next_round(self) -> TournamentRound:
        # Calculate scores and color history for all players
        player_stats = {p.id: {'score': 0.0, 'colors': []} for p in self.all_players}
        
        for round in self.all_rounds:
            for game in round.get_games():
                white_id = game.white.id
                black_id = game.black.id
                
                # Record colors
                player_stats[white_id]['colors'].append('W')
                player_stats[black_id]['colors'].append('B')

                # Calculate scores
                if game.outcome == GameOutcome.WHITE_WIN:
                    player_stats[white_id]['score'] += 1.0
                elif game.outcome == GameOutcome.BLACK_WIN:
                    player_stats[black_id]['score'] += 1.0
                elif game.outcome == GameOutcome.DRAW:
                    player_stats[white_id]['score'] += 0.5
                    player_stats[black_id]['score'] += 0.5
                    
        # Sort players by score (desc), then rating (desc)
        # Using a tuple for sort key: (score, rating)
        # We need to access player object attributes inside the sort key, so define a helper
        def get_sort_key(player):
            score = player_stats[player.id]['score']
            # Treat None rating as 0 for sorting
            rating = player.rating if player.rating is not None else 0
            return (score, rating)

        # Create a list of players to pair
        sorted_players = sorted(self.all_players, key=get_sort_key, reverse=True)
        
        next_round = TournamentRound()
        self.all_rounds.append(next_round)

        # Pair players
        # Simple adjacent pairing after sorting
        # P1 vs P2, P3 vs P4, etc.
        # This satisfies:
        # 1. Winners play winners (sorted by score)
        # 2. Similar rating paired (sorted by rating within score groups)
        
        paired_players = []
        
        # We process players and remove them from the list, or simpler, iterate by index
        # Need to handle odd number of players - simplified to assume even or drop last for now as per previous simple implementation style
        # But robust code should handle bye. Let's assume even for now or leave last one out
        
        matchups = []
        while len(sorted_players) >= 2:
            p1 = sorted_players.pop(0)
            p2 = sorted_players.pop(0)
            matchups.append((p1, p2))
            
        if len(sorted_players) == 1:
             # Handle bye - user didn't specify, maybe just don't pair? 
             # Or add a bye game? For now, ignore odd player or print warning?
             # Previous code didn't handle odd either (range(0, len, 2))
             print(f"Warning: Odd number of players, {sorted_players[0].firstName} {sorted_players[0].lastName} receives a bye (not implemented).")
             pass

        for p1, p2 in matchups:
            white, black = self._assign_colors(p1, p2, player_stats)
            game = Game(self.next_game_id, white, black)
            next_round.add_game(game, self.next_game_id)
            self.next_game_id += 1
            
        return next_round

    def _assign_colors(self, p1: Player, p2: Player, stats: dict):
        p1_colors = stats[p1.id]['colors']
        p2_colors = stats[p2.id]['colors']
        
        p1_last = p1_colors[-1] if p1_colors else None
        p2_last = p2_colors[-1] if p2_colors else None
        
        # Helper to check streaks
        def get_streak(colors):
            if not colors: return 0, None
            last = colors[-1]
            count = 0
            for c in reversed(colors):
                if c == last: count += 1
                else: break
            return count, last

        p1_streak_len, p1_streak_color = get_streak(p1_colors)
        p2_streak_len, p2_streak_color = get_streak(p2_colors)

        # Constraint: No 3 same colors in a row
        p1_must_switch = (p1_streak_len >= 2)
        p2_must_switch = (p2_streak_len >= 2)
        
        # Decision Logic
        if p1_must_switch and not p2_must_switch:
            # P1 must switch from their streak color
            if p1_streak_color == 'W': return (p2, p1) # P1 needs B
            else: return (p1, p2) # P1 needs W
            
        elif p2_must_switch and not p1_must_switch:
            # P2 must switch
            if p2_streak_color == 'W': return (p1, p2) # P2 needs B
            else: return (p2, p1) # P2 needs W
            
        elif p1_must_switch and p2_must_switch:
            # Both must switch. If they have different streak colors, great!
            if p1_streak_color != p2_streak_color:
                # P1 needs (not P1_streak), P2 needs (not P2_streak)
                # Since P1_streak != P2_streak, e.g. P1=W, P2=B
                # P1 needs B, P2 needs W. Fits!
                if p1_streak_color == 'W': return (p2, p1)
                else: return (p1, p2)
            else:
                # Both have same streak color (e.g. both WW). Both need B. Conflict!
                # One must suffer 3 in a row.
                # Lower score or rating usually takes the hit in real pairing systems.
                # Here, we just pick P1 as White arbitrarily or keep score order (P1 is higher ranked).
                # If both need Black (streak W), give P1 White (3rd W) and P2 Black.
                # Or based on "interchangeably", try to follow alternation history further back.
                # Default: Give P1 White.
                 return (p1, p2) 

        # No forced switches due to streaks. Optimize for alternation.
        # Preference: Opposite of last color.
        p1_prefers = 'W' if p1_last == 'B' else 'B'
        p2_prefers = 'W' if p2_last == 'B' else 'B'
        
        if p1_prefers != p2_prefers:
            # They want different things, perfect!
            if p1_prefers == 'W': return (p1, p2)
            else: return (p2, p1)
        
        # Conflict in preference (e.g. both want White)
        # Tie-breaker: 
        # 1. Who has greater color imbalance? (Total W - Total B). Not calculated here.
        # 2. Who played the preferred color more recently?
        # Simple fallback: Higher ranked (P1) gets preference? 
        # Or alternating based on round number? 
        # Let's give it to P1 (first in pair).
        if p1_prefers == 'W': return (p1, p2)
        else: return (p2, p1)


        
    def set_outcome(self, gameId: int, result: GameOutcome):
        game = self._find_game(gameId)
        if game:
            game.set_outcome(result)
        else:
             raise ValueError(f"Game {gameId} not found")

    def switch_sides(self, game_id):
        game = self._find_game(game_id)
        if game:
            game.switch_sides()
        else:
            raise ValueError(f"Game {game_id} not found")

    def get_games(self, round_number: int) -> List[Game]:
        return self.all_rounds[round_number].get_games()

    def _find_game(self, game_id: int):
        for t_round in self.all_rounds:
            game = t_round.get_game(game_id)
            if game:
                 return game
        return None
