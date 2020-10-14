#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..BoardGame import Player
from .ChineseChessBoard import ChineseChessBoard
from .ChineseChessStatus import ChineseChessGameStatus
from .ChineseChessAction import ChineseChessAction, ChineseChessMoveAction
from .ChineseChessUtils import ChineseChessSide, ChineseChessType
from .ChineseChessRule import getAllPossibleMoveActions
from ..structs import Location
from termcolor import colored
import random
from typing import List, Tuple, Optional
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

    # TODO: 考虑无棋可走的情况：可以返回一个认输Action。
    def play(self, status: ChineseChessGameStatus) -> ChineseChessAction:
        self.print_playing_info(status)

        # 随机移动棋子
        actions = getAllPossibleMoveActions(status.board, status.side)
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

        actions = getAllPossibleMoveActions(status.board, status.side)

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


# TODO: move to BoardGame.py
class BoardHashTable():
    def __init__(self, type_number, location_number, N):
        random.seed(10)
        self.type_number = type_number  # 棋子种类
        self.location_number = location_number  # 位置总数
        self.N = N  # 置换表中可存储棋盘的总数为2^N
        self.board_number = (2 ** N)
        self.lock_list = self.create_random_list()
        self.key_list = self.create_random_list()
        self.hash = {}
        self.side = None
        self.hit_cache_counter = 0
        self.conflict_counter = 0


    # TODO: 将hash从字典换成数组
    # TODO: 局面的评估对不同side是可以对等的吗？需要保证evaluation函数的对称性，即evaluate(board, side) = 1 - evaluate(board, opposite_side)
    # NOTE: side为当前局面先手。
    def get_score(self, lock: int, key: int, min_level: int, side: ChineseChessSide) -> Optional[float]:
        if self.side is None:
            return None

        if key in self.hash and ('lock' in self.hash[key]) and (self.hash[key]['lock'] == lock):
            if self.hash[key]['level'] >= min_level:
                self.hit_cache_counter += 1
                if self.hash[key]['score'] == None:
                    return 1.0
                if side == self.side:
                    return self.hash[key]['score']
                else:
                    return 1 - self.hash[key]['score']
        else:
            return None

    def set_score(self, lock: int, key: int, score: float, level: int, side: ChineseChessSide) -> bool:
        if self.side is None:
            self.side = side
        elif self.side != side:
            score = 1 - score

        # print(f"lock: {lock}, key: {key}, score: {score}, level: {level}")
        if key not in self.hash:
            self.hash[key] = {}
            data = self.hash[key]
        else:
            data = self.hash[key]
            if data['lock'] == lock and data['level'] > level:
                return False
            elif data['lock'] != lock:
                self.conflict_counter += 1

        data['lock'] = lock
        data['level'] = level
        data['score'] = score

        return True

    def create_random_list(self):
        result = []
        # factor = 100000007
        for i in range(self.type_number * self.location_number):
            rnd = random.randrange(self.board_number)
            result.append(rnd)
        return result

    # TODO: how to cache functions
    def get_type_id(self, item) -> int:
        type_map = {
            ChineseChessType.JU: 0,
            ChineseChessType.MA: 1,
            ChineseChessType.PAO: 2,
            ChineseChessType.XIANG: 3,
            ChineseChessType.SHI: 4,
            ChineseChessType.JIANG: 5,
            ChineseChessType.ZU: 6,
        }
        color_map = {
            "红": 0,
            "绿": 7,
        }
        return type_map[item.type_] + color_map[item.color]

    # TODO: how to cache functions
    def get_id(self, item, loc, width=9):
        if loc:
            type_id = self.get_type_id(item)
            loc_id = loc.y * width + loc.x
            id_ = type_id * self.location_number + loc_id
            return id_
        else:
            return None

    def gen_key_for_board(self, board) -> Tuple[int, int]:
        key = 0
        lock = 0

        for item in board.items.values():
            id_ = self.get_id(item, board.get_location(item))
            if id_:
                key = key ^ self.key_list[id_]
                lock = lock ^ self.lock_list[id_]
        return (lock, key)

    def gen_key_for_action(self, previous_lock, previous_key, action) -> Tuple[int, int]:
        id_ = self.get_id(action.item, action.from_)
        previous_lock = previous_lock ^ self.key_list[id_]
        previous_key = previous_key ^ self.lock_list[id_]

        id_ = self.get_id(action.item, action.to_)
        previous_lock = previous_lock ^ self.key_list[id_]
        previous_key = previous_key ^ self.lock_list[id_]

        if action.captured_item:
            id_ = self.get_id(action.captured_item, action.to_)
            previous_lock = previous_lock ^ self.key_list[id_]
            previous_key = previous_key ^ self.lock_list[id_]

        return (previous_lock, previous_key)

    # # TODO:
    # def gen_key_for_action_reverse(self, previous_lock, previous_key, action) -> Tuple[int, int]:
    #     return previous_key


