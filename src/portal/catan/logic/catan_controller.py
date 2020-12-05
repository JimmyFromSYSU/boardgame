import random
from ..models import Game
from ..models import Bank
from ..models import CardSet
from ..models import Player
from ..models import RobberHistory
from ..models import Tile
from ..models import DiceHistory
from .constans import BANK_RESOURCE_NUM
from .constans import SCORE_TO_WIN
from .map_template import CATAN_MAPS
from ..db.catan_database import get_player_by_user_id
from ..db.catan_database import get_player_by_order
from ..db.catan_database import get_construction
from ..db.catan_database import get_game
from ..db.catan_database import get_bank


class CatanBaseController:

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
        curr_game = Game(map_name=map_name, current_player=0, num_of_player=player_num)
        
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
            player = Player(
                card_set=player_card_set, order=order, color=player_colors[user_id], game=curr_game, user_id=user_id)
            player_orders[player.id] = order
            order += 1

        map = CATAN_MAPS[map_name]
        robber_dict = map['robber']
        robber_history = RobberHistory(turn_id=0, game=curr_game)
        for tile in map['tiles']:
            type_name = tile['name']
            tile = Tile(
                type=self.__get_tile_type(type_name),
                number=tile['number'],
                x=tile['x'],
                y=tile['y'],
                game=curr_game)

        return {'game_id': curr_game.id, 'player_orders': player_orders}

    def place_construction(self, game_id, user_id, cx, cy, cz, ctype):
        player = get_player_by_user_id(game_id, user_id)
        construction = get_construction(game_id, cx, cy, cz)
        construction.owner = player
        construction.type = ctype

    def end_turn(self, game_id):
        game = get_game(game_id)
        turn_id = game.turn_id
        player_num = game.number_of_player
        curr_player = game.current_player

        if self.score(game_id) >= SCORE_TO_WIN:
            game.status = Game.END
            return

        if player_num <= turn_id < (2 * player_num):
            game.current_player = (curr_player - 1 + player_num) % player_num
        else:
            game.current_player = (curr_player + 1) % player_num

        if player_num - 1 == turn_id:
            game.current_player = (game.current_player - 1 + player_num) % player_num

        game.turn_id = turn_id + 1
        if game.turn_id < 2 * player_num:
            game.status = Game.SETTLE
        else:
            game.status = Game.MAIN

    def score(self, game_id):
        pass

    def roll_dice(self, game_id):
        game = get_game(game_id)
        player = get_player_by_order(game.id, game.current_player)
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        dice_history = DiceHistory(dice1=dice1, dice2=dice2, game=game, player=player, turn_id=game.turn_id)
        return [dice1, dice2]

    def compute_resource(self, game_id, dice_sum):
        game = get_game(game_id)

    def disturb_resource(self, game_id, user_id, resource_card_list):
        bank = get_bank(game_id)
        player = get_player_by_user_id(user_id, game_id)
        bank_card_set = bank.card_set
        player_card_set = player.card_set

        for resource_type in resource_card_list:
            num = resource_card_list[resource_type]
            if resource_type == 'lumber':
                player_card_set.lumber = player_card_set.lumber + num
                bank_card_set.lumber = bank_card_set.lumber - num
            elif resource_type == 'brick':
                player_card_set.brick = player_card_set.brick + num
                bank_card_set.brick = bank_card_set.brick - num

    def get_game_info(self, game_id):
        game = get_game(game_id)
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






