import os

import pygame


class Console(object):
    def __init__(self, grid, lines):
        self.lines = 5
        self.grid = grid
        self.height = self.lines * 20
        self.text_queue = []
        self.posy = 0

    def set_width(self, width):
        self.width = width

    def set_posy(self, posy):
        self.posy = posy

    def draw(self):
        console = pygame.Surface((self.width, self.lines * 20))
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        console.fill((255, 200, 255))

        for i, text in enumerate(self.text_queue):
            line = pygame.Surface((self.width, 20))
            line.fill((255, 255, 200))
            label = myfont.render(text, 1, (0, 0, 0))
            line.blit(label, (0, 0))
            pygame.screen.blit(line, (0, self.posy + i * 20))

    def print(self, text):
        self.text_queue.append(text)
        print(self.text_queue)
        if len(self.text_queue) > self.lines:
            self.text_queue.pop(0)
