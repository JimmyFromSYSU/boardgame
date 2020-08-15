#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List, Optional, Dict
from termcolor import colored
from .structs import Location

from .ChineseChessUtils import ChineseChessSide, ChineseChessType, down
from .BoardGame import Board

import json


# 棋子类
class ChineseChess():
    # side can be 'up' or 'down'
    def __init__(self, color: str, name: str, number: str, side: str):
        self.color = color
        self.name = name
        self.number = number
        self.side = side
        self.type_ = None

        if name in ["車", "车"]:
            self.type_ = ChineseChessType.JU
        elif name in ["馬", "马"]:
            self.type_ = ChineseChessType.MA
        elif name in ["炮", "砲"]:
            self.type_ = ChineseChessType.PAO
        elif name in ["象", "相"]:
            self.type_ = ChineseChessType.XIANG
        elif name in ["士", "仕"]:
            self.type_ = ChineseChessType.SHI
        elif name in ["將", "帥", "将", "帅"]:
            self.type_ = ChineseChessType.JIANG
        elif name in ["卒", "兵"]:
            self.type_ = ChineseChessType.ZU

        assert self.type_ is not None


    def get_id(self) -> str:
        return self.color + self.name + self.number

    def print(self):
        print(self, end='')

    def __str__(self):
        if self.color == "绿":
            return colored(self.name, 'green')
        elif self.color == "红":
            return colored(self.name, 'red')
        else:
            return self.name


