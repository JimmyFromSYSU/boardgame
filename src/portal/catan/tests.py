from django.test import TestCase
from unittest.mock import patch
from .models import Game
from .models import Construction
from .models import Player
from .logic.constans import SCORE_TO_WIN
from .logic.catan_controller import CatanBaseController


# Create your tests here.
class CatanControllerTests(TestCase):
    GAME_ID = 12345
    USER_ID = 54321
    CURR_PLAYER_ORDER = 0
    PLAYER_NUM = 4

    def _get_game(self):
        return Game(map_name='map_name', current_player=self.CURR_PLAYER_ORDER,
                    number_of_player=self.PLAYER_NUM, state='START')

    @patch("catan.logic.catan_controller.get_game")
    def test_get_game_info_successful(self, get_game_method):
        controller = CatanBaseController()
        get_game_method.return_value = self._get_game()

        expected = {
            'turn_id': 0,
            'number_of_player': 4,
            'status': Game.SETTLE,
            'state': 'START',
            'current_player_id': 0
        }

        game_info = controller.get_game_info(self.GAME_ID)
        assert game_info == expected

    @patch("catan.logic.catan_controller.get_player_by_user_id")
    @patch("catan.logic.catan_controller.get_construction")
    def test_place_construction_successful(self, get_const_method, get_player_method):
        controller = CatanBaseController();
        const = Construction(type=Construction.ROAD);
        player = Player();
        get_const_method.return_value = const
        get_player_method.return_value = player

        expect = Construction(owner=player, type=Construction.HOUSE)

        controller.place_construction(self.GAME_ID, self.USER_ID, 10, 10, 1, Construction.HOUSE)
        assert const.type == expect.type
        assert const.owner == expect.owner

    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_end(self, score_method, get_game_method):
        controller = CatanBaseController()
        game = self._get_game()
        get_game_method.return_value = game
        score_method.return_value = SCORE_TO_WIN

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.END

    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_first_found_start(self, score_method, get_game_method):
        controller = CatanBaseController()
        game = self._get_game()
        get_game_method.return_value = game
        expected_player = (game.current_player + 1) % self.PLAYER_NUM
        score_method.return_value = 0

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.SETTLE
        assert game.current_player == expected_player


    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_first_round_end(self, score_method, get_game_method):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = self.PLAYER_NUM - 1
        get_game_method.return_value = game
        expected_player = game.current_player
        score_method.return_value = 1

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.SETTLE
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_second_round_start(self, score_method, get_game_method):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = self.PLAYER_NUM
        get_game_method.return_value = game
        expected_player = (game.current_player - 1 + self.PLAYER_NUM) % self.PLAYER_NUM
        score_method.return_value = 1

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.SETTLE
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_second_round_end(self, score_method, get_game_method):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = 2 * self.PLAYER_NUM - 1
        get_game_method.return_value = game
        expected_player = (game.current_player - 1 + self.PLAYER_NUM) % self.PLAYER_NUM
        score_method.return_value = 2

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.MAIN
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_main_round(self, score_method, get_game_method):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = 2 * self.PLAYER_NUM
        get_game_method.return_value = game
        expected_player = (game.current_player + 1) % self.PLAYER_NUM
        score_method.return_value = 2

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.MAIN
        assert game.current_player == expected_player








