import os

import pygame


class Console(object):
    def __init__(self, grid, lines):
        self.lines = 5
        self.grid = grid
        self.height = self.lines * 20
        self.text_queue = []
        self.posy = 0
        self.width=self.grid.__grid_width_in_pixels__
        self.dirty = 1

    def set_width(self, width):
        self.width = width

    def set_posy(self, posy):
        self.posy = posy

    def draw(self):
        if self.dirty == 1:
            console = pygame.Surface((self.grid.__grid_width_in_pixels__, self.height))
            console.fill((200, 200, 200))
            package_directory = os.path.dirname(os.path.abspath(__file__))
            myfont = pygame.font.SysFont("monospace", 15)
            for i, text in enumerate(self.text_queue):
                line = pygame.Surface((self.width, 20))
                line.fill((200, 200, 200))
                label = myfont.render(text, 1, (0, 0, 0))
                line.blit(label, (0, 0))
                console.blit(line, (0, i * 20))
            print((0,self.posy, self.width, self.height))
            self.grid.screen_surface.blit(console,(0,self.posy, self.width, self.height))
            self.grid.schedule_repaint((0,self.posy, self.width, self.height))
            self.dirty = 0


    def print(self, text):
        self.text_queue.append(text)
        print(self.text_queue)
        if len(self.text_queue) > self.lines:
            self.text_queue.pop(0)
        self.dirty = 1

