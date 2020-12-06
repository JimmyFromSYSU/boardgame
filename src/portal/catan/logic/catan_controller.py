import random
from typing import Dict, Any, List, Tuple, Optional
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
CardSetDict = Dict[str, int]
# CardType could be
CardType = str
UserId = int


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

    # TODO: change to user_colors
    # TODO: list comprehensive
    # Note:
    # 初始化开始顺序，保存Player，Bank,以及整个地图（Tiles）到数据库。
    def initial_game(self, map_name, player_colors: Dict[int, str]) -> Dict[str, Any]:
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
        for user_id, user_color in player_colors.items():
            player_card_set = CardSet()
            order = (order - current_player + player_num) % player_num
            player = Player(
                card_set=player_card_set, order=order, color=user_color, game=curr_game, user_id=user_id)
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

    # Note
    # 在指定位置放置Construction，并删除旧的Construction
    def place_construction(self, game_id, user_id, cx, cy, cz, ctype: str) -> bool:
        player = get_player_by_user_id(game_id, user_id)
        construction = get_construction(game_id, cx, cy, cz)
        construction.owner = player
        construction.type = ctype
        return True

    # 玩家结束回合，更新Game的status，curr_player, turn_id
    def end_turn(self, game_id) -> bool:
        game = get_game(game_id)
        turn_id = game.turn_id
        player_num = game.number_of_player
        curr_player = game.current_player

        if self.score(game_id) >= SCORE_TO_WIN:
            game.status = Game.END
            return True

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
        return True

    # 返回指定玩家当前得分
    def score(self, game_id, user_id) -> int:
        pass

    # Note：dice range from [1, 6]
    # 保存并返回玩家丢骰子的数值
    def roll_dice(self, game_id, user_id) -> Tuple[int, int]:
        game = get_game(game_id)
        player = get_player_by_order(game.id, game.current_player)
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        dice_history = DiceHistory(dice1=dice1, dice2=dice2, game=game, player=player, turn_id=game.turn_id)
        return dice1, dice2

    # todo list cardset key
    # Note: dice_sum is from 2~12.
    # 根据骰子数值计算玩家所得资源，从银行移动资源到玩家，保存银行和玩家的资源到数据库。
    def compute_resource(self, game_id, dice_sum: int) -> Dict[UserId, CardSetDict]:
        game = get_game(game_id)

    # 将List
    def __build_cardset_dict(self, cards: List[str]) -> Dict[str, int]:
        pass

    # Note：only distribute 5 resource card, not including development cards.
    # 从银行移动资源到玩家，保存银行和玩家的资源到数据库。
    def distribute_resource_from_bank(self, game_id, user_id, cards: List[str]) -> bool:
        bank = get_bank(game_id)
        player = get_player_by_user_id(user_id, game_id)
        bank_card_set = bank.card_set
        player_card_set = player.card_set

        resource_cards = self.__build_cardset_dict(cards)
        for resource_type, num in resource_cards.items():
            # move to cardSet model
            if resource_type == 'lumber':
                player_card_set.lumber = player_card_set.lumber + num
                bank_card_set.lumber = bank_card_set.lumber - num
            elif resource_type == 'brick':
                player_card_set.brick = player_card_set.brick + num
                bank_card_set.brick = bank_card_set.brick - num

    # 返回当前游戏信息
    def get_game_info(self, game_id) -> Dict[str, Any]:
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

    # 返回资源给银行，指定玩家得到一张随机技能卡，保存数据库。
    def trade_random_development_card(self, game_id, user_id) -> CardType:
        # return resource card
        # get random development card
        pass

    # todo: 确定银行是否能获得以使用的技能卡
    # Note：return development card to bank only.
    # 玩家消耗技能卡，银行获得该张技能卡，保存到数据库
    def withdraw_development_card(self, game_id, user_id, used_card: CardType) -> bool:
        pass

    # 将一组资源卡从一个玩家移动到另一个玩家的牌堆，保存数据库。
    # todo：需检查玩家牌数
    def move_player_resource_card(self, game_id, from_user: UserId, to_user: UserId, resource_card_list) -> bool:
        pass

    # 玩家将robber从原来位置移动到指定位置, 并设置受害者。保存数据库
    def move_robber(self, game_id, user_id, tile_x, tile_y, victim_id) -> bool:
        pass

    # 玩家从受害者随机抽取卡牌。如果受害者没有卡牌，则返回none。
    def get_random_resource(self, game_id, user_id, victim_id) -> Optional[CardType]:
        pass







