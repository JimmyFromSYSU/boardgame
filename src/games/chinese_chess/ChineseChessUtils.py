#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..structs import Location
from enum import Enum

class ChineseChessType(Enum):
    JU = "JU"
    MA = "MA"
    PAO = "PAO"
    XIANG = "XIANG"
    SHI = "SHI"
    JIANG = "JIANG"
    ZU = "ZU"


class ChineseChessSide(Enum):
    UP = "UP"
    DOWN = "DOWN"


def up(loc: Location) -> Location:
    return Location(loc.x, loc.y-1)

def down(loc: Location) -> Location:
    return Location(loc.x, loc.y+1)

def left(loc: Location) -> Location:
    return Location(loc.x-1, loc.y)

def right(loc: Location) -> Location:
    return Location(loc.x+1, loc.y)

def up_left(loc: Location) -> Location:
    return up(left(loc))

def up_right(loc: Location) -> Location:
    return up(right(loc))

def down_left(loc: Location) -> Location:
    return down(left(loc))

def down_right(loc: Location) -> Location:
    return down(right(loc))
