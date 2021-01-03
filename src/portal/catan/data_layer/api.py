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
DEFAULT_MAP = 'normal'
Color = [
    {'color': 'blue', 'selected': False,},
    {'color': 'red', 'selected': False,},
    {'color': 'green', 'selected': False,},
    {'color': 'orange', 'selected': False,},
]


def get_room_data():
    return Room


def update_user(user_id, room_id, color=None):
    user_id = str(user_id)
    room_id = str(room_id)
    if room_id not in Room:
        Room[room_id] = {
            # host of the room, host can start the game
            'host': None,
            'users': {},
            'selected_map': DEFAULT_MAP,
        }

    if Room[room_id]['host'] is None:
        Room[room_id]['host'] = user_id

    users = Room[room_id]['users']

    # user is already in the list
    if user_id in users:
        user = users[user_id]
        if color is None:
            color = user['color']

    # assign random color
    if color is None:
        l = len(users)
        if (l < len(Color)):
            color = Color[l]['color']

    users[user_id] = {
        'last_update': int(time.time()),
        'is_active': True,
        'color': color,
    }


def set_selected_map(room_id, map_name):
    # user_id = str(user_id)
    room_id = str(room_id)
    Room[room_id]['selected_map'] = map_name


def get_selected_map(room_id):
    # user_id = str(user_id)
    room_id = str(room_id)
    if 'selected_map' in Room[room_id]:
        return Room[room_id]['selected_map']
    else:
        return DEFAULT_MAP


def get_users_config(room_id):
    room_id = str(room_id)
    return Room[room_id]['users']


@database_sync_to_async
def get_users_in_room(room_id):
    room_id = str(room_id)
    if room_id not in Room:
        return []
    else:
        now_ = int(time.time())

        # Unit is second
        # if a user doesn't update user info within threshold time
        # the backend will treat it as log off
        # TODO: create a heat beat for each user in front-end
        threshold = 100000
        user_ids = [id_ for id_, info in Room[room_id]['users'].items() if info['is_active'] and info['last_update'] + threshold > now_]
        users = [User.objects.get(id=user_id) for user_id in user_ids]
        return users
