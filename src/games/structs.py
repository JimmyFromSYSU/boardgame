#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Location):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"({self.x+1}, {self.y+1})"
