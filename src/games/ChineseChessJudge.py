#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import List
from .BoardGame import Judge
from .ChineseChessStatus import ChineseChessGameStatus
from .ChineseChessConfig import ChineseChessGameConfig
from .ChineseChessAction import ChineseChessAction, ChineseChessMoveAction
from .ChineseChessPlayer import ChineseChessPlayer
from .ChineseChessUtils import ChineseChessSide, down
from .utils import getch

class  ChineseChessJudge(Judge):
    def __init__(self, config: ChineseChessGameConfig, level: int = 1):
        name = "中国象棋裁判"
        super().__init__(config, name, level)

    def validate_action(self, action: ChineseChessAction, status: ChineseChessGameStatus) -> bool:
        return True

    # TODO: 增加规则：将帅不能直接相对。
    def check_end(self, status: ChineseChessGameStatus, players: List[ChineseChessPlayer]) -> bool:
        assert len(players) == 2, f"ChineseChessGame MUST have 2 players, {len(players)} are given"
        if status.turns_count >= self.config.max_turns:
            return True

        sides = [ChineseChessSide.UP, ChineseChessSide.DOWN]
        for side in sides:
            king_loc = status.board.get_king_location(side)
            if king_loc is None:
                status.game_end = True
                status.winner_names = [p.name for p in players if p.side != side]
                return True

        # up_king_loc = status.board.get_king_location(ChineseChessSide.UP)
        # down_king_loc = status.board.get_king_location(ChineseChessSide.DOWN)
        # if status.board.no_blocker(up_king_loc, down_king_loc, down):
        if status.board.check_king_meet():
            status.game_end = True
            current_player_id = status.current_player_id
            # 当前玩家下完后，导致了将帅碰面的情况，所以当前玩家的对手是winner。
            status.winner_names = [players[0].name if current_player_id == 1 else players[1].name]
            return True

        if self.config.wait_each_turn:
            c = getch()
            if c == 'q':
                return True

        return False

    # TODO: set type of the action!
    # For now, assume all action is move action and is valid move
    def run(self, player: ChineseChessPlayer, action: ChineseChessAction, status: ChineseChessGameStatus) -> bool:

        board = status.board

        # 判断是否未移动
        # TODO: move to validate_action
        if action.from_ == action.to_:
            self.print_info(f"把{action.item}从{action.from_}移动到{action.to_}不合法，{player}重玩")
            return False

        board.run(action.item, action.from_, action.to_, action.captured_item)

        # 保存走法
        status.push(action)

        if action.captured_item:
            self.print_info(f"把{action.item}从{action.from_}移动到{action.to_}，并吃掉{action.captured_item}。")
        else:
            self.print_info(f"把{action.item}从{action.from_}移动到{action.to_}")
        if self.config.silent_mode is False:
            status.board.print()
        return True
