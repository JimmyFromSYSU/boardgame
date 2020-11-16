import random
from .models import Game
from .models import Bank
from .models import CardSet
from .models import Player
from constants import BANK_RESOURCE_NUM


class CantanBaseController:
    def initial_game(map_name, player_colors):
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
        return {'game_id':curr_game.id, 'player_orders':player_orders}