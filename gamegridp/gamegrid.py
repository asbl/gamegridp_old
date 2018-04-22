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

    grid = []
    actors = []
    done = False
    cell_size = 16
    grid_rows = 0
    grid_columns = 0
    grid_height = 0
    grid_width = 0
    running = False
    cell_margin = 0
    background_color = (255, 255, 255)
    cell_color = (0, 0, 0)
    surface = None
    img_action = "resize"
    cell_transparency = 0
    logging = None
    threads = []
    __clock = None

    def __init__(self, title, cell_size=32,
                 columns=8, rows=8, margin=0,
                 background_color=(255, 255, 255), cell_color=(0, 0, 0),
                 img_path=None, img_action="scale", log=True, speed=10):
        """
        Initialises the grid
        """
        # Init model
        self.cell_margin = margin
        self.grid_columns = columns
        self.grid_rows = rows
        self.cell_size = cell_size
        self.background_color = background_color
        self.cell_color = cell_color
        self.speed = speed
        for row in range(rows):
            self.grid.append([])
            for column in range(columns):
                self.grid[row].append(0)
        # Init gui
        x_res = self.grid_width()
        y_res = self.grid_height()+30
        if img_path is not None:
            self.cell_transparency = 0
        if img_path is not None and img_action == "scale":
            self.surface = pygame.image.load(img_path)
            self.surface = pygame.transform.scale(
                self.surface, (self.grid_width(), self.grid_height()))
        if img_path is not None and img_action == "crop":
            self.surface = pygame.image.load(img_path)
            cropped_surface = pygame.Surface(
                (self.grid_width(), self.grid_height()))
            cropped_surface.blit(self.surface, (0, 0),
                                 (0, 0, self.grid_width(), self.grid_height()))
            self.surface = cropped_surface

        if log is True:
            self.log()
        self.logging.info("Created windows of dimension: ("
                          + str(x_res) + "," + str(y_res) + ")")
        WINDOW_SIZE = (x_res, y_res)
        pygame.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.init()

    def reset(self):
        self.remove_all_actors()
        self.setup()
        self.update()

    def setup(self):
        pass

    def grid_width(self):
        width = self.grid_columns * self.cell_size + (self.grid_columns+1) * self.cell_margin
        return width

    def grid_height(self):
        height = self.grid_rows * self.cell_size + (self.grid_rows+1) * self.cell_margin
        return height

    def cell_size(self):
        return self.cell_size

    def grid_dimensions(self):
        return (self.grid_width(), self.grid_height())

    def draw_actionbar(self):
        """
        Draws the action bar
        """
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        # Act Button:
        path = os.path.join(package_directory, "data", 'play.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image, (5, (self.grid_height()+5)))
        label = myfont.render("Act", 1, (0, 0, 0))
        pygame.screen.blit(label, (30, (self.grid_height()+5)))
        # Run Button:
        if self.running is False:
            path = os.path.join(package_directory, "data", 'run.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            pygame.screen.blit(image, (60, self.grid_height()+5))
            label = myfont.render("Run", 1, (0, 0, 0))
            pygame.screen.blit(label, (85, (self.grid_height()+5)))
        if self.running is True:
            path = os.path.join(package_directory, "data", 'pause.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            pygame.screen.blit(image, (60, self.grid_height() + 5))
            label = myfont.render("Pause", 1, (0, 0, 0))
            pygame.screen.blit(label, (85, (self.grid_height()+5)))
        # Reset Button:
        path = os.path.join(package_directory, "data", 'reset.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image, (140, self.grid_height() + 5))
        label = myfont.render("Reset", 1, (0, 0, 0))
        pygame.screen.blit(label, (165, (self.grid_height() + 5)))



    def draw_grid(self, grid):
        """
        Draws grid with all actors in it.
        """
        pygame.screen.fill(self.background_color)
        # Draw the gamegrid-cells
        if self.surface is not None:
            pygame.screen.blit(self.surface, (0, 0,
                                              self.grid_width(),
                                              self.grid_height()))
        for row in range(self.grid_rows):
            for column in range(self.grid_columns):
                grid_location = (column, row)
                cell_left = self.cell_margin + (self.cell_margin + self.cell_size) * column
                cell_top = self.cell_margin + (self.cell_margin + self.cell_size) * row

                # draw cells

                s = pygame.Surface((self.cell_size, self.cell_size))
                s.set_alpha(self.cell_transparency)
                s.fill(self.cell_color)  # this fills the entire surface
                pygame.screen.blit(s, (cell_left, cell_top))

        # draw grid around the cells
        i = 0
        while (i <= self.grid_width()):
            pygame.draw.rect(pygame.screen, self.background_color,
                             [i, 0, self.cell_margin, self.grid_height()])
            i += self.cell_size+self.cell_margin
        i = 0
        while (i <= self.grid_height()):
            pygame.draw.rect(pygame.screen, self.background_color,
                             [0, i, self.grid_width(), self.cell_margin])
            i += self.cell_size+self.cell_margin
        # Draw Actors at actual position
        for actor in self.actors:
            actor.draw()

    def add_actor(self, actor, location=None):
        """
        Adds an actor to the grid.
        The method is called when a new actor is created.
        """
        self.logging.debug("Actor zum Grid hinzugefügt: " + actor.title +
                           " Location:"+str(location))
        self.actors.append(actor)
        if location is not None:
            actor.set_location(location)

    def get_actors_at_location(self, location):
        """
        Get all actors at a specific location
        """
        actors_at_location = []
        for actor in self.actors:
            if actor.get_location() == location:
                actors_at_location.append(actor)
        return actors_at_location

    def get_actors_at_location_by_class(self, location, class_name):
        """
        Geta all actors of a specific class at a specific location
        """
        actors_at_location = []
        for actor in self.actors:
            if actor.get_location == location and actor.__class__.__name__ == class_name:
                actors_at_location.append(actor)
        return actors_at_location

    def act(self):
        """
        Should be overwritten in sub-classes
        """
        pass

    def __listen__(self):
            #elf.logging.info("Listen...")
            do_act = False
            for event in pygame.event.get():
                key = False
                cell = False
                # Event: Quit
                if event.type == pygame.QUIT:
                    self.done = True
                    pygame.quit()
                    os._exit(0)
                # Event: Mouse-Button Down
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Click is in gamegrid
                    if pos[0] < self.grid_width() \
                    and pos[1] < self.grid_height():
                        cell_location = self.__pixel_to_cell__(pos)
                        self.logging.info(str(cell_location))
                        column = cell_location[0]
                        row = cell_location[1]
                        cell_clicked = (column, row)
                        self.__listen_all__("mouse", cell_location)
                        self.logging.info("Mouseclick at grid-position:",
                                          str(cell_clicked))
                    # Click is in status_bar
                    elif pos[1] >= self.grid_height() \
                    and pos[0] > 5 and pos[0] < 30:
                        if not self.running:
                            self.logging.info("Act")
                            return True
                    elif pos[1] >= self.grid_height() \
                    and pos[0] > 60 and pos[0] < 120 \
                    and not self.running:
                        self.running = True
                        self.logging.debug("Play")
                    elif pos[1] >= self.grid_height() \
                    and pos[0] > 60 and pos[0] < 120 \
                    and self.running:
                        self.running = False
                        self.logging.debug("Pause")
                    elif pos[1] >= self.grid_height() \
                    and pos[0] > 120 \
                    and pos[0] < 180:
                        self.running = False
                        self.reset()
                        self.logging.debug("Reset")
                # Event: Keydown
                elif event.type == pygame.KEYDOWN:
                    self.__listen_all__(self, "key", key)
                    self.logging.debug("key pressed : "+str(event.key))
            return False

    def __listen_all__(self, event=None, data=None):
        # Call listen() method with key and cell in which was clicked
        # und übergebe den gedrückten
        for actor in self.actors:
            actor.listen(event, data)

    def remove_all_actors(self):
        for actor in self.actors:
            self.actors.remove(actor)
            del actor

    def update(self, do_act=False, act_disabled=False):
        #self.logging.debug("Update...")
        ''' Part 1:
            For grid an all actors
            listen to events
            react with listen() method
        '''
        do_act = self.__listen__()

        ''' Part 2:
            For grid an all actors
            act()
        '''
        '''self.logging.info("Acting... do act:"+str(do_act)+" + running "
                          +str(self.running)+" act disabled"+str(act_disabled))'''
        if (self.running or do_act) and (not act_disabled):
            self.act_all(metoo=True)
        do_act = False
        '''' Part 3: Draw actors'''
        self.draw()
        self.clock.tick(self.speed)
        pygame.display.flip()

    def show(self):
        self.setup()
        """
        Starts the mainloop
        """
        # Start Mainloop
        while not self.done:
            self.update()
        pygame.quit()

    def draw(self):
        self.draw_grid(self.grid)
        self.draw_actionbar()


    def __pixel_to_cell__(self,pos):
        column = \
        (pos[0] - self.cell_margin) // (self.cell_size + self.cell_margin)
        row = \
        (pos[1] - self.cell_margin) // (self.cell_size + self.cell_margin)
        return (column, row)

    def act_all(self, metoo=True):
        for actor in self.actors:
            actor.act()

    def log(self):
        self.logging = logging.getLogger('gglogger')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        self.logging.addHandler(ch)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    grid=GameGrid("My Grid", cell_size=64, columns=4, rows=4, margin=10)
    grid.show()


if __name__ == "__main__":
    main()
