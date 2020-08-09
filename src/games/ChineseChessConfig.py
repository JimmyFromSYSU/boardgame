#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .BoardGame import GameConfig


class ChineseChessGameConfig(GameConfig):
    def __init__(self, name = "中国象棋", silent_mode: bool = False, max_turns=99999999, wait_each_turn=False):
        super().__init__(name, silent_mode)
        self.is_default = True
        self.max_turns = max_turns
        self.wait_each_turn = wait_each_turn
