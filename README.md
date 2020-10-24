{{wiki/images/image0.tex}}[image]


## 概述

本项目用于实现各类桌游小游戏的游戏流程，AI玩家，对弈平台等。目前正在开发中国象棋的基本游戏流程和AI算法。

### 安装与设置
```
python3 -m pip install termcolor
```

## 基本元素

{{wiki/images/image1.dot}}[dot:桌游小游戏基本元素]

游戏中的基本元素有，Board，Status，Action，Player，Judge，Game等。外部程序通过设置Game，Players，和Config，可以调用该框架。

### Board

游戏中最基本的元素是Board，相当与棋盘，牌桌。其中包含各类游戏物件以及他们的位置，比如棋子，纸牌和骰子等。

Board提供对这些游戏物件的访问和改变，比如改变某个物件的位置。同时也对Board上的基本状态进行检测，比如在中国象棋中判断当前局面上将帅是否照面。

### Action

Action代表某个玩家可以在Board上的一个操作。比如把某个子移动到另一个地方，称为MoveAction。可以通过继承Action实现更高级的动作，比如悔棋操作。MoveAction应当是可以撤销的（roll\_back），这样可以支持悔棋的功能，以及在AI搜索算法中可以利用其实现回溯。

认输也可以是一个Action。

### Status

当前游戏的所有状态，包括Board的格局，当前玩家，获胜玩家，Action的历史栈等。
获得Status就可以知道游戏从初始到现在所有的需要的状态数据，也就是可以通过Status对整个游戏过程进行复盘。

### Player

Player的主要任务是，在自己为主的一轮当中，通过当前的Status，按照顺序作出一个或多个Action。

Player可以是自动的AIPlayer，也可以接收输入的真人玩家，网络玩家等。

### Judge

Judge负责判定Player产生的Action是否合法，并最终负责执行合法的Action。Judge还负责判断游戏是否已经结束，谁是胜利玩家等。Judge通过Rule来进行这些判定，不同的Rule集合可以产生略微不同的游戏规则，比如，可以在象棋中去掉将帅不可照面的规则等。

某些特殊的中国象棋残局添加了额外的限定，这种Judge和Rule解耦分开处理的方式有利于实现这些残局游戏。

Judge还可以用于控制游戏状态和流程，比如实现回退，保存局面等。

### Game

Game控制整个游戏的流程，每个游戏由准备阶段开始，然后经过若干轮，每轮以其中一位Player为主，并由Judge执行操作。最后利用Judge判断游戏结束和得出胜利玩家列表。

## 卡坦岛设计

### 游戏状态转换

 {{images/README/catan_web_player_state_machine.dot}}[dot:卡坦岛玩家状态转换]

### 坐标系设计

## AI设计

AIPlayer可以实现自动的游戏过程，一些通用的AIPlayer可以被不同的游戏重复利用。


### AIPlayer
最基本的AIPlayer是随机的AIPlayer。首先根据规则，获取所有可能的Action，然后在其中随机选择一个Action返回。


### Evaluator

Evaluator是对当前Board局面的一个评估函数，返回一个[0, 1]的值，0代表是最糟糕的局面，1代表是最好的局面。

通过Evaluator，我们可以获得稍好于随机操作的AIPlayer。同样的，可以首先根据规则，获取所有可能的Action。然后执行每个Action，对新的局面调用评估函数，可以得出执行哪一个Action会得到对自己最有利的局面，然后返回这个Action。

### MaxMinAIPlayer

通过极大极小搜索和AlphaBeta剪枝实现多步的搜索。同样的会在搜索的尾部，调用Evaluator对局面进行评估。目前的单机搜索深度能够达到4到5层。

### 置换表

置换表可以用于保存某个局面的搜索评分，这样，下一次搜索到同一个局面时，可以检查是否已经有可用的评分了。通过哈希函数可以将局面映射到一个哈希键值，以及为局面加锁以防止冲突局面。

### 历史表

历史表对每种移动走法打分，并对打分高的的走法优先搜索，使得AlphaBeta剪枝的效率更高。本框架未实现历史表，而是通过对Action导致的新局面的评估函数作为该Action的分数进行排序。

## 对弈平台

目前尚未开始这个阶段的工作。

## TODO

### 基础设施

* 平台化
    * 制作游戏UI。
* Better Engineering
    * 完善Readme文档。
    * Modify all assert to exception

### 中国象棋

* 将中国象棋相关代码移动到一个folder下。
* 判断和棋：长将，长捉，50步无吃子，双方无子可以过河等
* 棋型监测：双炮，马后炮，双车错，侧面虎等。
* 借助latex项目，实现静态棋盘的图片的生成，以及实现动态棋局gif图的生成。
* 整理以前写的[Javascript版本的象棋引擎](https://github.com/JimmyFromSYSU/ChineseChess)

#### AI设计

AI相关内容更加复杂，需要更长时间的test，先Focus在基础设施的建设上，为AI的开发提供足够的工具集合。

* 添加Unit Test，对每个部件单独进行测试，比如player，evaluator，judge等。现在还有许多需要改进的点，每个点都建立对应的test cases。
* 制作工具快速添加新棋局到data中。
* 残局库：将象棋软件中的残局库添加到data中，可以通过残局对AI进行测试。
* 加强残局能力：对将军的action优先搜索，或者对将军的局面提高评分。可以同时计算所有的控子情况。通过对局面计算所有的actions，然后对所有吃子进行加成。
* 假设后手先走，现将后手可能的杀招计算出来，从而能够对actions的排序更加精确。
* 如何训练和制作开局库？
* 添加多线程实现AI加速。
* 当AI意识到自己输了的时候，AI也要选取最长路径来走。
* MCT:
    * MCT还有很多不明确的点，先确认算法，然后实现一种更加readable的版本，并对每个步骤提供足够的unit test。
    * 似乎后手的搜索不太起作用。考虑一个残局，先手优先可以吃子，但是后手可以将死先手。这时，先手陷入到了吃子的陷阱，并没有发现会被将死。测试"data/JJ象棋残局第98关.bd"。
* 实现AI的自动博弈，并计算每次结局的基本情况和整体胜率。
* 实现训练框架对评估函数进行训练。
* 参加中国象棋在线比赛，构建中国象棋在线比赛平台：[UCCI 中国象棋通用引擎协议　版本：3.0](https://www.xqbase.com/protocol/cchess_ucci.htm)


### 五子棋

* 扩展到五子棋的游戏流程。
* 将MaxMinAIPlayer通用化，使得在五子棋等其他游戏中也可以直接复用。

### 卡坦岛
