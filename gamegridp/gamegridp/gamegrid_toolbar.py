import os

import pygame


class Toolbar(object):
    def __init__(self, grid):
        self.width = 200
        self.posx = 0
        self.grid = grid
        self.height = 0
        self.elements = []
        self.dirty = 1

    def set_height(self, height):
        self.height = height

    def set_posx(self, posx):
        self.posx = posx

    def draw(self):
        """
        Creates a toolbar on the left side of the window
        """
        if self.dirty == 1:
            toolbar = pygame.Surface((self.width, self.height))
            toolbar.fill((255, 255, 255))
            i = 0
            height = 0
            for element in self.elements:
                toolbar.blit(element.get_surface(), (0, height))
                height = height + element.height
            self.grid.screen_surface.blit(toolbar, (self.posx, 0, self.width, self.height))
            self.grid.schedule_repaint((self.posx, 0, self.width, self.height))
            self.dirty = 0

    def add_button(self, text, img_path=None, color=(255,255,255), border=(255,255,255)):
        """
          Fügt einen Button zur Toolbar hinzu.
          Parameters
          ----------
          text
              Der Text
          img_path
              Pfad zum Bild vor dem Text (optional)
          color
              Die Hintergrundfarbe
          border
              Die Rahmenfarbe
          Returns
              Der erstellte Button
          """
        button = ToolbarButton(self.width, 25, img_path=img_path, text=text, color=color, border=border)
        button.setup(self)
        self.elements.append(button)
        self.dirty = 1
        return button

    def add_label(self, text, img_path=None, color=(255,255,255), border=(255,255,255)):
        """
        Fügt ein Label zur Toolbar hinzu
        Parameters
        ----------
        text
            Der Text
        img_path
            Pfad zum Bild vor dem Text (optional)
        color
            Die Hintergrundfarbe
        border
            Die Rahmenfarbe

        Returns
            Das erstellte Label
        """
        label = ToolbarLabel(self.width, 25, img_path=img_path, text=text, color=color, border=border)
        label.setup(self)
        self.elements.append(label)
        self.dirty = 1
        return label

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
    def __init__(self, width, height, color):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.height = 25
        self.surface = None
        self.background_color = color
        self.title = ""
        self.event = "no event"
        self.parent = None
        self._dirty = 1
        self.width = width
        self.height = height
        self.color = color
        self.clear()

    def setup(self, parent):
        self.parent = parent
        self.dirty = 1

    def get_surface(self):
        return self.surface

    def listen(self, event, position: tuple):
        return self.event, 0
    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if self.parent:
            self.parent._dirty = value

    def clear(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)

    def set_text(self, text, padding_left):
        label = self.myfont.render(text, 1, (0, 0, 0))
        self.surface.blit(label, (padding_left, 5))
        self.dirty = 1

    def set_image(self, img_path):
        image = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (22, 22))
        self.surface.blit(image, (2, 0))
        self.dirty = 1

    def draw_border(self, color, width):
        border_rect = pygame.Rect(0, 0, self.width, self.height - 2)
        pygame.draw.rect(self.surface, color, border_rect, width)
        self.dirty = 1

class ToolbarButton(ToolbarElement):

    def __init__(self, width, height, text, img_path, color=(255,255,255), border=(255,255,255)):
        super().__init__(width, height, color)
        if img_path is not None:
            self.set_image(img_path)
            self.set_text(text, 25)
        else:
            self.set_text(text,2)
        self.event = "button"
        self.data = text

    def listen(self, event, position: tuple):
        return self.event, self.data

class ToolbarLabel(ToolbarElement):
    def __init__(self, width, height, text, img_path, color=(255,255,255), border=(255,255,255)):
        super().__init__(width, height, color)
        self.surface.fill(color)
        if img_path is not None:
            self.set_image(img_path)
            self.set_text(text, 25)
        else:
            self.set_text(text,2)
        self.event = "label"
        self.data = text