#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .BoardGame import StatusEvaluator
from .ChineseChessBoard import ChineseChessBoard, ChineseChess
from .ChineseChessUtils import ChineseChessType, ChineseChessSide
from typing import Dict

# 每个棋子的价值
CHESS_VALUES = {
    ChineseChessType.JU: 90,
    ChineseChessType.MA: 40,
    ChineseChessType.PAO: 45,
    ChineseChessType.XIANG: 20,
    ChineseChessType.SHI: 20,
    ChineseChessType.JIANG: 90,
    ChineseChessType.ZU: 10,
}


# 每个棋子的个数
CHESS_COUNTS = {
    ChineseChessType.JU: 2,
    ChineseChessType.MA: 2,
    ChineseChessType.PAO: 2,
    ChineseChessType.XIANG: 2,
    ChineseChessType.SHI: 2,
    ChineseChessType.JIANG: 1,
    ChineseChessType.ZU: 5,
}

POSITION_FACTOR = 0.1  # best position will add 1% additional value

# max value = 100
MAX_POSITION_VALUE = 100

# For ChineseChessSide.DOWN
CHESS_POSITION_DEFAULT_VALUES = [
    [100, 100, 100, 100, 100, 100, 100, 100, 100],
    [ 90,  90,  90,  90,  90,  90,  90,  90,  90],
    [ 80,  80,  80,  80,  80,  80,  80,  80,  80],
    [ 70,  70,  70,  70,  70,  70,  70,  70,  70],
    [ 60,  60,  60,  60,  60,  60,  60,  60,  60],

    [ 50,  50,  50,  50,  50,  50,  50,  50,  50],
    [ 40,  40,  40,  40,  40,  40,  40,  40,  40],
    [ 30,  30,  30,  30,  30,  30,  30,  30,  30],
    [ 10,  20,  20,  20,  20,  20,  20,  20,  10],
    [  0,  10,  10,  10,   0,  10,  10,  10,   0],
]

CHESS_POSITION_VALUES = {
    ChineseChessType.JU: [
        [100, 100, 100, 100, 100, 100, 100, 100, 100],
        [ 90,  90,  90,  90,  90,  90,  90,  90,  90],
        [ 80,  80,  80,  80,  80,  80,  80,  80,  80],
        [ 70,  70,  70,  70,  70,  70,  70,  70,  70],
        [ 60,  60,  60,  60,  60,  60,  60,  60,  60],

        [ 50,  50,  50,  50,  50,  50,  50,  50,  50],
        [ 40,  40,  40,  40,  40,  40,  40,  40,  40],
        [ 30,  30,  30,  30,  30,  30,  30,  30,  30],
        [ 20,  20,  20,  20,  20,  20,  20,  20,  20],
        [  0,  10,  10,  10,   0,  10,  10,  10,   0],
    ],
    ChineseChessType.PAO: [
        [100, 100, 100,  50,  50,  50, 100, 100, 100],
        [ 90,  90,  90,  70,  60,  70,  90,  90,  90],
        [ 80,  80,  80,  80,  70,  80,  80,  80,  80],
        [ 70,  70,  70,  80,  90,  80,  70,  70,  70],
        [ 60,  60,  60,  80,  90,  80,  60,  60,  60],

        [ 50,  50,  50,  80,  90,  80,  50,  50,  50],
        [ 40,  40,  40,  80,  90,  80,  40,  40,  40],
        [ 30,  30,  30,  70,  80,  70,  30,  30,  30],
        [ 20,  20,  20,  20,  20,  20,  20,  20,  20],
        [  0,  10,  10,  10,   0,  10,  10,  10,   0],
    ],
    ChineseChessType.JIANG: [
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],

        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,  10,   0,   0,   0,   0],
        [  0,   0,   0,  10,  15,  10,   0,   0,   0],
        [  0,   0,   0,  20, 100,  20,   0,   0,   0],
    ],
    ChineseChessType.XIANG: [
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],

        [  0,   0,  60,   0,   0,   0,  60,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [ 20,   0,   0,   0, 100,   0,   0,   0,  20],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,  80,   0,   0,   0,  80,   0,   0],
    ],
    ChineseChessType.SHI: [
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],

        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,  60,   0,  60,   0,   0,   0],
        [  0,   0,   0,   0, 100,   0,   0,   0,   0],
        [  0,   0,   0,  80,   0,  80,   0,   0,   0],
    ],
}


class ChineseChessEvaluator(StatusEvaluator):
    def __init__(
        self,
    ):
        super().__init__()
        self.side = None

    def set_status(self, side: ChineseChessSide):
        self.side = side

    def get_position_value(self, chess: ChineseChess, board: ChineseChessBoard) -> float:
        loc = board.get_location(chess)
        x = loc.x
        y = loc.y
        if chess.side == ChineseChessSide.UP:
            y = board.height - y - 1

        if chess.type_ in CHESS_POSITION_VALUES:
            return CHESS_POSITION_VALUES[chess.type_][y][x]
        else:
            return CHESS_POSITION_DEFAULT_VALUES[y][x]

    # NOTE: make sure evaluate(board, side) = 1 - evaluate(board, opposite_side)
    # TODO: 添加先手优势FIRST_HAND_FACTOR。
    def evaluateBoard(self, board: ChineseChessBoard) -> float:
        assert self.side is not None
        opposite_side = ChineseChessSide.DOWN if self.side == ChineseChessSide.UP else ChineseChessSide.UP

        # count = self.count_chess(board)

        # 判断是否已经有一方的King被吃掉了
        if board.get_king_location(self.side) is None:
            return 0.0
        elif board.get_king_location(opposite_side) is None:
            return 1.0

        # 判断两个king是否照面。
        # TODO: 该逻辑无法保证对称性：evaluate(board, side) = 1 - evaluate(board, opposite_side)
        if board.check_king_meet():
            return 1.0

        # 计算单边可能的最高分
        TOTAL_VALUE = (1 + POSITION_FACTOR) * sum([
            CHESS_VALUES[type_] * CHESS_COUNTS[type_] for type_ in CHESS_VALUES.keys()
        ])

        sum_side = 0
        sum_opposite_side = 0
        for item in board.items.values():
            if board.get_location(item):
                value = CHESS_VALUES[item.type_]
                position_value = self.get_position_value(item, board)
                value += value * POSITION_FACTOR * position_value * 1.0 / MAX_POSITION_VALUE
                if item.side == self.side:
                    sum_side += value
                else:
                    sum_opposite_side += value

        return ((sum_side - sum_opposite_side) + TOTAL_VALUE) / (2.0 * TOTAL_VALUE)
