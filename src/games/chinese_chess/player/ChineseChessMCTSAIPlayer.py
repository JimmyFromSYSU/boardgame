#!/usr/bin/python
# -*- coding: UTF-8 -*-

from games.BoardGame import Player
from games.ChineseChessBoard import ChineseChessBoard
from games.ChineseChessStatus import ChineseChessGameStatus
from games.ChineseChessAction import ChineseChessAction, ChineseChessMoveAction
from games.ChineseChessUtils import ChineseChessSide, ChineseChessType
from games.ChineseChessRule import getAllPossibleMoveActions, runActions, rollbackActions, runAction, rollbackAction
from games.ChineseChessPlayer import ChineseChessMaxMinAIPlayer

from games.structs import Location
from termcolor import colored
from typing import List, Tuple, Optional
import time
import math

C = 0.01

class ChineseChessMCTSTreeNode():
    def __init__(
        self,
        side,
        parent=None,
        action=None,
        level:int = 1,
        key=None,
        lock=None,
    ):
        self.Q = 0  # total reward
        self.Q_from_children = 0
        self.N = 0  # total number of visit
        self.score = None

        self.side = side
        self.opposite_side = ChineseChessSide.DOWN if side == ChineseChessSide.UP else ChineseChessSide.UP

        # self.visited = False    # a node is visited if it's simulated
        self.expanded = False   # a node is expanded if all children are visited
        self.children_done_count = 0

        # 相对于player的win_status
        # = True代表当前player会赢 （不是该Node的side，而是上层player的side）
        self.win_status = None
        self.height = 0

        self.children = None
        self.parent = parent
        self.action = action
        self.visit_id = 0

        self.key = key
        self.lock = lock

    def print_action_link(self):
        if self.parent:
            self.parent.print_action_link()
        if self.action:
            self.action.print(end="")
            # print(f"({self.win_status})", end="")

    # Can return None
    # Make sure not all children are done.
    def best_uct(self):
        max_uct = 0
        best_child = None
        # print(f"len of children: {len(self.children)}")
        # print(f"children_done_count: {self.children_done_count}")
        # print(f"win_status: {self.win_status}")
        for child in self.children:
            # child.action.print(end=": ")
            # print(f"win_status={child.win_status}")
            if child.win_status is not None:
                continue
            uct = child.Q * 1.0 / child.N + C * math.sqrt( math.log(self.N) / child.N)
            # print(f"uct: {uct}")
            # print(child.Q * 1.0 / child.N)
            assert child.Q * 1.0 / child.N > 0
            if uct > max_uct:
                max_uct = uct
                best_child = child
        return best_child

    def traverse(self):
        node = self
        while node.expanded:
            node = node.best_uct()
            # if node and node.action:
            #     print("----------> ", end="")
            #     node.action.print()
            if node == None:
                return None
        return node

    def print_all_children(self):
        for child in self.children:
            win_ratio = child.Q * 1.0 / child.N
            # DEBUG:
            action = child.action
            captured_stmt = ""
            if action.captured_item:
                captured_stmt = f"，并吃掉{action.captured_item}"
            win_ratio_str = f"胜率：{round(child.Q)} / {child.N}\t = {round(win_ratio * 100, 1)}%,\t {child.win_status}"
            print(f"{win_ratio_str}, {action.item}从{action.from_}移动到{action.to_}{captured_stmt}。")


    def best_child(self):
        max_win_ratio = 0
        max_N = 0
        _best_child = None
        for child in self.children:
            win_ratio = child.Q * 1.0 / child.N

            # DEBUG:
            action = child.action
            captured_stmt = ""
            if action.captured_item:
                captured_stmt = f"，并吃掉{action.captured_item}"
            win_ratio_str = f"胜率：{round(child.Q)} / {child.N}\t = {round(win_ratio * 100, 1)}%"
            print(f"{win_ratio_str},\t {child.win_status}, {action.item}从{action.from_}移动到{action.to_}{captured_stmt}。")
            # child.print_all_children()

            # TODO: What if all False?
            if child.win_status == False:
                continue



            if max_N < child.N:
                max_win_ratio = win_ratio
                max_N = child.N
                _best_child = child
        return _best_child, max_win_ratio


