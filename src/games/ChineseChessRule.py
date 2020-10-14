#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .ChineseChessAction import  ChineseChessMoveAction
from .ChineseChessBoard import ChineseChessBoard, ChineseChess
from .ChineseChessUtils import ChineseChessSide, ChineseChessType
from .ChineseChessUtils import up, down, left, right, up_left, up_right, down_left, down_right

from .structs import Location
from typing import List, Callable


def getPossibleMoveActions(board: ChineseChessBoard, item: ChineseChess) -> List[ChineseChessMoveAction]:
    orign_loc = board.get_location(item)

    result = []

    # Move item to loc
    # return if loc is empty previously
    def add_move_action(loc: Location, ignore_block=False, ignore_empty=False) -> bool:
        block_chess = board.get_chess(loc)
        if block_chess:
            # 如果遇到的是对方的棋子，则添加吃子Action
            if not ignore_block and block_chess.side != item.side:
                result.append(ChineseChessMoveAction(item, orign_loc, loc, block_chess))
            # 如果遇到自己的棋子，则不操作
            return False
        else:
            # 如果遇到空位则添加移动Action
            if not ignore_empty:
                result.append(ChineseChessMoveAction(item, orign_loc, loc, None))
            return True

    def in_box(loc: Location, width: int, height: int, left: int = 0, top: int = 0) -> bool:
        if loc.x >= left and loc.y >= top and loc.x < left + width and loc.y < top + height:
            return True
        else:
            return False

    def in_board(loc: Location) -> bool:
        return in_box(loc, board.width, board.height)

    def in_city(loc: Location) -> bool:
        if item.side == ChineseChessSide.UP:
            return in_box(loc, 3, 3, 3, 0)
        else:
            return in_box(loc, 3, 3, 3, 7)

    def in_half(loc: Location) -> bool:
        if item.side == ChineseChessSide.UP:
            return in_box(loc, 9, 5, 0, 0)
        else:
            return in_box(loc, 9, 5, 0, 5)

    if item.type_ == ChineseChessType.JU:
        for move in [up, down, left, right]:
            # 往一个方向一直走
            loc = move(orign_loc)
            # 遇到边界则退出
            while(in_board(loc)):
                if add_move_action(loc):
                    loc = move(loc)
                else:
                    break
    elif item.type_ == ChineseChessType.MA:
        MA_TWO_MOVES = [
            [up, up_left], [up, up_right], [down, down_left], [down, down_right],
            [left, up_left], [right, up_right], [left, down_left], [right, down_right],
        ]
        for two_moves in MA_TWO_MOVES:
            loc = two_moves[0](orign_loc)
            # 没有绊马脚
            if in_board(loc) and board.get_chess(loc) is None:
                loc = two_moves[1](loc)
                if in_board(loc):
                    add_move_action(loc)
    elif item.type_ == ChineseChessType.PAO:
        for move in [up, down, left, right]:
            # 往一个方向一直走
            loc = move(orign_loc)
            # 遇到边界则退出
            while(in_board(loc)):
                if add_move_action(loc, ignore_block=True):
                    loc = move(loc)
                else:
                    break
            if in_board(loc):
                loc = move(loc)
                # 遇到边界则退出
                while(in_board(loc)):
                    if add_move_action(loc, ignore_empty=True):
                        loc = move(loc)
                    else:
                        break
    elif item.type_ == ChineseChessType.XIANG:
        XIANG_TWO_MOVES = [
            [up_left, up_left], [up_right, up_right], [down_left, down_left], [down_right, down_right],
        ]
        for two_moves in XIANG_TWO_MOVES:
            loc = two_moves[0](orign_loc)
            # 没有绊象脚
            if in_half(loc) and board.get_chess(loc) is None:
                loc = two_moves[1](loc)
                if in_half(loc):
                    add_move_action(loc)
    elif item.type_ == ChineseChessType.SHI:
        SHI_MOVES = [up_left, up_right, down_left, down_right]
        for move in SHI_MOVES:
            loc = move(orign_loc)
            if in_city(loc):
                add_move_action(loc)
    elif item.type_ == ChineseChessType.JIANG:
        JIANG_MOVES = [left, right, up, down]
        for move in JIANG_MOVES:
            loc = move(orign_loc)
            if in_city(loc):
                add_move_action(loc)
    elif item.type_ == ChineseChessType.ZU:
        ZU_MOVES = [up] if item.side == ChineseChessSide.DOWN else [down]
        if in_half(orign_loc) is False:
            ZU_MOVES.extend([left, right])
        for move in ZU_MOVES:
            loc = move(orign_loc)
            if in_board(loc):
                add_move_action(loc)
    return result


def getAllPossibleMoveActions(board: ChineseChessBoard, side: ChineseChessSide) -> List[ChineseChessMoveAction]:
    items = [
        item
        for item in list(board.items.values())
        if item.side == side # make sure use the current color
        if board.get_location(item) # make sure the item has not been captured
    ]
    actions = []
    for item in items:
        actions.extend(getPossibleMoveActions(board, item))
    return actions

def runAction(board: ChineseChessBoard, action: ChineseChessMoveAction):
    board.run(action.item, action.from_, action.to_, action.captured_item)


def rollbackAction(board: ChineseChessBoard, action: ChineseChessMoveAction):
    board.roll_back(action.item, action.from_, action.to_, action.captured_item)


def runActions(board: ChineseChessBoard, actions: List[ChineseChessMoveAction]):
    for action in actions:
        board.run(action.item, action.from_, action.to_, action.captured_item)


def rollbackActions(board: ChineseChessBoard, actions: List[ChineseChessMoveAction]):
    for action in actions:
        board.roll_back(action.item, action.from_, action.to_, action.captured_item)
