# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""


import logging
import math

import pygame


class Actor(object):

    def __init__(self, grid, location=(0,0), title="Actor", img_path=None, img_action="do_nothing", img_heading="E", log=False):
        # define instance variables
        self.title = title
        self._logging=None
        self.log()
        # Define instance variables
        self._original_images = []  # All images stores for actor
        self._image = None
        self._image_index = 0
        self._is_rotatable = False
        self._is_flipped = False
        self.__grid__ = grid
        self._location = location
        self._direction = 0
        self._animation_speed = 4
        self._animated = False
        self._animations = []
        self._animation = ""
        self._blocked = False
        # Set Actor image
        self._logging.debug("Target-Location:" + str(self.location))
        if img_path is not None:
            self._original_images.append(pygame.image.load(img_path).convert_alpha())
            self._image = self._original_images[0]
            self.add_image(img_path, img_action)
            if img_heading == 'S':
                self._direction = 270
            elif img_heading == 'E':
                self._direction = 0
            elif img_heading == 'W':
                self._direction = 180
            elif img_heading == 'N':
                self._direction = 90
        else:
            self._image=pygame.Surface((20, 20))
            self._image.fill((0, 0, 255))
        self._logging.debug("Actor: " + str(title) + "'s setup wurde ausgeführt"+str(self._is_rotatable))
        grid.add_actor(self, location)
        self.setup()
        self._logging.debug("Actor " + str(title) + " wurde initialisiert")

    def act(self):
        """
        The method should be overwritten in subclasses
        """
        pass

    def add_image(self, img_path: str, img_action="do nothing", data=None):
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self._original_images.append(pygame.image.load(img_path).convert_alpha())
        self._logging.info("Number of Actor images:" + str(self._original_images.__len__()))
        self.__image_transform__(self._original_images.__len__() - 1, img_action, data)
        if self._original_images.__len__() == 1:
            self._image = self._original_images[0]
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))


    def animate(self, animation=""):
        """
        Starts an animation
        :param animation: Type of animation (not implemented)
        """
        if not self._animated:
            self._animation = animation
            self._animated = True

    def stop(self):
        """
        Stops all animations
        """
        self._animated = False

    def next_sprite(self):
        """
        Loads the next sprite in the current animation
        """
        if self._animated:
            if self.__grid__.frame % self._animation_speed == 0:
                self.image_next()

    @property
    def direction(self):
        """ Gets the direction of actor """
        return self._direction

    @direction.setter
    def direction(self, value):
        self._logging.info("Direction set" + str(value))
        self._logging.info("rotated by " + str(value) + " degrees. Is rotatable?: " + str(self._is_rotatable))
        self.__rotate(value)
        self._direction = value

    def __rotate(self, direction):
        if self.is_rotatable:
            self.__grid__.repaint_area(self.bounding_box)
            # rotate the original image to new direction
            self._logging.debug("rotate Image" + str(dir(self._original_images)) + ", Image: " + str(
                            self._image) + "Index:" + str(self._image_index) + ",value:" + str(direction))
            self._image = pygame.transform.rotate(self._original_images[self._image_index], direction)
            self.__grid__.repaint_area(pygame.Rect(self.bounding_box))

    def is_in_grid(self,grid):
        if self.__grid__== grid and grid.is_location_in_grid(self.location):
            return True
        else:
            return False

    def is_blocked(self):
        return self._blocked

    def set_blocked(self):
        self._blocked = True

    def set_unblocked(self):
        self._blocked = False

    def __flip_x__(self):
        """
        Doesn't change status.
        Used for flipping all sprites according to flipped state
        """
        try:
            if not self._is_flipped:
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
                self._logging.debug("Flipping " + self.title + " image number "+str(self._image_index))
                self._image = pygame.transform.flip(self._original_images[self._image_index], False, False)
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
            else:
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
                self._image = pygame.transform.flip(self._original_images[self._image_index], True, False)
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        except IndexError:
            self._logging.warning("Index Error in __flip_x__() in: Image Index is out of bounds")

    def flip_x(self):
        """
        Mirrors image over y-axis. x-Coordinates are flipped.
        Actor is turned by 180 degrees.
        is_rotatable should be False.
        """
        if not self._is_flipped:
            self._is_flipped = True
        else:
            self._is_flipped = False
        self.__flip_x__()
        self.turn_left(180)

    @property
    def image(self):
        """
        Gets the actual image of the actor.
        """
        return self._image

    def listen(self, key, data):
        pass

    def image_next(self):
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        if self._image_index < self._original_images.__len__()-1:
            self._image_index = self._image_index + 1
        else:
            self._image_index = 0
        self._image = self._original_images[self._image_index]
        self.draw()
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self._logging.debug("Actual image:" + str(self._image_index) + "/" + str(self._original_images.__len__() - 1))

    @property
    def is_rotatable(self):
        """ Gets the direction of actor """
        return self._is_rotatable

    def set_rotatable(self):
        self._is_rotatable = True

    def __image_transform__(self, index, img_action, data=None):
        """
        Should be called before main-loop
        """
        cell_size = self.__grid__.cell_size
        if img_action == "scale":
            if data is None:
                self._original_images[self._image_index] = pygame.transform.scale(self._original_images[index], (cell_size, cell_size))
            else:
                self._original_images[self._image_index] = pygame.transform.scale(self._original_images[index], (data[0], data[1]))
        elif img_action == "crop":
            cropped_surface = pygame.Surface()
            cropped_surface.blit(self._original_images[self._image_index], (0, 0),
                                 (0, 0, self.__grid__.grid_width_in_pixels, self.__grid__.grid_height_in_pixels))
            self._original_images[self._image_index] = cropped_surface
        elif img_action == "do_nothing":
            self._original_images[self._image_index] = self._original_images[self._image_index]

    @property
    def bounding_box(self):
        cell_left, cell_top = self.get_image_postion()
        width = self._image.get_width()
        height = self._image.get_height()
        return pygame.Rect(cell_left, cell_top, width, height)

    def get_image_postion(self):
        """
        Gets coordinates of top-left image position
        :return: location (x,y)
        """
        column = self.location[0]
        row = self.location[1]
        cell_margin = self.__grid__.cell_margin
        cell_size = self.__grid__.cell_size
        if self._image.get_width() > cell_size:
            overlapping_x = (self._image.get_width() - cell_size) / 2
        else:
            overlapping_x = 0

        if self._image.get_height() > cell_size:
            overlapping_y = (self._image.get_height() - cell_size) / 2
        else:
            overlapping_y = 0

        cell_left = cell_margin + (cell_margin + cell_size) * column - overlapping_x
        cell_top = cell_margin + (cell_margin + cell_size) * row - overlapping_y
        return cell_left, cell_top

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

    def log(self):
        self._logging = logging.getLogger('Actor:')

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._logging.debug("Location set")
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self._location = value
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self.__grid__.update(act_disabled=True, listen_disabled=True)

    def set_x(self, x):
        self.location[0] = x

    def set_y(self, y):
        self.location[1] = y

    def setup(self):
        pass

    def set_location(self, location):
        self.location = location

    def turn_left(self, degrees=90):
        direction = self.direction + degrees
        if self.direction > 360:
            direction = direction % 360
        self.direction = direction
        self._logging.debug("Richtung:" + str(self.direction))

    def turn_right(self, degrees):
        direction = self.direction - degrees
        if self.direction < 0:
            direction = direction % 360
        self.direction = direction
        self._logging.debug("Richtung:" + str(self.direction))

    def move_to(self, location):
        target = location
        if self.is_valid_move(target):
            self.location = target

    def move(self, distance : int =1):
        target = self.look_forward()
        self._logging.debug("self" + str(self.location) + ", target" + str(target))
        target = self.look_forward(distance)
        if self.is_valid_move(target):
            self.location = target
        self._logging.debug("self" + str(self.location) + ", target" + str(target))


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

    def look_forward(self, distance = 1):
        self._logging.info("Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = round(self.location[0] + math.cos(math.radians(self.direction)) * distance)
        loc_y = round(self.location[1] - math.sin(math.radians(self.direction)) * distance)
        return loc_x, loc_y

    def is_valid_move(self,target : tuple = None):
        valid=False
        if target is None:
            target=self.look_forward()
        # Check if target is in grid
        self._logging.debug("actor.is_valid_move::target:" + str(target))
        if self.__grid__.is_location_in_grid(target):
            valid = True
        else:
            valid = False
        # check if target is not blocked
        actors_at_position = self.__grid__.get_actors_at_location(target)
        for actor in actors_at_position:
            if actor.is_blocked():
                valid=False
        return valid



    def has_image(self):
        if self._image is None or self._original_images.__len__() == 0:
            return False
        else:
            return True

    def mouse_pressed(self,location):
        pass

    def draw(self):
        if self.has_image():
            cell_left, cell_top = self.get_image_postion()
            self.__flip_x__()
            self.__rotate(self.direction)
            pygame.screen.blit(self._image, (cell_left, cell_top))

    def remove_from_grid(self):
        self.__grid__=None