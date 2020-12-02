import mock
from django.test import TestCase
from unittest.mock import patch
from .models import Game
from .logic.catan_controller import CatanBaseController


# Create your tests here.
class CatanControllerTests(TestCase):

    def _get_game(self):
        return Game(map_name='map_name', current_player=0, number_of_player=4, state='START')

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

        game_info = controller.get_game_info(12345)
        assert game_info == expected
