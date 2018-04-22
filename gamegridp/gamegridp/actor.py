# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""


import logging
import math
import pygame


class Actor(object):
    title = ""
    grid = None
    __original_image__ = None #
    image = None
    is_rotatable = False
    logging = None
    is_flipped = False

    def __init__(self, title, grid, location,img_path=None, img_action="do_nothing", img_heading="E"):
        self.log()
        self.title = title
        self.grid = grid
        self._location = location
        self._direction = 0
        # Set Actor image
        cell_size=(grid.cell_size, grid.cell_size)
        self.logging.debug("Target-Location:" + str(self.location))
        self.__original_image__ = pygame.image.load(img_path).convert_alpha()
        self.image = self.__original_image__
        if img_action=="scale":
            self.image_transform("scale")
        if img_action=="crop":
            self.image_transform("crop")
        if img_action=="do_nothing":
            self.image_transform("do_nothing")
        if img_heading == 'S':
            self.direction = 270
        elif img_heading == 'E':
            self.direction = 0
        elif img_heading == 'W':
            self.direction = 180
        elif img_heading == 'N':
            self.direction = 90
        try:
            grid.add_actor(self,location)
        except ValueError:
            self.logging.error("Achtung.... kein Grid angegeben! ")
        self.logging.debug("Actor "+title+" wurde initialisiert")

    def flip_x(self):
        """
        Mirrors image over y-axis. x-Coordinates are flipped.
        Actor is turned by 180 degrees.
        is_rotatable should be False.
        """
        if self.is_flipped:
            self.grid.draw_queue.append(pygame.Rect(self.image_rect))
            self.image = pygame.transform.flip(self.__original_image__, False, False)
            self.grid.draw_queue.append(pygame.Rect(self.image_rect))
            self.turn_left(180)
            self.is_flipped = False
        else:
            self.grid.draw_queue.append(pygame.Rect(self.image_rect))
            self.image = pygame.transform.flip(self.__original_image__, True, False)
            self.grid.draw_queue.append(pygame.Rect(self.image_rect))
            self.turn_left(180)
            self.is_flipped=True

    def image_transform(self, img_action, data=None):
        cell_size = self.grid.cell_size
        self.grid.draw_queue.append(pygame.Rect(self.image_rect))
        if img_action == "scale":
            if data is None:
                self.image = pygame.transform.scale(self.__original_image__, (cell_size, cell_size))
            else:
                self.image = pygame.transform.scale(self.__original_image__, (data[0], data[1]))
        elif img_action == "crop":
            cropped_surface = pygame.Surface()
            cropped_surface.blit(self.__original_image__, (0, 0),
                                 (0, 0, self.grid.grid_width(), self.grid.grid_height()))
            self.image = cropped_surface
        elif img_action == "do_nothing":
            self.image = self.__original_image__
        self.__original_image__=self.image
        self.grid.draw_queue.append(pygame.Rect(self.image_rect))

    def log(self):
        self.logging = logging.getLogger('actor-'+self.title)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self.logging.debug("Location set")
        self.grid.draw_queue.append(pygame.Rect(self.image_rect))
        self._location = value
        self.grid.draw_queue.append(pygame.Rect(self.image_rect))
        self.grid.update(act_disabled=True, listen_disabled=True)

    @property
    def direction(self):
        """ Gets the direction of actor """
        return self._direction

    @direction.setter
    def direction(self, value):
        self.logging.debug("Direction set"+ str(value))
        logging.info("rotated by "+str(value)+" degrees")
        if self.is_rotatable:
            # Rotate back to old location
            self.grid.draw_queue.append(pygame.Rect(self.image_rect))
            self.image = pygame.transform.rotate(self.__original_image__, value)
            self._direction = value
            self.grid.draw_queue.append(pygame.Rect(self.image_rect))
            self.grid.update(act_disabled=True, listen_disabled=True)
        else:
            self._direction = value

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

    def turn_left(self, degrees=90):
        direction = self.direction + degrees
        if self.direction > 360:
            direction = direction % 360
        self.direction = direction
        self.logging.debug("Richtung:"+str(self.direction))

    def turn_right(self, degrees):
        direction = self.direction - degrees
        if self.direction < 0:
            direction = direction % 360
        self.direction = direction
        self.logging.debug("Richtung:"+str(self.direction))

    def move_to(self, location):
        target = location
        if self.is_location_in_grid(target):
            self.location = target

    def move(self, distance=1):
        target = self.look_forward()
        self.logging.debug("self"+str(self.location)+", target"+str(target))
        target = self.look_forward(distance)
        if self.is_location_in_grid(target):
            self.location = target
        self.logging.debug("self"+str(self.location)+", target"+str(target))


    def move_up(self):
        self.direction=90
        self.move()

    def move_right(self):
        self.direction = 0
        self.move()

    def move_left(self):
        self.direction = 180
        self.move()

    def move_down(self):
        self.direction = 270
        self.move()

    def look_forward(self, distance=1):
        logging.debug("Location:"+ str(self.location)+ "Direction" + str(self.direction))
        loc_x = round(self.location[0] + math.cos(math.radians(self.direction))*distance)
        loc_y = round(self.location[1] - math.sin(math.radians(self.direction))*distance)
        return loc_x, loc_y

    def is_valid_move(self):
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
        if self.image is None:
            return False
        else:
            return True

    def mouse_pressed(self,location):
        pass

    def get_image_postion(self):
        """
        Gets coordinates of top-left image position
        :return: location (x,y)
        """
        column = self.location[0]
        row = self.location[1]
        cell_margin = self.grid.cell_margin
        cell_size = self.grid.cell_size
        if self.image.get_width() > cell_size:
            overlapping_x = (self.image.get_width() - cell_size) / 2
        else:
            overlapping_x = 0

        if self.image.get_height() > cell_size:
            overlapping_y = (self.image.get_height() - cell_size) / 2
        else:
            overlapping_y = 0

        cell_left = cell_margin + (cell_margin + cell_size) * column - overlapping_x
        cell_top = cell_margin + (cell_margin + cell_size) * row - overlapping_y

        return cell_left, cell_top

    @property
    def image_rect(self):
        cell_left, cell_top = self.get_image_postion()
        width=self.image.get_width()
        height = self.image.get_height()
        return pygame.Rect(cell_left, cell_top, width, height)

    def draw(self):
        if self.hasImage():
            cell_left, cell_top = self.get_image_postion()
            pygame.screen.blit(self.image, (cell_left, cell_top))

def main():
    import gamegrid
    grid=gamegrid.GameGrid("My Grid", cell_size=64, columns=4, rows=4,margin=10)
    grid.log()
    python=Actor("Python",grid, (4,4), )
    grid.show()


if __name__ == "__main__":
    main()
