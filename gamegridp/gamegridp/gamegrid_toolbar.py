import os

import pygame


class Toolbar(object):
    def __init__(self, grid):
        self.width = 200
        self.posx = 0
        self.grid = grid
        self.height = 0
        self.elements = []

    def set_height(self, height):
        self.height = height

    def set_posx(self, posx):
        self.posx = posx

    def draw(self):
        """
        Creates a toolbar on the left side of the window
        """
        toolbar = pygame.Surface((self.width, self.height))
        toolbar.fill((255, 255, 255))
        i = 0
        height = 0
        for element in self.elements:
            pygame.screen.blit(element.get_surface(), (self.posx, height))
            height = height + element.height

    def add_button(self, text, img_path=None):
        """
        adds a button to toolbar
        :param img_path: image button
        :param text: button text. This is also the text for the data variable in listen(event,data)
        :return:
        """
        button = ToolbarButton(self.width, 20, img_path=img_path, text=text)
        self.elements.append(button)
        return button

    def __elements_height__(self):
        height = 0
        for element in self.elements:
            height += element.height
        return height

    def listen(self, event, position: tuple):
        if event == "mouse_left":
            height = 0
            if not position[1] > self.__elements_height__():
                for element in self.elements:
                    if height + element.height > position[1]:
                        return element.listen(event, position)
                    else:
                        height = height + element.height
        else:
            return "no toolbar event"


class ToolbarElement():
    def __init__(self):
        self.height = 25
        self.surface = None
        self.title = ""
        self.event = "no event"

    def get_surface(self):
        return self.surface

    def listen(self, event, position: tuple):
        return self.event


class ToolbarButton(ToolbarElement):

    def __init__(self, width, height, text, img_path):
        super().__init__()
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        button = pygame.Surface((width, 25))
        button.fill((255, 255, 255))
        label = myfont.render(text, 1, (0, 0, 0))

        if img_path != None:
            image = pygame.image.load(img_path)
            image = pygame.transform.scale(image, (25, 25))
            button.blit(image, (2, 0))
            button.blit(label, (25, 5))
        else:
            button.blit(label, (0, 0))

        self.surface = button
        self.event = text

    def listen(self, event, position: tuple):
        return self.event
