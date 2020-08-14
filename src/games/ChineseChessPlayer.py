#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .BoardGame import Player
from .ChineseChessBoard import ChineseChessBoard
from .ChineseChessStatus import ChineseChessGameStatus
from .ChineseChessAction import ChineseChessAction, ChineseChessMoveAction
from .ChineseChessUtils import ChineseChessSide
from .ChineseChessRule import getPossibleMoveActions
from .structs import Location
from termcolor import colored
import random
from typing import List, Tuple
import time

class ChineseChessPlayer(Player):
    def __init__(self, name, level:int = 1):
        super().__init__(name, level)
        self.side = None

    def prepare(self) -> bool:
        if super().prepare() is False:
            return False
        return True

    def set_side(self, side: ChineseChessSide):
        self.side = side

    def print_playing_info(self, status: ChineseChessGameStatus):
        if status.color == "绿":
            self.print_info(f"正在下{colored('绿', 'green')}棋")
        elif status.color == "红":
            self.print_info(f"正在下{colored('红', 'red')}棋")
        else:
            self.print_info("playing chess")

    def getAllPossibleMoveActions(self, board: ChineseChessBoard, side: ChineseChessSide) -> List[ChineseChessAction]:
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

    # TODO: 考虑无棋可走的情况：可以返回一个认输Action。
    def play(self, status: ChineseChessGameStatus) -> ChineseChessAction:
        self.print_playing_info(status)

        # 随机移动棋子
        actions = self.getAllPossibleMoveActions(status.board, status.side)
        action = random.choice(actions)
        self.print_info(f"计划把{action.item}从{action.from_}移动到{action.to_}")
        return action


from .ChineseChessEvaluator import ChineseChessEvaluator

class ChineseChessAIPlayer(ChineseChessPlayer):
    def __init__(self, name, level:int = 1):
        super().__init__(name, level)
        self.evaluator = ChineseChessEvaluator()

    # TODO: 考虑无棋可走的情况：可以返回一个认输Action。
    def play(self, status: ChineseChessGameStatus) -> ChineseChessAction:
        assert(self.side == status.side)
        self.print_playing_info(status)

        actions = self.getAllPossibleMoveActions(status.board, status.side)

        max_score = 0
        max_score_action = None
        opposite_side = ChineseChessSide.DOWN if self.side == ChineseChessSide.UP else ChineseChessSide.UP

        for action in actions:
            status.board.run(action.item, action.from_, action.to_, action.captured_item)
            self.evaluator.set_status(opposite_side)
            score = 1 - self.evaluator.evaluateBoard(status.board)
            status.board.roll_back(action.item, action.from_, action.to_, action.captured_item)
            if score >= max_score:
                max_score = score
                max_score_action = action

        action = max_score_action
        self.print_info(f"下一步最高的评估分数为{max_score * 100.0} / 100")

        self.print_info(f"计划把{action.item}从{action.from_}移动到{action.to_}")
        return action



class ChineseChessMaxMinAIPlayer(ChineseChessAIPlayer):
    def __init__(self, name, search_level, level:int = 1):
        super().__init__(name, level)
        self.search_level = search_level

    # 当前棋局，以side为先手，所有action中，让side获得最高分的走法
    def search(self, board: ChineseChessBoard, side: ChineseChessSide, search_level: int, threshold: float = 1) -> Tuple[ChineseChessAction, float]:
        assert search_level >= 1
        MAX_ACTIONS_LIMIT = 10000

        max_score = 0
        max_score_action = None
        actions = self.getAllPossibleMoveActions(board, side)
        opposite_side = ChineseChessSide.DOWN if side == ChineseChessSide.UP else ChineseChessSide.UP

        # 对actions进行排序
        # direct_scores[action]: 如果执行action，新局面对side的直接打分。
        direct_scores = {}
        for action in actions:
            board.run(action.item, action.from_, action.to_, action.captured_item)

            self.evaluator.set_status(opposite_side)
            score = 1 - self.evaluator.evaluateBoard(board)
            direct_scores[action] = score

            board.roll_back(action.item, action.from_, action.to_, action.captured_item)

        actions = sorted(actions, key=lambda action: 1 - direct_scores[action])

        # 限制自身决策时最多所能搜的actions数量
        if side == self.side:
            actions = actions[0:MAX_ACTIONS_LIMIT]

        for action in actions:

            board.run(action.item, action.from_, action.to_, action.captured_item)

            direct_score = direct_scores[action]

            # 确保游戏尚未结束，然后再进行进一步的搜索
            # score: 如果执行action，新局面对side的搜索打分。
            if search_level > 1 and direct_score != 1 and direct_score != 0:
                (t_action, t_score) = self.search(board, opposite_side, search_level - 1, 1 - max_score)
                score = 1 - t_score
            else:
                score = direct_score

            board.roll_back(action.item, action.from_, action.to_, action.captured_item)

            # 更新最高分
            if score > max_score:
                max_score = score
                max_score_action = action
            elif score == max_score:
                max_score_action = random.choice([action, max_score_action])

            # FOR DEBUG:
            # if search_level >= SEARCH_LEVEL - 1:
            #     self.print_info(f"{search_level}：{side}：{action.item}从{action.from_}移动到{action.to_}，直接得分：{direct_score}，搜索得分：{score}， 最高分：{max_score}，阈值：{threshold}")

            # AlphaBeta剪枝
            if max_score >= threshold:
                return (max_score_action, max_score)

        # FOR DEBUG:
        # if search_level >= SEARCH_LEVEL - 1:
        #     self.print_info(f"最终选择：{search_level}：{max_score_action.item}从{max_score_action.from_}移动到{max_score_action.to_}，直接得分：{direct_score}，搜索得分：{score}， 最高分：{max_score}，阈值：{threshold}")
        return (max_score_action, max_score)

    # TODO: 考虑无棋可走的情况：可以返回一个认输Action。
    def play(self, status: ChineseChessGameStatus) -> ChineseChessAction:
        assert(self.side == status.side)

        self.print_playing_info(status)

        start = time.time()

        (action, max_score) = self.search(status.board, status.side, self.search_level)

        end = time.time()

        self.print_info(f"下一步最高的评估分数为{round(max_score * 100.0, 2)} / 100，计算用时：{round(end - start, 2)}秒")

        self.print_info(f"计划把{action.item}从{action.from_}移动到{action.to_}")
        return action