# TODO: abstract ChessBoard
class ChineseChessBoard(Board):
    def __init__(self, name="中国象棋棋盘", level:int = 1):
        super().__init__(name, level)
        self.width = 9
        self.height = 10

    def prepare(self) -> bool:
        if super().prepare() is False:
            return False

        # item_id -> item, a chess will stay in the items list even though it's captured
        self.items = {}
        # item_id -> location, if a chess is captured, the location is None
        self.locations = {}
        # grids[y][x] = item
        self.grids = [[None for w in range(self.width)] for h in range(self.height)]

        if self.config.is_default:
            side = ChineseChessSide.UP
            self.init_chess(ChineseChess("绿", "車", "01", side), Location(0, 0))
            self.init_chess(ChineseChess("绿", "馬", "01", side), Location(1, 0))
            self.init_chess(ChineseChess("绿", "象", "01", side), Location(2, 0))
            self.init_chess(ChineseChess("绿", "士", "01", side), Location(3, 0))
            self.init_chess(ChineseChess("绿", "將", "01", side), Location(4, 0))
            self.init_chess(ChineseChess("绿", "士", "02", side), Location(5, 0))
            self.init_chess(ChineseChess("绿", "象", "02", side), Location(6, 0))
            self.init_chess(ChineseChess("绿", "馬", "02", side), Location(7, 0))
            self.init_chess(ChineseChess("绿", "車", "02", side), Location(8, 0))
            self.init_chess(ChineseChess("绿", "砲", "01", side), Location(1, 2))
            self.init_chess(ChineseChess("绿", "砲", "02", side), Location(7, 2))
            self.init_chess(ChineseChess("绿", "卒", "01", side), Location(0, 3))
            self.init_chess(ChineseChess("绿", "卒", "02", side), Location(2, 3))
            self.init_chess(ChineseChess("绿", "卒", "03", side), Location(4, 3))
            self.init_chess(ChineseChess("绿", "卒", "04", side), Location(6, 3))
            self.init_chess(ChineseChess("绿", "卒", "05", side), Location(8, 3))

            side = ChineseChessSide.DOWN
            self.init_chess(ChineseChess("红", "車", "01", side), Location(0, 9))
            self.init_chess(ChineseChess("红", "馬", "01", side), Location(1, 9))
            self.init_chess(ChineseChess("红", "相", "01", side), Location(2, 9))
            self.init_chess(ChineseChess("红", "仕", "01", side), Location(3, 9))
            self.init_chess(ChineseChess("红", "帥", "01", side), Location(4, 9))
            self.init_chess(ChineseChess("红", "仕", "02", side), Location(5, 9))
            self.init_chess(ChineseChess("红", "相", "02", side), Location(6, 9))
            self.init_chess(ChineseChess("红", "馬", "02", side), Location(7, 9))
            self.init_chess(ChineseChess("红", "車", "02", side), Location(8, 9))
            self.init_chess(ChineseChess("红", "炮", "01", side), Location(1, 7))
            self.init_chess(ChineseChess("红", "炮", "02", side), Location(7, 7))
            self.init_chess(ChineseChess("红", "兵", "01", side), Location(0, 6))
            self.init_chess(ChineseChess("红", "兵", "02", side), Location(2, 6))
            self.init_chess(ChineseChess("红", "兵", "03", side), Location(4, 6))
            self.init_chess(ChineseChess("红", "兵", "04", side), Location(6, 6))
            self.init_chess(ChineseChess("红", "兵", "05", side), Location(8, 6))
        elif self.config.load_file:
            self.load(self.config.load_file)
        elif self.config.custom_board:
            for color, type_, number, side, x, y in self.config.custom_board:
                self.init_chess(ChineseChess(color, type_, number, side), Location(x, y))

        assert len(self.items) > 0, "MUST have at lease 1 chess"
        return True

    def save(self, file_path):
        chesses = [
            {
                'color': item.color,
                'name': item.name,
                'number': item.number,
                'side': item.side.name,
                'location': self.get_location_dict(item)
            }
            for item in self.items.values()
        ]
        with open(file_path, 'w+') as outfile:
            json.dump(chesses, outfile)

    def load(self, file_path):
        with open(file_path) as json_file:
            chesses = json.load(json_file)
        for chess in chesses:
            color = chess['color']
            name = chess['name']
            number = chess['number']
            side = ChineseChessSide.DOWN if chess['side'] == ChineseChessSide.DOWN.name else ChineseChessSide.UP
            loc = chess['location']
            loc = Location(loc['x'], loc['y']) if loc else None
            self.init_chess(ChineseChess(color, name, number, side), loc)

    def get_king_location(self, side: ChineseChessSide) -> Optional[Location]:
        for item in self.items.values():
            if item.type_ == ChineseChessType.JIANG:
                if item.side == side:
                    return self.get_location(item)
        return None

    def init_chess(self, chess: ChineseChess, location: Optional[Location]) -> bool:
        id_ = chess.get_id()
        assert id_ not in self.items
        self.items[id_] = chess
        if location:
            self.grids[location.y][location.x] = chess
        self.locations[id_] = location
        return True

    # 将chess从from_移除并移出grids
    def capture_chess(self, chess: ChineseChess, from_: Location) -> bool:
        self.locations[chess.get_id()] = None
        self.grids[from_.y][from_.x] = None
        return True

    # 将chess从原位置移动到location，location保证为空
    def move_chess(self, chess: ChineseChess, to_: Location) -> bool:
        from_ = self.locations[chess.get_id()]
        assert from_ is not None
        self.grids[from_.y][from_.x] = None

        self.locations[chess.get_id()] = to_
        self.grids[to_.y][to_.x] = chess
        return True

    # 将被吃的子放回
    def reset_chess(self, chess: ChineseChess, to_: Location):
        assert self.locations[chess.get_id()] is None
        self.locations[chess.get_id()] = to_
        self.grids[to_.y][to_.x] = chess

    def get_location(self, item: ChineseChess) -> Optional[Location]:
        return self.locations[item.get_id()]

    def get_location_dict(self, item: ChineseChess) -> Optional[Dict[str, int]]:
        loc = self.locations[item.get_id()]
        if loc is None:
            return  None
        else:
            return {'x': loc.x, 'y': loc.y}

    def get_chess(self, location: Location) -> Optional[ChineseChess]:
        return self.grids[location.y][location.x]

    def in_board(self, location: Location) -> bool:
        return location.x >= 0 and location.y >= 0 and location.x < self.width and location.y < self.height

    def run(
        self,
        item: ChineseChess,
        from_: Location,
        to_: Location,
        captured_item: Optional[ChineseChess]
    ) -> None:
        # 吃子
        if captured_item:
            self.capture_chess(captured_item, to_)
        # 走子
        self.move_chess(item, to_)

    def roll_back(
        self,
        item: ChineseChess,
        from_: Location,
        to_: Location,
        captured_item: Optional[ChineseChess]
    ) -> None:
        # 撤回走子
        self.move_chess(item, from_)
        # 恢复被吃的
        if captured_item:
            self.reset_chess(captured_item, to_)

    # Return if there is item between loc1 and loc2 excluded.
    # Assume loc1 != loc2
    # Assume we can use move fuc to move from loc1 to loc2 or to outside of the board
    def no_blocker(self, loc1: Location, loc2: Location, move):
        loc = move(loc1)
        while(loc != loc2):
            if self.in_board(loc) is False or self.get_chess(loc):
                return False
            loc = move(loc)
        return True

    def check_king_meet(self) -> bool:
        up_king_loc = self.get_king_location(ChineseChessSide.UP)
        down_king_loc = self.get_king_location(ChineseChessSide.DOWN)
        return self.no_blocker(up_king_loc, down_king_loc, down)

    # TODO: make the print function more clear
    def print(self):
        # get useful character: https://www.fuhaoku.net/fuhao/216.html#:~:text=%E7%AB%96%E7%BA%BF%E7%AC%A6%E5%8F%B7%E5%9C%A8%E9%94%AE%E7%9B%98,%E6%89%93%E5%87%BA%E7%AB%96%E7%BA%BF%E7%9A%84%E7%AC%A6%E5%8F%B7%E3%80%82
        # 制表符：https://www.fuhaoku.net/block/Box_Drawing
        # Chinese character: ︱
        self.print_info("打印当前棋盘")

        for y in range(self.height):
            print(f"{self.prefix}\t*", end = '')

            for x in range(self.width):
                grid = self.grids[y][x]
                if x != 0:
                    print("─", end = '')

                if grid is None:
                    if x == 0:
                        if y == 0:
                            print(" ┌──", end = '')
                        elif y == self.height - 1:
                            print(" └──", end = '')
                        else:
                            print(" ├──", end = '')
                    elif x == self.width - 1:
                        if y == 0:
                            print("─┐ ", end = '')
                        elif y == self.height - 1:
                            print("─┘ ", end = '')
                        else:
                            print("─┤ ", end = '')
                    elif y == 0 or y == self.height / 2:
                        print("─┬──", end = '')
                    elif y == self.height - 1 or y == self.height / 2 -1 :
                        print("─┴──", end = '')
                    else:
                        if x == 4 and y == 1:
                            print("─X──", end = '')  # ❊
                        elif x == 4 and y == 8:
                            print("─X──", end = '')
                        else:
                            print("─┼──", end = '')
                else:
                    if x == 0:
                        print(" ", end = '')
                    else:
                        print("─", end = '')
                    grid.print()
                    if x != self.width -1:
                        print("─", end = '')

            print("*")
            if y == self.height -1:
                break

            print(f"{self.prefix}\t*", end = '')

            for x in range(self.width):
                if x == 0:
                    print(" │ ", end = '')
                elif y == self.height/2-1 and x!=0 and x != self.width-1:
                    if x == 2:
                        print(f"   楚", end = '')
                    elif x == 3:
                        print(f"河   ", end = '')
                    elif x == self.width - 3:
                        print(f"汉界 ", end = '')
                    else:
                        print(f"     ", end = '')
                else:
                    print(f"   │ ", end = '')
            print("*")
