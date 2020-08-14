#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .BoardGame import GameConfig


class ChineseChessGameConfig(GameConfig):
    def __init__(self, name = "中国象棋", silent_mode: bool = False, max_turns=99999999, wait_each_turn=False, load_file=None):
        super().__init__(name, silent_mode)
        self.is_default = True
        self.load_file = load_file
        if load_file:
            self.is_default = False
        self.max_turns = max_turns
        self.wait_each_turn = wait_each_turn
