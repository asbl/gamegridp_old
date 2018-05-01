# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:49:29 2018

@author: asieb
"""
import logging
import os
import sys
import pygame
from gamegridp import keys



class GameGrid(object):
    """The Main GameGrid."""

    grid = None

    def __init__(self, title, cell_size=32,
                 columns=8, rows=8, margin=0,
                 background_color=(255, 255, 255), cell_color=(0, 0, 0),
                 img_path=None, img_action="upscale", speed=60, toolbar=False):
        self.grid=self
        self.__is_setting_up__=False
        # Define instance variables
        self.title = title#
        self._logging = logging.getLogger('GameGrid')
        self.__done__ = False
        self.__original_image__ = None
        self._grid = []
        self._speed= speed
        self._actors = []
        self._frame = 0
        self._key_holding_allowed=False
        self._resolution = ()
        self._running = False
        self._cell_margin = 0
        self._collision_type= "cell"
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
            self._collision_type = "bounding_box"
        else:
            self._key_holding_allowed = False
            self._collision_type = "bounding_box"
        self._background_color = background_color
        self._cell_color = cell_color
        # grid and grid-dimensions
        for row in range(rows):
            self._grid.append([])
            for column in range(columns):
                self._grid[row].append(0)
        # Init gui
        x_res = self.__grid_width_in_pixels__ + self.toolbar_size
        y_res = self.__grid_height_in_pixels__ + 30  # 100 pixels for actionbar
        self._resolution = x_res, y_res
        WINDOW_SIZE = (self._resolution[0], self._resolution[1])
        self._logging.info(
            "gamegrid.__init__(): Created windows of dimension: (" + str(self._resolution[0]) + "," + str(self._resolution[1]) + ")")
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
        self.set_image(img_path, img_action)
        self._setup()
        # Draw_Qeue
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))

    def set_image(self, img_path : str, img_action : str = "upscale", size = None):
        self._logging.info("gamegrid.set_image : Set new image with action:"+str(img_action)+" and path:"+str(img_path))
        if img_path is not None:
            self.__original_image__ = pygame.image.load(img_path).convert()
            self._image=self.__original_image__
            self._cell_transparency = 0
            if img_path is not None and img_action == "scale":
                if size is None:
                    self.__original_image__ = pygame.transform.scale(self.__original_image__,
                                                                                      (self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
                else:
                    self.__original_image__ = pygame.transform.scale(self.__original_image__,(size[0],size[1]))
                self._image = pygame.transform.scale(
                    self.__original_image__, (self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
            elif img_path is not None and img_action == "upscale":
                if self._image.get_width() < self.__grid_width_in_pixels__ or self._image.get_height() < self.__grid_height_in_pixels__:
                        self.__original_image__ = pygame.transform.scale(
                            self.__original_image__, (self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
            elif img_path is not None and img_action == "fill":
                if size is None:
                    self.__original_image__ = pygame.transform.scale(self.__original_image__,
                                                                                      (self.cell_size, self.cell_size))
                else:
                    self.__original_image__ = pygame.transform.scale(self.__original_image__,(size[0],size[1]))
                i=0
                j=0
                surface = pygame.Surface((self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
                while(i<self.__grid_width_in_pixels__):
                    j=0
                    while (j<self.__grid_height_in_pixels__):
                        surface.blit(self.__original_image__, (i,j),(0,0, self.__original_image__.get_width(),
                                                                     self.__original_image__.get_height()))
                        j = j + self.__original_image__.get_height()+self.cell_margin
                    i = i + self.__original_image__.get_width()+self.cell_margin
                self.__original_image__= surface
        else:
            self._cell_transparency = None
            self.__original_image__ = pygame.Surface((self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))

        # Crop surface
        cropped_surface = pygame.Surface((self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
        cropped_surface.fill((255,255,255))
        cropped_surface.blit(self.__original_image__, (0, 0),
                             (0, 0, self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
        self._image = cropped_surface


        # draw grid around the cells
        if self._cell_margin > 0:
            i = 0
            while i <= self.__grid_width_in_pixels__:
                pygame.draw.rect(self._image, self._background_color,
                                 [i, 0, self._cell_margin, self.__grid_height_in_pixels__])
                i += self.cell_size + self._cell_margin
            i = 0
            while i <= self.__grid_height_in_pixels__:
                pygame.draw.rect(self._image, self._background_color,
                                 [0, i, self.__grid_width_in_pixels__, self._cell_margin])
                i += self.cell_size + self._cell_margin
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))

    def act(self):
        """
        Should be overwritten in sub-classes. Act is called in every cycle of the mainloop
        """
        pass

    def add_actor(self, actor, location=None):
        """
        Adds an actor to the grid.
        The method is called when a new actor is created.
        """
        self._logging.debug("gamegrid.add_actor() : Actor zum Grid hinzugefügt: " + actor.title +
                            " Location:" + str(location))
        self._actors.append(actor)
        self.repaint_area(actor.bounding_box)
        if location is not None:
            actor.location = location

    def __act_all__(self):
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
        """"""
        return self._cell_size

    @cell_size.setter
    def cell_size(self, value : int):
        """ Sets the cell-size"""
        self._cell_size = value

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

    def __draw_actionbar__(self):
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
                pygame.Rect(0, self.__grid_height_in_pixels__, actionbar.get_width(), actionbar.get_height()))
        if self._running is True:
            path = os.path.join(package_directory, "data", 'pause.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            actionbar.blit(image, (60, 5))
            label = myfont.render("Pause", 1, (0, 0, 0))
            actionbar.blit(label, (85, 5))
            self._draw_queue.append(
                pygame.Rect(0, self.__grid_height_in_pixels__, actionbar.get_width(), actionbar.get_height()))
        # Reset Button:
        path = os.path.join(package_directory, "data", 'reset.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (140, 5))
        label = myfont.render("Reset", 1, (0, 0, 0))
        actionbar.blit(label, (165, 5))
        pygame.screen.blit(actionbar, (0, self.__grid_height_in_pixels__, actionbar.get_width(), actionbar.get_height()))

    @property
    def cell_margin(self):
        """
        returns the margin between cells
        """
        return self._cell_margin

    def draw(self):
        """
        draws the entire window with grid, actionbar and toolbar
        :return:
        """
        self.__draw_grid__()
        self.__draw_actionbar__()
        self.__draw_toolbaar__()

    def __draw_grid__(self):
        """
        Draws grid with all actors in it.
        """
        # Draw the gamegrid-cells
        if self._image is not None:
            pygame.screen.blit(self._image, (0, 0, self.__grid_width_in_pixels__, self.__grid_height_in_pixels__))
        for actor in self._actors:
            actor.next_sprite()
            actor.draw()

    @property
    def actors(self) -> list:
        """
        returns all actors in grid
        :return: a list of all actors
        """
        return self._actors

    @property
    def frame(self) -> int:
        """
        Returns the actual frame
        :return: the value of actual frame
        """
        return self._frame


    @property
    def __grid_width_in_pixels__(self) -> int:
        """ returns the grid with in pixes
        :return: The grid_width in pixels
        """
        return self._grid_columns * self.cell_size + (self._grid_columns + 1) * self._cell_margin

    @property
    def __grid_height_in_pixels__(self) -> int:
        """ returns the grid-height in pixels"""
        height = self._grid_rows * self.cell_size + (self._grid_rows + 1) * self._cell_margin
        return height

    def __grid_dimensions_in_pixels__(self) -> tuple:
        """
        Returns the grid-dimension in pixesls
        :return:
        """
        return self.__grid_width_in_pixels__, self.__grid_height_in_pixels__

    def __check_colliding_cell__(self, actor1, actor2) -> bool:
        """
        Checks if two actors are in the same cell
        :param actor1: first actor
        :param actor2: partner
        :return: true if both actors are on the same cell
        """
        if actor1.is_in_grid(self) and actor2.is_in_grid(self):
            self._logging.debug("gamegrid.colliding() : Colliding? A1:" + str(actor1.location) + ",A2:" + str(actor2.location))
            if actor1.location == actor2.location:
                return True
            else:
                return False

    def __check_colliding_bounding_box__(self, actor1, actor2) -> bool:
        """
        Checks if the bounding boxes of two actors collide
        :param actor1: first actor
        :param actor2: partner
        :return: true if the bounding boxes collide
        """
        if actor1.bounding_box.colliderect(actor2.bounding_box):
            self._logging.debug("gamegrid.colliding_bounding_box: colliding")
            return True
        else:
            self._logging.debug("gamegrid.colliding_bounding_box: not colliding")
            return False

    def __get_bounding_box_collisions__(self, actor):
        """
        Gets all bounding box collisions for one actor
        :param actor:
        :return:
        """
        for partner in actor._colliding_partners:
            if self.__check_colliding_bounding_box__(actor, partner):
                return partner
        return None

    def __get_cell_collisions__(self, actor):
        """
        Gets all cell collisions for one actor
        :param actor:
        :return:
        """
        for partner in actor._colliding_partners:
            if self.__check_colliding_cell__(actor, partner):
                return partner
        return None

    def __collision__(self):
        self._logging.debug("gamegrid.__collision__() - Type:"+str(self._collision_type))
        for actor in self.actors:
            if self._collision_type== "bounding_box":
                partner2 = self.__get_bounding_box_collisions__(actor)
                if partner2 is not None:
                    partner1 = actor
                    self.collision(partner1, partner2)
            else:
                partner2 = self.__get_cell_collisions__(actor)
                if partner2 is not None:
                    partner1 = actor
                    self.collision(partner1, partner2)


    def collision(self, partner1, partner2):
        """
        overwritten by main_method
        :return:
        """

    def get_actors_at_location(self, location:tuple) -> list:
        """
        Get all actors at a specific location
        """
        actors_at_location = []
        for actor in self._actors:
            if actor.get_location() == location:
                actors_at_location.append(actor)
        return actors_at_location

    def get_actors_at_location_by_class(self, location : tuple, class_name : str):
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

    def is_empty_cell(self, cell: tuple) -> bool:
        if not self.get_actors_at_location(cell):
            return True
        else:
            return False

    def __listen__(self):
        """
        Listen to key events
        """
        if self.__is_setting_up__:
            return
        key_pressed = False
        self._logging.debug("gamegrid.__listen__() : Listen...")
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
                self._logging.info("gamegrid.__listen__(): Mouseclick with button:" + str(event.button))
                # Click is in gamegrid
                if pos[0] < self.__grid_width_in_pixels__ and pos[1] < self.__grid_height_in_pixels__ and event.button == 1:
                    cell_location = self.__pixel_to_cell__(pos)
                    self._logging.info("gamegrid.__listen__() : "+str(cell_location))
                    column = cell_location[0]
                    row = cell_location[1]
                    cell_clicked = (column, row)
                    self.__listen_all__("mouse_left", cell_location)
                    self._logging.info("gamegrid.__listen__(): Mouseclick left at grid-position:" +
                                       str(cell_clicked))
                elif pos[0] < self.__grid_width_in_pixels__ and pos[1] < self.__grid_height_in_pixels__ and event.button == 3:
                    cell_location = self.__pixel_to_cell__(pos)
                    self._logging.info("gamegrid.__listen__() : "+str(cell_location))
                    column = cell_location[0]
                    row = cell_location[1]
                    cell_clicked = (column, row)
                    self._logging.info("gamegrid.__listen__(): - Mouseclick right at grid-position:" +
                                       str(cell_clicked))
                    self.__listen_all__("mouse_right", cell_location)
                # Click is in status_bar
                elif pos[1] >= self.__grid_height_in_pixels__:
                    if pos[0] > 5 and pos[0] < 60:
                        if not self._running:
                            self._logging.debug("gamegrid.__listen__(): : Act")
                            return True
                    elif pos[1] >= self.__grid_height_in_pixels__ and pos[0] > 60 and pos[0] < 120 and not self._running:
                        self._running = True
                        self._logging.debug("gamegrid.__listen__(): : Play")
                    elif pos[1] >= self.__grid_height_in_pixels__ and pos[0] > 60 and pos[0] < 120 and self._running:
                        self._running = False
                        self._logging.debug("gamegrid.__listen__() : Pause")
                    elif pos[1] >= self.__grid_height_in_pixels__ and pos[0] > 120 and pos[0] < 180:
                        self._running = False
                        self.reset()
                        self._logging.debug("gamegrid.__listen__() : Reset")
                elif pos[0] > self.__grid_width_in_pixels__:
                    if not pos[1] > len(self._toolbar_actions) * 20:
                        button_index = pos[1] // 20
                        self.__listen_all__("button", self._toolbar_actions[button_index])
            # Event: Key down
            #self._logging.info("gamegrid.__listen__():: keys_pressed count:"+str(pygame.key.get_pressed().count(1)))
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            self._logging.info("gamegrid.__listen__():: keys_pressed : "+str(keys_pressed))
            # self.key_pressed = False
            self.__listen_all__("key", keys.key_pressed_to_key(keys_pressed))
            self._logging.debug("gamegrid.__listen() key-holding allows: "+str(self._key_holding_allowed))
        return False

    def __listen_all__(self, event : str =None, data=None):
        """ Calls listen of grid and all actors """
        self.listen(event, data)
        for actor in self._actors:
            actor.listen(event, data)

    def listen(self, event : str =None, data=None):
        """
        should be overwritten in sub classes
        :param event: The event which was triggered (e.g. mouse-left, key, mouse-right, button...
        :param data: The data submitted by the event (e.g. cell-location
        """
        pass

    def __update__(self, do_act=False, act_disabled : bool =False, listen_disabled : bool = False, collision_disabled = False, draw_disabled=False):
        ''' Part 1:
        For grid an all actors
        listen to events
        react with listen() method
        '''
        if self.__is_setting_up__:
            listen_disabled=True
            collision_disabled=True
            draw_disabled=True
            max_speed=120
        else:
            max_speed = self._max_frames


        if not listen_disabled:
            do_act = self.__listen__()
            ''' Part 2:
                For grid an all actors
                act()
            '''
            if (self._running or do_act) and (not act_disabled):
                self.__act_all__()
        ''' Part 3: Draw actors
            Draw actors in every frame, regardless of speed
        '''
        if not collision_disabled:
            self.__collision__()
        if not draw_disabled:
            self.draw()
            pygame.display.update(self._draw_queue)
            self._draw_queue = []
        self._logging.debug("gamegrid.update() : str(self.clock.tick()")
        self.clock.tick(max_speed)
        self._logging.debug("gamegrid.update() frame:"+ str(self._frame)+"speed:"+str(max_speed))
        if self._frame % 100 == 0:
            self._frame = 1
        else:
            self._frame = self._frame + 1


    def repaint_area(self, rect: pygame.Rect):
        """
        Repaints area on next update
        :param rect: The rectangle which should be redrawn
        """
        self._draw_queue.append(pygame.Rect(rect))

    def remove_actor(self, actor=None, cell: tuple = None):
        """
        Removes actor from grid
        :param actor: Removes the actor from the grid
        :param cell: Removes all actors in one cell from the grid
        :return:
        """
        if cell == None:
            try:
                self._actors.remove(actor)
                actor._remove_from_grid()
            except ValueError:
                self._logging.warning("gamegrid.__remove_actor() : Nicht in Liste vorhanden")
        else:
            actors_at_cell = self.get_actors_at_location(cell)
            self._logging.info("gamegrid.remove_actor(): Remove actor at: " + str(cell))
            for actor in actors_at_cell:
                try:
                    self._logging.info("gamegrid.remove_actor() : remove_actor"+str(actor) + " wird gelöscht...")
                    self._actors.remove(actor)
                    actor._remove_from_grid()
                except ValueError:
                    self._logging.warning("gamegrid.remove_actor() : Nicht in Liste vorhanden")

    def remove_all_actors(self):
        """ remove all actors from the grid
        """
        for actor in self._actors:
            self.remove_actor(actor)

    def reset(self):
        """ resets the grid:
        Sets all actors to their starting positions.
        May not work if custom variables where set
        """
        self.remove_all_actors()
        self._setup()
        self._draw_queue.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))
        self.__update__()

    def stop(self):
        self._running=False

    def run(self):
        self._running=True

    def show(self):
        """
        Starts the mainloop
        """
        # Start Mainloop
        self.__update__()
        while not self.__done__:
            self.__update__()
        pygame.quit()

    def _setup(self):
        self.__is_setting_up__ = True
        self.setup()
        self.__is_setting_up__ = False

    def setup(self):
        """
        should be overwritten in sub_classes
        """
        pass

    def __pixel_to_cell__(self, pos : tuple):
        """
        transforms a pixel-coordinate into a cell coordinate in grid
        :param pos: the position in pixels
        """
        column = \
            (pos[0] - self._cell_margin) // (self.cell_size + self._cell_margin)
        row = \
            (pos[1] - self._cell_margin) // (self.cell_size + self._cell_margin)
        return column, row
