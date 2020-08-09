#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List
from .BoardGame import BoardGame
from .ChineseChessStatus import ChineseChessGameStatus
from .ChineseChessConfig import ChineseChessGameConfig
from .ChineseChessBoard import ChineseChessBoard
from .ChineseChessUtils import ChineseChessSide
from .ChineseChessPlayer import ChineseChessPlayer
from .ChineseChessJudge import ChineseChessJudge

class ChineseChessGame(BoardGame):
    def __init__(
        self,
        players: List[ChineseChessPlayer],
        config: ChineseChessGameConfig,
        level:int = 0
    ):
        assert len(players) == 2, f"ChineseChessGame MUST have 2 players, {len(players)} are given"
        board = ChineseChessBoard(level=level+1)
        super().__init__(players=players, board=board, config=config, level=level)

    def init_status(self) -> ChineseChessGameStatus:
        status = ChineseChessGameStatus(self.board, 0)
        return status

    def init_judge(self) -> ChineseChessJudge:
        judge = ChineseChessJudge(self.config, self.level + 1)
        return judge

    def prepare(self) -> bool:
        if super().prepare() is False:
            return False
        self.players[0].set_side(ChineseChessSide.UP)
        self.players[1].set_side(ChineseChessSide.DOWN)
        return True

    # TODO: Move to Judge
    def next_player(self) -> None:
        if self.status.color == "红":
            self.status.color = "绿"
            self.status.side = ChineseChessSide.DOWN
        else:
            self.status.color = "红"
            self.status.side = ChineseChessSide.UP
        self.status.switch((self.status.turns_count)%2)

    def result(self) -> List[ChineseChessPlayer]:
        assert len(self.status.winner_names) <= 1
        if len(self.status.winner_names) == 0:
            self.print_info(f"结局：和局")
            return []
        else:
            winner_name = self.status.winner_names[0]
            self.print_info(f"结局：{winner_name}胜利")
            return [p for p in self.players if p.name == winner_name]
