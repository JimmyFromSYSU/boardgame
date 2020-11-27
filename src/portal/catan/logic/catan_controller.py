import random
from ..models import Game
from ..models import Bank
from ..models import CardSet
from ..models import Player
from ..models import RobberHistory
from ..models import Tile
from constants import BANK_RESOURCE_NUM
from map_template import CATAN_MAPS


class CatanBaseController:
    def __init__(self, catan_db):
        self.db = catan_db

    def __get_tile_type(self, type_name):
        resource_dict = {
            'lumber': Tile.LUMBER,
            'brick': Tile.BRICK,
            'wool': Tile.WOOL,
            'grain': Tile.GRAIN,
            'ore': Tile.ORE,
            'desert': Tile.DESERT,
            'sea': Tile.SEA,
        }
        return resource_dict.get(type_name, "Invalid resource type.")

    def initial_game(self, map_name, player_colors):
        player_num = len(player_colors)
        current_player = random.randint(0, player_num-1)
        curr_game = Game(map_name=map_name, current_player=current_player, player_num=player_num)
        
        bank_card_set = CardSet(
            lumber=BANK_RESOURCE_NUM,  
            brick=BANK_RESOURCE_NUM,  
            wool=BANK_RESOURCE_NUM,  
            grain=BANK_RESOURCE_NUM,  
            ore=BANK_RESOURCE_NUM,  
            dev_knight=BANK_RESOURCE_NUM,  
            dev_one_victory_point=BANK_RESOURCE_NUM,  
            dev_road_building=BANK_RESOURCE_NUM,  
            dev_monopoly=BANK_RESOURCE_NUM,  
            dev_year_of_plenty=BANK_RESOURCE_NUM)
        bank = Bank(card_set=bank_card_set, game=curr_game)

        order = 0
        player_orders = {}
        for user_id in player_colors:
            player_card_set = CardSet()
            order = (order - current_player + player_num) % player_num
            player = Player(card_set=player_card_set, order=order, color=player_colors[user_id], game=curr_game)
            player_orders[player.id] = order
            order += 1

        # todo: read map from a map dict and intialize tiles, harbors and robbers.
        map = CATAN_MAPS[map_name]
        robber_dict = map['robber']
        robber_history = RobberHistory(turn_id=0, game=curr_game)
        for tile in map['tiles']:
            type_name = tile['name']
            tile = Tile(
                type=__get_tile_type(type_name),
                number=tile['number'],
                x=tile['x'],
                y=tile['y'],
                game=curr_game)

        return {'game_id': curr_game.id, 'player_orders': player_orders}

    def place_construction(self, player_id, cx, cy, cz, ctype):
        player = self.db.get_player(player_id)
        construction = self.db.get_construction(player.game.id, cx, cy, cz)
        construction.owner = player
        construction.type = ctype

    def get_curr_player(self, game):
        pass

    def end_turn(self, game):
        pass

    def get_game_info(self, game_id):
        game = self.db.get_game(game_id)
        turn_id = game.turn_id
        number_of_player = game.number_of_player
        status = game.status
        state = game.state
        current_player_id = game.current_player
        return {
            'turn_id': turn_id,
            'number_of_player': number_of_player,
            'status': status,
            'state': state,
            'current_player_id': current_player_id
        }






