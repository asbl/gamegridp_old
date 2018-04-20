# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""


import logging
import math
import pygame
import sys


class Actor(object):
    title = ""
    grid = None
    surface = None
    is_rotatable = False
    logging = None

    def __init__(self, title, grid, location, heading='E', img_path=None, img_action="scale"):
        self.log()
        self.title = title
        self.grid=grid
        self.location=location
        self.direction=0
        cell_size=self.grid.cell_size
        # Set Actor image
        cell_size=(grid.cell_size, grid.cell_size)
        if img_path != None and img_action == "scale":
            self.surface = pygame.image.load(img_path)
            self.surface = pygame.transform.scale(self.surface, (cell_size,cell_size))
        if img_path != None and img_action == "crop":
            self.surface = pygame.image.load(img_path)
            cropped_surface = pygame.Surface()
            cropped_surface.blit(self.surface, (0, 0), (0, 0, self.grid.grid_width(), self.grid.grid_height()))
            self.surface = cropped_surface
        if img_path != None and img_action == "do_nothing":
            self.surface = pygame.image.load(img_path)
        self.logging.debug("Target-Location:" + str(self.location))
        if heading == 'S':
            self.direction=270
        try:
            grid.add_actor(self,location)
        except ValueError:
            self.logging.error("Achtung.... kein Grid angegeben! ")
        self.logging.debug("Actor "+title+" wurde initialisiert")


    def log(self):
        self.logging = logging.getLogger('actor-'+self.title)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self.logging.debug("Location set")
        self._location = value
        self.grid.update(act_disabled=True)

    @property
    def direction(self):
        """ Gets the direction of actor """
        return self._direction

    @direction.setter
    def direction(self, value):
        self.logging.debug("Direction set"+ str(value))
        self._direction = value
        self.grid.update(act_disabled=True)

    def listen(self, key, data):
        pass

    def act(self):
        pass

    def setX(self, x):
        self.location[0] = x

    def setY(self, y):
        self.location[1] = y

    def set_location(self, location):
        self.location = location

    def turn_left(self):
        if (self.direction < 270):
            self.set_direction(self.direction+90)
        else:
            self.set_direction(0)
        self.logging.debug("Richtung:"+str(self.direction))

    def turn_right(self):
        if (self.direction > 0):
            self.set_direction(self.direction-90)
        else:
            self.set_direction(270)
        self.logging.debug("Richtung:"+str(self.direction))

    def move(self):
        target = self.look_forward()
        if (self.is_location_in_grid(target)):
            self.location = target
        self.logging.debug("self"+str(self.location)+", target"+str(target))

    def set_direction(self, direction):
        self.surface = pygame.transform.rotate(self.surface, -self.direction)
        self.surface = pygame.transform.rotate(self.surface, direction)
        self.direction = direction

    def move_up(self):
        self.set_direction(90)
        self.move()

    def move_right(self):
        self.set_direction(0)
        self.move()

    def move_left(self):
        self.set_direction(180)
        self.move()

    def move_down(self):
        self.set_direction(270)
        self.move()

    def look_forward(self):
        logging.debug("Location:"+ str(self.location)+ "Direction" + str(self.direction))
        loc_x = round(self.location[0] + math.cos(math.radians(self.direction)))
        loc_y = round(self.location[1] - math.sin(math.radians(self.direction)))
        return loc_x, loc_y

    def is_move_valid(self):
        if self.is_location_in_grid(self.look_forward()):
            return True
        else:
            return False

    def is_location_in_grid(self, location):
        if location[0] > self.grid.grid_columns - 1:
            return False
        elif location[1] > self.grid.grid_rows - 1:
            return False
        elif location[0] < 0 or location[1]<0:
            return False
        else :
            return True

    def get_location(self):
        return self.location

    def get_neighbours(self):
        locations = []
        y_pos = self.location[0]
        x_pos = self.location[1]
        locations.append([x_pos+1, y_pos])
        locations.append([x_pos+1, y_pos+1])
        locations.append([x_pos, y_pos+1])
        locations.append([x_pos-1, y_pos+1])
        locations.append([x_pos-1, y_pos])
        locations.append([x_pos-1, y_pos-1])
        locations.append([x_pos, y_pos-1])
        locations.append([x_pos+1, y_pos-1])
        return locations

    def hasImage(self):
        if self.surface==None:
            return False
        else:
            return True

    def mouse_pressed(self,location):
        pass

    def draw(self):
        if self.hasImage():
            column=self.location[0]
            row=self.location[1]
            cell_margin=self.grid.cell_margin
            cell_size=self.grid.cell_size
            if self.surface.get_width() > cell_size:
                overlapping_x=(self.surface.get_width()- cell_size)/2
            else:
                overlapping_x = 0

            if self.surface.get_height() > cell_size:
                overlapping_y=(self.surface.get_height()- cell_size)/2
            else:
                overlapping_y = 0

            cell_left = cell_margin + (cell_margin + cell_size) * column - overlapping_x
            cell_top =  cell_margin + (cell_margin + cell_size) * row - overlapping_y
            pygame.screen.blit(self.surface,(cell_left,cell_top))

def main():
    import gamegrid
    grid=gamegrid.GameGrid("My Grid", cell_size=64, columns=4, rows=4,margin=10)
    grid.log()
    python=Actor("Python",grid, (4,4), )
    grid.show()


if __name__ == "__main__":
    main()
