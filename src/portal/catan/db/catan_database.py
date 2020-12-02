from ..models import Game
from ..models import Player
from ..models import Construction
from ..models import Bank


def get_player_by_user_id(game_id, user_id):
    return Player.objects.get(game=game_id, user_id=user_id)


def get_player_by_order(game_id, order):
    return Player.objects.get(game=game_id, order=order)


def get_construction(game_id, cx, cy, cz):
    return Construction.objects.get(game=game_id, x=cx, y=cy, z=cz)


def get_game(game_id):
    return Game.objects.get(pk=game_id)


def get_bank(game_id):
    return Bank.objects.get(game=game_id)
