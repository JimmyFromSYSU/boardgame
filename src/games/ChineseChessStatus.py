#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .BoardGame import GameStatus
from .ChineseChessBoard import ChineseChessBoard
from .ChineseChessUtils import ChineseChessSide


class ChineseChessGameStatus(GameStatus):
    def __init__(self, board: ChineseChessBoard, current_player_id: int):
        super().__init__(board, current_player_id)
        self.color = "红"
        self.side = ChineseChessSide.UP
