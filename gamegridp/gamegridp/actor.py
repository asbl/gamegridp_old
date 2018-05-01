# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""

import logging
import math
import pygame
import typing

class Actor(object):

    def __init__(self, grid, location : list = (0, 0), color:tuple=(0,0,255), title : str ="Actor", img_path: str =None, size:tuple=(40,40), img_action: str="do_nothing"):
        # define instance variables
        self.title = title
        self._logging = logging.getLogger('Actor:')
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
        self._colliding_partners=[]
        # Set Actor image
        self._logging.debug("actor.__init__() : Target-Location:" + str(self.location))
        self._has_image=False
        if img_path is not None:
            self._has_image = True
            self.add_image(img_path, img_action, size)
        else:
            self._image = pygame.Surface(size)
            self._image.fill(color)
            self._original_images.append(self._image)
        self._logging.debug("actor.__init__() : Actor: " + str(title) + "'s setup wurde ausgeführt" + str(self._is_rotatable))
        grid.add_actor(self, location)
        self.setup()
        self._logging.debug("actor.__init__() : Actor " + str(title) + " wurde initialisiert")

    def act(self):
        """
        The method should be overwritten in subclasses
        """
        pass

    def set_image(self, img_path: str, img_action : str ="do nothing", size=None):
        """
        Adds an single image to an actor, deletes all other images
        :param img_path: The path of the image relative to the actual path
        :param img_action: The image action (scale, do_nothing, crop)
        :param size: scale/crop : Size as 2-Tuple
        """
        self.has_image=False
        self.add_image(img_path, img_action, size)

    def add_image(self, img_path: str, img_action : str ="do nothing", size=None):
        """ adds an image to the actor
        :param img_path: The path of the image relative to the actual path
        :param img_action: The image action (scale, do_nothing, crop)
        :param size: scale/crop : Size as 2-Tuple
        """
        self._logging.info("actor.add_image() : Number of Actor images:" + str(self._original_images.__len__()))
        self._logging.info("Has image" + str(self.has_image))
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        if not self.has_image:
            self._original_images=[]
            self.has_image = True
            self._logging.info("list was cleared:"+str(self._original_images.__len__()))
        self._original_images.append(pygame.image.load(img_path).convert_alpha())
        self._logging.info("actor.add_image() : Number of Actor images:" + str(self._original_images.__len__()))
        self.__image_transform__(self._original_images.__len__() - 1, img_action, size)
        self._logging.info("Actor.add_image:"+str(self._original_images.__len__()))
        if self._original_images.__len__() == 1:
            self.image = self._original_images[0]
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))

    def animate(self, animation : str =""):
        """
        Starts an animation
        :param animation: Type of animation (not implemented)
        """
        if not self._animated:
            self._animation = animation
            self._animated = True

    def add_collision_partner(self, partner):
        self._colliding_partners.append(partner)

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
    def direction(self) -> int:
        """ Gets the direction of actor """
        return self._direction

    @direction.setter
    def direction(self, value : int):
        self._logging.info("actor.rotation() : rotated by " + str(value) + " degrees. Is rotatable?: " + str(self._is_rotatable))
        self.__rotate__(value)
        self._direction = value

    def __rotate__(self, direction : int):
        """
        rotates the actor by _direction_ degrees
        :param direction:
        """
        if self.is_rotatable:
            self.__grid__.repaint_area(self.bounding_box)
            # rotate the original image to new direction
            self._logging.debug("actor.__rotate: rotate Image" + str(dir(self._original_images)) + ", Image: " + str(
                self._image) + "Index:" + str(self._image_index) )
            self.image = pygame.transform.rotate(self._original_images[self._image_index], direction)
            self.__grid__.repaint_area(pygame.Rect(self.bounding_box))

    def is_in_grid(self, grid):
        """
        Checks if the actor is in grid
        :param grid: the grid to check
        :return:
        """
        if self.__grid__ == grid and grid.is_location_in_grid(self.location):
            return True
        else:
            return False

    def is_blocking(self):
        """
        Checks if actor blocks a field for other actors
        :return : true if actor blocks a field
        """
        return self._blocked

    def set_blocked(self):
        """
        Sets the blocked-status of actor. If blocked is true, the field can't be passed by another actor
        """
        self._blocked = True

    def set_unblocked(self):
        """
        Unsets the blocked-status of actor. If blocked is true, the field can't be passed by another actor
        """
        self._blocked = False

    def __flip_x__(self):
        """
        Doesn't change status.
        Used for flipping all sprites according to flipped state
        """
        try:
            if not self._is_flipped:
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
                self._logging.debug("actor.flip_x() : Flipping " + self.title + " image number " + str(self._image_index))
                self.image = pygame.transform.flip(self._original_images[self._image_index], False, False)
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
            else:
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
                self.image = pygame.transform.flip(self._original_images[self._image_index], True, False)
                self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        except IndexError:
            self._logging.warning("actor.flip_x : Index Error in __flip_x__() in: Image Index is out of bounds")

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

    @image.setter
    def image(self, value : str):
        """
        sets the actual image
        :param value: the path to the image
        """
        self._image = value

    def image_next(self):
        """
        switches to the next image by image_index
        """
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        if self._image_index < self._original_images.__len__() - 1:
            self._image_index = self._image_index + 1
        else:
            self._image_index = 0
        self.image = self._original_images[self._image_index]
        self.draw()
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self._logging.debug("actor.image_next() : Image Index:" + str(self._image_index) + "/" + str(self._original_images.__len__() - 1))

    @property
    def is_rotatable(self):
        """
        : return true if actor-image is rotatable, else false
         """
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value : bool):
        """
        sets the actual image
        :param value: the path to the image
        """
        self.__rotatable = value

    def set_rotatable(self):
        """
        Sets the actor-image rotatable.
        """
        self._is_rotatable = True

    def set_text(self,text,size):
        myfont = pygame.font.SysFont("monospace", size)
        label = myfont.render(text, 1, (0, 0, 0))
        self.image.blit(label, (0, 0))
        self._original_images[0]=self._image
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))


    def __image_transform__(self, index : int, img_action : str, data : str =None):
        """
        Should be called before main-loop
        :type data: img_acton : "scale" -> data : location
        """
        cell_size = self.__grid__.cell_size
        if img_action == "scale":
            if data is None:
                self._original_images[self._image_index] = pygame.transform.scale(self._original_images[index],
                                                                                  (cell_size, cell_size))
            else:
                self._original_images[self._image_index] = pygame.transform.scale(self._original_images[index],
                                                                                  (data[0], data[1]))
        elif img_action == "crop":
            cropped_surface = pygame.Surface()
            cropped_surface.blit(self._original_images[self._image_index], (0, 0),
                                 (0, 0, self.__grid__.__grid_width_in_pixels__, self.__grid__.__grid_height_in_pixels__))
            self._original_images[self._image_index] = cropped_surface
        elif img_action == "do_nothing":
            self._original_images[self._image_index] = self._original_images[self._image_index]

    @property
    def bounding_box(self):
        """
        :return: The surrounding Rectangle
        """
        try:
            left, top = self.__get_image_coordinates_in_pixels__()
            width = self._image.get_width()
            height = self._image.get_height()
        except AttributeError:
            left, top, width, height = 0, 0, 0, 0
        return pygame.Rect(left, top, width, height)

    def __get_image_coordinates_in_pixels__(self):
        """
        Gets coordinates of top-left image position
        :return: (x-coordinate, y-coordinate)
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

    def get_neighbour_cells(self) -> list:
        """
        :rtype: all neighbour cells in a list.
        """
        locations = []
        y_pos = self.location[0]
        x_pos = self.location[1]
        locations.append([x_pos + 1, y_pos])
        locations.append([x_pos + 1, y_pos + 1])
        locations.append([x_pos, y_pos + 1])
        locations.append([x_pos - 1, y_pos + 1])
        locations.append([x_pos - 1, y_pos])
        locations.append([x_pos - 1, y_pos - 1])
        locations.append([x_pos, y_pos - 1])
        locations.append([x_pos + 1, y_pos - 1])
        return locations

    def listen(self, key, data):
        """ Should be overwritten in child-classes
        """
        pass

    def get_location(self) -> list:
        """
        Returns the location of actor
        :return: the location as tuple
        """
        return self.location

    @property
    def location(self) -> list:
        """
        returns the location of object
        """
        return self._location

    @location.setter
    def location(self, value : list):
        """
        Sets the location
        :type value: tuple with x and y-coordinate
        """
        self._logging.debug("actor.location: Location set")
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self._location = value
        self.__grid__.repaint_area(pygame.Rect(self.bounding_box))
        self.__grid__.__update__(act_disabled=True, listen_disabled=True, collision_disabled = True)

    def set_x(self, x):
        """
        :param x: the x-coordinate
        """
        self.location[0] = x

    def set_y(self, y):
        """
        :param y: the y-coordinate
        """
        self.location[1] = y

    def get_x(self):
        """
        :param x: the x-coordinate
        """
        return self.location[0]

    def get_y(self):
        """
        :param y: the y-coordinate
        """
        return self.location[1]


    def setup(self):
        """
        Should be overwritten by child-classes
        """
        pass

    def __deprecated_set_location__(self, location):
        """
        sets the location
        deprecated: use location-proberty instead
        :param location:
        :return:
        """
        self.location = location

    def turn_left(self, degrees : int = 90):
        """
        Turns the actor left by x degress
        """
        direction = self.direction + degrees
        if self.direction > 360:
            direction = direction % 360
        self.direction = direction
        self._logging.debug("Richtung:" + str(self.direction))

    def turn_right(self, degrees : int = 90):
        """
        Turns the actor right by x degress
        """
        direction = self.direction - degrees
        if self.direction < 0:
            direction = direction % 360
        self.direction = direction
        self._logging.debug("Richtung:" + str(self.direction))

    def move_to(self, location):
        """
        Moves actor to specific location
        """
        target = location
        if self.is_valid_move(target):
            self.location = target

    def move(self, distance: int = 1):
        """
        Moves actor by x steps
        :param distance : number of steps the actor should step forward.
        """
        target = self.look_forward()
        self._logging.debug("actor.move(): self" + str(self.location) + ", target" + str(target))
        target = self.look_forward(distance)
        if self.is_valid_move(target):
            self.location = target
        self._logging.debug("actor.move(): self" + str(self.location) + ", target" + str(target))

    def move_up(self):
        """
        Moves the actor one step up
        Sets the direction to 90° (North)
        """
        self.direction = 90
        self.move()

    def move_right(self):
        """
        Moves the actor one step right
        Sets the direction to 0° (East)
        """
        self.direction = 0
        self.move()

    def move_left(self):
        """
        Moves the actor one step left
        Sets the direction to 180° (West)
        """
        self.direction = 180
        self.move()

    def move_down(self):
        """
        Moves the actor one step down
        Sets the direction to 170° (South)
        """
        self.direction = 270
        self.move()

    def look_forward(self, distance : int = 1) -> tuple:
        """
        looks x steps forward
        :param distance : Number of steps to look forward
        :return location : Location as tuple (x_cell, y_cell)
        """
        self._logging.info("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = round(self.location[0] + math.cos(math.radians(self.direction)) * distance)
        loc_y = round(self.location[1] - math.sin(math.radians(self.direction)) * distance)
        return loc_x, loc_y

    def is_valid_move(self, target: tuple = None):
        """
        Checks is a move to a specific target is a valid move
        :return true if move is legal, else false
        """
        valid = False
        if target is None:
            target = self.look_forward()
        # Check if target is in grid
        self._logging.debug("actor.is_valid_mode() : target:" + str(target))
        if self.__grid__.is_location_in_grid(target):
            valid = True
        else:
            valid = False
        # check if target is not blocked
        actors_at_position = self.__grid__.get_actors_at_location(target)
        for actor in actors_at_position:
            if actor.is_blocking():
                valid = False
        return valid

    @property
    def has_image(self):
        """
        Checks if actor has an image
        :return: true if actor has an image, else false
        """
        return self._has_image
    @has_image.setter
    def has_image(self, value):
        self._has_image=value

    def draw(self):
        """
        Draws the actor to the grid
        """
        if self.has_image:
            cell_left, cell_top = self.__get_image_coordinates_in_pixels__()
            self.__flip_x__()
            self.__rotate__(self.direction)
            pygame.screen.blit(self._image, (cell_left, cell_top))

    def remove(self):
        """
        removes the actor from grid
        """
        self.__grid__.remove_actor(self)

    def _remove_from_grid(self):
        """
        removes the actor from grid
        """
        self.__grid__ = None