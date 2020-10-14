#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..BoardGame import Action
from .ChineseChessBoard import ChineseChess
from ..structs import Location
from typing import Optional


class ChineseChessAction(Action):
    def __init__(self):
        pass


# TODO: 添加吃子，用于悔棋。
# TODO: 使用item id而不是item本身
class ChineseChessMoveAction(ChineseChessAction):
    def __init__(self, item: ChineseChess, from_: Location, to_: Location, captured_item: Optional[ChineseChess] = None):
        super().__init__()
        self.item = item
        self.from_ = from_
        self.to_ = to_
        self.captured_item = captured_item

    def print(self, end='\n'):
        captured_stmt = ""
        if self.captured_item:
            captured_stmt = f"，并吃掉{self.captured_item}"
        print(f"{self.item}从{self.from_}移动到{self.to_}{captured_stmt}。", end=end)
