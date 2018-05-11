import os
import pygame

class Console(object):
    def __init__(self, grid, lines):
        self.lines=5
        self.grid = grid
        self.height = self.lines*20

