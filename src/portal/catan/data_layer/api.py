from typing import Dict, Tuple
import time
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

DiceHistory = {}
RobberHistory = {}
Cardset = {}
Player = {}
Construction = {}
Tile = {}
HarborSea = {}
HarborLand = {}
Bank = {}
Game = {}

number_of_games = 0
number_of_players = 0


def _get_new_game_id() -> int:
    global number_of_games
    game_id = number_of_games
    number_of_games = number_of_games + 1
    return game_id


def _get_new_player_id() -> int:
    global number_of_players
    player_id = number_of_players
    number_of_players = number_of_players + 1
    return player_id

# HACK: no need  for DB API
def get_last_game_id():
    global number_of_games
    return number_of_games - 1


def init_game(
    map_name: str,
    player_colors: Dict[int, str],
) -> Tuple[int, Dict[int, str], Dict[int, str]]:
    # return game_id, user_to_player, player_orders
    # TODO: DB API need to return user_to_player mapping

    order = 0
    game_id = _get_new_game_id()

    player_orders = {}
    user_to_player = {}

    # set up players
    for user_id, color in player_colors.items():
        player_id = _get_new_player_id()
        user_to_player[user_id] = player_id

        Player[player_id] = {}
        Player[player_id]['color'] = color

        Player[player_id]['order'] = order
        player_orders[player_id] = order

        order = order + 1
    return (game_id, user_to_player, player_orders)



##########################################
# Game Room
##########################################

Room = {}

def update_user(user_id, room_id, color=None):
    user_id = str(user_id)
    room_id = str(room_id)
    if room_id not in Room:
        Room[room_id] = {
            'host': None,
            'users': {},
        }

    if Room[room_id]['host'] is None:
        Room[room_id]['host'] = user_id

    users = Room[room_id]['users']

    if user_id in users:
        user = users[user_id]
        if color is None:
            color = user['color']

    users[user_id] = {
            'last_update': int(time.time()),
            'is_active': True,
            'color': color,
        }



@database_sync_to_async
def get_users_in_room(room_id):
    room_id = str(room_id)
    if room_id not in Room:
        return []
    else:
        now_ = int(time.time())
        threshold = 10
        user_ids = [id_ for id_, info in Room[room_id]['users'].items() if info['is_active'] and info['last_update'] + threshold > now_]
        users = [User.objects.get(id=user_id) for user_id in user_ids]
        return users