class ChineseChessMaxMinAIPlayer(ChineseChessAIPlayer):
    def __init__(self, name, search_level, level:int = 1):
        super().__init__(name, level)
        self.search_level = search_level

    def prepare(self) -> bool:
        if super().prepare() is False:
            return False
        self.hash_table = BoardHashTable(14, 90, 20)
        return True

    # 当前棋局，以side为先手，所有action中，让side获得最高分的走法
    def search(self, board: ChineseChessBoard, lock: int, key: int, side: ChineseChessSide, search_level: int, threshold_max: float = 1) -> Tuple[ChineseChessAction, float]:
        # self.print_info(f"level: {search_level}, lock: {lock}, key: {key}")

        assert search_level >= 1

        actions = getAllPossibleMoveActions(board, side)
        opposite_side = ChineseChessSide.DOWN if side == ChineseChessSide.UP else ChineseChessSide.UP

        # TODO: 使用历史表对actions进行排序
        # direct_scores[action]: 如果执行action，新局面对side的直接打分。
        direct_scores = {}
        for action in actions:
            # 执行 Action
            board.run(action.item, action.from_, action.to_, action.captured_item)

            # TODO: cache the new_lock and new_key
            # (new_lock, new_key) = self.hash_table.gen_key_for_board(board)
            (new_lock, new_key) = self.hash_table.gen_key_for_action(lock, key, action)
            t_score = self.hash_table.get_score(new_lock, new_key, 0, opposite_side)
            if t_score is None:
                # TODO: 评估函数可以通过action进行更新。
                self.evaluator.set_status(opposite_side)
                t_score = self.evaluator.evaluateBoard(board)
                self.hash_table.set_score(new_lock, new_key, t_score, 0, opposite_side)

                # score == None代表将互相照面，则当前局面的先手获胜。
                if t_score == None:
                    t_score = 1.0
                self.evaluate_counter += 1
            score = 1 - t_score
            direct_scores[action] = score

            # 回退 Action
            board.roll_back(action.item, action.from_, action.to_, action.captured_item)

        actions = sorted(actions, key=lambda action: 1 - direct_scores[action])

        assert len(actions) >= 0
        max_score = 0
        max_score_action = actions[0]

        for action in actions:
            # 执行 Action
            board.run(action.item, action.from_, action.to_, action.captured_item)

            direct_score = direct_scores[action]
            # 确保游戏尚未结束，然后再进行进一步的搜索
            # score: 如果执行action，新局面对side的搜索打分。
            if search_level > 1 and direct_score != 1 and direct_score != 0:
                (new_lock, new_key) = self.hash_table.gen_key_for_action(lock, key, action)
                t_score = self.hash_table.get_score(new_lock, new_key, search_level - 1, opposite_side)
                if t_score is None:
                    (t_action, t_score) = self.search(board, new_lock, new_key, opposite_side, search_level - 1, 1 - max_score)
                score = 1 - t_score
            else:
                score = direct_score

            # 回退 Action
            board.roll_back(action.item, action.from_, action.to_, action.captured_item)

            # 更新最高分
            if score > max_score:
                max_score = score
                max_score_action = action

            # # FOR DEBUG:
            # if search_level >= self.search_level:
            #     captured_stmt = ""
            #     if action.captured_item:
            #         captured_stmt = f"，并吃掉{action.captured_item}"
            #     self.print_info(f"{search_level}：{side}：{action.item}从{action.from_}移动到{action.to_}{captured_stmt}。直接得分：{direct_score}，搜索得分：{score}， 最高分：{max_score}，阈值：{threshold_max}")

            # AlphaBeta剪枝
            # 假设每个局面有N种走法，则最好情况下：
            # * 初始点是A节点
            # * 每个A节点下面有1个A节点，N-1个B节点
            # * 每个B节点下只有一个A节点，（B节点下的所有B节点都有可能被该层的A节点剪枝）
            # 对于4步搜索初始的局面，不减枝需要计算200多万个局面，剪枝只需要计算7万多个局面。
            if max_score >= threshold_max:
                return (max_score_action, max_score)

        self.hash_table.set_score(lock, key, max_score, search_level, side)

        return (max_score_action, max_score)

    # TODO: 考虑无棋可走的情况：可以返回一个认输Action。
    def play(self, status: ChineseChessGameStatus) -> ChineseChessAction:
        assert(self.side == status.side)

        self.print_playing_info(status)

        start = time.time()

        self.evaluate_counter = 0
        self.hash_table.hit_cache_counter = 0
        self.hash_table.conflict_counter = 0

        # TODO: move lock/key to search function so we don't need to add it in parameter list
        (lock, key) = self.hash_table.gen_key_for_board(status.board)

        # for level in range(self.search_level):
        #     (action, max_score) = self.search(status.board, lock, key, status.side, level + 1)
        (action, max_score) = self.search(status.board, lock, key, status.side, self.search_level)

        end = time.time()

        evaluate_counter = self.evaluate_counter
        hit_cache_counter = self.hash_table.hit_cache_counter
        board_counter = evaluate_counter + hit_cache_counter
        hit_cache_ratio = hit_cache_counter * 100.0 / board_counter
        conflict_counter = self.hash_table.conflict_counter
        self.print_info(f"下一步最高的评估分数为{round(max_score * 100.0, 2)} / 100，计算用时：{round(end - start, 2)}秒，评估局面{evaluate_counter}次，使用缓存{hit_cache_counter}次({round(hit_cache_ratio, 2)}%)，哈希冲突{conflict_counter}次。")

        self.print_info(f"计划把{action.item}从{action.from_}移动到{action.to_}")
        return action
