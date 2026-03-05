import webview
import os
from domain.player import Player
from domain.gameOutcome import GameOutcome
from application.tournamentOperations import TournamentOperations
from parser.csv_to_player import parse_file


class TournamentAPI:
    """Exposes tournament operations to the JS frontend via PyWebView."""

    def __init__(self):
        self.tournament_ops: TournamentOperations | None = None

    def pick_file(self) -> dict:
        result = window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=('CSV Files (*.csv)',)
        )
        if result and len(result) > 0:
            return {"path": result[0]}
        return {"path": None}

    def load_players(self, filename: str) -> dict:
        try:
            players_list = parse_file(filename)
            self.tournament_ops = TournamentOperations(players_list)
            return {
                "players": [self._player_to_dict(p) for p in players_list]
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_round(self) -> dict:
        if not self.tournament_ops:
            return {"error": "No players loaded."}
        try:
            round_obj = self.tournament_ops.generate_next_round()
            games = round_obj.get_games()
            return {"games": [g.to_dict() for g in games]}
        except Exception as e:
            return {"error": str(e)}

    def record_result(self, game_id: int, result_code: int) -> dict:
        if not self.tournament_ops:
            return {"error": "No tournament in progress."}
        outcome_map = {
            1: GameOutcome.WHITE_WIN,
            2: GameOutcome.BLACK_WIN,
            3: GameOutcome.DRAW,
        }
        outcome = outcome_map.get(result_code)
        if outcome is None:
            return {"error": f"Invalid result code: {result_code}. Use 1, 2, or 3."}
        try:
            self.tournament_ops.set_outcome(game_id, outcome)
            return {"outcome": outcome.name}
        except Exception as e:
            return {"error": str(e)}

    def swap_players(self, game_id: int) -> dict:
        if not self.tournament_ops:
            return {"error": "No tournament in progress."}
        try:
            self.tournament_ops.switch_sides(game_id)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    def _player_to_dict(self, player: Player) -> dict:
        return {
            "firstName": player.firstName,
            "lastName": player.lastName,
            "rating": getattr(player, "rating", None),
        }


if __name__ == "__main__":
    api = TournamentAPI()
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    print(ui_path)
    window = webview.create_window(
        title="Arbiter — Tournament Manager",
        url=ui_path,
        js_api=api,
        width=1100,
        height=720,
        min_size=(800, 600),
    )
    api.window = window  # give the API a reference to the window

    webview.start()
