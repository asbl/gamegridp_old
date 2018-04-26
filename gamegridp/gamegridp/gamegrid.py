# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:49:29 2018

@author: asieb
"""
import logging
import os
import sys

import pygame


class GameGrid(object):
    """The Main GameGrid."""

    def __init__(self, title, cell_size=32,
                 columns=8, rows=8, margin=0,
                 background_color=(255, 255, 255), cell_color=(0, 0, 0),
                 img_path=None, img_action="scale", log=True, speed=60, toolbar=False):

        # Define instance variables
        self.title = title#
        self._logging = False
        if log is True:
            self.log()
        self.__done__ = False
        self.__original_image__ = None
        self._grid = []
        self._actors = []
        self._frame = 0
        self._key_holding_allowed=False
        self._resolution = ()
        self._running = False
        self._cell_margin = 0
        self._image = None
        self._cell_transparency = 0
        self._clock = None
        self._grid_rows = 0
        self._grid_columns = 0
        self._background_color = (255, 255, 255)
        self._cell_color = (0, 0, 0)
        self._draw_queue = []  # a queue of rectangles
        self._key_pressed = False
        self._key = 0
        self._max_frames = speed
        self._animated = False
        self._toolbar_buttons = []  # containts the toolbar buttons
        self._toolbar_actions = []  # contains the corresponding actions as string
        self.toolbar = toolbar
        if self.toolbar == True:
            self.toolbar_size = 200
        else:
            self.toolbar_size = 0
        """
        Initialises the grid
        """
        # attributes
        self._cell_margin = margin
        self._grid_columns = columns
        self._grid_rows = rows
        self._cell_size = cell_size
        if self.cell_size == 1:
            self._key_holding_allowed = True
        else:
            self._key_holding_allowed = False
        self._background_color = background_color
        self._cell_color = cell_color
        # grid and grid-dimensions
        for row in range(rows):
            self._grid.append([])
            for column in range(columns):
                self._grid[row].append(0)
        # Init gui
        x_res = self.grid_width_in_pixels + self.toolbar_size
        y_res = self.grid_height_in_pixels + 30  # 100 pixels for actionbar
        self._resolution = x_res, y_res
        WINDOW_SIZE = (self._resolution[0], self._resolution[1])
        self._logging.info(
            "Created windows of dimension: (" + str(self._resolution[0]) + "," + str(self._resolution[1]) + ")")
        # Init pygame
        pygame.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(title)
        pygame.screen.fill((255, 255, 255))
        # Init clock
        self.clock = pygame.time.Clock()
        # time of last frame change
        self.last_update = pygame.time.get_ticks()
        # current frame
        self._frame = 0
        pygame.init()
        # image
        if img_path is not None:
            self.__original_image__ = pygame.image.load(img_path).convert()
            self._cell_transparency = 0
            if img_path is not None and img_action == "scale":
                self._image = pygame.transform.scale(
                    self.__original_image__, (self.grid_width_in_pixels, self.grid_height_in_pixels))
            elif img_path is not None and img_action == "crop":
                cropped_surface = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
                cropped_surface.blit(self.__original_image__, (0, 0),
                                     (0, 0, self.grid_width_in_pixels, self.grid_height_in_pixels))
                self._image = cropped_surface
        else:
            self._cell_transparency = None
            self._image = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
        if self._cell_margin is not 0:
            for row in range(self._grid_rows):
                for column in range(self._grid_columns):
                    cell_left = self._cell_margin + (self._cell_margin + self.cell_size) * column
                    cell_top = self._cell_margin + (self._cell_margin + self.cell_size) * row
                    # draw cells
                    s = pygame.Surface((self.cell_size, self.cell_size))
                    s.set_alpha(self._cell_transparency)
                    s.fill(self._cell_color)  # this fills the entire surface
                    self._image.blit(s, (cell_left, cell_top, self.grid_width_in_pixels, self.grid_height_in_pixels))

        # draw grid around the cells
        if self._cell_margin > 0:
            i = 0
            while i <= self.grid_width_in_pixels:
                pygame.draw.rect(self._image, self._background_color,
                                 [i, 0, self._cell_margin, self.grid_height_in_pixels])
                i += self.cell_size + self._cell_margin
            i = 0
            while i <= self.grid_height_in_pixels:
                pygame.draw.rect(self._image, self._background_color,
                                 [0, i, self.grid_width_in_pixels, self._cell_margin])
                i += self.cell_size + self._cell_margin

        self.setup()
        # Draw_Qeue
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))

    def act(self):
        """
        Should be overwritten in sub-classes
        """
        pass

    def add_actor(self, actor, location=None):
        """
        Adds an actor to the grid.
        The method is called when a new actor is created.
        """
        self._logging.debug("Actor zum Grid hinzugefügt: " + actor.title +
                            " Location:" + str(location))
        self._actors.append(actor)
        self.repaint_area(actor.bounding_box)
        if location is not None:
            actor.set_location(location)

    def act_all(self, grid_act=True):
        """
        act_all() is called in every cycle of the game loop.
        It acts in the following order:
          1. All actors act
          2. The grid acts
        :param grid_act: Does the grid act
        """
        for actor in self._actors:
            actor.act()
        self.act()

    @property
    def cell_size(self):
        return self._cell_size

    @cell_size.setter
    def cell_size(self, value):
        self._cell_size = value

    def draw_toolbaar(self):
        res_x = self._resolution[0]
        res_y = self._resolution[1]
        toolbar = pygame.Surface((self.toolbar_size, res_y))
        toolbar.fill((255, 255, 255))
        i = 0
        for button in self._toolbar_buttons:
            pygame.screen.blit(button, (self.grid_width_in_pixels, i * 20))
            self._draw_queue.append(
                pygame.Rect(0, 0, button.get_width(), button.get_height()))
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))

    def add_toolbar_button(self, img_path, text):
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

    def draw_actionbar(self):
        """
        Draws the action bar
        """
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        res_x = self._resolution[0]
        res_y = self._resolution[1]
        actionbar = pygame.Surface((res_x, 30))
        actionbar.fill((255, 255, 255))
        # Act Button:
        path = os.path.join(package_directory, "data", 'play.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (5, 5))
        label = myfont.render("Act", 1, (0, 0, 0))
        actionbar.blit(label, (30, 5))
        # Run Button:
        if self._running is False:
            path = os.path.join(package_directory, "data", 'run.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            actionbar.blit(image, (60, 5))
            label = myfont.render("Run", 1, (0, 0, 0))
            actionbar.blit(label, (85, 5))
            self._draw_queue.append(
                pygame.Rect(0, self.grid_height_in_pixels, actionbar.get_width(), actionbar.get_height()))
        if self._running is True:
            path = os.path.join(package_directory, "data", 'pause.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            actionbar.blit(image, (60, 5))
            label = myfont.render("Pause", 1, (0, 0, 0))
            actionbar.blit(label, (85, 5))
            self._draw_queue.append(
                pygame.Rect(0, self.grid_height_in_pixels, actionbar.get_width(), actionbar.get_height()))
        # Reset Button:
        path = os.path.join(package_directory, "data", 'reset.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (140, 5))
        label = myfont.render("Reset", 1, (0, 0, 0))
        actionbar.blit(label, (165, 5))
        pygame.screen.blit(actionbar, (0, self.grid_height_in_pixels, actionbar.get_width(), actionbar.get_height()))

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def cell_margin(self):
        return self._cell_margin

    def draw(self):
        self.draw_grid()
        self.draw_actionbar()
        self.draw_toolbaar()

    def draw_grid(self):
        """
        Draws grid with all actors in it.
        """
        # Draw the gamegrid-cells
        if self._image is not None:
            pygame.screen.blit(self._image, (0, 0, self.grid_width_in_pixels, self.grid_height_in_pixels))
        for actor in self._actors:
            actor.next_sprite()
            actor.draw()

    @property
    def actors(self):
        return self._actors

    @property
    def frame(self):
        return self._frame

    @property
    def grid_width_in_pixels(self):
        return self._grid_columns * self.cell_size + (self._grid_columns + 1) * self._cell_margin

    @property
    def grid_height_in_pixels(self):
        height = self._grid_rows * self.cell_size + (self._grid_rows + 1) * self._cell_margin
        return height

    def grid_dimensions(self):
        return self.grid_width_in_pixels, self.grid_height_in_pixels

    def colliding(self, actor1, actor2, cell_based: bool = True):
        if cell_based:
            if actor1.is_in_grid(self) and actor2.is_in_grid(self):
                self._logging.info("Colliding? A1:" + str(actor1.location) + ",A2:" + str(actor2.location))
                if actor1.location == actor2.location:
                    return True
                else:
                    return False
        #else:
        #    if pygame.sprite.collide_rect(actor1.bounding_box,actor2.bounding_box):
         #       return True
         #   else:
         #       return False

    def get_actors_at_location(self, location:tuple):
        """
        Get all actors at a specific location
        """
        actors_at_location = []
        for actor in self._actors:
            if actor.get_location() == location:
                actors_at_location.append(actor)
        return actors_at_location

    def get_actors_at_location_by_class(self, location, class_name):
        """
        Geta all actors of a specific class at a specific location
        """
        actors_at_location = []
        for actor in self._actors:
            if actor.get_location == location and actor.__class__.__name__ == class_name:
                actors_at_location.append(actor)
        return actors_at_location

    def is_location_in_grid(self, location):
        if location[0] > self._grid_columns - 1:
            return False
        elif location[1] > self._grid_rows - 1:
            return False
        elif location[0] < 0 or location[1] < 0:
            return False
        else:
            return True

    def is_empty(self, cell: list):
        if not self.get_actors_at_location(cell):
            return True
        else:
            return False

    def __listen__(self):
        key_pressed = False
        self._logging.debug("Listen...")
        do_act = False
        for event in pygame.event.get():
            key = False
            cell = False
            # Event: Quit
            if event.type == pygame.QUIT:
                self.__done__ = True
                pygame.quit()
                os._exit(0)
            # Event: Mouse-Button Down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self._logging.info("Mouseclick with button:" + str(event.button))
                # Click is in gamegrid
                if pos[0] < self.grid_width_in_pixels and pos[1] < self.grid_height_in_pixels and event.button == 1:
                    cell_location = self.__pixel_to_cell__(pos)
                    self._logging.info(str(cell_location))
                    column = cell_location[0]
                    row = cell_location[1]
                    cell_clicked = (column, row)
                    self.__listen_all__("mouse_left", cell_location)
                    self._logging.info("Mouseclick left at grid-position:" +
                                       str(cell_clicked))
                elif pos[0] < self.grid_width_in_pixels and pos[1] < self.grid_height_in_pixels and event.button == 3:
                    cell_location = self.__pixel_to_cell__(pos)
                    self._logging.info(str(cell_location))
                    column = cell_location[0]
                    row = cell_location[1]
                    cell_clicked = (column, row)
                    self._logging.info("Mouseclick right at grid-position:" +
                                       str(cell_clicked))
                    self.__listen_all__("mouse_right", cell_location)
                # Click is in status_bar
                elif pos[1] >= self.grid_height_in_pixels:
                    if pos[0] > 5 and pos[0] < 60:
                        if not self._running:
                            self._logging.debug("Act")
                            return True
                    elif pos[1] >= self.grid_height_in_pixels and pos[0] > 60 and pos[0] < 120 and not self._running:
                        self._running = True
                        self._logging.debug("Play")
                    elif pos[1] >= self.grid_height_in_pixels and pos[0] > 60 and pos[0] < 120 and self._running:
                        self._running = False
                        self._logging.debug("Pause")
                    elif pos[1] >= self.grid_height_in_pixels and pos[0] > 120 and pos[0] < 180:
                        self._running = False
                        self.reset()
                        self._logging.debug("Reset")
                elif pos[0] > self.grid_width_in_pixels:
                    if not pos[1] > self._toolbar_actions.len * 20:
                        button_index = pos[1] // 20
                        self.__listen_all__("button", self._toolbar_actions[button_index])
            # Event: Key down
            elif event.type == pygame.KEYDOWN:
                self._key_pressed = True
                self._key = event.key
                if not self._key_holding_allowed and self._key_pressed:
                    self.__listen_all__("key", self._key) # react immediately
                    self._logging.info("__listen__ in gamegrid: key pressed : " + str(event.key) + "status:" + str(self._key_pressed))
            # Event: Key up
            elif event.type == pygame.KEYUP:
                self._key_pressed = False
                self._key = event.key
                self._logging.info(
                    "__listen__ in gamegrid: key released : " + str(event.key) + "status:" + str(self._key_pressed))
                self._logging.info("__listen__: key pressed: " + str(self._key_pressed) + " / holding allowed: :" + str(self._key_holding_allowed))
        if self._key_pressed:
            # self.key_pressed = False
            if self._key_holding_allowed:
                self.__listen_all__("key", self._key)
        print(self._key_holding_allowed)
        return False

    def __listen_all__(self, event=None, data=None):
        # Call listen() method with key and cell in which was clicked
        self.listen(event, data)
        for actor in self._actors:
            actor.listen(event, data)

    def listen(self, event=None, data=None):
        pass

    def update(self, do_act=False, act_disabled=False, listen_disabled=False):
        ''' Part 1:
            For grid an all actors
            listen to events
            react with listen() method
        '''
        if not listen_disabled:
            do_act = self.__listen__()
        ''' Part 2:
            For grid an all actors
            act()
        '''
        '''self.logging.info("Acting... do act:"+str(do_act)+" + running "
                          +str(self.running)+" act disabled"+str(act_disabled))'''
        if (self._running or do_act) and (not act_disabled):
            self.act_all(grid_act=True)
        '''' Part 3: Draw actors'''
        self.draw()
        self._logging.debug(str(self.clock.tick()))
        self.clock.tick(self._max_frames)
        self._frame = self.frame + 1
        pygame.display.update(self._draw_queue)
        self._draw_queue = []

    def repaint_area(self, rect: pygame.Rect):
        """
        Repaints area on next update
        :param rect: The rectangle which should be redrawn
        """
        self._draw_queue.append(pygame.Rect(rect))

    def remove_actor(self, actor=None, cell: list = None):
        if cell == None:
            try:
                self._actors.remove(actor)
                actor.remove_from_grid()
            except ValueError:
                self._logging.warning("Nicht in Liste vorhanden")
        else:
            actors_at_cell = self.get_actors_at_location(cell)
            self._logging.info("Remove actor at: " + str(cell))
            for actor in actors_at_cell:
                try:
                    self._logging.info(str(actor) + " wird gelöscht...")
                    self._actors.remove(actor)
                    actor.remove_from_grid()
                except ValueError:
                    self._logging.warning("Nicht in Liste vorhanden")

    def remove_all_actors(self):
        for actor in self._actors:
            self.remove_actor(actor)

    def reset(self):
        self.remove_all_actors()
        self.setup()
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))
        self.update()

    def show(self):
        """
        Starts the mainloop
        """
        # Start Mainloop
        self.update()
        while not self.__done__:
            self.update()
        pygame.quit()

    def setup(self):
        pass

    def __pixel_to_cell__(self, pos):
        column = \
            (pos[0] - self._cell_margin) // (self.cell_size + self._cell_margin)
        row = \
            (pos[1] - self._cell_margin) // (self.cell_size + self._cell_margin)
        return column, row

    def log(self):
        self._logging = logging.getLogger('gglogger')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        self._logging.addHandler(ch)
