from django.test import TestCase
from .models import Game


# Create your tests here.
class CatanControllerTests(TestCase):
    def test_get_game_info_successful(self):
        game = Game(map_name='map_name', current_player=0, player_num=4, state='START')
