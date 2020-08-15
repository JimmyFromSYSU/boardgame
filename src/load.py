#!/usr/bin/python
# -*- coding: UTF-8 -*-
from games.ChineseChessBoard import ChineseChessBoard
from games.ChineseChessConfig import ChineseChessGameConfig
from games.ChineseChessUtils import ChineseChessSide


SILENT_MODE = False
MAX_TURNS = 1000
WAIT_EACH_TURN = True
custom_board_name = "丹山起凤"
custom_boards = {
    "一虎下山": [
        ("红", "帥", "01", ChineseChessSide.DOWN, 3, 9),
        ("红", "相", "01", ChineseChessSide.DOWN, 2, 9),
        ("红", "相", "02", ChineseChessSide.DOWN, 4, 7),
        ("红", "馬", "01", ChineseChessSide.DOWN, 4, 4),
        ("红", "兵", "01", ChineseChessSide.DOWN, 3, 1),
        ("红", "兵", "02", ChineseChessSide.DOWN, 7, 1),

        ("绿", "將", "01", ChineseChessSide.UP, 5, 1),
        ("绿", "士", "01", ChineseChessSide.UP, 4, 1),
        ("绿", "士", "02", ChineseChessSide.UP, 5, 2),
        ("绿", "車", "01", ChineseChessSide.UP, 4, 8),
        ("绿", "卒", "01", ChineseChessSide.UP, 5, 8),
        ("绿", "卒", "02", ChineseChessSide.UP, 1, 8),
    ],
    "丹山起凤": [
        ("红", "帥", "01", ChineseChessSide.DOWN, 3, 9),
        ("红", "相", "01", ChineseChessSide.DOWN, 4, 7),
        ("红", "仕", "01", ChineseChessSide.DOWN, 3, 7),
        ("红", "馬", "01", ChineseChessSide.DOWN, 5, 9),

        ("红", "車", "01", ChineseChessSide.DOWN, 1, 0),
        ("红", "車", "02", ChineseChessSide.DOWN, 3, 5),
        ("红", "炮", "01", ChineseChessSide.DOWN, 3, 3),
        ("红", "馬", "02", ChineseChessSide.DOWN, 8, 4),

        ("绿", "將", "01", ChineseChessSide.UP, 5, 1),
        ("绿", "士", "01", ChineseChessSide.UP, 5, 0),
        ("绿", "士", "02", ChineseChessSide.UP, 5, 2),
        ("绿", "象", "01", ChineseChessSide.UP, 6, 0),
        ("绿", "象", "02", ChineseChessSide.UP, 6, 4),

        ("绿", "車", "01", ChineseChessSide.UP, 3, 2),
        ("绿", "車", "02", ChineseChessSide.UP, 7, 9),
        ("绿", "砲", "01", ChineseChessSide.UP, 3, 0),
        ("绿", "砲", "02", ChineseChessSide.UP, 8, 9),
        ("绿", "卒", "01", ChineseChessSide.UP, 2, 8),
        ("绿", "卒", "02", ChineseChessSide.UP, 4, 8),
    ],
}

config = ChineseChessGameConfig(
    silent_mode=SILENT_MODE,
    max_turns=MAX_TURNS,
    wait_each_turn=WAIT_EACH_TURN,
    # load_file="data/conflict_curr_733103_1770994.bd"
    # load_file="data/conflict_prev_733103_2950783.bd"
    custom_board = custom_boards[custom_board_name],
)

board = ChineseChessBoard(level=0)
board.set_config(config)
board.prepare()
board.print()
board.save(f"data/{custom_board_name}.bd")
