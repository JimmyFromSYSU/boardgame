#!/usr/bin/python
# -*- coding: UTF-8 -*-

# TODO: 将所有ChineseChess相关类打包到ChineseChess.py中，一次性导入
from games.ChineseChessGame import ChineseChessGame
from games.ChineseChessConfig import ChineseChessGameConfig
from games.ChineseChessPlayer import ChineseChessPlayer, ChineseChessAIPlayer, ChineseChessMaxMinAIPlayer
from games.chinese_chess.player.ChineseChessMCTSAIPlayer import ChineseChessMCTSAIPlayer

SILENT_MODE = False
MAX_TURNS = 1000
WAIT_EACH_TURN = True

players = [
    # ChineseChessPlayer("Player1"),
    # ChineseChessPlayer("Player2"),
    # ChineseChessMCTSAIPlayer("Player1", search_level=10),
    ChineseChessMaxMinAIPlayer("Player1", search_level=4),
    ChineseChessMaxMinAIPlayer("Player2", search_level=4),
    # ChineseChessMCTSAIPlayer("Player2", search_level=2),
]
config = ChineseChessGameConfig(
    silent_mode=SILENT_MODE,
    max_turns=MAX_TURNS,
    wait_each_turn=WAIT_EACH_TURN,
    # load_file="data/test03.bd",
    # load_file="data/temp.bd",
    # load_file="data/一虎下山.bd",
    # load_file="data/丹山起凤.bd",
    load_file="data/JJ象棋残局第98关.bd",
)


game = ChineseChessGame(players, config)
game.start()

if SILENT_MODE:
    winners = game.result()
    if len(winners) == 1:
        print(f"结局：{game.turns_count}轮后{winners[0].name}胜利")
    else:
        print(f"结局：{game.turns_count}轮后和局")