# MCTS/Monte Carlo Tree Search
class ChineseChessMCTSAIPlayer(ChineseChessMaxMinAIPlayer):
    def __init__(self, name, search_level, level:int = 1):
        super().__init__(name, search_level, level)

    def simulate(self, leaf, board):
        actions = getAllPossibleMoveActions(board, leaf.side)
        if len(actions) == 0:
            leaf.win_status = (leaf.side != self.side)
            leaf.score = 0
            leaf.N = 1
            leaf.Q = 0
            leaf.expanded = True
        else:
            leaf.children = []
            for action in actions:
                runAction(board, action)

                (new_lock, new_key) = self.hash_table.gen_key_for_action(
                    leaf.lock, leaf.key, action
                )
                child = ChineseChessMCTSTreeNode(
                    side=leaf.opposite_side,
                    level=self.level,
                    parent=leaf,
                    action=action,
                    lock=new_lock,
                    key=new_key
                )
                leaf.children.append(child)

                child.N = 1
                self.evaluator.set_status(child.side)
                child.score = self.evaluator.evaluateBoard(board)
                self.evaluate_counter += 1
                # action.print(end=": ")
                # print(child.score)

                child.Q = 1 - child.score
                if self.side != child.side:
                    child.score = 1 - child.score

                if child.score == 0:
                    leaf.children_done_count += 1
                    child.win_status = False
                elif child.score == 1:
                    leaf.children_done_count += 1
                    child.win_status = True

                if self.side == leaf.side:
                    if child.win_status is True:
                        leaf.win_status = True
                else:
                    if child.win_status is False:
                        leaf.win_status = False

                leaf.N += child.N
                leaf.Q += 1 - child.Q
                leaf.Q_from_children += 1 - child.Q

                rollbackAction(board, action)

            leaf.expanded = True

    # TODO: handle done.
    def backpropagate(self, node, board):
        N = len(node.children)
        Q = node.Q_from_children

        if node.win_status != None:
            if node.parent:
                node.parent.children_done_count += 1

        if node.parent and len(node.parent.children) == node.parent.children_done_count:
            if node.side == self.side:
                node.parent.win_status = False
            else:
                node.parent.win_status = True

        while(node.parent):
            node.parent.N += N
            node.parent.Q += N - Q
            Q = N - Q
            if node.parent.win_status != None:
                if node.parent.parent:
                    node.parent.parent.children_done_count += 1

            if node.parent.parent and len(node.parent.parent.children) == node.parent.parent.children_done_count:
                if node.parent.side == self.side:
                    node.parent.parent.win_status = False
                else:
                    node.parent.parent.win_status = True

            node = node.parent

    def getActions(self, node):
        actions = []
        while(node):
            if node.action:
                actions.append(node.action)
            node = node.parent
        return actions

    # TODO: 考虑无棋可走的情况：可以返回一个认输Action。
    def play(self, status: ChineseChessGameStatus) -> ChineseChessAction:
        assert(self.side == status.side)

        self.print_playing_info(status)

        start = time.time()

        self.evaluate_counter = 0

        (lock, key) = self.hash_table.gen_key_for_board(status.board)
        root = ChineseChessMCTSTreeNode(
            side=self.side,
            level=self.level+1,
            lock=lock,
            key=key,
        )
        #  MAX_SEC = 30
        MAX_COUNT = 3000
        count = 0
        # while time.time() - start < MAX_SEC:
        while count < MAX_COUNT:
            leaf = root.traverse() # leaf = unexpanded node

            if leaf == None:
                # print("leaf == None")
                break

            # print(f"{count}: ", end="")
            # leaf.print_action_link()
            actions = self.getActions(leaf)
            runActions(status.board, reversed(actions))
            self.simulate(leaf, status.board)
            self.backpropagate(leaf, status.board)
            rollbackActions(status.board, actions)
            # print(f"win_status = {leaf.win_status}")
            # print("")
            count += 1

        node, max_score = root.best_child()
        action = node.action

        end = time.time()

        evaluate_counter = self.evaluate_counter
        hit_cache_counter = self.hash_table.hit_cache_counter
        board_counter = evaluate_counter + hit_cache_counter
        hit_cache_ratio = hit_cache_counter * 100.0 / board_counter
        conflict_counter = self.hash_table.conflict_counter
        self.print_info(f"下一步最高的评估分数为{round(max_score * 100.0, 2)} / 100，计算用时：{round(end - start, 2)}秒，评估局面{evaluate_counter}次，使用缓存{hit_cache_counter}次({round(hit_cache_ratio, 2)}%)，哈希冲突{conflict_counter}次。")

        self.print_info(f"计划把{action.item}从{action.from_}移动到{action.to_}")
        return action
