import logging
from gamegridp import keys
import os
import sys
import pygame


class Toolbar(object):
    def __init__(self, grid):
        self._toolbar_buttons = []  # containts the toolbar buttons
        self._toolbar_actions = []  # contains the corresponding actions as string
        self.size = 200
        self.grid = grid

    def __draw_toolbaar__(self):
        """
        Creates a toolbar on the left side of the window
        """
        res_x = self._resolution[0]
        res_y = self._resolution[1]
        toolbar = pygame.Surface((self.toolbar_size, res_y))
        toolbar.fill((255, 255, 255))
        i = 0
        for button in self._toolbar_buttons:
            pygame.screen.blit(button, (self.__grid_width_in_pixels__, i * 20))
            self._draw_queue.append(
                pygame.Rect(0, 0, button.get_width(), button.get_height()))
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))

    def add_toolbar_button(self, img_path, text):
        """
        adds a button to toolbar
        :param img_path: image button
        :param text: button text. This is also the text for the data variable in listen(event,data)
        :return:
        """
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        image = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (20, 20))
        button = pygame.Surface((self.toolbar_size, 20))
        button.fill((255, 255, 255))
        button.blit(image, (5, 5))
        label = myfont.render(text, 1, (0, 0, 0))
        button.blit(label, (25, 0))
        self._toolbar_buttons.append(button)
        self._toolbar_actions.append(text)
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))