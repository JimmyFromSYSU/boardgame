from typing import Dict, Tuple

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
