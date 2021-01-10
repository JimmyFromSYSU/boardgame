
from .catan_controller import CatanBaseController
from channels.db import database_sync_to_async

controller = CatanBaseController()


class GameState:
    START = "START"
    SETTLE_HOUSE = "SETTLE_HOUSE"
    SETTLE_ROAD = "SETTLE_ROAD"


class GameStatus:
    SETTLE = 'ST'
    MAIN = 'MA'
    END = 'ED'


class BuildType:
    HOUSE = 'HS'
    TOWN = 'TN'
    ROAD = 'RD'


@database_sync_to_async
def build_house(game_id, data):
    game_info = controller.get_game_info(game_id)
    status = game_info['status']
    state = game_info['state']
    user_id = data['user_id']

    if status == GameStatus.SETTLE:
        controller.place_construction(game_id, user_id, data['x'], data['y'], data['z'], BuildType.HOUSE)
        controller.change_game_state(game_id, GameState.SETTLE_ROAD)

    response = {
        'action': 'COMFIRM_BUILD_HOUSE',
        'x': data['x'],
        'y': data['y'],
        'z': data['z'],
        'color': data['color'],
    }
    return response
