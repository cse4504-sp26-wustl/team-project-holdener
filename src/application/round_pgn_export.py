from domain.gameOutcome import GameOutcome
from domain.player import Player
from domain.tournamentRound import TournamentRound

DEFAULT_EVENT_NAME = "Arbiter Tournament"


def export_round_to_pgn(
    tournament_round: TournamentRound,
    round_number: int,
    event_name: str = DEFAULT_EVENT_NAME,
) -> str:
    entries = []

    for game in tournament_round.get_games():
        entries.append(
            _format_pgn_game(
                event_name=event_name,
                round_number=round_number,
                white_name=_player_name(game.white),
                black_name=_player_name(game.black),
                white_uscf_id=game.white.id,
                black_uscf_id=game.black.id,
                result=_outcome_to_pgn_result(game.outcome),
            )
        )

    for bye_player in tournament_round.byes:
        entries.append(
            _format_pgn_game(
                event_name=event_name,
                round_number=round_number,
                white_name=_player_name(bye_player),
                black_name="BYE",
                white_uscf_id=bye_player.id,
                black_uscf_id=None,
                result="1-0",
            )
        )

    return "\n\n".join(entries)


def _format_pgn_game(
    event_name: str,
    round_number: int,
    white_name: str,
    black_name: str,
    white_uscf_id: str,
    black_uscf_id: str | None,
    result: str,
) -> str:
    headers = [
        _header("Event", event_name),
        _header("Round", str(round_number)),
        _header("White", white_name),
        _header("Black", black_name),
        _header("WhiteUSCFId", white_uscf_id),
    ]
    if black_uscf_id is not None:
        headers.append(_header("BlackUSCFId", black_uscf_id))
    headers.append(_header("Result", result))
    headers.append("")
    headers.append(result)
    return "\n".join(headers)


def _header(name: str, value: str) -> str:
    safe_value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'[{name} "{safe_value}"]'


def _player_name(player: Player) -> str:
    return f"{player.firstName} {player.lastName}"


def _outcome_to_pgn_result(outcome: GameOutcome) -> str:
    if outcome == GameOutcome.WHITE_WIN:
        return "1-0"
    if outcome == GameOutcome.BLACK_WIN:
        return "0-1"
    if outcome == GameOutcome.DRAW:
        return "1/2-1/2"
    return "*"
