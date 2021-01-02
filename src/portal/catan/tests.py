import random
from django.test import TestCase
from django.forms.models import model_to_dict
from unittest.mock import patch
from .models import Game
from .models import Construction
from .models import Player
from .models import Bank
from .models import CardSet
from .models import Tile
from .logic.constans import SCORE_TO_WIN
from .logic.constans import BANK_RESOURCE_NUM
from .logic.catan_controller import CatanBaseController


# Create your tests here.
class CatanControllerTests(TestCase):
    GAME_ID = 12345
    USER_ID = 54321
    EXTRA_USER_ID = 67890
    CURR_PLAYER_ORDER = 0
    PLAYER_NUM = 4
    controller: CatanBaseController
    game: Game

    def setUp(self):
        self.controller = CatanBaseController()
        self.game = self._get_game()

    def _get_game(self):
        return Game(map_name='map_name', current_player=self.CURR_PLAYER_ORDER,
                    number_of_player=self.PLAYER_NUM, state='START')

    def _get_bank(self):
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
        return Bank(card_set=bank_card_set, game=self.game)

    def _get_player(self):
        return Player(user_id=self.USER_ID, game=self.game, card_set=CardSet())

    def _get_extra_player(self):
        return Player(user_id=self.EXTRA_USER_ID, game=self.game, card_set=CardSet())

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.Bank.save_all")
    @patch("catan.logic.catan_controller.Player.save_all")
    @patch("catan.logic.catan_controller.Tile.save_all")
    @patch("catan.logic.catan_controller.random.randint")
    def test_init_game(self, randint_method, tile_save, player_save, bank_save, game_save):
        randint_method.return_value = 1

        # expected game_id is None since no game is actually created.
        expected = {
            'game_id': None,
            'player_orders': {
                self.USER_ID: 1,
                self.EXTRA_USER_ID: 0
            }
        }

        result = self.controller.initial_game('normal', {self.USER_ID: 'red', self.EXTRA_USER_ID: 'blue'})
        assert result == expected

    @patch("catan.logic.catan_controller.Construction.save_all")
    @patch("catan.logic.catan_controller.get_player_by_user_id")
    @patch("catan.logic.catan_controller.get_construction_by_location")
    def test_place_construction_successful(self, get_const_method, get_player_method, construction_save):
        controller = CatanBaseController();
        const = Construction(type=Construction.ROAD);
        player = self._get_player();
        get_const_method.return_value = const
        get_player_method.return_value = player

        expect = Construction(owner=player, type=Construction.HOUSE)

        controller.place_construction(self.GAME_ID, self.USER_ID, 10, 10, 1, Construction.HOUSE)
        assert const.type == expect.type
        assert const.owner == expect.owner

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_end(self, score_method, get_game_method, game_save):
        controller = CatanBaseController()
        game = self._get_game()
        get_game_method.return_value = game
        score_method.return_value = SCORE_TO_WIN

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.END

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_first_found_start(self, score_method, get_game_method, game_save):
        controller = CatanBaseController()
        game = self._get_game()
        get_game_method.return_value = game
        expected_player = (game.current_player + 1) % self.PLAYER_NUM
        score_method.return_value = 0

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.SETTLE
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_first_round_end(self, score_method, get_game_method, game_save):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = self.PLAYER_NUM - 1
        get_game_method.return_value = game
        expected_player = game.current_player
        score_method.return_value = 1

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.SETTLE
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_second_round_start(self, score_method, get_game_method, game_save):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = self.PLAYER_NUM
        get_game_method.return_value = game
        expected_player = (game.current_player - 1 + self.PLAYER_NUM) % self.PLAYER_NUM
        score_method.return_value = 1

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.SETTLE
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_second_round_end(self, score_method, get_game_method, game_save):
        controller = CatanBaseController()
        game = self._get_game()
        game.turn_id = 2 * self.PLAYER_NUM - 1
        get_game_method.return_value = game
        expected_player = (game.current_player - 1 + self.PLAYER_NUM) % self.PLAYER_NUM
        score_method.return_value = 2

        controller.end_turn(self.GAME_ID)
        assert game.status == Game.MAIN
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.Game.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.CatanBaseController.score")
    def test_end_turn_status_settle_main_round(self, score_method, get_game_method, game_save):
        game = self._get_game()
        game.turn_id = 2 * self.PLAYER_NUM
        get_game_method.return_value = game
        expected_player = (game.current_player + 1) % self.PLAYER_NUM
        score_method.return_value = 2

        self.controller.end_turn(self.GAME_ID)
        assert game.status == Game.MAIN
        assert game.current_player == expected_player

    @patch("catan.logic.catan_controller.DiceHistory.save_all")
    @patch("catan.logic.catan_controller.get_game")
    @patch("catan.logic.catan_controller.get_player_by_order")
    def test_roll_dice(self, get_player_by_order_method, get_game_method, dice_history_save):
        get_game_method.return_value = self._get_game()
        get_player_by_order_method.return_value = self._get_player()
        dice1, dice2 = self.controller.roll_dice(self.GAME_ID, self.USER_ID)

        assert dice1 >= 1
        assert dice1 <= 6
        assert dice2 >= 1
        assert dice2 <= 6

    @patch("catan.logic.catan_controller.Bank.save_all")
    @patch("catan.logic.catan_controller.Player.save_all")
    @patch("catan.logic.catan_controller.get_bank")
    @patch("catan.logic.catan_controller.get_player_by_user_id")
    def test_distribute_resource_from_bank_successful(self, get_player_method, get_bank_method, player_save, bank_save):
        bank = self._get_bank()
        player = self._get_player()
        get_bank_method.return_value = bank
        get_player_method.return_value = player
        card_list = ['wool', 'grain', 'wool']

        self.controller.distribute_resource_from_bank(self.GAME_ID, self.USER_ID, card_list)
        assert player.card_set.wool == 2
        assert player.card_set.grain == 1
        assert bank.card_set.wool == BANK_RESOURCE_NUM - 2
        assert bank.card_set.grain == BANK_RESOURCE_NUM - 1

    @patch("catan.logic.catan_controller.get_tiles_by_number")
    @patch("catan.logic.catan_controller.get_houses")
    @patch("catan.logic.catan_controller.get_towns")
    @patch("catan.logic.catan_controller.CatanBaseController.distribute_resource_from_bank")
    def test_compute_resource_successful(self, distribute_resource_method, get_towns_method, get_houses_method,
                                         get_tiles_method):
        player = self._get_player()
        extra_player = self._get_extra_player()
        tile_list = [
            Tile(game=self.game, type=Tile.GRAIN),
            Tile(game=self.game, type=Tile.ORE),
            Tile(game=self.game, type=Tile.GRAIN),
        ]
        house_list = [
            Construction(game=self.game, type=Construction.HOUSE, owner=player),
            Construction(game=self.game, type=Construction.HOUSE, owner=extra_player),
            Construction(game=self.game, type=Construction.HOUSE, owner=extra_player),
        ]
        town_list = [
            Construction(game=self.game, type=Construction.TOWN, owner=player),
        ]
        get_tiles_method.return_value = tile_list
        get_houses_method.return_value = house_list
        get_towns_method.return_value = town_list

        expected_dict = {
            player.user_id: {'GRAIN': 6, 'ORE': 3},
            extra_player.user_id: {'GRAIN': 4, 'ORE': 2}
        }

        user_resource_dict = self.controller.compute_resource(self.GAME_ID, 8)
        assert user_resource_dict == expected_dict

    @patch("catan.logic.catan_controller.count_houses_by_user_id")
    @patch("catan.logic.catan_controller.count_towns_by_user_id")
    def test_score_successful(self, count_town_method, count_house_method):
        count_house_method.return_value = 3
        count_town_method.return_value = 1

        expected_score = 5

        score = self.controller.score(self.GAME_ID, self.USER_ID)
        assert score == expected_score

    @patch("catan.logic.catan_controller.get_game")
    def test_get_game_info_successful(self, get_game_method):
        controller = CatanBaseController()
        get_game_method.return_value = self._get_game()

        expected = {
            'turn_id': 0,
            'number_of_player': 4,
            'status': Game.SETTLE,
            'state': 'START',
            'current_player_id': 0
        }

        game_info = controller.get_game_info(self.GAME_ID)
        assert game_info == expected

    @patch("catan.logic.catan_controller.get_tiles")
    @patch("catan.logic.catan_controller.get_constructions")
    def test_get_map_resource(self, get_constructions_method, get_tiles_method):
        player = self._get_player()
        extra_player = self._get_extra_player()
        test_tile1 = Tile(type=Tile.GRAIN, x=random.randint(0, 5), y=random.randint(0, 5), number=random.randint(2, 12))
        test_tile2 = Tile(type=Tile.GRAIN, x=random.randint(0, 5), y=random.randint(0, 5), number=random.randint(2, 12))
        test_tile3 = Tile(type=Tile.GRAIN, x=random.randint(0, 5), y=random.randint(0, 5), number=random.randint(2, 12))
        test_construction1 = Construction(type=Construction.ROAD, x=random.randint(0, 5), y=random.randint(0, 5),
                                          z=random.randint(-1, 1), owner=player)
        test_construction2 = Construction(type=Construction.HOUSE, x=random.randint(0, 5), y=random.randint(0, 5),
                                          z=random.randint(-1, 1), owner=player)
        test_construction3 = Construction(type=Construction.TOWN, x=random.randint(0, 5), y=random.randint(0, 5),
                                          z=random.randint(-1, 1), owner=extra_player)

        tiles = [test_tile1, test_tile2, test_tile3]
        constructions = [test_construction1, test_construction2, test_construction3]
        get_tiles_method.return_value = tiles
        get_constructions_method.return_value = constructions

        expected = {
            'tiles': [model_to_dict(tile) for tile in tiles],
            'constructions': [model_to_dict(construction) for construction in constructions]
        }

        map_resource = self.controller.get_map_resource(self.GAME_ID)
        assert map_resource == expected

    @patch("catan.logic.catan_controller.get_player_by_user_id")
    def test_get_player_card_set(self, get_player_method):
        get_player_method.return_value = self._get_player()

        expected = model_to_dict(CardSet())

        result = self.controller.get_player_card_set(self.GAME_ID, self.USER_ID)
        assert result == expected

    @patch("catan.logic.catan_controller.get_bank")
    def test_get_bank_card_set(self, get_bank_method):
        get_bank_method.return_value = self._get_bank()

        expected = model_to_dict(CardSet(
            lumber=BANK_RESOURCE_NUM,
            brick=BANK_RESOURCE_NUM,
            wool=BANK_RESOURCE_NUM,
            grain=BANK_RESOURCE_NUM,
            ore=BANK_RESOURCE_NUM,
            dev_knight=BANK_RESOURCE_NUM,
            dev_one_victory_point=BANK_RESOURCE_NUM,
            dev_road_building=BANK_RESOURCE_NUM,
            dev_monopoly=BANK_RESOURCE_NUM,
            dev_year_of_plenty=BANK_RESOURCE_NUM))

        result = self.controller.get_bank_card_set(self.GAME_ID)
        assert result == expected











