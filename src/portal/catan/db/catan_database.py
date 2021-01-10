from ..models import Game
from ..models import Player
from ..models import Construction
from ..models import Bank
from ..models import Tile
from typing import Dict, Any, List, Tuple, Optional


def get_player_by_user_id(game_id, user_id) -> Player:
    return Player.objects.get(game=game_id, user_id=user_id)


def get_player_by_order(game_id, order) -> Player:
    return Player.objects.get(game=game_id, order=order)


def get_players(game_id) -> List[Player]:
    return Player.objects.filter(game=game_id)


def get_constructions(game_id) -> List[Construction]:
    return Construction.objects.filter(game=game_id)


def get_construction_by_location(game_id, cx, cy, cz) -> Optional[Construction]:
    try:
        return Construction.objects.get(game__id=game_id, x=cx, y=cy, z=cz)
    except Construction.DoesNotExist:
        return None


def get_houses(game_id, cx, cy) -> List[Construction]:
    return Construction.objects.filter(game=game_id, x=cx, y=cy, type=Construction.HOUSE)


def count_houses_by_user_id(game_id, user_id) -> int:
    return Construction.objects.filter(game=game_id, owner=user_id, type=Construction.HOUSE).count()


def get_towns(game_id, cx, cy) -> List[Construction]:
    return Construction.objects.filter(game=game_id, x=cx, y=cy, type=Construction.TOWN)


def count_towns_by_user_id(game_id, user_id) -> int:
    return Construction.objects.filter(game=game_id, owner=user_id, type=Construction.TOWN).count()


def get_game(game_id):
    return Game.objects.get(pk=game_id)


def get_game_map_name(game_id):
    return Game.objects.get(pk=game_id).map_name


def get_bank(game_id):
    return Bank.objects.get(game=game_id)


def get_tiles_by_number(game_id:int, dice_sum: int) -> List[Tile]:
    return Tile.objects.filter(game=game_id, number=dice_sum)


def get_tiles(game_id: int) -> List[Tile]:
    return Tile.objects.filter(game=game_id)
