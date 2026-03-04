from pathlib import Path
from py4swiss.trf import ParsedTrf
from py4swiss.trf.sections import PlayerSection, TournamentSection, XSection
from py4swiss.trf.results import RoundResult, ScoringPointSystem
from py4swiss.trf.codes import PlayerCode
from domain.scoreCard import ScoreCard

from py4swiss.trf.results import ColorToken
from py4swiss.trf.results import ResultToken
from domain.gamePoints import GamePoints
from domain.gameColor import GameColor
from domain.gameOutcome import GameOutcome

def scorecards_to_parsed_trf(scorecards: list[ScoreCard], tournament_name: str = "", number_of_rounds: int = 0) -> ParsedTrf:
    """Convert a list of ScoreCard objects to a ParsedTrf object."""
    
    # Create player sections from scorecards
    player_sections = []

    for rank, scorecard in enumerate(scorecards):
        # Convert GamePoints/GameColor results to RoundResult objects
        round_results = []
        for i, outcome in enumerate(scorecard.outcomes):
            if i < len(scorecard.opponents):
                opponent_id = scorecard.opponents[i]
                color = scorecard.sides[i]
                # Map GameColor to ColorToken
                color_token = _game_color_to_color_token(color)
                
                # Map GamePoints to ResultToken
                result_token = _game_outcome_to_result_token(outcome, color)
                
                round_result = RoundResult(
                    id=opponent_id,
                    color=color_token,
                    result=result_token
                )
                round_results.append(round_result)
        
        # Calculate points times ten (points stored as float, need to convert to int)
        points_times_ten = int(scorecard.get_total_score() * 10)
        
        player_section = PlayerSection(
            code=PlayerCode.PLAYER,
            starting_number=scorecard.id,
            name=f"Player {scorecard.id}",
            fide_rating=scorecard.rating,
            points_times_ten=points_times_ten,
            rank=rank+1,
            results=round_results
        )
        player_sections.append(player_section)
    
    # Create tournament section
    tournament_section = TournamentSection(
        tournament_name=tournament_name
    )
    
    # Create X section with default scoring system
    scoring_point_system = ScoringPointSystem()
    x_section = XSection(
        number_of_rounds=number_of_rounds,
        scoring_point_system=scoring_point_system
    )
    print(player_sections)
    # Create and return ParsedTrf
    parsed_trf = ParsedTrf(
        player_sections=player_sections,
        tournament_section=tournament_section,
        team_sections=[],
        x_section=x_section
    )
    
    return parsed_trf


def _game_outcome_to_result_token(game_outcome: GameOutcome, game_color: GameColor):
    """Map GameOutcome to ResultToken."""

    if game_outcome == GameOutcome.FORCED_BYE:
        return ResultToken.FULL_POINT_BYE
    elif game_outcome == GameOutcome.WHITE_WIN:
        if game_color == GameColor.WHITE:
            return ResultToken.WIN
        else:
            return ResultToken.LOSS
    elif game_outcome == GameOutcome.BLACK_WIN:
        if game_color == GameColor.BLACK:
            return ResultToken.WIN
        else:
            return ResultToken.LOSS
    elif game_outcome == GameOutcome.DRAW:
        return ResultToken.DRAW
    elif game_outcome == GamePoints.LOSE:
        return ResultToken.LOSS
    else:
        return ResultToken.LOSS  # Default fallback

def _game_color_to_color_token(color):
    """Map GameColor to ColorToken."""
    
    if color == GameColor.WHITE:
        return ColorToken.WHITE
    elif color == GameColor.BLACK:
        return ColorToken.BLACK
    else:
        return ColorToken.BYE_OR_NOT_PAIRED