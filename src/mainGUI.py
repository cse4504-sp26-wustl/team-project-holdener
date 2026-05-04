import webview
import os
from domain.player import Player
from domain.gameOutcome import GameOutcome
from application.round_pgn_export import export_round_to_pgn
from application.tournamentOperations import TournamentOperations
from parser.csv_to_player import parse_file


OPEN_DIALOG = getattr(getattr(webview, "FileDialog", None), "OPEN", webview.OPEN_DIALOG)
SAVE_DIALOG = getattr(getattr(webview, "FileDialog", None), "SAVE", webview.SAVE_DIALOG)


class TournamentAPI:
    """Exposes tournament operations to the JS frontend via PyWebView."""

    def __init__(self):
        self.tournament_ops: TournamentOperations | None = None

    def pick_file(self) -> dict:
        result = window.create_file_dialog(
            OPEN_DIALOG,
            file_types=('CSV Files (*.csv)',)
        )
        path = self._normalize_dialog_result(result)
        if path:
            return {"path": path}
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

    def export_round_pgn(self, round_index: int) -> dict:
        if not self.tournament_ops:
            return {"error": "No tournament in progress."}

        if round_index < 0 or round_index >= len(self.tournament_ops.all_rounds):
            return {"error": f"Round {round_index + 1} does not exist."}

        round_number = round_index + 1
        tournament_round = self.tournament_ops.all_rounds[round_index]

        try:
            pgn_text = export_round_to_pgn(tournament_round, round_number)
            save_path = self._pick_export_file(round_number)
            if not save_path:
                return {"cancelled": True}

            with open(save_path, "w", encoding="utf-8") as output_file:
                output_file.write(pgn_text)
            return {"success": True, "path": save_path}
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

    def _pick_export_file(self, round_number: int) -> str | None:
        suggested_name = f"round_{round_number}.pgn"
        result = window.create_file_dialog(
            SAVE_DIALOG,
            save_filename=suggested_name,
            file_types=("PGN Files (*.pgn)",),
        )
        return self._normalize_dialog_result(result)

    def _normalize_dialog_result(self, result) -> str | None:
        if not result:
            return None
        if isinstance(result, str):
            return result
        if isinstance(result, (list, tuple)) and len(result) > 0:
            return result[0]
        return None


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
