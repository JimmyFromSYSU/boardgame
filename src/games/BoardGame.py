#!/usr/bin/python
# -*- coding: UTF-8 -*-
import abc
from typing import List


###################################
# 基本元素
###################################

# TODO: Items

class Action():
    def __init__(self):
        self.is_reversible = False


class Board():
    def __init__(self, name, level:int = 1):
        self.name = name
        self.set_level(level)

    @abc.abstractmethod
    def prepare(self) -> bool:
        self.print_info("Preparing")
        return True

    def set_config(self, config):
        self.config = config

    def set_level(self, level):
        self.level = level
        self.prefix = "\t" * level

    def print_info(self, line: str):
        if self.config.silent_mode:
            return
        print(f"{self.prefix}[{self.name}]: {line}")

    @abc.abstractmethod
    def print(self):
        pass


class GameConfig():
    def __init__(self, name, silent_mode: bool = False):
        self.name = name
        self.silent_mode = silent_mode


class GameStatus():
    def __init__(self, board: Board, current_player_id: int):
        self.board = board
        self.action_stack = []
        self.current_player_id = current_player_id
        self.game_end = False
        self.winner_names = []
        self.turns_count = 0


    def push(self, action: Action):
        self.action_stack.append(action)

    def switch(self, player_id: int):
        self.current_player_id = player_id


class Player():
    def __init__(self, name, level:int = 1):
        self.name = name
        self.set_level(level)

    @abc.abstractmethod
    def prepare(self) -> bool:
        self.print_info("Preparing")
        return True

    def set_config(self, config):
        self.config = config

    @abc.abstractmethod
    def play(self, status: GameStatus) -> Action:
        pass

    def set_level(self, level):
        self.level = level
        self.prefix = "\t" * level

    def print_info(self, line: str):
        if self.config.silent_mode:
            return
        print(f"{self.prefix}[{self.name}]: {line}")

    def __str__(self):
        return self.name


class Judge():
    def __init__(self, config: GameConfig, name: str, level: int = 1):
        self.config = config
        self.name = name
        self.set_level(level)

    def set_level(self, level):
        self.level = level
        self.prefix = "\t" * level

    def print_info(self, line: str):
        if self.config.silent_mode:
            return
        print(f"{self.prefix}[{self.name}]: {line}")

    @abc.abstractmethod
    def check_end(self, status: GameStatus, players: List[Player]) -> bool:
        pass


    @abc.abstractmethod
    def validate_action(self, action: Action, status: GameStatus) -> bool:
        pass

    # Return true is this the last Action of the turn
    # Help current player to run the action under the current status
    # Assume the action has been validated.
    @abc.abstractmethod
    def run(self, player: Player, action: Action, status: GameStatus) -> bool:
        pass


# 充当游戏流程与裁判的角色
class BoardGame():
    def __init__(
        self,
        players: List[Player],
        board: Board,
        config: GameConfig,
        level:int = 0
    ):
        self.name = config.name

        assert len(players) > 0, f"MUST have at least 1 player"
        self.players = players
        for player in self.players:
            player.set_level(level + 1)

        self.board = board
        self.config = config
        self.set_level(level)

    def set_level(self, level):
        self.level = level
        self.prefix = "\t" * level

    def print_info(self, line: str):
        if self.config.silent_mode:
            return
        print(f"{self.prefix}[{self.name}]: {line}")


    @abc.abstractmethod
    def init_status(self) -> GameStatus:
        pass

    @abc.abstractmethod
    def init_judge(self) -> Judge:
        pass

    @abc.abstractmethod
    def check_end(self) -> bool:
        pass

    def prepare(self) -> bool:
        self.board.set_config(self.config)
        self.board.prepare()
        for player in self.players:
            player.set_config(self.config)
            if player.prepare() is False:
                return False
        self.status = self.init_status()
        self.judge = self.init_judge()
        if self.config.silent_mode is False:
            self.board.print()

        return True

    # TODO: Move to Judge
    @abc.abstractmethod
    def next_player(self) -> None:
        pass

    def turn(self) -> None:
        turn_end = False
        current_player = self.players[self.status.current_player_id]
        while(turn_end is False):
            action = current_player.play(self.status)
            # TODO: handle invalid steps
            turn_end = self.judge.run(current_player, action, self.status)

    # return list of winner
    @abc.abstractmethod
    def result(self) -> List[Player]:
        pass

    def start(self):
        self.print_info("游戏开始")
        self.prepare()

        # 每一轮的定义：从决定下一个player开始，到该player进行操作，最后到就判断游戏是否结束。
        while(self.judge.check_end(self.status, self.players) is False):
            self.print_info(f"第{self.status.turns_count+1}轮")
            # for next turn
            if self.status.turns_count > 0:
                self.next_player()
            self.turn()
            self.status.turns_count += 1

        self.result()
        self.print_info("游戏结束")


###################################
# AI设计
###################################


class StatusEvaluator():
    def __init__(
        self,
        # level:int = 0
    ):
        pass

    # Return value between [0, 1], 1 is the best
    @abc.abstractmethod
    def evaluateBoard(self, board: Board) -> float:
        pass
